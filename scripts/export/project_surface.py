"""Project core/risk generated documents for the Agent Skills export builder."""

from __future__ import annotations

import pathlib
from typing import Any

from skill_model import skill_layout


def build_project_core_kernel_doc(kernel_doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "source_config": "config/project_core_skill_kernel.json",
        "kernel_id": kernel_doc["kernel_id"],
        "owner_repo": kernel_doc["owner_repo"],
        "description": kernel_doc["description"],
        "canonical_install_profile": kernel_doc["canonical_install_profile"],
        "backward_compatible_aliases": kernel_doc.get("backward_compatible_aliases", []),
        "skill_count": len(kernel_doc["skills"]),
        "skills": kernel_doc["skills"],
        "governance_contract": kernel_doc["governance_contract"],
        "skill_contracts": kernel_doc["skill_contracts"],
    }


def build_project_core_kernel_governance_doc(
    *,
    repo_root: pathlib.Path,
    skills_root: pathlib.Path,
    kernel_doc: dict[str, Any],
    export_map: dict[str, Any],
) -> dict[str, Any]:
    export_by_name = {entry["name"]: entry for entry in export_map["exports"]}
    governance_contract = kernel_doc["governance_contract"]
    skill_contracts = {
        entry["skill_name"]: entry
        for entry in kernel_doc["skill_contracts"]
    }
    skills: list[dict[str, Any]] = []

    for skill_name in kernel_doc["skills"]:
        contract = skill_contracts[skill_name]
        export_entry = export_by_name.get(skill_name, {})
        source_skill_dir = skill_layout.skill_dir_path(repo_root, skill_name)
        export_skill_dir = skills_root / skill_name
        references = set((export_entry.get("resource_inventory") or {}).get("references", []))
        blockers: list[str] = []

        detail_ref = contract["detail_receipt_schema_ref"]
        core_ref = governance_contract["core_receipt_schema_ref"]
        if not (source_skill_dir / detail_ref).exists():
            blockers.append("missing_source_detail_receipt_schema")
        if not (source_skill_dir / core_ref).exists():
            blockers.append("missing_source_core_receipt_schema")
        if detail_ref not in references:
            blockers.append("missing_portable_detail_receipt_schema")
        if core_ref not in references:
            blockers.append("missing_portable_core_receipt_schema")
        if not (export_skill_dir / detail_ref).exists():
            blockers.append("missing_exported_detail_receipt_schema")
        if not (export_skill_dir / core_ref).exists():
            blockers.append("missing_exported_core_receipt_schema")

        skills.append(
            {
                "skill_name": skill_name,
                "detail_event_kind": contract["detail_event_kind"],
                "detail_receipt_schema_ref": detail_ref,
                "core_receipt_schema_ref": core_ref,
                "detail_publisher": governance_contract["detail_publisher"],
                "core_publisher": governance_contract["core_publisher"],
                "stats_surface": governance_contract["stats_surface"],
                "gate_passed": not blockers,
                "blockers": blockers,
            }
        )

    return {
        "schema_version": 1,
        "source_config": "config/project_core_skill_kernel.json",
        "kernel_id": kernel_doc["kernel_id"],
        "canonical_install_profile": kernel_doc["canonical_install_profile"],
        "stats_surface": governance_contract["stats_surface"],
        "skills": skills,
    }


def build_project_core_outer_ring_doc(ring_doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "source_config": "config/project_core_outer_ring.json",
        "ring_id": ring_doc["ring_id"],
        "owner_repo": ring_doc["owner_repo"],
        "description": ring_doc["description"],
        "canonical_install_profile": ring_doc["canonical_install_profile"],
        "adjacent_kernel_id": ring_doc["adjacent_kernel_id"],
        "skill_count": len(ring_doc["skills"]),
        "skills": ring_doc["skills"],
        "clusters": [
            {
                "cluster_id": cluster["cluster_id"],
                "skill_count": len(cluster["skills"]),
                "skills": cluster["skills"],
            }
            for cluster in ring_doc["clusters"]
        ],
    }


def build_project_core_outer_ring_readiness_doc(
    *,
    ring_doc: dict[str, Any],
    skill_catalog: dict[str, Any],
    profiles_doc: dict[str, Any],
    collision_doc: dict[str, Any],
) -> dict[str, Any]:
    catalog_by_name = {entry["name"]: entry for entry in skill_catalog["skills"]}
    profile_map = profiles_doc.get("profiles", {})
    repo_core_only = set((profile_map.get("repo-core-only") or {}).get("skills", []))
    repo_outer_ring = set((profile_map.get(ring_doc["canonical_install_profile"]) or {}).get("skills", []))
    user_curated_core = set((profile_map.get("user-curated-core") or {}).get("skills", []))
    collision_by_name: dict[str, str | None] = {skill_name: None for skill_name in ring_doc["skills"]}
    cluster_by_name: dict[str, str] = {}
    for cluster in ring_doc["clusters"]:
        cluster_id = cluster["cluster_id"]
        for skill_name in cluster["skills"]:
            cluster_by_name[skill_name] = cluster_id
    for family in collision_doc.get("families", []):
        family_id = family["family"]
        for skill_name in family.get("skills", []):
            if skill_name in collision_by_name and collision_by_name[skill_name] is None:
                collision_by_name[skill_name] = family_id

    skills: list[dict[str, Any]] = []
    for skill_name in ring_doc["skills"]:
        catalog_entry = catalog_by_name.get(skill_name, {})
        blockers: list[str] = []
        cluster_id = cluster_by_name.get(skill_name)
        collision_family = collision_by_name.get(skill_name)
        if cluster_id is None:
            cluster_id = "unmapped"
            blockers.append("missing_cluster_mapping")
        if skill_name not in repo_outer_ring:
            blockers.append("missing_from_repo_project_core_outer_ring")
        if skill_name not in repo_core_only:
            blockers.append("missing_from_repo_core_only")
        if catalog_entry.get("scope") != "core":
            blockers.append("scope_not_core")
        if catalog_entry.get("status") not in {"canonical", "evaluated"}:
            blockers.append("status_not_ring_ready")
        if collision_family is None:
            blockers.append("missing_collision_family")
        elif collision_family != cluster_id:
            blockers.append("collision_family_mismatch")
        skills.append(
            {
                "skill_name": skill_name,
                "cluster_id": cluster_id,
                "scope": catalog_entry.get("scope"),
                "status": catalog_entry.get("status"),
                "invocation_mode": catalog_entry.get("invocation_mode"),
                "in_repo_core_only": skill_name in repo_core_only,
                "in_repo_project_core_outer_ring": skill_name in repo_outer_ring,
                "in_user_curated_core": skill_name in user_curated_core,
                "collision_family": collision_family,
                "readiness_passed": not blockers,
                "blockers": blockers,
            }
        )

    return {
        "schema_version": 1,
        "source_config": "config/project_core_outer_ring.json",
        "ring_id": ring_doc["ring_id"],
        "canonical_install_profile": ring_doc["canonical_install_profile"],
        "repo_core_only_profile": "repo-core-only",
        "user_curated_core_profile": "user-curated-core",
        "skills": skills,
    }


def build_project_risk_guard_ring_doc(ring_doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "source_config": "config/project_risk_guard_ring.json",
        "ring_id": ring_doc["ring_id"],
        "owner_repo": ring_doc["owner_repo"],
        "description": ring_doc["description"],
        "canonical_install_profile": ring_doc["canonical_install_profile"],
        "backcompat_alias_profile": ring_doc["backcompat_alias_profile"],
        "adjacent_kernel_id": ring_doc["adjacent_kernel_id"],
        "adjacent_outer_ring_id": ring_doc["adjacent_outer_ring_id"],
        "skill_count": len(ring_doc["skills"]),
        "skills": ring_doc["skills"],
        "clusters": [
            {
                "cluster_id": cluster["cluster_id"],
                "skill_count": len(cluster["skills"]),
                "skills": cluster["skills"],
            }
            for cluster in ring_doc["clusters"]
        ],
        "adjacent_overlays": ring_doc.get("adjacent_overlays", []),
    }


def build_project_risk_guard_ring_governance_doc(
    *,
    ring_doc: dict[str, Any],
    skill_catalog: dict[str, Any],
    profiles_doc: dict[str, Any],
    collision_doc: dict[str, Any],
) -> dict[str, Any]:
    catalog_by_name = {entry["name"]: entry for entry in skill_catalog["skills"]}
    profile_map = profiles_doc.get("profiles", {})
    repo_risk_ring = set(
        (profile_map.get(ring_doc["canonical_install_profile"]) or {}).get("skills", [])
    )
    repo_risk_alias = set(
        (profile_map.get(ring_doc["backcompat_alias_profile"]) or {}).get("skills", [])
    )
    repo_default = set((profile_map.get("repo-default") or {}).get("skills", []))
    collision_by_name: dict[str, str | None] = {skill_name: None for skill_name in ring_doc["skills"]}
    cluster_by_name: dict[str, str] = {}
    adjacent_overlay_by_name = {
        entry["base_skill_name"]: entry["overlay_skill_name"]
        for entry in ring_doc.get("adjacent_overlays", [])
    }
    for cluster in ring_doc["clusters"]:
        cluster_id = cluster["cluster_id"]
        for skill_name in cluster["skills"]:
            cluster_by_name[skill_name] = cluster_id
    for family in collision_doc.get("families", []):
        family_id = family["family"]
        for skill_name in family.get("skills", []):
            if skill_name in collision_by_name and collision_by_name[skill_name] is None:
                collision_by_name[skill_name] = family_id

    skills: list[dict[str, Any]] = []
    for skill_name in ring_doc["skills"]:
        catalog_entry = catalog_by_name.get(skill_name, {})
        blockers: list[str] = []
        cluster_id = cluster_by_name.get(skill_name)
        collision_family = collision_by_name.get(skill_name)
        if cluster_id is None:
            cluster_id = "unmapped"
            blockers.append("missing_cluster_mapping")
        adjacent_overlay_skill_name = adjacent_overlay_by_name.get(skill_name)
        adjacent_overlay_present = bool(
            adjacent_overlay_skill_name and adjacent_overlay_skill_name in catalog_by_name
        )
        if skill_name not in repo_risk_ring:
            blockers.append("missing_from_repo_project_risk_guard_ring")
        if skill_name not in repo_risk_alias:
            blockers.append("missing_from_repo_risk_explicit")
        if skill_name not in repo_default:
            blockers.append("missing_from_repo_default")
        if catalog_entry.get("scope") != "risk":
            blockers.append("scope_not_risk")
        if catalog_entry.get("status") not in {"canonical", "evaluated"}:
            blockers.append("status_not_ring_ready")
        if catalog_entry.get("invocation_mode") != "explicit-only":
            blockers.append("invocation_mode_not_explicit_only")
        if collision_family is None:
            blockers.append("missing_collision_family")
        elif collision_family != cluster_id:
            blockers.append("collision_family_mismatch")
        skills.append(
            {
                "skill_name": skill_name,
                "cluster_id": cluster_id,
                "scope": catalog_entry.get("scope"),
                "status": catalog_entry.get("status"),
                "invocation_mode": catalog_entry.get("invocation_mode"),
                "in_repo_project_risk_guard_ring": skill_name in repo_risk_ring,
                "in_repo_risk_explicit": skill_name in repo_risk_alias,
                "in_repo_default": skill_name in repo_default,
                "collision_family": collision_family,
                "adjacent_overlay_skill_name": adjacent_overlay_skill_name,
                "adjacent_overlay_present": adjacent_overlay_present,
                "governance_passed": not blockers,
                "blockers": blockers,
            }
        )

    return {
        "schema_version": 1,
        "source_config": "config/project_risk_guard_ring.json",
        "ring_id": ring_doc["ring_id"],
        "canonical_install_profile": ring_doc["canonical_install_profile"],
        "backcompat_alias_profile": ring_doc["backcompat_alias_profile"],
        "repo_default_profile": "repo-default",
        "skills": skills,
    }


def build_project_foundation_profile_doc(
    *,
    kernel_doc: dict[str, Any],
    outer_ring_doc: dict[str, Any],
    risk_ring_doc: dict[str, Any],
    profiles_doc: dict[str, Any],
) -> dict[str, Any]:
    foundation_profile_name = "repo-project-foundation"
    profile_map = profiles_doc.get("profiles", {})
    foundation_profile = profile_map.get(foundation_profile_name) or {}
    kernel_skills = list(kernel_doc["skills"])
    outer_ring_skills = list(outer_ring_doc["skills"])
    risk_ring_skills = list(risk_ring_doc["skills"])
    foundation_skills = [*kernel_skills, *outer_ring_skills, *risk_ring_skills]
    return {
        "schema_version": 1,
        "source_config": "config/skill_pack_profiles.json",
        "foundation_id": "project-foundation-v1",
        "owner_repo": "aoa-skills",
        "description": foundation_profile.get("description", ""),
        "canonical_install_profile": foundation_profile_name,
        "kernel_id": kernel_doc["kernel_id"],
        "outer_ring_id": outer_ring_doc["ring_id"],
        "risk_ring_id": risk_ring_doc["ring_id"],
        "skill_count": len(foundation_skills),
        "skills": foundation_skills,
        "kernel_skills": kernel_skills,
        "outer_ring_skills": outer_ring_skills,
        "risk_ring_skills": risk_ring_skills,
    }
