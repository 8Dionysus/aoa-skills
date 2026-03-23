from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

import skill_catalog_contract
import skill_evaluation_surface
import skill_governance_lane_contract
import skill_governance_surface
import skill_source_model


GOVERNANCE_BACKLOG_VERSION = 2
GOVERNANCE_BACKLOG_JSON_PATH = Path("generated") / "governance_backlog.json"
GOVERNANCE_BACKLOG_MARKDOWN_PATH = Path("generated") / "governance_backlog.md"
GOVERNANCE_BACKLOG_SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "technique_manifest": "skills/*/techniques.yaml",
    "status_promotion_reviews": "docs/reviews/status-promotions/*.md",
    "canonical_candidate_reviews": "docs/reviews/canonical-candidates/*.md",
    "evaluation_fixtures": "tests/fixtures/skill_evaluation_cases.yaml",
    "governance_lanes": skill_governance_lane_contract.GOVERNANCE_LANES_PATH.as_posix(),
    "evaluation_matrix": "generated/skill_evaluation_matrix.json",
    "public_surface": "generated/public_surface.json",
}
CANDIDATE_READY_WITHOUT_REVIEW = "candidate_ready_without_review"
BLOCKED_BY_PENDING_LINEAGE = "blocked_by_pending_lineage"
CANONICAL_MAINTENANCE = "canonical_maintenance"
COMPARATIVE_PENDING = "comparative_pending"
DOCS_TRUTH_SYNC = "docs_truth_sync"
DOCS_TRUTH_PATHS = (
    Path("README.md"),
    Path("docs") / "README.md",
    Path("docs") / "ROADMAP.md",
    Path("docs") / "MATURITY_MODEL.md",
)
STALE_DOC_PHRASES = (
    "13 skills",
    "13 public skills",
)


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def docs_truth_sync_issues(repo_root: Path) -> list[str]:
    issues: list[str] = []
    for relative_path in DOCS_TRUTH_PATHS:
        path = repo_root / relative_path
        if not path.is_file():
            continue
        normalized = path.read_text(encoding="utf-8").lower()
        if any(phrase in normalized for phrase in STALE_DOC_PHRASES):
            issues.append(relative_path.as_posix())
    return sorted(issues)


def readiness_reconciliation(
    *,
    canonical_candidate_ready: bool,
    canonical_eval_ready: bool,
) -> str:
    if canonical_candidate_ready and canonical_eval_ready:
        return "governance_and_eval_ready"
    if canonical_candidate_ready and not canonical_eval_ready:
        return "governance_ready_but_eval_blocked"
    if not canonical_candidate_ready and canonical_eval_ready:
        return "eval_ready_but_governance_blocked"
    return "blocked_in_both"


def evaluation_entry_by_name(
    payload: Mapping[str, Any],
    skill_name: str,
) -> Mapping[str, Any]:
    for entry in payload.get("skills", []):
        if isinstance(entry, Mapping) and entry.get("name") == skill_name:
            return entry
    raise KeyError(skill_name)


def build_governance_backlog_payload(
    repo_root: Path,
    skill_names: Sequence[str],
) -> dict[str, Any]:
    public_payload = {
        "skills": [],
        "cohorts": {},
    }
    evaluation_payload = skill_evaluation_surface.build_evaluation_matrix_payload(
        repo_root,
        skill_names,
    )
    fixtures = skill_source_model.load_optional_yaml(
        repo_root / skill_governance_surface.PUBLIC_SURFACE_SOURCE_OF_TRUTH["evaluation_fixtures"]
    )
    coverage_by_skill = skill_governance_surface.collect_evaluation_coverage(fixtures)
    signals_by_skill = skill_governance_lane_contract.governance_skill_signals(
        skill_governance_lane_contract.load_governance_lanes(repo_root)
    )
    public_entries: list[dict[str, Any]] = []
    for source in skill_source_model.load_skill_sources(repo_root, skill_names):
        techniques = skill_catalog_contract.normalize_technique_refs(source.manifest)
        public_entries.append(
            skill_governance_surface.derive_public_surface_skill_entry(
                skill_name=source.name,
                metadata=source.metadata,
                headings=set(source.sections),
                techniques=techniques,
                evaluation_coverage=skill_governance_surface.coverage_for_skill(
                    coverage_by_skill,
                    source.name,
                ),
                policy_exists=source.policy_exists,
                policy_allow_implicit_invocation=source.policy_allow_implicit_invocation,
                promotion_review_path=source.promotion_review_path,
                candidate_review_path=source.candidate_review_path,
                skill_path=relative_location(source.skill_md_path, repo_root),
                governance_signals=skill_governance_lane_contract.governance_signals_for_skill(
                    signals_by_skill,
                    source.name,
                ),
            )
        )
    public_payload = {
        "skills": public_entries,
        "cohorts": skill_governance_surface.derive_public_surface_cohorts(public_entries),
    }

    skills: list[dict[str, Any]] = []
    for public_entry in public_entries:
        evaluation_entry = evaluation_entry_by_name(evaluation_payload, public_entry["name"])
        skills.append(
            {
                "name": public_entry["name"],
                "status": public_entry["status"],
                "scope": public_entry["scope"],
                "skill_path": public_entry["skill_path"],
                "lineage_state": public_entry["lineage_state"],
                "canonical_candidate_ready": public_entry["canonical_candidate_ready"],
                "canonical_candidate_blockers": list(
                    public_entry["canonical_candidate_blockers"]
                ),
                "canonical_eval_ready": evaluation_entry["canonical_eval_ready"],
                "canonical_eval_blockers": list(evaluation_entry["canonical_eval_blockers"]),
                "promotion_review_path": public_entry["promotion_review_path"],
                "candidate_review_path": public_entry["candidate_review_path"],
                "governance_decision": public_entry["governance_decision"],
                "governance_lane_ids": list(public_entry["governance_lane_ids"]),
                "governance_evidence_case_ids": list(
                    public_entry["governance_evidence_case_ids"]
                ),
                "readiness_reconciliation": readiness_reconciliation(
                    canonical_candidate_ready=bool(
                        public_entry["canonical_candidate_ready"]
                    ),
                    canonical_eval_ready=bool(evaluation_entry["canonical_eval_ready"]),
                ),
            }
        )

    docs_truth = docs_truth_sync_issues(repo_root)
    cohorts = {
        CANDIDATE_READY_WITHOUT_REVIEW: sorted(
            [
                entry["name"]
                for entry in skills
                if entry["canonical_candidate_ready"] and not entry["candidate_review_path"]
            ]
        ),
        BLOCKED_BY_PENDING_LINEAGE: list(
            public_payload["cohorts"].get(skill_governance_surface.PENDING_LINEAGE_COHORT, [])
        ),
        CANONICAL_MAINTENANCE: sorted(
            [
                entry["name"]
                for entry in skills
                if entry["governance_decision"]
                == skill_governance_lane_contract.GOVERNANCE_DECISION_DEFAULT_REFERENCE
            ]
        ),
        COMPARATIVE_PENDING: sorted(
            [
                entry["name"]
                for entry in skills
                if entry["governance_decision"]
                == skill_governance_lane_contract.GOVERNANCE_DECISION_STAY_EVALUATED
            ]
        ),
        DOCS_TRUTH_SYNC: docs_truth,
    }

    return {
        "governance_backlog_version": GOVERNANCE_BACKLOG_VERSION,
        "source_of_truth": GOVERNANCE_BACKLOG_SOURCE_OF_TRUTH,
        "cohorts": cohorts,
        "skills": skills,
    }


def render_governance_backlog_markdown(payload: Mapping[str, Any]) -> str:
    skill_entries = payload.get("skills", [])
    if not isinstance(skill_entries, list):
        raise ValueError("governance backlog field 'skills' must be a list")
    cohorts = payload.get("cohorts", {})
    docs_truth = cohorts.get(DOCS_TRUTH_SYNC, [])

    lines = [
        "# Governance backlog",
        "",
        "This derived file reconciles repo-local governance readiness and evaluation readiness without changing status.",
        "It is a backlog/maintenance view, not a promotion decision surface.",
        "",
        "## Summary",
        "",
        f"- total skills: {len(skill_entries)}",
        f"- candidate ready without review: {len(cohorts.get(CANDIDATE_READY_WITHOUT_REVIEW, []))}",
        f"- blocked by pending lineage: {len(cohorts.get(BLOCKED_BY_PENDING_LINEAGE, []))}",
        f"- canonical maintenance cohort: {len(cohorts.get(CANONICAL_MAINTENANCE, []))}",
        f"- comparative pending cohort: {len(cohorts.get(COMPARATIVE_PENDING, []))}",
        f"- docs truth-sync issues: {len(docs_truth)}",
        "",
        "| name | status | lineage | governance ready | eval ready | governance decision | lanes | reconciliation | candidate review | promotion review |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    if not skill_entries:
        lines.append("| - | - | - | - | - | - | - | - | - | - |")
    else:
        for entry in skill_entries:
            if not isinstance(entry, Mapping):
                continue
            candidate_review_path = entry.get("candidate_review_path") or "-"
            promotion_review_path = entry.get("promotion_review_path") or "-"
            governance_lane_ids = ", ".join(entry.get("governance_lane_ids", [])) or "-"
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(entry["name"]),
                        str(entry["status"]),
                        str(entry["lineage_state"]),
                        "true" if entry["canonical_candidate_ready"] else "false",
                        "true" if entry["canonical_eval_ready"] else "false",
                        str(entry.get("governance_decision") or "-"),
                        governance_lane_ids,
                        str(entry["readiness_reconciliation"]),
                        str(candidate_review_path),
                        str(promotion_review_path),
                    ]
                )
                + " |"
            )
    lines.extend(
        [
            "",
            "## Cohorts",
            "",
            f"- `{CANDIDATE_READY_WITHOUT_REVIEW}`: {', '.join(cohorts.get(CANDIDATE_READY_WITHOUT_REVIEW, [])) or '-'}",
            f"- `{BLOCKED_BY_PENDING_LINEAGE}`: {', '.join(cohorts.get(BLOCKED_BY_PENDING_LINEAGE, [])) or '-'}",
            f"- `{CANONICAL_MAINTENANCE}`: {', '.join(cohorts.get(CANONICAL_MAINTENANCE, [])) or '-'}",
            f"- `{COMPARATIVE_PENDING}`: {', '.join(cohorts.get(COMPARATIVE_PENDING, [])) or '-'}",
            f"- `{DOCS_TRUTH_SYNC}`: {', '.join(docs_truth) or '-'}",
            "",
        ]
    )
    return "\n".join(lines)
