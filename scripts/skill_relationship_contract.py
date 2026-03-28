from __future__ import annotations

from typing import Any, Mapping, Sequence

import skill_catalog_contract
import skill_source_model


RELATIONSHIP_VIEW_PATHS = (
    "generated/skill_bundle_index.json",
    "generated/skill_bundle_index.md",
    "generated/skill_graph.json",
    "generated/skill_graph.md",
)
SUPPORT_RESOURCE_ARTIFACT_GROUP_ID = "support_resources"


def profile_skill_names(profile_entry: Any) -> list[str]:
    if not isinstance(profile_entry, Mapping):
        return []
    raw_skills = profile_entry.get("skills", [])
    if not isinstance(raw_skills, list):
        return []

    names: list[str] = []
    for item in raw_skills:
        if isinstance(item, str):
            names.append(item)
            continue
        if isinstance(item, Mapping):
            name = item.get("name")
            if isinstance(name, str):
                names.append(name)
    return names


def build_install_profile_membership(
    skill_names: Sequence[str],
    profiles_doc: Mapping[str, Any],
) -> dict[str, list[str]]:
    membership = {skill_name: [] for skill_name in skill_names}
    profiles = profiles_doc.get("profiles", {})
    if not isinstance(profiles, Mapping):
        return membership

    for profile_name in sorted(profiles):
        profile_entry = profiles[profile_name]
        for skill_name in profile_skill_names(profile_entry):
            if skill_name in membership:
                membership[skill_name].append(profile_name)
    return membership


def build_artifact_group_coverage(
    skill_names: Sequence[str],
    artifact_groups: Sequence[Mapping[str, Any]],
    *,
    support_resource_skill_names: Sequence[str],
) -> dict[str, list[str]]:
    support_skill_set = set(support_resource_skill_names)
    coverage: dict[str, list[str]] = {}
    for skill_name in skill_names:
        coverage[skill_name] = []
        for group in artifact_groups:
            group_id = group.get("id")
            if not isinstance(group_id, str):
                continue
            if group_id == SUPPORT_RESOURCE_ARTIFACT_GROUP_ID:
                if skill_name in support_skill_set:
                    coverage[skill_name].append(group_id)
                continue
            coverage[skill_name].append(group_id)
    return coverage


def technique_lineage_state(technique_entry: Mapping[str, Any]) -> str:
    technique_id = technique_entry.get("id")
    path_value = technique_entry.get("path")
    source_ref = technique_entry.get("source_ref")
    if isinstance(technique_id, str) and technique_id.startswith("AOA-T-PENDING-"):
        return "pending"
    if path_value == "TBD" or source_ref == "TBD":
        return "pending"
    return "published"


def build_technique_lineage(
    source: skill_source_model.SkillSource,
) -> list[dict[str, str]]:
    techniques = skill_catalog_contract.normalize_technique_refs(source.manifest)
    lineage: list[dict[str, str]] = []
    for technique in techniques:
        lineage.append(
            {
                "id": str(technique.get("id") or ""),
                "repo": str(technique.get("repo") or ""),
                "path": str(technique.get("path") or ""),
                "source_ref": str(technique.get("source_ref") or ""),
                "lineage_state": technique_lineage_state(technique),
            }
        )
    return lineage


def build_skill_relationship_layers(
    skill_sources: Sequence[skill_source_model.SkillSource],
    *,
    profiles_doc: Mapping[str, Any],
    artifact_groups: Sequence[Mapping[str, Any]],
    support_resource_skill_names: Sequence[str],
) -> dict[str, dict[str, Any]]:
    skill_names = [source.name for source in skill_sources]
    install_profiles = build_install_profile_membership(skill_names, profiles_doc)
    artifact_group_coverage = build_artifact_group_coverage(
        skill_names,
        artifact_groups,
        support_resource_skill_names=support_resource_skill_names,
    )

    relationship_layers: dict[str, dict[str, Any]] = {}
    for source in skill_sources:
        relationship_layers[source.name] = {
            "install_profiles": install_profiles.get(source.name, []),
            "artifact_group_coverage": artifact_group_coverage.get(source.name, []),
            "technique_lineage": build_technique_lineage(source),
        }
    return relationship_layers
