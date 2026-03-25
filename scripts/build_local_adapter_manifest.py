#!/usr/bin/env python3
"""Build local-adapter manifests from the Codex-facing .agents/skills export."""

from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any

import yaml

RESOURCE_DIR_NAMES = ("scripts", "references", "assets")


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


def inventory_resources(skill_dir: pathlib.Path) -> dict[str, list[str]]:
    inventory: dict[str, list[str]] = {}
    for resource_dir_name in RESOURCE_DIR_NAMES:
        resource_dir = skill_dir / resource_dir_name
        if not resource_dir.exists():
            inventory[resource_dir_name] = []
            continue
        inventory[resource_dir_name] = sorted(
            str(path.relative_to(skill_dir).as_posix())
            for path in resource_dir.rglob("*")
            if path.is_file()
        )
    return inventory


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root containing .agents/skills")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    skills_root = repo_root / ".agents" / "skills"
    generated_dir = repo_root / "generated"
    generated_dir.mkdir(exist_ok=True)
    runtime_doc = load_json(generated_dir / "skill_runtime_contracts.json")
    runtime_by_name = {entry["name"]: entry for entry in runtime_doc.get("skills", [])}

    contracts = {
        "runtime": "generated/skill_runtime_contracts.json",
        "context_retention": "generated/context_retention_manifest.json",
        "trust_policy": "generated/trust_policy_matrix.json",
    }
    manifest: dict[str, Any] = {
        "manifest_version": 2,
        "profile": "codex-facing-local-adapter",
        "root": ".agents/skills",
        "activation_tool": "scripts/activate_skill.py",
        "discovery_view": "generated/local_adapter_manifest.min.json",
        "permission_allowlist": [".agents/skills"],
        "contracts": contracts,
        "source_of_truth": {
            "portable_export_root": ".agents/skills",
            "portable_catalog": "generated/agent_skill_catalog.json",
            "policy_source": "agents/openai.yaml",
        },
        "skills": [],
    }
    manifest_min: dict[str, Any] = {
        "manifest_version": 2,
        "profile": "codex-facing-local-adapter",
        "root": ".agents/skills",
        "activation_tool": "scripts/activate_skill.py",
        "contracts": contracts,
        "skills": [],
    }

    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        openai_yaml = skill_dir / "agents" / "openai.yaml"
        frontmatter, _ = parse_frontmatter(skill_md)
        openai_doc = yaml.safe_load(openai_yaml.read_text(encoding="utf-8")) or {}
        policy = openai_doc.get("policy", {}) if isinstance(openai_doc, dict) else {}
        allow_implicit = policy.get("allow_implicit_invocation")
        inventory = inventory_resources(skill_dir)
        runtime = runtime_by_name.get(frontmatter["name"], {})

        manifest["skills"].append(
            {
                "name": frontmatter["name"],
                "description": frontmatter["description"],
                "path": str(skill_md.relative_to(repo_root).as_posix()),
                "openai_config_path": str(openai_yaml.relative_to(repo_root).as_posix()),
                "allow_implicit_invocation": allow_implicit,
                "invocation_mode": frontmatter.get("metadata", {}).get("aoa_invocation_mode"),
                "allowlist_paths": [str(skill_dir.relative_to(repo_root).as_posix())],
                "resource_inventory": inventory,
                "metadata": frontmatter.get("metadata", {}),
                "trust_posture": runtime.get("trust_posture"),
                "context_retention_ref": runtime.get("context_retention_ref"),
            }
        )
        manifest_min["skills"].append(
            {
                "name": frontmatter["name"],
                "description": frontmatter["description"],
                "path": str(skill_md.relative_to(repo_root).as_posix()),
                "allow_implicit_invocation": allow_implicit,
                "trust_posture": runtime.get("trust_posture"),
            }
        )

    (generated_dir / "local_adapter_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (generated_dir / "local_adapter_manifest.min.json").write_text(json.dumps(manifest_min, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(manifest['skills'])} skills into local adapter manifests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
