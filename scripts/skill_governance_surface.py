from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import skill_catalog_contract
import skill_governance_lane_contract


PUBLIC_SURFACE_VERSION = 3
PUBLIC_SURFACE_JSON_PATH = Path("generated") / "public_surface.json"
PUBLIC_SURFACE_MARKDOWN_PATH = Path("generated") / "public_surface.md"
PUBLIC_SURFACE_SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "technique_manifest": "skills/*/techniques.yaml",
    "status_promotion_reviews": "docs/reviews/status-promotions/*.md",
    "canonical_candidate_reviews": "docs/reviews/canonical-candidates/*.md",
    "evaluation_fixtures": "tests/fixtures/skill_evaluation_cases.yaml",
    "governance_lanes": skill_governance_lane_contract.GOVERNANCE_LANES_PATH.as_posix(),
}

BLOCKER_STATUS_BELOW_EVALUATED = "status_below_evaluated"
BLOCKER_PENDING_TECHNIQUE_DEPENDENCIES = "pending_technique_dependencies"
BLOCKER_PENDING_TECHNIQUE_ENTRIES = "pending_technique_entries"
BLOCKER_TBD_TECHNIQUE_REFS = "tbd_technique_refs"
BLOCKER_MISSING_TRACEABILITY_HEADING = "missing_technique_traceability_heading"
BLOCKER_MISSING_AUTONOMY_CHECK = "missing_autonomy_check"
BLOCKER_MISSING_USE_CASE = "missing_use_case"
BLOCKER_MISSING_DO_NOT_USE_CASE = "missing_do_not_use_case"
BLOCKER_EXPLICIT_ONLY_POLICY_VIOLATION = "explicit_only_policy_violation"

DEFAULT_REFERENCES_COHORT = "default_references"
DEFAULT_REFERENCE_READY_COHORT = "default_reference_ready"
CANDIDATE_READY_COHORT = "candidate_ready"
PENDING_LINEAGE_COHORT = "blocked_by_pending_lineage"
RISK_SURFACES_COHORT = "risk_surfaces"

DEFAULT_REFERENCE_READINESS_READY = "ready"
DEFAULT_REFERENCE_READINESS_BLOCKED = "blocked"
DEFAULT_REFERENCE_READINESS_NOT_APPLICABLE = "not_applicable"

PENDING_LINEAGE_BLOCKERS = {
    BLOCKER_PENDING_TECHNIQUE_DEPENDENCIES,
    BLOCKER_PENDING_TECHNIQUE_ENTRIES,
    BLOCKER_TBD_TECHNIQUE_REFS,
}


@dataclass(frozen=True)
class EvaluationCoverage:
    has_autonomy_check: bool
    use_case_count: int
    do_not_use_case_count: int


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def collect_evaluation_coverage(
    fixtures: Mapping[str, Any] | None,
) -> dict[str, EvaluationCoverage]:
    coverage_by_skill: dict[str, dict[str, int | bool]] = {}
    if not isinstance(fixtures, Mapping):
        return {}

    for check in fixtures.get("autonomy_checks", []):
        if not isinstance(check, Mapping):
            continue
        skill_name = check.get("skill")
        if not isinstance(skill_name, str):
            continue
        coverage = coverage_by_skill.setdefault(
            skill_name,
            {
                "has_autonomy_check": False,
                "use_case_count": 0,
                "do_not_use_case_count": 0,
            },
        )
        coverage["has_autonomy_check"] = True

    for case in fixtures.get("trigger_cases", []):
        if not isinstance(case, Mapping):
            continue
        skill_name = case.get("skill")
        expected = case.get("expected")
        if not isinstance(skill_name, str) or expected not in {"use", "do_not_use"}:
            continue
        coverage = coverage_by_skill.setdefault(
            skill_name,
            {
                "has_autonomy_check": False,
                "use_case_count": 0,
                "do_not_use_case_count": 0,
            },
        )
        if expected == "use":
            coverage["use_case_count"] = int(coverage["use_case_count"]) + 1
        else:
            coverage["do_not_use_case_count"] = int(coverage["do_not_use_case_count"]) + 1

    return {
        skill_name: EvaluationCoverage(
            has_autonomy_check=bool(raw["has_autonomy_check"]),
            use_case_count=int(raw["use_case_count"]),
            do_not_use_case_count=int(raw["do_not_use_case_count"]),
        )
        for skill_name, raw in coverage_by_skill.items()
    }


def coverage_for_skill(
    coverage_by_skill: Mapping[str, EvaluationCoverage],
    skill_name: str,
) -> EvaluationCoverage:
    return coverage_by_skill.get(
        skill_name,
        EvaluationCoverage(
            has_autonomy_check=False,
            use_case_count=0,
            do_not_use_case_count=0,
        ),
    )


def has_pending_technique_dependencies(technique_dependencies: Sequence[Any]) -> bool:
    return any(
        isinstance(dependency, str) and dependency.startswith("AOA-T-PENDING-")
        for dependency in technique_dependencies
    )


def has_pending_technique_entries(techniques: Sequence[Mapping[str, Any]]) -> bool:
    return any(
        isinstance(technique.get("id"), str)
        and technique["id"].startswith("AOA-T-PENDING-")
        for technique in techniques
    )


def has_tbd_technique_refs(techniques: Sequence[Mapping[str, Any]]) -> bool:
    return any(
        technique.get("path") == "TBD" or technique.get("source_ref") == "TBD"
        for technique in techniques
    )


def derive_lineage_state(
    technique_dependencies: Sequence[Any],
    techniques: Sequence[Mapping[str, Any]],
) -> str:
    if has_pending_technique_dependencies(technique_dependencies):
        return "pending"
    if has_pending_technique_entries(techniques):
        return "pending"
    if has_tbd_technique_refs(techniques):
        return "pending"
    return "published"


def has_technique_traceability_heading(headings: set[str]) -> bool:
    return "Technique traceability" in headings and "Future traceability" not in headings


def has_explicit_only_policy_violation(
    invocation_mode: Any,
    *,
    policy_exists: bool,
    policy_allow_implicit_invocation: Any,
) -> bool:
    if invocation_mode != "explicit-only":
        return False
    if not policy_exists:
        return True
    return policy_allow_implicit_invocation is not False


def derive_canonical_candidate_blockers(
    *,
    status: Any,
    headings: set[str],
    technique_dependencies: Sequence[Any],
    techniques: Sequence[Mapping[str, Any]],
    evaluation_coverage: EvaluationCoverage,
    invocation_mode: Any,
    policy_exists: bool,
    policy_allow_implicit_invocation: Any,
) -> list[str]:
    blockers: list[str] = []

    if status not in {"evaluated", "canonical"}:
        blockers.append(BLOCKER_STATUS_BELOW_EVALUATED)
    if has_pending_technique_dependencies(technique_dependencies):
        blockers.append(BLOCKER_PENDING_TECHNIQUE_DEPENDENCIES)
    if has_pending_technique_entries(techniques):
        blockers.append(BLOCKER_PENDING_TECHNIQUE_ENTRIES)
    if has_tbd_technique_refs(techniques):
        blockers.append(BLOCKER_TBD_TECHNIQUE_REFS)
    if not has_technique_traceability_heading(headings):
        blockers.append(BLOCKER_MISSING_TRACEABILITY_HEADING)
    if not evaluation_coverage.has_autonomy_check:
        blockers.append(BLOCKER_MISSING_AUTONOMY_CHECK)
    if evaluation_coverage.use_case_count < 1:
        blockers.append(BLOCKER_MISSING_USE_CASE)
    if evaluation_coverage.do_not_use_case_count < 1:
        blockers.append(BLOCKER_MISSING_DO_NOT_USE_CASE)
    if has_explicit_only_policy_violation(
        invocation_mode,
        policy_exists=policy_exists,
        policy_allow_implicit_invocation=policy_allow_implicit_invocation,
    ):
        blockers.append(BLOCKER_EXPLICIT_ONLY_POLICY_VIOLATION)

    return blockers


def canonical_candidate_path_applies(
    *,
    scope: Any,
    governance_signals: skill_governance_lane_contract.GovernanceSkillSignals,
) -> bool:
    if scope != "project":
        return True
    return bool(
        governance_signals.governance_decision
        or governance_signals.governance_lane_ids
        or governance_signals.governance_evidence_case_ids
    )


def derive_canonical_candidate_ready(
    *,
    scope: Any,
    governance_signals: skill_governance_lane_contract.GovernanceSkillSignals,
    blockers: Sequence[str],
) -> bool:
    return canonical_candidate_path_applies(
        scope=scope,
        governance_signals=governance_signals,
    ) and not blockers


def derive_default_reference_readiness(
    *,
    scope: Any,
    governance_signals: skill_governance_lane_contract.GovernanceSkillSignals,
    blockers: Sequence[str],
) -> str:
    if not canonical_candidate_path_applies(
        scope=scope,
        governance_signals=governance_signals,
    ):
        return DEFAULT_REFERENCE_READINESS_NOT_APPLICABLE
    if blockers:
        return DEFAULT_REFERENCE_READINESS_BLOCKED
    return DEFAULT_REFERENCE_READINESS_READY


def derive_public_surface_skill_entry(
    *,
    skill_name: str,
    metadata: Mapping[str, Any],
    headings: set[str],
    techniques: Sequence[Mapping[str, Any]],
    evaluation_coverage: EvaluationCoverage,
    policy_exists: bool,
    policy_allow_implicit_invocation: Any,
    promotion_review_path: str | None,
    candidate_review_path: str | None,
    skill_path: str,
    governance_signals: skill_governance_lane_contract.GovernanceSkillSignals,
) -> dict[str, Any]:
    technique_dependencies = list(metadata.get("technique_dependencies", []))
    blockers = derive_canonical_candidate_blockers(
        status=metadata.get("status"),
        headings=headings,
        technique_dependencies=technique_dependencies,
        techniques=techniques,
        evaluation_coverage=evaluation_coverage,
        invocation_mode=metadata.get("invocation_mode"),
        policy_exists=policy_exists,
        policy_allow_implicit_invocation=policy_allow_implicit_invocation,
    )
    scope = metadata.get("scope")
    status = metadata.get("status")
    canonical_candidate_ready = derive_canonical_candidate_ready(
        scope=scope,
        governance_signals=governance_signals,
        blockers=blockers,
    )
    default_reference_readiness = derive_default_reference_readiness(
        scope=scope,
        governance_signals=governance_signals,
        blockers=blockers,
    )
    is_default_reference = (
        governance_signals.governance_decision
        == skill_governance_lane_contract.GOVERNANCE_DECISION_DEFAULT_REFERENCE
    )
    if governance_signals.governance_decision is None:
        is_default_reference = status == "canonical"

    return {
        "name": skill_name,
        "scope": scope,
        "status": status,
        "maturity_status": status,
        "summary": metadata.get("summary"),
        "invocation_mode": metadata.get("invocation_mode"),
        "skill_path": skill_path,
        "lineage_state": derive_lineage_state(technique_dependencies, techniques),
        "is_default_reference": is_default_reference,
        "governance_decision": governance_signals.governance_decision,
        "governance_lane_ids": list(governance_signals.governance_lane_ids),
        "governance_evidence_case_ids": list(
            governance_signals.governance_evidence_case_ids
        ),
        "default_reference_readiness": default_reference_readiness,
        "default_reference_readiness_blockers": (
            list(blockers)
            if default_reference_readiness == DEFAULT_REFERENCE_READINESS_BLOCKED
            else []
        ),
        "canonical_candidate_ready": canonical_candidate_ready,
        "canonical_candidate_blockers": blockers,
        "promotion_review_path": promotion_review_path,
        "candidate_review_path": candidate_review_path,
    }


def derive_public_surface_cohorts(skill_entries: Sequence[Mapping[str, Any]]) -> dict[str, list[str]]:
    default_references: list[str] = []
    default_reference_ready: list[str] = []
    candidate_ready: list[str] = []
    blocked_by_pending_lineage: list[str] = []
    risk_surfaces: list[str] = []

    for entry in skill_entries:
        skill_name = entry["name"]
        lineage_state = entry.get("lineage_state")
        if entry.get("is_default_reference"):
            default_references.append(skill_name)
        elif (
            entry.get("default_reference_readiness")
            == DEFAULT_REFERENCE_READINESS_READY
        ):
            default_reference_ready.append(skill_name)
            candidate_ready.append(skill_name)
        if lineage_state == "pending":
            blocked_by_pending_lineage.append(skill_name)
        if entry.get("scope") == "risk":
            risk_surfaces.append(skill_name)

    return {
        DEFAULT_REFERENCES_COHORT: sorted(default_references),
        DEFAULT_REFERENCE_READY_COHORT: sorted(default_reference_ready),
        CANDIDATE_READY_COHORT: sorted(candidate_ready),
        PENDING_LINEAGE_COHORT: sorted(blocked_by_pending_lineage),
        RISK_SURFACES_COHORT: sorted(risk_surfaces),
    }


def find_skill_entry(
    skill_entries: Sequence[Mapping[str, Any]],
    skill_name: str,
) -> Mapping[str, Any]:
    for entry in skill_entries:
        if entry.get("name") == skill_name:
            return entry
    raise KeyError(skill_name)


def format_path_or_dash(path_value: Any) -> str:
    if isinstance(path_value, str) and path_value:
        return f"`{path_value}`"
    return "-"


def format_blockers_or_dash(blockers: Sequence[Any]) -> str:
    blocker_values = [blocker for blocker in blockers if isinstance(blocker, str)]
    if blocker_values:
        return ", ".join(blocker_values)
    return "-"


def format_values_or_dash(values: Sequence[Any]) -> str:
    formatted_values = [value for value in values if isinstance(value, str) and value]
    if formatted_values:
        return ", ".join(formatted_values)
    return "-"


def render_public_surface_markdown(payload: Mapping[str, Any]) -> str:
    skill_entries = payload["skills"]
    cohorts = payload["cohorts"]
    default_reference_entries = [
        find_skill_entry(skill_entries, skill_name)
        for skill_name in cohorts[DEFAULT_REFERENCES_COHORT]
    ]
    default_reference_ready_entries = [
        find_skill_entry(skill_entries, skill_name)
        for skill_name in cohorts[DEFAULT_REFERENCE_READY_COHORT]
    ]
    blocked_by_pending_entries = [
        find_skill_entry(skill_entries, skill_name)
        for skill_name in cohorts[PENDING_LINEAGE_COHORT]
    ]
    risk_entries = [
        find_skill_entry(skill_entries, skill_name)
        for skill_name in cohorts[RISK_SURFACES_COHORT]
    ]

    lines = [
        "# Public surface",
        "",
        "This derived file summarizes the current public-product surface of `aoa-skills`.",
        "It is built from committed skill bundles, review records, and evaluation fixtures.",
        "",
        "## Summary",
        "",
        f"- total skills: {len(skill_entries)}",
        f"- default references: {len(default_reference_entries)}",
        f"- default-reference ready skills: {len(default_reference_ready_entries)}",
        f"- blocked by pending lineage: {len(blocked_by_pending_entries)}",
        f"- risk surfaces: {len(risk_entries)}",
        "",
    ]

    def append_table(title: str, entries: Sequence[Mapping[str, Any]]) -> None:
        lines.extend(
            [
                f"## {title}",
                "",
                "| name | maturity | readiness | scope | invocation | lineage | governance decision | lanes | readiness blockers | promotion review | candidate review |",
                "|---|---|---|---|---|---|---|---|---|---|---|",
            ]
        )
        if not entries:
            lines.append("| - | - | - | - | - | - | - | - | - | - | - |")
        else:
            for entry in entries:
                lines.append(
                    "| "
                    + " | ".join(
                        [
                            str(entry["name"]),
                            str(entry["maturity_status"]),
                            str(entry["default_reference_readiness"]),
                            str(entry["scope"]),
                            str(entry["invocation_mode"]),
                            str(entry["lineage_state"]),
                            str(entry.get("governance_decision") or "-"),
                            format_values_or_dash(entry.get("governance_lane_ids", [])),
                            format_blockers_or_dash(
                                entry["default_reference_readiness_blockers"]
                            ),
                            format_path_or_dash(entry["promotion_review_path"]),
                            format_path_or_dash(entry["candidate_review_path"]),
                        ]
                    )
                    + " |"
                )
        lines.append("")

    append_table("Default references", default_reference_entries)
    append_table("Default-reference ready cohort", default_reference_ready_entries)
    append_table("Blocked by pending lineage", blocked_by_pending_entries)
    append_table("Risk surfaces", risk_entries)

    lines.extend(
        [
            "## Legend",
            "",
            "- `maturity` is the source-owned skill status ladder (`scaffold` through `canonical`).",
            "- `default_reference_readiness` is the derived machine gate for default-reference consideration and stays separate from maturity.",
            "- `ready` means the current machine-readable default-reference gate passes for a governance-eligible path without implying promotion.",
            "- `blocked` means the default-reference path applies, but machine-checkable blockers remain visible.",
            "- `not_applicable` means the default-reference path does not currently apply, most notably for project overlays without a governance lane.",
            "- `stay_evaluated` means the current governance lane decision is to keep the skill evaluated in this wave even though its canonical gate checks may already pass.",
            "- `pending lineage` means upstream technique publication or refresh still blocks the canonical path.",
            "- `explicit-only` means the skill requires an explicit invocation posture and policy alignment.",
            "- `candidate_ready` remains in the JSON payload as a compatibility alias for the `default_reference_ready` cohort.",
            "",
        ]
    )
    return "\n".join(lines)
