"""Portable per-skill export phase for Agent Skills."""

from __future__ import annotations

import copy
import hashlib
import pathlib
import re
import shutil
from dataclasses import dataclass
from typing import Any

import yaml
from activation.skill_activation_policy import (
    allow_implicit_invocation,
    manual_invocation_required,
    resolve_implicit_activation_policy,
)
from skill_model import skill_layout

RESOURCE_DIR_NAMES = ("scripts", "references", "assets", "checks", "examples")
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


@dataclass(frozen=True)
class ExportBuildDocuments:
    catalog_full: dict[str, Any]
    catalog_min: dict[str, Any]
    export_map: dict[str, Any]
    context_manifest: dict[str, Any]
    handoff_contracts: dict[str, Any]
    trust_matrix: dict[str, Any]
    runtime_contracts: dict[str, Any]
    openai_docs: dict[str, dict[str, Any]]


def write_text_file(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


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


def slugify(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    value = re.sub(r"-+", "-", value)
    return value or "artifact"


def compact_artifact_tag(slug: str, *, seen_tags: set[str], max_length: int = 64) -> str:
    candidate = slug[:max_length] or "artifact"
    if candidate not in seen_tags:
        return candidate

    full_digest = hashlib.sha1(slug.encode("utf-8")).hexdigest()
    for digest_length in range(10, len(full_digest) + 1, 6):
        digest = full_digest[:digest_length]
        base_length = max_length - len(digest) - 1
        base = slug[:base_length].rstrip("-") or "artifact"
        candidate = f"{base}-{digest}"
        if candidate not in seen_tags:
            return candidate

    fallback = str(len(seen_tags) + 1)
    base_length = max_length - len(fallback) - 1
    base = slug[:base_length].rstrip("-") or "artifact"
    return f"{base}-{fallback}"


def artifact_tags(items: list[str], limit: int = 8) -> list[str]:
    tags: list[str] = []
    seen_slugs: set[str] = set()
    seen_tags: set[str] = set()
    for item in items:
        if not item:
            continue
        slug = slugify(item)
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        tag = compact_artifact_tag(slug, seen_tags=seen_tags)
        seen_tags.add(tag)
        tags.append(tag)
        if len(tags) >= limit:
            break
    return tags


def section_map(skill: dict[str, Any]) -> dict[str, str]:
    return {section["heading"]: section["content_markdown"] for section in skill["sections"]}


def extract_bullets(markdown: str, limit: int | None = 3) -> list[str]:
    items: list[str] = []
    accepting_continuation = False
    for raw_line in markdown.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue
        is_continuation = (
            raw_line[:1].isspace()
            and items
            and not stripped.startswith("- ")
            and ". " not in stripped[:4]
        )
        if is_continuation:
            if accepting_continuation:
                items[-1] = normalize_space(f"{items[-1]} {stripped}")
            continue
        bullet: str | None = None
        if stripped.startswith("- "):
            bullet = stripped[2:]
        elif stripped[:2].isdigit() and ". " in stripped[:4]:
            bullet = stripped.split(". ", 1)[1]
        elif stripped[:1].isdigit() and ". " in stripped[:3]:
            bullet = stripped.split(". ", 1)[1]
        if bullet is None:
            accepting_continuation = False
            continue
        if limit is not None and len(items) >= limit:
            accepting_continuation = False
            continue
        items.append(normalize_space(bullet))
        accepting_continuation = True
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
        write_text_file(small_path, skill_svg(scope, 32))
    if not large_path.exists():
        write_text_file(large_path, skill_svg(scope, 128))
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
    policy_entry: dict[str, Any],
) -> dict[str, Any]:
    ui = scope_defaults(skill["scope"])
    activation_policy = resolve_implicit_activation_policy(policy_entry, skill["name"])
    allow_implicit = allow_implicit_invocation(policy_entry, skill["name"])
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
            "implicit_activation_policy": activation_policy,
            "allow_implicit_invocation": allow_implicit,
        },
    }

    global_extension = extension_doc.get("global", {})
    per_skill_extension = extension_doc.get("skills", {}).get(skill["name"], {})
    merged = merge_dict(base_doc, global_extension)
    merged = merge_dict(merged, per_skill_extension)

    merged.setdefault("policy", {})
    merged["policy"]["implicit_activation_policy"] = activation_policy
    merged["policy"]["allow_implicit_invocation"] = allow_implicit

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
    activation_policy = resolve_implicit_activation_policy(policy_entry, skill["name"])
    return {
        "name": skill["name"],
        "scope": skill["scope"],
        "invocation_mode": catalog_entry["invocation_mode"],
        "implicit_activation_policy": activation_policy,
        "trust_posture": policy_entry["trust_posture"],
        "mutation_surface": policy_entry["mutation_surface"],
        "requires_manual_invocation": manual_invocation_required(policy_entry, skill["name"]),
        "candidate_only": activation_policy == "suggest",
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
    activation_policy = resolve_implicit_activation_policy(policy_entry, skill["name"])
    return {
        "name": skill["name"],
        "display_name": titleize_skill_name(skill["name"]),
        "description": override["description"],
        "short_description": override["short_description"],
        "path": f".agents/skills/{skill['name']}/SKILL.md",
        "openai_config_path": f".agents/skills/{skill['name']}/agents/openai.yaml",
        "invocation_mode": catalog_entry["invocation_mode"],
        "implicit_activation_policy": activation_policy,
        "allow_implicit_invocation": openai_doc.get("policy", {}).get("allow_implicit_invocation"),
        "manual_invocation_required": manual_invocation_required(policy_entry, skill["name"]),
        "candidate_only": activation_policy == "suggest",
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


def initialize_export_documents(source_repo: str, source_of_truth: dict[str, str]) -> ExportBuildDocuments:
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
        context_manifest={
            "schema_version": 1,
            "profile": EXPORT_PROFILE,
            "skills": [],
        },
        handoff_contracts={
            "schema_version": 1,
            "profile": EXPORT_PROFILE,
            "source_of_truth": "generated/skill_sections.full.json",
            "skills": [],
        },
        trust_matrix={
            "schema_version": 1,
            "profile": EXPORT_PROFILE,
            "skills": [],
        },
        runtime_contracts={
            "schema_version": 1,
            "profile": EXPORT_PROFILE,
            "root": ".agents/skills",
            "skills": [],
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
    documents = initialize_export_documents(source_repo, source_of_truth)
    catalog_by_name = {entry["name"]: entry for entry in skill_catalog["skills"]}
    overrides = overrides_doc["skills"]
    policies = policy_doc["skills"]
    compatibility_default = overrides_doc["compatibility_default"]

    for skill in skill_sections["skills"]:
        catalog_entry = catalog_by_name[skill["name"]]
        override = overrides[skill["name"]]
        policy_entry = policies[skill["name"]]

        skill_dir = skills_root / skill["name"]
        (skill_dir / "agents").mkdir(parents=True)

        inventory = copy_optional_resources(
            skill_layout.skill_dir_path(repo_root, skill["name"]),
            skill_dir,
        )
        icon_paths = ensure_scope_assets(skill_dir, skill["scope"])

        write_text_file(
            skill_dir / "SKILL.md",
            build_markdown(skill, catalog_entry, override, compatibility_default, source_repo),
        )

        openai_doc = build_openai_yaml(
            skill,
            catalog_entry,
            override,
            extension_doc,
            icon_paths,
            policy_entry,
        )
        documents.openai_docs[skill["name"]] = openai_doc
        write_text_file(
            skill_dir / "agents" / "openai.yaml",
            yaml.safe_dump(openai_doc, sort_keys=False, allow_unicode=True, width=1000),
        )

        inventory["assets"] = sorted(
            str(path.relative_to(skill_dir).as_posix())
            for path in (skill_dir / "assets").rglob("*")
            if path.is_file()
        )

        activation_policy = resolve_implicit_activation_policy(policy_entry, skill["name"])
        allow_implicit = allow_implicit_invocation(policy_entry, skill["name"])
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
            "implicit_activation_policy": activation_policy,
            "allow_implicit_invocation": allow_implicit,
            "manual_invocation_required": manual_invocation_required(policy_entry, skill["name"]),
            "candidate_only": activation_policy == "suggest",
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
        documents.catalog_full["skills"].append(catalog_skill_entry)
        documents.catalog_min["skills"].append(
            {
                "name": skill["name"],
                "description": override["description"],
                "path": catalog_skill_entry["path"],
                "implicit_activation_policy": activation_policy,
                "allow_implicit_invocation": allow_implicit,
                "candidate_only": activation_policy == "suggest",
                "trust_posture": policy_entry["trust_posture"],
            }
        )
        documents.export_map["exports"].append(
            {
                "name": skill["name"],
                "source_skill_path": skill["skill_path"],
                "target_dir": f".agents/skills/{skill['name']}",
                "target_skill_path": catalog_skill_entry["path"],
                "target_openai_config_path": catalog_skill_entry["openai_config_path"],
                "invocation_mode": catalog_entry["invocation_mode"],
                "implicit_activation_policy": activation_policy,
                "allow_implicit_invocation": allow_implicit,
                "candidate_only": activation_policy == "suggest",
                "resource_inventory": inventory,
            }
        )

        documents.context_manifest["skills"].append(build_context_entry(skill, override, policy_entry))
        documents.handoff_contracts["skills"].append(
            build_handoff_entry(skill=skill, catalog_entry=catalog_entry, override=override)
        )
        documents.trust_matrix["skills"].append(build_trust_entry(skill, catalog_entry, policy_entry))
        documents.runtime_contracts["skills"].append(
            build_runtime_entry(
                skill=skill,
                catalog_entry=catalog_entry,
                override=override,
                openai_doc=openai_doc,
                inventory=inventory,
                policy_entry=policy_entry,
            )
        )

    return documents
