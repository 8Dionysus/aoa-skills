from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import skill_artifact_contract
import skill_catalog_contract
import skill_source_model


SKILL_COMPOSITION_VERSION = 1
SKILL_COMPOSITION_JSON_PATH = Path("generated") / "skill_composition_audit.json"
SKILL_COMPOSITION_MARKDOWN_PATH = Path("generated") / "skill_composition_audit.md"
COMPOSITION_EXCEPTION_REVIEWS_DIR = (
    Path("docs") / "reviews" / "skill-composition-exceptions"
)
COMPOSITION_EXCEPTION_REVIEW_HEADINGS = (
    "Current shape",
    "Package rationale",
    "Why this is not just the technique",
    "Adjacent skills considered",
    "Recommendation",
)
COMPOSITION_RECOMMENDATION_KEEP_EXCEPTION = "keep_exception"
COMPOSITION_RECOMMENDATION_REFRAME = "reframe_multi_technique"
COMPOSITION_RECOMMENDATION_MERGE_OR_REMOVE = "merge_or_remove"
COMPOSITION_RECOMMENDATIONS = (
    COMPOSITION_RECOMMENDATION_KEEP_EXCEPTION,
    COMPOSITION_RECOMMENDATION_REFRAME,
    COMPOSITION_RECOMMENDATION_MERGE_OR_REMOVE,
)
COMPOSITION_CLASS_MULTI_TECHNIQUE = "multi_technique"
COMPOSITION_CLASS_SINGLE_EXCEPTION = "single_technique_exception"
COMPOSITION_CLASS_SINGLE_NEEDS_REFRAME = "single_technique_needs_reframe"
SKILL_COMPOSITION_SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "technique_manifest": "skills/*/techniques.yaml",
    "exception_reviews": "docs/reviews/skill-composition-exceptions/*.md",
}
RECOMMENDATION_PATTERN = re.compile(
    r"`(keep_exception|reframe_multi_technique|merge_or_remove)`"
    r"|\b(keep_exception|reframe_multi_technique|merge_or_remove)\b"
)


@dataclass(frozen=True)
class CompositionReviewAnalysis:
    review_path: str | None
    recommendation: str | None
    is_valid: bool
    issues: tuple[str, ...]


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def exception_review_file_path(repo_root: Path, skill_name: str) -> Path:
    return repo_root / COMPOSITION_EXCEPTION_REVIEWS_DIR / f"{skill_name}.md"


def exception_review_path(repo_root: Path, skill_name: str) -> str | None:
    review_path = exception_review_file_path(repo_root, skill_name)
    if review_path.is_file():
        return relative_location(review_path, repo_root)
    return None


def _extract_recommendation(section_text: str) -> str | None:
    values: list[str] = []
    for match in RECOMMENDATION_PATTERN.finditer(section_text):
        value = next(
            (
                candidate
                for candidate in match.groups()
                if isinstance(candidate, str) and candidate
            ),
            None,
        )
        if value is not None and value not in values:
            values.append(value)
    if len(values) != 1:
        return None
    return values[0]


def analyze_exception_review(repo_root: Path, skill_name: str) -> CompositionReviewAnalysis:
    review_path = exception_review_file_path(repo_root, skill_name)
    location = exception_review_path(repo_root, skill_name)
    if not review_path.is_file() or location is None:
        return CompositionReviewAnalysis(
            review_path=None,
            recommendation=None,
            is_valid=False,
            issues=(),
        )

    section_pairs = skill_artifact_contract.extract_artifact_sections(
        review_path.read_text(encoding="utf-8")
    )
    issues: list[str] = [
        issue.message
        for issue in skill_artifact_contract.collect_heading_contract_issues(
            section_pairs,
            location=location,
            artifact_label="skill composition exception review",
            expected_headings=COMPOSITION_EXCEPTION_REVIEW_HEADINGS,
        )
    ]

    recommendation: str | None = None
    if not issues:
        section_map = {heading: content for heading, content in section_pairs}
        recommendation = _extract_recommendation(section_map.get("Recommendation", ""))
        if recommendation is None:
            issues.append(
                "skill composition exception review must contain exactly one allowed recommendation value"
            )

    return CompositionReviewAnalysis(
        review_path=location,
        recommendation=recommendation,
        is_valid=not issues,
        issues=tuple(issues),
    )


def technique_ids_from_source(source: skill_source_model.SkillSource) -> list[str]:
    return skill_catalog_contract.technique_ids_from_manifest(source.manifest)


def composition_entry_for_source(
    repo_root: Path,
    source: skill_source_model.SkillSource,
) -> dict[str, Any]:
    technique_ids = technique_ids_from_source(source)
    review = analyze_exception_review(repo_root, source.name)

    if len(technique_ids) >= 2:
        composition_class = COMPOSITION_CLASS_MULTI_TECHNIQUE
        recommended_action = "keep_multi_technique"
    elif (
        review.is_valid
        and review.recommendation == COMPOSITION_RECOMMENDATION_KEEP_EXCEPTION
    ):
        composition_class = COMPOSITION_CLASS_SINGLE_EXCEPTION
        recommended_action = COMPOSITION_RECOMMENDATION_KEEP_EXCEPTION
    else:
        composition_class = COMPOSITION_CLASS_SINGLE_NEEDS_REFRAME
        recommended_action = (
            review.recommendation or COMPOSITION_RECOMMENDATION_REFRAME
        )

    return {
        "name": source.name,
        "technique_count": len(technique_ids),
        "technique_ids": technique_ids,
        "composition_class": composition_class,
        "exception_review_path": review.review_path,
        "recommended_action": recommended_action,
    }


def build_skill_composition_audit_payload(
    repo_root: Path,
    skill_names: Sequence[str],
) -> dict[str, Any]:
    skills = [
        composition_entry_for_source(repo_root, source)
        for source in skill_source_model.load_skill_sources(repo_root, skill_names)
    ]
    skills.sort(key=lambda entry: entry["name"])
    return {
        "skill_composition_version": SKILL_COMPOSITION_VERSION,
        "source_of_truth": SKILL_COMPOSITION_SOURCE_OF_TRUTH,
        "summary": {
            "total_skill_count": len(skills),
            "multi_technique_skill_count": sum(
                1
                for entry in skills
                if entry["composition_class"] == COMPOSITION_CLASS_MULTI_TECHNIQUE
            ),
            "single_technique_skill_count": sum(
                1 for entry in skills if entry["technique_count"] == 1
            ),
            "approved_exception_count": sum(
                1
                for entry in skills
                if entry["composition_class"] == COMPOSITION_CLASS_SINGLE_EXCEPTION
            ),
            "needs_reframe_count": sum(
                1
                for entry in skills
                if entry["composition_class"] == COMPOSITION_CLASS_SINGLE_NEEDS_REFRAME
            ),
        },
        "skills": skills,
    }


def render_skill_composition_audit_markdown(payload: Mapping[str, Any]) -> str:
    skill_entries = payload.get("skills", [])
    if not isinstance(skill_entries, list):
        raise ValueError("skill composition audit field 'skills' must be a list")

    summary = payload.get("summary", {})
    if not isinstance(summary, Mapping):
        raise ValueError("skill composition audit field 'summary' must be an object")

    lines = [
        "# Skill composition audit",
        "",
        "This derived file audits whether skills are multi-technique packages or explicit single-technique exceptions.",
        "It is a boundary/readiness view, not a direct status surface.",
        "",
        "## Summary",
        "",
        f"- total skills: {summary.get('total_skill_count', 0)}",
        f"- multi-technique skills: {summary.get('multi_technique_skill_count', 0)}",
        f"- single-technique skills: {summary.get('single_technique_skill_count', 0)}",
        f"- approved exceptions: {summary.get('approved_exception_count', 0)}",
        f"- needs reframe: {summary.get('needs_reframe_count', 0)}",
        "",
        "| name | techniques | composition class | recommended action | exception review |",
        "|---|---:|---|---|---|",
    ]
    if not skill_entries:
        lines.append("| - | 0 | - | - | - |")
        lines.append("")
        return "\n".join(lines)

    for entry in skill_entries:
        if not isinstance(entry, Mapping):
            continue
        review_path = entry.get("exception_review_path")
        review_display = review_path if review_path else "-"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(entry.get("name", "-")),
                    str(entry.get("technique_count", 0)),
                    str(entry.get("composition_class", "-")),
                    str(entry.get("recommended_action", "-")),
                    str(review_display),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)
