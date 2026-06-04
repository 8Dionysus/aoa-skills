"""Project core/risk generated-surface validator phase for Agent Skills export."""

from __future__ import annotations

import pathlib
from typing import Any

from skill_model import skill_layout
from validation.validators.agent_skills_export_contract import load_contract as load_export_contract

EXPORT_CONTRACT = load_export_contract()
EXPECTED_OUTER_RING_SKILLS = list(EXPORT_CONTRACT.expected_outer_ring_skills)
EXPECTED_OUTER_RING_CLUSTERS = list(EXPORT_CONTRACT.expected_outer_ring_clusters)
EXPECTED_RISK_RING_SKILLS = list(EXPORT_CONTRACT.expected_risk_ring_skills)
EXPECTED_RISK_RING_CLUSTERS = list(EXPORT_CONTRACT.expected_risk_ring_clusters)
EXPECTED_RISK_RING_ADJACENT_OVERLAYS = list(EXPORT_CONTRACT.expected_risk_ring_adjacent_overlays)
EXPECTED_FOUNDATION_PROFILE_SKILLS = list(EXPORT_CONTRACT.expected_foundation_profile_skills)


def first_payload_difference(expected: Any, actual: Any, prefix: str = "") -> str | None:
    if type(expected) is not type(actual):
        return f"{prefix}type mismatch: expected {type(expected).__name__}, got {type(actual).__name__}"
    if isinstance(expected, dict):
        expected_keys = set(expected)
        actual_keys = set(actual)
        if expected_keys != actual_keys:
            return (
                f"{prefix}key mismatch: expected {sorted(expected_keys)!r}, "
                f"got {sorted(actual_keys)!r}"
            )
        for key in expected:
            next_prefix = f"{prefix}.{key}" if prefix else str(key)
            difference = first_payload_difference(expected[key], actual[key], next_prefix)
            if difference is not None:
                return difference
        return None
    if isinstance(expected, list):
        if len(expected) != len(actual):
            return f"{prefix}length mismatch: expected {len(expected)}, got {len(actual)}"
        for index, (expected_item, actual_item) in enumerate(zip(expected, actual)):
            next_prefix = f"{prefix}[{index}]"
            difference = first_payload_difference(expected_item, actual_item, next_prefix)
            if difference is not None:
                return difference
        return None
    if expected != actual:
        return f"{prefix} mismatch: expected {expected!r}, got {actual!r}"
    return None


def validate_project_core_kernel_surfaces(
    repo_root: pathlib.Path,
    skills_root: pathlib.Path,
    docs: Any,
    indexes: Any,
    errors: list[str],
) -> None:
    kernel_skills = docs.kernel_doc.get("skills", [])
    governance_contract = docs.kernel_doc.get("governance_contract")
    skill_contracts = docs.kernel_doc.get("skill_contracts", [])
    if docs.kernel_doc.get("schema_version") != 1:
        errors.append("config/project_core_skill_kernel.json schema_version must be 1")
    if not isinstance(docs.kernel_doc.get("kernel_id"), str) or not docs.kernel_doc["kernel_id"]:
        errors.append("config/project_core_skill_kernel.json kernel_id must be a non-empty string")
    if not isinstance(docs.kernel_doc.get("canonical_install_profile"), str) or not docs.kernel_doc["canonical_install_profile"]:
        errors.append("config/project_core_skill_kernel.json canonical_install_profile must be a non-empty string")
    if not isinstance(docs.kernel_doc.get("backward_compatible_aliases"), list):
        errors.append("config/project_core_skill_kernel.json backward_compatible_aliases must be a list")
    if not isinstance(governance_contract, dict):
        errors.append("config/project_core_skill_kernel.json governance_contract must be an object")
        governance_contract = {}
    if not isinstance(kernel_skills, list) or not kernel_skills:
        errors.append("config/project_core_skill_kernel.json skills must be a non-empty list")
    elif len(kernel_skills) != len(set(kernel_skills)):
        errors.append("config/project_core_skill_kernel.json skills must not contain duplicates")
    if not isinstance(skill_contracts, list) or not skill_contracts:
        errors.append("config/project_core_skill_kernel.json skill_contracts must be a non-empty list")
        skill_contracts = []

    expected_governance_contract = {
        "core_receipt_kind": "core_skill_application_receipt",
        "core_receipt_schema_ref": "references/core-skill-application-receipt-schema.yaml",
        "detail_publisher": "aoa-skills.session-harvest-family",
        "core_publisher": "aoa-skills.core-kernel-applications",
        "stats_surface": "aoa-stats.core_skill_application_summary.min",
        "application_stage": "finish",
    }
    if governance_contract != expected_governance_contract:
        errors.append("config/project_core_skill_kernel.json governance_contract must match the canonical kernel telemetry contract")

    skill_contracts_by_name: dict[str, dict[str, Any]] = {}
    for entry in skill_contracts:
        if not isinstance(entry, dict):
            errors.append("config/project_core_skill_kernel.json skill_contracts entries must be objects")
            continue
        skill_name = entry.get("skill_name")
        if not isinstance(skill_name, str) or not skill_name:
            errors.append("config/project_core_skill_kernel.json skill_contracts skill_name must be a non-empty string")
            continue
        if skill_name in skill_contracts_by_name:
            errors.append(f"config/project_core_skill_kernel.json duplicate skill_contract entry for {skill_name}")
            continue
        skill_contracts_by_name[skill_name] = entry
        for field in ("detail_event_kind", "detail_receipt_schema_ref"):
            value = entry.get(field)
            if not isinstance(value, str) or not value:
                errors.append(f"config/project_core_skill_kernel.json skill_contracts[{skill_name!r}].{field} must be a non-empty string")

    if list(skill_contracts_by_name) != kernel_skills:
        errors.append("config/project_core_skill_kernel.json skill_contract order must match skills exactly")

    expected_resolved_kernel = {
        "schema_version": 1,
        "source_config": "config/project_core_skill_kernel.json",
        "kernel_id": docs.kernel_doc.get("kernel_id"),
        "owner_repo": docs.kernel_doc.get("owner_repo"),
        "description": docs.kernel_doc.get("description"),
        "canonical_install_profile": docs.kernel_doc.get("canonical_install_profile"),
        "backward_compatible_aliases": docs.kernel_doc.get("backward_compatible_aliases", []),
        "skill_count": len(kernel_skills) if isinstance(kernel_skills, list) else 0,
        "skills": kernel_skills,
        "governance_contract": governance_contract,
        "skill_contracts": skill_contracts,
    }
    if docs.resolved_kernel != expected_resolved_kernel:
        errors.append("generated/project_core_skill_kernel.min.json mismatch")
        difference = first_payload_difference(expected_resolved_kernel, docs.resolved_kernel)
        if difference is not None:
            errors.append(f"generated/project_core_skill_kernel.min.json detail: {difference}")

    canonical_profile_name = docs.kernel_doc.get("canonical_install_profile")
    alias_profile_names = (
        docs.kernel_doc.get("backward_compatible_aliases", [])
        if isinstance(docs.kernel_doc.get("backward_compatible_aliases"), list)
        else []
    )
    if isinstance(canonical_profile_name, str):
        canonical_profile = (docs.profile_doc.get("profiles") or {}).get(canonical_profile_name)
        if canonical_profile is None:
            errors.append(f"config/project_core_skill_kernel.json canonical_install_profile missing from skill profiles: {canonical_profile_name}")
        elif canonical_profile.get("skills") != kernel_skills:
            errors.append("config/project_core_skill_kernel.json canonical profile skills must match kernel skills exactly")
    for alias_profile_name in alias_profile_names:
        alias_profile = (docs.profile_doc.get("profiles") or {}).get(alias_profile_name)
        if alias_profile is None:
            errors.append(f"config/project_core_skill_kernel.json alias missing from skill profiles: {alias_profile_name}")
            continue
        if alias_profile.get("skills") != kernel_skills:
            errors.append(f"config/project_core_skill_kernel.json alias {alias_profile_name} must match kernel skills exactly")

    expected_kernel_governance_skills: list[dict[str, Any]] = []
    for skill_name in kernel_skills:
        contract = skill_contracts_by_name.get(skill_name, {})
        export_entry = indexes.export_by_name.get(skill_name, {})
        exported_references = set((export_entry.get("resource_inventory") or {}).get("references", []))
        source_skill_dir = skill_layout.skill_dir_path(repo_root, skill_name)
        exported_skill_dir = skills_root / skill_name
        detail_ref = contract.get("detail_receipt_schema_ref")
        core_ref = governance_contract.get("core_receipt_schema_ref")
        blockers: list[str] = []
        if not isinstance(detail_ref, str) or not detail_ref:
            blockers.append("missing_detail_contract")
        else:
            if not (source_skill_dir / detail_ref).exists():
                blockers.append("missing_source_detail_receipt_schema")
            if detail_ref not in exported_references:
                blockers.append("missing_portable_detail_receipt_schema")
            if not (exported_skill_dir / detail_ref).exists():
                blockers.append("missing_exported_detail_receipt_schema")
        if not isinstance(core_ref, str) or not core_ref:
            blockers.append("missing_core_contract")
        else:
            if not (source_skill_dir / core_ref).exists():
                blockers.append("missing_source_core_receipt_schema")
            if core_ref not in exported_references:
                blockers.append("missing_portable_core_receipt_schema")
            if not (exported_skill_dir / core_ref).exists():
                blockers.append("missing_exported_core_receipt_schema")
        expected_kernel_governance_skills.append(
            {
                "skill_name": skill_name,
                "detail_event_kind": contract.get("detail_event_kind"),
                "detail_receipt_schema_ref": detail_ref,
                "core_receipt_schema_ref": core_ref,
                "detail_publisher": governance_contract.get("detail_publisher"),
                "core_publisher": governance_contract.get("core_publisher"),
                "stats_surface": governance_contract.get("stats_surface"),
                "gate_passed": not blockers,
                "blockers": blockers,
            }
        )

    expected_kernel_governance = {
        "schema_version": 1,
        "source_config": "config/project_core_skill_kernel.json",
        "kernel_id": docs.kernel_doc.get("kernel_id"),
        "canonical_install_profile": docs.kernel_doc.get("canonical_install_profile"),
        "stats_surface": governance_contract.get("stats_surface"),
        "skills": expected_kernel_governance_skills,
    }
    if docs.kernel_governance != expected_kernel_governance:
        errors.append("generated/project_core_kernel_governance.min.json mismatch")
        difference = first_payload_difference(expected_kernel_governance, docs.kernel_governance)
        if difference is not None:
            errors.append(f"generated/project_core_kernel_governance.min.json detail: {difference}")
    for entry in expected_kernel_governance_skills:
        if not entry["gate_passed"]:
            blockers = ", ".join(entry["blockers"])
            errors.append(f"project-core kernel governance gate failed for {entry['skill_name']}: {blockers}")


def validate_project_core_outer_ring_surfaces(docs: Any, indexes: Any, errors: list[str]) -> None:
    kernel_skills = docs.kernel_doc.get("skills", [])
    outer_ring_skills = docs.outer_ring_doc.get("skills", [])
    outer_ring_clusters = docs.outer_ring_doc.get("clusters", [])
    if docs.outer_ring_doc.get("schema_version") != 1:
        errors.append("config/project_core_outer_ring.json schema_version must be 1")
    if docs.outer_ring_doc.get("ring_id") != "project-core-engineering-ring-v1":
        errors.append("config/project_core_outer_ring.json ring_id must be 'project-core-engineering-ring-v1'")
    if docs.outer_ring_doc.get("owner_repo") != "aoa-skills":
        errors.append("config/project_core_outer_ring.json owner_repo must be 'aoa-skills'")
    if not isinstance(docs.outer_ring_doc.get("description"), str) or not docs.outer_ring_doc["description"]:
        errors.append("config/project_core_outer_ring.json description must be a non-empty string")
    if docs.outer_ring_doc.get("canonical_install_profile") != "repo-project-core-outer-ring":
        errors.append("config/project_core_outer_ring.json canonical_install_profile must be 'repo-project-core-outer-ring'")
    if docs.outer_ring_doc.get("adjacent_kernel_id") != docs.kernel_doc.get("kernel_id"):
        errors.append("config/project_core_outer_ring.json adjacent_kernel_id must match the canonical project-core kernel id")
    if outer_ring_skills != EXPECTED_OUTER_RING_SKILLS:
        errors.append("config/project_core_outer_ring.json skills must match the canonical project-core engineering ring order exactly")
    if len(outer_ring_skills) != len(set(outer_ring_skills)):
        errors.append("config/project_core_outer_ring.json skills must not contain duplicates")
    expected_cluster_payload = EXPECTED_OUTER_RING_CLUSTERS
    if outer_ring_clusters != expected_cluster_payload:
        errors.append("config/project_core_outer_ring.json clusters must match the canonical project-core engineering ring cluster map exactly")

    expected_resolved_outer_ring = {
        "schema_version": 1,
        "source_config": "config/project_core_outer_ring.json",
        "ring_id": docs.outer_ring_doc.get("ring_id"),
        "owner_repo": docs.outer_ring_doc.get("owner_repo"),
        "description": docs.outer_ring_doc.get("description"),
        "canonical_install_profile": docs.outer_ring_doc.get("canonical_install_profile"),
        "adjacent_kernel_id": docs.outer_ring_doc.get("adjacent_kernel_id"),
        "skill_count": len(outer_ring_skills) if isinstance(outer_ring_skills, list) else 0,
        "skills": outer_ring_skills,
        "clusters": [
            {
                "cluster_id": cluster["cluster_id"],
                "skill_count": len(cluster["skills"]),
                "skills": cluster["skills"],
            }
            for cluster in outer_ring_clusters
            if isinstance(cluster, dict) and isinstance(cluster.get("skills"), list)
        ],
    }
    if docs.resolved_outer_ring != expected_resolved_outer_ring:
        errors.append("generated/project_core_outer_ring.min.json mismatch")
        difference = first_payload_difference(expected_resolved_outer_ring, docs.resolved_outer_ring)
        if difference is not None:
            errors.append(f"generated/project_core_outer_ring.min.json detail: {difference}")

    outer_ring_profile = (docs.profile_doc.get("profiles") or {}).get(docs.outer_ring_doc.get("canonical_install_profile"))
    if outer_ring_profile is None:
        errors.append("config/project_core_outer_ring.json canonical_install_profile missing from skill profiles")
        outer_ring_profile_skills: list[str] = []
    else:
        outer_ring_profile_skills = outer_ring_profile.get("skills", [])
        if outer_ring_profile_skills != outer_ring_skills:
            errors.append("config/project_core_outer_ring.json canonical profile skills must match outer ring skills exactly")

    repo_core_only_profile = (docs.profile_doc.get("profiles") or {}).get("repo-core-only")
    if repo_core_only_profile is None:
        errors.append("config/skill_pack_profiles.json missing repo-core-only")
        repo_core_only_skills: list[str] = []
    else:
        repo_core_only_skills = repo_core_only_profile.get("skills", [])
        expected_repo_core_only = [*kernel_skills, *outer_ring_skills]
        if repo_core_only_skills != expected_repo_core_only:
            errors.append("config/skill_pack_profiles.json repo-core-only must equal project-core kernel plus project-core outer ring in canonical order")

    user_curated_core_profile = (docs.profile_doc.get("profiles") or {}).get("user-curated-core")
    user_curated_core_skills = (
        user_curated_core_profile.get("skills", [])
        if isinstance(user_curated_core_profile, dict)
        else []
    )
    expected_cluster_by_skill = {
        skill_name: cluster["cluster_id"]
        for cluster in EXPECTED_OUTER_RING_CLUSTERS
        for skill_name in cluster["skills"]
    }
    expected_outer_ring_readiness_skills: list[dict[str, Any]] = []
    for skill_name in outer_ring_skills:
        source_entry = indexes.source_by_name.get(skill_name, {})
        expected_cluster = expected_cluster_by_skill.get(skill_name)
        actual_families = sorted(indexes.description_families_by_skill.get(skill_name, []))
        actual_collision_family = (
            expected_cluster
            if expected_cluster is not None and expected_cluster in actual_families
            else (actual_families[0] if actual_families else None)
        )
        blockers: list[str] = []
        if expected_cluster is None:
            expected_cluster = "unmapped"
            blockers.append("missing_cluster_mapping")
        if skill_name not in outer_ring_profile_skills:
            blockers.append("missing_from_repo_project_core_outer_ring")
        if skill_name not in repo_core_only_skills:
            blockers.append("missing_from_repo_core_only")
        if source_entry.get("scope") != "core":
            blockers.append("scope_not_core")
        if source_entry.get("status") not in {"canonical", "evaluated"}:
            blockers.append("status_not_ring_ready")
        if actual_collision_family is None:
            blockers.append("missing_collision_family")
        elif actual_collision_family != expected_cluster:
            blockers.append("collision_family_mismatch")
        expected_outer_ring_readiness_skills.append(
            {
                "skill_name": skill_name,
                "cluster_id": expected_cluster,
                "scope": source_entry.get("scope"),
                "status": source_entry.get("status"),
                "invocation_mode": source_entry.get("invocation_mode"),
                "in_repo_core_only": skill_name in repo_core_only_skills,
                "in_repo_project_core_outer_ring": skill_name in outer_ring_profile_skills,
                "in_user_curated_core": skill_name in user_curated_core_skills,
                "collision_family": actual_collision_family,
                "readiness_passed": not blockers,
                "blockers": blockers,
            }
        )

    expected_outer_ring_readiness = {
        "schema_version": 1,
        "source_config": "config/project_core_outer_ring.json",
        "ring_id": docs.outer_ring_doc.get("ring_id"),
        "canonical_install_profile": docs.outer_ring_doc.get("canonical_install_profile"),
        "repo_core_only_profile": "repo-core-only",
        "user_curated_core_profile": "user-curated-core",
        "skills": expected_outer_ring_readiness_skills,
    }
    if docs.outer_ring_readiness != expected_outer_ring_readiness:
        errors.append("generated/project_core_outer_ring_readiness.min.json mismatch")
        difference = first_payload_difference(expected_outer_ring_readiness, docs.outer_ring_readiness)
        if difference is not None:
            errors.append(f"generated/project_core_outer_ring_readiness.min.json detail: {difference}")
    for entry in expected_outer_ring_readiness_skills:
        if not entry["readiness_passed"]:
            blockers = ", ".join(entry["blockers"])
            errors.append(f"project-core outer ring readiness gate failed for {entry['skill_name']}: {blockers}")


def validate_project_risk_ring_surfaces(
    docs: Any,
    indexes: Any,
    actual_names: set[str],
    errors: list[str],
) -> None:
    risk_ring_skills = docs.risk_ring_doc.get("skills", [])
    risk_ring_clusters = docs.risk_ring_doc.get("clusters", [])
    risk_ring_adjacent_overlays = docs.risk_ring_doc.get("adjacent_overlays", [])
    if docs.risk_ring_doc.get("schema_version") != 1:
        errors.append("config/project_risk_guard_ring.json schema_version must be 1")
    if docs.risk_ring_doc.get("ring_id") != "project-risk-guard-ring-v1":
        errors.append("config/project_risk_guard_ring.json ring_id must be 'project-risk-guard-ring-v1'")
    if docs.risk_ring_doc.get("owner_repo") != "aoa-skills":
        errors.append("config/project_risk_guard_ring.json owner_repo must be 'aoa-skills'")
    if not isinstance(docs.risk_ring_doc.get("description"), str) or not docs.risk_ring_doc["description"]:
        errors.append("config/project_risk_guard_ring.json description must be a non-empty string")
    if docs.risk_ring_doc.get("canonical_install_profile") != "repo-project-risk-guard-ring":
        errors.append("config/project_risk_guard_ring.json canonical_install_profile must be 'repo-project-risk-guard-ring'")
    if docs.risk_ring_doc.get("backcompat_alias_profile") != "repo-risk-explicit":
        errors.append("config/project_risk_guard_ring.json backcompat_alias_profile must be 'repo-risk-explicit'")
    if docs.risk_ring_doc.get("adjacent_kernel_id") != docs.kernel_doc.get("kernel_id"):
        errors.append("config/project_risk_guard_ring.json adjacent_kernel_id must match the canonical project-core kernel id")
    if docs.risk_ring_doc.get("adjacent_outer_ring_id") != docs.outer_ring_doc.get("ring_id"):
        errors.append("config/project_risk_guard_ring.json adjacent_outer_ring_id must match the canonical project-core outer ring id")
    if risk_ring_skills != EXPECTED_RISK_RING_SKILLS:
        errors.append("config/project_risk_guard_ring.json skills must match the canonical risk guard ring order exactly")
    if len(risk_ring_skills) != len(set(risk_ring_skills)):
        errors.append("config/project_risk_guard_ring.json skills must not contain duplicates")
    if risk_ring_clusters != EXPECTED_RISK_RING_CLUSTERS:
        errors.append("config/project_risk_guard_ring.json clusters must match the canonical risk guard ring cluster map exactly")
    if risk_ring_adjacent_overlays != EXPECTED_RISK_RING_ADJACENT_OVERLAYS:
        errors.append("config/project_risk_guard_ring.json adjacent_overlays must match the canonical adjacent overlay map exactly")

    expected_resolved_risk_ring = {
        "schema_version": 1,
        "source_config": "config/project_risk_guard_ring.json",
        "ring_id": docs.risk_ring_doc.get("ring_id"),
        "owner_repo": docs.risk_ring_doc.get("owner_repo"),
        "description": docs.risk_ring_doc.get("description"),
        "canonical_install_profile": docs.risk_ring_doc.get("canonical_install_profile"),
        "backcompat_alias_profile": docs.risk_ring_doc.get("backcompat_alias_profile"),
        "adjacent_kernel_id": docs.risk_ring_doc.get("adjacent_kernel_id"),
        "adjacent_outer_ring_id": docs.risk_ring_doc.get("adjacent_outer_ring_id"),
        "skill_count": len(risk_ring_skills) if isinstance(risk_ring_skills, list) else 0,
        "skills": risk_ring_skills,
        "clusters": [
            {
                "cluster_id": cluster["cluster_id"],
                "skill_count": len(cluster["skills"]),
                "skills": cluster["skills"],
            }
            for cluster in risk_ring_clusters
            if isinstance(cluster, dict) and isinstance(cluster.get("skills"), list)
        ],
        "adjacent_overlays": risk_ring_adjacent_overlays,
    }
    if docs.resolved_risk_ring != expected_resolved_risk_ring:
        errors.append("generated/project_risk_guard_ring.min.json mismatch")
        difference = first_payload_difference(expected_resolved_risk_ring, docs.resolved_risk_ring)
        if difference is not None:
            errors.append(f"generated/project_risk_guard_ring.min.json detail: {difference}")

    risk_ring_profile = (docs.profile_doc.get("profiles") or {}).get(
        docs.risk_ring_doc.get("canonical_install_profile")
    )
    if risk_ring_profile is None:
        errors.append("config/project_risk_guard_ring.json canonical_install_profile missing from skill profiles")
        risk_ring_profile_skills: list[str] = []
    else:
        risk_ring_profile_skills = risk_ring_profile.get("skills", [])
        if risk_ring_profile_skills != risk_ring_skills:
            errors.append("config/project_risk_guard_ring.json canonical profile skills must match risk guard ring skills exactly")

    risk_ring_alias_profile = (docs.profile_doc.get("profiles") or {}).get(
        docs.risk_ring_doc.get("backcompat_alias_profile")
    )
    if risk_ring_alias_profile is None:
        errors.append("config/project_risk_guard_ring.json backcompat_alias_profile missing from skill profiles")
        risk_ring_alias_skills: list[str] = []
    else:
        risk_ring_alias_skills = risk_ring_alias_profile.get("skills", [])
        if risk_ring_alias_skills != risk_ring_skills:
            errors.append("config/project_risk_guard_ring.json backcompat alias skills must match risk guard ring skills exactly")

    repo_default_profile = (docs.profile_doc.get("profiles") or {}).get("repo-default")
    if repo_default_profile is None:
        errors.append("config/skill_pack_profiles.json missing repo-default")
        repo_default_skills: list[str] = []
    else:
        repo_default_skills = repo_default_profile.get("skills", [])
        missing_default_risk_skills = [
            skill_name for skill_name in risk_ring_skills if skill_name not in repo_default_skills
        ]
        if missing_default_risk_skills:
            errors.append(
                "config/skill_pack_profiles.json repo-default must include every risk guard ring skill"
            )

    expected_risk_cluster_by_skill = {
        skill_name: cluster["cluster_id"]
        for cluster in EXPECTED_RISK_RING_CLUSTERS
        for skill_name in cluster["skills"]
    }
    adjacent_overlay_by_skill = {
        entry["base_skill_name"]: entry["overlay_skill_name"]
        for entry in EXPECTED_RISK_RING_ADJACENT_OVERLAYS
    }
    expected_risk_governance_skills: list[dict[str, Any]] = []
    for skill_name in risk_ring_skills:
        source_entry = indexes.source_by_name.get(skill_name, {})
        expected_cluster = expected_risk_cluster_by_skill[skill_name]
        actual_families = sorted(indexes.description_families_by_skill.get(skill_name, []))
        actual_collision_family = (
            expected_cluster if expected_cluster in actual_families else (actual_families[0] if actual_families else None)
        )
        adjacent_overlay_skill_name = adjacent_overlay_by_skill.get(skill_name)
        adjacent_overlay_present = bool(
            adjacent_overlay_skill_name and adjacent_overlay_skill_name in actual_names
        )
        blockers: list[str] = []
        if skill_name not in risk_ring_profile_skills:
            blockers.append("missing_from_repo_project_risk_guard_ring")
        if skill_name not in risk_ring_alias_skills:
            blockers.append("missing_from_repo_risk_explicit")
        if skill_name not in repo_default_skills:
            blockers.append("missing_from_repo_default")
        if source_entry.get("scope") != "risk":
            blockers.append("scope_not_risk")
        if source_entry.get("status") not in {"canonical", "evaluated"}:
            blockers.append("status_not_ring_ready")
        if source_entry.get("invocation_mode") != "explicit-only":
            blockers.append("invocation_mode_not_explicit_only")
        if actual_collision_family is None:
            blockers.append("missing_collision_family")
        elif actual_collision_family != expected_cluster:
            blockers.append("collision_family_mismatch")
        expected_risk_governance_skills.append(
            {
                "skill_name": skill_name,
                "cluster_id": expected_cluster,
                "scope": source_entry.get("scope"),
                "status": source_entry.get("status"),
                "invocation_mode": source_entry.get("invocation_mode"),
                "in_repo_project_risk_guard_ring": skill_name in risk_ring_profile_skills,
                "in_repo_risk_explicit": skill_name in risk_ring_alias_skills,
                "in_repo_default": skill_name in repo_default_skills,
                "collision_family": actual_collision_family,
                "adjacent_overlay_skill_name": adjacent_overlay_skill_name,
                "adjacent_overlay_present": adjacent_overlay_present,
                "governance_passed": not blockers,
                "blockers": blockers,
            }
        )

    expected_risk_ring_governance = {
        "schema_version": 1,
        "source_config": "config/project_risk_guard_ring.json",
        "ring_id": docs.risk_ring_doc.get("ring_id"),
        "canonical_install_profile": docs.risk_ring_doc.get("canonical_install_profile"),
        "backcompat_alias_profile": docs.risk_ring_doc.get("backcompat_alias_profile"),
        "repo_default_profile": "repo-default",
        "skills": expected_risk_governance_skills,
    }
    if docs.risk_ring_governance != expected_risk_ring_governance:
        errors.append("generated/project_risk_guard_ring_governance.min.json mismatch")
        difference = first_payload_difference(expected_risk_ring_governance, docs.risk_ring_governance)
        if difference is not None:
            errors.append(f"generated/project_risk_guard_ring_governance.min.json detail: {difference}")
    for entry in expected_risk_governance_skills:
        if not entry["governance_passed"]:
            blockers = ", ".join(entry["blockers"])
            errors.append(f"project risk guard ring governance gate failed for {entry['skill_name']}: {blockers}")


def validate_project_foundation_profile(docs: Any, errors: list[str]) -> None:
    foundation_profile_doc = (docs.profile_doc.get("profiles") or {}).get("repo-project-foundation")
    if foundation_profile_doc is None:
        errors.append("config/skill_pack_profiles.json missing repo-project-foundation")
    else:
        if foundation_profile_doc.get("scope") != "repo":
            errors.append("config/skill_pack_profiles.json repo-project-foundation scope must be 'repo'")
        if foundation_profile_doc.get("install_mode") != "symlink-preferred":
            errors.append(
                "config/skill_pack_profiles.json repo-project-foundation install_mode must be 'symlink-preferred'"
            )
        foundation_profile_skills = foundation_profile_doc.get("skills") or []
        if foundation_profile_skills != EXPECTED_FOUNDATION_PROFILE_SKILLS:
            errors.append(
                "config/skill_pack_profiles.json repo-project-foundation must equal kernel + outer ring + risk ring in canonical order"
            )
        expected_foundation_profile = {
            "schema_version": 1,
            "source_config": "config/skill_pack_profiles.json",
            "foundation_id": "project-foundation-v1",
            "owner_repo": "aoa-skills",
            "description": foundation_profile_doc.get("description", ""),
            "canonical_install_profile": "repo-project-foundation",
            "kernel_id": docs.kernel_doc.get("kernel_id"),
            "outer_ring_id": docs.outer_ring_doc.get("ring_id"),
            "risk_ring_id": docs.risk_ring_doc.get("ring_id"),
            "skill_count": len(EXPECTED_FOUNDATION_PROFILE_SKILLS),
            "skills": EXPECTED_FOUNDATION_PROFILE_SKILLS,
            "kernel_skills": docs.kernel_doc.get("skills"),
            "outer_ring_skills": docs.outer_ring_doc.get("skills"),
            "risk_ring_skills": docs.risk_ring_doc.get("skills"),
        }
        if docs.foundation_profile != expected_foundation_profile:
            errors.append("generated/project_foundation_profile.min.json mismatch")
            difference = first_payload_difference(expected_foundation_profile, docs.foundation_profile)
            if difference is not None:
                errors.append(f"generated/project_foundation_profile.min.json detail: {difference}")
