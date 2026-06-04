#!/usr/bin/env python3
"""Build the cumulative Codex-facing Agent Skills export and support artifacts."""

from __future__ import annotations

import argparse
import copy
import json
import pathlib
import shutil
from dataclasses import dataclass
from typing import Any

from export import (
    local_adapter_manifest,
    portable_skill_export,
    project_surface,
    release_manifest_contract,
)
import yaml

STANDARD_INSTALL_ROOTS = {
    "repo": ".agents/skills",
    "user": "$HOME/.agents/skills",
    "admin": "/etc/codex/skills",
}
EXPORT_PROFILE = portable_skill_export.EXPORT_PROFILE
DEFAULT_EXPORT_ROOT = pathlib.Path(".agents") / "skills"


@dataclass(frozen=True)
class ExportBuildInputs:
    repo_root: pathlib.Path
    generated_dir: pathlib.Path
    config_dir: pathlib.Path
    skill_sections: dict[str, Any]
    skill_catalog: dict[str, Any]
    overrides_doc: dict[str, Any]
    extension_doc: dict[str, Any]
    profiles_doc: dict[str, Any]
    kernel_doc: dict[str, Any]
    ring_doc: dict[str, Any]
    risk_ring_doc: dict[str, Any]
    policy_doc: dict[str, Any]
    source_repo: str


ExportBuildDocuments = portable_skill_export.ExportBuildDocuments


def write_text_file(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def load_json(path: pathlib.Path, default: Any | None = None) -> Any:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    if default is not None:
        return copy.deepcopy(default)
    raise FileNotFoundError(path)


def path_reference(path: pathlib.Path, repo_root: pathlib.Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def prepare_skills_root(repo_root: pathlib.Path, skills_root: pathlib.Path) -> None:
    default_skills_root = (repo_root / DEFAULT_EXPORT_ROOT).resolve()
    if skills_root == default_skills_root:
        if skills_root.exists():
            shutil.rmtree(skills_root)
        skills_root.mkdir(parents=True, exist_ok=True)
        return
    if skills_root.exists():
        if not skills_root.is_dir():
            raise ValueError(f"--output-root must point to a directory: {skills_root}")
        if any(skills_root.iterdir()):
            raise ValueError(
                "--output-root must point to a new or empty directory; refusing to delete existing external contents"
            )
    else:
        skills_root.mkdir(parents=True, exist_ok=True)


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


titleize_skill_name = portable_skill_export.titleize_skill_name
dump_yaml_frontmatter = portable_skill_export.dump_yaml_frontmatter
merge_dict = portable_skill_export.merge_dict
normalize_space = portable_skill_export.normalize_space
slugify = portable_skill_export.slugify
compact_artifact_tag = portable_skill_export.compact_artifact_tag
artifact_tags = portable_skill_export.artifact_tags
section_map = portable_skill_export.section_map
extract_bullets = portable_skill_export.extract_bullets
scope_defaults = portable_skill_export.scope_defaults
skill_svg = portable_skill_export.skill_svg
ensure_scope_assets = portable_skill_export.ensure_scope_assets
build_markdown = portable_skill_export.build_markdown
build_openai_yaml = portable_skill_export.build_openai_yaml
copy_optional_resources = portable_skill_export.copy_optional_resources
build_context_entry = portable_skill_export.build_context_entry
build_trust_entry = portable_skill_export.build_trust_entry
build_runtime_entry = portable_skill_export.build_runtime_entry
build_handoff_entry = portable_skill_export.build_handoff_entry


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
                    "implicit_activation_policy": skill_entry["implicit_activation_policy"],
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


def build_project_core_kernel_doc(kernel_doc: dict[str, Any]) -> dict[str, Any]:
    return project_surface.build_project_core_kernel_doc(kernel_doc)


def build_project_core_kernel_governance_doc(
    *,
    repo_root: pathlib.Path,
    skills_root: pathlib.Path,
    kernel_doc: dict[str, Any],
    export_map: dict[str, Any],
) -> dict[str, Any]:
    return project_surface.build_project_core_kernel_governance_doc(
        repo_root=repo_root,
        skills_root=skills_root,
        kernel_doc=kernel_doc,
        export_map=export_map,
    )


def build_project_core_outer_ring_doc(ring_doc: dict[str, Any]) -> dict[str, Any]:
    return project_surface.build_project_core_outer_ring_doc(ring_doc)


def build_project_core_outer_ring_readiness_doc(
    *,
    ring_doc: dict[str, Any],
    skill_catalog: dict[str, Any],
    profiles_doc: dict[str, Any],
    collision_doc: dict[str, Any],
) -> dict[str, Any]:
    return project_surface.build_project_core_outer_ring_readiness_doc(
        ring_doc=ring_doc,
        skill_catalog=skill_catalog,
        profiles_doc=profiles_doc,
        collision_doc=collision_doc,
    )


def build_project_risk_guard_ring_doc(ring_doc: dict[str, Any]) -> dict[str, Any]:
    return project_surface.build_project_risk_guard_ring_doc(ring_doc)


def build_project_risk_guard_ring_governance_doc(
    *,
    ring_doc: dict[str, Any],
    skill_catalog: dict[str, Any],
    profiles_doc: dict[str, Any],
    collision_doc: dict[str, Any],
) -> dict[str, Any]:
    return project_surface.build_project_risk_guard_ring_governance_doc(
        ring_doc=ring_doc,
        skill_catalog=skill_catalog,
        profiles_doc=profiles_doc,
        collision_doc=collision_doc,
    )


def build_project_foundation_profile_doc(
    *,
    kernel_doc: dict[str, Any],
    outer_ring_doc: dict[str, Any],
    risk_ring_doc: dict[str, Any],
    profiles_doc: dict[str, Any],
) -> dict[str, Any]:
    return project_surface.build_project_foundation_profile_doc(
        kernel_doc=kernel_doc,
        outer_ring_doc=outer_ring_doc,
        risk_ring_doc=risk_ring_doc,
        profiles_doc=profiles_doc,
    )


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Path to target aoa-skills repository root")
    parser.add_argument(
        "--output-root",
        default=None,
        help="Optional override for where to write the portable layer. Defaults to <repo-root>/.agents/skills",
    )
    return parser.parse_args()


def build_source_of_truth() -> dict[str, str]:
    return {
        "skill_sections": "generated/skill_sections.full.json",
        "skill_catalog": "generated/skill_catalog.min.json",
        "portable_overrides": "config/portable_skill_overrides.json",
        "openai_extensions": "config/openai_skill_extensions.json",
        "policy_matrix": "config/skill_policy_matrix.json",
        "profile_matrix": "config/skill_pack_profiles.json",
        "project_core_kernel": "config/project_core_skill_kernel.json",
        "project_core_outer_ring": "config/project_core_outer_ring.json",
        "project_risk_guard_ring": "config/project_risk_guard_ring.json",
    }


def load_export_build_inputs(repo_root: pathlib.Path) -> ExportBuildInputs:
    generated_dir = repo_root / "generated"
    config_dir = repo_root / "config"
    return ExportBuildInputs(
        repo_root=repo_root,
        generated_dir=generated_dir,
        config_dir=config_dir,
        skill_sections=load_json(generated_dir / "skill_sections.full.json"),
        skill_catalog=load_json(generated_dir / "skill_catalog.min.json"),
        overrides_doc=load_json(config_dir / "portable_skill_overrides.json"),
        extension_doc=load_json(
            config_dir / "openai_skill_extensions.json",
            default={"schema_version": 1, "global": {}, "skills": {}},
        ),
        profiles_doc=load_json(config_dir / "skill_pack_profiles.json"),
        kernel_doc=load_json(config_dir / "project_core_skill_kernel.json"),
        ring_doc=load_json(config_dir / "project_core_outer_ring.json"),
        risk_ring_doc=load_json(config_dir / "project_risk_guard_ring.json"),
        policy_doc=load_json(config_dir / "skill_policy_matrix.json"),
        source_repo="8Dionysus/aoa-skills",
    )


def build_portable_skill_exports(
    inputs: ExportBuildInputs,
    skills_root: pathlib.Path,
) -> ExportBuildDocuments:
    return portable_skill_export.build_portable_skill_exports(
        repo_root=inputs.repo_root,
        skills_root=skills_root,
        source_repo=inputs.source_repo,
        source_of_truth=build_source_of_truth(),
        skill_sections=inputs.skill_sections,
        skill_catalog=inputs.skill_catalog,
        overrides_doc=inputs.overrides_doc,
        extension_doc=inputs.extension_doc,
        policy_doc=inputs.policy_doc,
    )


def build_generated_file_texts(
    inputs: ExportBuildInputs,
    skills_root: pathlib.Path,
    documents: ExportBuildDocuments,
) -> dict[pathlib.Path, str]:
    collision_doc = load_json(inputs.generated_dir / "skill_trigger_collision_matrix.json")
    resolved_profiles = resolve_pack_profiles(inputs.profiles_doc, documents.catalog_full)
    project_core_kernel = project_surface.build_project_core_kernel_doc(inputs.kernel_doc)
    project_core_kernel_governance = project_surface.build_project_core_kernel_governance_doc(
        repo_root=inputs.repo_root,
        skills_root=skills_root,
        kernel_doc=inputs.kernel_doc,
        export_map=documents.export_map,
    )
    project_core_outer_ring = project_surface.build_project_core_outer_ring_doc(inputs.ring_doc)
    project_core_outer_ring_readiness = project_surface.build_project_core_outer_ring_readiness_doc(
        ring_doc=inputs.ring_doc,
        skill_catalog=inputs.skill_catalog,
        profiles_doc=inputs.profiles_doc,
        collision_doc=collision_doc,
    )
    project_risk_guard_ring = project_surface.build_project_risk_guard_ring_doc(inputs.risk_ring_doc)
    project_risk_guard_ring_governance = project_surface.build_project_risk_guard_ring_governance_doc(
        ring_doc=inputs.risk_ring_doc,
        skill_catalog=inputs.skill_catalog,
        profiles_doc=inputs.profiles_doc,
        collision_doc=collision_doc,
    )
    project_foundation_profile = project_surface.build_project_foundation_profile_doc(
        kernel_doc=inputs.kernel_doc,
        outer_ring_doc=inputs.ring_doc,
        risk_ring_doc=inputs.risk_ring_doc,
        profiles_doc=inputs.profiles_doc,
    )
    config_snippets = build_codex_config_snippets(resolved_profiles)
    local_manifest, local_manifest_min = local_adapter_manifest.build_local_adapter_manifests(
        repo_root=inputs.repo_root,
        skills_root=skills_root,
        catalog_full=documents.catalog_full,
    )
    mcp_manifest = build_mcp_dependency_manifest(documents.catalog_full, documents.openai_docs)
    generated_dir = inputs.generated_dir
    file_texts = {
        generated_dir / "agent_skill_catalog.json": json.dumps(documents.catalog_full, indent=2) + "\n",
        generated_dir / "agent_skill_catalog.min.json": json.dumps(documents.catalog_min, indent=2) + "\n",
        generated_dir / "portable_export_map.json": json.dumps(documents.export_map, indent=2) + "\n",
        generated_dir / "local_adapter_manifest.json": json.dumps(local_manifest, indent=2) + "\n",
        generated_dir / "local_adapter_manifest.min.json": json.dumps(local_manifest_min, indent=2) + "\n",
        generated_dir / "skill_handoff_contracts.json": json.dumps(documents.handoff_contracts, indent=2) + "\n",
        generated_dir / "context_retention_manifest.json": json.dumps(documents.context_manifest, indent=2) + "\n",
        generated_dir / "trust_policy_matrix.json": json.dumps(documents.trust_matrix, indent=2) + "\n",
        generated_dir / "skill_runtime_contracts.json": json.dumps(documents.runtime_contracts, indent=2) + "\n",
        generated_dir / "skill_pack_profiles.resolved.json": json.dumps(resolved_profiles, indent=2) + "\n",
        generated_dir / "project_core_skill_kernel.min.json": json.dumps(project_core_kernel, indent=2) + "\n",
        generated_dir / "project_core_kernel_governance.min.json": json.dumps(project_core_kernel_governance, indent=2) + "\n",
        generated_dir / "project_core_outer_ring.min.json": json.dumps(project_core_outer_ring, indent=2) + "\n",
        generated_dir / "project_core_outer_ring_readiness.min.json": json.dumps(project_core_outer_ring_readiness, indent=2) + "\n",
        generated_dir / "project_risk_guard_ring.min.json": json.dumps(project_risk_guard_ring, indent=2) + "\n",
        generated_dir / "project_risk_guard_ring_governance.min.json": json.dumps(project_risk_guard_ring_governance, indent=2) + "\n",
        generated_dir / "project_foundation_profile.min.json": json.dumps(project_foundation_profile, indent=2) + "\n",
        generated_dir / "codex_config_snippets.json": json.dumps(config_snippets, indent=2) + "\n",
        generated_dir / "mcp_dependency_manifest.json": json.dumps(mcp_manifest, indent=2) + "\n",
    }
    release_manifest = release_manifest_contract.build_release_manifest(
        inputs.repo_root,
        file_overrides=file_texts,
    )
    file_texts[generated_dir / "release_manifest.json"] = json.dumps(release_manifest, indent=2) + "\n"
    return file_texts


def write_generated_file_texts(file_texts: dict[pathlib.Path, str]) -> None:
    for path, text in file_texts.items():
        write_text_file(path, text)


def main() -> int:
    args = parse_args()
    repo_root = pathlib.Path(args.repo_root).resolve()
    inputs = load_export_build_inputs(repo_root)
    skills_root = pathlib.Path(args.output_root).resolve() if args.output_root else repo_root / DEFAULT_EXPORT_ROOT
    prepare_skills_root(repo_root, skills_root)
    documents = build_portable_skill_exports(inputs, skills_root)
    inputs.generated_dir.mkdir(exist_ok=True)
    write_generated_file_texts(build_generated_file_texts(inputs, skills_root, documents))
    print(f"built {len(documents.catalog_full['skills'])} skills into {skills_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
