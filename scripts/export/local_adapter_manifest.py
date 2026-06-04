"""Build local-adapter manifests from the portable Agent Skills catalog."""

from __future__ import annotations

import pathlib
from typing import Any

import yaml


def path_reference(path: pathlib.Path, repo_root: pathlib.Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


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


def build_local_adapter_manifests(
    *,
    repo_root: pathlib.Path,
    skills_root: pathlib.Path,
    catalog_full: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    root = path_reference(skills_root, repo_root)
    contracts = {
        "runtime": "generated/skill_runtime_contracts.json",
        "context_retention": "generated/context_retention_manifest.json",
        "trust_policy": "generated/trust_policy_matrix.json",
    }
    manifest: dict[str, Any] = {
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
    manifest_min: dict[str, Any] = {
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
                "implicit_activation_policy": entry["implicit_activation_policy"],
                "invocation_mode": entry["invocation_mode"],
                "allowlist_paths": [path_reference(skills_root / entry["name"], repo_root)],
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
                "implicit_activation_policy": entry["implicit_activation_policy"],
                "trust_posture": entry["trust_posture"],
            }
        )
    return manifest, manifest_min
