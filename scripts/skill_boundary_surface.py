from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

import skill_catalog_contract
import skill_evaluation_contract
import skill_governance_lane_contract
import skill_governance_surface
import skill_source_model


BOUNDARY_MATRIX_VERSION = 2
BOUNDARY_MATRIX_JSON_PATH = Path("generated") / "skill_boundary_matrix.json"
BOUNDARY_MATRIX_MARKDOWN_PATH = Path("generated") / "skill_boundary_matrix.md"
BOUNDARY_MATRIX_SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "technique_manifest": "skills/*/techniques.yaml",
    "evaluation_fixtures": "tests/fixtures/skill_evaluation_cases.yaml",
    "evaluation_snapshots": "tests/fixtures/skill_evaluation_snapshots/*/*.md",
    "governance_lanes": skill_governance_lane_contract.GOVERNANCE_LANES_PATH.as_posix(),
}
ADJACENCY_REQUIRED_BLOCKER = "missing_required_adjacency_coverage"


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def adjacency_cases(fixtures: Mapping[str, Any] | None) -> list[Mapping[str, Any]]:
    return skill_evaluation_contract.adjacency_cases(fixtures)


def governance_ready(
    source: skill_source_model.SkillSource,
    governance_signals: skill_governance_lane_contract.GovernanceSkillSignals,
    evaluation_coverage: skill_governance_surface.EvaluationCoverage,
) -> bool:
    techniques = skill_catalog_contract.normalize_technique_refs(source.manifest)
    blockers = skill_governance_surface.derive_canonical_candidate_blockers(
        status=source.metadata.get("status"),
        headings=set(source.sections),
        technique_dependencies=list(source.metadata.get("technique_dependencies", [])),
        techniques=techniques,
        evaluation_coverage=evaluation_coverage,
        invocation_mode=source.metadata.get("invocation_mode"),
        policy_exists=source.policy_exists,
        policy_allow_implicit_invocation=source.policy_allow_implicit_invocation,
    )
    return skill_governance_surface.derive_canonical_candidate_ready(
        scope=source.metadata.get("scope"),
        governance_signals=governance_signals,
        blockers=blockers,
    )


def case_blockers(repo_root: Path, case: Mapping[str, Any]) -> list[str]:
    return sorted(skill_evaluation_contract.snapshot_blockers_for_case(repo_root, case))


def build_case_entry(
    repo_root: Path,
    case: Mapping[str, Any],
    *,
    case_lane_ids: Sequence[str],
) -> dict[str, Any]:
    return {
        "skill": case.get("skill"),
        "adjacent_skill": case.get("adjacent_skill"),
        "case_id": case.get("case_id"),
        "expected": case.get("expected"),
        "prompt": case.get("prompt"),
        "snapshot_path": case.get("snapshot_path"),
        "governance_lane_ids": list(case_lane_ids),
        "blockers": case_blockers(repo_root, case),
    }


def build_skill_entry(
    source: skill_source_model.SkillSource,
    *,
    repo_root: Path,
    evaluation_coverage_by_skill: Mapping[str, skill_governance_surface.EvaluationCoverage],
    case_entries: Sequence[Mapping[str, Any]],
    governance_signals_by_skill: Mapping[
        str, skill_governance_lane_contract.GovernanceSkillSignals
    ],
) -> dict[str, Any]:
    evaluation_coverage = skill_governance_surface.coverage_for_skill(
        evaluation_coverage_by_skill,
        source.name,
    )
    governance_signals = skill_governance_lane_contract.governance_signals_for_skill(
        governance_signals_by_skill,
        source.name,
    )
    required_coverage = source.metadata.get("status") == "canonical" or governance_ready(
        source,
        governance_signals,
        evaluation_coverage,
    )
    skill_cases = [case for case in case_entries if case.get("skill") == source.name]
    use_count = sum(1 for case in skill_cases if case.get("expected") == "use")
    do_not_use_count = sum(
        1 for case in skill_cases if case.get("expected") == "do_not_use"
    )
    blockers = sorted(
        {
            blocker
            for case in skill_cases
            for blocker in case.get("blockers", [])
            if isinstance(blocker, str)
        }
    )
    adjacency_ready = len(skill_cases) >= 1 and not blockers
    if required_coverage and not adjacency_ready:
        blockers = sorted({*blockers, ADJACENCY_REQUIRED_BLOCKER})

    adjacent_skill_names = sorted(
        {
            str(case["adjacent_skill"])
            for case in skill_cases
            if isinstance(case.get("adjacent_skill"), str)
        }
    )

    return {
        "name": source.name,
        "status": source.metadata.get("status"),
        "scope": source.metadata.get("scope"),
        "skill_path": relative_location(source.skill_md_path, repo_root),
        "required_adjacency_coverage": required_coverage,
        "adjacency_use_count": use_count,
        "adjacency_do_not_use_count": do_not_use_count,
        "adjacent_skill_names": adjacent_skill_names,
        "adjacency_ready": adjacency_ready,
        "adjacency_blockers": blockers,
        "governance_lane_ids": list(
            governance_signals.governance_lane_ids
        ),
    }


def build_boundary_matrix_payload(
    repo_root: Path,
    skill_names: Sequence[str],
) -> dict[str, Any]:
    fixtures = skill_evaluation_contract.load_evaluation_fixtures(repo_root) or {}
    lanes = skill_governance_lane_contract.load_governance_lanes(repo_root)
    case_lane_ids_by_case = skill_governance_lane_contract.governance_lane_ids_by_case(
        lanes
    )
    governance_signals_by_skill = skill_governance_lane_contract.governance_skill_signals(
        lanes
    )
    case_entries = [
        build_case_entry(
            repo_root,
            case,
            case_lane_ids=case_lane_ids_by_case.get(str(case.get("case_id")), ()),
        )
        for case in adjacency_cases(fixtures)
    ]
    evaluation_coverage_by_skill = skill_governance_surface.collect_evaluation_coverage(
        fixtures
    )
    sources = skill_source_model.load_skill_sources(repo_root, skill_names)
    skills = [
        build_skill_entry(
            source,
            repo_root=repo_root,
            evaluation_coverage_by_skill=evaluation_coverage_by_skill,
            case_entries=case_entries,
            governance_signals_by_skill=governance_signals_by_skill,
        )
        for source in sources
    ]
    return {
        "boundary_matrix_version": BOUNDARY_MATRIX_VERSION,
        "source_of_truth": BOUNDARY_MATRIX_SOURCE_OF_TRUTH,
        "skills": skills,
        "cases": case_entries,
    }


def render_boundary_matrix_markdown(payload: Mapping[str, Any]) -> str:
    skill_entries = payload.get("skills", [])
    case_entries = payload.get("cases", [])
    if not isinstance(skill_entries, list):
        raise ValueError("boundary matrix field 'skills' must be a list")
    if not isinstance(case_entries, list):
        raise ValueError("boundary matrix field 'cases' must be a list")

    required_skills = [
        entry
        for entry in skill_entries
        if isinstance(entry, Mapping) and entry.get("required_adjacency_coverage")
    ]
    required_gap_skills = [
        entry
        for entry in required_skills
        if isinstance(entry, Mapping) and not entry.get("adjacency_ready")
    ]

    lines = [
        "# Skill boundary matrix",
        "",
        "This derived file summarizes adjacency-focused boundary evidence for neighboring `aoa-skills`.",
        "It is built from committed adjacency cases and snapshot-backed evidence only.",
        "",
        "## Summary",
        "",
        f"- total skills: {len(skill_entries)}",
        f"- adjacency cases: {len(case_entries)}",
        f"- skills with required adjacency coverage: {len(required_skills)}",
        f"- required adjacency gaps: {len(required_gap_skills)}",
        "",
        "| name | status | scope | required coverage | use cases | do_not_use cases | adjacent skills | lane ids | ready | blockers |",
        "|---|---|---|---|---:|---:|---|---|---|---|",
    ]
    if not skill_entries:
        lines.append("| - | - | - | - | - | - | - | - | - | - |")
    else:
        for entry in skill_entries:
            if not isinstance(entry, Mapping):
                continue
            blockers = entry.get("adjacency_blockers", [])
            blocker_text = ", ".join(blockers) if blockers else "-"
            adjacent_skill_text = ", ".join(entry.get("adjacent_skill_names", [])) or "-"
            governance_lane_text = ", ".join(entry.get("governance_lane_ids", [])) or "-"
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(entry["name"]),
                        str(entry["status"]),
                        str(entry["scope"]),
                        "true" if entry["required_adjacency_coverage"] else "false",
                        str(entry["adjacency_use_count"]),
                        str(entry["adjacency_do_not_use_count"]),
                        adjacent_skill_text,
                        governance_lane_text,
                        "true" if entry["adjacency_ready"] else "false",
                        blocker_text,
                    ]
                )
                + " |"
            )

    lines.extend(
        [
            "",
            "## Adjacency cases",
            "",
            "| skill | adjacent skill | case id | expected | lane ids | blockers |",
            "|---|---|---|---|---|---|",
        ]
    )
    if not case_entries:
        lines.append("| - | - | - | - | - | - |")
    else:
        for case in case_entries:
            if not isinstance(case, Mapping):
                continue
            blocker_text = ", ".join(case.get("blockers", [])) or "-"
            governance_lane_text = ", ".join(case.get("governance_lane_ids", [])) or "-"
            lines.append(
                f"| {case.get('skill')} | {case.get('adjacent_skill')} | {case.get('case_id')} | {case.get('expected')} | {governance_lane_text} | {blocker_text} |"
            )
    lines.append("")
    return "\n".join(lines)
