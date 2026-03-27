#!/usr/bin/env python3
"""Build the cumulative Codex-facing Agent Skills export and support artifacts."""

from __future__ import annotations

import argparse
import copy
import json
import pathlib
import re
import shutil
from typing import Any

import yaml

RESOURCE_DIR_NAMES = ("scripts", "references", "assets")
STANDARD_INSTALL_ROOTS = {
    "repo": ".agents/skills",
    "user": "$HOME/.agents/skills",
    "admin": "/etc/codex/skills",
}
SCOPE_UI_DEFAULTS = {
    "core": {
        "brand_color": "#2563EB",
        "accent": "#2563EB",
        "scope_icon": "core",
    },
    "risk": {
        "brand_color": "#B45309",
        "accent": "#B45309",
        "scope_icon": "risk",
    },
    "project": {
        "brand_color": "#6D28D9",
        "accent": "#6D28D9",
        "scope_icon": "project",
    },
}
EXPORT_PROFILE = "codex-facing-wave-3"
GENERATED_PORTABLE_FILES = [
    "generated/agent_skill_catalog.json",
    "generated/agent_skill_catalog.min.json",
    "generated/portable_export_map.json",
    "generated/local_adapter_manifest.json",
    "generated/local_adapter_manifest.min.json",
    "generated/skill_handoff_contracts.json",
    "generated/context_retention_manifest.json",
    "generated/trust_policy_matrix.json",
    "generated/skill_runtime_contracts.json",
    "generated/skill_pack_profiles.resolved.json",
    "generated/codex_config_snippets.json",
    "generated/mcp_dependency_manifest.json",
    "generated/runtime_discovery_index.json",
    "generated/runtime_discovery_index.min.json",
    "generated/runtime_disclosure_index.json",
    "generated/runtime_activation_aliases.json",
    "generated/runtime_tool_schemas.json",
    "generated/runtime_session_contract.json",
    "generated/runtime_prompt_blocks.json",
    "generated/runtime_router_hints.json",
    "generated/runtime_seam_manifest.json",
    "generated/release_manifest.json",
]


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
        return copy.deepcopy(default)
    raise FileNotFoundError(path)


def merge_dict(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_dict(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


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


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


TOKEN_RE = re.compile(r"[a-z0-9]+")


def slugify(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    value = re.sub(r"-+", "-", value)
    return value or "artifact"


def unique_preserve(items: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def artifact_tags(items: list[str], limit: int = 8) -> list[str]:
    tags = [slugify(item)[:64] for item in items if item]
    tags = [tag for tag in tags if tag]
    return unique_preserve(tags)[:limit]


def section_map(skill: dict[str, Any]) -> dict[str, str]:
    return {section["heading"]: section["content_markdown"] for section in skill["sections"]}


def extract_bullets(markdown: str, limit: int | None = 3) -> list[str]:
    items: list[str] = []
    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- "):
            items.append(normalize_space(line[2:]))
        elif line[:2].isdigit() and ". " in line[:4]:
            items.append(normalize_space(line.split(". ", 1)[1]))
        elif line[:1].isdigit() and ". " in line[:3]:
            items.append(normalize_space(line.split(". ", 1)[1]))
        if limit is not None and len(items) >= limit:
            break
    return items


def scope_defaults(scope: str) -> dict[str, str]:
    return SCOPE_UI_DEFAULTS.get(scope, SCOPE_UI_DEFAULTS["core"])


def skill_svg(scope: str, size: int) -> str:
    ui = scope_defaults(scope)
    accent = ui["accent"]
    if ui["scope_icon"] == "risk":
        shape = """
  <path d="M32 14 L50 46 H14 Z" fill="none" stroke="white" stroke-width="4" stroke-linejoin="round"/>
  <path d="M32 24 V35" stroke="white" stroke-width="4" stroke-linecap="round"/>
  <circle cx="32" cy="42" r="2.8" fill="white"/>
"""
    elif ui["scope_icon"] == "project":
        shape = """
  <rect x="16" y="18" width="24" height="24" rx="5" fill="none" stroke="white" stroke-width="4"/>
  <rect x="24" y="24" width="24" height="24" rx="5" fill="none" stroke="white" stroke-width="4" opacity="0.95"/>
"""
    else:
        shape = """
  <path d="M18 23 H46" stroke="white" stroke-width="4" stroke-linecap="round"/>
  <path d="M18 32 H46" stroke="white" stroke-width="4" stroke-linecap="round" opacity="0.95"/>
  <path d="M18 41 H38" stroke="white" stroke-width="4" stroke-linecap="round" opacity="0.9"/>
"""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="{size}" '
        f'height="{size}" fill="none" role="img" aria-label="{scope} skill icon">\n'
        f'  <rect x="4" y="4" width="56" height="56" rx="14" fill="{accent}"/>\n'
        f"{shape.strip()}\n"
        "</svg>\n"
    )


def ensure_scope_assets(skill_dir: pathlib.Path, scope: str) -> dict[str, str]:
    assets_dir = skill_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    small_path = assets_dir / "small-logo.svg"
    large_path = assets_dir / "large-logo.svg"
    if not small_path.exists():
        small_path.write_text(skill_svg(scope, 32), encoding="utf-8")
    if not large_path.exists():
        large_path.write_text(skill_svg(scope, 128), encoding="utf-8")
    return {
        "icon_small": "./assets/small-logo.svg",
        "icon_large": "./assets/large-logo.svg",
    }


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
            "aoa_portable_profile": EXPORT_PROFILE,
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
    icon_paths: dict[str, str],
) -> dict[str, Any]:
    ui = scope_defaults(skill["scope"])
    base_doc: dict[str, Any] = {
        "interface": {
            "display_name": titleize_skill_name(skill["name"]),
            "short_description": override["short_description"],
            "default_prompt": override["default_prompt"],
            "icon_small": icon_paths["icon_small"],
            "icon_large": icon_paths["icon_large"],
            "brand_color": ui["brand_color"],
        },
        "policy": {
            "allow_implicit_invocation": catalog_entry["invocation_mode"] != "explicit-only",
        },
    }

    global_extension = extension_doc.get("global", {})
    per_skill_extension = extension_doc.get("skills", {}).get(skill["name"], {})
    merged = merge_dict(base_doc, global_extension)
    merged = merge_dict(merged, per_skill_extension)

    merged.setdefault("policy", {})
    merged["policy"]["allow_implicit_invocation"] = catalog_entry["invocation_mode"] != "explicit-only"

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
        if source_dir.exists():
            shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
        if target_dir.exists():
            inventory[resource_dir_name] = sorted(
                str(path.relative_to(target_skill_dir).as_posix())
                for path in target_dir.rglob("*")
                if path.is_file()
            )
    return inventory


def build_context_entry(
    skill: dict[str, Any],
    override: dict[str, Any],
    policy_entry: dict[str, Any],
) -> dict[str, Any]:
    section_by_heading = {section["heading"]: section["content_markdown"] for section in skill["sections"]}
    must_keep = (
        extract_bullets(section_by_heading.get("Inputs", ""), limit=2)
        + extract_bullets(section_by_heading.get("Outputs", ""), limit=2)
    )
    if not must_keep:
        must_keep = extract_bullets(section_by_heading.get("Procedure", ""), limit=4)
    keep_text = ", ".join(must_keep) if must_keep else override["short_description"]
    return {
        "name": skill["name"],
        "compact_summary": override["short_description"],
        "activation_card_markdown": (
            f"Use when: {override['description']}\n\n"
            f"Keep in memory: {keep_text}.\n\n"
            "If the skill drops out of context, reload Trigger boundary, Procedure, and Verification from SKILL.md."
        ),
        "must_keep": must_keep,
        "retain_sections": ["Trigger boundary", "Procedure", "Verification"],
        "metadata_keys": ["aoa_scope", "aoa_status", "aoa_invocation_mode"],
        "rehydration_hint": (
            "Reload the full SKILL.md and keep policy, procedure, and verification in active context before resuming."
        ),
        "requires_confirmation_seam": bool(policy_entry.get("requires_confirmation_seam")),
    }


def build_trust_entry(
    skill: dict[str, Any],
    catalog_entry: dict[str, Any],
    policy_entry: dict[str, Any],
) -> dict[str, Any]:
    return {
        "name": skill["name"],
        "scope": skill["scope"],
        "invocation_mode": catalog_entry["invocation_mode"],
        "trust_posture": policy_entry["trust_posture"],
        "mutation_surface": policy_entry["mutation_surface"],
        "requires_manual_invocation": catalog_entry["invocation_mode"] == "explicit-only",
        "requires_confirmation_seam": bool(policy_entry.get("requires_confirmation_seam")),
        "recommended_install_scopes": policy_entry["recommended_install_scopes"],
        "notes": policy_entry["notes"],
    }


def build_runtime_entry(
    *,
    skill: dict[str, Any],
    catalog_entry: dict[str, Any],
    override: dict[str, Any],
    openai_doc: dict[str, Any],
    inventory: dict[str, list[str]],
    policy_entry: dict[str, Any],
) -> dict[str, Any]:
    return {
        "name": skill["name"],
        "display_name": titleize_skill_name(skill["name"]),
        "description": override["description"],
        "short_description": override["short_description"],
        "path": f".agents/skills/{skill['name']}/SKILL.md",
        "openai_config_path": f".agents/skills/{skill['name']}/agents/openai.yaml",
        "invocation_mode": catalog_entry["invocation_mode"],
        "allow_implicit_invocation": openai_doc.get("policy", {}).get("allow_implicit_invocation"),
        "trust_posture": policy_entry["trust_posture"],
        "mutation_surface": policy_entry["mutation_surface"],
        "requires_confirmation_seam": bool(policy_entry.get("requires_confirmation_seam")),
        "recommended_install_scopes": policy_entry["recommended_install_scopes"],
        "default_prompt": openai_doc.get("interface", {}).get("default_prompt"),
        "resource_inventory": inventory,
        "context_retention_ref": f"generated/context_retention_manifest.json#{skill['name']}",
        "notes": policy_entry["notes"],
    }


def build_handoff_entry(
    *,
    skill: dict[str, Any],
    catalog_entry: dict[str, Any],
    override: dict[str, Any],
) -> dict[str, Any]:
    sections = section_map(skill)
    inputs = extract_bullets(sections.get("Inputs", ""), limit=None)
    outputs = extract_bullets(sections.get("Outputs", ""), limit=None)
    verification = extract_bullets(sections.get("Verification", ""), limit=None)
    contracts = extract_bullets(sections.get("Contracts", ""), limit=None)
    consumes = artifact_tags(inputs)
    provides = artifact_tags(outputs)
    return {
        "name": skill["name"],
        "display_name": titleize_skill_name(skill["name"]),
        "description": override["description"],
        "invocation_mode": catalog_entry["invocation_mode"],
        "inputs": inputs,
        "outputs": outputs,
        "verification": verification,
        "contracts": contracts,
        "consumes_artifact_tags": consumes,
        "provides_artifact_tags": provides,
        "handoff_packet_template": {
            "from_skill": skill["name"],
            "produced_artifacts": provides,
            "verification_notes": verification[:3],
            "contract_notes": contracts[:3],
            "next_recommended_skills": [],
        },
    }


def resolve_pack_profiles(
    profiles_doc: dict[str, Any],
    catalog_full: dict[str, Any],
) -> dict[str, Any]:
    skills_by_name = {entry["name"]: entry for entry in catalog_full["skills"]}
    resolved = {
        "schema_version": 1,
        "profile": EXPORT_PROFILE,
        "source_config": "config/skill_pack_profiles.json",
        "profiles": {},
    }
    for profile_name, profile in profiles_doc.get("profiles", {}).items():
        scope = profile["scope"]
        install_root = STANDARD_INSTALL_ROOTS[scope]
        entries = []
        for skill_name in profile["skills"]:
            skill_entry = skills_by_name[skill_name]
            target_root = f"{install_root}/{skill_name}"
            entries.append(
                {
                    "name": skill_name,
                    "source_path": skill_entry["path"],
                    "target_path": f"{target_root}/SKILL.md",
                    "openai_config_path": f"{target_root}/agents/openai.yaml",
                    "allow_implicit_invocation": skill_entry["allow_implicit_invocation"],
                    "trust_posture": skill_entry["trust_posture"],
                }
            )
        resolved["profiles"][profile_name] = {
            "description": profile["description"],
            "scope": scope,
            "install_mode": profile["install_mode"],
            "install_root": install_root,
            "skills": entries,
        }
    return resolved


def build_codex_config_snippets(resolved_profiles: dict[str, Any]) -> dict[str, Any]:
    doc = {
        "schema_version": 1,
        "profile": EXPORT_PROFILE,
        "snippets": {},
        "project_root_markers_example": 'project_root_markers = [".git", ".hg", ".sl"]',
    }
    for profile_name, profile in resolved_profiles["profiles"].items():
        lines: list[str] = []
        for entry in profile["skills"]:
            lines.extend(
                [
                    "[[skills.config]]",
                    f'path = "{entry["target_path"]}"',
                    "enabled = false",
                    "",
                ]
            )
        doc["snippets"][profile_name] = {
            "scope": profile["scope"],
            "disable_profile_toml": "\n".join(lines).rstrip() + ("\n" if lines else ""),
        }
    return doc


def build_mcp_dependency_manifest(
    catalog_full: dict[str, Any],
    openai_docs: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "profile": EXPORT_PROFILE,
        "skills": [
            {
                "name": entry["name"],
                "tools": (openai_docs[entry["name"]].get("dependencies", {}) or {}).get("tools", []),
            }
            for entry in catalog_full["skills"]
        ],
    }


def build_local_adapter_manifests(
    *,
    repo_root: pathlib.Path,
    skills_root: pathlib.Path,
    catalog_full: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    root = str(skills_root.relative_to(repo_root).as_posix())
    contracts = {
        "runtime": "generated/skill_runtime_contracts.json",
        "context_retention": "generated/context_retention_manifest.json",
        "trust_policy": "generated/trust_policy_matrix.json",
    }
    manifest = {
        "manifest_version": 2,
        "profile": "codex-facing-local-adapter",
        "root": root,
        "activation_tool": "scripts/activate_skill.py",
        "discovery_view": "generated/local_adapter_manifest.min.json",
        "permission_allowlist": [root],
        "contracts": contracts,
        "source_of_truth": {
            "portable_export_root": root,
            "portable_catalog": "generated/agent_skill_catalog.json",
            "policy_source": "agents/openai.yaml",
        },
        "skills": [],
    }
    manifest_min = {
        "manifest_version": 2,
        "profile": "codex-facing-local-adapter",
        "root": root,
        "activation_tool": "scripts/activate_skill.py",
        "contracts": contracts,
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
                "trust_posture": entry["trust_posture"],
                "context_retention_ref": f"generated/context_retention_manifest.json#{entry['name']}",
            }
        )
        manifest_min["skills"].append(
            {
                "name": entry["name"],
                "description": entry["description"],
                "path": entry["path"],
                "allow_implicit_invocation": entry["allow_implicit_invocation"],
                "trust_posture": entry["trust_posture"],
            }
        )
    return manifest, manifest_min


def build_release_manifest(catalog_full: dict[str, Any], resolved_profiles: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "profile": EXPORT_PROFILE,
        "included_waves": [1, 2, 3, 4],
        "skill_root": ".agents/skills",
        "skill_count": len(catalog_full["skills"]),
        "explicit_only_count": sum(1 for entry in catalog_full["skills"] if not entry["allow_implicit_invocation"]),
        "profile_count": len(resolved_profiles["profiles"]),
        "authoring_inputs": [
            "generated/skill_sections.full.json",
            "generated/skill_catalog.min.json",
            "config/portable_skill_overrides.json",
            "config/openai_skill_extensions.json",
            "config/skill_pack_profiles.json",
            "config/skill_policy_matrix.json",
        ],
        "generated_files": GENERATED_PORTABLE_FILES,
        "release_identity": {
            "changelog": "CHANGELOG.md",
            "releasing_doc": "docs/RELEASING.md",
        },
    }


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
    generated_dir = repo_root / "generated"
    config_dir = repo_root / "config"

    skill_sections = load_json(generated_dir / "skill_sections.full.json")
    skill_catalog = load_json(generated_dir / "skill_catalog.min.json")
    overrides_doc = load_json(config_dir / "portable_skill_overrides.json")
    extension_doc = load_json(
        config_dir / "openai_skill_extensions.json",
        default={"schema_version": 1, "global": {}, "skills": {}},
    )
    profiles_doc = load_json(config_dir / "skill_pack_profiles.json")
    policy_doc = load_json(config_dir / "skill_policy_matrix.json")

    catalog_by_name = {entry["name"]: entry for entry in skill_catalog["skills"]}
    overrides = overrides_doc["skills"]
    policies = policy_doc["skills"]
    compatibility_default = overrides_doc["compatibility_default"]
    source_repo = "8Dionysus/aoa-skills"

    skills_root = pathlib.Path(args.output_root).resolve() if args.output_root else repo_root / ".agents" / "skills"
    if skills_root.exists():
        shutil.rmtree(skills_root)
    skills_root.mkdir(parents=True)

    source_of_truth = {
        "skill_sections": "generated/skill_sections.full.json",
        "skill_catalog": "generated/skill_catalog.min.json",
        "portable_overrides": "config/portable_skill_overrides.json",
        "openai_extensions": "config/openai_skill_extensions.json",
        "policy_matrix": "config/skill_policy_matrix.json",
        "profile_matrix": "config/skill_pack_profiles.json",
    }
    catalog_full = {
        "catalog_version": 2,
        "profile": EXPORT_PROFILE,
        "root": ".agents/skills",
        "source_repo": source_repo,
        "source_of_truth": source_of_truth,
        "skills": [],
    }
    catalog_min = {
        "catalog_version": 2,
        "profile": EXPORT_PROFILE,
        "root": ".agents/skills",
        "skills": [],
    }
    export_map = {
        "export_version": 2,
        "profile": EXPORT_PROFILE,
        "root": ".agents/skills",
        "source_repo": source_repo,
        "source_of_truth": source_of_truth,
        "exports": [],
    }
    context_manifest = {
        "schema_version": 1,
        "profile": EXPORT_PROFILE,
        "skills": [],
    }
    handoff_contracts = {
        "schema_version": 1,
        "profile": EXPORT_PROFILE,
        "source_of_truth": "generated/skill_sections.full.json",
        "skills": [],
    }
    trust_matrix = {
        "schema_version": 1,
        "profile": EXPORT_PROFILE,
        "skills": [],
    }
    runtime_contracts = {
        "schema_version": 1,
        "profile": EXPORT_PROFILE,
        "root": ".agents/skills",
        "skills": [],
    }
    openai_docs: dict[str, dict[str, Any]] = {}

    for skill in skill_sections["skills"]:
        catalog_entry = catalog_by_name[skill["name"]]
        override = overrides[skill["name"]]
        policy_entry = policies[skill["name"]]

        skill_dir = skills_root / skill["name"]
        (skill_dir / "agents").mkdir(parents=True)

        inventory = copy_optional_resources(repo_root / "skills" / skill["name"], skill_dir)
        icon_paths = ensure_scope_assets(skill_dir, skill["scope"])

        skill_md_path = skill_dir / "SKILL.md"
        skill_md_path.write_text(
            build_markdown(skill, catalog_entry, override, compatibility_default, source_repo),
            encoding="utf-8",
        )

        openai_doc = build_openai_yaml(skill, catalog_entry, override, extension_doc, icon_paths)
        openai_docs[skill["name"]] = openai_doc
        (skill_dir / "agents" / "openai.yaml").write_text(
            yaml.safe_dump(openai_doc, sort_keys=False, allow_unicode=True, width=1000),
            encoding="utf-8",
        )

        inventory["assets"] = sorted(
            str(path.relative_to(skill_dir).as_posix())
            for path in (skill_dir / "assets").rglob("*")
            if path.is_file()
        )

        allow_implicit = catalog_entry["invocation_mode"] != "explicit-only"
        ui = openai_doc.get("interface", {})
        catalog_skill_entry = {
            "name": skill["name"],
            "display_name": titleize_skill_name(skill["name"]),
            "description": override["description"],
            "short_description": override["short_description"],
            "path": f".agents/skills/{skill['name']}/SKILL.md",
            "openai_config_path": f".agents/skills/{skill['name']}/agents/openai.yaml",
            "scope": skill["scope"],
            "status": skill["status"],
            "invocation_mode": catalog_entry["invocation_mode"],
            "allow_implicit_invocation": allow_implicit,
            "source_skill_path": skill["skill_path"],
            "technique_dependencies": catalog_entry.get("technique_dependencies", []),
            "trust_posture": policy_entry["trust_posture"],
            "mutation_surface": policy_entry["mutation_surface"],
            "recommended_install_scopes": policy_entry["recommended_install_scopes"],
            "resource_inventory": inventory,
            "ui": {
                "brand_color": ui.get("brand_color"),
                "icon_small": ui.get("icon_small"),
                "icon_large": ui.get("icon_large"),
            },
        }
        catalog_full["skills"].append(catalog_skill_entry)
        catalog_min["skills"].append(
            {
                "name": skill["name"],
                "description": override["description"],
                "path": catalog_skill_entry["path"],
                "allow_implicit_invocation": allow_implicit,
                "trust_posture": policy_entry["trust_posture"],
            }
        )
        export_map["exports"].append(
            {
                "name": skill["name"],
                "source_skill_path": skill["skill_path"],
                "target_dir": f".agents/skills/{skill['name']}",
                "target_skill_path": catalog_skill_entry["path"],
                "target_openai_config_path": catalog_skill_entry["openai_config_path"],
                "invocation_mode": catalog_entry["invocation_mode"],
                "allow_implicit_invocation": allow_implicit,
                "resource_inventory": inventory,
            }
        )

        context_entry = build_context_entry(skill, override, policy_entry)
        trust_entry = build_trust_entry(skill, catalog_entry, policy_entry)
        runtime_entry = build_runtime_entry(
            skill=skill,
            catalog_entry=catalog_entry,
            override=override,
            openai_doc=openai_doc,
            inventory=inventory,
            policy_entry=policy_entry,
        )
        context_manifest["skills"].append(context_entry)
        handoff_contracts["skills"].append(
            build_handoff_entry(
                skill=skill,
                catalog_entry=catalog_entry,
                override=override,
            )
        )
        trust_matrix["skills"].append(trust_entry)
        runtime_contracts["skills"].append(runtime_entry)

    resolved_profiles = resolve_pack_profiles(profiles_doc, catalog_full)
    config_snippets = build_codex_config_snippets(resolved_profiles)
    local_manifest, local_manifest_min = build_local_adapter_manifests(
        repo_root=repo_root,
        skills_root=skills_root,
        catalog_full=catalog_full,
    )
    mcp_manifest = build_mcp_dependency_manifest(catalog_full, openai_docs)
    release_manifest = build_release_manifest(catalog_full, resolved_profiles)

    generated_dir.mkdir(exist_ok=True)
    (generated_dir / "agent_skill_catalog.json").write_text(json.dumps(catalog_full, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "agent_skill_catalog.min.json").write_text(json.dumps(catalog_min, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "portable_export_map.json").write_text(json.dumps(export_map, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "local_adapter_manifest.json").write_text(json.dumps(local_manifest, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "local_adapter_manifest.min.json").write_text(json.dumps(local_manifest_min, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "skill_handoff_contracts.json").write_text(json.dumps(handoff_contracts, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "context_retention_manifest.json").write_text(json.dumps(context_manifest, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "trust_policy_matrix.json").write_text(json.dumps(trust_matrix, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "skill_runtime_contracts.json").write_text(json.dumps(runtime_contracts, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "skill_pack_profiles.resolved.json").write_text(json.dumps(resolved_profiles, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "codex_config_snippets.json").write_text(json.dumps(config_snippets, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "mcp_dependency_manifest.json").write_text(json.dumps(mcp_manifest, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "release_manifest.json").write_text(json.dumps(release_manifest, indent=2) + "\n", encoding="utf-8")
    print(f"built {len(catalog_full['skills'])} skills into {skills_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
