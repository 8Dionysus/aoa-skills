"""Validate the authored whole-family skill-effectiveness disposition review.

The review is a governance record over current source bundles. Its live and
session-derived episode references remain reviewed candidate evidence only;
this validator does not turn them into proof, promotion, or runtime authority.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any, Sequence

from jsonschema import Draft202012Validator

from skill_model import skill_layout, skill_source_model


REVIEW_PATH = "docs/reviews/skill-effectiveness/aoa-family-current.json"
SCHEMA_PATH = (
    "mechanics/method-growth/schemas/skill_effectiveness_family_review_v1.json"
)
DISPOSITIONS = ("improve", "split", "merge", "promote", "retain", "retire")
STATUS_ORDER = {
    "scaffold": 0,
    "linked": 1,
    "reviewed": 2,
    "evaluated": 3,
    "canonical": 4,
    "deprecated": 5,
}
CLAIM_LIMIT = (
    "This gate validates an authored, source-exact family disposition record. "
    "Referenced session and live-dispatch episodes remain reviewed candidate "
    "evidence; the record is not proof, promotion, or runtime authority."
)
URI_OR_DRIVE = re.compile(r"^(?:[A-Za-z][A-Za-z0-9+.-]*:|[A-Za-z]:[\\/])")


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


@dataclass(frozen=True)
class ValidationSummary:
    expected_skill_count: int
    reviewed_skill_count: int
    issues: tuple[ValidationIssue, ...]


def _load_object(path: Path, issues: list[ValidationIssue]) -> dict[str, Any] | None:
    location = path.as_posix()
    if not path.is_file():
        issues.append(ValidationIssue(location, "required file is missing"))
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(ValidationIssue(location, f"could not read JSON: {exc}"))
        return None
    if not isinstance(value, dict):
        issues.append(ValidationIssue(location, "document root must be an object"))
        return None
    return value


def _source_index(repo_root: Path, issues: list[ValidationIssue]) -> dict[str, dict[str, str]]:
    try:
        bundles = skill_layout.discover_skill_bundle_paths(repo_root)
    except (FileNotFoundError, ValueError) as exc:
        issues.append(ValidationIssue("skills", str(exc)))
        return {}

    sources: dict[str, dict[str, str]] = {}
    for bundle in bundles:
        try:
            metadata, _ = skill_source_model.parse_skill_document(bundle.skill_md_path)
        except (OSError, ValueError) as exc:
            issues.append(
                ValidationIssue(bundle.skill_md_path.as_posix(), f"could not read source: {exc}")
            )
            continue
        sources[bundle.name] = {
            "skill_path": bundle.skill_md_path.relative_to(repo_root).as_posix(),
            "scope": str(metadata.get("scope", "")),
            "source_status": str(metadata.get("status", "")),
        }
    return sources


def _schema_issues(
    repo_root: Path,
    payload: dict[str, Any],
    issues: list[ValidationIssue],
) -> None:
    schema = _load_object(repo_root / SCHEMA_PATH, issues)
    if schema is None:
        return
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes several schema error subclasses
        issues.append(ValidationIssue(SCHEMA_PATH, f"invalid JSON Schema: {exc}"))
        return
    errors = sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    for error in errors:
        suffix = ".".join(str(part) for part in error.absolute_path)
        location = REVIEW_PATH if not suffix else f"{REVIEW_PATH}:{suffix}"
        issues.append(ValidationIssue(location, error.message))


def _index_entries(
    payload: dict[str, Any], issues: list[ValidationIssue]
) -> dict[str, dict[str, Any]]:
    entries = payload.get("entries")
    if not isinstance(entries, list):
        return {}
    by_name: dict[str, dict[str, Any]] = {}
    duplicates: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            continue
        if name in by_name:
            duplicates.add(name)
        else:
            by_name[name] = entry
    if duplicates:
        issues.append(
            ValidationIssue(REVIEW_PATH, f"duplicate skill names: {', '.join(sorted(duplicates))}")
        )
    return by_name


def _validate_source_parity(
    sources: dict[str, dict[str, str]],
    entries: dict[str, dict[str, Any]],
    issues: list[ValidationIssue],
) -> None:
    missing = sorted(set(sources) - set(entries))
    unexpected = sorted(set(entries) - set(sources))
    if missing:
        issues.append(ValidationIssue(REVIEW_PATH, f"missing skills: {', '.join(missing)}"))
    if unexpected:
        issues.append(ValidationIssue(REVIEW_PATH, f"unexpected skills: {', '.join(unexpected)}"))
    for name in sorted(set(sources) & set(entries)):
        for field in ("skill_path", "scope", "source_status"):
            actual = entries[name].get(field)
            expected = sources[name][field]
            if actual != expected:
                issues.append(
                    ValidationIssue(
                        f"{REVIEW_PATH}:{name}.{field}",
                        f"must match source value {expected!r}; got {actual!r}",
                    )
                )


def _validate_decisions(
    payload: dict[str, Any],
    entries: dict[str, dict[str, Any]],
    sources: dict[str, dict[str, str]],
    issues: list[ValidationIssue],
) -> None:
    actual = Counter(
        entry.get("disposition")
        for entry in entries.values()
        if entry.get("disposition") in DISPOSITIONS
    )
    counts = payload.get("decision_counts")
    if isinstance(counts, dict):
        for disposition in DISPOSITIONS:
            if counts.get(disposition) != actual[disposition]:
                issues.append(
                    ValidationIssue(
                        f"{REVIEW_PATH}:decision_counts.{disposition}",
                        f"must equal entry count {actual[disposition]}",
                    )
                )
    for name, entry in entries.items():
        disposition = entry.get("disposition")
        if entry.get("nearest_alternative_rejected") == disposition:
            issues.append(
                ValidationIssue(
                    f"{REVIEW_PATH}:{name}.nearest_alternative_rejected",
                    "must differ from the chosen disposition",
                )
            )
        if disposition == "merge" and entry.get("merge_target") == name:
            issues.append(
                ValidationIssue(f"{REVIEW_PATH}:{name}.merge_target", "cannot target itself")
            )
        if disposition == "merge" and entry.get("merge_target") not in sources:
            issues.append(
                ValidationIssue(
                    f"{REVIEW_PATH}:{name}.merge_target", "must name a current skill"
                )
            )
        if disposition == "promote":
            current = STATUS_ORDER.get(str(entry.get("source_status")))
            target = STATUS_ORDER.get(str(entry.get("target_status")))
            state = entry.get("action_state")
            if current is not None and target is not None:
                allowed = target > current or (state == "landed" and target == current)
                if not allowed:
                    issues.append(
                        ValidationIssue(
                            f"{REVIEW_PATH}:{name}.target_status",
                            "must advance source status, or equal it after a landed promotion",
                        )
                    )


def _unsafe_ref_reason(ref: str) -> str | None:
    if not ref or ref.startswith(("/", "~")):
        return "must be a non-empty repository-relative path"
    if "\\" in ref or URI_OR_DRIVE.match(ref):
        return "must not be a URI, drive path, or backslash path"
    parts = PurePosixPath(ref).parts
    if any(part in {"", ".", ".."} for part in parts):
        return "must not contain empty, dot, or parent-traversal components"
    if any(part in {".aoa", ".codex"} for part in parts):
        return "must not reference raw session or private Codex surfaces"
    return None


def _validate_ref(
    repo_root: Path,
    ref: Any,
    location: str,
    issues: list[ValidationIssue],
    *,
    episode: bool = False,
) -> None:
    if not isinstance(ref, str):
        return
    reason = _unsafe_ref_reason(ref)
    if reason is not None:
        issues.append(ValidationIssue(location, reason))
        return
    if episode and not ref.startswith("evals/reports/"):
        issues.append(
            ValidationIssue(location, "episode refs must use public reviewed evals/reports JSON")
        )
        return
    path = repo_root / ref
    if not path.is_file():
        issues.append(ValidationIssue(location, f"referenced repository file is missing: {ref}"))


def _validate_refs(
    repo_root: Path, payload: dict[str, Any], entries: dict[str, dict[str, Any]], issues: list[ValidationIssue]
) -> None:
    for index, ref in enumerate(payload.get("source_refs", [])):
        _validate_ref(repo_root, ref, f"{REVIEW_PATH}:source_refs[{index}]", issues)
    for name, entry in entries.items():
        _validate_ref(repo_root, entry.get("skill_path"), f"{REVIEW_PATH}:{name}.skill_path", issues)
        for index, ref in enumerate(entry.get("action_refs", [])):
            _validate_ref(repo_root, ref, f"{REVIEW_PATH}:{name}.action_refs[{index}]", issues)
        evidence = entry.get("evidence")
        if isinstance(evidence, dict):
            for index, ref in enumerate(evidence.get("episode_refs", [])):
                _validate_ref(
                    repo_root,
                    ref,
                    f"{REVIEW_PATH}:{name}.evidence.episode_refs[{index}]",
                    issues,
                    episode=True,
                )
        replacement = entry.get("replacement_route")
        if replacement is not None:
            _validate_ref(repo_root, replacement, f"{REVIEW_PATH}:{name}.replacement_route", issues)


def validate_document(repo_root: Path, payload: dict[str, Any]) -> ValidationSummary:
    root = repo_root.resolve()
    issues: list[ValidationIssue] = []
    _schema_issues(root, payload, issues)
    sources = _source_index(root, issues)
    entries = _index_entries(payload, issues)
    _validate_source_parity(sources, entries, issues)
    _validate_decisions(payload, entries, sources, issues)
    _validate_refs(root, payload, entries, issues)
    return ValidationSummary(len(sources), len(entries), tuple(issues))


def validate_summary(
    repo_root: Path,
    review_path: str = REVIEW_PATH,
) -> ValidationSummary:
    root = repo_root.resolve()
    issues: list[ValidationIssue] = []
    payload = _load_object(root / review_path, issues)
    if payload is None:
        sources = _source_index(root, issues)
        return ValidationSummary(len(sources), 0, tuple(issues))
    summary = validate_document(root, payload)
    return ValidationSummary(
        summary.expected_skill_count,
        summary.reviewed_skill_count,
        tuple(issues) + summary.issues,
    )


def main_validate(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--review-path", default=REVIEW_PATH)
    args = parser.parse_args(argv)
    summary = validate_summary(args.repo_root, args.review_path)
    print(CLAIM_LIMIT)
    print(
        "skill effectiveness family review: "
        f"{summary.reviewed_skill_count}/{summary.expected_skill_count} skills, "
        f"{len(summary.issues)} issue(s)"
    )
    for issue in summary.issues:
        print(f"- {issue.location}: {issue.message}")
    return 1 if summary.issues else 0
