#!/usr/bin/env python3
"""Preview or explicitly apply manifest-driven SKILL.md refreshes."""

from __future__ import annotations

import argparse
import difflib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR_NAME = "skills"
TRACEABILITY_HEADINGS = {
    "## Technique traceability",
    "## Future traceability",
}


@dataclass(frozen=True)
class RefreshResult:
    skill_name: str
    skill_md_path: Path
    proposed_text: str
    changed: bool
    diff: str


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview manifest-driven SKILL.md refreshes."
    )
    parser.add_argument(
        "--skill",
        help="Refresh-preview a single skill bundle by directory name.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Apply the refresh to one explicitly named skill. Requires --skill.",
    )
    return parser.parse_args(argv)


def discover_skill_names(repo_root: Path) -> list[str]:
    skills_dir = repo_root / SKILLS_DIR_NAME
    if not skills_dir.is_dir():
        raise FileNotFoundError(f"missing skills directory at {skills_dir}")
    return sorted(path.name for path in skills_dir.iterdir() if path.is_dir())


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def parse_skill_document(path: Path) -> tuple[dict[str, Any], list[str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path} is missing frontmatter")

    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        raise ValueError(f"{path} is missing a closing frontmatter delimiter")

    frontmatter_lines = lines[1:closing_index]
    frontmatter_text = "\n".join(frontmatter_lines)
    body_text = "\n".join(lines[closing_index + 1 :]).strip("\n")
    metadata = yaml.safe_load(frontmatter_text) or {}
    if not isinstance(metadata, dict):
        raise ValueError(f"{path} frontmatter must parse to a mapping")
    return metadata, frontmatter_lines, body_text


def replace_technique_dependencies(
    frontmatter_lines: list[str], technique_ids: list[str]
) -> list[str]:
    start_index = None
    end_index = len(frontmatter_lines)

    for index, line in enumerate(frontmatter_lines):
        if line.startswith("technique_dependencies:"):
            start_index = index
            for next_index in range(index + 1, len(frontmatter_lines)):
                next_line = frontmatter_lines[next_index]
                if next_line.startswith("  - "):
                    continue
                end_index = next_index
                break
            break

    if start_index is None:
        raise ValueError("frontmatter is missing technique_dependencies")

    replacement = ["technique_dependencies:"] + [
        f"  - {technique_id}" for technique_id in technique_ids
    ]
    return frontmatter_lines[:start_index] + replacement + frontmatter_lines[end_index:]


def build_traceability_lines(techniques: list[dict[str, Any]]) -> list[str]:
    lines = ["Manifest-backed techniques:"]
    for technique in techniques:
        sections = ", ".join(technique["use_sections"])
        lines.append(
            "- "
            f"{technique['id']} from `{technique['repo']}` at `{technique['source_ref']}` "
            f"using path `{technique['path']}` and sections: {sections}"
        )
    return lines


def replace_traceability_section(body_text: str, techniques: list[dict[str, Any]]) -> str:
    lines = body_text.splitlines()
    start_index = None
    end_index = len(lines)

    for index, line in enumerate(lines):
        if line.strip() in TRACEABILITY_HEADINGS:
            start_index = index
            for next_index in range(index + 1, len(lines)):
                if lines[next_index].startswith("## "):
                    end_index = next_index
                    break
            break

    if start_index is None:
        raise ValueError("skill body is missing a traceability section")

    new_section = ["## Technique traceability", "", *build_traceability_lines(techniques), ""]
    updated_lines = lines[:start_index] + new_section + lines[end_index:]
    return "\n".join(updated_lines).strip() + "\n"


def render_skill_document(frontmatter_lines: list[str], body_text: str) -> str:
    return (
        "---\n"
        + "\n".join(frontmatter_lines).strip()
        + "\n---\n\n"
        + body_text.strip()
        + "\n"
    )


def write_skill_document(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def relative_path(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def build_refresh_result(repo_root: Path, skill_name: str) -> RefreshResult:
    skill_dir = repo_root / SKILLS_DIR_NAME / skill_name
    skill_md_path = skill_dir / "SKILL.md"
    manifest_path = skill_dir / "techniques.yaml"

    _, frontmatter_lines, body_text = parse_skill_document(skill_md_path)
    manifest = load_yaml(manifest_path)
    if not isinstance(manifest, dict) or not isinstance(manifest.get("techniques"), list):
        raise ValueError(f"{manifest_path} must contain a techniques list")

    proposed_frontmatter_lines = replace_technique_dependencies(
        frontmatter_lines,
        [
            technique["id"] for technique in manifest["techniques"]
        ],
    )
    proposed_body = replace_traceability_section(body_text, manifest["techniques"])
    current_text = skill_md_path.read_text(encoding="utf-8")
    proposed_text = render_skill_document(proposed_frontmatter_lines, proposed_body)

    diff_lines = list(
        difflib.unified_diff(
            current_text.splitlines(),
            proposed_text.splitlines(),
            fromfile=f"current/{relative_path(skill_md_path, repo_root)}",
            tofile=f"proposed/{relative_path(skill_md_path, repo_root)}",
            lineterm="",
        )
    )
    return RefreshResult(
        skill_name=skill_name,
        skill_md_path=skill_md_path,
        proposed_text=proposed_text,
        changed=bool(diff_lines),
        diff="\n".join(diff_lines),
    )


def build_report(results: list[RefreshResult]) -> str:
    blocks: list[str] = []
    for result in results:
        if result.changed:
            blocks.append(
                f"Skill: {result.skill_name}\nStatus: needs refresh\n{result.diff}"
            )
        else:
            blocks.append(f"Skill: {result.skill_name}\nStatus: already aligned")
    return "\n\n".join(blocks)


def build_write_report(result: RefreshResult, repo_root: Path) -> str:
    if result.changed:
        return (
            f"Skill: {result.skill_name}\n"
            "Status: refreshed\n"
            f"Updated: {relative_path(result.skill_md_path, repo_root)}"
        )
    return f"Skill: {result.skill_name}\nStatus: already aligned"


def run_refresh_preview(repo_root: Path, skill_name: str | None = None) -> list[RefreshResult]:
    all_skill_names = discover_skill_names(repo_root)
    if skill_name is not None:
        if skill_name not in all_skill_names:
            raise ValueError(f"unknown skill '{skill_name}'")
        target_skills = [skill_name]
    else:
        target_skills = all_skill_names

    return [build_refresh_result(repo_root, name) for name in target_skills]


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        if args.write:
            if args.skill is None:
                print(
                    "Runtime error: write mode requires --skill so the first write "
                    "contract stays bounded to a single bundle.",
                    file=sys.stderr,
                )
                return 2

            result = run_refresh_preview(repo_root, skill_name=args.skill)[0]
            if result.changed:
                write_skill_document(result.skill_md_path, result.proposed_text)
            print(build_write_report(result, repo_root))
            return 0

        results = run_refresh_preview(repo_root, skill_name=args.skill)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive runtime guard
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2

    print(build_report(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
