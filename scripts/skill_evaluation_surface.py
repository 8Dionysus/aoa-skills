from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

import skill_artifact_contract
import skill_catalog_contract
import skill_evaluation_contract
import skill_governance_surface
import skill_runtime_surface


SKILLS_DIR_NAME = "skills"
EVALUATION_MATRIX_VERSION = 1
EVALUATION_MATRIX_JSON_PATH = Path("generated") / "skill_evaluation_matrix.json"
EVALUATION_MATRIX_MARKDOWN_PATH = Path("generated") / "skill_evaluation_matrix.md"
EVALUATION_MATRIX_SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "runtime_examples": "skills/*/examples/*.md",
    "review_checks": "skills/*/checks/review.md",
    "status_promotion_reviews": "docs/reviews/status-promotions/*.md",
    "canonical_candidate_reviews": "docs/reviews/canonical-candidates/*.md",
    "evaluation_fixtures": "tests/fixtures/skill_evaluation_cases.yaml",
    "evaluation_snapshots": "tests/fixtures/skill_evaluation_snapshots/*/*.md",
}
STATUS_PROMOTION_REVIEWS_DIR = Path("docs") / "reviews" / "status-promotions"
CANONICAL_CANDIDATES_DIR = Path("docs") / "reviews" / "canonical-candidates"


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def discover_skill_names(repo_root: Path) -> list[str]:
    skills_dir = repo_root / SKILLS_DIR_NAME
    if not skills_dir.is_dir():
        raise FileNotFoundError(f"missing skills directory at {skills_dir}")
    return sorted(path.name for path in skills_dir.iterdir() if path.is_dir())


def review_record_path(
    repo_root: Path,
    reviews_dir: Path,
    skill_name: str,
) -> str | None:
    review_path = repo_root / reviews_dir / f"{skill_name}.md"
    if review_path.is_file():
        return relative_location(review_path, repo_root)
    return None


def selected_runtime_artifact_path(repo_root: Path, skill_name: str) -> str | None:
    selected_path = skill_artifact_contract.preferred_runtime_artifact(
        repo_root / SKILLS_DIR_NAME / skill_name
    )
    if selected_path is None:
        return None
    return relative_location(selected_path, repo_root)


def build_skill_evaluation_entry(
    repo_root: Path,
    skill_name: str,
    *,
    evaluation_coverage_by_skill: Mapping[str, skill_governance_surface.EvaluationCoverage],
    snapshot_coverage_by_skill: Mapping[str, skill_evaluation_contract.SnapshotCoverage],
) -> dict[str, Any]:
    skill_md_path = repo_root / SKILLS_DIR_NAME / skill_name / "SKILL.md"
    metadata, _body = skill_runtime_surface.parse_skill_document(skill_md_path)
    evaluation_coverage = skill_governance_surface.coverage_for_skill(
        evaluation_coverage_by_skill,
        skill_name,
    )
    snapshot_coverage = skill_evaluation_contract.snapshot_coverage_for_skill(
        snapshot_coverage_by_skill,
        skill_name,
    )
    blockers = skill_evaluation_contract.derive_canonical_eval_blockers(
        snapshot_coverage_by_skill,
        skill_name,
    )

    return {
        "name": skill_name,
        "status": metadata.get("status"),
        "scope": metadata.get("scope"),
        "invocation_mode": metadata.get("invocation_mode"),
        "skill_path": relative_location(skill_md_path, repo_root),
        "autonomy_check_count": 1 if evaluation_coverage.has_autonomy_check else 0,
        "use_case_count": evaluation_coverage.use_case_count,
        "do_not_use_case_count": evaluation_coverage.do_not_use_case_count,
        "use_snapshot_count": snapshot_coverage.use_snapshot_count,
        "do_not_use_snapshot_count": snapshot_coverage.do_not_use_snapshot_count,
        "selected_runtime_artifact_path": selected_runtime_artifact_path(repo_root, skill_name),
        "promotion_review_path": review_record_path(
            repo_root,
            STATUS_PROMOTION_REVIEWS_DIR,
            skill_name,
        ),
        "candidate_review_path": review_record_path(
            repo_root,
            CANONICAL_CANDIDATES_DIR,
            skill_name,
        ),
        "canonical_eval_ready": not blockers,
        "canonical_eval_blockers": blockers,
    }


def build_evaluation_matrix_payload(
    repo_root: Path,
    skill_names: Sequence[str],
) -> dict[str, Any]:
    fixtures = skill_evaluation_contract.load_evaluation_fixtures(repo_root) or {}
    evaluation_coverage_by_skill = skill_governance_surface.collect_evaluation_coverage(
        fixtures
    )
    snapshot_coverage_by_skill = skill_evaluation_contract.collect_snapshot_coverage(
        repo_root,
        fixtures,
    )
    return {
        "evaluation_matrix_version": EVALUATION_MATRIX_VERSION,
        "source_of_truth": EVALUATION_MATRIX_SOURCE_OF_TRUTH,
        "skills": [
            build_skill_evaluation_entry(
                repo_root,
                skill_name,
                evaluation_coverage_by_skill=evaluation_coverage_by_skill,
                snapshot_coverage_by_skill=snapshot_coverage_by_skill,
            )
            for skill_name in skill_names
        ],
    }


def find_skill_evaluation_entry(
    payload: Mapping[str, Any],
    skill_name: str,
) -> Mapping[str, Any]:
    skills = payload.get("skills", [])
    if not isinstance(skills, list):
        raise KeyError(skill_name)
    for entry in skills:
        if isinstance(entry, Mapping) and entry.get("name") == skill_name:
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


def render_evaluation_matrix_markdown(payload: Mapping[str, Any]) -> str:
    skill_entries = payload.get("skills", [])
    if not isinstance(skill_entries, list):
        raise ValueError("evaluation matrix field 'skills' must be a list")

    canonical_entries = [
        entry
        for entry in skill_entries
        if isinstance(entry, Mapping) and entry.get("status") == "canonical"
    ]
    canonical_gap_entries = [
        entry
        for entry in canonical_entries
        if isinstance(entry, Mapping) and not entry.get("canonical_eval_ready")
    ]

    lines = [
        "# Skill evaluation matrix",
        "",
        "This derived file summarizes deterministic evaluation evidence for `aoa-skills`.",
        "It is built from committed skill bundles, runtime artifacts, review records,",
        "evaluation fixtures, and authored snapshot-backed evidence files.",
        "",
        "## Summary",
        "",
        f"- total skills: {len(skill_entries)}",
        f"- canonical skills: {len(canonical_entries)}",
        f"- canonical skills with eval gaps: {len(canonical_gap_entries)}",
        "",
        "| name | status | scope | invocation | autonomy | use cases | do_not_use cases | use snapshots | do_not_use snapshots | runtime artifact | promotion review | candidate review | canonical eval ready | blockers |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|",
    ]
    if not skill_entries:
        lines.append("| - | - | - | - | - | - | - | - | - | - | - | - | - | - |")
    else:
        for entry in skill_entries:
            if not isinstance(entry, Mapping):
                continue
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(entry["name"]),
                        str(entry["status"]),
                        str(entry["scope"]),
                        str(entry["invocation_mode"]),
                        str(entry["autonomy_check_count"]),
                        str(entry["use_case_count"]),
                        str(entry["do_not_use_case_count"]),
                        str(entry["use_snapshot_count"]),
                        str(entry["do_not_use_snapshot_count"]),
                        format_path_or_dash(entry["selected_runtime_artifact_path"]),
                        format_path_or_dash(entry["promotion_review_path"]),
                        format_path_or_dash(entry["candidate_review_path"]),
                        "true" if entry["canonical_eval_ready"] else "false",
                        format_blockers_or_dash(entry["canonical_eval_blockers"]),
                    ]
                )
                + " |"
            )
    lines.extend(
        [
            "",
            "## Reading notes",
            "",
            "- Runtime artifacts support inspection and object use, but do not replace `SKILL.md` as the meaning-authoritative source.",
            "- The evaluation matrix is a separate derived evidence layer from the runtime walkthroughs and the public/governance surface.",
            "- In this wave, `canonical` skills must pass the snapshot-backed eval floor; other `evaluated` skills may still show reportable snapshot gaps without failing status.",
            "",
        ]
    )
    return "\n".join(lines)
