#!/usr/bin/env python3
"""Validate the Codex-facing Agent Skills export and its local-adapter metadata."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any

import yaml

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(path: pathlib.Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter start")
    try:
        _, fm_text, body = text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError(f"{path}: invalid frontmatter fence structure") from exc
    data = yaml.safe_load(fm_text) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter must parse to a mapping")
    return data, body


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root containing .agents/skills")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    skills_root = repo_root / ".agents" / "skills"
    generated_dir = repo_root / "generated"
    errors: list[str] = []

    catalog_by_name: dict[str, dict[str, Any]] = {}
    manifest_by_name: dict[str, dict[str, Any]] = {}

    catalog_path = generated_dir / "skill_catalog.min.json"
    if catalog_path.exists():
        try:
            source_catalog = load_json(catalog_path)
            catalog_by_name = {entry["name"]: entry for entry in source_catalog.get("skills", [])}
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{catalog_path}: invalid JSON: {exc}")

    local_manifest_path = generated_dir / "local_adapter_manifest.json"
    if local_manifest_path.exists():
        try:
            local_manifest = load_json(local_manifest_path)
            manifest_by_name = {entry["name"]: entry for entry in local_manifest.get("skills", [])}
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{local_manifest_path}: invalid JSON: {exc}")

    if not skills_root.exists():
        errors.append(f"missing skills root: {skills_root}")
    else:
        skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())
        for skill_dir in skill_dirs:
            skill_md = skill_dir / "SKILL.md"
            openai_yaml = skill_dir / "agents" / "openai.yaml"

            if not skill_md.exists():
                errors.append(f"{skill_dir}: missing SKILL.md")
                continue
            if not openai_yaml.exists():
                errors.append(f"{skill_dir}: missing agents/openai.yaml")
                continue

            try:
                frontmatter, body = parse_frontmatter(skill_md)
            except Exception as exc:  # noqa: BLE001
                errors.append(str(exc))
                continue

            name = frontmatter.get("name")
            description = frontmatter.get("description")
            metadata = frontmatter.get("metadata")

            if name != skill_dir.name:
                errors.append(f"{skill_md}: frontmatter name {name!r} does not match directory {skill_dir.name!r}")
            if not isinstance(name, str) or not NAME_RE.match(name):
                errors.append(f"{skill_md}: invalid skill name {name!r}")
            if not isinstance(description, str) or not description.strip():
                errors.append(f"{skill_md}: missing or empty description")
            else:
                if len(description) > 1024:
                    errors.append(f"{skill_md}: description exceeds 1024 characters")
                if "Use when" not in description:
                    errors.append(f"{skill_md}: description should include 'Use when' for trigger clarity")
                if "Do not use" not in description:
                    errors.append(f"{skill_md}: description should include 'Do not use' for boundary clarity")

            if not isinstance(metadata, dict):
                errors.append(f"{skill_md}: metadata must be a mapping")
            else:
                for key, value in metadata.items():
                    if not isinstance(key, str) or not isinstance(value, str):
                        errors.append(f"{skill_md}: metadata keys and values must be strings")
                        break

            if not body.strip():
                errors.append(f"{skill_md}: markdown body is empty")

            try:
                openai_doc = yaml.safe_load(openai_yaml.read_text(encoding="utf-8")) or {}
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{openai_yaml}: invalid YAML: {exc}")
                continue

            if not isinstance(openai_doc, dict):
                errors.append(f"{openai_yaml}: top-level YAML must be a mapping")
                continue

            interface = openai_doc.get("interface")
            if not isinstance(interface, dict):
                errors.append(f"{openai_yaml}: interface must be a mapping")
                interface = {}

            short_description = interface.get("short_description")
            default_prompt = interface.get("default_prompt")
            if not isinstance(short_description, str) or not short_description.strip():
                errors.append(f"{openai_yaml}: interface.short_description must be a non-empty string")
            if not isinstance(default_prompt, str) or f"${skill_dir.name}" not in default_prompt:
                errors.append(f"{openai_yaml}: interface.default_prompt must mention ${skill_dir.name}")

            policy = openai_doc.get("policy")
            if not isinstance(policy, dict):
                errors.append(f"{openai_yaml}: policy must be a mapping")
                policy = {}
            allow_implicit = policy.get("allow_implicit_invocation")
            if not isinstance(allow_implicit, bool):
                errors.append(f"{openai_yaml}: policy.allow_implicit_invocation must be a boolean")

            source_entry = catalog_by_name.get(skill_dir.name)
            if source_entry is not None and isinstance(allow_implicit, bool):
                expected_allow = source_entry.get("invocation_mode") != "explicit-only"
                if allow_implicit != expected_allow:
                    errors.append(
                        f"{openai_yaml}: policy.allow_implicit_invocation={allow_implicit} "
                        f"does not match canonical invocation_mode={source_entry.get('invocation_mode')!r}"
                    )

            dependencies = openai_doc.get("dependencies", {})
            if dependencies is not None:
                if not isinstance(dependencies, dict):
                    errors.append(f"{openai_yaml}: dependencies must be a mapping when present")
                else:
                    tools = dependencies.get("tools", [])
                    if tools is not None:
                        if not isinstance(tools, list):
                            errors.append(f"{openai_yaml}: dependencies.tools must be a list when present")
                        else:
                            for idx, tool in enumerate(tools):
                                if not isinstance(tool, dict):
                                    errors.append(f"{openai_yaml}: dependencies.tools[{idx}] must be a mapping")
                                    break
                                if not isinstance(tool.get("type"), str) or not tool["type"].strip():
                                    errors.append(f"{openai_yaml}: dependencies.tools[{idx}].type must be a non-empty string")
                                if not isinstance(tool.get("value"), str) or not tool["value"].strip():
                                    errors.append(f"{openai_yaml}: dependencies.tools[{idx}].value must be a non-empty string")

            manifest_entry = manifest_by_name.get(skill_dir.name)
            if manifest_entry is not None:
                manifest_path = repo_root / manifest_entry["path"]
                if manifest_path != skill_md:
                    errors.append(
                        f"{local_manifest_path}: {skill_dir.name} path {manifest_entry['path']!r} "
                        f"does not point to {skill_md.relative_to(repo_root).as_posix()!r}"
                    )
                if manifest_entry.get("allow_implicit_invocation") != allow_implicit:
                    errors.append(
                        f"{local_manifest_path}: {skill_dir.name} allow_implicit_invocation mismatch "
                        f"({manifest_entry.get('allow_implicit_invocation')!r} vs {allow_implicit!r})"
                    )
                for allowlist_path in manifest_entry.get("allowlist_paths", []):
                    full_path = repo_root / allowlist_path
                    if not full_path.exists():
                        errors.append(f"{local_manifest_path}: allowlist path does not exist: {allowlist_path}")

        if local_manifest_path.exists():
            actual_names = {path.name for path in skill_dirs}
            manifest_names = set(manifest_by_name)
            if actual_names != manifest_names:
                errors.append(
                    f"{local_manifest_path}: manifest skill set {sorted(manifest_names)!r} does not match export skill set {sorted(actual_names)!r}"
                )

        if not errors:
            print(f"validated {len(skill_dirs)} skills in {skills_root}")
            return 0

    for error in errors:
        print(error, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
