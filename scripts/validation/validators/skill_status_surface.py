"""Status-floor validation phases for skill source bundles."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import yaml

from skill_model import skill_catalog_contract
from skill_model import skill_evaluation_contract
from skill_model import skill_governance_surface
from skill_model import skill_layout
from skill_model import skill_section_contract
from skill_model import skill_source_model


EVALUATION_FIXTURES_PATH = Path("tests") / "fixtures" / "skill_evaluation_cases.yaml"


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


def relative_location(repo_root: Path, path: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def load_evaluation_fixtures(repo_root: Path) -> dict[str, Any] | None:
    try:
        return skill_evaluation_contract.load_evaluation_fixtures(repo_root)
    except (ValueError, yaml.YAMLError):
        return None


def load_canonical_skill_source(
    repo_root: Path,
    skill_name: str,
) -> tuple[dict[str, Any], set[str], dict[str, Any], Path, Path] | None:
    skill_md_path = skill_layout.skill_md_path(repo_root, skill_name)
    techniques_path = skill_layout.techniques_path(repo_root, skill_name)
    try:
        metadata, body = skill_source_model.parse_skill_document(skill_md_path)
    except (FileNotFoundError, ValueError, yaml.YAMLError):
        return None
    if metadata.get("status") != "canonical":
        return None

    try:
        techniques_data = yaml.safe_load(techniques_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, yaml.YAMLError):
        return None
    if not isinstance(techniques_data, dict):
        return None

    section_pairs = skill_section_contract.extract_top_level_sections(body)
    return (
        metadata,
        {heading for heading, _content in section_pairs},
        techniques_data,
        skill_md_path,
        techniques_path,
    )


def validate_canonical_status_floors(
    repo_root: Path,
    target_skills: Sequence[str],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    canonical_skills: list[
        tuple[str, dict[str, Any], set[str], dict[str, Any], Path, Path]
    ] = []

    for skill_name in target_skills:
        source = load_canonical_skill_source(repo_root, skill_name)
        if source is None:
            continue
        metadata, headings, techniques_data, skill_md_path, techniques_path = source
        canonical_skills.append(
            (
                skill_name,
                metadata,
                headings,
                techniques_data,
                skill_md_path,
                techniques_path,
            )
        )

    if not canonical_skills:
        return issues

    fixtures = load_evaluation_fixtures(repo_root)
    if fixtures is None:
        return issues

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
        policy_exists, policy_allow_implicit_invocation = skill_source_model.load_policy_signal(
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
        skill_location = relative_location(repo_root, skill_md_path)
        techniques_location = relative_location(repo_root, techniques_path)

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
