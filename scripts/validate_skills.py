#!/usr/bin/env python3
"""Local validator for aoa-skills bundles."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Sequence

import yaml
from jsonschema import Draft202012Validator

import build_catalog
import skill_artifact_contract
import skill_catalog_contract
import skill_evaluation_contract
import skill_governance_surface
import skill_section_contract


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR_NAME = "skills"
SKILL_INDEX_NAME = "SKILL_INDEX.md"
SCHEMAS_DIR_NAME = "schemas"
SKILL_NAME_PATTERN = r"(?:aoa|atm10|abyss)-[a-z0-9-]+"
STATUS_PROMOTION_REVIEWS_DIR = Path("docs") / "reviews" / "status-promotions"
CANONICAL_CANDIDATES_DIR = Path("docs") / "reviews" / "canonical-candidates"
EVALUATION_FIXTURES_PATH = Path("tests") / "fixtures" / "skill_evaluation_cases.yaml"

REQUIRED_HEADINGS = set(skill_section_contract.CANONICAL_HEADINGS)
EXPECTED_TECHNIQUE_REPO = skill_catalog_contract.EXPECTED_TECHNIQUE_REPO
EVALUATION_MATRIX_LOCATION = build_catalog.EVALUATION_MATRIX_JSON_PATH.as_posix()
EVALUATION_MATRIX_MARKDOWN_LOCATION = (
    build_catalog.EVALUATION_MATRIX_MARKDOWN_PATH.as_posix()
)


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


@lru_cache(maxsize=None)
def load_schema(schema_name: str) -> dict[str, Any]:
    schema_path = REPO_ROOT / SCHEMAS_DIR_NAME / schema_name
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=None)
def get_schema_validator(schema_name: str) -> Draft202012Validator:
    return Draft202012Validator(load_schema(schema_name))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate local aoa-skills bundles.")
    parser.add_argument(
        "--skill",
        help="Validate a single skill bundle by directory name.",
    )
    return parser.parse_args(argv)


def load_yaml_file(path: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path), "file is missing"))
        return None
    except yaml.YAMLError as exc:
        issues.append(
            ValidationIssue(relative_location(path), f"invalid YAML: {exc}")
        )
        return None
    return data


def relative_location(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def format_schema_path(path_parts: Iterable[Any]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        else:
            if parts:
                parts.append(f".{part}")
            else:
                parts.append(str(part))
    return "".join(parts)


def validate_against_schema(
    data: Any,
    schema_name: str,
    location: str,
    issues: list[ValidationIssue],
) -> bool:
    validator = get_schema_validator(schema_name)
    schema_errors = sorted(
        validator.iter_errors(data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    for error in schema_errors:
        error_path = format_schema_path(error.absolute_path)
        if error_path:
            message = f"schema violation at '{error_path}': {error.message}"
        else:
            message = f"schema violation: {error.message}"
        issues.append(ValidationIssue(location, message))
    return not schema_errors


def parse_skill_markdown(
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> tuple[dict[str, Any] | None, list[tuple[str, str]]]:
    try:
        text = skill_md_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(skill_md_path), "file is missing"))
        return None, []

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                "missing YAML frontmatter opening delimiter",
            )
        )
        return None, []

    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                "missing YAML frontmatter closing delimiter",
            )
        )
        return None, []

    frontmatter_text = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :])

    try:
        metadata = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as exc:
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                f"invalid frontmatter YAML: {exc}",
            )
        )
        return None, []

    if not isinstance(metadata, dict):
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                "frontmatter must parse to a mapping",
            )
        )
        return None, []

    section_pairs = skill_section_contract.extract_top_level_sections(body)
    return metadata, section_pairs


def find_support_artifacts(
    repo_root: Path,
    skill_name: str,
) -> list[dict[str, Any]]:
    return skill_artifact_contract.collect_support_artifacts(repo_root, skill_name)


def validate_skill_bundle(repo_root: Path, skill_name: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    skill_dir = repo_root / SKILLS_DIR_NAME / skill_name
    skill_md_path = skill_dir / "SKILL.md"
    techniques_path = skill_dir / "techniques.yaml"
    policy_path = skill_dir / "agents" / "openai.yaml"

    if not skill_dir.is_dir():
        issues.append(
            ValidationIssue(relative_location(skill_dir), "skill directory is missing")
        )
        return issues

    if not skill_md_path.is_file():
        issues.append(ValidationIssue(relative_location(skill_md_path), "file is missing"))

    if not techniques_path.is_file():
        issues.append(
            ValidationIssue(relative_location(techniques_path), "file is missing")
        )

    if not find_support_artifacts(repo_root, skill_name):
        issues.append(
            ValidationIssue(
                relative_location(skill_dir),
                "missing support artifact under examples/*.md, checks/review.md, or docs/reviews/*",
            )
        )
    else:
        for artifact_issue in skill_artifact_contract.collect_skill_artifact_issues(
            repo_root,
            skill_name,
        ):
            issues.append(
                ValidationIssue(artifact_issue.location, artifact_issue.message)
            )

    metadata: dict[str, Any] | None = None
    sections: dict[str, str] = {}
    techniques_data: dict[str, Any] | None = None
    if skill_md_path.is_file():
        metadata, section_pairs = parse_skill_markdown(skill_md_path, issues)
        sections = {heading: content for heading, content in section_pairs}
        if metadata is not None:
            validate_skill_frontmatter(skill_name, metadata, skill_md_path, issues)
            validate_section_contract(section_pairs, skill_md_path, issues)
            validate_capsule_source_sections(sections, skill_md_path, issues)

    if techniques_path.is_file():
        techniques_data = load_yaml_file(techniques_path, issues)
        if techniques_data is not None:
            validate_techniques_manifest(
                skill_name,
                techniques_data,
                techniques_path,
                issues,
            )

    if policy_path.is_file():
        policy_data = load_yaml_file(policy_path, issues)
        if policy_data is not None:
            validate_policy_file(policy_data, policy_path, issues)

    if metadata and metadata.get("invocation_mode") == "explicit-only":
        validate_explicit_only_policy(policy_path, issues)

    if metadata is not None and techniques_data is not None:
        validate_skill_manifest_parity(
            skill_name,
            metadata,
            techniques_data,
            skill_md_path,
            techniques_path,
            issues,
        )
        validate_status_floors(
            repo_root,
            skill_name,
            metadata,
            set(sections),
            techniques_data,
            skill_dir,
            skill_md_path,
            techniques_path,
            issues,
        )

    return issues


def validate_skill_frontmatter(
    skill_name: str,
    metadata: dict[str, Any],
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(skill_md_path)
    if not validate_against_schema(metadata, "skill-frontmatter.schema.json", location, issues):
        return

    if metadata.get("name") != skill_name:
        issues.append(
            ValidationIssue(location, "frontmatter 'name' must match the directory name")
        )


def validate_section_contract(
    section_pairs: list[tuple[str, str]],
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(skill_md_path)
    for contract_issue in skill_section_contract.collect_section_contract_issues(
        section_pairs,
        location=location,
    ):
        issues.append(ValidationIssue(contract_issue.location, contract_issue.message))


def validate_capsule_source_sections(
    sections: dict[str, str],
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(skill_md_path)
    for section_name in build_catalog.CAPSULE_REQUIRED_SECTIONS:
        if section_name not in sections:
            continue
        if not sections[section_name].strip():
            issues.append(
                ValidationIssue(
                    location,
                    f"capsule source section '{section_name}' must not be empty",
                )
            )


def validate_techniques_manifest(
    skill_name: str,
    manifest: Any,
    techniques_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(techniques_path)
    if not isinstance(manifest, dict):
        issues.append(ValidationIssue(location, "manifest must parse to a mapping"))
        return

    validate_against_schema(
        manifest,
        "techniques.schema.json",
        location,
        issues,
    )

    if manifest.get("skill_name") != skill_name:
        issues.append(
            ValidationIssue(location, "'skill_name' must match the directory name")
        )

    techniques = manifest.get("techniques")
    if not isinstance(techniques, list):
        return

    for contract_issue in skill_catalog_contract.collect_technique_ref_issues(
        manifest,
        techniques_path,
        techniques_path.parents[2],
    ):
        issues.append(
            ValidationIssue(contract_issue.location, contract_issue.message)
        )

    notes = manifest.get("notes")
    pending_ids: list[str] = []
    for technique in techniques:
        if not isinstance(technique, dict):
            continue
        technique_id = technique.get("id")
        if isinstance(technique_id, str) and technique_id.startswith("AOA-T-PENDING-"):
            pending_ids.append(technique_id)

    if pending_ids and not has_pending_note(notes, pending_ids):
        issues.append(
            ValidationIssue(
                location,
                "pending techniques require a note explaining that pending IDs and "
                "path/source_ref TBD must be replaced after publication",
            )
        )


def has_pending_note(notes: Any, pending_ids: Iterable[str]) -> bool:
    if not isinstance(notes, list):
        return False

    pending_tokens = [pending_id.lower() for pending_id in pending_ids]
    for note in notes:
        if not isinstance(note, str):
            continue
        lowered = note.lower()
        if "replace" not in lowered:
            continue
        if "path" not in lowered:
            continue
        if "source_ref" not in lowered:
            continue
        if "publish" not in lowered:
            continue
        if "pending" in lowered or any(token in lowered for token in pending_tokens):
            return True
    return False


def validate_policy_file(
    policy_data: Any,
    policy_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(policy_path)
    validate_against_schema(policy_data, "openai-policy.schema.json", location, issues)


def validate_explicit_only_policy(
    policy_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(policy_path)
    if not policy_path.is_file():
        issues.append(
            ValidationIssue(
                location,
                "explicit-only skills require agents/openai.yaml",
            )
        )
        return

    policy_issues: list[ValidationIssue] = []
    policy_data = load_yaml_file(policy_path, policy_issues)
    if policy_issues:
        issues.extend(policy_issues)
        return

    if not isinstance(policy_data, dict):
        issues.append(ValidationIssue(location, "policy file must parse to a mapping"))
        return

    policy = policy_data.get("policy")
    if not isinstance(policy, dict):
        issues.append(ValidationIssue(location, "missing mapping 'policy'"))
        return

    if policy.get("allow_implicit_invocation") is not False:
        issues.append(
            ValidationIssue(
                location,
                "explicit-only skills must set 'policy.allow_implicit_invocation' to false",
            )
        )


def load_policy_signal(repo_root: Path, skill_name: str) -> tuple[bool, Any]:
    policy_path = repo_root / SKILLS_DIR_NAME / skill_name / "agents" / "openai.yaml"
    if not policy_path.is_file():
        return False, None

    policy_issues: list[ValidationIssue] = []
    policy_data = load_yaml_file(policy_path, policy_issues)
    if policy_issues or not isinstance(policy_data, dict):
        return True, None

    policy = policy_data.get("policy")
    if not isinstance(policy, dict):
        return True, None
    return True, policy.get("allow_implicit_invocation")


def status_requires_floor(status: str, floor: str) -> bool:
    floors = {
        "linked": {"linked", "reviewed", "evaluated", "canonical"},
        "reviewed": {"reviewed", "evaluated", "canonical"},
        "evaluated": {"evaluated", "canonical"},
        "canonical": {"canonical"},
    }
    return status in floors[floor]


def validate_status_floors(
    repo_root: Path,
    skill_name: str,
    metadata: dict[str, Any],
    headings: set[str],
    techniques_data: dict[str, Any],
    skill_dir: Path,
    skill_md_path: Path,
    techniques_path: Path,
    issues: list[ValidationIssue],
) -> None:
    status = metadata.get("status")
    if not isinstance(status, str):
        return

    if status_requires_floor(status, "linked"):
        validate_linked_floor(status, techniques_data, techniques_path, issues)

    if status_requires_floor(status, "reviewed"):
        validate_reviewed_floor(repo_root, status, skill_name, skill_dir, skill_md_path, issues)


def validate_linked_floor(
    status: str,
    techniques_data: dict[str, Any],
    techniques_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(techniques_path)
    for technique in techniques_data.get("techniques", []):
        technique_id = technique.get("id", "")
        if technique_id.startswith("AOA-T-PENDING-"):
            continue
        if technique.get("source_ref") == "TBD":
            issues.append(
                ValidationIssue(
                    location,
                    f"status '{status}' requires published techniques to use concrete source_ref values",
                )
            )
            return


def has_review_evidence(repo_root: Path, skill_name: str, skill_dir: Path) -> bool:
    candidate_paths = [
        skill_dir / "checks" / "review.md",
        repo_root / STATUS_PROMOTION_REVIEWS_DIR / f"{skill_name}.md",
        repo_root / CANONICAL_CANDIDATES_DIR / f"{skill_name}.md",
    ]
    return any(path.is_file() for path in candidate_paths)


def validate_reviewed_floor(
    repo_root: Path,
    status: str,
    skill_name: str,
    skill_dir: Path,
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    if has_review_evidence(repo_root, skill_name, skill_dir):
        return

    issues.append(
        ValidationIssue(
            relative_location(skill_md_path),
            f"status '{status}' requires review evidence via checks/review.md or a public review record",
        )
    )


def validate_canonical_floor(
    metadata: dict[str, Any],
    headings: set[str],
    techniques_data: dict[str, Any],
    skill_md_path: Path,
    techniques_path: Path,
    issues: list[ValidationIssue],
) -> None:
    skill_location = relative_location(skill_md_path)
    techniques_location = relative_location(techniques_path)

    dependencies = metadata.get("technique_dependencies", [])
    if any(
        isinstance(dependency, str) and dependency.startswith("AOA-T-PENDING-")
        for dependency in dependencies
    ):
        issues.append(
            ValidationIssue(
                skill_location,
                "status 'canonical' cannot use pending technique_dependencies",
            )
        )

    if "Technique traceability" not in headings or "Future traceability" in headings:
        issues.append(
            ValidationIssue(
                skill_location,
                "status 'canonical' requires 'Technique traceability' and forbids legacy 'Future traceability'",
            )
        )

    for technique in techniques_data.get("techniques", []):
        if technique.get("id", "").startswith("AOA-T-PENDING-"):
            issues.append(
                ValidationIssue(
                    techniques_location,
                    "status 'canonical' cannot use pending techniques in techniques.yaml",
                )
            )
            break

    for technique in techniques_data.get("techniques", []):
        if technique.get("path") == "TBD" or technique.get("source_ref") == "TBD":
            issues.append(
                ValidationIssue(
                    techniques_location,
                    "status 'canonical' requires concrete path and source_ref for every technique",
                )
            )
            break


def load_evaluation_fixtures(
    repo_root: Path,
    issues: list[ValidationIssue],
) -> dict[str, Any] | None:
    fixtures_path = repo_root / EVALUATION_FIXTURES_PATH
    if not fixtures_path.is_file():
        issues.append(ValidationIssue(relative_location(fixtures_path), "file is missing"))
        return None
    try:
        data = skill_evaluation_contract.load_evaluation_fixtures(repo_root)
    except yaml.YAMLError as exc:
        issues.append(
            ValidationIssue(
                relative_location(fixtures_path),
                f"invalid YAML: {exc}",
            )
        )
        return None
    except ValueError as exc:
        issues.append(
            ValidationIssue(
                relative_location(fixtures_path),
                str(exc),
            )
        )
        return None
    if data is None:
        return None
    return data


def validate_snapshot_fixture_contract(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    fixtures_path = repo_root / EVALUATION_FIXTURES_PATH
    if not fixtures_path.is_file():
        return issues

    fixtures = load_evaluation_fixtures(repo_root, issues)
    if fixtures is None:
        return issues

    for contract_issue in skill_evaluation_contract.validate_snapshot_case_contract(fixtures):
        issues.append(ValidationIssue(contract_issue.location, contract_issue.message))
    for contract_issue in skill_evaluation_contract.collect_snapshot_file_issues(
        repo_root,
        fixtures,
    ):
        issues.append(ValidationIssue(contract_issue.location, contract_issue.message))
    return issues


def validate_evaluation_floors(
    repo_root: Path,
    target_skills: Sequence[str],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    skills_requiring_evaluation: dict[str, str] = {}

    for skill_name in target_skills:
        metadata, _sections = parse_skill_markdown(
            repo_root / SKILLS_DIR_NAME / skill_name / "SKILL.md",
            [],
        )
        if metadata is None:
            continue
        status = metadata.get("status")
        if isinstance(status, str) and status_requires_floor(status, "evaluated"):
            skills_requiring_evaluation[skill_name] = status

    if not skills_requiring_evaluation:
        return issues

    fixtures = load_evaluation_fixtures(repo_root, issues)
    if fixtures is None:
        return issues

    coverage_by_skill = skill_governance_surface.collect_evaluation_coverage(fixtures)
    fixtures_location = EVALUATION_FIXTURES_PATH.as_posix()
    for skill_name, status in skills_requiring_evaluation.items():
        coverage = skill_governance_surface.coverage_for_skill(
            coverage_by_skill,
            skill_name,
        )
        if not coverage.has_autonomy_check:
            issues.append(
                ValidationIssue(
                    fixtures_location,
                    f"skill '{skill_name}' with status '{status}' requires an autonomy_check entry",
                )
            )
        if coverage.use_case_count < 1:
            issues.append(
                ValidationIssue(
                    fixtures_location,
                    f"skill '{skill_name}' with status '{status}' requires at least one 'use' trigger case",
                )
            )
        if coverage.do_not_use_case_count < 1:
            issues.append(
                ValidationIssue(
                    fixtures_location,
                    f"skill '{skill_name}' with status '{status}' requires at least one 'do_not_use' trigger case",
                )
            )

    return issues


def validate_canonical_status_floors(
    repo_root: Path,
    target_skills: Sequence[str],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    canonical_skills: list[
        tuple[str, dict[str, Any], set[str], dict[str, Any], Path, Path]
    ] = []

    for skill_name in target_skills:
        skill_md_path = repo_root / SKILLS_DIR_NAME / skill_name / "SKILL.md"
        techniques_path = repo_root / SKILLS_DIR_NAME / skill_name / "techniques.yaml"
        metadata, section_pairs = parse_skill_markdown(skill_md_path, [])
        if metadata is None or metadata.get("status") != "canonical":
            continue

        manifest_issues: list[ValidationIssue] = []
        techniques_data = load_yaml_file(techniques_path, manifest_issues)
        if manifest_issues or not isinstance(techniques_data, dict):
            continue

        canonical_skills.append(
            (
                skill_name,
                metadata,
                {heading for heading, _content in section_pairs},
                techniques_data,
                skill_md_path,
                techniques_path,
            )
        )

    if not canonical_skills:
        return issues

    fixtures = load_evaluation_fixtures(repo_root, [])
    coverage_by_skill = skill_governance_surface.collect_evaluation_coverage(fixtures)
    snapshot_coverage_by_skill = skill_evaluation_contract.collect_snapshot_coverage(
        repo_root,
        fixtures,
    )
    fixtures_location = EVALUATION_FIXTURES_PATH.as_posix()
    snapshots_location = skill_evaluation_contract.EVALUATION_SNAPSHOTS_DIR.as_posix()

    for (
        skill_name,
        metadata,
        headings,
        techniques_data,
        skill_md_path,
        techniques_path,
    ) in canonical_skills:
        policy_exists, policy_allow_implicit_invocation = load_policy_signal(
            repo_root,
            skill_name,
        )
        blockers = skill_governance_surface.derive_canonical_candidate_blockers(
            status="canonical",
            headings=headings,
            technique_dependencies=list(metadata.get("technique_dependencies", [])),
            techniques=skill_catalog_contract.normalize_technique_refs(techniques_data),
            evaluation_coverage=skill_governance_surface.coverage_for_skill(
                coverage_by_skill,
                skill_name,
            ),
            invocation_mode=metadata.get("invocation_mode"),
            policy_exists=policy_exists,
            policy_allow_implicit_invocation=policy_allow_implicit_invocation,
        )
        skill_location = relative_location(skill_md_path)
        techniques_location = relative_location(techniques_path)

        if skill_governance_surface.BLOCKER_PENDING_TECHNIQUE_DEPENDENCIES in blockers:
            issues.append(
                ValidationIssue(
                    skill_location,
                    "status 'canonical' cannot use pending technique_dependencies",
                )
            )
        if skill_governance_surface.BLOCKER_MISSING_TRACEABILITY_HEADING in blockers:
            issues.append(
                ValidationIssue(
                    skill_location,
                    "status 'canonical' requires 'Technique traceability' and forbids legacy 'Future traceability'",
                )
            )
        if skill_governance_surface.BLOCKER_PENDING_TECHNIQUE_ENTRIES in blockers:
            issues.append(
                ValidationIssue(
                    techniques_location,
                    "status 'canonical' cannot use pending techniques in techniques.yaml",
                )
            )
        if skill_governance_surface.BLOCKER_TBD_TECHNIQUE_REFS in blockers:
            issues.append(
                ValidationIssue(
                    techniques_location,
                    "status 'canonical' requires concrete path and source_ref for every technique",
                )
            )
        eval_blockers = skill_evaluation_contract.derive_canonical_eval_blockers(
            snapshot_coverage_by_skill,
            skill_name,
        )
        if skill_evaluation_contract.BLOCKER_MISSING_USE_SNAPSHOT in eval_blockers:
            issues.append(
                ValidationIssue(
                    fixtures_location,
                    "status 'canonical' requires at least one 'use' snapshot case",
                )
            )
        if skill_evaluation_contract.BLOCKER_MISSING_DO_NOT_USE_SNAPSHOT in eval_blockers:
            issues.append(
                ValidationIssue(
                    fixtures_location,
                    "status 'canonical' requires at least one 'do_not_use' snapshot case",
                )
            )
        if skill_evaluation_contract.BLOCKER_MISSING_SNAPSHOT_FILE in eval_blockers:
            issues.append(
                ValidationIssue(
                    snapshots_location,
                    "status 'canonical' requires referenced snapshot files to exist",
                )
            )
        if skill_evaluation_contract.BLOCKER_SNAPSHOT_HEADING_CONTRACT_VIOLATION in eval_blockers:
            issues.append(
                ValidationIssue(
                    snapshots_location,
                    "status 'canonical' requires snapshot files to satisfy the canonical heading contract",
                )
            )
        if skill_evaluation_contract.BLOCKER_SNAPSHOT_MISSING_REQUIRED_PHRASE in eval_blockers:
            issues.append(
                ValidationIssue(
                    snapshots_location,
                    "status 'canonical' requires snapshot files to contain every required output phrase",
                )
            )
        if skill_evaluation_contract.BLOCKER_SNAPSHOT_CONTAINS_FORBIDDEN_PHRASE in eval_blockers:
            issues.append(
                ValidationIssue(
                    snapshots_location,
                    "status 'canonical' requires snapshot files to avoid forbidden output phrases",
                )
            )

    return issues


def validate_skill_index(
    repo_root: Path,
    selected_skills: set[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    index_path = repo_root / SKILL_INDEX_NAME
    try:
        text = index_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [ValidationIssue(SKILL_INDEX_NAME, "file is missing")]

    pattern = re.compile(rf"^\|\s*({SKILL_NAME_PATTERN})\s*\|", flags=re.MULTILINE)
    names = pattern.findall(text)
    counts = Counter(names)
    location = relative_location(index_path)

    if selected_skills is None:
        skill_dirs = {
            path.name
            for path in (repo_root / SKILLS_DIR_NAME).iterdir()
            if path.is_dir()
        }
        for name, count in sorted(counts.items()):
            if count > 1:
                issues.append(
                    ValidationIssue(
                        location,
                        f"skill '{name}' appears {count} times in the index",
                    )
                )

        for missing in sorted(skill_dirs - counts.keys()):
            issues.append(
                ValidationIssue(location, f"skill '{missing}' is missing from the index")
            )

        for extra in sorted(counts.keys() - skill_dirs):
            issues.append(
                ValidationIssue(
                    location,
                    f"index lists '{extra}' but no matching skill directory exists",
                )
            )
    else:
        for name in sorted(selected_skills):
            count = counts.get(name, 0)
            if count == 0:
                issues.append(
                    ValidationIssue(location, f"skill '{name}' is missing from the index")
                )
            elif count > 1:
                issues.append(
                    ValidationIssue(
                        location,
                        f"skill '{name}' appears {count} times in the index",
                    )
                )

    return issues


def discover_skill_names(repo_root: Path) -> list[str]:
    skills_dir = repo_root / SKILLS_DIR_NAME
    if not skills_dir.is_dir():
        raise FileNotFoundError(f"missing skills directory at {skills_dir}")
    return sorted(path.name for path in skills_dir.iterdir() if path.is_dir())


def technique_ids_from_manifest(manifest: dict[str, Any]) -> list[str]:
    techniques = manifest.get("techniques", [])
    if not isinstance(techniques, list):
        return []
    return [technique.get("id") for technique in techniques if isinstance(technique, dict)]


def validate_skill_manifest_parity(
    skill_name: str,
    metadata: dict[str, Any],
    manifest: dict[str, Any],
    skill_md_path: Path,
    _techniques_path: Path,
    issues: list[ValidationIssue],
) -> None:
    for contract_issue in skill_catalog_contract.collect_skill_parity_issues(
        skill_name,
        metadata,
        manifest,
        skill_md_path,
        skill_md_path.parents[2],
    ):
        if contract_issue.message == "frontmatter 'name' must match the directory name":
            continue
        issues.append(ValidationIssue(contract_issue.location, contract_issue.message))


def catalog_entries_by_name(
    catalog: dict[str, Any],
    *,
    array_key: str,
    key_name: str,
    location: str,
    issues: list[ValidationIssue],
) -> dict[str, dict[str, Any]]:
    entries = catalog.get(array_key)
    if not isinstance(entries, list):
        issues.append(
            ValidationIssue(location, f"catalog field '{array_key}' must be a list")
        )
        return {}

    entry_map: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            issues.append(
                ValidationIssue(
                    location,
                    f"catalog field '{array_key}[{index}]' must be an object",
                )
            )
            continue
        name = entry.get(key_name)
        if not isinstance(name, str):
            issues.append(
                ValidationIssue(
                    location,
                    f"catalog field '{array_key}[{index}].{key_name}' must be a string",
                )
            )
            continue
        entry_map[name] = entry
    return entry_map


def validate_generated_catalogs(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    full_path = repo_root / build_catalog.FULL_CATALOG_PATH
    min_path = repo_root / build_catalog.MIN_CATALOG_PATH

    full_text: str | None = None
    min_text: str | None = None
    full_data: dict[str, Any] | None = None
    min_data: dict[str, Any] | None = None

    for path in (full_path, min_path):
        if not path.is_file():
            issues.append(
                ValidationIssue(relative_location(path), "generated catalog is missing")
            )

    if full_path.is_file():
        full_text = full_path.read_text(encoding="utf-8")
        try:
            parsed = json.loads(full_text)
        except json.JSONDecodeError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(full_path),
                    f"invalid JSON: {exc.msg}",
                )
            )
        else:
            if isinstance(parsed, dict):
                full_data = parsed
            else:
                issues.append(
                    ValidationIssue(
                        relative_location(full_path),
                        "catalog must parse to an object",
                    )
                )

    if min_path.is_file():
        min_text = min_path.read_text(encoding="utf-8")
        try:
            parsed = json.loads(min_text)
        except json.JSONDecodeError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(min_path),
                    f"invalid JSON: {exc.msg}",
                )
            )
        else:
            if isinstance(parsed, dict):
                min_data = parsed
            else:
                issues.append(
                    ValidationIssue(
                        relative_location(min_path),
                        "catalog must parse to an object",
                    )
                )

    if full_data is None or min_data is None:
        return issues

    def project_min_catalog_safely(
        full_catalog: dict[str, Any],
        *,
        location: str,
        label: str,
    ) -> dict[str, Any] | None:
        try:
            return build_catalog.project_min_catalog(full_catalog)
        except (KeyError, TypeError):
            issues.append(
                ValidationIssue(
                    location,
                    f"{label} is malformed; min projection could not be computed",
                )
            )
            return None

    if skill_names is None:
        projected_min = project_min_catalog_safely(
            full_data,
            location=relative_location(full_path),
            label="generated catalog",
        )
        if projected_min is None:
            return issues
        if min_data != projected_min:
            issues.append(
                ValidationIssue(
                    relative_location(min_path),
                    "min catalog must be an exact projection of the full catalog",
                )
            )

        try:
            expected_full_text, expected_min_text = build_catalog.build_catalog_texts(repo_root)
        except (FileNotFoundError, ValueError):
            return issues

        if full_text is not None and full_text != expected_full_text:
            issues.append(
                ValidationIssue(
                    relative_location(full_path),
                    "generated catalog is out of date; run python scripts/build_catalog.py",
                )
            )
        if min_text is not None and min_text != expected_min_text:
            issues.append(
                ValidationIssue(
                    relative_location(min_path),
                    "generated catalog is out of date; run python scripts/build_catalog.py",
                )
            )
        return issues

    full_location = relative_location(full_path)
    min_location = relative_location(min_path)
    actual_full_entries = catalog_entries_by_name(
        full_data,
        array_key="skills",
        key_name="name",
        location=full_location,
        issues=issues,
    )
    actual_min_entries = catalog_entries_by_name(
        min_data,
        array_key="skills",
        key_name="name",
        location=min_location,
        issues=issues,
    )

    for skill_name in skill_names:
        expected_full_entry = build_catalog.build_skill_entry(repo_root, skill_name)
        expected_min_entry = build_catalog.project_min_catalog(
            {
                "catalog_version": build_catalog.CATALOG_VERSION,
                "source_of_truth": build_catalog.SOURCE_OF_TRUTH,
                "skills": [expected_full_entry],
            }
        )["skills"][0]

        actual_full_entry = actual_full_entries.get(skill_name)
        actual_min_entry = actual_min_entries.get(skill_name)
        if actual_full_entry is None:
            issues.append(
                ValidationIssue(
                    full_location,
                    f"generated catalog is missing skill '{skill_name}'",
                )
            )
            continue
        if actual_min_entry is None:
            issues.append(
                ValidationIssue(
                    min_location,
                    f"generated min catalog is missing skill '{skill_name}'",
                )
            )
            continue

        if actual_full_entry != expected_full_entry:
            issues.append(
                ValidationIssue(
                    full_location,
                    f"generated catalog entry for '{skill_name}' is out of date; run python scripts/build_catalog.py",
                )
            )
        if actual_min_entry != expected_min_entry:
            issues.append(
                ValidationIssue(
                    min_location,
                    f"generated min catalog entry for '{skill_name}' is out of date; run python scripts/build_catalog.py",
                )
            )
        projected_min_catalog_payload = project_min_catalog_safely(
            {
                "catalog_version": full_data.get("catalog_version"),
                "source_of_truth": full_data.get("source_of_truth"),
                "skills": [actual_full_entry],
            },
            location=full_location,
            label=f"generated catalog entry for '{skill_name}'",
        )
        if projected_min_catalog_payload is None:
            continue
        projected_min_entry = projected_min_catalog_payload["skills"][0]
        if actual_min_entry != projected_min_entry:
            issues.append(
                ValidationIssue(
                    min_location,
                    f"generated min catalog entry for '{skill_name}' must stay a projection of the full catalog",
                )
            )

    return issues


def validate_capsule_catalog_alignment(
    catalog_data: dict[str, Any],
    capsule_data: dict[str, Any],
    *,
    skill_names: Sequence[str] | None,
    issues: list[ValidationIssue],
    catalog_location: str,
    capsule_location: str,
) -> None:
    starting_issue_count = len(issues)
    catalog_entries = catalog_entries_by_name(
        catalog_data,
        array_key="skills",
        key_name="name",
        location=catalog_location,
        issues=issues,
    )
    capsule_entries = catalog_entries_by_name(
        capsule_data,
        array_key="skills",
        key_name="name",
        location=capsule_location,
        issues=issues,
    )
    if len(issues) != starting_issue_count:
        return

    if skill_names is None:
        missing = sorted(set(catalog_entries) - set(capsule_entries))
        extra = sorted(set(capsule_entries) - set(catalog_entries))
        for skill_name in missing:
            issues.append(
                ValidationIssue(
                    capsule_location,
                    f"generated capsules are missing skill '{skill_name}'",
                )
            )
        for skill_name in extra:
            issues.append(
                ValidationIssue(
                    capsule_location,
                    f"generated capsules include unknown skill '{skill_name}'",
                )
            )
        target_names = sorted(set(catalog_entries) & set(capsule_entries))
    else:
        target_names = list(skill_names)

    shared_fields = (
        "scope",
        "status",
        "summary",
        "invocation_mode",
        "technique_dependencies",
        "skill_path",
    )
    for skill_name in target_names:
        catalog_entry = catalog_entries.get(skill_name)
        capsule_entry = capsule_entries.get(skill_name)
        if catalog_entry is None or capsule_entry is None:
            continue
        for field_name in shared_fields:
            if capsule_entry.get(field_name) != catalog_entry.get(field_name):
                issues.append(
                    ValidationIssue(
                        capsule_location,
                        f"generated capsule entry for '{skill_name}' must align with full catalog field '{field_name}'",
                    )
                )


def validate_generated_capsules(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    capsule_path = repo_root / build_catalog.CAPSULE_PATH

    capsule_text: str | None = None
    capsule_data: dict[str, Any] | None = None

    if not capsule_path.is_file():
        issues.append(
            ValidationIssue(relative_location(capsule_path), "generated capsules are missing")
        )
        return issues

    capsule_text = capsule_path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(capsule_text)
    except json.JSONDecodeError as exc:
        issues.append(
            ValidationIssue(
                relative_location(capsule_path),
                f"invalid JSON: {exc.msg}",
            )
        )
        return issues

    if not isinstance(parsed, dict):
        issues.append(
            ValidationIssue(
                relative_location(capsule_path),
                "capsules must parse to an object",
            )
        )
        return issues

    capsule_data = parsed
    if capsule_data.get("capsule_version") != build_catalog.CAPSULE_VERSION:
        issues.append(
            ValidationIssue(
                relative_location(capsule_path),
                f"capsule_version must be {build_catalog.CAPSULE_VERSION}",
            )
        )
    if capsule_data.get("source_of_truth") != build_catalog.CAPSULE_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(
                relative_location(capsule_path),
                "capsule source_of_truth does not match the expected contract",
            )
        )
    if not isinstance(capsule_data.get("skills"), list):
        issues.append(
            ValidationIssue(
                relative_location(capsule_path),
                "capsules field 'skills' must be a list",
            )
        )
        return issues

    if skill_names is None:
        try:
            expected_capsule_text = build_catalog.build_capsule_text(repo_root)
        except (FileNotFoundError, ValueError) as exc:
            issues.append(
                ValidationIssue(
                    relative_location(capsule_path),
                    f"capsule source validation failed: {exc}",
                )
            )
            return issues

        if capsule_text != expected_capsule_text:
            issues.append(
                ValidationIssue(
                    relative_location(capsule_path),
                    "generated capsules are out of date; run python scripts/build_catalog.py",
                )
            )
    else:
        capsule_entries = catalog_entries_by_name(
            capsule_data,
            array_key="skills",
            key_name="name",
            location=relative_location(capsule_path),
            issues=issues,
        )
        for skill_name in skill_names:
            try:
                expected_capsule_entry = build_catalog.build_skill_capsule_entry(
                    repo_root, skill_name
                )
            except (FileNotFoundError, ValueError) as exc:
                issues.append(
                    ValidationIssue(
                        relative_location(capsule_path),
                        f"capsule source validation failed for '{skill_name}': {exc}",
                    )
                )
                continue

            actual_capsule_entry = capsule_entries.get(skill_name)
            if actual_capsule_entry is None:
                issues.append(
                    ValidationIssue(
                        relative_location(capsule_path),
                        f"generated capsules are missing skill '{skill_name}'",
                    )
                )
                continue
            if actual_capsule_entry != expected_capsule_entry:
                issues.append(
                    ValidationIssue(
                        relative_location(capsule_path),
                        f"generated capsule entry for '{skill_name}' is out of date; run python scripts/build_catalog.py",
                    )
                )

    full_catalog_path = repo_root / build_catalog.FULL_CATALOG_PATH
    if full_catalog_path.is_file():
        try:
            full_catalog_data = json.loads(full_catalog_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return issues
        if isinstance(full_catalog_data, dict):
            validate_capsule_catalog_alignment(
                full_catalog_data,
                capsule_data,
                skill_names=skill_names,
                issues=issues,
                catalog_location=relative_location(full_catalog_path),
                capsule_location=relative_location(capsule_path),
            )

    return issues


def validate_sections_catalog_alignment(
    full_catalog_data: dict[str, Any],
    sections_data: dict[str, Any],
    *,
    skill_names: Sequence[str] | None,
    issues: list[ValidationIssue],
    catalog_location: str,
    sections_location: str,
) -> None:
    starting_issue_count = len(issues)
    catalog_entries = catalog_entries_by_name(
        full_catalog_data,
        array_key="skills",
        key_name="name",
        location=catalog_location,
        issues=issues,
    )
    section_entries = catalog_entries_by_name(
        sections_data,
        array_key="skills",
        key_name="name",
        location=sections_location,
        issues=issues,
    )
    if len(issues) != starting_issue_count:
        return

    if skill_names is None:
        missing = sorted(set(catalog_entries) - set(section_entries))
        extra = sorted(set(section_entries) - set(catalog_entries))
        for skill_name in missing:
            issues.append(
                ValidationIssue(
                    sections_location,
                    f"generated sections are missing skill '{skill_name}'",
                )
            )
        for skill_name in extra:
            issues.append(
                ValidationIssue(
                    sections_location,
                    f"generated sections include unknown skill '{skill_name}'",
                )
            )
        target_names = sorted(set(catalog_entries) & set(section_entries))
    else:
        target_names = list(skill_names)

    shared_fields = ("scope", "status", "skill_path")
    for skill_name in target_names:
        catalog_entry = catalog_entries.get(skill_name)
        section_entry = section_entries.get(skill_name)
        if catalog_entry is None or section_entry is None:
            continue
        for field_name in shared_fields:
            if section_entry.get(field_name) != catalog_entry.get(field_name):
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"generated section entry for '{skill_name}' must align with full catalog field '{field_name}'",
                    )
                )


def validate_generated_sections(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    sections_path = repo_root / build_catalog.SECTIONS_PATH
    sections_location = relative_location(sections_path)

    if not sections_path.is_file():
        issues.append(
            ValidationIssue(sections_location, "generated sections are missing")
        )
        return issues

    sections_text = sections_path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(sections_text)
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(sections_location, f"invalid JSON: {exc.msg}"))
        return issues

    if not isinstance(parsed, dict):
        issues.append(
            ValidationIssue(sections_location, "sections must parse to an object")
        )
        return issues

    sections_data = parsed
    if sections_data.get("section_version") != build_catalog.SECTION_VERSION:
        issues.append(
            ValidationIssue(
                sections_location,
                f"section_version must be {build_catalog.SECTION_VERSION}",
            )
        )
    if sections_data.get("source_of_truth") != skill_section_contract.SECTION_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(
                sections_location,
                "section source_of_truth does not match the expected contract",
            )
        )
    if not isinstance(sections_data.get("skills"), list):
        issues.append(
            ValidationIssue(sections_location, "sections field 'skills' must be a list")
        )
        return issues

    if skill_names is None:
        try:
            expected_sections_text = build_catalog.build_sections_text(repo_root)
        except (FileNotFoundError, ValueError) as exc:
            issues.append(
                ValidationIssue(
                    sections_location,
                    f"section source validation failed: {exc}",
                )
            )
            return issues

        if sections_text != expected_sections_text:
            issues.append(
                ValidationIssue(
                    sections_location,
                    "generated sections are out of date; run python scripts/build_catalog.py",
                )
            )
    else:
        section_entries = catalog_entries_by_name(
            sections_data,
            array_key="skills",
            key_name="name",
            location=sections_location,
            issues=issues,
        )
        for skill_name in skill_names:
            skill_md_path = repo_root / SKILLS_DIR_NAME / skill_name / "SKILL.md"
            try:
                metadata, body = build_catalog.parse_skill_document(skill_md_path)
                expected_section_entry, contract_issues = skill_section_contract.build_sections_entry(
                    repo_root,
                    metadata,
                    skill_md_path,
                    body,
                )
            except (FileNotFoundError, ValueError) as exc:
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"section source validation failed for '{skill_name}': {exc}",
                    )
                )
                continue

            for contract_issue in contract_issues:
                issues.append(
                    ValidationIssue(contract_issue.location, contract_issue.message)
                )
            if contract_issues or expected_section_entry is None:
                continue

            actual_section_entry = section_entries.get(skill_name)
            if actual_section_entry is None:
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"generated sections are missing skill '{skill_name}'",
                    )
                )
                continue
            if actual_section_entry != expected_section_entry:
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"generated section entry for '{skill_name}' is out of date; run python scripts/build_catalog.py",
                    )
                )

    full_catalog_path = repo_root / build_catalog.FULL_CATALOG_PATH
    if full_catalog_path.is_file():
        try:
            full_catalog_data = json.loads(full_catalog_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return issues
        if isinstance(full_catalog_data, dict):
            validate_sections_catalog_alignment(
                full_catalog_data,
                sections_data,
                skill_names=skill_names,
                issues=issues,
                catalog_location=relative_location(full_catalog_path),
                sections_location=sections_location,
            )

    return issues


def validate_generated_walkthroughs(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    walkthrough_path = repo_root / build_catalog.WALKTHROUGHS_JSON_PATH
    walkthrough_markdown_path = repo_root / build_catalog.WALKTHROUGHS_MARKDOWN_PATH
    walkthrough_location = relative_location(walkthrough_path)
    walkthrough_markdown_location = relative_location(walkthrough_markdown_path)

    if not walkthrough_path.is_file():
        issues.append(
            ValidationIssue(
                walkthrough_location,
                "generated walkthrough surface is missing",
            )
        )
        if not walkthrough_markdown_path.is_file():
            issues.append(
                ValidationIssue(
                    walkthrough_markdown_location,
                    "generated walkthrough markdown is missing",
                )
            )
        return issues

    if not walkthrough_markdown_path.is_file():
        issues.append(
            ValidationIssue(
                walkthrough_markdown_location,
                "generated walkthrough markdown is missing",
            )
        )
        return issues

    walkthrough_text = walkthrough_path.read_text(encoding="utf-8")
    walkthrough_markdown_text = walkthrough_markdown_path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(walkthrough_text)
    except json.JSONDecodeError as exc:
        issues.append(
            ValidationIssue(
                walkthrough_location,
                f"invalid JSON: {exc.msg}",
            )
        )
        return issues

    if not isinstance(parsed, dict):
        issues.append(
            ValidationIssue(
                walkthrough_location,
                "walkthrough surface must parse to an object",
            )
        )
        return issues

    walkthrough_data = parsed
    if walkthrough_data.get("walkthrough_version") != build_catalog.WALKTHROUGH_VERSION:
        issues.append(
            ValidationIssue(
                walkthrough_location,
                f"walkthrough_version must be {build_catalog.WALKTHROUGH_VERSION}",
            )
        )
    if walkthrough_data.get("source_of_truth") != build_catalog.WALKTHROUGH_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(
                walkthrough_location,
                "walkthrough source_of_truth does not match the expected contract",
            )
        )
    if not isinstance(walkthrough_data.get("skills"), list):
        issues.append(
            ValidationIssue(
                walkthrough_location,
                "walkthrough surface field 'skills' must be a list",
            )
        )
        return issues

    try:
        expected_walkthrough_text, expected_walkthrough_markdown_text = (
            build_catalog.build_walkthrough_texts(repo_root)
        )
        expected_walkthrough_payload = build_catalog.build_walkthrough_payload(repo_root)
    except (FileNotFoundError, ValueError) as exc:
        issues.append(
            ValidationIssue(
                walkthrough_location,
                f"walkthrough source validation failed: {exc}",
            )
        )
        return issues

    if skill_names is None:
        if walkthrough_text != expected_walkthrough_text:
            issues.append(
                ValidationIssue(
                    walkthrough_location,
                    "generated walkthrough surface is out of date; run python scripts/build_catalog.py",
                )
            )
        if walkthrough_markdown_text != expected_walkthrough_markdown_text:
            issues.append(
                ValidationIssue(
                    walkthrough_markdown_location,
                    "generated walkthrough markdown is out of date; run python scripts/build_catalog.py",
                )
            )
        return issues

    actual_entries = catalog_entries_by_name(
        walkthrough_data,
        array_key="skills",
        key_name="name",
        location=walkthrough_location,
        issues=issues,
    )
    expected_entries = catalog_entries_by_name(
        expected_walkthrough_payload,
        array_key="skills",
        key_name="name",
        location=walkthrough_location,
        issues=[],
    )

    for skill_name in skill_names:
        actual_entry = actual_entries.get(skill_name)
        expected_entry = expected_entries.get(skill_name)
        if actual_entry is None:
            issues.append(
                ValidationIssue(
                    walkthrough_location,
                    f"generated walkthrough surface is missing skill '{skill_name}'",
                )
            )
            continue
        if expected_entry is None:
            continue
        if actual_entry != expected_entry:
            issues.append(
                ValidationIssue(
                    walkthrough_location,
                    f"generated walkthrough entry for '{skill_name}' is out of date; run python scripts/build_catalog.py",
                )
            )

    return issues


def validate_generated_public_surface(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    public_surface_path = repo_root / build_catalog.PUBLIC_SURFACE_JSON_PATH
    public_surface_markdown_path = repo_root / build_catalog.PUBLIC_SURFACE_MARKDOWN_PATH
    public_surface_location = relative_location(public_surface_path)
    public_surface_markdown_location = relative_location(public_surface_markdown_path)

    if not public_surface_path.is_file():
        issues.append(
            ValidationIssue(
                public_surface_location,
                "generated public surface is missing",
            )
        )
        if not public_surface_markdown_path.is_file():
            issues.append(
                ValidationIssue(
                    public_surface_markdown_location,
                    "generated public surface markdown is missing",
                )
            )
        return issues

    if not public_surface_markdown_path.is_file():
        issues.append(
            ValidationIssue(
                public_surface_markdown_location,
                "generated public surface markdown is missing",
            )
        )
        return issues

    public_surface_text = public_surface_path.read_text(encoding="utf-8")
    public_surface_markdown_text = public_surface_markdown_path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(public_surface_text)
    except json.JSONDecodeError as exc:
        issues.append(
            ValidationIssue(
                public_surface_location,
                f"invalid JSON: {exc.msg}",
            )
        )
        return issues

    if not isinstance(parsed, dict):
        issues.append(
            ValidationIssue(
                public_surface_location,
                "public surface must parse to an object",
            )
        )
        return issues

    public_surface_data = parsed
    if public_surface_data.get("public_surface_version") != build_catalog.PUBLIC_SURFACE_VERSION:
        issues.append(
            ValidationIssue(
                public_surface_location,
                f"public_surface_version must be {build_catalog.PUBLIC_SURFACE_VERSION}",
            )
        )
    if public_surface_data.get("source_of_truth") != build_catalog.PUBLIC_SURFACE_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(
                public_surface_location,
                "public surface source_of_truth does not match the expected contract",
            )
        )
    if not isinstance(public_surface_data.get("cohorts"), dict):
        issues.append(
            ValidationIssue(
                public_surface_location,
                "public surface field 'cohorts' must be an object",
            )
        )
    if not isinstance(public_surface_data.get("skills"), list):
        issues.append(
            ValidationIssue(
                public_surface_location,
                "public surface field 'skills' must be a list",
            )
        )
        return issues

    try:
        expected_public_surface_text, expected_public_surface_markdown_text = (
            build_catalog.build_public_surface_texts(repo_root)
        )
        expected_public_surface_payload = build_catalog.build_public_surface_payload(repo_root)
    except (FileNotFoundError, ValueError) as exc:
        issues.append(
            ValidationIssue(
                public_surface_location,
                f"public surface source validation failed: {exc}",
            )
        )
        return issues

    if skill_names is None:
        if public_surface_text != expected_public_surface_text:
            issues.append(
                ValidationIssue(
                    public_surface_location,
                    "generated public surface is out of date; run python scripts/build_catalog.py",
                )
            )
        if public_surface_markdown_text != expected_public_surface_markdown_text:
            issues.append(
                ValidationIssue(
                    public_surface_markdown_location,
                    "generated public surface markdown is out of date; run python scripts/build_catalog.py",
                )
            )
        return issues

    actual_entries = catalog_entries_by_name(
        public_surface_data,
        array_key="skills",
        key_name="name",
        location=public_surface_location,
        issues=issues,
    )
    expected_entries = catalog_entries_by_name(
        expected_public_surface_payload,
        array_key="skills",
        key_name="name",
        location=public_surface_location,
        issues=[],
    )
    actual_cohorts = public_surface_data.get("cohorts", {})
    expected_cohorts = expected_public_surface_payload.get("cohorts", {})
    cohort_names = (
        skill_governance_surface.DEFAULT_REFERENCES_COHORT,
        skill_governance_surface.CANDIDATE_READY_COHORT,
        skill_governance_surface.PENDING_LINEAGE_COHORT,
        skill_governance_surface.RISK_SURFACES_COHORT,
    )

    for skill_name in skill_names:
        actual_entry = actual_entries.get(skill_name)
        expected_entry = expected_entries.get(skill_name)
        if actual_entry is None:
            issues.append(
                ValidationIssue(
                    public_surface_location,
                    f"generated public surface is missing skill '{skill_name}'",
                )
            )
            continue
        if expected_entry is None:
            continue
        if actual_entry != expected_entry:
            issues.append(
                ValidationIssue(
                    public_surface_location,
                    f"generated public surface entry for '{skill_name}' is out of date; run python scripts/build_catalog.py",
                )
            )
        for cohort_name in cohort_names:
            actual_members = actual_cohorts.get(cohort_name, [])
            expected_members = expected_cohorts.get(cohort_name, [])
            if (skill_name in actual_members) != (skill_name in expected_members):
                issues.append(
                    ValidationIssue(
                        public_surface_location,
                        f"generated public surface cohorts for '{skill_name}' are out of date; run python scripts/build_catalog.py",
                    )
                )
                break

    return issues


def validate_generated_evaluation_matrix(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    matrix_path = repo_root / build_catalog.EVALUATION_MATRIX_JSON_PATH
    matrix_markdown_path = repo_root / build_catalog.EVALUATION_MATRIX_MARKDOWN_PATH
    matrix_location = relative_location(matrix_path)
    matrix_markdown_location = relative_location(matrix_markdown_path)

    if not matrix_path.is_file():
        issues.append(
            ValidationIssue(
                matrix_location,
                "generated evaluation matrix is missing",
            )
        )
        if not matrix_markdown_path.is_file():
            issues.append(
                ValidationIssue(
                    matrix_markdown_location,
                    "generated evaluation matrix markdown is missing",
                )
            )
        return issues

    if not matrix_markdown_path.is_file():
        issues.append(
            ValidationIssue(
                matrix_markdown_location,
                "generated evaluation matrix markdown is missing",
            )
        )
        return issues

    matrix_text = matrix_path.read_text(encoding="utf-8")
    matrix_markdown_text = matrix_markdown_path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(matrix_text)
    except json.JSONDecodeError as exc:
        issues.append(
            ValidationIssue(
                matrix_location,
                f"invalid JSON: {exc.msg}",
            )
        )
        return issues

    if not isinstance(parsed, dict):
        issues.append(
            ValidationIssue(
                matrix_location,
                "evaluation matrix must parse to an object",
            )
        )
        return issues

    matrix_data = parsed
    if matrix_data.get("evaluation_matrix_version") != build_catalog.EVALUATION_MATRIX_VERSION:
        issues.append(
            ValidationIssue(
                matrix_location,
                f"evaluation_matrix_version must be {build_catalog.EVALUATION_MATRIX_VERSION}",
            )
        )
    if matrix_data.get("source_of_truth") != build_catalog.EVALUATION_MATRIX_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(
                matrix_location,
                "evaluation matrix source_of_truth does not match the expected contract",
            )
        )
    if not isinstance(matrix_data.get("skills"), list):
        issues.append(
            ValidationIssue(
                matrix_location,
                "evaluation matrix field 'skills' must be a list",
            )
        )
        return issues

    try:
        expected_matrix_text, expected_matrix_markdown_text = (
            build_catalog.build_evaluation_matrix_texts(repo_root)
        )
        expected_matrix_payload = build_catalog.build_evaluation_matrix_payload(repo_root)
    except (FileNotFoundError, ValueError) as exc:
        issues.append(
            ValidationIssue(
                matrix_location,
                f"evaluation matrix source validation failed: {exc}",
            )
        )
        return issues

    if skill_names is None:
        if matrix_text != expected_matrix_text:
            issues.append(
                ValidationIssue(
                    matrix_location,
                    "generated evaluation matrix is out of date; run python scripts/build_catalog.py",
                )
            )
        if matrix_markdown_text != expected_matrix_markdown_text:
            issues.append(
                ValidationIssue(
                    matrix_markdown_location,
                    "generated evaluation matrix markdown is out of date; run python scripts/build_catalog.py",
                )
            )
        return issues

    actual_entries = catalog_entries_by_name(
        matrix_data,
        array_key="skills",
        key_name="name",
        location=matrix_location,
        issues=issues,
    )
    expected_entries = catalog_entries_by_name(
        expected_matrix_payload,
        array_key="skills",
        key_name="name",
        location=matrix_location,
        issues=[],
    )

    for skill_name in skill_names:
        actual_entry = actual_entries.get(skill_name)
        expected_entry = expected_entries.get(skill_name)
        if actual_entry is None:
            issues.append(
                ValidationIssue(
                    matrix_location,
                    f"generated evaluation matrix is missing skill '{skill_name}'",
                )
            )
            continue
        if expected_entry is None:
            continue
        if actual_entry != expected_entry:
            issues.append(
                ValidationIssue(
                    matrix_location,
                    f"generated evaluation matrix entry for '{skill_name}' is out of date; run python scripts/build_catalog.py",
                )
            )

    return issues


def format_issues(issues: Sequence[ValidationIssue]) -> str:
    lines = [f"- {issue.location}: {issue.message}" for issue in issues]
    return "\n".join(lines)


def run_validation(repo_root: Path, skill_name: str | None = None) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    all_skill_names = discover_skill_names(repo_root)
    bundle_issues_by_name: dict[str, list[ValidationIssue]] = {}
    if skill_name is not None:
        if skill_name not in all_skill_names:
            raise ValueError(f"unknown skill '{skill_name}'")
        target_skills = [skill_name]
        selected_skills = {skill_name}
    else:
        target_skills = all_skill_names
        selected_skills = None

    for name in target_skills:
        bundle_issues = validate_skill_bundle(repo_root, name)
        bundle_issues_by_name[name] = bundle_issues
        issues.extend(bundle_issues)

    issues.extend(validate_snapshot_fixture_contract(repo_root))
    issues.extend(validate_evaluation_floors(repo_root, target_skills))
    issues.extend(validate_canonical_status_floors(repo_root, target_skills))
    issues.extend(validate_skill_index(repo_root, selected_skills=selected_skills))
    if skill_name is None:
        issues.extend(validate_generated_catalogs(repo_root))
        issues.extend(validate_generated_capsules(repo_root))
        issues.extend(validate_generated_sections(repo_root))
        issues.extend(validate_generated_walkthroughs(repo_root))
        issues.extend(validate_generated_public_surface(repo_root))
        issues.extend(validate_generated_evaluation_matrix(repo_root))
    elif all(not bundle_issues_by_name[name] for name in target_skills):
        issues.extend(validate_generated_catalogs(repo_root, skill_names=target_skills))
        issues.extend(validate_generated_capsules(repo_root, skill_names=target_skills))
        issues.extend(validate_generated_sections(repo_root, skill_names=target_skills))
        issues.extend(validate_generated_walkthroughs(repo_root, skill_names=target_skills))
        issues.extend(validate_generated_public_surface(repo_root, skill_names=target_skills))
        issues.extend(validate_generated_evaluation_matrix(repo_root, skill_names=target_skills))
    return issues


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        issues = run_validation(repo_root, skill_name=args.skill)
    except ValueError as exc:
        print(f"Argument error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive runtime guard
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2

    if issues:
        scope = args.skill if args.skill else "repository"
        print(f"Validation failed for {scope}.")
        print(format_issues(issues))
        return 1

    if args.skill:
        print(f"Validation passed for skill '{args.skill}'.")
    else:
        skill_count = len(discover_skill_names(repo_root))
        print(f"Validation passed for {skill_count} skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
