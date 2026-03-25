#!/usr/bin/env python3
"""Activate a Codex-facing skill for local runtimes that need a tool seam."""

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


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root containing .agents/skills")
    parser.add_argument("--skill", required=True, help="Skill name to activate")
    parser.add_argument("--format", choices=("json", "markdown"), default="json", help="Output format")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    generated_dir = repo_root / "generated"
    skill_dir = repo_root / ".agents" / "skills" / args.skill
    skill_md = skill_dir / "SKILL.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not skill_md.exists():
        raise SystemExit(f"missing skill: {skill_md}")

    frontmatter, body = parse_frontmatter(skill_md)
    openai_doc = yaml.safe_load(openai_yaml.read_text(encoding="utf-8")) or {}
    inventory = inventory_resources(skill_dir)
    runtime_doc = load_json(generated_dir / "skill_runtime_contracts.json")
    context_doc = load_json(generated_dir / "context_retention_manifest.json")
    trust_doc = load_json(generated_dir / "trust_policy_matrix.json")
    runtime_by_name = {entry["name"]: entry for entry in runtime_doc.get("skills", [])}
    context_by_name = {entry["name"]: entry for entry in context_doc.get("skills", [])}
    trust_by_name = {entry["name"]: entry for entry in trust_doc.get("skills", [])}

    payload: dict[str, Any] = {
        "skill": {
            "name": frontmatter["name"],
            "description": frontmatter["description"],
            "path": str(skill_md.relative_to(repo_root).as_posix()),
            "invocation_mode": frontmatter.get("metadata", {}).get("aoa_invocation_mode"),
            "allow_implicit_invocation": openai_doc.get("policy", {}).get("allow_implicit_invocation"),
            "metadata": frontmatter.get("metadata", {}),
        },
        "resources": {
            "allowlist_paths": [str(skill_dir.relative_to(repo_root).as_posix())],
            "inventory": inventory,
        },
        "runtime_contract": runtime_by_name.get(frontmatter["name"]),
        "context_retention": context_by_name.get(frontmatter["name"]),
        "trust_policy": trust_by_name.get(frontmatter["name"]),
        "openai": openai_doc,
        "instructions_markdown": body.strip(),
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
        return 0

    lines = [
        f"# Skill activation: {payload['skill']['name']}",
        "",
        f"Description: {payload['skill']['description']}",
        f"Invocation mode: {payload['skill']['invocation_mode']}",
        f"Allow implicit invocation: {payload['skill']['allow_implicit_invocation']}",
        f"Path: {payload['skill']['path']}",
        f"Trust posture: {payload['trust_policy'].get('trust_posture') if payload['trust_policy'] else '(unknown)'}",
        "",
        "## Allowlist paths",
        *[f"- {path}" for path in payload["resources"]["allowlist_paths"]],
        "",
        "## Bundled resources",
    ]
    inventory_map = payload["resources"]["inventory"]
    for group_name in RESOURCE_DIR_NAMES:
        lines.append(f"### {group_name}")
        files = inventory_map[group_name]
        if files:
            lines.extend(f"- {item}" for item in files)
        else:
            lines.append("- (none)")
        lines.append("")
    if payload["context_retention"]:
        lines.extend(
            [
                "## Context retention",
                "",
                f"- Compact summary: {payload['context_retention']['compact_summary']}",
                f"- Retain sections: {', '.join(payload['context_retention']['retain_sections'])}",
                "",
            ]
        )
    lines.extend(["## Instructions", "", payload["instructions_markdown"]])
    print("\n".join(lines).rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
