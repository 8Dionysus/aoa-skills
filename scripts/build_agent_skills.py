#!/usr/bin/env python3
"""Build the Codex-facing Agent Skills export and local-adapter manifests.

Wave 2 additions:
- copies optional scripts/, references/, and assets/ from canonical skill folders
- merges optional per-skill OpenAI metadata extensions from config/openai_skill_extensions.json
- regenerates local-adapter manifests that wrap the Codex-facing export
"""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
from typing import Any

import yaml

RESOURCE_DIR_NAMES = ("scripts", "references", "assets")


def titleize_skill_name(name: str) -> str:
    parts = name.split("-")
    out: list[str] = []
    for part in parts:
        if part == "aoa":
            out.append("AoA")
        elif part == "atm10":
            out.append("ATM10")
        elif part == "tdd":
            out.append("TDD")
        elif part == "adr":
            out.append("ADR")
        else:
            out.append(part.capitalize())
    return " ".join(out)


def dump_yaml_frontmatter(data: dict[str, Any]) -> str:
    text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000)
    return f"---\n{text}---\n"


def load_json(path: pathlib.Path, default: Any | None = None) -> Any:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    if default is not None:
        return default
    raise FileNotFoundError(path)


def merge_dict(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_dict(merged[key], value)
        else:
            merged[key] = value
    return merged


def build_markdown(
    skill: dict[str, Any],
    catalog_entry: dict[str, Any],
    override: dict[str, Any],
    compatibility_default: str,
    source_repo: str,
) -> str:
    frontmatter = {
        "name": skill["name"],
        "description": override["description"],
        "license": "Apache-2.0",
        "compatibility": compatibility_default,
        "metadata": {
            "aoa_scope": skill["scope"],
            "aoa_status": skill["status"],
            "aoa_invocation_mode": catalog_entry["invocation_mode"],
            "aoa_source_skill_path": skill["skill_path"],
            "aoa_source_repo": source_repo,
            "aoa_technique_dependencies": ",".join(catalog_entry.get("technique_dependencies", [])),
            "aoa_portable_profile": "codex-facing-wave-2",
        },
    }

    lines = [dump_yaml_frontmatter(frontmatter), f"# {skill['name']}", ""]
    for section in skill["sections"]:
        lines.append(f"## {section['heading']}")
        lines.append(section["content_markdown"].rstrip())
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_openai_yaml(
    skill: dict[str, Any],
    catalog_entry: dict[str, Any],
    override: dict[str, Any],
    extension_doc: dict[str, Any],
) -> dict[str, Any]:
    base_doc: dict[str, Any] = {
        "interface": {
            "display_name": titleize_skill_name(skill["name"]),
            "short_description": override["short_description"],
            "default_prompt": override["default_prompt"],
        },
        "policy": {
            "allow_implicit_invocation": catalog_entry["invocation_mode"] != "explicit-only",
        },
    }

    global_extension = extension_doc.get("global", {})
    per_skill_extension = extension_doc.get("skills", {}).get(skill["name"], {})
    merged = merge_dict(base_doc, global_extension)
    merged = merge_dict(merged, per_skill_extension)

    # Canonical invocation policy wins over extension attempts.
    merged.setdefault("policy", {})
    merged["policy"]["allow_implicit_invocation"] = catalog_entry["invocation_mode"] != "explicit-only"

    # Omit empty dependencies/tools blocks for cleaner output.
    if merged.get("dependencies", {}).get("tools") == []:
        dependencies = dict(merged["dependencies"])
        dependencies.pop("tools", None)
        if dependencies:
            merged["dependencies"] = dependencies
        else:
            merged.pop("dependencies", None)
    return merged


def copy_optional_resources(source_skill_dir: pathlib.Path, target_skill_dir: pathlib.Path) -> dict[str, list[str]]:
    inventory: dict[str, list[str]] = {name: [] for name in RESOURCE_DIR_NAMES}
    for resource_dir_name in RESOURCE_DIR_NAMES:
        source_dir = source_skill_dir / resource_dir_name
        target_dir = target_skill_dir / resource_dir_name
        if not source_dir.exists():
            continue
        shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
        inventory[resource_dir_name] = sorted(
            str(path.relative_to(target_dir).as_posix())
            for path in target_dir.rglob("*")
            if path.is_file()
        )
    return inventory


def build_local_adapter_manifests(
    *,
    repo_root: pathlib.Path,
    skills_root: pathlib.Path,
    catalog_full: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = {
        "manifest_version": 1,
        "profile": "codex-facing-local-adapter",
        "root": str(skills_root.relative_to(repo_root).as_posix()),
        "activation_tool": "scripts/activate_skill.py",
        "discovery_view": "generated/local_adapter_manifest.min.json",
        "permission_allowlist": [str(skills_root.relative_to(repo_root).as_posix())],
        "source_of_truth": {
            "portable_export_root": str(skills_root.relative_to(repo_root).as_posix()),
            "portable_catalog": "generated/agent_skill_catalog.json",
            "policy_source": "agents/openai.yaml",
        },
        "skills": [],
    }
    manifest_min = {
        "manifest_version": 1,
        "profile": "codex-facing-local-adapter",
        "root": str(skills_root.relative_to(repo_root).as_posix()),
        "activation_tool": "scripts/activate_skill.py",
        "skills": [],
    }

    for entry in catalog_full["skills"]:
        skill_md_path = repo_root / entry["path"]
        frontmatter, _ = parse_frontmatter(skill_md_path)
        manifest["skills"].append(
            {
                "name": entry["name"],
                "description": entry["description"],
                "path": entry["path"],
                "openai_config_path": entry["openai_config_path"],
                "allow_implicit_invocation": entry["allow_implicit_invocation"],
                "invocation_mode": entry["invocation_mode"],
                "allowlist_paths": [str((skills_root / entry["name"]).relative_to(repo_root).as_posix())],
                "resource_inventory": entry.get("resource_inventory", {}),
                "metadata": frontmatter.get("metadata", {}),
            }
        )
        manifest_min["skills"].append(
            {
                "name": entry["name"],
                "description": entry["description"],
                "path": entry["path"],
                "allow_implicit_invocation": entry["allow_implicit_invocation"],
            }
        )
    return manifest, manifest_min


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Path to target aoa-skills repository root")
    parser.add_argument(
        "--output-root",
        default=None,
        help="Optional override for where to write the portable layer. Defaults to <repo-root>/.agents/skills",
    )
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    sections_path = repo_root / "generated" / "skill_sections.full.json"
    catalog_path = repo_root / "generated" / "skill_catalog.min.json"
    overrides_path = repo_root / "config" / "portable_skill_overrides.json"
    extensions_path = repo_root / "config" / "openai_skill_extensions.json"

    skill_sections = load_json(sections_path)
    skill_catalog = load_json(catalog_path)
    overrides_doc = load_json(overrides_path)
    extensions_doc = load_json(
        extensions_path,
        default={"schema_version": 1, "global": {"interface": {}}, "skills": {}},
    )

    catalog_by_name = {entry["name"]: entry for entry in skill_catalog["skills"]}
    overrides = overrides_doc["skills"]
    compatibility_default = overrides_doc["compatibility_default"]
    source_repo = "8Dionysus/aoa-skills"

    skills_root = pathlib.Path(args.output_root).resolve() if args.output_root else repo_root / ".agents" / "skills"
    if skills_root.exists():
        shutil.rmtree(skills_root)
    skills_root.mkdir(parents=True)

    catalog_full: dict[str, Any] = {
        "catalog_version": 2,
        "profile": "codex-facing-agent-skills-wave-2",
        "root": str(skills_root.relative_to(repo_root).as_posix()),
        "source_repo": source_repo,
        "source_of_truth": {
            "skill_sections": "generated/skill_sections.full.json",
            "skill_catalog": "generated/skill_catalog.min.json",
            "portable_overrides": "config/portable_skill_overrides.json",
            "openai_extensions": "config/openai_skill_extensions.json",
        },
        "skills": [],
    }
    catalog_min: dict[str, Any] = {
        "catalog_version": 2,
        "profile": "codex-facing-agent-skills-wave-2",
        "root": str(skills_root.relative_to(repo_root).as_posix()),
        "skills": [],
    }
    export_map: dict[str, Any] = {
        "export_version": 2,
        "profile": "codex-facing-agent-skills-wave-2",
        "root": str(skills_root.relative_to(repo_root).as_posix()),
        "source_repo": source_repo,
        "source_of_truth": {
            "skill_sections": "generated/skill_sections.full.json",
            "skill_catalog": "generated/skill_catalog.min.json",
            "portable_overrides": "config/portable_skill_overrides.json",
            "openai_extensions": "config/openai_skill_extensions.json",
        },
        "exports": [],
    }

    for skill in skill_sections["skills"]:
        catalog_entry = catalog_by_name[skill["name"]]
        override = overrides[skill["name"]]
        skill_dir = skills_root / skill["name"]
        agents_dir = skill_dir / "agents"
        agents_dir.mkdir(parents=True)

        skill_md_path = skill_dir / "SKILL.md"
        skill_md_path.write_text(
            build_markdown(skill, catalog_entry, override, compatibility_default, source_repo),
            encoding="utf-8",
        )

        openai_doc = build_openai_yaml(skill, catalog_entry, override, extensions_doc)
        (agents_dir / "openai.yaml").write_text(
            yaml.safe_dump(openai_doc, sort_keys=False, allow_unicode=True, width=1000),
            encoding="utf-8",
        )

        source_skill_path = repo_root / skill["skill_path"]
        source_skill_dir = source_skill_path.parent
        resource_inventory = copy_optional_resources(source_skill_dir, skill_dir)

        allow_implicit = catalog_entry["invocation_mode"] != "explicit-only"
        dependencies = openai_doc.get("dependencies", {})
        dependency_tools = dependencies.get("tools", []) if isinstance(dependencies, dict) else []

        catalog_full["skills"].append(
            {
                "name": skill["name"],
                "display_name": titleize_skill_name(skill["name"]),
                "description": override["description"],
                "short_description": override["short_description"],
                "path": str(skill_md_path.relative_to(repo_root).as_posix()),
                "openai_config_path": str((agents_dir / "openai.yaml").relative_to(repo_root).as_posix()),
                "scope": skill["scope"],
                "status": skill["status"],
                "invocation_mode": catalog_entry["invocation_mode"],
                "allow_implicit_invocation": allow_implicit,
                "source_skill_path": skill["skill_path"],
                "technique_dependencies": catalog_entry.get("technique_dependencies", []),
                "resource_inventory": resource_inventory,
                "dependency_tools": dependency_tools,
            }
        )
        catalog_min["skills"].append(
            {
                "name": skill["name"],
                "description": override["description"],
                "path": str(skill_md_path.relative_to(repo_root).as_posix()),
                "allow_implicit_invocation": allow_implicit,
            }
        )
        export_map["exports"].append(
            {
                "name": skill["name"],
                "source_skill_path": skill["skill_path"],
                "target_dir": str(skill_dir.relative_to(repo_root).as_posix()),
                "target_skill_path": str(skill_md_path.relative_to(repo_root).as_posix()),
                "target_openai_config_path": str((agents_dir / "openai.yaml").relative_to(repo_root).as_posix()),
                "copied_resource_dirs": [kind for kind, files in resource_inventory.items() if files],
                "invocation_mode": catalog_entry["invocation_mode"],
                "allow_implicit_invocation": allow_implicit,
            }
        )

    generated_dir = repo_root / "generated"
    generated_dir.mkdir(exist_ok=True)

    local_manifest, local_manifest_min = build_local_adapter_manifests(
        repo_root=repo_root,
        skills_root=skills_root,
        catalog_full=catalog_full,
    )

    (generated_dir / "agent_skill_catalog.json").write_text(json.dumps(catalog_full, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "agent_skill_catalog.min.json").write_text(json.dumps(catalog_min, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "portable_export_map.json").write_text(json.dumps(export_map, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "local_adapter_manifest.json").write_text(json.dumps(local_manifest, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "local_adapter_manifest.min.json").write_text(json.dumps(local_manifest_min, indent=2) + "\n", encoding="utf-8")
    print(f"built {len(catalog_full['skills'])} skills into {skills_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
