from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

import skill_artifact_contract
import skill_catalog_contract


EVALUATION_FIXTURES_PATH = Path("tests") / "fixtures" / "skill_evaluation_cases.yaml"
EVALUATION_SNAPSHOTS_DIR = Path("tests") / "fixtures" / "skill_evaluation_snapshots"
EVALUATION_SNAPSHOT_HEADINGS = (
    "Prompt",
    "Expected selection",
    "Why",
    "Expected object",
    "Boundary notes",
    "Verification hooks",
)
SNAPSHOT_EXPECTED_VALUES = {"use", "do_not_use"}
SNAPSHOT_TOP_LEVEL_KEYS = (
    "skill",
    "case_id",
    "prompt",
    "expected",
    "snapshot_path",
    "required_output_phrases",
    "forbidden_output_phrases",
)
OUTPUT_SECTION_NAMES = (
    "Expected selection",
    "Why",
    "Expected object",
    "Boundary notes",
    "Verification hooks",
)

BLOCKER_MISSING_USE_SNAPSHOT = "missing_use_snapshot"
BLOCKER_MISSING_DO_NOT_USE_SNAPSHOT = "missing_do_not_use_snapshot"
BLOCKER_MISSING_SNAPSHOT_FILE = "missing_snapshot_file"
BLOCKER_SNAPSHOT_HEADING_CONTRACT_VIOLATION = "snapshot_heading_contract_violation"
BLOCKER_SNAPSHOT_MISSING_REQUIRED_PHRASE = "snapshot_missing_required_phrase"
BLOCKER_SNAPSHOT_CONTAINS_FORBIDDEN_PHRASE = "snapshot_contains_forbidden_phrase"
CANONICAL_EVAL_BLOCKER_ORDER = (
    BLOCKER_MISSING_USE_SNAPSHOT,
    BLOCKER_MISSING_DO_NOT_USE_SNAPSHOT,
    BLOCKER_MISSING_SNAPSHOT_FILE,
    BLOCKER_SNAPSHOT_HEADING_CONTRACT_VIOLATION,
    BLOCKER_SNAPSHOT_MISSING_REQUIRED_PHRASE,
    BLOCKER_SNAPSHOT_CONTAINS_FORBIDDEN_PHRASE,
)


@dataclass(frozen=True)
class EvaluationContractIssue:
    location: str
    message: str


@dataclass(frozen=True)
class SnapshotCoverage:
    use_snapshot_count: int
    do_not_use_snapshot_count: int
    blockers: tuple[str, ...]


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


def load_evaluation_fixtures(repo_root: Path) -> dict[str, Any] | None:
    fixtures_path = repo_root / EVALUATION_FIXTURES_PATH
    if not fixtures_path.is_file():
        return None
    data = yaml.safe_load(fixtures_path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(
            f"{relative_location(fixtures_path, repo_root)} must parse to a mapping"
        )
    return data


def ordered_blockers(blockers: Sequence[str]) -> tuple[str, ...]:
    blocker_set = {blocker for blocker in blockers if blocker in CANONICAL_EVAL_BLOCKER_ORDER}
    return tuple(
        blocker
        for blocker in CANONICAL_EVAL_BLOCKER_ORDER
        if blocker in blocker_set
    )


def default_snapshot_coverage() -> SnapshotCoverage:
    return SnapshotCoverage(
        use_snapshot_count=0,
        do_not_use_snapshot_count=0,
        blockers=ordered_blockers(
            (
                BLOCKER_MISSING_USE_SNAPSHOT,
                BLOCKER_MISSING_DO_NOT_USE_SNAPSHOT,
            )
        ),
    )


def snapshot_coverage_for_skill(
    coverage_by_skill: Mapping[str, SnapshotCoverage],
    skill_name: str,
) -> SnapshotCoverage:
    return coverage_by_skill.get(skill_name, default_snapshot_coverage())


def snapshot_cases(fixtures: Mapping[str, Any] | None) -> list[Mapping[str, Any]]:
    if not isinstance(fixtures, Mapping):
        return []
    raw_cases = fixtures.get("snapshot_cases", [])
    if not isinstance(raw_cases, list):
        return []
    return [case for case in raw_cases if isinstance(case, Mapping)]


def fixture_location_with_case(index: int, field_name: str | None = None) -> str:
    base = f"{EVALUATION_FIXTURES_PATH.as_posix()}:snapshot_cases[{index}]"
    if field_name is None:
        return base
    return f"{base}.{field_name}"


def validate_snapshot_case_contract(
    fixtures: Mapping[str, Any] | None,
) -> list[EvaluationContractIssue]:
    issues: list[EvaluationContractIssue] = []
    if not isinstance(fixtures, Mapping):
        return issues

    raw_cases = fixtures.get("snapshot_cases")
    if raw_cases is None:
        issues.append(
            EvaluationContractIssue(
                EVALUATION_FIXTURES_PATH.as_posix(),
                "evaluation fixtures must define top-level 'snapshot_cases'",
            )
        )
        return issues

    if not isinstance(raw_cases, list):
        issues.append(
            EvaluationContractIssue(
                EVALUATION_FIXTURES_PATH.as_posix(),
                "evaluation fixtures field 'snapshot_cases' must be a list",
            )
        )
        return issues

    for index, raw_case in enumerate(raw_cases):
        if not isinstance(raw_case, Mapping):
            issues.append(
                EvaluationContractIssue(
                    fixture_location_with_case(index),
                    "snapshot case must be a mapping",
                )
            )
            continue

        for key in SNAPSHOT_TOP_LEVEL_KEYS:
            if key not in raw_case:
                issues.append(
                    EvaluationContractIssue(
                        fixture_location_with_case(index),
                        f"snapshot case missing required field '{key}'",
                    )
                )

        skill_name = raw_case.get("skill")
        if not isinstance(skill_name, str) or not skill_name.strip():
            issues.append(
                EvaluationContractIssue(
                    fixture_location_with_case(index, "skill"),
                    "snapshot case field 'skill' must be a non-empty string",
                )
            )

        case_id = raw_case.get("case_id")
        if not isinstance(case_id, str) or not case_id.strip():
            issues.append(
                EvaluationContractIssue(
                    fixture_location_with_case(index, "case_id"),
                    "snapshot case field 'case_id' must be a non-empty string",
                )
            )

        prompt = raw_case.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            issues.append(
                EvaluationContractIssue(
                    fixture_location_with_case(index, "prompt"),
                    "snapshot case field 'prompt' must be a non-empty string",
                )
            )

        expected = raw_case.get("expected")
        if expected not in SNAPSHOT_EXPECTED_VALUES:
            issues.append(
                EvaluationContractIssue(
                    fixture_location_with_case(index, "expected"),
                    "snapshot case field 'expected' must be 'use' or 'do_not_use'",
                )
            )

        snapshot_path = raw_case.get("snapshot_path")
        if not isinstance(snapshot_path, str) or not snapshot_path.strip():
            issues.append(
                EvaluationContractIssue(
                    fixture_location_with_case(index, "snapshot_path"),
                    "snapshot case field 'snapshot_path' must be a non-empty string",
                )
            )
        else:
            snapshot_path_value = Path(snapshot_path)
            expected_dir = EVALUATION_SNAPSHOTS_DIR / str(skill_name or "")
            if (
                not skill_catalog_contract.is_repo_relative_path(snapshot_path)
                or snapshot_path_value.suffix.lower() != ".md"
                or expected_dir not in snapshot_path_value.parents
            ):
                issues.append(
                    EvaluationContractIssue(
                        fixture_location_with_case(index, "snapshot_path"),
                        "snapshot paths must stay under tests/fixtures/skill_evaluation_snapshots/<skill>/*.md",
                    )
                )

        for field_name in ("required_output_phrases", "forbidden_output_phrases"):
            field_value = raw_case.get(field_name)
            if not isinstance(field_value, list) or not all(
                isinstance(item, str) and item.strip() for item in field_value
            ):
                issues.append(
                    EvaluationContractIssue(
                        fixture_location_with_case(index, field_name),
                        f"snapshot case field '{field_name}' must be a list of non-empty strings",
                    )
                )

    return issues


def snapshot_output_text(path: Path) -> str:
    section_pairs = skill_artifact_contract.extract_artifact_sections(
        path.read_text(encoding="utf-8")
    )
    sections = {
        heading: content_markdown
        for heading, content_markdown in section_pairs
    }
    return normalize_text(
        "\n".join(sections.get(heading, "") for heading in OUTPUT_SECTION_NAMES)
    )


def collect_snapshot_file_issues(
    repo_root: Path,
    fixtures: Mapping[str, Any] | None,
) -> list[EvaluationContractIssue]:
    issues: list[EvaluationContractIssue] = []
    for case in snapshot_cases(fixtures):
        snapshot_path_value = case.get("snapshot_path")
        if not isinstance(snapshot_path_value, str) or not snapshot_path_value.strip():
            continue

        snapshot_path = repo_root / snapshot_path_value
        location = relative_location(snapshot_path, repo_root)
        if not snapshot_path.is_file():
            issues.append(
                EvaluationContractIssue(location, "evaluation snapshot file is missing")
            )
            continue

        section_pairs = skill_artifact_contract.extract_artifact_sections(
            snapshot_path.read_text(encoding="utf-8")
        )
        for contract_issue in skill_artifact_contract.collect_heading_contract_issues(
            section_pairs,
            location=location,
            artifact_label="evaluation snapshot",
            expected_headings=EVALUATION_SNAPSHOT_HEADINGS,
        ):
            issues.append(
                EvaluationContractIssue(contract_issue.location, contract_issue.message)
            )

        output_text = snapshot_output_text(snapshot_path)
        required_phrases = case.get("required_output_phrases", [])
        if isinstance(required_phrases, list):
            for phrase in required_phrases:
                if isinstance(phrase, str) and normalize_text(phrase) not in output_text:
                    issues.append(
                        EvaluationContractIssue(
                            location,
                            f"evaluation snapshot is missing required output phrase '{phrase}'",
                        )
                    )

        forbidden_phrases = case.get("forbidden_output_phrases", [])
        if isinstance(forbidden_phrases, list):
            for phrase in forbidden_phrases:
                if isinstance(phrase, str) and normalize_text(phrase) in output_text:
                    issues.append(
                        EvaluationContractIssue(
                            location,
                            f"evaluation snapshot contains forbidden output phrase '{phrase}'",
                        )
                    )

    return issues


def snapshot_blockers_for_case(
    repo_root: Path,
    case: Mapping[str, Any],
) -> set[str]:
    blockers: set[str] = set()
    snapshot_path_value = case.get("snapshot_path")
    if not isinstance(snapshot_path_value, str) or not snapshot_path_value.strip():
        blockers.add(BLOCKER_MISSING_SNAPSHOT_FILE)
        return blockers

    snapshot_path = repo_root / snapshot_path_value
    if not snapshot_path.is_file():
        blockers.add(BLOCKER_MISSING_SNAPSHOT_FILE)
        return blockers

    section_pairs = skill_artifact_contract.extract_artifact_sections(
        snapshot_path.read_text(encoding="utf-8")
    )
    heading_issues = skill_artifact_contract.collect_heading_contract_issues(
        section_pairs,
        location=relative_location(snapshot_path, repo_root),
        artifact_label="evaluation snapshot",
        expected_headings=EVALUATION_SNAPSHOT_HEADINGS,
    )
    if heading_issues:
        blockers.add(BLOCKER_SNAPSHOT_HEADING_CONTRACT_VIOLATION)

    output_text = snapshot_output_text(snapshot_path)
    required_phrases = case.get("required_output_phrases", [])
    if isinstance(required_phrases, list) and any(
        isinstance(phrase, str) and normalize_text(phrase) not in output_text
        for phrase in required_phrases
    ):
        blockers.add(BLOCKER_SNAPSHOT_MISSING_REQUIRED_PHRASE)

    forbidden_phrases = case.get("forbidden_output_phrases", [])
    if isinstance(forbidden_phrases, list) and any(
        isinstance(phrase, str) and normalize_text(phrase) in output_text
        for phrase in forbidden_phrases
    ):
        blockers.add(BLOCKER_SNAPSHOT_CONTAINS_FORBIDDEN_PHRASE)

    return blockers


def collect_snapshot_coverage(
    repo_root: Path,
    fixtures: Mapping[str, Any] | None,
) -> dict[str, SnapshotCoverage]:
    raw_coverage: dict[str, dict[str, Any]] = {}
    for case in snapshot_cases(fixtures):
        skill_name = case.get("skill")
        expected = case.get("expected")
        if not isinstance(skill_name, str) or expected not in SNAPSHOT_EXPECTED_VALUES:
            continue

        coverage = raw_coverage.setdefault(
            skill_name,
            {
                "use_snapshot_count": 0,
                "do_not_use_snapshot_count": 0,
                "blockers": set(),
            },
        )
        if expected == "use":
            coverage["use_snapshot_count"] = int(coverage["use_snapshot_count"]) + 1
        else:
            coverage["do_not_use_snapshot_count"] = (
                int(coverage["do_not_use_snapshot_count"]) + 1
            )
        coverage["blockers"].update(snapshot_blockers_for_case(repo_root, case))

    result: dict[str, SnapshotCoverage] = {}
    for skill_name, raw in raw_coverage.items():
        blockers = set(raw["blockers"])
        if int(raw["use_snapshot_count"]) < 1:
            blockers.add(BLOCKER_MISSING_USE_SNAPSHOT)
        if int(raw["do_not_use_snapshot_count"]) < 1:
            blockers.add(BLOCKER_MISSING_DO_NOT_USE_SNAPSHOT)
        result[skill_name] = SnapshotCoverage(
            use_snapshot_count=int(raw["use_snapshot_count"]),
            do_not_use_snapshot_count=int(raw["do_not_use_snapshot_count"]),
            blockers=ordered_blockers(sorted(blockers)),
        )
    return result


def derive_canonical_eval_blockers(
    coverage_by_skill: Mapping[str, SnapshotCoverage],
    skill_name: str,
) -> list[str]:
    return list(snapshot_coverage_for_skill(coverage_by_skill, skill_name).blockers)
