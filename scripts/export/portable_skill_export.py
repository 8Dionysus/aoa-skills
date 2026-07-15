"""Build the portable Agent Skills view from owner-authored source bundles."""

from __future__ import annotations

import copy
import pathlib
import re
import shutil
from dataclasses import dataclass
from typing import Any

import yaml

from skill_model import skill_layout


RESOURCE_DIR_NAMES = ("scripts", "references", "assets", "checks", "examples")
EXPORT_PROFILE = "codex-facing-v2"
ACTIVATION_POLICIES = {"invoke", "suggest", "manual"}
MANUAL_ACTIVATION_DESCRIPTION_PREFIX = (
    "Explicit activation required: do not load this skill from an implicit match; "
    "wait for explicit user or operator invocation. "
)
SUGGEST_ACTIVATION_DESCRIPTION_PREFIX = (
    "An implicit match may suggest this skill, but must not load or execute it "
    "until explicit invocation or a source-authorized parent-route selection. "
)
SCOPE_UI_DEFAULTS = {
    "core": {"brand_color": "#2563EB", "accent": "#2563EB"},
    "risk": {"brand_color": "#B45309", "accent": "#B45309"},
    "project": {"brand_color": "#6D28D9", "accent": "#6D28D9"},
}


@dataclass(frozen=True)
class ExportBuildDocuments:
    catalog_full: dict[str, Any]
    catalog_min: dict[str, Any]
    export_map: dict[str, Any]
    openai_docs: dict[str, dict[str, Any]]


def write_text_file(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def titleize_skill_name(name: str) -> str:
    special = {"aoa": "AoA", "atm10": "ATM10", "tdd": "TDD", "adr": "ADR"}
    return " ".join(special.get(part, part.capitalize()) for part in name.split("-"))


def merge_dict(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_dict(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def resolve_activation_policy(policy_entry: dict[str, Any], skill_name: str) -> str:
    value = policy_entry.get("implicit_activation_policy")
    if value not in ACTIVATION_POLICIES:
        raise ValueError(
            f"skill policy for {skill_name!r} must use one of {sorted(ACTIVATION_POLICIES)!r}"
        )
    return str(value)


def with_prompt_visible_activation_policy(
    override: dict[str, Any],
    policy_entry: dict[str, Any],
    skill_name: str,
) -> dict[str, Any]:
    policy = resolve_activation_policy(policy_entry, skill_name)
    prompt_visible = copy.deepcopy(override)
    description = normalize_space(str(prompt_visible["description"]))
    if policy == "manual":
        description = MANUAL_ACTIVATION_DESCRIPTION_PREFIX + description
    elif policy == "suggest":
        description = SUGGEST_ACTIVATION_DESCRIPTION_PREFIX + description
    prompt_visible["description"] = description
    return prompt_visible


def scope_defaults(scope: str) -> dict[str, str]:
    return SCOPE_UI_DEFAULTS.get(scope, SCOPE_UI_DEFAULTS["core"])


def skill_svg(scope: str, size: int) -> str:
    ui = scope_defaults(scope)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" '
        f'width="{size}" height="{size}" role="img" aria-label="{scope} skill icon">\n'
        f'  <rect x="4" y="4" width="56" height="56" rx="14" fill="{ui["accent"]}"/>\n'
        '  <path d="M18 23 H46 M18 32 H46 M18 41 H38" '
        'stroke="white" stroke-width="4" stroke-linecap="round"/>\n'
        "</svg>\n"
    )


def ensure_scope_assets(skill_dir: pathlib.Path, scope: str) -> dict[str, str]:
    assets_dir = skill_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    for filename, size in (("small-logo.svg", 32), ("large-logo.svg", 128)):
        path = assets_dir / filename
        if not path.exists():
            write_text_file(path, skill_svg(scope, size))
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
            "aoa_portable_profile": EXPORT_PROFILE,
        },
    }
    frontmatter_text = yaml.safe_dump(
        frontmatter, sort_keys=False, allow_unicode=True, width=1000
    )
    lines = [f"---\n{frontmatter_text}---\n", f"# {skill['name']}", ""]
    for section in skill["sections"]:
        lines.extend(
            [
                f"## {section['heading']}",
                section["content_markdown"].rstrip(),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_openai_yaml(
    *,
    source_doc: dict[str, Any],
    skill: dict[str, Any],
    override: dict[str, Any],
    extension_doc: dict[str, Any],
    icon_paths: dict[str, str],
    policy_entry: dict[str, Any],
) -> dict[str, Any]:
    policy = resolve_activation_policy(policy_entry, skill["name"])
    ui = scope_defaults(skill["scope"])
    generated = {
        "interface": {
            "display_name": titleize_skill_name(skill["name"]),
            "short_description": override["short_description"],
            "default_prompt": override["default_prompt"],
            "icon_small": icon_paths["icon_small"],
            "icon_large": icon_paths["icon_large"],
            "brand_color": ui["brand_color"],
        },
        "policy": {
            "implicit_activation_policy": policy,
            "allow_implicit_invocation": policy == "invoke",
        },
    }
    merged = merge_dict(source_doc, generated)
    merged = merge_dict(merged, extension_doc.get("global", {}))
    merged = merge_dict(merged, extension_doc.get("skills", {}).get(skill["name"], {}))
    merged.setdefault("policy", {})
    merged["policy"]["implicit_activation_policy"] = policy
    merged["policy"]["allow_implicit_invocation"] = policy == "invoke"
    dependencies = merged.get("dependencies")
    if isinstance(dependencies, dict) and dependencies.get("tools") == []:
        dependencies = {key: value for key, value in dependencies.items() if key != "tools"}
        if dependencies:
            merged["dependencies"] = dependencies
        else:
            merged.pop("dependencies", None)
    return merged


def copy_optional_resources(
    source_skill_dir: pathlib.Path,
    target_skill_dir: pathlib.Path,
) -> dict[str, list[str]]:
    inventory: dict[str, list[str]] = {name: [] for name in RESOURCE_DIR_NAMES}
    for name in RESOURCE_DIR_NAMES:
        source_dir = source_skill_dir / name
        target_dir = target_skill_dir / name
        if source_dir.exists():
            shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
        if target_dir.exists():
            inventory[name] = sorted(
                path.relative_to(target_skill_dir).as_posix()
                for path in target_dir.rglob("*")
                if path.is_file()
            )
    return inventory


def initialize_documents(
    source_repo: str,
    source_of_truth: dict[str, str],
) -> ExportBuildDocuments:
    return ExportBuildDocuments(
        catalog_full={
            "catalog_version": 2,
            "profile": EXPORT_PROFILE,
            "root": ".agents/skills",
            "source_repo": source_repo,
            "source_of_truth": source_of_truth,
            "skills": [],
        },
        catalog_min={
            "catalog_version": 2,
            "profile": EXPORT_PROFILE,
            "root": ".agents/skills",
            "skills": [],
        },
        export_map={
            "export_version": 2,
            "profile": EXPORT_PROFILE,
            "root": ".agents/skills",
            "source_repo": source_repo,
            "source_of_truth": source_of_truth,
            "exports": [],
        },
        openai_docs={},
    )


def build_portable_skill_exports(
    *,
    repo_root: pathlib.Path,
    skills_root: pathlib.Path,
    source_repo: str,
    source_of_truth: dict[str, str],
    skill_sections: dict[str, Any],
    skill_catalog: dict[str, Any],
    overrides_doc: dict[str, Any],
    extension_doc: dict[str, Any],
    policy_doc: dict[str, Any],
) -> ExportBuildDocuments:
    documents = initialize_documents(source_repo, source_of_truth)
    catalog_by_name = {entry["name"]: entry for entry in skill_catalog["skills"]}
    overrides = overrides_doc["skills"]
    policies = policy_doc["skills"]
    compatibility_default = overrides_doc["compatibility_default"]

    for skill in skill_sections["skills"]:
        name = skill["name"]
        catalog_entry = catalog_by_name[name]
        policy_entry = policies[name]
        activation_policy = resolve_activation_policy(policy_entry, name)
        override = with_prompt_visible_activation_policy(
            overrides[name], policy_entry, name
        )
        source_skill_dir = skill_layout.skill_dir_path(repo_root, name)
        target_skill_dir = skills_root / name
        (target_skill_dir / "agents").mkdir(parents=True)
        inventory = copy_optional_resources(source_skill_dir, target_skill_dir)
        icon_paths = ensure_scope_assets(target_skill_dir, skill["scope"])
        write_text_file(
            target_skill_dir / "SKILL.md",
            build_markdown(
                skill,
                catalog_entry,
                override,
                compatibility_default,
                source_repo,
            ),
        )
        source_agent_path = source_skill_dir / "agents" / "openai.yaml"
        source_doc = yaml.safe_load(source_agent_path.read_text(encoding="utf-8")) or {}
        if not isinstance(source_doc, dict):
            raise ValueError(f"{source_agent_path} must contain a YAML mapping")
        openai_doc = build_openai_yaml(
            source_doc=source_doc,
            skill=skill,
            override=override,
            extension_doc=extension_doc,
            icon_paths=icon_paths,
            policy_entry=policy_entry,
        )
        documents.openai_docs[name] = openai_doc
        write_text_file(
            target_skill_dir / "agents" / "openai.yaml",
            yaml.safe_dump(
                openai_doc, sort_keys=False, allow_unicode=True, width=1000
            ),
        )
        inventory["assets"] = sorted(
            path.relative_to(target_skill_dir).as_posix()
            for path in (target_skill_dir / "assets").rglob("*")
            if path.is_file()
        )
        allow_implicit = activation_policy == "invoke"
        candidate_only = activation_policy != "invoke"
        ui = openai_doc.get("interface", {})
        full_entry = {
            "name": name,
            "display_name": titleize_skill_name(name),
            "description": override["description"],
            "short_description": override["short_description"],
            "path": f".agents/skills/{name}/SKILL.md",
            "openai_config_path": f".agents/skills/{name}/agents/openai.yaml",
            "scope": skill["scope"],
            "status": skill["status"],
            "invocation_mode": catalog_entry["invocation_mode"],
            "implicit_activation_policy": activation_policy,
            "allow_implicit_invocation": allow_implicit,
            "manual_invocation_required": not allow_implicit,
            "candidate_only": candidate_only,
            "source_skill_path": skill["skill_path"],
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
        documents.catalog_full["skills"].append(full_entry)
        documents.catalog_min["skills"].append(
            {
                "name": name,
                "description": override["description"],
                "path": full_entry["path"],
                "implicit_activation_policy": activation_policy,
                "allow_implicit_invocation": allow_implicit,
                "candidate_only": candidate_only,
                "trust_posture": policy_entry["trust_posture"],
            }
        )
        documents.export_map["exports"].append(
            {
                "name": name,
                "source_skill_path": skill["skill_path"],
                "target_dir": f".agents/skills/{name}",
                "target_skill_path": full_entry["path"],
                "target_openai_config_path": full_entry["openai_config_path"],
                "invocation_mode": catalog_entry["invocation_mode"],
                "implicit_activation_policy": activation_policy,
                "allow_implicit_invocation": allow_implicit,
                "candidate_only": candidate_only,
                "resource_inventory": inventory,
            }
        )
    return documents
