from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Mapping, Sequence

import yaml

import skill_catalog_contract
import skill_evaluation_contract
import skill_source_model


GOVERNANCE_LANES_VERSION = 1
GOVERNANCE_LANES_PATH = Path("docs") / "governance" / "lanes.yaml"
GOVERNANCE_LANES_SCHEMA = "governance_lanes.schema.json"
GOVERNANCE_DECISION_DEFAULT_REFERENCE = "default_reference"
GOVERNANCE_DECISION_STAY_EVALUATED = "stay_evaluated"
GOVERNANCE_LANE_STATE_STABLE_DEFAULTS = "stable_defaults"
GOVERNANCE_LANE_STATE_COMPARATIVE_PENDING = "comparative_pending"
ALLOWED_GOVERNANCE_DECISIONS = {
    GOVERNANCE_DECISION_DEFAULT_REFERENCE,
    GOVERNANCE_DECISION_STAY_EVALUATED,
}
ALLOWED_GOVERNANCE_LANE_STATES = {
    GOVERNANCE_LANE_STATE_STABLE_DEFAULTS,
    GOVERNANCE_LANE_STATE_COMPARATIVE_PENDING,
}


@dataclass(frozen=True)
class GovernanceLaneIssue:
    location: str
    message: str


@dataclass(frozen=True)
class GovernanceLaneSkill:
    name: str
    decision: str


@dataclass(frozen=True)
class GovernanceLane:
    lane_id: str
    title: str
    scope: str
    state: str
    skills: tuple[GovernanceLaneSkill, ...]
    review_path: str
    evidence_case_ids: tuple[str, ...]


@dataclass(frozen=True)
class GovernanceSkillSignals:
    governance_decision: str | None
    governance_lane_ids: tuple[str, ...]
    governance_evidence_case_ids: tuple[str, ...]


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def strip_anchor(path_value: str) -> str:
    return path_value.split("#", 1)[0]


def normalize_repo_relative_path(path_value: str) -> str | None:
    normalized = strip_anchor(path_value).replace("\\", "/")
    if not normalized:
        return None
    if re.match(r"^[A-Za-z]:/", normalized) or normalized.startswith(("/", "//")):
        return None
    if ".." in Path(normalized).parts:
        return None
    return normalized


def load_governance_lane_document(repo_root: Path) -> dict[str, Any] | None:
    path = repo_root / GOVERNANCE_LANES_PATH
    if not path.is_file():
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(
            f"{relative_location(path, repo_root)} invalid YAML: {exc}"
        ) from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(
            f"{relative_location(path, repo_root)} must parse to a mapping"
        )
    return data


def load_governance_lanes(repo_root: Path) -> list[GovernanceLane]:
    payload = load_governance_lane_document(repo_root)
    if not isinstance(payload, Mapping):
        return []
    raw_lanes = payload.get("lanes", [])
    if not isinstance(raw_lanes, list):
        raise ValueError(
            f"{relative_location(repo_root / GOVERNANCE_LANES_PATH, repo_root)} field 'lanes' must be a list"
        )

    lanes: list[GovernanceLane] = []
    for raw_lane in raw_lanes:
        if not isinstance(raw_lane, Mapping):
            continue
        raw_skills = raw_lane.get("skills", [])
        if not isinstance(raw_skills, list):
            continue
        skills: list[GovernanceLaneSkill] = []
        for raw_skill in raw_skills:
            if not isinstance(raw_skill, Mapping):
                continue
            skill_name = raw_skill.get("name")
            decision = raw_skill.get("decision")
            if not isinstance(skill_name, str) or not isinstance(decision, str):
                continue
            skills.append(
                GovernanceLaneSkill(
                    name=skill_name,
                    decision=decision,
                )
            )
        lane_id = raw_lane.get("id")
        title = raw_lane.get("title")
        scope = raw_lane.get("scope")
        state = raw_lane.get("state")
        review_path = raw_lane.get("review_path")
        evidence_case_ids = raw_lane.get("evidence_case_ids", [])
        if not (
            isinstance(lane_id, str)
            and isinstance(title, str)
            and isinstance(scope, str)
            and isinstance(state, str)
            and isinstance(review_path, str)
            and isinstance(evidence_case_ids, list)
        ):
            continue
        lanes.append(
            GovernanceLane(
                lane_id=lane_id,
                title=title,
                scope=scope,
                state=state,
                skills=tuple(skills),
                review_path=review_path,
                evidence_case_ids=tuple(
                    case_id
                    for case_id in evidence_case_ids
                    if isinstance(case_id, str)
                ),
            )
        )
    return lanes


def governance_skill_signals(
    lanes: Sequence[GovernanceLane],
) -> dict[str, GovernanceSkillSignals]:
    skill_decisions: dict[str, str | None] = {}
    skill_lane_ids: dict[str, set[str]] = {}
    skill_evidence_case_ids: dict[str, set[str]] = {}

    for lane in lanes:
        for lane_skill in lane.skills:
            existing = skill_decisions.get(lane_skill.name)
            if existing is not None and existing != lane_skill.decision:
                raise ValueError(
                    f"skill '{lane_skill.name}' has conflicting governance decisions"
                )
            skill_decisions[lane_skill.name] = lane_skill.decision
            skill_lane_ids.setdefault(lane_skill.name, set()).add(lane.lane_id)
            skill_evidence_case_ids.setdefault(lane_skill.name, set()).update(
                lane.evidence_case_ids
            )

    return {
        skill_name: GovernanceSkillSignals(
            governance_decision=skill_decisions.get(skill_name),
            governance_lane_ids=tuple(sorted(skill_lane_ids.get(skill_name, set()))),
            governance_evidence_case_ids=tuple(
                sorted(skill_evidence_case_ids.get(skill_name, set()))
            ),
        )
        for skill_name in sorted(skill_decisions)
    }


def governance_lane_ids_by_case(
    lanes: Sequence[GovernanceLane],
) -> dict[str, tuple[str, ...]]:
    lane_ids_by_case: dict[str, set[str]] = {}
    for lane in lanes:
        for case_id in lane.evidence_case_ids:
            lane_ids_by_case.setdefault(case_id, set()).add(lane.lane_id)
    return {
        case_id: tuple(sorted(lane_ids))
        for case_id, lane_ids in lane_ids_by_case.items()
    }


def default_governance_skill_signals() -> GovernanceSkillSignals:
    return GovernanceSkillSignals(
        governance_decision=None,
        governance_lane_ids=(),
        governance_evidence_case_ids=(),
    )


def governance_signals_for_skill(
    signals_by_skill: Mapping[str, GovernanceSkillSignals],
    skill_name: str,
) -> GovernanceSkillSignals:
    return signals_by_skill.get(skill_name, default_governance_skill_signals())


def validate_governance_lanes(
    repo_root: Path,
    *,
    skill_names: Sequence[str] | None = None,
) -> list[GovernanceLaneIssue]:
    issues: list[GovernanceLaneIssue] = []
    manifest_path = repo_root / GOVERNANCE_LANES_PATH
    known_sources: dict[str, Mapping[str, Any]] = {}
    try:
        discovered_skill_names = skill_source_model.discover_skill_names(repo_root)
    except FileNotFoundError:
        discovered_skill_names = []
    for skill_name in discovered_skill_names:
        skill_md_path = repo_root / "skills" / skill_name / "SKILL.md"
        if not skill_md_path.is_file():
            continue
        try:
            metadata, _body = skill_source_model.parse_skill_document(skill_md_path)
        except (FileNotFoundError, ValueError, yaml.YAMLError):
            continue
        if isinstance(metadata, Mapping):
            known_sources[skill_name] = metadata
    target_skill_names = set(skill_names or known_sources.keys())
    payload = load_governance_lane_document(repo_root)
    location = relative_location(manifest_path, repo_root)
    if payload is None:
        if any(
            skill_name.startswith("aoa-")
            and metadata.get("status") in {"evaluated", "canonical"}
            and skill_name in target_skill_names
            for skill_name, metadata in known_sources.items()
        ):
            issues.append(
                GovernanceLaneIssue(
                    location=location,
                    message="governance lanes manifest is missing",
                )
            )
        return issues
    if payload.get("governance_lanes_version") != GOVERNANCE_LANES_VERSION:
        issues.append(
            GovernanceLaneIssue(
                location=location,
                message=(
                    "governance_lanes_version must be "
                    f"{GOVERNANCE_LANES_VERSION}"
                ),
            )
        )

    try:
        lanes = load_governance_lanes(repo_root)
    except ValueError as exc:
        issues.append(
            GovernanceLaneIssue(
                location=location,
                message=str(exc),
            )
        )
        return issues

    fixtures = skill_evaluation_contract.load_evaluation_fixtures(repo_root) or {}
    adjacency_cases = {
        str(case.get("case_id")): case
        for case in skill_evaluation_contract.adjacency_cases(fixtures)
        if isinstance(case.get("case_id"), str)
    }
    governed_skill_names: set[str] = set()
    decision_by_skill: dict[str, str] = {}
    seen_lane_ids: set[str] = set()

    for lane_index, lane in enumerate(lanes):
        lane_location = f"{location}:lanes[{lane_index}]"
        lane_skill_names = {lane_skill.name for lane_skill in lane.skills}

        if lane.lane_id in seen_lane_ids:
            issues.append(
                GovernanceLaneIssue(
                    location=f"{lane_location}.id",
                    message=f"governance lane id '{lane.lane_id}' must be unique",
                )
            )
        else:
            seen_lane_ids.add(lane.lane_id)

        if lane.state not in ALLOWED_GOVERNANCE_LANE_STATES:
            issues.append(
                GovernanceLaneIssue(
                    location=f"{lane_location}.state",
                    message="governance lane state must be 'stable_defaults' or 'comparative_pending'",
                )
            )

        relative_review_path = normalize_repo_relative_path(lane.review_path)
        if relative_review_path is None:
            issues.append(
                GovernanceLaneIssue(
                    location=f"{lane_location}.review_path",
                    message=f"governance lane review_path '{lane.review_path}' must be repo-relative",
                )
            )
        else:
            review_path = repo_root / relative_review_path
            if not review_path.is_file():
                issues.append(
                    GovernanceLaneIssue(
                        location=f"{lane_location}.review_path",
                        message=f"governance lane review_path '{lane.review_path}' must reference an existing file",
                    )
                )

        has_stay_evaluated = False
        for skill_index, lane_skill in enumerate(lane.skills):
            skill_location = f"{lane_location}.skills[{skill_index}]"
            metadata = known_sources.get(lane_skill.name)
            if metadata is None:
                issues.append(
                    GovernanceLaneIssue(
                        location=f"{skill_location}.name",
                        message=f"governance lane references unknown skill '{lane_skill.name}'",
                    )
                )
                continue
            if (
                not lane_skill.name.startswith("aoa-")
                or metadata.get("scope") == "project"
            ):
                issues.append(
                    GovernanceLaneIssue(
                        location=f"{skill_location}.name",
                        message=f"governance lanes may only reference aoa-* public skills, not '{lane_skill.name}'",
                    )
                )

            if lane_skill.decision not in ALLOWED_GOVERNANCE_DECISIONS:
                issues.append(
                    GovernanceLaneIssue(
                        location=f"{skill_location}.decision",
                        message="governance decision must be 'default_reference' or 'stay_evaluated'",
                    )
                )
                continue

            if lane_skill.decision == GOVERNANCE_DECISION_STAY_EVALUATED:
                has_stay_evaluated = True

            status = metadata.get("status")
            if (
                lane_skill.decision == GOVERNANCE_DECISION_DEFAULT_REFERENCE
                and status != "canonical"
            ):
                issues.append(
                    GovernanceLaneIssue(
                        location=f"{skill_location}.decision",
                        message=(
                            f"skill '{lane_skill.name}' uses decision 'default_reference' "
                            "but is not currently 'canonical'"
                        ),
                    )
                )
            if (
                lane_skill.decision == GOVERNANCE_DECISION_STAY_EVALUATED
                and status != "evaluated"
            ):
                issues.append(
                    GovernanceLaneIssue(
                        location=f"{skill_location}.decision",
                        message=(
                            f"skill '{lane_skill.name}' uses decision 'stay_evaluated' "
                            "but is not currently 'evaluated'"
                        ),
                    )
                )

            existing_decision = decision_by_skill.get(lane_skill.name)
            if existing_decision is not None and existing_decision != lane_skill.decision:
                issues.append(
                    GovernanceLaneIssue(
                        location=f"{skill_location}.decision",
                        message=(
                            f"skill '{lane_skill.name}' has conflicting governance decisions "
                            f"('{existing_decision}' vs '{lane_skill.decision}') across lanes"
                        ),
                    )
                )
            decision_by_skill[lane_skill.name] = lane_skill.decision
            governed_skill_names.add(lane_skill.name)

        if lane.state == GOVERNANCE_LANE_STATE_STABLE_DEFAULTS and has_stay_evaluated:
            issues.append(
                GovernanceLaneIssue(
                    location=f"{lane_location}.state",
                    message="stable_defaults lanes cannot include 'stay_evaluated' decisions",
                )
            )
        if lane.state == GOVERNANCE_LANE_STATE_COMPARATIVE_PENDING and not has_stay_evaluated:
            issues.append(
                GovernanceLaneIssue(
                    location=f"{lane_location}.state",
                    message="comparative_pending lanes must include at least one 'stay_evaluated' decision",
                )
            )

        for case_index, case_id in enumerate(lane.evidence_case_ids):
            case_location = f"{lane_location}.evidence_case_ids[{case_index}]"
            case = adjacency_cases.get(case_id)
            if case is None:
                issues.append(
                    GovernanceLaneIssue(
                        location=case_location,
                        message=(
                            f"governance lane evidence_case_id '{case_id}' must reference an existing adjacency case"
                        ),
                    )
                )
                continue

            case_skill = case.get("skill")
            adjacent_skill = case.get("adjacent_skill")
            if case_skill not in lane_skill_names or adjacent_skill not in lane_skill_names:
                issues.append(
                    GovernanceLaneIssue(
                        location=case_location,
                        message=(
                            f"governance lane evidence_case_id '{case_id}' must stay within the lane skill set"
                        ),
                    )
                )

    for skill_name, metadata in known_sources.items():
        status = metadata.get("status")
        if skill_name not in target_skill_names:
            continue
        if not skill_name.startswith("aoa-"):
            continue
        if status not in {"evaluated", "canonical"}:
            continue
        if skill_name not in governed_skill_names:
            issues.append(
                GovernanceLaneIssue(
                    location=location,
                    message=(
                        f"skill '{skill_name}' with status '{status}' requires governance lane coverage"
                    ),
                )
            )

    return issues
