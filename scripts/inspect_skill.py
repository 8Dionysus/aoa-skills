#!/usr/bin/env python3
"""Read-only inspect CLI for local aoa-skills runtime surfaces."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import build_catalog
import skill_runtime_surface


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR_NAME = "skills"
SUPPORTED_VIEWS = {"capsule", "sections", "full", "walkthrough", "evidence"}
SUPPORTED_FORMATS = {"text", "json"}


class InspectSkillError(ValueError):
    pass


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect a local aoa-skills bundle surface.")
    parser.add_argument("--skill", required=True, help="Skill directory name.")
    parser.add_argument(
        "--view",
        default="walkthrough",
        help="One of: capsule, sections, full, walkthrough, evidence.",
    )
    parser.add_argument(
        "--format",
        default="text",
        help="One of: text, json.",
    )
    return parser.parse_args(argv)


def relative_location(path: Path, repo_root: Path) -> str:
    return build_catalog.relative_path(path, repo_root)


def load_json_file(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise InspectSkillError(f"missing required generated artifact at {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise InspectSkillError(f"invalid JSON in {path}: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise InspectSkillError(f"generated artifact at {path} must parse to an object")
    return payload


def find_named_entry(payload: Mapping[str, Any], skill_name: str) -> Mapping[str, Any]:
    skills = payload.get("skills", [])
    if not isinstance(skills, list):
        raise InspectSkillError("generated artifact field 'skills' must be a list")
    for entry in skills:
        if isinstance(entry, Mapping) and entry.get("name") == skill_name:
            return entry
    raise InspectSkillError(f"unknown skill '{skill_name}'")


def selected_support_artifact(entry: Mapping[str, Any]) -> Mapping[str, Any] | None:
    support_artifacts = entry.get("support_artifacts", [])
    if not isinstance(support_artifacts, list):
        return None
    for artifact in support_artifacts:
        if isinstance(artifact, Mapping) and artifact.get("selected_for_runtime_inspection"):
            return artifact
    return None


def resolve_view_payload(
    repo_root: Path,
    skill_name: str,
    view_name: str,
) -> Mapping[str, Any]:
    skill_path = repo_root / SKILLS_DIR_NAME / skill_name / "SKILL.md"
    if view_name not in SUPPORTED_VIEWS:
        raise InspectSkillError(f"unknown view '{view_name}'")

    if view_name == "full":
        if not skill_path.is_file():
            raise InspectSkillError(f"unknown skill '{skill_name}'")
        return {
            "name": skill_name,
            "skill_path": relative_location(skill_path, repo_root),
            "content_markdown": skill_path.read_text(encoding="utf-8"),
        }

    if view_name == "capsule":
        payload = load_json_file(repo_root / build_catalog.CAPSULE_PATH)
        return find_named_entry(payload, skill_name)

    if view_name == "sections":
        payload = load_json_file(repo_root / build_catalog.SECTIONS_PATH)
        return find_named_entry(payload, skill_name)

    walkthrough_payload = load_json_file(repo_root / build_catalog.WALKTHROUGHS_JSON_PATH)
    try:
        walkthrough_entry = skill_runtime_surface.find_skill_walkthrough_entry(
            walkthrough_payload,
            skill_name,
        )
    except KeyError as exc:
        raise InspectSkillError(f"unknown skill '{skill_name}'") from exc
    if view_name == "walkthrough":
        return walkthrough_entry
    return {
        "name": walkthrough_entry["name"],
        "skill_path": walkthrough_entry["skill_path"],
        "support_artifacts": walkthrough_entry.get("support_artifacts", []),
        "selected_runtime_artifact": selected_support_artifact(walkthrough_entry),
    }


def render_list(title: str, values: Sequence[Any]) -> list[str]:
    lines = [title]
    if values:
        for value in values:
            lines.append(f"- {value}")
    else:
        lines.append("- none")
    return lines


def render_capsule_text(entry: Mapping[str, Any]) -> str:
    lines = [
        f"# {entry['name']}",
        "",
        f"scope: {entry['scope']}",
        f"status: {entry['status']}",
        f"invocation mode: {entry['invocation_mode']}",
        f"skill path: {entry['skill_path']}",
        "",
        f"summary: {entry['summary']}",
        f"trigger boundary: {entry['trigger_boundary_short']}",
        f"inputs: {entry['inputs_short']}",
        f"outputs: {entry['outputs_short']}",
        f"workflow: {entry['workflow_short']}",
        f"anti-patterns: {entry['main_anti_patterns_short']}",
        f"verification: {entry['verification_short']}",
    ]
    return "\n".join(lines)


def render_sections_text(entry: Mapping[str, Any]) -> str:
    lines = [
        f"# {entry['name']}",
        "",
        f"scope: {entry['scope']}",
        f"status: {entry['status']}",
        f"skill path: {entry['skill_path']}",
        "",
    ]
    sections = entry.get("sections", [])
    if not isinstance(sections, list):
        raise InspectSkillError("sections entry field 'sections' must be a list")
    for section in sections:
        if not isinstance(section, Mapping):
            continue
        lines.extend(
            [
                f"## {section.get('heading')}",
                "",
                str(section.get("content_markdown", "")).rstrip(),
                "",
            ]
        )
    return "\n".join(lines).rstrip()


def render_walkthrough_text(entry: Mapping[str, Any]) -> str:
    lines = [
        f"# {entry['name']}",
        "",
        f"scope: {entry['scope']}",
        f"status: {entry['status']}",
        f"invocation mode: {entry['invocation_mode']}",
        f"skill path: {entry['skill_path']}",
        "",
        f"pick summary: {entry['pick_summary']}",
        "",
    ]
    lines.extend(render_list("Use when", entry.get("use_when", [])))
    lines.append("")
    lines.extend(render_list("Do not use when", entry.get("do_not_use_when", [])))
    lines.append("")
    lines.extend(render_list("Inspection order", entry.get("inspection_order", [])))
    lines.append("")
    lines.extend(render_list("Expand sections", entry.get("expand_sections", [])))
    lines.append("")
    lines.extend(render_list("Object use shape", entry.get("object_use_shape", [])))
    lines.append("")
    lines.append("Support artifacts")
    support_artifacts = entry.get("support_artifacts", [])
    if isinstance(support_artifacts, list) and support_artifacts:
        for artifact in support_artifacts:
            if not isinstance(artifact, Mapping):
                continue
            selection_suffix = ""
            if artifact.get("selected_for_runtime_inspection"):
                selection_suffix = " (selected)"
            lines.append(
                f"- {artifact.get('type')}{selection_suffix}: {artifact.get('path')}"
            )
    else:
        lines.append("- none")
    return "\n".join(lines)


def render_evidence_text(entry: Mapping[str, Any]) -> str:
    lines = [
        f"# {entry['name']}",
        "",
        f"skill path: {entry['skill_path']}",
        "",
        "Support artifacts",
    ]
    support_artifacts = entry.get("support_artifacts", [])
    if isinstance(support_artifacts, list) and support_artifacts:
        for artifact in support_artifacts:
            if not isinstance(artifact, Mapping):
                continue
            selection_suffix = ""
            if artifact.get("selected_for_runtime_inspection"):
                selection_suffix = " (selected)"
            lines.append(
                f"- {artifact.get('type')}{selection_suffix}: {artifact.get('path')}"
            )
    else:
        lines.append("- none")

    selected_artifact = entry.get("selected_runtime_artifact")
    if isinstance(selected_artifact, Mapping):
        lines.extend(
            [
                "",
                f"Selected runtime artifact: {selected_artifact.get('path')}",
            ]
        )
    return "\n".join(lines)


def render_text(view_name: str, payload: Mapping[str, Any]) -> str:
    if view_name == "full":
        return str(payload["content_markdown"]).rstrip()
    if view_name == "capsule":
        return render_capsule_text(payload)
    if view_name == "sections":
        return render_sections_text(payload)
    if view_name == "walkthrough":
        return render_walkthrough_text(payload)
    if view_name == "evidence":
        return render_evidence_text(payload)
    raise InspectSkillError(f"unknown view '{view_name}'")


def render_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        if args.view not in SUPPORTED_VIEWS:
            raise InspectSkillError(f"unknown view '{args.view}'")
        if args.format not in SUPPORTED_FORMATS:
            raise InspectSkillError(f"unknown format '{args.format}'")

        payload = resolve_view_payload(repo_root, args.skill, args.view)
        if args.format == "json":
            sys.stdout.write(render_json(payload))
        else:
            sys.stdout.write(render_text(args.view, payload) + "\n")
    except InspectSkillError as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive runtime guard
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
