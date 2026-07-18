#!/usr/bin/env python3
"""Build the compact Codex-facing export from current AoA skill sources."""

from __future__ import annotations

import argparse
import copy
import json
import pathlib
import shutil
import tempfile
from dataclasses import dataclass
from typing import Any

from export import portable_skill_export, release_manifest_contract
from skill_model import capability_system, skill_source_model


STANDARD_INSTALL_ROOTS = {
    "repo": ".agents/skills",
    "user": "$HOME/.codex/skills",
    "admin": "/etc/codex/skills",
}
EXPORT_PROFILE = portable_skill_export.EXPORT_PROFILE
LEGACY_ACTIVE_EXPORT_ROOT = pathlib.Path(".agents") / "skills"


@dataclass(frozen=True)
class ExportBuildInputs:
    repo_root: pathlib.Path
    generated_dir: pathlib.Path
    overrides_doc: dict[str, Any]
    extension_doc: dict[str, Any]
    profiles_doc: dict[str, Any]
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


def prepare_skills_root(repo_root: pathlib.Path, skills_root: pathlib.Path) -> None:
    if skills_root == (repo_root / LEGACY_ACTIVE_EXPORT_ROOT).resolve():
        raise ValueError(
            "refusing to materialize globally selected shared skills inside "
            "aoa-skills/.agents/skills; use an explicit external consumer root"
        )
    if skills_root.exists():
        if not skills_root.is_dir():
            raise ValueError(f"--output-root must point to a directory: {skills_root}")
        if any(skills_root.iterdir()):
            raise ValueError(
                "--output-root must point to a new or empty directory; refusing to delete existing external contents"
            )
    else:
        skills_root.mkdir(parents=True, exist_ok=True)


def build_source_documents(repo_root: pathlib.Path) -> tuple[dict[str, Any], dict[str, Any]]:
    families = capability_system.validate_sources(repo_root)
    nodes = capability_system.node_map(families)
    policies = load_json(repo_root / "config" / "skill_policy_matrix.json")["skills"]
    overrides = load_json(repo_root / "config" / "portable_skill_overrides.json")["skills"]
    invocation_modes = {
        "invoke": "implicit-friendly",
        "suggest": "explicit-preferred",
        "manual": "explicit-only",
    }
    sections: list[dict[str, Any]] = []
    catalog: list[dict[str, Any]] = []
    for source in skill_source_model.load_skill_sources(repo_root):
        node = nodes[f"skill.{source.name}"]
        lifecycle = node["lifecycle"]
        activation = policies[source.name]["implicit_activation_policy"]
        skill_path = source.skill_md_path.relative_to(repo_root).as_posix()
        sections.append(
            {
                "name": source.name,
                "scope": "core",
                "status": lifecycle["state"],
                "skill_path": skill_path,
                "sections": [
                    {"heading": heading, "content_markdown": content}
                    for heading, content in source.sections.items()
                ],
            }
        )
        catalog.append(
            {
                "name": source.name,
                "scope": "core",
                "status": lifecycle["state"],
                "summary": overrides[source.name]["short_description"],
                "invocation_mode": invocation_modes[activation],
                "skill_path": skill_path,
            }
        )
    return {"skills": sections}, {"skills": catalog}


def resolve_pack_profiles(
    profiles_doc: dict[str, Any],
    catalog_full: dict[str, Any],
) -> dict[str, Any]:
    skills_by_name = {entry["name"]: entry for entry in catalog_full["skills"]}
    resolved = {
        "schema_version": 2,
        "profile": EXPORT_PROFILE,
        "source_config": "config/skill_pack_profiles.json",
        "profiles": {},
    }
    for profile_name, profile in profiles_doc.get("profiles", {}).items():
        scope = profile["scope"]
        install_root = STANDARD_INSTALL_ROOTS[scope]
        entries = []
        for skill_name in profile["skills"]:
            if skill_name not in skills_by_name:
                raise ValueError(f"profile {profile_name!r} references unknown skill {skill_name!r}")
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


def build_mcp_dependency_manifest(
    catalog_full: dict[str, Any],
    openai_docs: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": 2,
        "profile": EXPORT_PROFILE,
        "skills": [
            {
                "name": entry["name"],
                "tools": (openai_docs[entry["name"]].get("dependencies", {}) or {}).get(
                    "tools", []
                ),
            }
            for entry in catalog_full["skills"]
        ],
    }


def build_source_of_truth() -> dict[str, str]:
    return {
        "skill_sources": "skills/**/SKILL.md",
        "capability_families": "capabilities/families/*.yaml",
        "portable_overrides": "config/portable_skill_overrides.json",
        "openai_extensions": "config/openai_skill_extensions.json",
        "policy_matrix": "config/skill_policy_matrix.json",
        "profile_matrix": "config/skill_pack_profiles.json",
    }


def load_export_build_inputs(repo_root: pathlib.Path) -> ExportBuildInputs:
    config_dir = repo_root / "config"
    return ExportBuildInputs(
        repo_root=repo_root,
        generated_dir=repo_root / "generated",
        overrides_doc=load_json(config_dir / "portable_skill_overrides.json"),
        extension_doc=load_json(
            config_dir / "openai_skill_extensions.json",
            default={"schema_version": 2, "global": {}, "skills": {}},
        ),
        profiles_doc=load_json(config_dir / "skill_pack_profiles.json"),
        policy_doc=load_json(config_dir / "skill_policy_matrix.json"),
        source_repo="8Dionysus/aoa-skills",
    )


def build_portable_skill_exports(
    inputs: ExportBuildInputs,
    skills_root: pathlib.Path,
) -> ExportBuildDocuments:
    skill_sections, skill_catalog = build_source_documents(inputs.repo_root)
    return portable_skill_export.build_portable_skill_exports(
        repo_root=inputs.repo_root,
        skills_root=skills_root,
        source_repo=inputs.source_repo,
        source_of_truth=build_source_of_truth(),
        skill_sections=skill_sections,
        skill_catalog=skill_catalog,
        overrides_doc=inputs.overrides_doc,
        extension_doc=inputs.extension_doc,
        policy_doc=inputs.policy_doc,
    )


def build_generated_file_texts(
    inputs: ExportBuildInputs,
    documents: ExportBuildDocuments,
    portable_root: pathlib.Path,
) -> dict[pathlib.Path, str]:
    resolved_profiles = resolve_pack_profiles(inputs.profiles_doc, documents.catalog_full)
    mcp_manifest = build_mcp_dependency_manifest(documents.catalog_full, documents.openai_docs)
    generated_dir = inputs.generated_dir
    file_texts = {
        generated_dir / "agent_skill_catalog.json": json.dumps(
            documents.catalog_full, ensure_ascii=False, indent=2
        )
        + "\n",
        generated_dir / "agent_skill_catalog.min.json": json.dumps(
            documents.catalog_min, ensure_ascii=False, separators=(",", ":")
        )
        + "\n",
        generated_dir / "portable_export_map.json": json.dumps(
            documents.export_map, ensure_ascii=False, indent=2
        )
        + "\n",
        generated_dir / "skill_pack_profiles.resolved.json": json.dumps(
            resolved_profiles, ensure_ascii=False, indent=2
        )
        + "\n",
        generated_dir / "mcp_dependency_manifest.json": json.dumps(
            mcp_manifest, ensure_ascii=False, indent=2
        )
        + "\n",
    }
    release_manifest = release_manifest_contract.build_release_manifest(
        inputs.repo_root,
        portable_root=portable_root,
        file_overrides=file_texts,
    )
    file_texts[generated_dir / "release_manifest.json"] = json.dumps(
        release_manifest, ensure_ascii=False, indent=2
    ) + "\n"
    return file_texts


def write_generated_file_texts(file_texts: dict[pathlib.Path, str]) -> None:
    for path, content in file_texts.items():
        write_text_file(path, content)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Path to the aoa-skills repository root")
    parser.add_argument(
        "--output-root",
        default=None,
        help=(
            "Optional new or empty external consumer skill root. Without it, "
            "portable bytes are staged temporarily only to build deterministic metadata."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = pathlib.Path(args.repo_root).resolve()
    inputs = load_export_build_inputs(repo_root)
    if args.output_root:
        skills_root = pathlib.Path(args.output_root).resolve()
        prepare_skills_root(repo_root, skills_root)
        documents = build_portable_skill_exports(inputs, skills_root)
        inputs.generated_dir.mkdir(exist_ok=True)
        write_generated_file_texts(
            build_generated_file_texts(inputs, documents, skills_root)
        )
        print(
            f"built {len(documents.catalog_full['skills'])} portable skills "
            f"into explicit consumer root {skills_root}"
        )
        return 0

    with tempfile.TemporaryDirectory(prefix="aoa-skills-portable-") as temp_dir:
        skills_root = pathlib.Path(temp_dir)
        documents = build_portable_skill_exports(inputs, skills_root)
        inputs.generated_dir.mkdir(exist_ok=True)
        write_generated_file_texts(
            build_generated_file_texts(inputs, documents, skills_root)
        )
    print(
        f"built metadata for {len(documents.catalog_full['skills'])} skills "
        "from a temporary portable assembly"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
