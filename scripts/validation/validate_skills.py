#!/usr/bin/env python3
"""Validate authored AoA skill bundles without claiming behavioral quality."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

import yaml
from jsonschema import Draft202012Validator

from skill_model import capability_system, skill_source_model


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def validate_source_skills(repo_root: Path) -> list[str]:
    errors: list[str] = []
    schema = load_json(repo_root / "schemas" / "skill-frontmatter.schema.json")
    validator = Draft202012Validator(schema)
    sources = skill_source_model.load_skill_sources(repo_root)
    source_by_name: dict[str, skill_source_model.SkillSource] = {}
    for source in sources:
        rel_path = source.skill_md_path.relative_to(repo_root).as_posix()
        if source.name in source_by_name:
            errors.append(f"duplicate skill identity {source.name!r}")
            continue
        source_by_name[source.name] = source
        for issue in sorted(
            validator.iter_errors(source.metadata), key=lambda item: list(item.absolute_path)
        ):
            location = "/".join(str(part) for part in issue.absolute_path) or "<root>"
            errors.append(f"{rel_path} {location}: {issue.message}")
        if source.metadata.get("name") != source.skill_dir.name:
            errors.append(f"{rel_path}: frontmatter name must match bundle directory")
        if "technique_dependencies" in source.metadata:
            errors.append(f"{rel_path}: retired technique_dependencies field is forbidden")
        techniques_path = source.skill_dir / "techniques.yaml"
        if techniques_path.exists():
            errors.append(
                f"{techniques_path.relative_to(repo_root)}: techniques.yaml is no longer a runtime skill contract"
            )
        if not source.body.strip():
            errors.append(f"{rel_path}: skill body must not be empty")
        for heading, content in source.sections.items():
            if not content.strip():
                errors.append(f"{rel_path}: section {heading!r} must not be empty")
        line_count = len(source.skill_md_path.read_text(encoding="utf-8").splitlines())
        if line_count > 500:
            errors.append(f"{rel_path}: {line_count} lines exceeds the 500-line portable skill limit")
        openai_path = source.skill_dir / "agents" / "openai.yaml"
        if not openai_path.is_file():
            errors.append(f"{rel_path}: missing agents/openai.yaml activation adapter")
            continue
        openai_doc = yaml.safe_load(openai_path.read_text(encoding="utf-8")) or {}
        if not isinstance(openai_doc, dict) or not isinstance(openai_doc.get("policy"), dict):
            errors.append(f"{openai_path.relative_to(repo_root)}: policy mapping is required")

    try:
        families = capability_system.validate_sources(repo_root)
        graph_nodes = capability_system.node_map(families)
    except (OSError, ValueError) as exc:
        errors.append(f"capability contract invalid: {exc}")
        return errors
    bound_skill_names = {
        node_id.removeprefix("skill.")
        for node_id, node in graph_nodes.items()
        if node.get("kind") == "skill"
        and isinstance(node.get("binding"), dict)
        and str(node["binding"].get("ref", "")).startswith("skills/")
    }
    if set(source_by_name) != bound_skill_names:
        errors.append(
            "source skill membership differs from local capability skill bindings: "
            f"source={sorted(source_by_name)!r}, capability={sorted(bound_skill_names)!r}"
        )
    return errors


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    try:
        errors = validate_source_skills(repo_root)
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"skill source validation failed: {exc}")
        return 2
    if errors:
        print("skill source validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("skill sources valid: structural and owner-contract checks only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
