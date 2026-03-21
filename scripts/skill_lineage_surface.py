from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

import skill_catalog_contract
import skill_governance_surface
import skill_source_model


LINEAGE_SURFACE_VERSION = 1
LINEAGE_SURFACE_JSON_PATH = Path("generated") / "skill_lineage_surface.json"
LINEAGE_SURFACE_MARKDOWN_PATH = Path("generated") / "skill_lineage_surface.md"
LINEAGE_SURFACE_SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "technique_manifest": "skills/*/techniques.yaml",
}
PUBLISHED_LINEAGE_COHORT = "published_lineage"
PENDING_LINEAGE_COHORT = "pending_lineage"


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def lineage_blockers(
    technique_dependencies: Sequence[Any],
    techniques: Sequence[Mapping[str, Any]],
) -> list[str]:
    blockers: list[str] = []
    if skill_governance_surface.has_pending_technique_dependencies(technique_dependencies):
        blockers.append(skill_governance_surface.BLOCKER_PENDING_TECHNIQUE_DEPENDENCIES)
    if skill_governance_surface.has_pending_technique_entries(techniques):
        blockers.append(skill_governance_surface.BLOCKER_PENDING_TECHNIQUE_ENTRIES)
    if skill_governance_surface.has_tbd_technique_refs(techniques):
        blockers.append(skill_governance_surface.BLOCKER_TBD_TECHNIQUE_REFS)
    return blockers


def technique_counts(
    technique_dependencies: Sequence[Any],
    techniques: Sequence[Mapping[str, Any]],
) -> tuple[int, int, int]:
    published_count = 0
    pending_count = 0
    tbd_ref_count = 0

    if any(
        isinstance(dependency, str) and dependency.startswith("AOA-T-PENDING-")
        for dependency in technique_dependencies
    ):
        pending_count += sum(
            1
            for dependency in technique_dependencies
            if isinstance(dependency, str) and dependency.startswith("AOA-T-PENDING-")
        )

    for technique in techniques:
        technique_id = technique.get("id")
        path_value = technique.get("path")
        source_ref = technique.get("source_ref")
        if isinstance(technique_id, str) and technique_id.startswith("AOA-T-PENDING-"):
            pending_count += 1
        else:
            published_count += 1
        if path_value == "TBD" or source_ref == "TBD":
            tbd_ref_count += 1

    # The frontmatter dependency count and manifest count may overlap for pending IDs.
    pending_count = max(
        pending_count,
        sum(
            1
            for technique in techniques
            if isinstance(technique.get("id"), str)
            and technique["id"].startswith("AOA-T-PENDING-")
        ),
    )
    return published_count, pending_count, tbd_ref_count


def build_skill_lineage_entry(source: skill_source_model.SkillSource) -> dict[str, Any]:
    technique_dependencies = list(source.metadata.get("technique_dependencies", []))
    techniques = skill_catalog_contract.normalize_technique_refs(source.manifest)
    blockers = lineage_blockers(technique_dependencies, techniques)
    published_count, pending_count, tbd_ref_count = technique_counts(
        technique_dependencies,
        techniques,
    )

    return {
        "name": source.name,
        "scope": source.metadata.get("scope"),
        "status": source.metadata.get("status"),
        "skill_path": skill_source_model.relative_location(source.skill_md_path, source.skill_md_path.parents[2]),
        "lineage_state": skill_governance_surface.derive_lineage_state(
            technique_dependencies,
            techniques,
        ),
        "published_technique_count": published_count,
        "pending_technique_count": pending_count,
        "tbd_ref_count": tbd_ref_count,
        "manifest_canonical_path_ready": not blockers,
        "lineage_blockers": blockers,
    }


def derive_lineage_cohorts(skill_entries: Sequence[Mapping[str, Any]]) -> dict[str, list[str]]:
    published: list[str] = []
    pending: list[str] = []
    for entry in skill_entries:
        if entry.get("lineage_state") == "pending":
            pending.append(str(entry["name"]))
        else:
            published.append(str(entry["name"]))
    return {
        PUBLISHED_LINEAGE_COHORT: sorted(published),
        PENDING_LINEAGE_COHORT: sorted(pending),
    }


def build_lineage_surface_payload(
    repo_root: Path,
    skill_names: Sequence[str],
) -> dict[str, Any]:
    sources = skill_source_model.load_skill_sources(repo_root, skill_names)
    skills = [build_skill_lineage_entry(source) for source in sources]
    return {
        "lineage_surface_version": LINEAGE_SURFACE_VERSION,
        "source_of_truth": LINEAGE_SURFACE_SOURCE_OF_TRUTH,
        "cohorts": derive_lineage_cohorts(skills),
        "skills": skills,
    }


def render_lineage_surface_markdown(payload: Mapping[str, Any]) -> str:
    skill_entries = payload.get("skills", [])
    if not isinstance(skill_entries, list):
        raise ValueError("lineage surface field 'skills' must be a list")

    cohorts = payload.get("cohorts", {})
    published = cohorts.get(PUBLISHED_LINEAGE_COHORT, [])
    pending = cohorts.get(PENDING_LINEAGE_COHORT, [])

    lines = [
        "# Skill lineage surface",
        "",
        "This derived file summarizes manifest-only technique lineage readiness inside `aoa-skills`.",
        "It does not fetch or compare upstream repos; it only reflects committed bundle facts.",
        "",
        "## Summary",
        "",
        f"- total skills: {len(skill_entries)}",
        f"- published lineage: {len(published)}",
        f"- pending lineage: {len(pending)}",
        "",
        "| name | status | scope | lineage | published techniques | pending techniques | tbd refs | manifest canonical-path ready | blockers |",
        "|---|---|---|---|---:|---:|---:|---|---|",
    ]
    if not skill_entries:
        lines.append("| - | - | - | - | - | - | - | - | - |")
    else:
        for entry in skill_entries:
            blockers = entry.get("lineage_blockers", [])
            blocker_text = ", ".join(blockers) if blockers else "-"
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(entry["name"]),
                        str(entry["status"]),
                        str(entry["scope"]),
                        str(entry["lineage_state"]),
                        str(entry["published_technique_count"]),
                        str(entry["pending_technique_count"]),
                        str(entry["tbd_ref_count"]),
                        "true" if entry["manifest_canonical_path_ready"] else "false",
                        blocker_text,
                    ]
                )
                + " |"
            )
    lines.extend(
        [
            "",
            "## Reading notes",
            "",
            "- `manifest canonical-path ready` only reflects committed manifest facts, not upstream drift or human promotion judgment.",
            "- Skills blocked here still may be `evaluated`; this layer is about lineage readiness only.",
            "",
        ]
    )
    return "\n".join(lines)
