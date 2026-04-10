from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


GENERATED_DIR_NAME = "generated"
SECTIONS_NAME = "skill_sections.full.json"
SECTION_VERSION = 1
SECTION_SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "sections": [
        "Intent",
        "Trigger boundary",
        "Inputs",
        "Outputs",
        "Procedure",
        "Contracts",
        "Risks and anti-patterns",
        "Verification",
        "Technique traceability",
        "Adaptation points",
    ],
}
CANONICAL_HEADINGS = tuple(SECTION_SOURCE_OF_TRUTH["sections"])
SECTION_KEY_BY_HEADING = {
    "Intent": "intent",
    "Trigger boundary": "trigger_boundary",
    "Inputs": "inputs",
    "Outputs": "outputs",
    "Procedure": "procedure",
    "Contracts": "contracts",
    "Risks and anti-patterns": "risks_and_anti_patterns",
    "Verification": "verification",
    "Technique traceability": "technique_traceability",
    "Adaptation points": "adaptation_points",
}
SECTION_HEADING_PATTERN = re.compile(r"^[ ]{0,3}##\s+(.+?)\s*$")


@dataclass(frozen=True)
class ContractIssue:
    location: str
    message: str


def relative_location(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def format_issues(issues: list[ContractIssue]) -> str:
    return "\n".join(f"- {issue.location}: {issue.message}" for issue in issues)


def trim_boundary_blank_lines(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def extract_top_level_sections(body: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_heading: str | None = None
    current_lines: list[str] = []
    normalized_body = body.replace("\r\n", "\n").replace("\r", "\n")

    def flush_current() -> None:
        nonlocal current_heading, current_lines
        if current_heading is None:
            return
        sections.append((current_heading, trim_boundary_blank_lines("\n".join(current_lines))))
        current_heading = None
        current_lines = []

    for line in normalized_body.split("\n"):
        heading_match = SECTION_HEADING_PATTERN.match(line)
        if heading_match:
            flush_current()
            current_heading = heading_match.group(1).strip()
            continue
        if current_heading is not None:
            current_lines.append(line)

    flush_current()
    return sections


def collect_section_contract_issues(
    section_pairs: list[tuple[str, str]],
    *,
    location: str,
) -> list[ContractIssue]:
    issues: list[ContractIssue] = []
    headings = [heading for heading, _content in section_pairs]
    heading_counts = Counter(headings)

    for heading in CANONICAL_HEADINGS:
        if heading_counts[heading] == 0:
            issues.append(ContractIssue(location, f"missing required section '{heading}'"))
        elif heading_counts[heading] > 1:
            issues.append(ContractIssue(location, f"duplicate top-level section '{heading}'"))

    for heading in headings:
        if heading not in SECTION_KEY_BY_HEADING:
            issues.append(ContractIssue(location, f"unexpected top-level section '{heading}'"))

    if headings != list(CANONICAL_HEADINGS):
        issues.append(
            ContractIssue(
                location,
                "top-level sections must match the canonical order exactly",
            )
        )

    for heading, content_markdown in section_pairs:
        if heading in SECTION_KEY_BY_HEADING and not content_markdown.strip():
            issues.append(ContractIssue(location, f"section '{heading}' must not be empty"))

    return issues


def build_section_entries(section_pairs: list[tuple[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "key": SECTION_KEY_BY_HEADING[heading],
            "heading": heading,
            "content_markdown": content_markdown,
        }
        for heading, content_markdown in section_pairs
        if heading in SECTION_KEY_BY_HEADING
    ]


def build_sections_entry(
    repo_root: Path,
    metadata: dict[str, Any],
    skill_md_path: Path,
    body: str,
) -> tuple[dict[str, Any] | None, list[ContractIssue]]:
    location = relative_location(skill_md_path, repo_root)
    section_pairs = extract_top_level_sections(body)
    issues = collect_section_contract_issues(section_pairs, location=location)
    for field in ("name", "scope", "status"):
        value = metadata.get(field)
        if not isinstance(value, str) or not value:
            issues.append(
                ContractIssue(location, f"frontmatter metadata.{field} must be a non-empty string")
            )
    if issues:
        return None, issues

    return (
        {
            "name": metadata["name"],
            "scope": metadata["scope"],
            "status": metadata["status"],
            "skill_path": relative_location(skill_md_path, repo_root),
            "sections": build_section_entries(section_pairs),
        },
        [],
    )
