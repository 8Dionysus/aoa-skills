"""Deterministic completeness checks for committed skill evidence readouts.

The evaluation matrix is the generated source for the current skill set and
its status/scope classification. Quality and promotion reports remain advisory,
but a committed report must not silently omit current skills or describe an old
classification.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


MATRIX_PATH = "generated/skill_evaluation_matrix.json"
READOUT_SPECS = (
    (
        "generated/skill_quality_audit.json",
        "generated/skill_quality_audit.md",
    ),
    (
        "generated/skill_promotion_pressure.json",
        "generated/skill_promotion_pressure.md",
    ),
)
PARITY_FIELDS = ("status", "scope")
CLAIM_LIMIT = (
    "This gate validates committed JSON skill membership and status/scope parity "
    "plus Markdown skill/status projection; "
    "it does not validate live usage, session, dispatch, hook, reality-trial, "
    "or technique-drift freshness."
)
SKILL_COUNT_RE = re.compile(r"^- skill count: (?P<count>\d+)$", re.MULTILINE)
SKILL_ROW_RE = re.compile(
    r"^\| `(?P<name>[^`]+)` \| `(?P<status>[^`]+)` \|",
    re.MULTILINE,
)


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


@dataclass(frozen=True)
class ValidationSummary:
    expected_skill_count: int
    issues: tuple[ValidationIssue, ...]


def load_object(
    repo_root: Path,
    rel_path: str,
    issues: list[ValidationIssue],
) -> dict[str, Any] | None:
    path = repo_root / rel_path
    if not path.is_file():
        issues.append(ValidationIssue(rel_path, "required generated readout is missing"))
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(ValidationIssue(rel_path, f"could not read JSON: {exc}"))
        return None
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(rel_path, "document root must be an object"))
        return None
    return payload


def index_skills(
    payload: dict[str, Any],
    *,
    location: str,
    issues: list[ValidationIssue],
) -> dict[str, dict[str, Any]]:
    entries = payload.get("skills")
    if not isinstance(entries, list):
        issues.append(ValidationIssue(location, "skills must be a list"))
        return {}

    by_name: dict[str, dict[str, Any]] = {}
    duplicates: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            issues.append(ValidationIssue(location, f"skills[{index}] must be an object"))
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            issues.append(
                ValidationIssue(location, f"skills[{index}].name must be a non-empty string")
            )
            continue
        if name in by_name:
            duplicates.add(name)
            continue
        by_name[name] = entry

    if duplicates:
        issues.append(
            ValidationIssue(location, f"duplicate skill names: {', '.join(sorted(duplicates))}")
        )
    return by_name


def validate_matrix(
    payload: dict[str, Any],
    issues: list[ValidationIssue],
) -> dict[str, dict[str, Any]]:
    expected = index_skills(payload, location=MATRIX_PATH, issues=issues)
    for name, entry in expected.items():
        for field in PARITY_FIELDS:
            if not isinstance(entry.get(field), str) or not entry[field]:
                issues.append(
                    ValidationIssue(
                        MATRIX_PATH,
                        f"{name} {field} must be a non-empty string",
                    )
                )
    return expected


def validate_readout(
    payload: dict[str, Any],
    *,
    location: str,
    expected: dict[str, dict[str, Any]],
    issues: list[ValidationIssue],
) -> None:
    expected_count = len(expected)
    skill_count = payload.get("skill_count")
    if isinstance(skill_count, bool) or not isinstance(skill_count, int):
        issues.append(ValidationIssue(location, "skill_count must be an integer"))
    elif skill_count != expected_count:
        issues.append(
            ValidationIssue(
                location,
                f"skill_count must equal evaluation matrix count {expected_count}; got {skill_count}",
            )
        )

    actual = index_skills(payload, location=location, issues=issues)
    missing = sorted(set(expected) - set(actual))
    unexpected = sorted(set(actual) - set(expected))
    if missing:
        issues.append(ValidationIssue(location, f"missing skills: {', '.join(missing)}"))
    if unexpected:
        issues.append(ValidationIssue(location, f"unexpected skills: {', '.join(unexpected)}"))

    for name in sorted(set(expected) & set(actual)):
        for field in PARITY_FIELDS:
            expected_value = expected[name].get(field)
            actual_value = actual[name].get(field)
            if actual_value != expected_value:
                issues.append(
                    ValidationIssue(
                        location,
                        f"{name} {field} must be {expected_value!r}; got {actual_value!r}",
                    )
                )


def validate_markdown_projection(
    repo_root: Path,
    *,
    markdown_path: str,
    json_payload: dict[str, Any],
    json_skills: dict[str, dict[str, Any]],
    issues: list[ValidationIssue],
) -> None:
    path = repo_root / markdown_path
    if not path.is_file():
        issues.append(ValidationIssue(markdown_path, "required generated readout is missing"))
        return
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        issues.append(ValidationIssue(markdown_path, f"could not read Markdown: {exc}"))
        return

    count_match = SKILL_COUNT_RE.search(text)
    if count_match is None:
        issues.append(ValidationIssue(markdown_path, "skill count line is missing or invalid"))
    else:
        markdown_count = int(count_match.group("count"))
        json_count = json_payload.get("skill_count")
        if markdown_count != json_count:
            issues.append(
                ValidationIssue(
                    markdown_path,
                    f"skill count must equal JSON skill_count {json_count}; got {markdown_count}",
                )
            )

    marker = "## Skill Matrix"
    if marker not in text:
        issues.append(ValidationIssue(markdown_path, "Skill Matrix section is missing"))
        return
    matrix_text = text.split(marker, 1)[1]
    markdown_skills: dict[str, str] = {}
    duplicates: set[str] = set()
    for match in SKILL_ROW_RE.finditer(matrix_text):
        name = match.group("name")
        if name in markdown_skills:
            duplicates.add(name)
            continue
        markdown_skills[name] = match.group("status")
    if duplicates:
        issues.append(
            ValidationIssue(
                markdown_path,
                f"duplicate skill names: {', '.join(sorted(duplicates))}",
            )
        )

    missing = sorted(set(json_skills) - set(markdown_skills))
    unexpected = sorted(set(markdown_skills) - set(json_skills))
    if missing:
        issues.append(ValidationIssue(markdown_path, f"missing skills: {', '.join(missing)}"))
    if unexpected:
        issues.append(
            ValidationIssue(markdown_path, f"unexpected skills: {', '.join(unexpected)}")
        )
    for name in sorted(set(json_skills) & set(markdown_skills)):
        expected_status = json_skills[name].get("status")
        if markdown_skills[name] != expected_status:
            issues.append(
                ValidationIssue(
                    markdown_path,
                    f"{name} status must be {expected_status!r}; got {markdown_skills[name]!r}",
                )
            )


def validate_summary(repo_root: Path) -> ValidationSummary:
    issues: list[ValidationIssue] = []
    matrix = load_object(repo_root, MATRIX_PATH, issues)
    expected = validate_matrix(matrix, issues) if matrix is not None else {}
    for json_path, markdown_path in READOUT_SPECS:
        readout = load_object(repo_root, json_path, issues)
        if readout is not None:
            validate_readout(
                readout,
                location=json_path,
                expected=expected,
                issues=issues,
            )
            json_skills = index_skills(readout, location=json_path, issues=[])
            validate_markdown_projection(
                repo_root,
                markdown_path=markdown_path,
                json_payload=readout,
                json_skills=json_skills,
                issues=issues,
            )
    return ValidationSummary(len(expected), tuple(issues))


def validate(repo_root: Path) -> list[ValidationIssue]:
    return list(validate_summary(repo_root).issues)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate completeness of committed skill quality and promotion readouts."
    )
    parser.add_argument("--repo-root", default=".", help="aoa-skills repository root")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable verdict")
    return parser.parse_args(argv)


def main_validate(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    summary = validate_summary(Path(args.repo_root).resolve())
    payload = {
        "status": "ok" if not summary.issues else "fail",
        "expected_skill_count": summary.expected_skill_count,
        "issue_count": len(summary.issues),
        "issues": [
            {"location": issue.location, "message": issue.message}
            for issue in summary.issues
        ],
        "claim_limit": CLAIM_LIMIT,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif summary.issues:
        for issue in summary.issues:
            print(f"{issue.location}: {issue.message}")
    else:
        print(
            "validated committed skill evidence readout membership and "
            f"status/scope parity for {summary.expected_skill_count} skills"
        )
    return 0 if not summary.issues else 1
