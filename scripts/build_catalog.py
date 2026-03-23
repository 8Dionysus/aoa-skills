#!/usr/bin/env python3
"""Build deterministic derived skill catalogs and reader/runtime surfaces."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import skill_boundary_surface
import skill_bundle_surface
import skill_catalog_contract
import skill_composition_audit
import skill_evaluation_surface
import skill_governance_backlog_surface
import skill_governance_lane_contract
import skill_governance_surface
import skill_lineage_surface
import skill_overlay_contract
import skill_runtime_surface
import skill_section_contract
import skill_source_model


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR_NAME = "skills"
GENERATED_DIR_NAME = "generated"
FULL_CATALOG_PATH = Path(GENERATED_DIR_NAME) / "skill_catalog.json"
MIN_CATALOG_PATH = Path(GENERATED_DIR_NAME) / "skill_catalog.min.json"
CAPSULE_PATH = Path(GENERATED_DIR_NAME) / "skill_capsules.json"
SECTIONS_PATH = Path(GENERATED_DIR_NAME) / skill_section_contract.SECTIONS_NAME
PUBLIC_SURFACE_JSON_PATH = skill_governance_surface.PUBLIC_SURFACE_JSON_PATH
PUBLIC_SURFACE_MARKDOWN_PATH = skill_governance_surface.PUBLIC_SURFACE_MARKDOWN_PATH
WALKTHROUGHS_JSON_PATH = skill_runtime_surface.WALKTHROUGHS_JSON_PATH
WALKTHROUGHS_MARKDOWN_PATH = skill_runtime_surface.WALKTHROUGHS_MARKDOWN_PATH
EVALUATION_MATRIX_JSON_PATH = skill_evaluation_surface.EVALUATION_MATRIX_JSON_PATH
EVALUATION_MATRIX_MARKDOWN_PATH = skill_evaluation_surface.EVALUATION_MATRIX_MARKDOWN_PATH
LINEAGE_SURFACE_JSON_PATH = skill_lineage_surface.LINEAGE_SURFACE_JSON_PATH
LINEAGE_SURFACE_MARKDOWN_PATH = skill_lineage_surface.LINEAGE_SURFACE_MARKDOWN_PATH
BOUNDARY_MATRIX_JSON_PATH = skill_boundary_surface.BOUNDARY_MATRIX_JSON_PATH
BOUNDARY_MATRIX_MARKDOWN_PATH = skill_boundary_surface.BOUNDARY_MATRIX_MARKDOWN_PATH
GOVERNANCE_BACKLOG_JSON_PATH = (
    skill_governance_backlog_surface.GOVERNANCE_BACKLOG_JSON_PATH
)
GOVERNANCE_BACKLOG_MARKDOWN_PATH = (
    skill_governance_backlog_surface.GOVERNANCE_BACKLOG_MARKDOWN_PATH
)
SKILL_COMPOSITION_AUDIT_JSON_PATH = skill_composition_audit.SKILL_COMPOSITION_JSON_PATH
SKILL_COMPOSITION_AUDIT_MARKDOWN_PATH = (
    skill_composition_audit.SKILL_COMPOSITION_MARKDOWN_PATH
)
OVERLAY_READINESS_JSON_PATH = skill_overlay_contract.OVERLAY_READINESS_JSON_PATH
OVERLAY_READINESS_MARKDOWN_PATH = skill_overlay_contract.OVERLAY_READINESS_MARKDOWN_PATH
BUNDLE_INDEX_JSON_PATH = skill_bundle_surface.BUNDLE_INDEX_JSON_PATH
BUNDLE_INDEX_MARKDOWN_PATH = skill_bundle_surface.BUNDLE_INDEX_MARKDOWN_PATH
SKILL_GRAPH_JSON_PATH = skill_bundle_surface.SKILL_GRAPH_JSON_PATH
SKILL_GRAPH_MARKDOWN_PATH = skill_bundle_surface.SKILL_GRAPH_MARKDOWN_PATH

CATALOG_VERSION = 1
CAPSULE_VERSION = 1
SECTION_VERSION = skill_section_contract.SECTION_VERSION
PUBLIC_SURFACE_VERSION = skill_governance_surface.PUBLIC_SURFACE_VERSION
WALKTHROUGH_VERSION = skill_runtime_surface.WALKTHROUGH_VERSION
EVALUATION_MATRIX_VERSION = skill_evaluation_surface.EVALUATION_MATRIX_VERSION
LINEAGE_SURFACE_VERSION = skill_lineage_surface.LINEAGE_SURFACE_VERSION
BOUNDARY_MATRIX_VERSION = skill_boundary_surface.BOUNDARY_MATRIX_VERSION
GOVERNANCE_BACKLOG_VERSION = (
    skill_governance_backlog_surface.GOVERNANCE_BACKLOG_VERSION
)
SKILL_COMPOSITION_AUDIT_VERSION = skill_composition_audit.SKILL_COMPOSITION_VERSION
OVERLAY_READINESS_VERSION = skill_overlay_contract.OVERLAY_READINESS_VERSION
BUNDLE_INDEX_VERSION = skill_bundle_surface.BUNDLE_INDEX_VERSION
SKILL_GRAPH_VERSION = skill_bundle_surface.SKILL_GRAPH_VERSION

SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "technique_manifest": "skills/*/techniques.yaml",
}
CAPSULE_SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "frontmatter_fields": [
        "name",
        "scope",
        "status",
        "summary",
        "invocation_mode",
        "technique_dependencies",
    ],
    "sections": [
        "Intent",
        "Trigger boundary",
        "Inputs",
        "Outputs",
        "Procedure",
        "Risks and anti-patterns",
        "Verification",
    ],
}
CAPSULE_REQUIRED_SECTIONS = tuple(CAPSULE_SOURCE_OF_TRUTH["sections"])
PUBLIC_SURFACE_SOURCE_OF_TRUTH = skill_governance_surface.PUBLIC_SURFACE_SOURCE_OF_TRUTH
WALKTHROUGH_SOURCE_OF_TRUTH = skill_runtime_surface.WALKTHROUGH_SOURCE_OF_TRUTH
EVALUATION_MATRIX_SOURCE_OF_TRUTH = skill_evaluation_surface.EVALUATION_MATRIX_SOURCE_OF_TRUTH
LIST_ITEM_PATTERN = re.compile(r"^(?:[-*]|\d+\.)\s+(.*)$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\([^)]+\)")
INLINE_CODE_PATTERN = re.compile(r"`([^`]+)`")
EMPHASIS_PATTERN = re.compile(r"(\*\*|\*|__|_)")
MAX_SHORT_FIELD_LENGTH = 220
MAX_WORKFLOW_SHORT_LENGTH = 260


@dataclass(frozen=True)
class GeneratedSurfaceOutput:
    path: Path
    is_json: bool = False
    item_collection_key: str | None = None
    item_key: str = "name"
    aggregate_sensitive: bool = False


@dataclass(frozen=True)
class GeneratedSurfaceSpec:
    key: str
    outputs: tuple[GeneratedSurfaceOutput, ...]
    build_texts: Callable[[Path], dict[Path, str]]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build derived reader catalogs for aoa-skills."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check whether generated surfaces are present and current.",
    )
    return parser.parse_args(argv)


def discover_skill_names(repo_root: Path) -> list[str]:
    return skill_source_model.discover_skill_names(repo_root)


def parse_skill_document(path: Path) -> tuple[dict[str, Any], str]:
    return skill_source_model.parse_skill_document(path)


def parse_skill_sections(body: str) -> dict[str, str]:
    return skill_source_model.parse_skill_sections(body)


def load_yaml(path: Path) -> Any:
    return skill_source_model.load_yaml(path)


def relative_path(path: Path, repo_root: Path) -> str:
    return skill_source_model.relative_location(path, repo_root)


def normalize_inline_markdown(text: str) -> str:
    normalized = MARKDOWN_LINK_PATTERN.sub(r"\1", text)
    normalized = INLINE_CODE_PATTERN.sub(r"\1", normalized)
    normalized = EMPHASIS_PATTERN.sub("", normalized)
    normalized = normalized.replace("\\", "")
    return " ".join(normalized.split())


def normalize_phrase(text: str) -> str:
    return normalize_inline_markdown(text).strip(" \t\r\n.;:")


def limit_text(text: str, limit: int) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) <= limit:
        return collapsed
    trimmed = collapsed[: limit - 3].rstrip(" ,;:-")
    if " " in trimmed:
        trimmed = trimmed.rsplit(" ", 1)[0]
    return f"{trimmed}..."


def ensure_sentence(text: str, limit: int) -> str:
    stripped = text.strip()
    if not stripped:
        return stripped
    if stripped[-1] not in ".!?":
        stripped += "."
    return limit_text(stripped, limit)


def extract_markdown_items(section_text: str) -> list[str]:
    items: list[str] = []
    current_item: str | None = None

    for raw_line in section_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            continue

        match = LIST_ITEM_PATTERN.match(stripped)
        if match:
            if current_item is not None:
                items.append(current_item)
            current_item = normalize_phrase(match.group(1))
            continue

        if current_item is not None and raw_line[:1].isspace():
            continuation = normalize_phrase(stripped)
            if continuation:
                current_item = f"{current_item} {continuation}".strip()
            continue

        if current_item is not None:
            items.append(current_item)
            current_item = None

        items.append(normalize_phrase(stripped))

    if current_item is not None:
        items.append(current_item)

    return [item for item in items if item]


def extract_first_sentence(section_text: str) -> str:
    normalized = normalize_inline_markdown(section_text.strip())
    if not normalized:
        return ""

    for delimiter in (". ", "! ", "? "):
        if delimiter in normalized:
            return normalized.split(delimiter, 1)[0].strip(" .!?")
    return normalized.strip(" .!?")


def build_compact_list_summary(
    prefix: str,
    section_text: str,
    *,
    limit: int = MAX_SHORT_FIELD_LENGTH,
    max_items: int = 4,
) -> str:
    items = extract_markdown_items(section_text)
    if items:
        text = f"{prefix}: {'; '.join(items[:max_items])}"
    else:
        sentence = extract_first_sentence(section_text)
        text = f"{prefix}: {sentence}" if sentence else prefix
    return ensure_sentence(text, limit)


def build_trigger_boundary_summary(section_text: str) -> str:
    use_items, avoid_items = skill_runtime_surface.extract_trigger_boundary_items(
        section_text
    )
    parts: list[str] = []
    if use_items:
        parts.append(f"Use when {'; '.join(use_items[:2])}")
    if avoid_items:
        parts.append(f"Avoid when {'; '.join(avoid_items[:2])}")
    if not parts:
        fallback = extract_first_sentence(section_text)
        parts.append(f"Use when {fallback}" if fallback else "Use when bounded context is clear")
    return ensure_sentence("; ".join(parts), MAX_SHORT_FIELD_LENGTH)


def build_intent_clause(intent_text: str) -> str:
    clause = extract_first_sentence(intent_text)
    if not clause:
        return ""

    lowered = clause.lower()
    prefixes = (
        "use this skill to ",
        "use this skill when ",
        "use ",
        "this skill helps ",
        "this skill is for ",
    )
    for prefix in prefixes:
        if lowered.startswith(prefix):
            clause = clause[len(prefix) :]
            break

    clause = normalize_phrase(clause)
    clause = re.sub(r"\bso the result\b", "to keep results", clause, flags=re.IGNORECASE)
    clause = re.sub(r"\bso that\b", "to", clause, flags=re.IGNORECASE)
    clause = re.sub(r"\bso\b", "to", clause, flags=re.IGNORECASE)
    return clause


def build_workflow_summary(intent_text: str, procedure_text: str) -> str:
    parts: list[str] = []
    intent_clause = build_intent_clause(intent_text)
    if intent_clause:
        parts.append(f"Purpose: {intent_clause}")

    steps = extract_markdown_items(procedure_text)
    if steps:
        parts.append(f"Flow: {' -> '.join(steps[:4])}")
    else:
        sentence = extract_first_sentence(procedure_text)
        if sentence:
            parts.append(f"Flow: {sentence}")

    if not parts:
        raise ValueError("workflow summary requires intent or procedure content")
    return ensure_sentence(". ".join(parts), MAX_WORKFLOW_SHORT_LENGTH)


def require_capsule_sections(source: skill_source_model.SkillSource) -> dict[str, str]:
    for section_name in CAPSULE_REQUIRED_SECTIONS:
        if section_name not in source.sections:
            raise ValueError(
                f"{source.skill_md_path} capsule source section '{section_name}' is missing"
            )
        if not source.sections[section_name].strip():
            raise ValueError(
                f"{source.skill_md_path} capsule source section '{section_name}' must not be empty"
            )
    return source.sections


def build_skill_entry_from_source(
    source: skill_source_model.SkillSource,
    repo_root: Path,
) -> dict[str, Any]:
    entry, issues = skill_catalog_contract.build_skill_entry_from_sources(
        repo_root,
        source.name,
        source.metadata,
        source.manifest,
        source.skill_md_path,
        source.techniques_path,
    )
    if issues:
        raise ValueError(skill_catalog_contract.format_issues(issues))
    if entry is None:
        raise ValueError(f"failed to build routing entry for {source.name}")
    return entry


def build_skill_capsule_entry(
    source: skill_source_model.SkillSource | Path,
    repo_root: Path | str,
) -> dict[str, Any]:
    if isinstance(source, skill_source_model.SkillSource):
        resolved_source = source
        resolved_repo_root = Path(repo_root)
    else:
        resolved_repo_root = Path(source)
        resolved_source = skill_source_model.load_skill_source(
            resolved_repo_root,
            str(repo_root),
        )
    source = resolved_source
    repo_root = resolved_repo_root
    sections = require_capsule_sections(source)
    technique_dependencies = source.metadata.get("technique_dependencies")
    if not isinstance(technique_dependencies, list) or not all(
        isinstance(item, str) for item in technique_dependencies
    ):
        raise ValueError(
            f"{source.skill_md_path} frontmatter 'technique_dependencies' must be a list of strings"
        )

    return {
        "name": source.metadata.get("name"),
        "scope": source.metadata.get("scope"),
        "status": source.metadata.get("status"),
        "summary": source.metadata.get("summary"),
        "trigger_boundary_short": build_trigger_boundary_summary(
            sections["Trigger boundary"]
        ),
        "inputs_short": build_compact_list_summary("Needs", sections["Inputs"]),
        "outputs_short": build_compact_list_summary("Produces", sections["Outputs"]),
        "workflow_short": build_workflow_summary(
            sections["Intent"],
            sections["Procedure"],
        ),
        "main_anti_patterns_short": build_compact_list_summary(
            "Avoid",
            sections["Risks and anti-patterns"],
        ),
        "verification_short": build_compact_list_summary(
            "Checks",
            sections["Verification"],
        ),
        "invocation_mode": source.metadata.get("invocation_mode"),
        "technique_dependencies": list(technique_dependencies),
        "skill_path": relative_path(source.skill_md_path, repo_root),
    }


def render_json(payload: dict[str, Any], *, indent: int | None) -> str:
    kwargs: dict[str, Any] = {
        "ensure_ascii": True,
        "sort_keys": True,
    }
    if indent is None:
        kwargs["separators"] = (",", ":")
    else:
        kwargs["indent"] = indent
    return json.dumps(payload, **kwargs) + "\n"


def build_full_catalog(repo_root: Path) -> dict[str, Any]:
    skills = [
        build_skill_entry_from_source(source, repo_root)
        for source in skill_source_model.load_skill_sources(repo_root)
    ]
    return {
        "catalog_version": CATALOG_VERSION,
        "source_of_truth": SOURCE_OF_TRUTH,
        "skills": skills,
    }


def project_min_catalog(full_catalog: dict[str, Any]) -> dict[str, Any]:
    min_skills: list[dict[str, Any]] = []
    for skill in full_catalog["skills"]:
        min_skills.append(
            {
                "name": skill["name"],
                "scope": skill["scope"],
                "status": skill["status"],
                "summary": skill["summary"],
                "invocation_mode": skill["invocation_mode"],
                "technique_dependencies": skill["technique_dependencies"],
                "skill_path": skill["skill_path"],
            }
        )
    return {
        "catalog_version": full_catalog["catalog_version"],
        "source_of_truth": full_catalog["source_of_truth"],
        "skills": min_skills,
    }


def build_catalog_texts(repo_root: Path) -> tuple[str, str]:
    full_catalog = build_full_catalog(repo_root)
    min_catalog = project_min_catalog(full_catalog)
    return render_json(full_catalog, indent=2), render_json(min_catalog, indent=None)


def build_skill_entry(repo_root: Path, skill_name: str) -> dict[str, Any]:
    for entry in build_full_catalog(repo_root)["skills"]:
        if entry.get("name") == skill_name:
            return entry
    raise KeyError(skill_name)


def build_min_skill_entry(repo_root: Path, skill_name: str) -> dict[str, Any]:
    return project_min_catalog({"catalog_version": CATALOG_VERSION, "source_of_truth": SOURCE_OF_TRUTH, "skills": [build_skill_entry(repo_root, skill_name)]})["skills"][0]


def build_capsules_payload(repo_root: Path) -> dict[str, Any]:
    return {
        "capsule_version": CAPSULE_VERSION,
        "source_of_truth": CAPSULE_SOURCE_OF_TRUTH,
        "skills": [
            build_skill_capsule_entry(source, repo_root)
            for source in skill_source_model.load_skill_sources(repo_root)
        ],
    }


def build_capsule_text(repo_root: Path) -> str:
    return render_json(build_capsules_payload(repo_root), indent=2)


def build_sections_payload(repo_root: Path) -> dict[str, Any]:
    skills: list[dict[str, Any]] = []
    issues: list[skill_section_contract.ContractIssue] = []
    for source in skill_source_model.load_skill_sources(repo_root):
        entry, entry_issues = skill_section_contract.build_sections_entry(
            repo_root,
            source.metadata,
            source.skill_md_path,
            source.body,
        )
        issues.extend(entry_issues)
        if entry is not None:
            skills.append(entry)
    if issues:
        raise ValueError(skill_section_contract.format_issues(issues))
    return {
        "section_version": SECTION_VERSION,
        "source_of_truth": skill_section_contract.SECTION_SOURCE_OF_TRUTH,
        "skills": skills,
    }


def build_sections_text(repo_root: Path) -> str:
    return render_json(build_sections_payload(repo_root), indent=2)


def evaluation_coverage_by_skill(
    repo_root: Path,
) -> dict[str, skill_governance_surface.EvaluationCoverage]:
    fixtures = skill_source_model.load_optional_yaml(
        repo_root
        / skill_governance_surface.PUBLIC_SURFACE_SOURCE_OF_TRUTH["evaluation_fixtures"]
    )
    if not isinstance(fixtures, Mapping):
        return {}
    return skill_governance_surface.collect_evaluation_coverage(fixtures)


def governance_signals_by_skill(
    repo_root: Path,
) -> dict[str, skill_governance_lane_contract.GovernanceSkillSignals]:
    lanes = skill_governance_lane_contract.load_governance_lanes(repo_root)
    return skill_governance_lane_contract.governance_skill_signals(lanes)


def build_public_surface_payload(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> dict[str, Any]:
    coverage_by_skill = evaluation_coverage_by_skill(repo_root)
    signals_by_skill = governance_signals_by_skill(repo_root)
    sources = skill_source_model.load_skill_sources(repo_root, skill_names)
    skills: list[dict[str, Any]] = []
    for source in sources:
        techniques = skill_catalog_contract.normalize_technique_refs(source.manifest)
        skills.append(
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
                skill_path=relative_path(source.skill_md_path, repo_root),
                governance_signals=skill_governance_lane_contract.governance_signals_for_skill(
                    signals_by_skill,
                    source.name,
                ),
            )
        )
    return {
        "public_surface_version": PUBLIC_SURFACE_VERSION,
        "source_of_truth": PUBLIC_SURFACE_SOURCE_OF_TRUTH,
        "cohorts": skill_governance_surface.derive_public_surface_cohorts(skills),
        "skills": skills,
    }


def build_public_surface_texts(repo_root: Path) -> tuple[str, str]:
    payload = build_public_surface_payload(repo_root)
    return (
        render_json(payload, indent=2),
        skill_governance_surface.render_public_surface_markdown(payload) + "\n",
    )


def build_walkthrough_payload(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> dict[str, Any]:
    selected_skill_names = (
        list(skill_names) if skill_names is not None else discover_skill_names(repo_root)
    )
    return skill_runtime_surface.build_walkthrough_payload(repo_root, selected_skill_names)


def build_walkthrough_texts(repo_root: Path) -> tuple[str, str]:
    payload = build_walkthrough_payload(repo_root)
    return (
        render_json(payload, indent=2),
        skill_runtime_surface.render_walkthrough_markdown(payload) + "\n",
    )


def build_evaluation_matrix_payload(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> dict[str, Any]:
    selected_skill_names = (
        list(skill_names) if skill_names is not None else discover_skill_names(repo_root)
    )
    return skill_evaluation_surface.build_evaluation_matrix_payload(
        repo_root,
        selected_skill_names,
    )


def build_evaluation_matrix_texts(repo_root: Path) -> tuple[str, str]:
    payload = build_evaluation_matrix_payload(repo_root)
    return (
        render_json(payload, indent=2),
        skill_evaluation_surface.render_evaluation_matrix_markdown(payload) + "\n",
    )


def build_lineage_surface_payload(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> dict[str, Any]:
    selected_skill_names = (
        list(skill_names) if skill_names is not None else discover_skill_names(repo_root)
    )
    return skill_lineage_surface.build_lineage_surface_payload(
        repo_root,
        selected_skill_names,
    )


def build_lineage_surface_texts(repo_root: Path) -> tuple[str, str]:
    payload = build_lineage_surface_payload(repo_root)
    return (
        render_json(payload, indent=2),
        skill_lineage_surface.render_lineage_surface_markdown(payload) + "\n",
    )


def build_boundary_matrix_payload(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> dict[str, Any]:
    selected_skill_names = (
        list(skill_names) if skill_names is not None else discover_skill_names(repo_root)
    )
    return skill_boundary_surface.build_boundary_matrix_payload(
        repo_root,
        selected_skill_names,
    )


def build_boundary_matrix_texts(repo_root: Path) -> tuple[str, str]:
    payload = build_boundary_matrix_payload(repo_root)
    return (
        render_json(payload, indent=2),
        skill_boundary_surface.render_boundary_matrix_markdown(payload) + "\n",
    )


def build_governance_backlog_payload(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> dict[str, Any]:
    selected_skill_names = (
        list(skill_names) if skill_names is not None else discover_skill_names(repo_root)
    )
    return skill_governance_backlog_surface.build_governance_backlog_payload(
        repo_root,
        selected_skill_names,
    )


def build_governance_backlog_texts(repo_root: Path) -> tuple[str, str]:
    payload = build_governance_backlog_payload(repo_root)
    return (
        render_json(payload, indent=2),
        skill_governance_backlog_surface.render_governance_backlog_markdown(payload)
        + "\n",
    )


def build_skill_composition_audit_payload(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> dict[str, Any]:
    selected_skill_names = (
        list(skill_names) if skill_names is not None else discover_skill_names(repo_root)
    )
    return skill_composition_audit.build_skill_composition_audit_payload(
        repo_root,
        selected_skill_names,
    )


def build_skill_composition_audit_texts(repo_root: Path) -> tuple[str, str]:
    payload = build_skill_composition_audit_payload(repo_root)
    return (
        render_json(payload, indent=2),
        skill_composition_audit.render_skill_composition_audit_markdown(payload) + "\n",
    )


def generated_surface_versions() -> dict[str, int]:
    return {
        "catalog": CATALOG_VERSION,
        "capsule": CAPSULE_VERSION,
        "sections": SECTION_VERSION,
        "walkthrough": WALKTHROUGH_VERSION,
        "public_surface": PUBLIC_SURFACE_VERSION,
        "evaluation_matrix": EVALUATION_MATRIX_VERSION,
        "lineage_surface": LINEAGE_SURFACE_VERSION,
        "boundary_matrix": BOUNDARY_MATRIX_VERSION,
        "governance_backlog": GOVERNANCE_BACKLOG_VERSION,
        "skill_composition_audit": SKILL_COMPOSITION_AUDIT_VERSION,
        "overlay_readiness": OVERLAY_READINESS_VERSION,
        "bundle_index": BUNDLE_INDEX_VERSION,
        "skill_graph": SKILL_GRAPH_VERSION,
    }


def build_bundle_index_payload(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> dict[str, Any]:
    selected_skill_names = (
        list(skill_names) if skill_names is not None else discover_skill_names(repo_root)
    )
    return skill_bundle_surface.build_bundle_index_payload(
        repo_root,
        selected_skill_names,
        generated_surface_versions=generated_surface_versions(),
    )


def build_bundle_index_texts(repo_root: Path) -> tuple[str, str]:
    payload = build_bundle_index_payload(repo_root)
    return (
        render_json(payload, indent=2),
        skill_bundle_surface.render_bundle_index_markdown(payload) + "\n",
    )


def build_skill_graph_payload(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> dict[str, Any]:
    selected_skill_names = (
        list(skill_names) if skill_names is not None else discover_skill_names(repo_root)
    )
    return skill_bundle_surface.build_skill_graph_payload(
        repo_root,
        selected_skill_names,
        generated_surface_versions=generated_surface_versions(),
    )


def build_skill_graph_texts(repo_root: Path) -> tuple[str, str]:
    payload = build_skill_graph_payload(repo_root)
    return (
        render_json(payload, indent=2),
        skill_bundle_surface.render_skill_graph_markdown(payload) + "\n",
    )


def build_overlay_readiness_payload(repo_root: Path) -> dict[str, Any]:
    return skill_overlay_contract.build_overlay_readiness_payload(repo_root)


def build_overlay_readiness_texts(repo_root: Path) -> tuple[str, str]:
    payload = build_overlay_readiness_payload(repo_root)
    return (
        render_json(payload, indent=2),
        skill_overlay_contract.render_overlay_readiness_markdown(payload) + "\n",
    )


def build_catalog_surface_texts(repo_root: Path) -> dict[Path, str]:
    full_text, min_text = build_catalog_texts(repo_root)
    return {
        FULL_CATALOG_PATH: full_text,
        MIN_CATALOG_PATH: min_text,
    }


def build_capsule_surface_texts(repo_root: Path) -> dict[Path, str]:
    return {CAPSULE_PATH: build_capsule_text(repo_root)}


def build_sections_surface_texts(repo_root: Path) -> dict[Path, str]:
    return {SECTIONS_PATH: build_sections_text(repo_root)}


def build_walkthrough_surface_texts(repo_root: Path) -> dict[Path, str]:
    json_text, markdown_text = build_walkthrough_texts(repo_root)
    return {
        WALKTHROUGHS_JSON_PATH: json_text,
        WALKTHROUGHS_MARKDOWN_PATH: markdown_text,
    }


def build_public_surface_outputs(repo_root: Path) -> dict[Path, str]:
    json_text, markdown_text = build_public_surface_texts(repo_root)
    return {
        PUBLIC_SURFACE_JSON_PATH: json_text,
        PUBLIC_SURFACE_MARKDOWN_PATH: markdown_text,
    }


def build_evaluation_matrix_outputs(repo_root: Path) -> dict[Path, str]:
    json_text, markdown_text = build_evaluation_matrix_texts(repo_root)
    return {
        EVALUATION_MATRIX_JSON_PATH: json_text,
        EVALUATION_MATRIX_MARKDOWN_PATH: markdown_text,
    }


def build_lineage_surface_outputs(repo_root: Path) -> dict[Path, str]:
    json_text, markdown_text = build_lineage_surface_texts(repo_root)
    return {
        LINEAGE_SURFACE_JSON_PATH: json_text,
        LINEAGE_SURFACE_MARKDOWN_PATH: markdown_text,
    }


def build_boundary_matrix_outputs(repo_root: Path) -> dict[Path, str]:
    json_text, markdown_text = build_boundary_matrix_texts(repo_root)
    return {
        BOUNDARY_MATRIX_JSON_PATH: json_text,
        BOUNDARY_MATRIX_MARKDOWN_PATH: markdown_text,
    }


def build_governance_backlog_outputs(repo_root: Path) -> dict[Path, str]:
    json_text, markdown_text = build_governance_backlog_texts(repo_root)
    return {
        GOVERNANCE_BACKLOG_JSON_PATH: json_text,
        GOVERNANCE_BACKLOG_MARKDOWN_PATH: markdown_text,
    }


def build_skill_composition_audit_outputs(repo_root: Path) -> dict[Path, str]:
    json_text, markdown_text = build_skill_composition_audit_texts(repo_root)
    return {
        SKILL_COMPOSITION_AUDIT_JSON_PATH: json_text,
        SKILL_COMPOSITION_AUDIT_MARKDOWN_PATH: markdown_text,
    }


def build_overlay_readiness_outputs(repo_root: Path) -> dict[Path, str]:
    json_text, markdown_text = build_overlay_readiness_texts(repo_root)
    return {
        OVERLAY_READINESS_JSON_PATH: json_text,
        OVERLAY_READINESS_MARKDOWN_PATH: markdown_text,
    }


def build_bundle_index_outputs(repo_root: Path) -> dict[Path, str]:
    json_text, markdown_text = build_bundle_index_texts(repo_root)
    return {
        BUNDLE_INDEX_JSON_PATH: json_text,
        BUNDLE_INDEX_MARKDOWN_PATH: markdown_text,
    }


def build_skill_graph_outputs(repo_root: Path) -> dict[Path, str]:
    json_text, markdown_text = build_skill_graph_texts(repo_root)
    return {
        SKILL_GRAPH_JSON_PATH: json_text,
        SKILL_GRAPH_MARKDOWN_PATH: markdown_text,
    }


def generated_surface_specs() -> tuple[GeneratedSurfaceSpec, ...]:
    return (
        GeneratedSurfaceSpec(
            key="catalogs",
            outputs=(
                GeneratedSurfaceOutput(
                    path=FULL_CATALOG_PATH,
                    is_json=True,
                    item_collection_key="skills",
                ),
                GeneratedSurfaceOutput(
                    path=MIN_CATALOG_PATH,
                    is_json=True,
                    item_collection_key="skills",
                ),
            ),
            build_texts=build_catalog_surface_texts,
        ),
        GeneratedSurfaceSpec(
            key="capsules",
            outputs=(
                GeneratedSurfaceOutput(
                    path=CAPSULE_PATH,
                    is_json=True,
                    item_collection_key="skills",
                ),
            ),
            build_texts=build_capsule_surface_texts,
        ),
        GeneratedSurfaceSpec(
            key="sections",
            outputs=(
                GeneratedSurfaceOutput(
                    path=SECTIONS_PATH,
                    is_json=True,
                    item_collection_key="skills",
                ),
            ),
            build_texts=build_sections_surface_texts,
        ),
        GeneratedSurfaceSpec(
            key="walkthroughs",
            outputs=(
                GeneratedSurfaceOutput(
                    path=WALKTHROUGHS_JSON_PATH,
                    is_json=True,
                    item_collection_key="skills",
                ),
                GeneratedSurfaceOutput(path=WALKTHROUGHS_MARKDOWN_PATH),
            ),
            build_texts=build_walkthrough_surface_texts,
        ),
        GeneratedSurfaceSpec(
            key="public_surface",
            outputs=(
                GeneratedSurfaceOutput(
                    path=PUBLIC_SURFACE_JSON_PATH,
                    is_json=True,
                    item_collection_key="skills",
                    aggregate_sensitive=True,
                ),
                GeneratedSurfaceOutput(
                    path=PUBLIC_SURFACE_MARKDOWN_PATH,
                    aggregate_sensitive=True,
                ),
            ),
            build_texts=build_public_surface_outputs,
        ),
        GeneratedSurfaceSpec(
            key="evaluation_matrix",
            outputs=(
                GeneratedSurfaceOutput(
                    path=EVALUATION_MATRIX_JSON_PATH,
                    is_json=True,
                    item_collection_key="skills",
                ),
                GeneratedSurfaceOutput(path=EVALUATION_MATRIX_MARKDOWN_PATH),
            ),
            build_texts=build_evaluation_matrix_outputs,
        ),
        GeneratedSurfaceSpec(
            key="lineage_surface",
            outputs=(
                GeneratedSurfaceOutput(
                    path=LINEAGE_SURFACE_JSON_PATH,
                    is_json=True,
                    item_collection_key="skills",
                    aggregate_sensitive=True,
                ),
                GeneratedSurfaceOutput(
                    path=LINEAGE_SURFACE_MARKDOWN_PATH,
                    aggregate_sensitive=True,
                ),
            ),
            build_texts=build_lineage_surface_outputs,
        ),
        GeneratedSurfaceSpec(
            key="boundary_matrix",
            outputs=(
                GeneratedSurfaceOutput(
                    path=BOUNDARY_MATRIX_JSON_PATH,
                    is_json=True,
                    item_collection_key="skills",
                    aggregate_sensitive=True,
                ),
                GeneratedSurfaceOutput(
                    path=BOUNDARY_MATRIX_MARKDOWN_PATH,
                    aggregate_sensitive=True,
                ),
            ),
            build_texts=build_boundary_matrix_outputs,
        ),
        GeneratedSurfaceSpec(
            key="governance_backlog",
            outputs=(
                GeneratedSurfaceOutput(
                    path=GOVERNANCE_BACKLOG_JSON_PATH,
                    is_json=True,
                    item_collection_key="skills",
                    aggregate_sensitive=True,
                ),
                GeneratedSurfaceOutput(
                    path=GOVERNANCE_BACKLOG_MARKDOWN_PATH,
                    aggregate_sensitive=True,
                ),
            ),
            build_texts=build_governance_backlog_outputs,
        ),
        GeneratedSurfaceSpec(
            key="skill_composition_audit",
            outputs=(
                GeneratedSurfaceOutput(
                    path=SKILL_COMPOSITION_AUDIT_JSON_PATH,
                    is_json=True,
                    item_collection_key="skills",
                ),
                GeneratedSurfaceOutput(path=SKILL_COMPOSITION_AUDIT_MARKDOWN_PATH),
            ),
            build_texts=build_skill_composition_audit_outputs,
        ),
        GeneratedSurfaceSpec(
            key="overlay_readiness",
            outputs=(
                GeneratedSurfaceOutput(
                    path=OVERLAY_READINESS_JSON_PATH,
                    is_json=True,
                    item_collection_key="skills",
                ),
                GeneratedSurfaceOutput(path=OVERLAY_READINESS_MARKDOWN_PATH),
            ),
            build_texts=build_overlay_readiness_outputs,
        ),
        GeneratedSurfaceSpec(
            key="bundle_index",
            outputs=(
                GeneratedSurfaceOutput(
                    path=BUNDLE_INDEX_JSON_PATH,
                    is_json=True,
                    item_collection_key="skills",
                    aggregate_sensitive=True,
                ),
                GeneratedSurfaceOutput(
                    path=BUNDLE_INDEX_MARKDOWN_PATH,
                    aggregate_sensitive=True,
                ),
            ),
            build_texts=build_bundle_index_outputs,
        ),
        GeneratedSurfaceSpec(
            key="skill_graph",
            outputs=(
                GeneratedSurfaceOutput(
                    path=SKILL_GRAPH_JSON_PATH,
                    is_json=True,
                    aggregate_sensitive=True,
                ),
                GeneratedSurfaceOutput(
                    path=SKILL_GRAPH_MARKDOWN_PATH,
                    aggregate_sensitive=True,
                ),
            ),
            build_texts=build_skill_graph_outputs,
        ),
    )


def generated_surface_spec(key: str) -> GeneratedSurfaceSpec:
    for spec in generated_surface_specs():
        if spec.key == key:
            return spec
    raise KeyError(key)


def build_surface_text_map(repo_root: Path, spec: GeneratedSurfaceSpec) -> dict[Path, str]:
    return spec.build_texts(repo_root)


def write_generated_surface(
    repo_root: Path,
    spec: GeneratedSurfaceSpec,
) -> tuple[Path, ...]:
    generated_dir = repo_root / GENERATED_DIR_NAME
    generated_dir.mkdir(exist_ok=True)
    texts = build_surface_text_map(repo_root, spec)
    written_paths: list[Path] = []
    for output in spec.outputs:
        target_path = repo_root / output.path
        target_path.write_text(texts[output.path], encoding="utf-8", newline="\n")
        written_paths.append(target_path)
    return tuple(written_paths)


def check_generated_surface(repo_root: Path, spec: GeneratedSurfaceSpec) -> list[str]:
    problems: list[str] = []
    try:
        expected_texts = build_surface_text_map(repo_root, spec)
    except ValueError as exc:
        return [f"{spec.key} source validation failed:\n{exc}"]

    for output in spec.outputs:
        path = repo_root / output.path
        if not path.is_file():
            problems.append(f"missing {relative_path(path, repo_root)}")
            continue
        if path.read_text(encoding="utf-8") != expected_texts[output.path]:
            problems.append(f"stale {relative_path(path, repo_root)}")
    return problems


def write_catalogs(repo_root: Path) -> tuple[Path, Path]:
    written_paths = write_generated_surface(repo_root, generated_surface_spec("catalogs"))
    return written_paths[0], written_paths[1]


def write_capsules(repo_root: Path) -> Path:
    return write_generated_surface(repo_root, generated_surface_spec("capsules"))[0]


def write_sections(repo_root: Path) -> Path:
    return write_generated_surface(repo_root, generated_surface_spec("sections"))[0]


def write_walkthroughs(repo_root: Path) -> tuple[Path, Path]:
    written_paths = write_generated_surface(
        repo_root,
        generated_surface_spec("walkthroughs"),
    )
    return written_paths[0], written_paths[1]


def write_public_surface(repo_root: Path) -> tuple[Path, Path]:
    written_paths = write_generated_surface(
        repo_root,
        generated_surface_spec("public_surface"),
    )
    return written_paths[0], written_paths[1]


def write_evaluation_matrix(repo_root: Path) -> tuple[Path, Path]:
    written_paths = write_generated_surface(
        repo_root,
        generated_surface_spec("evaluation_matrix"),
    )
    return written_paths[0], written_paths[1]


def write_lineage_surface(repo_root: Path) -> tuple[Path, Path]:
    written_paths = write_generated_surface(
        repo_root,
        generated_surface_spec("lineage_surface"),
    )
    return written_paths[0], written_paths[1]


def write_boundary_matrix(repo_root: Path) -> tuple[Path, Path]:
    written_paths = write_generated_surface(
        repo_root,
        generated_surface_spec("boundary_matrix"),
    )
    return written_paths[0], written_paths[1]


def write_governance_backlog(repo_root: Path) -> tuple[Path, Path]:
    written_paths = write_generated_surface(
        repo_root,
        generated_surface_spec("governance_backlog"),
    )
    return written_paths[0], written_paths[1]


def write_skill_composition_audit(repo_root: Path) -> tuple[Path, Path]:
    written_paths = write_generated_surface(
        repo_root,
        generated_surface_spec("skill_composition_audit"),
    )
    return written_paths[0], written_paths[1]


def write_overlay_readiness(repo_root: Path) -> tuple[Path, Path]:
    written_paths = write_generated_surface(
        repo_root,
        generated_surface_spec("overlay_readiness"),
    )
    return written_paths[0], written_paths[1]


def write_bundle_index(repo_root: Path) -> tuple[Path, Path]:
    written_paths = write_generated_surface(
        repo_root,
        generated_surface_spec("bundle_index"),
    )
    return written_paths[0], written_paths[1]


def write_skill_graph(repo_root: Path) -> tuple[Path, Path]:
    written_paths = write_generated_surface(
        repo_root,
        generated_surface_spec("skill_graph"),
    )
    return written_paths[0], written_paths[1]


def check_catalogs(repo_root: Path) -> list[str]:
    return check_generated_surface(repo_root, generated_surface_spec("catalogs"))


def check_capsules(repo_root: Path) -> list[str]:
    return check_generated_surface(repo_root, generated_surface_spec("capsules"))


def check_sections(repo_root: Path) -> list[str]:
    return check_generated_surface(repo_root, generated_surface_spec("sections"))


def check_walkthroughs(repo_root: Path) -> list[str]:
    return check_generated_surface(repo_root, generated_surface_spec("walkthroughs"))


def check_public_surface(repo_root: Path) -> list[str]:
    return check_generated_surface(repo_root, generated_surface_spec("public_surface"))


def check_evaluation_matrix(repo_root: Path) -> list[str]:
    return check_generated_surface(
        repo_root,
        generated_surface_spec("evaluation_matrix"),
    )


def check_lineage_surface(repo_root: Path) -> list[str]:
    return check_generated_surface(repo_root, generated_surface_spec("lineage_surface"))


def check_boundary_matrix(repo_root: Path) -> list[str]:
    return check_generated_surface(repo_root, generated_surface_spec("boundary_matrix"))


def check_governance_backlog(repo_root: Path) -> list[str]:
    return check_generated_surface(
        repo_root,
        generated_surface_spec("governance_backlog"),
    )


def check_skill_composition_audit(repo_root: Path) -> list[str]:
    return check_generated_surface(
        repo_root,
        generated_surface_spec("skill_composition_audit"),
    )


def check_overlay_readiness(repo_root: Path) -> list[str]:
    return check_generated_surface(repo_root, generated_surface_spec("overlay_readiness"))


def check_bundle_index(repo_root: Path) -> list[str]:
    return check_generated_surface(repo_root, generated_surface_spec("bundle_index"))


def check_skill_graph(repo_root: Path) -> list[str]:
    return check_generated_surface(repo_root, generated_surface_spec("skill_graph"))


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        if args.check:
            problems: list[str] = []
            for spec in generated_surface_specs():
                problems.extend(check_generated_surface(repo_root, spec))
            if problems:
                print("Generated surface check failed.")
                for problem in problems:
                    print(f"- {problem}")
                return 1
            print(
                f"Generated surface check passed for {len(discover_skill_names(repo_root))} skills."
            )
            return 0

        written_paths: list[Path] = []
        for spec in generated_surface_specs():
            written_paths.extend(write_generated_surface(repo_root, spec))
    except (FileNotFoundError, ValueError) as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive runtime guard
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2

    relative_paths = [relative_path(path, repo_root) for path in written_paths]
    print("Generated surface build wrote " + ", ".join(relative_paths) + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
