#!/usr/bin/env python3
"""Validate full Codex-facing openai.yaml files against workspace MCP config."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import tomllib
import yaml


@dataclass
class SkillReport:
    skill_name: str
    path: str
    implicit_invocation: bool | None
    mcp_dependencies: list[str]
    errors: list[str]
    warnings: list[str]


def load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML object")
    return data


def discover_skill_name(path: Path) -> str:
    parts = path.parts
    if len(parts) >= 3 and parts[-2] == "agents" and parts[-1] == "openai.yaml":
        return parts[-3]
    name = path.name
    if name.startswith("openai.") and name.endswith(".example.yaml"):
        return name[len("openai.") : -len(".example.yaml")]
    return path.stem


def extract_configured_mcp_names(config: dict[str, Any]) -> set[str]:
    mcp_servers = config.get("mcp_servers", {})
    if isinstance(mcp_servers, dict):
        return set(mcp_servers.keys())
    return set()


def load_manifest_entries(path: Path | None) -> dict[str, bool]:
    if path is None or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    entries: dict[str, bool] = {}

    def add_entry(item: dict[str, Any]) -> None:
        name = item.get("name")
        value = item.get("allow_implicit_invocation")
        if isinstance(name, str) and isinstance(value, bool):
            entries[name] = value

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                add_entry(item)
    elif isinstance(data, dict):
        skills = data.get("skills")
        if isinstance(skills, list):
            for item in skills:
                if isinstance(item, dict):
                    add_entry(item)
        else:
            for key, value in data.items():
                if isinstance(value, dict) and "allow_implicit_invocation" in value:
                    add_entry(
                        {
                            "name": value.get("name", key),
                            "allow_implicit_invocation": value.get(
                                "allow_implicit_invocation"
                            ),
                        }
                    )
    return entries


def extract_mcp_dependencies(
    payload: dict[str, Any],
    *,
    configured_mcp_names: set[str],
    allow_missing_mcp: bool,
    errors: list[str],
    warnings: list[str],
) -> list[str]:
    mcp_dependencies: list[str] = []
    dependencies = payload.get("dependencies")
    if dependencies is None:
        warnings.append("no dependencies section")
        return mcp_dependencies
    if not isinstance(dependencies, dict):
        errors.append("dependencies must be a mapping")
        return mcp_dependencies

    tools = dependencies.get("tools", [])
    if tools is None:
        warnings.append("no dependencies.tools section")
        return mcp_dependencies
    if not isinstance(tools, list):
        errors.append("dependencies.tools must be a list when present")
        return mcp_dependencies

    for idx, tool in enumerate(tools):
        if not isinstance(tool, dict):
            errors.append(f"dependencies.tools[{idx}] must be a mapping")
            continue
        tool_type = tool.get("type")
        if not isinstance(tool_type, str) or not tool_type.strip():
            errors.append(f"dependencies.tools[{idx}].type must be a non-empty string")
            continue
        if tool_type != "mcp":
            continue
        name = tool.get("value")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"dependencies.tools[{idx}].value must be a non-empty string")
            continue
        mcp_dependencies.append(name)
        if not allow_missing_mcp and name not in configured_mcp_names:
            errors.append(f"unknown MCP dependency: {name}")

    if not mcp_dependencies:
        warnings.append("no MCP dependencies declared")
    return mcp_dependencies


def validate_skill_file(
    path: Path,
    *,
    configured_mcp_names: set[str],
    manifest_entries: dict[str, bool],
    allow_missing_mcp: bool,
) -> SkillReport:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        payload = load_yaml(path)
    except Exception as exc:  # noqa: BLE001
        return SkillReport(
            skill_name=discover_skill_name(path),
            path=str(path),
            implicit_invocation=None,
            mcp_dependencies=[],
            errors=[str(exc)],
            warnings=[],
        )

    interface = payload.get("interface")
    if interface is None:
        warnings.append("missing interface section")
    elif not isinstance(interface, dict):
        errors.append("interface must be a mapping")
    else:
        if not interface.get("display_name"):
            warnings.append("missing interface.display_name")
        if not interface.get("short_description"):
            warnings.append("missing interface.short_description")
        if not interface.get("default_prompt"):
            warnings.append("missing interface.default_prompt")

    policy = payload.get("policy")
    implicit_value: bool | None = None
    if not isinstance(policy, dict) or "allow_implicit_invocation" not in policy:
        errors.append("missing policy.allow_implicit_invocation")
    else:
        implicit_value = policy.get("allow_implicit_invocation")
        if not isinstance(implicit_value, bool):
            errors.append("policy.allow_implicit_invocation must be boolean")

    mcp_dependencies = extract_mcp_dependencies(
        payload,
        configured_mcp_names=configured_mcp_names,
        allow_missing_mcp=allow_missing_mcp,
        errors=errors,
        warnings=warnings,
    )

    skill_name = discover_skill_name(path)
    manifest_value = manifest_entries.get(skill_name)
    if (
        manifest_value is not None
        and implicit_value is not None
        and manifest_value != implicit_value
    ):
        errors.append(
            "allow_implicit_invocation mismatch against local adapter manifest "
            f"(manifest={manifest_value}, openai.yaml={implicit_value})"
        )

    return SkillReport(
        skill_name=skill_name,
        path=str(path),
        implicit_invocation=implicit_value,
        mcp_dependencies=mcp_dependencies,
        errors=errors,
        warnings=warnings,
    )


def collect_paths(repo_root: Path, explicit_paths: list[Path]) -> list[Path]:
    if explicit_paths:
        return explicit_paths
    discovered = list((repo_root / ".agents" / "skills").glob("*/agents/openai.yaml"))
    discovered.extend((repo_root / "examples").glob("openai.*.example.yaml"))
    return sorted(set(discovered))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."), help="Root of aoa-skills")
    parser.add_argument(
        "--workspace-config",
        type=Path,
        required=True,
        help="Workspace .codex/config.toml",
    )
    parser.add_argument(
        "--local-adapter-manifest",
        type=Path,
        default=None,
        help="Path to generated/local_adapter_manifest.min.json",
    )
    parser.add_argument(
        "--paths",
        type=Path,
        nargs="*",
        default=[],
        help="Explicit full openai.yaml files to validate",
    )
    parser.add_argument(
        "--allow-missing-mcp",
        action="store_true",
        help="Allow MCP dependency names missing from workspace config",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    workspace_config = args.workspace_config.resolve()
    manifest_path = args.local_adapter_manifest
    if manifest_path is None:
        default_manifest = repo_root / "generated" / "local_adapter_manifest.min.json"
        manifest_path = default_manifest if default_manifest.exists() else None

    config = load_toml(workspace_config)
    configured_mcp_names = extract_configured_mcp_names(config)
    manifest_entries = load_manifest_entries(manifest_path)
    paths = collect_paths(repo_root, [path.resolve() for path in args.paths])

    reports = [
        validate_skill_file(
            path,
            configured_mcp_names=configured_mcp_names,
            manifest_entries=manifest_entries,
            allow_missing_mcp=args.allow_missing_mcp,
        )
        for path in paths
    ]
    ok = bool(paths) and all(not report.errors for report in reports)

    if args.format == "json":
        payload = {
            "ok": ok,
            "configured_mcp_servers": sorted(configured_mcp_names),
            "skills": [asdict(report) for report in reports],
            "path_count": len(paths),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"Configured MCP servers: {', '.join(sorted(configured_mcp_names)) or '(none)'}")
        print(f"Paths checked: {len(paths)}")
        for report in reports:
            print(f"\n[{report.skill_name}] {report.path}")
            print(f"  implicit_invocation: {report.implicit_invocation}")
            print(f"  mcp_dependencies: {', '.join(report.mcp_dependencies) or '(none)'}")
            for warning in report.warnings:
                print(f"  warning: {warning}")
            for error in report.errors:
                print(f"  error: {error}")
        if not paths:
            print("\nResult: FAILED")
            print("  error: no full openai.yaml files found to validate")
        else:
            print(f"\nResult: {'OK' if ok else 'FAILED'}")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
