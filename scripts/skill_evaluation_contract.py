from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

import skill_artifact_contract
import skill_catalog_contract


EVALUATION_FIXTURES_PATH = Path("tests") / "fixtures" / "skill_evaluation_cases.yaml"
EVALUATION_SNAPSHOTS_DIR = Path("tests") / "fixtures" / "skill_evaluation_snapshots"
EVALUATION_FIXTURES_SCHEMA = "skill-evaluation-cases.schema.json"
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
ADJACENCY_TOP_LEVEL_KEYS = (
    "skill",
    "adjacent_skill",
    "case_id",
    "prompt",
    "expected",
    "snapshot_path",
    "required_output_phrases",
    "forbidden_output_phrases",
)
TOP_LEVEL_FIXTURE_KEYS = (
    "autonomy_checks",
    "trigger_cases",
    "snapshot_cases",
    "adjacency_cases",
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


def adjacency_cases(fixtures: Mapping[str, Any] | None) -> list[Mapping[str, Any]]:
    if not isinstance(fixtures, Mapping):
        return []
    raw_cases = fixtures.get("adjacency_cases", [])
    if not isinstance(raw_cases, list):
        return []
    return [case for case in raw_cases if isinstance(case, Mapping)]


def trigger_cases(fixtures: Mapping[str, Any] | None) -> list[Mapping[str, Any]]:
    if not isinstance(fixtures, Mapping):
        return []
    raw_cases = fixtures.get("trigger_cases", [])
    if not isinstance(raw_cases, list):
        return []
    return [case for case in raw_cases if isinstance(case, Mapping)]


def discover_skill_names(repo_root: Path) -> list[str]:
    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        return []
    return sorted(path.name for path in skills_dir.iterdir() if path.is_dir())


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


def validate_adjacency_case_contract(
    fixtures: Mapping[str, Any] | None,
) -> list[EvaluationContractIssue]:
    issues: list[EvaluationContractIssue] = []
    if not isinstance(fixtures, Mapping):
        return issues

    raw_cases = fixtures.get("adjacency_cases")
    if raw_cases is None:
        issues.append(
            EvaluationContractIssue(
                EVALUATION_FIXTURES_PATH.as_posix(),
                "evaluation fixtures must define top-level 'adjacency_cases'",
            )
        )
        return issues

    if not isinstance(raw_cases, list):
        issues.append(
            EvaluationContractIssue(
                EVALUATION_FIXTURES_PATH.as_posix(),
                "evaluation fixtures field 'adjacency_cases' must be a list",
            )
        )
        return issues

    for index, raw_case in enumerate(raw_cases):
        location = f"{EVALUATION_FIXTURES_PATH.as_posix()}:adjacency_cases[{index}]"
        if not isinstance(raw_case, Mapping):
            issues.append(EvaluationContractIssue(location, "adjacency case must be a mapping"))
            continue

        for key in ADJACENCY_TOP_LEVEL_KEYS:
            if key not in raw_case:
                issues.append(
                    EvaluationContractIssue(
                        location,
                        f"adjacency case missing required field '{key}'",
                    )
                )

        for field_name in ("skill", "adjacent_skill", "case_id", "prompt", "snapshot_path"):
            field_value = raw_case.get(field_name)
            if not isinstance(field_value, str) or not field_value.strip():
                issues.append(
                    EvaluationContractIssue(
                        f"{location}.{field_name}",
                        f"adjacency case field '{field_name}' must be a non-empty string",
                    )
                )

        if raw_case.get("skill") == raw_case.get("adjacent_skill"):
            issues.append(
                EvaluationContractIssue(
                    f"{location}.adjacent_skill",
                    "adjacency case must compare against a different adjacent_skill",
                )
            )

        expected = raw_case.get("expected")
        if expected not in SNAPSHOT_EXPECTED_VALUES:
            issues.append(
                EvaluationContractIssue(
                    f"{location}.expected",
                    "adjacency case field 'expected' must be 'use' or 'do_not_use'",
                )
            )

        snapshot_path = raw_case.get("snapshot_path")
        if isinstance(snapshot_path, str) and snapshot_path.strip():
            snapshot_path_value = Path(snapshot_path)
            skill_name = str(raw_case.get("skill") or "")
            expected_dir = EVALUATION_SNAPSHOTS_DIR / skill_name
            if (
                not skill_catalog_contract.is_repo_relative_path(snapshot_path)
                or snapshot_path_value.suffix.lower() != ".md"
                or expected_dir not in snapshot_path_value.parents
            ):
                issues.append(
                    EvaluationContractIssue(
                        f"{location}.snapshot_path",
                        "adjacency snapshot paths must stay under tests/fixtures/skill_evaluation_snapshots/<skill>/*.md",
                    )
                )

        for field_name in ("required_output_phrases", "forbidden_output_phrases"):
            field_value = raw_case.get(field_name)
            if not isinstance(field_value, list) or not all(
                isinstance(item, str) and item.strip() for item in field_value
            ):
                issues.append(
                    EvaluationContractIssue(
                        f"{location}.{field_name}",
                        f"adjacency case field '{field_name}' must be a list of non-empty strings",
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
        if not skill_catalog_contract.is_repo_relative_path(snapshot_path_value):
            issues.append(
                EvaluationContractIssue(
                    EVALUATION_FIXTURES_PATH.as_posix(),
                    f"snapshot_path must stay repo-relative: {snapshot_path_value!r}",
                )
            )
            continue

        snapshot_path = (repo_root / snapshot_path_value).resolve()
        try:
            snapshot_path.relative_to(repo_root)
        except ValueError:
            issues.append(
                EvaluationContractIssue(
                    EVALUATION_FIXTURES_PATH.as_posix(),
                    f"snapshot_path escapes the repository root: {snapshot_path_value!r}",
                )
            )
            continue
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


def snapshot_reference_cases(fixtures: Mapping[str, Any] | None) -> list[Mapping[str, Any]]:
    return list(snapshot_cases(fixtures)) + list(adjacency_cases(fixtures))


def validate_fixture_integrity(
    repo_root: Path,
    fixtures: Mapping[str, Any] | None,
) -> list[EvaluationContractIssue]:
    issues: list[EvaluationContractIssue] = []
    if not isinstance(fixtures, Mapping):
        return issues

    available_skills = set(discover_skill_names(repo_root))
    seen_case_ids: dict[str, str] = {}
    seen_snapshot_paths: dict[str, str] = {}
    trigger_by_case_id: dict[str, Mapping[str, Any]] = {}

    for top_level_key in TOP_LEVEL_FIXTURE_KEYS:
        if top_level_key not in fixtures:
            issues.append(
                EvaluationContractIssue(
                    EVALUATION_FIXTURES_PATH.as_posix(),
                    f"evaluation fixtures must define top-level '{top_level_key}'",
                )
            )

    for case in trigger_cases(fixtures):
        case_id = case.get("case_id")
        skill_name = case.get("skill")
        location = EVALUATION_FIXTURES_PATH.as_posix()
        if isinstance(skill_name, str) and skill_name not in available_skills:
            issues.append(
                EvaluationContractIssue(
                    location,
                    f"trigger case references unknown skill '{skill_name}'",
                )
            )
        if isinstance(case_id, str):
            trigger_by_case_id[case_id] = case

    for case in snapshot_reference_cases(fixtures):
        case_id = case.get("case_id")
        snapshot_path = case.get("snapshot_path")
        skill_name = case.get("skill")
        expected = case.get("expected")

        if isinstance(skill_name, str) and skill_name not in available_skills:
            issues.append(
                EvaluationContractIssue(
                    EVALUATION_FIXTURES_PATH.as_posix(),
                    f"snapshot-backed case references unknown skill '{skill_name}'",
                )
            )

        if isinstance(case_id, str):
            if case_id in seen_case_ids:
                issues.append(
                    EvaluationContractIssue(
                        EVALUATION_FIXTURES_PATH.as_posix(),
                        f"duplicate snapshot-backed case_id '{case_id}'",
                    )
                )
            seen_case_ids[case_id] = str(case.get("skill") or "")
            if case in snapshot_cases(fixtures):
                trigger_case = trigger_by_case_id.get(case_id)
                if trigger_case is None:
                    issues.append(
                        EvaluationContractIssue(
                            EVALUATION_FIXTURES_PATH.as_posix(),
                            f"snapshot case '{case_id}' must have a matching trigger case",
                        )
                    )
                else:
                    if trigger_case.get("expected") != expected:
                        issues.append(
                            EvaluationContractIssue(
                                EVALUATION_FIXTURES_PATH.as_posix(),
                                f"snapshot case '{case_id}' must match trigger-case expected value",
                            )
                        )
                    if trigger_case.get("prompt") != case.get("prompt"):
                        issues.append(
                            EvaluationContractIssue(
                                EVALUATION_FIXTURES_PATH.as_posix(),
                                f"snapshot case '{case_id}' must keep prompt aligned with its trigger case",
                            )
                        )

        if isinstance(snapshot_path, str):
            if snapshot_path in seen_snapshot_paths:
                issues.append(
                    EvaluationContractIssue(
                        EVALUATION_FIXTURES_PATH.as_posix(),
                        f"duplicate snapshot_path '{snapshot_path}'",
                    )
                )
            seen_snapshot_paths[snapshot_path] = str(case_id or "")
            if isinstance(case_id, str) and Path(snapshot_path).name != f"{case_id}.md":
                issues.append(
                    EvaluationContractIssue(
                        EVALUATION_FIXTURES_PATH.as_posix(),
                        f"snapshot_path '{snapshot_path}' must match case_id '{case_id}.md'",
                    )
                )

    referenced_paths = {
        str(case.get("snapshot_path"))
        for case in snapshot_reference_cases(fixtures)
        if isinstance(case.get("snapshot_path"), str)
    }
    snapshots_root = repo_root / EVALUATION_SNAPSHOTS_DIR
    if snapshots_root.is_dir():
        for snapshot_path in sorted(snapshots_root.rglob("*.md")):
            relative = relative_location(snapshot_path, repo_root)
            if relative not in referenced_paths:
                issues.append(
                    EvaluationContractIssue(
                        relative,
                        "evaluation snapshot file is orphaned and not referenced by snapshot_cases or adjacency_cases",
                    )
                )

    return issues


def derive_canonical_eval_blockers(
    coverage_by_skill: Mapping[str, SnapshotCoverage],
    skill_name: str,
) -> list[str]:
    return list(snapshot_coverage_for_skill(coverage_by_skill, skill_name).blockers)
