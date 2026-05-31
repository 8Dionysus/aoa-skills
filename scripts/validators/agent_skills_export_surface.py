"""Agent Skills export/runtime surface validator for aoa-skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
import tempfile
from dataclasses import dataclass
from typing import Any

import release_manifest_contract
import yaml
import build_catalog
from skill_activation_policy import (
    allow_implicit_invocation,
    required_case_classes as activation_required_case_classes,
    resolve_implicit_activation_policy,
)
import skill_layout

from skill_runtime_guardrails import (
    activate_guarded_payload,
    discover_guarded_payload,
    load_guardrails,
    trust_payload,
)
from validators.agent_skills_export_contract import load_contract as load_export_contract

EXPORT_CONTRACT = load_export_contract()
EXPORT_PROFILE = EXPORT_CONTRACT.export_profile
RUNTIME_PROFILE = EXPORT_CONTRACT.runtime_profile
GUARDRAIL_PROFILE = EXPORT_CONTRACT.guardrail_profile
DESCRIPTION_TRIGGER_PROFILE = EXPORT_CONTRACT.description_trigger_profile
SKILLS_REF_PROFILE = EXPORT_CONTRACT.skills_ref_profile
SUPPORT_RESOURCE_PROFILE = EXPORT_CONTRACT.support_resource_profile
TINY_ROUTER_PROFILE = EXPORT_CONTRACT.tiny_router_profile
TARGETED_SUPPORT_SKILLS = set(EXPORT_CONTRACT.targeted_support_skills)
SUPPORT_STANDARD_DIRS = EXPORT_CONTRACT.support_standard_dirs
SUPPORT_LEGACY_DIRS = EXPORT_CONTRACT.support_legacy_dirs
PORTABLE_RESOURCE_DIRS = EXPORT_CONTRACT.portable_resource_dirs
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
REQUIRED_METADATA = set(EXPORT_CONTRACT.required_metadata)
REQUIRED_GENERATED_FILES = list(EXPORT_CONTRACT.required_generated_files)
REQUIRED_CONFIG_FILES = list(EXPORT_CONTRACT.required_config_files)
EXPECTED_OUTER_RING_SKILLS = list(EXPORT_CONTRACT.expected_outer_ring_skills)
EXPECTED_OUTER_RING_CLUSTERS = list(EXPORT_CONTRACT.expected_outer_ring_clusters)
EXPECTED_RISK_RING_SKILLS = list(EXPORT_CONTRACT.expected_risk_ring_skills)
EXPECTED_RISK_RING_CLUSTERS = list(EXPORT_CONTRACT.expected_risk_ring_clusters)
EXPECTED_RISK_RING_ADJACENT_OVERLAYS = list(EXPORT_CONTRACT.expected_risk_ring_adjacent_overlays)
EXPECTED_FOUNDATION_PROFILE_SKILLS = list(EXPORT_CONTRACT.expected_foundation_profile_skills)

def parse_frontmatter(path: pathlib.Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter start")
    try:
        _, fm_text, body = text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError(f"{path}: invalid frontmatter fence structure") from exc
    data = yaml.safe_load(fm_text) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter must parse to a mapping")
    return data, body


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def file_sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(65536)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def append_missing_files(errors: list[str], repo_root: pathlib.Path, rel_paths: list[str]) -> None:
    for rel_path in rel_paths:
        if not (repo_root / rel_path).exists():
            errors.append(f"missing required file: {rel_path}")


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



@dataclass(frozen=True)
class ExportSurfaceDocuments:
    source_catalog: Any
    agent_catalog: Any
    agent_catalog_min: Any
    export_map: Any
    local_manifest: Any
    local_manifest_min: Any
    handoff_doc: Any
    runtime_doc: Any
    trust_doc: Any
    context_doc: Any
    resolved_profiles: Any
    resolved_kernel: Any
    kernel_governance: Any
    resolved_outer_ring: Any
    outer_ring_readiness: Any
    resolved_risk_ring: Any
    risk_ring_governance: Any
    foundation_profile: Any
    snippets_doc: Any
    mcp_doc: Any
    runtime_discovery: Any
    runtime_discovery_min: Any
    runtime_disclosure: Any
    runtime_aliases: Any
    runtime_tool_schemas: Any
    runtime_session_contract: Any
    runtime_prompt_blocks: Any
    runtime_router_hints: Any
    collision_doc: Any
    runtime_seam_manifest: Any
    guardrail_trust_gate: Any
    guardrail_allowlist: Any
    guardrail_context: Any
    guardrail_tool_schemas: Any
    guardrail_prompt_blocks: Any
    guardrail_manifest: Any
    description_signals: Any
    description_cases: Any
    description_manifest: Any
    skills_ref_manifest: Any
    support_manifest: Any
    support_index: Any
    support_schema_index: Any
    support_bridge_map: Any
    support_eval_cases: Any
    expected_support_dirs: Any
    tiny_router_signals: Any
    tiny_router_bands: Any
    tiny_router_capsules: Any
    tiny_router_eval_cases: Any
    tiny_router_manifest: Any
    bundle_index: Any
    skill_graph: Any
    release_manifest: Any
    overrides_doc: Any
    profile_doc: Any
    kernel_doc: Any
    outer_ring_doc: Any
    risk_ring_doc: Any
    policy_doc: Any
    guardrail_policy: Any
    description_eval_policy: Any
    tiny_router_policy: Any



def load_export_surface_documents(repo_root: pathlib.Path) -> ExportSurfaceDocuments:
    generated_dir = repo_root / "generated"
    config_dir = repo_root / "config"
    return ExportSurfaceDocuments(
        source_catalog=load_json(generated_dir / "skill_catalog.min.json"),
        agent_catalog=load_json(generated_dir / "agent_skill_catalog.json"),
        agent_catalog_min=load_json(generated_dir / "agent_skill_catalog.min.json"),
        export_map=load_json(generated_dir / "portable_export_map.json"),
        local_manifest=load_json(generated_dir / "local_adapter_manifest.json"),
        local_manifest_min=load_json(generated_dir / "local_adapter_manifest.min.json"),
        handoff_doc=load_json(generated_dir / "skill_handoff_contracts.json"),
        runtime_doc=load_json(generated_dir / "skill_runtime_contracts.json"),
        trust_doc=load_json(generated_dir / "trust_policy_matrix.json"),
        context_doc=load_json(generated_dir / "context_retention_manifest.json"),
        resolved_profiles=load_json(generated_dir / "skill_pack_profiles.resolved.json"),
        resolved_kernel=load_json(generated_dir / "project_core_skill_kernel.min.json"),
        kernel_governance=load_json(generated_dir / "project_core_kernel_governance.min.json"),
        resolved_outer_ring=load_json(generated_dir / "project_core_outer_ring.min.json"),
        outer_ring_readiness=load_json(generated_dir / "project_core_outer_ring_readiness.min.json"),
        resolved_risk_ring=load_json(generated_dir / "project_risk_guard_ring.min.json"),
        risk_ring_governance=load_json(generated_dir / "project_risk_guard_ring_governance.min.json"),
        foundation_profile=load_json(generated_dir / "project_foundation_profile.min.json"),
        snippets_doc=load_json(generated_dir / "codex_config_snippets.json"),
        mcp_doc=load_json(generated_dir / "mcp_dependency_manifest.json"),
        runtime_discovery=load_json(generated_dir / "runtime_discovery_index.json"),
        runtime_discovery_min=load_json(generated_dir / "runtime_discovery_index.min.json"),
        runtime_disclosure=load_json(generated_dir / "runtime_disclosure_index.json"),
        runtime_aliases=load_json(generated_dir / "runtime_activation_aliases.json"),
        runtime_tool_schemas=load_json(generated_dir / "runtime_tool_schemas.json"),
        runtime_session_contract=load_json(generated_dir / "runtime_session_contract.json"),
        runtime_prompt_blocks=load_json(generated_dir / "runtime_prompt_blocks.json"),
        runtime_router_hints=load_json(generated_dir / "runtime_router_hints.json"),
        collision_doc=load_json(generated_dir / "skill_trigger_collision_matrix.json"),
        runtime_seam_manifest=load_json(generated_dir / "runtime_seam_manifest.json"),
        guardrail_trust_gate=load_json(generated_dir / "repo_trust_gate_manifest.json"),
        guardrail_allowlist=load_json(generated_dir / "permission_allowlist_manifest.json"),
        guardrail_context=load_json(generated_dir / "skill_context_guard_manifest.json"),
        guardrail_tool_schemas=load_json(generated_dir / "runtime_guardrail_tool_schemas.json"),
        guardrail_prompt_blocks=load_json(generated_dir / "runtime_guardrail_prompt_blocks.json"),
        guardrail_manifest=load_json(generated_dir / "runtime_guardrail_manifest.json"),
        description_signals=load_json(generated_dir / "skill_description_signals.json"),
        description_cases=load_jsonl(generated_dir / "description_trigger_eval_cases.jsonl"),
        description_manifest=load_json(generated_dir / "description_trigger_eval_manifest.json"),
        skills_ref_manifest=load_json(generated_dir / "skills_ref_validation_manifest.json"),
        support_manifest=load_json(generated_dir / "deterministic_resource_manifest.json"),
        support_index=load_json(generated_dir / "support_resource_index.json"),
        support_schema_index=load_json(generated_dir / "structured_output_schema_index.json"),
        support_bridge_map=load_json(generated_dir / "support_resource_bridge_map.json"),
        support_eval_cases=load_jsonl(generated_dir / "deterministic_resource_eval_cases.jsonl"),
        expected_support_dirs=load_json(generated_dir / "expected_existing_aoa_support_dirs.json"),
        tiny_router_signals=load_json(generated_dir / "tiny_router_skill_signals.json"),
        tiny_router_bands=load_json(generated_dir / "tiny_router_candidate_bands.json"),
        tiny_router_capsules=load_json(generated_dir / "tiny_router_capsules.min.json"),
        tiny_router_eval_cases=load_jsonl(generated_dir / "tiny_router_eval_cases.jsonl"),
        tiny_router_manifest=load_json(generated_dir / "tiny_router_overlay_manifest.json"),
        bundle_index=load_json(generated_dir / "skill_bundle_index.json"),
        skill_graph=load_json(generated_dir / "skill_graph.json"),
        release_manifest=load_json(generated_dir / "release_manifest.json"),
        overrides_doc=load_json(config_dir / "portable_skill_overrides.json"),
        profile_doc=load_json(config_dir / "skill_pack_profiles.json"),
        kernel_doc=load_json(config_dir / "project_core_skill_kernel.json"),
        outer_ring_doc=load_json(config_dir / "project_core_outer_ring.json"),
        risk_ring_doc=load_json(config_dir / "project_risk_guard_ring.json"),
        policy_doc=load_json(config_dir / "skill_policy_matrix.json"),
        guardrail_policy=load_json(config_dir / "runtime_guardrail_policy.json"),
        description_eval_policy=load_json(config_dir / "description_trigger_eval_policy.json"),
        tiny_router_policy=load_json(config_dir / "tiny_router_skill_bands.json"),
    )


@dataclass(frozen=True)
class ExportSurfaceIndexes:
    source_by_name: Any
    agent_by_name: Any
    agent_min_by_name: Any
    export_by_name: Any
    manifest_by_name: Any
    manifest_min_by_name: Any
    handoff_by_name: Any
    runtime_by_name: Any
    trust_by_name: Any
    context_by_name: Any
    mcp_by_name: Any
    discovery_by_name: Any
    discovery_min_by_name: Any
    disclosure_by_name: Any
    router_by_name: Any
    alias_by_name: Any
    guardrail_trust_by_name: Any
    guardrail_allowlist_by_name: Any
    guardrail_context_by_name: Any
    description_signal_by_name: Any
    description_manifest_by_name: Any
    skills_ref_target_by_name: Any
    support_manifest_by_name: Any
    support_index_by_name: Any
    support_bridge_by_name: Any
    expected_support_by_name: Any
    tiny_router_signal_by_name: Any
    tiny_router_capsule_by_name: Any
    tiny_router_manifest_by_name: Any
    tiny_router_band_by_id: Any
    description_cases_by_skill: Any
    description_families_by_skill: Any
    description_neighbors_by_skill: Any



def build_export_surface_indexes(docs: ExportSurfaceDocuments) -> ExportSurfaceIndexes:
    source_by_name = {entry["name"]: entry for entry in docs.source_catalog.get("skills", [])}
    agent_by_name = {entry["name"]: entry for entry in docs.agent_catalog.get("skills", [])}
    agent_min_by_name = {entry["name"]: entry for entry in docs.agent_catalog_min.get("skills", [])}
    export_by_name = {entry["name"]: entry for entry in docs.export_map.get("exports", [])}
    manifest_by_name = {entry["name"]: entry for entry in docs.local_manifest.get("skills", [])}
    manifest_min_by_name = {entry["name"]: entry for entry in docs.local_manifest_min.get("skills", [])}
    handoff_by_name = {entry["name"]: entry for entry in docs.handoff_doc.get("skills", [])}
    runtime_by_name = {entry["name"]: entry for entry in docs.runtime_doc.get("skills", [])}
    trust_by_name = {entry["name"]: entry for entry in docs.trust_doc.get("skills", [])}
    context_by_name = {entry["name"]: entry for entry in docs.context_doc.get("skills", [])}
    mcp_by_name = {entry["name"]: entry for entry in docs.mcp_doc.get("skills", [])}
    discovery_by_name = {entry["name"]: entry for entry in docs.runtime_discovery.get("skills", [])}
    discovery_min_by_name = {entry["name"]: entry for entry in docs.runtime_discovery_min.get("skills", [])}
    disclosure_by_name = {entry["name"]: entry for entry in docs.runtime_disclosure.get("skills", [])}
    router_by_name = {entry["name"]: entry for entry in docs.runtime_router_hints.get("skills", [])}
    alias_by_name = {entry["name"]: entry for entry in docs.runtime_aliases.get("aliases", [])}
    guardrail_trust_by_name = {entry["name"]: entry for entry in docs.guardrail_trust_gate.get("skills", [])}
    guardrail_allowlist_by_name = {entry["name"]: entry for entry in docs.guardrail_allowlist.get("skills", [])}
    guardrail_context_by_name = {entry["name"]: entry for entry in docs.guardrail_context.get("skills", [])}
    description_signal_by_name = {entry["name"]: entry for entry in docs.description_signals.get("skills", [])}
    description_manifest_by_name = {entry["name"]: entry for entry in docs.description_manifest.get("skills", [])}
    skills_ref_target_by_name = {entry["skill_name"]: entry for entry in docs.skills_ref_manifest.get("targets", [])}
    support_manifest_by_name = {entry["name"]: entry for entry in docs.support_manifest.get("skills", [])}
    support_index_by_name = {entry["name"]: entry for entry in docs.support_index.get("skills", [])}
    support_bridge_by_name = docs.support_bridge_map.get("skills", {})
    expected_support_by_name = docs.expected_support_dirs.get("skills", {})
    tiny_router_signal_by_name = {entry["name"]: entry for entry in docs.tiny_router_signals.get("skills", [])}
    tiny_router_capsule_by_name = {entry["name"]: entry for entry in docs.tiny_router_capsules.get("skills", [])}
    tiny_router_manifest_by_name = {entry["name"]: entry for entry in docs.tiny_router_manifest.get("skills", [])}
    tiny_router_band_by_id = {entry["id"]: entry for entry in docs.tiny_router_bands.get("bands", [])}
    description_cases_by_skill: dict[str, list[dict[str, Any]]] = {
        name: [] for name in source_by_name
    }
    for case in docs.description_cases:
        skill_name = case.get("skill_name")
        if skill_name in description_cases_by_skill:
            description_cases_by_skill[skill_name].append(case)
    description_families_by_skill: dict[str, list[str]] = {
        name: [] for name in source_by_name
    }
    description_neighbors_by_skill: dict[str, set[str]] = {
        name: set() for name in source_by_name
    }
    for family in docs.collision_doc.get("families", []):
        members = family.get("skills", [])
        for skill_name in members:
            description_families_by_skill.setdefault(skill_name, []).append(family["family"])
            description_neighbors_by_skill.setdefault(skill_name, set()).update(
                name for name in members if name != skill_name
            )
    for collision_case in docs.collision_doc.get("cases", []):
        skill_name = collision_case.get("skill_name")
        competing = collision_case.get("competing_skills", [])
        description_neighbors_by_skill.setdefault(skill_name, set()).update(competing)
        for competing_skill in competing:
            description_neighbors_by_skill.setdefault(competing_skill, set()).add(skill_name)
            description_neighbors_by_skill.setdefault(competing_skill, set()).update(
                name for name in competing if name != competing_skill
            )
    return ExportSurfaceIndexes(
        source_by_name=source_by_name,
        agent_by_name=agent_by_name,
        agent_min_by_name=agent_min_by_name,
        export_by_name=export_by_name,
        manifest_by_name=manifest_by_name,
        manifest_min_by_name=manifest_min_by_name,
        handoff_by_name=handoff_by_name,
        runtime_by_name=runtime_by_name,
        trust_by_name=trust_by_name,
        context_by_name=context_by_name,
        mcp_by_name=mcp_by_name,
        discovery_by_name=discovery_by_name,
        discovery_min_by_name=discovery_min_by_name,
        disclosure_by_name=disclosure_by_name,
        router_by_name=router_by_name,
        alias_by_name=alias_by_name,
        guardrail_trust_by_name=guardrail_trust_by_name,
        guardrail_allowlist_by_name=guardrail_allowlist_by_name,
        guardrail_context_by_name=guardrail_context_by_name,
        description_signal_by_name=description_signal_by_name,
        description_manifest_by_name=description_manifest_by_name,
        skills_ref_target_by_name=skills_ref_target_by_name,
        support_manifest_by_name=support_manifest_by_name,
        support_index_by_name=support_index_by_name,
        support_bridge_by_name=support_bridge_by_name,
        expected_support_by_name=expected_support_by_name,
        tiny_router_signal_by_name=tiny_router_signal_by_name,
        tiny_router_capsule_by_name=tiny_router_capsule_by_name,
        tiny_router_manifest_by_name=tiny_router_manifest_by_name,
        tiny_router_band_by_id=tiny_router_band_by_id,
        description_cases_by_skill=description_cases_by_skill,
        description_families_by_skill=description_families_by_skill,
        description_neighbors_by_skill=description_neighbors_by_skill,
    )

@dataclass(frozen=True)
class ValidationResult:
    errors: list[str]
    validated_skill_count: int
    skills_root: pathlib.Path


def validate_profile_markers(docs: ExportSurfaceDocuments, errors: list[str]) -> None:
    if docs.overrides_doc.get("profile") != EXPORT_PROFILE:
        errors.append(f"config/portable_skill_overrides.json profile must be {EXPORT_PROFILE!r}")
    if docs.resolved_profiles.get("profile") != EXPORT_PROFILE:
        errors.append(f"generated/skill_pack_profiles.resolved.json profile must be {EXPORT_PROFILE!r}")
    if docs.snippets_doc.get("profile") != EXPORT_PROFILE:
        errors.append(f"generated/codex_config_snippets.json profile must be {EXPORT_PROFILE!r}")
    if docs.release_manifest.get("profile") != EXPORT_PROFILE:
        errors.append(f"generated/release_manifest.json profile must be {EXPORT_PROFILE!r}")
    if docs.handoff_doc.get("profile") != EXPORT_PROFILE:
        errors.append(f"generated/skill_handoff_contracts.json profile must be {EXPORT_PROFILE!r}")
    for label, doc in {
        "generated/runtime_discovery_index.json": docs.runtime_discovery,
        "generated/runtime_discovery_index.min.json": docs.runtime_discovery_min,
        "generated/runtime_disclosure_index.json": docs.runtime_disclosure,
        "generated/runtime_activation_aliases.json": docs.runtime_aliases,
        "generated/runtime_tool_schemas.json": docs.runtime_tool_schemas,
        "generated/runtime_session_contract.json": docs.runtime_session_contract,
        "generated/runtime_prompt_blocks.json": docs.runtime_prompt_blocks,
        "generated/runtime_router_hints.json": docs.runtime_router_hints,
        "generated/runtime_seam_manifest.json": docs.runtime_seam_manifest,
    }.items():
        if doc.get("profile") != RUNTIME_PROFILE:
            errors.append(f"{label} profile must be {RUNTIME_PROFILE!r}")
    for label, doc in {
        "config/runtime_guardrail_policy.json": docs.guardrail_policy,
        "generated/repo_trust_gate_manifest.json": docs.guardrail_trust_gate,
        "generated/permission_allowlist_manifest.json": docs.guardrail_allowlist,
        "generated/skill_context_guard_manifest.json": docs.guardrail_context,
        "generated/runtime_guardrail_tool_schemas.json": docs.guardrail_tool_schemas,
        "generated/runtime_guardrail_prompt_blocks.json": docs.guardrail_prompt_blocks,
        "generated/runtime_guardrail_manifest.json": docs.guardrail_manifest,
    }.items():
        if doc.get("profile") != GUARDRAIL_PROFILE:
            errors.append(f"{label} profile must be {GUARDRAIL_PROFILE!r}")
    for label, doc in {
        "config/description_trigger_eval_policy.json": docs.description_eval_policy,
        "generated/skill_description_signals.json": docs.description_signals,
        "generated/description_trigger_eval_manifest.json": docs.description_manifest,
    }.items():
        if doc.get("profile") != DESCRIPTION_TRIGGER_PROFILE:
            errors.append(f"{label} profile must be {DESCRIPTION_TRIGGER_PROFILE!r}")
    if docs.skills_ref_manifest.get("profile") != SKILLS_REF_PROFILE:
        errors.append(f"generated/skills_ref_validation_manifest.json profile must be {SKILLS_REF_PROFILE!r}")
    for label, doc in {
        "generated/deterministic_resource_manifest.json": docs.support_manifest,
        "generated/support_resource_index.json": docs.support_index,
        "generated/structured_output_schema_index.json": docs.support_schema_index,
        "generated/support_resource_bridge_map.json": docs.support_bridge_map,
        "generated/expected_existing_aoa_support_dirs.json": docs.expected_support_dirs,
    }.items():
        if doc.get("profile") != SUPPORT_RESOURCE_PROFILE:
            errors.append(f"{label} profile must be {SUPPORT_RESOURCE_PROFILE!r}")
    for label, doc in {
        "config/tiny_router_skill_bands.json": docs.tiny_router_policy,
        "generated/tiny_router_skill_signals.json": docs.tiny_router_signals,
        "generated/tiny_router_candidate_bands.json": docs.tiny_router_bands,
        "generated/tiny_router_capsules.min.json": docs.tiny_router_capsules,
        "generated/tiny_router_overlay_manifest.json": docs.tiny_router_manifest,
    }.items():
        if doc.get("profile") != TINY_ROUTER_PROFILE:
            errors.append(f"{label} profile must be {TINY_ROUTER_PROFILE!r}")



def discover_exported_skill_names(skills_root: pathlib.Path, errors: list[str]) -> set[str]:
    if not skills_root.exists():
        errors.append(f"missing skills root: {skills_root}")
        return set()
    return {path.name for path in skills_root.iterdir() if path.is_dir()}


def validate_export_skill_sets(
    docs: ExportSurfaceDocuments,
    indexes: ExportSurfaceIndexes,
    actual_names: set[str],
    errors: list[str],
) -> None:
    expected_sets = {
        "generated/skill_catalog.min.json": set(indexes.source_by_name),
        "generated/agent_skill_catalog.json": set(indexes.agent_by_name),
        "generated/agent_skill_catalog.min.json": set(indexes.agent_min_by_name),
        "generated/portable_export_map.json": set(indexes.export_by_name),
        "generated/local_adapter_manifest.json": set(indexes.manifest_by_name),
        "generated/local_adapter_manifest.min.json": set(indexes.manifest_min_by_name),
        "generated/skill_handoff_contracts.json": set(indexes.handoff_by_name),
        "generated/skill_runtime_contracts.json": set(indexes.runtime_by_name),
        "generated/trust_policy_matrix.json": set(indexes.trust_by_name),
        "generated/context_retention_manifest.json": set(indexes.context_by_name),
        "generated/mcp_dependency_manifest.json": set(indexes.mcp_by_name),
        "generated/runtime_discovery_index.json": set(indexes.discovery_by_name),
        "generated/runtime_discovery_index.min.json": set(indexes.discovery_min_by_name),
        "generated/runtime_disclosure_index.json": set(indexes.disclosure_by_name),
        "generated/runtime_router_hints.json": set(indexes.router_by_name),
        "generated/runtime_activation_aliases.json": set(indexes.alias_by_name),
        "generated/repo_trust_gate_manifest.json": set(indexes.guardrail_trust_by_name),
        "generated/permission_allowlist_manifest.json": set(indexes.guardrail_allowlist_by_name),
        "generated/skill_context_guard_manifest.json": set(indexes.guardrail_context_by_name),
        "generated/skill_description_signals.json": set(indexes.description_signal_by_name),
        "generated/description_trigger_eval_manifest.json": set(indexes.description_manifest_by_name),
        "generated/skills_ref_validation_manifest.json": set(indexes.skills_ref_target_by_name),
        "generated/tiny_router_skill_signals.json": set(indexes.tiny_router_signal_by_name),
        "generated/tiny_router_capsules.min.json": set(indexes.tiny_router_capsule_by_name),
        "generated/tiny_router_overlay_manifest.json": set(indexes.tiny_router_manifest_by_name),
        "config/skill_policy_matrix.json": set((docs.policy_doc.get("skills") or {}).keys()),
        "config/tiny_router_skill_bands.json": set((docs.tiny_router_policy.get("skill_overrides") or {}).keys()),
    }
    for label, names in expected_sets.items():
        if names != actual_names:
            errors.append(f"{label} skill set {sorted(names)!r} does not match export {sorted(actual_names)!r}")
    if set(indexes.support_manifest_by_name) != TARGETED_SUPPORT_SKILLS:
        errors.append("generated/deterministic_resource_manifest.json skill set mismatch for wave-8 targeted skills")
    if set(indexes.support_index_by_name) != TARGETED_SUPPORT_SKILLS:
        errors.append("generated/support_resource_index.json skill set mismatch for wave-8 targeted skills")
    if set(indexes.support_bridge_by_name) != TARGETED_SUPPORT_SKILLS:
        errors.append("generated/support_resource_bridge_map.json skill set mismatch for wave-8 targeted skills")
    if set(indexes.expected_support_by_name) != TARGETED_SUPPORT_SKILLS:
        errors.append("generated/expected_existing_aoa_support_dirs.json skill set mismatch for wave-8 targeted skills")
    if {case.get('skill_name') for case in docs.support_eval_cases} != TARGETED_SUPPORT_SKILLS:
        errors.append("generated/deterministic_resource_eval_cases.jsonl skill set mismatch for wave-8 targeted skills")
    tiny_band_skill_names = {
        skill_name
        for band_entry in docs.tiny_router_bands.get("bands", [])
        for skill_name in band_entry.get("skills", [])
    }
    if tiny_band_skill_names != actual_names:
        errors.append("generated/tiny_router_candidate_bands.json aggregated skill set mismatch")



def validate_exported_resource_surfaces(repo_root: pathlib.Path, skill_dir: pathlib.Path, indexes: ExportSurfaceIndexes, agent_entry: Any, export_entry: Any, manifest_entry: Any, errors: list[str]) -> None:
    source_skill_root = skill_layout.skill_dir_path(repo_root, skill_dir.name)
    for dirname in ("checks", "examples"):
        canonical_dir = source_skill_root / dirname
        if not canonical_dir.exists():
            continue
        exported_dir = skill_dir / dirname
        if not exported_dir.exists():
            errors.append(f"{skill_dir}: missing exported {dirname}/ from canonical source")
            continue
        expected_inventory = sorted(
            f"{dirname}/{path.relative_to(canonical_dir).as_posix()}"
            for path in canonical_dir.rglob("*")
            if path.is_file()
        )
        actual_inventory = sorted(
            str(path.relative_to(skill_dir).as_posix())
            for path in exported_dir.rglob("*")
            if path.is_file()
        )
        if actual_inventory != expected_inventory:
            errors.append(f"{skill_dir}: exported {dirname}/ inventory does not match canonical source")
        for owner_label, owner_entry in {
            "generated/agent_skill_catalog.json": agent_entry,
            "generated/portable_export_map.json": export_entry,
            "generated/local_adapter_manifest.json": manifest_entry,
        }.items():
            if owner_entry is None:
                continue
            resource_inventory = owner_entry.get("resource_inventory", {})
            if resource_inventory.get(dirname) != expected_inventory:
                errors.append(f"{owner_label} {dirname} resource inventory mismatch for {skill_dir.name}")

    if skill_dir.name in TARGETED_SUPPORT_SKILLS:
        support_manifest_entry = indexes.support_manifest_by_name.get(skill_dir.name)
        support_index_entry = indexes.support_index_by_name.get(skill_dir.name)
        support_bridge_entry = indexes.support_bridge_by_name.get(skill_dir.name)
        expected_support_entry = indexes.expected_support_by_name.get(skill_dir.name)
        if support_manifest_entry is None:
            errors.append(f"generated/deterministic_resource_manifest.json missing {skill_dir.name}")
        if support_index_entry is None:
            errors.append(f"generated/support_resource_index.json missing {skill_dir.name}")
        if support_bridge_entry is None:
            errors.append(f"generated/support_resource_bridge_map.json missing {skill_dir.name}")
        if expected_support_entry is None:
            errors.append(f"generated/expected_existing_aoa_support_dirs.json missing {skill_dir.name}")

        for dirname in SUPPORT_STANDARD_DIRS:
            canonical_dir = source_skill_root / dirname
            if not canonical_dir.exists():
                errors.append(f"{source_skill_root}: missing canonical {dirname}/")
                continue
            rel_paths = [path.relative_to(canonical_dir).as_posix() for path in sorted(p for p in canonical_dir.rglob('*') if p.is_file())]
            expected_inventory_paths = [f"{dirname}/{path}" for path in rel_paths]
            portable_dir = skill_dir / dirname
            if not portable_dir.exists():
                errors.append(f"{skill_dir}: missing portable support dir {dirname}/")
            else:
                for rel_path in rel_paths:
                    canonical_path = canonical_dir / rel_path
                    portable_path = portable_dir / rel_path
                    if not portable_path.exists():
                        errors.append(f"{skill_dir.name}: missing portable support file {dirname}/{rel_path}")
                    elif file_sha256(canonical_path) != file_sha256(portable_path):
                        errors.append(f"{skill_dir.name}: portable support drift in {dirname}/{rel_path}")

            if support_manifest_entry is not None:
                manifest_paths = [item["path"] for item in support_manifest_entry["standard_dirs"].get(dirname, [])]
                if manifest_paths != rel_paths:
                    errors.append(f"generated/deterministic_resource_manifest.json {skill_dir.name} {dirname} mismatch")
            if support_bridge_entry is not None and support_bridge_entry.get("standard_support_dirs", {}).get(dirname) != rel_paths:
                errors.append(f"generated/support_resource_bridge_map.json {skill_dir.name} {dirname} mismatch")
            if support_index_entry is not None and support_index_entry.get("standard_dir_counts", {}).get(dirname) != len(rel_paths):
                errors.append(f"generated/support_resource_index.json {skill_dir.name} {dirname} count mismatch")
            if manifest_entry is not None:
                inventory_paths = manifest_entry.get("resource_inventory", {}).get(dirname, [])
                for rel_path in expected_inventory_paths:
                    if rel_path not in inventory_paths:
                        errors.append(f"generated/local_adapter_manifest.json missing support resource {rel_path} for {skill_dir.name}")

        for dirname in SUPPORT_LEGACY_DIRS:
            canonical_dir = source_skill_root / dirname
            if not canonical_dir.exists():
                errors.append(f"{source_skill_root}: missing legacy {dirname}/")
                continue
            rel_paths = [path.relative_to(canonical_dir).as_posix() for path in sorted(p for p in canonical_dir.rglob('*') if p.is_file())]
            if expected_support_entry is not None and expected_support_entry.get(dirname) != rel_paths:
                errors.append(f"generated/expected_existing_aoa_support_dirs.json {skill_dir.name} {dirname} mismatch")
            if support_manifest_entry is not None:
                manifest_paths = [item["path"] for item in support_manifest_entry["legacy_dirs"].get(dirname, [])]
                if manifest_paths != rel_paths:
                    errors.append(f"generated/deterministic_resource_manifest.json legacy {dirname} mismatch for {skill_dir.name}")
            if support_bridge_entry is not None and support_bridge_entry.get("legacy_support_dirs", {}).get(dirname) != rel_paths:
                errors.append(f"generated/support_resource_bridge_map.json legacy {dirname} mismatch for {skill_dir.name}")
            if support_index_entry is not None and support_index_entry.get("legacy_dir_counts", {}).get(dirname) != len(rel_paths):
                errors.append(f"generated/support_resource_index.json legacy {dirname} count mismatch for {skill_dir.name}")



def validate_exported_runtime_catalog_surfaces(repo_root: pathlib.Path, skill_dir: pathlib.Path, skill_md: pathlib.Path, openai_yaml: pathlib.Path, indexes: ExportSurfaceIndexes, source_entry: Any, frontmatter: Any, manifest_entry: Any, dependency_tools: list[dict[str, Any]], allow_implicit: Any, activation_policy: str, description: Any, errors: list[str]) -> Any:
    handoff_entry = indexes.handoff_by_name.get(skill_dir.name)
    if handoff_entry is None:
        errors.append(f"generated/skill_handoff_contracts.json missing {skill_dir.name}")
    else:
        for field_name in (
            "inputs",
            "outputs",
            "verification",
            "contracts",
            "consumes_artifact_tags",
            "provides_artifact_tags",
        ):
            value = handoff_entry.get(field_name)
            if not isinstance(value, list):
                errors.append(
                    f"generated/skill_handoff_contracts.json {skill_dir.name} field {field_name!r} must be a list"
                )
                continue
            if any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(
                    f"generated/skill_handoff_contracts.json {skill_dir.name} field {field_name!r} must contain non-empty strings"
                )
        packet = handoff_entry.get("handoff_packet_template")
        if not isinstance(packet, dict):
            errors.append(
                f"generated/skill_handoff_contracts.json {skill_dir.name} handoff_packet_template must be a mapping"
            )
        else:
            if packet.get("from_skill") != skill_dir.name:
                errors.append(
                    f"generated/skill_handoff_contracts.json {skill_dir.name} handoff_packet_template.from_skill mismatch"
                )
            for field_name in ("produced_artifacts", "verification_notes", "contract_notes", "next_recommended_skills"):
                value = packet.get(field_name)
                if not isinstance(value, list):
                    errors.append(
                        f"generated/skill_handoff_contracts.json {skill_dir.name} handoff_packet_template.{field_name} must be a list"
                    )
                elif any(not isinstance(item, str) or not item.strip() for item in value):
                    errors.append(
                        f"generated/skill_handoff_contracts.json {skill_dir.name} handoff_packet_template.{field_name} must contain non-empty strings"
                    )

    runtime_entry = indexes.runtime_by_name.get(skill_dir.name)
    if runtime_entry is None:
        errors.append(f"generated/skill_runtime_contracts.json missing {skill_dir.name}")
    else:
        if runtime_entry.get("implicit_activation_policy") != activation_policy:
            errors.append(f"generated/skill_runtime_contracts.json implicit_activation_policy mismatch for {skill_dir.name}")
        if runtime_entry.get("allow_implicit_invocation") != allow_implicit:
            errors.append(f"generated/skill_runtime_contracts.json allow_implicit_invocation mismatch for {skill_dir.name}")
        if runtime_entry.get("manual_invocation_required") != (activation_policy != "invoke"):
            errors.append(f"generated/skill_runtime_contracts.json manual_invocation_required mismatch for {skill_dir.name}")
        if runtime_entry.get("candidate_only") != (activation_policy == "suggest"):
            errors.append(f"generated/skill_runtime_contracts.json candidate_only mismatch for {skill_dir.name}")
        if runtime_entry.get("context_retention_ref") != f"generated/context_retention_manifest.json#{skill_dir.name}":
            errors.append(f"generated/skill_runtime_contracts.json context_retention_ref mismatch for {skill_dir.name}")

    trust_entry = indexes.trust_by_name.get(skill_dir.name)
    if trust_entry is None:
        errors.append(f"generated/trust_policy_matrix.json missing {skill_dir.name}")
    else:
        if source_entry and trust_entry.get("invocation_mode") != source_entry.get("invocation_mode"):
            errors.append(f"generated/trust_policy_matrix.json invocation_mode mismatch for {skill_dir.name}")
        if trust_entry.get("implicit_activation_policy") != activation_policy:
            errors.append(f"generated/trust_policy_matrix.json implicit_activation_policy mismatch for {skill_dir.name}")
        requires_manual = activation_policy != "invoke"
        if trust_entry.get("requires_manual_invocation") != requires_manual:
            errors.append(f"generated/trust_policy_matrix.json requires_manual_invocation mismatch for {skill_dir.name}")
        if trust_entry.get("candidate_only") != (activation_policy == "suggest"):
            errors.append(f"generated/trust_policy_matrix.json candidate_only mismatch for {skill_dir.name}")

    context_entry = indexes.context_by_name.get(skill_dir.name)
    if context_entry is None:
        errors.append(f"generated/context_retention_manifest.json missing {skill_dir.name}")
    else:
        if not context_entry.get("retain_sections"):
            errors.append(f"generated/context_retention_manifest.json retain_sections missing for {skill_dir.name}")

    guardrail_trust_entry = indexes.guardrail_trust_by_name.get(skill_dir.name)
    if guardrail_trust_entry is None:
        errors.append(f"generated/repo_trust_gate_manifest.json missing {skill_dir.name}")
    else:
        if source_entry and guardrail_trust_entry.get("invocation_mode") != source_entry.get("invocation_mode"):
            errors.append(f"generated/repo_trust_gate_manifest.json invocation_mode mismatch for {skill_dir.name}")
        if trust_entry is not None and guardrail_trust_entry.get("trust_posture") != trust_entry.get("trust_posture"):
            errors.append(f"generated/repo_trust_gate_manifest.json trust_posture mismatch for {skill_dir.name}")
        if guardrail_trust_entry.get("source_scope") != "repo":
            errors.append(f"generated/repo_trust_gate_manifest.json source_scope mismatch for {skill_dir.name}")

    guardrail_allowlist_entry = indexes.guardrail_allowlist_by_name.get(skill_dir.name)
    if guardrail_allowlist_entry is None:
        errors.append(f"generated/permission_allowlist_manifest.json missing {skill_dir.name}")
    else:
        if guardrail_allowlist_entry.get("source_scope") != "repo":
            errors.append(f"generated/permission_allowlist_manifest.json source_scope mismatch for {skill_dir.name}")
        if guardrail_allowlist_entry.get("resource_inventory") != manifest_entry.get("resource_inventory"):
            errors.append(f"generated/permission_allowlist_manifest.json resource_inventory mismatch for {skill_dir.name}")
        if guardrail_allowlist_entry.get("allowlist_id") != f"skill:{skill_dir.name}":
            errors.append(f"generated/permission_allowlist_manifest.json allowlist_id mismatch for {skill_dir.name}")

    guardrail_context_entry = indexes.guardrail_context_by_name.get(skill_dir.name)
    if guardrail_context_entry is None:
        errors.append(f"generated/skill_context_guard_manifest.json missing {skill_dir.name}")
    else:
        if guardrail_context_entry.get("source_scope") != "repo":
            errors.append(f"generated/skill_context_guard_manifest.json source_scope mismatch for {skill_dir.name}")
        if context_entry is not None and guardrail_context_entry.get("must_keep") != context_entry.get("must_keep"):
            errors.append(f"generated/skill_context_guard_manifest.json must_keep mismatch for {skill_dir.name}")
        if context_entry is not None and guardrail_context_entry.get("retain_sections") != context_entry.get("retain_sections"):
            errors.append(f"generated/skill_context_guard_manifest.json retain_sections mismatch for {skill_dir.name}")
        if not isinstance(guardrail_context_entry.get("instruction_sha256"), str) or len(guardrail_context_entry["instruction_sha256"]) != 64:
            errors.append(f"generated/skill_context_guard_manifest.json instruction_sha256 mismatch for {skill_dir.name}")
        if guardrail_context_entry.get("dedupe_key") != f"{skill_dir.name}:{guardrail_context_entry.get('instruction_sha256')}":
            errors.append(f"generated/skill_context_guard_manifest.json dedupe_key mismatch for {skill_dir.name}")

    mcp_entry = indexes.mcp_by_name.get(skill_dir.name)
    if mcp_entry is None:
        errors.append(f"generated/mcp_dependency_manifest.json missing {skill_dir.name}")
    else:
        if mcp_entry.get("tools", []) != dependency_tools:
            errors.append(f"generated/mcp_dependency_manifest.json tools mismatch for {skill_dir.name}")

    discovery_entry = indexes.discovery_by_name.get(skill_dir.name)
    if discovery_entry is None:
        errors.append(f"generated/runtime_discovery_index.json missing {skill_dir.name}")
    else:
        if discovery_entry.get("path") != skill_md.relative_to(repo_root).as_posix():
            errors.append(f"generated/runtime_discovery_index.json path mismatch for {skill_dir.name}")
        if discovery_entry.get("allow_implicit_invocation") != allow_implicit:
            errors.append(f"generated/runtime_discovery_index.json allow_implicit_invocation mismatch for {skill_dir.name}")
        if discovery_entry.get("implicit_activation_policy") != activation_policy:
            errors.append(f"generated/runtime_discovery_index.json implicit_activation_policy mismatch for {skill_dir.name}")
        if discovery_entry.get("candidate_only") != (activation_policy == "suggest"):
            errors.append(f"generated/runtime_discovery_index.json candidate_only mismatch for {skill_dir.name}")
        if discovery_entry.get("invocation_mode") != frontmatter.get("metadata", {}).get("aoa_invocation_mode"):
            errors.append(f"generated/runtime_discovery_index.json invocation_mode mismatch for {skill_dir.name}")
        if "instructions_markdown" in discovery_entry:
            errors.append(f"generated/runtime_discovery_index.json must not expose instructions_markdown for {skill_dir.name}")
        if discovery_entry.get("explicit_handles", {}).get("codex", {}).get("mention") != f"${skill_dir.name}":
            errors.append(f"generated/runtime_discovery_index.json explicit handle mismatch for {skill_dir.name}")

    discovery_min_entry = indexes.discovery_min_by_name.get(skill_dir.name)
    if discovery_min_entry is None:
        errors.append(f"generated/runtime_discovery_index.min.json missing {skill_dir.name}")
    else:
        if discovery_min_entry.get("allow_implicit_invocation") != allow_implicit:
            errors.append(f"generated/runtime_discovery_index.min.json allow_implicit_invocation mismatch for {skill_dir.name}")
        if discovery_min_entry.get("implicit_activation_policy") != activation_policy:
            errors.append(f"generated/runtime_discovery_index.min.json implicit_activation_policy mismatch for {skill_dir.name}")

    disclosure_entry = indexes.disclosure_by_name.get(skill_dir.name)
    if disclosure_entry is None:
        errors.append(f"generated/runtime_disclosure_index.json missing {skill_dir.name}")
    else:
        if disclosure_entry.get("path") != skill_md.relative_to(repo_root).as_posix():
            errors.append(f"generated/runtime_disclosure_index.json path mismatch for {skill_dir.name}")
        if disclosure_entry.get("skill_dir") != skill_dir.relative_to(repo_root).as_posix():
            errors.append(f"generated/runtime_disclosure_index.json skill_dir mismatch for {skill_dir.name}")
        if "instructions_markdown" in disclosure_entry:
            errors.append(f"generated/runtime_disclosure_index.json must not expose instructions_markdown for {skill_dir.name}")
        if disclosure_entry.get("runtime_contract_ref") != f"generated/skill_runtime_contracts.json#{skill_dir.name}":
            errors.append(f"generated/runtime_disclosure_index.json runtime_contract_ref mismatch for {skill_dir.name}")
        if disclosure_entry.get("context_retention_ref") != f"generated/context_retention_manifest.json#{skill_dir.name}":
            errors.append(f"generated/runtime_disclosure_index.json context_retention_ref mismatch for {skill_dir.name}")
        if disclosure_entry.get("trust_policy_ref") != f"generated/trust_policy_matrix.json#{skill_dir.name}":
            errors.append(f"generated/runtime_disclosure_index.json trust_policy_ref mismatch for {skill_dir.name}")

    router_entry = indexes.router_by_name.get(skill_dir.name)
    if router_entry is None:
        errors.append(f"generated/runtime_router_hints.json missing {skill_dir.name}")
    else:
        if router_entry.get("description") != description:
            errors.append(f"generated/runtime_router_hints.json description mismatch for {skill_dir.name}")
        should_trigger = router_entry.get("should_trigger", [])
        manual_required = router_entry.get("manual_invocation_required", [])
        negative_controls = router_entry.get("negative_controls", [])
        overlap = (
            (set(should_trigger) & set(manual_required))
            | (set(should_trigger) & set(negative_controls))
            | (set(manual_required) & set(negative_controls))
        )
        if overlap:
            errors.append(
                "generated/runtime_router_hints.json routing buckets must be disjoint "
                f"for {skill_dir.name}: {sorted(overlap)!r}"
            )

    alias_entry = indexes.alias_by_name.get(skill_dir.name)
    if alias_entry is None:
        errors.append(f"generated/runtime_activation_aliases.json missing {skill_dir.name}")
    else:
        if alias_entry.get("codex_mention") != f"${skill_dir.name}":
            errors.append(f"generated/runtime_activation_aliases.json codex_mention mismatch for {skill_dir.name}")
        if alias_entry.get("tool_call", {}).get("arguments", {}).get("skill_name") != skill_dir.name:
            errors.append(f"generated/runtime_activation_aliases.json tool_call mismatch for {skill_dir.name}")

    return router_entry


def validate_exported_description_router_surfaces(docs: ExportSurfaceDocuments, indexes: ExportSurfaceIndexes, skill_dir: pathlib.Path, description: Any, source_scope: Any, source_invocation_mode: Any, allow_implicit: Any, activation_policy: str, router_entry: Any, errors: list[str]) -> None:
    description_signal = indexes.description_signal_by_name.get(skill_dir.name)
    description_manifest_entry = indexes.description_manifest_by_name.get(skill_dir.name)
    skills_ref_target = indexes.skills_ref_target_by_name.get(skill_dir.name)
    skill_description_cases = indexes.description_cases_by_skill.get(skill_dir.name, [])
    if description_signal is None:
        errors.append(f"generated/skill_description_signals.json missing {skill_dir.name}")
    else:
        description_sha = hashlib.sha256(description.encode("utf-8")).hexdigest()
        expected_families = sorted(indexes.description_families_by_skill.get(skill_dir.name, []))
        expected_family = expected_families[0] if expected_families else None
        if description_signal.get("description") != description:
            errors.append(f"generated/skill_description_signals.json description mismatch for {skill_dir.name}")
        if description_signal.get("description_sha256") != description_sha:
            errors.append(f"generated/skill_description_signals.json description_sha256 mismatch for {skill_dir.name}")
        if description_signal.get("invocation_mode") != source_invocation_mode:
            errors.append(f"generated/skill_description_signals.json invocation_mode mismatch for {skill_dir.name}")
        if description_signal.get("implicit_activation_policy") != activation_policy:
            errors.append(f"generated/skill_description_signals.json implicit_activation_policy mismatch for {skill_dir.name}")
        if description_signal.get("allow_implicit_invocation") != allow_implicit:
            errors.append(f"generated/skill_description_signals.json allow_implicit_invocation mismatch for {skill_dir.name}")
        if description_signal.get("family") != expected_family:
            errors.append(f"generated/skill_description_signals.json family mismatch for {skill_dir.name}")
        if set(description_signal.get("families", [])) != set(expected_families):
            errors.append(f"generated/skill_description_signals.json families mismatch for {skill_dir.name}")
        if set(description_signal.get("adjacent_skills", [])) != indexes.description_neighbors_by_skill.get(skill_dir.name, set()):
            errors.append(f"generated/skill_description_signals.json adjacent_skills mismatch for {skill_dir.name}")
        if "Use when" in description and not description_signal.get("use_when_clause"):
            errors.append(f"generated/skill_description_signals.json missing use_when_clause for {skill_dir.name}")
        if "Do not use" in description and not description_signal.get("do_not_use_clause"):
            errors.append(f"generated/skill_description_signals.json missing do_not_use_clause for {skill_dir.name}")

    if description_manifest_entry is None:
        errors.append(f"generated/description_trigger_eval_manifest.json missing {skill_dir.name}")
    else:
        try:
            required_classes = list(
                activation_required_case_classes(
                    docs.description_eval_policy,
                    activation_policy=activation_policy,
                    invocation_mode=str(source_invocation_mode),
                )
            )
        except ValueError as exc:
            errors.append(
                f"generated/description_trigger_eval_manifest.json cannot resolve required_case_classes for {skill_dir.name}: {exc}"
            )
            required_classes = []
        if description_manifest_entry.get("implicit_activation_policy") != activation_policy:
            errors.append(f"generated/description_trigger_eval_manifest.json implicit_activation_policy mismatch for {skill_dir.name}")
        if required_classes and description_manifest_entry.get("required_case_classes") != required_classes:
            errors.append(f"generated/description_trigger_eval_manifest.json required_case_classes mismatch for {skill_dir.name}")
        if description_signal is not None and description_manifest_entry.get("description_sha256") != description_signal.get("description_sha256"):
            errors.append(f"generated/description_trigger_eval_manifest.json description_sha256 mismatch for {skill_dir.name}")
        if description_manifest_entry.get("coverage_ok") is not True:
            errors.append(f"generated/description_trigger_eval_manifest.json coverage_ok mismatch for {skill_dir.name}")
        if description_manifest_entry.get("total_cases") != len(skill_description_cases):
            errors.append(f"generated/description_trigger_eval_manifest.json total_cases mismatch for {skill_dir.name}")

    if skills_ref_target is None:
        errors.append(f"generated/skills_ref_validation_manifest.json missing {skill_dir.name}")
    else:
        if skills_ref_target.get("path") != f".agents/skills/{skill_dir.name}":
            errors.append(f"generated/skills_ref_validation_manifest.json path mismatch for {skill_dir.name}")
        if skills_ref_target.get("command") != ["skills-ref", "validate", f".agents/skills/{skill_dir.name}"]:
            errors.append(f"generated/skills_ref_validation_manifest.json command mismatch for {skill_dir.name}")
        if description_signal is not None and skills_ref_target.get("description_sha256") != description_signal.get("description_sha256"):
            errors.append(f"generated/skills_ref_validation_manifest.json description_sha256 mismatch for {skill_dir.name}")

    tiny_router_signal = indexes.tiny_router_signal_by_name.get(skill_dir.name)
    tiny_router_capsule = indexes.tiny_router_capsule_by_name.get(skill_dir.name)
    tiny_router_manifest_entry = indexes.tiny_router_manifest_by_name.get(skill_dir.name)
    if tiny_router_signal is None:
        errors.append(f"generated/tiny_router_skill_signals.json missing {skill_dir.name}")
    else:
        expected_band = docs.tiny_router_policy["skill_overrides"][skill_dir.name]["band"]
        if tiny_router_signal.get("band") != expected_band:
            errors.append(f"generated/tiny_router_skill_signals.json band mismatch for {skill_dir.name}")
        if tiny_router_signal.get("invocation_mode") != source_invocation_mode:
            errors.append(f"generated/tiny_router_skill_signals.json invocation_mode mismatch for {skill_dir.name}")
        if tiny_router_signal.get("implicit_activation_policy") != activation_policy:
            errors.append(f"generated/tiny_router_skill_signals.json implicit_activation_policy mismatch for {skill_dir.name}")
        if tiny_router_signal.get("allow_implicit_invocation") != allow_implicit:
            errors.append(f"generated/tiny_router_skill_signals.json allow_implicit_invocation mismatch for {skill_dir.name}")
        if tiny_router_signal.get("manual_invocation_required") != (activation_policy != "invoke"):
            errors.append(f"generated/tiny_router_skill_signals.json manual_invocation_required mismatch for {skill_dir.name}")
        if tiny_router_signal.get("candidate_only") != (activation_policy == "suggest"):
            errors.append(f"generated/tiny_router_skill_signals.json candidate_only mismatch for {skill_dir.name}")
        if tiny_router_signal.get("project_overlay") != (source_scope == "project"):
            errors.append(f"generated/tiny_router_skill_signals.json project_overlay mismatch for {skill_dir.name}")
        if tiny_router_signal.get("description") != description:
            errors.append(f"generated/tiny_router_skill_signals.json description mismatch for {skill_dir.name}")
        if description_signal is not None and tiny_router_signal.get("description_sha256") != description_signal.get("description_sha256"):
            errors.append(f"generated/tiny_router_skill_signals.json description_sha256 mismatch for {skill_dir.name}")
        if tiny_router_signal.get("companions") != docs.tiny_router_policy.get("companions", {}).get(skill_dir.name, []):
            errors.append(f"generated/tiny_router_skill_signals.json companions mismatch for {skill_dir.name}")
        if len(tiny_router_signal.get("positive_cues", [])) < 3:
            errors.append(f"generated/tiny_router_skill_signals.json must keep at least 3 positive cues for {skill_dir.name}")
        if not tiny_router_signal.get("cue_tokens"):
            errors.append(f"generated/tiny_router_skill_signals.json must keep cue_tokens for {skill_dir.name}")

    if tiny_router_capsule is None:
        errors.append(f"generated/tiny_router_capsules.min.json missing {skill_dir.name}")
    else:
        expected_band = docs.tiny_router_policy["skill_overrides"][skill_dir.name]["band"]
        if tiny_router_capsule.get("band") != expected_band:
            errors.append(f"generated/tiny_router_capsules.min.json band mismatch for {skill_dir.name}")
        if tiny_router_capsule.get("implicit_activation_policy") != activation_policy:
            errors.append(f"generated/tiny_router_capsules.min.json implicit_activation_policy mismatch for {skill_dir.name}")
        if tiny_router_capsule.get("manual_invocation_required") != (activation_policy != "invoke"):
            errors.append(f"generated/tiny_router_capsules.min.json manual_invocation_required mismatch for {skill_dir.name}")
        if tiny_router_capsule.get("candidate_only") != (activation_policy == "suggest"):
            errors.append(f"generated/tiny_router_capsules.min.json candidate_only mismatch for {skill_dir.name}")
        if tiny_router_capsule.get("project_overlay") != (source_scope == "project"):
            errors.append(f"generated/tiny_router_capsules.min.json project_overlay mismatch for {skill_dir.name}")
        if description_signal is not None and tiny_router_capsule.get("description_sha256") != description_signal.get("description_sha256"):
            errors.append(f"generated/tiny_router_capsules.min.json description_sha256 mismatch for {skill_dir.name}")

    if tiny_router_manifest_entry is None:
        errors.append(f"generated/tiny_router_overlay_manifest.json missing {skill_dir.name}")
    else:
        expected_band = docs.tiny_router_policy["skill_overrides"][skill_dir.name]["band"]
        if tiny_router_manifest_entry.get("band") != expected_band:
            errors.append(f"generated/tiny_router_overlay_manifest.json band mismatch for {skill_dir.name}")
        if tiny_router_manifest_entry.get("implicit_activation_policy") != activation_policy:
            errors.append(f"generated/tiny_router_overlay_manifest.json implicit_activation_policy mismatch for {skill_dir.name}")
        if tiny_router_manifest_entry.get("manual_invocation_required") != (activation_policy != "invoke"):
            errors.append(f"generated/tiny_router_overlay_manifest.json manual_invocation_required mismatch for {skill_dir.name}")
        if tiny_router_manifest_entry.get("candidate_only") != (activation_policy == "suggest"):
            errors.append(f"generated/tiny_router_overlay_manifest.json candidate_only mismatch for {skill_dir.name}")
        if tiny_router_manifest_entry.get("project_overlay") != (source_scope == "project"):
            errors.append(f"generated/tiny_router_overlay_manifest.json project_overlay mismatch for {skill_dir.name}")
        if description_signal is not None and tiny_router_manifest_entry.get("description_sha256") != description_signal.get("description_sha256"):
            errors.append(f"generated/tiny_router_overlay_manifest.json description_sha256 mismatch for {skill_dir.name}")

    class_totals: dict[str, int] = {}
    for case in skill_description_cases:
        class_totals[case["case_class"]] = class_totals.get(case["case_class"], 0) + 1
        if description_signal is not None and case.get("description_sha256") != description_signal.get("description_sha256"):
            errors.append(f"{case['case_id']}: description trigger case hash mismatch for {skill_dir.name}")
        if case.get("implicit_activation_policy") != activation_policy:
            errors.append(f"{case['case_id']}: description trigger activation policy mismatch for {skill_dir.name}")
        if case.get("case_class") == "should-trigger" and activation_policy != "invoke":
            errors.append(f"{case['case_id']}: non-invoke skill must not have should-trigger cases")
        if case.get("case_class") == "prefer-other-skill":
            expected_skill = case.get("expected_skill")
            if expected_skill == skill_dir.name:
                errors.append(f"{case['case_id']}: prefer-other-skill must defer to another skill")
    try:
        required_classes = list(
            activation_required_case_classes(
                docs.description_eval_policy,
                activation_policy=activation_policy,
                invocation_mode=str(source_invocation_mode),
            )
        )
    except ValueError as exc:
        errors.append(f"{skill_dir.name}: unknown description-trigger coverage policy: {exc}")
        required_classes = []
    for case_class in required_classes:
        if class_totals.get(case_class, 0) < 1:
            errors.append(f"{skill_dir.name}: missing description-trigger class {case_class!r}")
    if router_entry is not None and router_entry.get("collision_family") and activation_policy != "manual":
        if class_totals.get("prefer-other-skill", 0) < 1:
            errors.append(f"{skill_dir.name}: missing mirrored defer coverage in description-trigger cases")


def validate_exported_skill_directory(
    repo_root: pathlib.Path,
    docs: ExportSurfaceDocuments,
    indexes: ExportSurfaceIndexes,
    errors: list[str],
    skill_dir: pathlib.Path,
) -> None:
    skill_md = skill_dir / "SKILL.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    small_icon = skill_dir / "assets" / "small-logo.svg"
    large_icon = skill_dir / "assets" / "large-logo.svg"
    if not skill_md.exists():
        errors.append(f"{skill_dir}: missing SKILL.md")
        return
    if not openai_yaml.exists():
        errors.append(f"{skill_dir}: missing agents/openai.yaml")
        return
    if not small_icon.exists() or not large_icon.exists():
        errors.append(f"{skill_dir}: missing icon assets")
        return

    try:
        frontmatter, body = parse_frontmatter(skill_md)
    except Exception as exc:  # noqa: BLE001
        errors.append(str(exc))
        return

    name = frontmatter.get("name")
    description = frontmatter.get("description")
    metadata = frontmatter.get("metadata")

    if name != skill_dir.name:
        errors.append(f"{skill_md}: frontmatter name {name!r} does not match directory {skill_dir.name!r}")
    if not isinstance(name, str) or not NAME_RE.match(name):
        errors.append(f"{skill_md}: invalid skill name {name!r}")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{skill_md}: missing or empty description")
    else:
        if len(description) > 1024:
            errors.append(f"{skill_md}: description exceeds 1024 characters")
        if "Use when" not in description:
            errors.append(f"{skill_md}: description should include 'Use when' for trigger clarity")
        if "Do not use" not in description:
            errors.append(f"{skill_md}: description should include 'Do not use' for boundary clarity")

    if not isinstance(metadata, dict):
        errors.append(f"{skill_md}: metadata must be a mapping")
    else:
        if set(metadata) != REQUIRED_METADATA:
            errors.append(f"{skill_md}: metadata keys mismatch; got {sorted(metadata)!r}")
        if metadata.get("aoa_portable_profile") != EXPORT_PROFILE:
            errors.append(f"{skill_md}: aoa_portable_profile must be {EXPORT_PROFILE!r}")
        for key, value in metadata.items():
            if not isinstance(key, str) or not isinstance(value, str):
                errors.append(f"{skill_md}: metadata keys and values must be strings")
                break

    if not body.strip():
        errors.append(f"{skill_md}: markdown body is empty")

    try:
        openai_doc = yaml.safe_load(openai_yaml.read_text(encoding="utf-8")) or {}
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{openai_yaml}: invalid YAML: {exc}")
        return
    if not isinstance(openai_doc, dict):
        errors.append(f"{openai_yaml}: top-level YAML must be a mapping")
        return

    interface = openai_doc.get("interface")
    if not isinstance(interface, dict):
        errors.append(f"{openai_yaml}: interface must be a mapping")
        interface = {}
    for key in ("display_name", "short_description", "default_prompt", "icon_small", "icon_large", "brand_color"):
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{openai_yaml}: interface.{key} must be a non-empty string")
    brand_color = interface.get("brand_color")
    if isinstance(brand_color, str) and not HEX_COLOR_RE.match(brand_color):
        errors.append(f"{openai_yaml}: interface.brand_color must be a #RRGGBB string")
    default_prompt = interface.get("default_prompt")
    if isinstance(default_prompt, str) and f"${skill_dir.name}" not in default_prompt:
        errors.append(f"{openai_yaml}: interface.default_prompt must mention ${skill_dir.name}")
    for icon_key in ("icon_small", "icon_large"):
        icon_rel = interface.get(icon_key)
        if isinstance(icon_rel, str):
            icon_path = skill_dir / icon_rel.replace("./", "", 1)
            if not icon_path.exists():
                errors.append(f"{openai_yaml}: {icon_key} path does not exist: {icon_rel}")

    policy = openai_doc.get("policy")
    if not isinstance(policy, dict):
        errors.append(f"{openai_yaml}: policy must be a mapping")
        policy = {}
    allow_implicit = policy.get("allow_implicit_invocation")
    if not isinstance(allow_implicit, bool):
        errors.append(f"{openai_yaml}: policy.allow_implicit_invocation must be a boolean")
    policy_matrix_entry = (docs.policy_doc.get("skills") or {}).get(skill_dir.name)
    try:
        activation_policy = resolve_implicit_activation_policy(
            policy_matrix_entry,
            skill_dir.name,
        )
        expected_allow = allow_implicit_invocation(policy_matrix_entry, skill_dir.name)
    except ValueError as exc:
        errors.append(str(exc))
        activation_policy = "manual"
        expected_allow = False
    if policy.get("implicit_activation_policy") != activation_policy:
        errors.append(
            f"{openai_yaml}: policy.implicit_activation_policy does not match config/skill_policy_matrix.json"
        )

    dependency_tools: list[dict[str, Any]] = []
    dependencies = openai_doc.get("dependencies", {})
    if dependencies is not None:
        if not isinstance(dependencies, dict):
            errors.append(f"{openai_yaml}: dependencies must be a mapping when present")
        else:
            tools = dependencies.get("tools", [])
            if tools is not None:
                if not isinstance(tools, list):
                    errors.append(f"{openai_yaml}: dependencies.tools must be a list when present")
                else:
                    dependency_tools = tools
                    for idx, tool in enumerate(tools):
                        if not isinstance(tool, dict):
                            errors.append(f"{openai_yaml}: dependencies.tools[{idx}] must be a mapping")
                            break
                        if not isinstance(tool.get("type"), str) or not tool["type"].strip():
                            errors.append(f"{openai_yaml}: dependencies.tools[{idx}].type must be a non-empty string")
                        if not isinstance(tool.get("value"), str) or not tool["value"].strip():
                            errors.append(f"{openai_yaml}: dependencies.tools[{idx}].value must be a non-empty string")

    source_entry = indexes.source_by_name.get(skill_dir.name)
    source_scope = source_entry.get("scope") if source_entry else None
    source_invocation_mode = source_entry.get("invocation_mode") if source_entry else None
    if source_entry is None:
        errors.append(f"generated/skill_catalog.min.json missing {skill_dir.name}")
    if source_entry is not None:
        if allow_implicit != expected_allow:
            errors.append(
                f"{openai_yaml}: policy.allow_implicit_invocation={allow_implicit} does not match "
                f"implicit_activation_policy={activation_policy!r}"
            )

    agent_entry = indexes.agent_by_name.get(skill_dir.name)
    if agent_entry is None:
        errors.append(f"generated/agent_skill_catalog.json missing {skill_dir.name}")
    else:
        if agent_entry.get("path") != skill_md.relative_to(repo_root).as_posix():
            errors.append(f"generated/agent_skill_catalog.json path mismatch for {skill_dir.name}")
        if agent_entry.get("openai_config_path") != openai_yaml.relative_to(repo_root).as_posix():
            errors.append(f"generated/agent_skill_catalog.json openai_config_path mismatch for {skill_dir.name}")
        if agent_entry.get("allow_implicit_invocation") != allow_implicit:
            errors.append(f"generated/agent_skill_catalog.json allow_implicit_invocation mismatch for {skill_dir.name}")
        if agent_entry.get("implicit_activation_policy") != activation_policy:
            errors.append(f"generated/agent_skill_catalog.json implicit_activation_policy mismatch for {skill_dir.name}")
        if agent_entry.get("candidate_only") != (activation_policy == "suggest"):
            errors.append(f"generated/agent_skill_catalog.json candidate_only mismatch for {skill_dir.name}")

    export_entry = indexes.export_by_name.get(skill_dir.name)
    if export_entry is None:
        errors.append(f"generated/portable_export_map.json missing {skill_dir.name}")
    else:
        if export_entry.get("target_skill_path") != skill_md.relative_to(repo_root).as_posix():
            errors.append(f"generated/portable_export_map.json target_skill_path mismatch for {skill_dir.name}")
        if export_entry.get("implicit_activation_policy") != activation_policy:
            errors.append(f"generated/portable_export_map.json implicit_activation_policy mismatch for {skill_dir.name}")
        if export_entry.get("allow_implicit_invocation") != allow_implicit:
            errors.append(f"generated/portable_export_map.json allow_implicit_invocation mismatch for {skill_dir.name}")
        if export_entry.get("candidate_only") != (activation_policy == "suggest"):
            errors.append(f"generated/portable_export_map.json candidate_only mismatch for {skill_dir.name}")

    manifest_entry = indexes.manifest_by_name.get(skill_dir.name)
    if manifest_entry is None:
        errors.append(f"generated/local_adapter_manifest.json missing {skill_dir.name}")
    else:
        if manifest_entry.get("allow_implicit_invocation") != allow_implicit:
            errors.append(f"generated/local_adapter_manifest.json allow_implicit_invocation mismatch for {skill_dir.name}")
        if manifest_entry.get("implicit_activation_policy") != activation_policy:
            errors.append(f"generated/local_adapter_manifest.json implicit_activation_policy mismatch for {skill_dir.name}")
        if manifest_entry.get("trust_posture") != indexes.runtime_by_name.get(skill_dir.name, {}).get("trust_posture"):
            errors.append(f"generated/local_adapter_manifest.json trust_posture mismatch for {skill_dir.name}")
        for allowlist_path in manifest_entry.get("allowlist_paths", []):
            if not (repo_root / allowlist_path).exists():
                errors.append(f"generated/local_adapter_manifest.json allowlist path does not exist: {allowlist_path}")

    validate_exported_resource_surfaces(
        repo_root, skill_dir, indexes, agent_entry, export_entry, manifest_entry, errors
    )

    router_entry = validate_exported_runtime_catalog_surfaces(
        repo_root,
        skill_dir,
        skill_md,
        openai_yaml,
        indexes,
        source_entry,
        frontmatter,
        manifest_entry,
        dependency_tools,
        allow_implicit,
        activation_policy,
        description,
        errors,
    )

    validate_exported_description_router_surfaces(
        docs,
        indexes,
        skill_dir,
        description,
        source_scope,
        source_invocation_mode,
        allow_implicit,
        activation_policy,
        router_entry,
        errors,
    )


def validate_exported_skill_directories(
    repo_root: pathlib.Path,
    skills_root: pathlib.Path,
    docs: ExportSurfaceDocuments,
    indexes: ExportSurfaceIndexes,
    errors: list[str],
) -> None:
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        validate_exported_skill_directory(repo_root, docs, indexes, errors, skill_dir)



def validate_profile_set_surfaces(docs: ExportSurfaceDocuments, errors: list[str]) -> None:
    config_profile_names = set((docs.profile_doc.get("profiles") or {}).keys())
    resolved_profile_names = set((docs.resolved_profiles.get("profiles") or {}).keys())
    snippet_profile_names = set((docs.snippets_doc.get("snippets") or {}).keys())
    if config_profile_names != resolved_profile_names:
        errors.append("resolved profile set does not match config profile set")
    if config_profile_names != snippet_profile_names:
        errors.append("config snippet profile set does not match config profile set")



def validate_project_core_kernel_surfaces(repo_root: pathlib.Path, skills_root: pathlib.Path, docs: ExportSurfaceDocuments, indexes: ExportSurfaceIndexes, errors: list[str]) -> None:
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



def validate_project_core_outer_ring_surfaces(docs: ExportSurfaceDocuments, indexes: ExportSurfaceIndexes, errors: list[str]) -> None:
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



def validate_project_risk_ring_surfaces(docs: ExportSurfaceDocuments, indexes: ExportSurfaceIndexes, actual_names: set[str], errors: list[str]) -> None:
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



def validate_project_foundation_profile(docs: ExportSurfaceDocuments, errors: list[str]) -> None:
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



def validate_install_profile_surfaces(docs: ExportSurfaceDocuments, actual_names: set[str], errors: list[str]) -> None:
    for profile_name, profile in (docs.profile_doc.get("profiles") or {}).items():
        seen: set[str] = set()
        for skill_name in profile.get("skills", []):
            if skill_name not in actual_names:
                errors.append(f"config/skill_pack_profiles.json: unknown skill {skill_name!r} in {profile_name}")
            if skill_name in seen:
                errors.append(f"config/skill_pack_profiles.json: duplicate skill {skill_name!r} in {profile_name}")
            seen.add(skill_name)

    for profile_name, profile in (docs.resolved_profiles.get("profiles") or {}).items():
        for entry in profile.get("skills", []):
            if entry.get("name") not in actual_names:
                errors.append(f"generated/skill_pack_profiles.resolved.json: unknown skill {entry.get('name')!r} in {profile_name}")
        snippet = (docs.snippets_doc.get("snippets") or {}).get(profile_name, {})
        disable_profile_toml = snippet.get("disable_profile_toml", "")
        for entry in profile.get("skills", []):
            if entry["target_path"] not in disable_profile_toml:
                errors.append(f"generated/codex_config_snippets.json missing {entry['target_path']!r} in {profile_name}")



def validate_generated_evaluation_surfaces(docs: ExportSurfaceDocuments, indexes: ExportSurfaceIndexes, actual_names: set[str], errors: list[str]) -> None:
    description_case_totals: dict[str, int] = {}
    for case in docs.description_cases:
        description_case_totals[case["case_class"]] = description_case_totals.get(case["case_class"], 0) + 1
    if docs.description_manifest.get("skill_count") != len(actual_names):
        errors.append("generated/description_trigger_eval_manifest.json skill_count mismatch")
    if docs.description_manifest.get("total_cases") != len(docs.description_cases):
        errors.append("generated/description_trigger_eval_manifest.json total_cases mismatch")
    if docs.description_manifest.get("case_class_totals") != dict(sorted(description_case_totals.items())):
        errors.append("generated/description_trigger_eval_manifest.json case_class_totals mismatch")
    if docs.skills_ref_manifest.get("validator") != "skills-ref":
        errors.append("generated/skills_ref_validation_manifest.json validator mismatch")
    if docs.skills_ref_manifest.get("mode") != "soft-conformance-lane":
        errors.append("generated/skills_ref_validation_manifest.json mode mismatch")
    if len(docs.skills_ref_manifest.get("targets", [])) != len(actual_names):
        errors.append("generated/skills_ref_validation_manifest.json target count mismatch")
    support_schema_entries = docs.support_schema_index.get("schemas", [])
    if len(support_schema_entries) != len(TARGETED_SUPPORT_SKILLS):
        errors.append("generated/structured_output_schema_index.json schema count mismatch")
    if {entry.get("skill") for entry in support_schema_entries} != TARGETED_SUPPORT_SKILLS:
        errors.append("generated/structured_output_schema_index.json skill set mismatch")
    if docs.tiny_router_manifest.get("skill_count") != len(actual_names):
        errors.append("generated/tiny_router_overlay_manifest.json skill_count mismatch")
    if docs.tiny_router_manifest.get("band_count") != len(indexes.tiny_router_band_by_id):
        errors.append("generated/tiny_router_overlay_manifest.json band_count mismatch")
    if docs.tiny_router_manifest.get("case_count") != len(docs.tiny_router_eval_cases):
        errors.append("generated/tiny_router_overlay_manifest.json case_count mismatch")
    if "config/tiny_router_skill_bands.json" not in docs.tiny_router_manifest.get("source_files", []):
        errors.append("generated/tiny_router_overlay_manifest.json must include config/tiny_router_skill_bands.json")
    positive_tiny_router_coverage = {name: 0 for name in actual_names}
    for case in docs.tiny_router_eval_cases:
        for skill_name in case.get("expected_shortlist_includes", []):
            if skill_name not in actual_names:
                errors.append(f"{case.get('case_id')}: unknown tiny-router expected_shortlist skill {skill_name!r}")
            else:
                positive_tiny_router_coverage[skill_name] += 1
        top1 = case.get("expected_top1")
        if top1 is not None and top1 not in actual_names:
            errors.append(f"{case.get('case_id')}: unknown tiny-router expected_top1 {top1!r}")
        top1_not = case.get("expected_top1_not")
        if top1_not is not None and top1_not not in actual_names:
            errors.append(f"{case.get('case_id')}: unknown tiny-router expected_top1_not {top1_not!r}")
    missing_tiny_router_coverage = sorted(
        skill_name for skill_name, count in positive_tiny_router_coverage.items() if count < 1
    )
    if missing_tiny_router_coverage:
        errors.append(
            "generated/tiny_router_eval_cases.jsonl missing positive shortlist coverage for "
            + ", ".join(missing_tiny_router_coverage)
        )
    for band_id, band_entry in indexes.tiny_router_band_by_id.items():
        signal_entries = [
            entry for entry in docs.tiny_router_signals.get("skills", []) if entry.get("band") == band_id
        ]
        expected_band_skills = [entry["name"] for entry in signal_entries]
        expected_manual_only = sorted(
            entry["name"] for entry in signal_entries if entry.get("manual_invocation_required")
        )
        expected_suggest_only = sorted(
            entry["name"] for entry in signal_entries if entry.get("candidate_only")
        )
        expected_overlay = sorted(entry["name"] for entry in signal_entries if entry.get("project_overlay"))
        if band_entry.get("skills") != expected_band_skills:
            errors.append(f"generated/tiny_router_candidate_bands.json skills mismatch for band {band_id}")
        if sorted(band_entry.get("manual_only_skills", [])) != expected_manual_only:
            errors.append(f"generated/tiny_router_candidate_bands.json manual_only_skills mismatch for band {band_id}")
        if sorted(band_entry.get("suggest_only_skills", [])) != expected_suggest_only:
            errors.append(f"generated/tiny_router_candidate_bands.json suggest_only_skills mismatch for band {band_id}")
        if sorted(band_entry.get("overlay_skills", [])) != expected_overlay:
            errors.append(f"generated/tiny_router_candidate_bands.json overlay_skills mismatch for band {band_id}")



def validate_release_relationship_surfaces(repo_root: pathlib.Path, docs: ExportSurfaceDocuments, errors: list[str]) -> None:
    expected_release_manifest = release_manifest_contract.build_release_manifest(repo_root)
    for field_name in (
        "schema_version",
        "profile",
        "included_waves",
        "skill_root",
        "skill_count",
        "explicit_only_count",
        "profile_count",
        "authoring_inputs",
        "generated_files",
        "relationship_views",
        "artifact_groups",
        "authoring_input_digests",
        "generated_file_digests",
        "skill_bundle_revisions",
        "install_profile_revisions",
        "release_identity",
    ):
        if docs.release_manifest.get(field_name) != expected_release_manifest.get(field_name):
            errors.append(f"generated/release_manifest.json {field_name} mismatch")
    expected_bundle_index = build_catalog.build_bundle_index_payload(repo_root)
    if docs.bundle_index != expected_bundle_index:
        errors.append("generated/skill_bundle_index.json mismatch")
        difference = first_payload_difference(expected_bundle_index, docs.bundle_index)
        if difference is not None:
            errors.append(f"generated/skill_bundle_index.json detail: {difference}")
    expected_skill_graph = build_catalog.build_skill_graph_payload(repo_root)
    if docs.skill_graph != expected_skill_graph:
        errors.append("generated/skill_graph.json mismatch")
        difference = first_payload_difference(expected_skill_graph, docs.skill_graph)
        if difference is not None:
            errors.append(f"generated/skill_graph.json detail: {difference}")
    for rel_path in docs.release_manifest.get("relationship_views", []):
        if rel_path not in docs.release_manifest.get("generated_files", []):
            errors.append(
                "generated/release_manifest.json missing relationship view from generated_files: "
                + rel_path
            )



def validate_runtime_seam_surfaces(docs: ExportSurfaceDocuments, errors: list[str]) -> None:
    if docs.runtime_discovery.get("root") != ".agents/skills":
        errors.append("generated/runtime_discovery_index.json root mismatch")
    if docs.runtime_discovery_min.get("root") != ".agents/skills":
        errors.append("generated/runtime_discovery_index.min.json root mismatch")
    if docs.runtime_disclosure.get("root") != ".agents/skills":
        errors.append("generated/runtime_disclosure_index.json root mismatch")

    tool_names = [tool.get("name") for tool in docs.runtime_tool_schemas.get("tools", [])]
    if tool_names != [
        "discover_skills",
        "disclose_skill",
        "activate_skill",
        "skill_session_status",
        "deactivate_skill",
        "compact_skill_session",
    ]:
        errors.append("generated/runtime_tool_schemas.json tool set mismatch")
    if not docs.runtime_prompt_blocks.get("system_prompt_block"):
        errors.append("generated/runtime_prompt_blocks.json missing system_prompt_block")
    if not docs.runtime_prompt_blocks.get("tool_description_block"):
        errors.append("generated/runtime_prompt_blocks.json missing tool_description_block")
    if docs.runtime_session_contract.get("session_file_hint") != ".aoa/skill-runtime-session.json":
        errors.append("generated/runtime_session_contract.json session_file_hint mismatch")

    manifest_tools = docs.runtime_seam_manifest.get("tools", {})
    expected_manifest_tools = {
        "discover": "scripts/skill_runtime_seam.py discover",
        "disclose": "scripts/skill_runtime_seam.py disclose",
        "activate": "scripts/skill_runtime_seam.py activate",
        "status": "scripts/skill_runtime_seam.py status",
        "deactivate": "scripts/skill_runtime_seam.py deactivate",
        "compact": "scripts/skill_runtime_seam.py compact",
    }
    if manifest_tools != expected_manifest_tools:
        errors.append("generated/runtime_seam_manifest.json tools mismatch")
    if docs.runtime_seam_manifest.get("common_surface") != ".agents/skills":
        errors.append("generated/runtime_seam_manifest.json common_surface mismatch")
    if docs.runtime_seam_manifest.get("backward_compatibility", {}).get("legacy_activation_tool") != "scripts/activate_skill.py":
        errors.append("generated/runtime_seam_manifest.json legacy activation tool mismatch")
    generated_refs = docs.runtime_seam_manifest.get("generated", {})
    if generated_refs.get("discovery_index") != "generated/runtime_discovery_index.json":
        errors.append("generated/runtime_seam_manifest.json discovery_index mismatch")
    if generated_refs.get("disclosure_index") != "generated/runtime_disclosure_index.json":
        errors.append("generated/runtime_seam_manifest.json disclosure_index mismatch")



def validate_runtime_guardrail_surfaces(repo_root: pathlib.Path, docs: ExportSurfaceDocuments, indexes: ExportSurfaceIndexes, actual_names: set[str], errors: list[str]) -> None:
    guardrail_tool_names = [tool.get("name") for tool in docs.guardrail_tool_schemas.get("tools", [])]
    if guardrail_tool_names != [
        "guarded_discover_skills",
        "guarded_disclose_skill",
        "guarded_activate_skill",
        "guarded_skill_session_status",
        "repo_trust_gate",
        "resolve_skill_allowlist",
        "guarded_compact_skill_session",
        "rehydrate_skill_context",
    ]:
        errors.append("generated/runtime_guardrail_tool_schemas.json tool set mismatch")
    if not docs.guardrail_prompt_blocks.get("system_prompt_block"):
        errors.append("generated/runtime_guardrail_prompt_blocks.json missing system_prompt_block")
    if not docs.guardrail_prompt_blocks.get("tool_description_block"):
        errors.append("generated/runtime_guardrail_prompt_blocks.json missing tool_description_block")
    if docs.guardrail_manifest.get("common_surface") != ".agents/skills":
        errors.append("generated/runtime_guardrail_manifest.json common_surface mismatch")
    if docs.guardrail_manifest.get("trust_store_hint") != ".aoa/repo-trust-store.json":
        errors.append("generated/runtime_guardrail_manifest.json trust_store_hint mismatch")
    if docs.guardrail_manifest.get("session_file_hint") != ".aoa/skill-runtime-session.json":
        errors.append("generated/runtime_guardrail_manifest.json session_file_hint mismatch")
    if docs.guardrail_manifest.get("downstream_of", {}).get("runtime_seam") != "scripts/skill_runtime_seam.py":
        errors.append("generated/runtime_guardrail_manifest.json runtime_seam mismatch")
    if docs.guardrail_manifest.get("downstream_of", {}).get("legacy_activation_shim") != "scripts/activate_skill.py":
        errors.append("generated/runtime_guardrail_manifest.json legacy_activation_shim mismatch")

    repo_scoped_skills = sorted(
        name for name, entry in indexes.guardrail_trust_by_name.items() if entry.get("source_scope") == "repo"
    )
    if repo_scoped_skills:
        guarded_docs = load_guardrails(repo_root)
        with tempfile.TemporaryDirectory() as tmpdir:
            trust_store = pathlib.Path(tmpdir) / "repo-trust-store.json"
            blocked_discovery = discover_guarded_payload(
                repo_root,
                guarded_docs,
                trust_store_path=trust_store,
                repo_trusted="auto",
            )
            expected_visible = len(actual_names) - len(repo_scoped_skills)
            if blocked_discovery.get("count") != expected_visible:
                errors.append("guarded discover count mismatch for untrusted repo")
            if blocked_discovery.get("blocked_count") != len(repo_scoped_skills):
                errors.append("guarded discover blocked_count mismatch for untrusted repo")

            blocked_activate = activate_guarded_payload(
                repo_root,
                guarded_docs,
                skill_name=repo_scoped_skills[0],
                trust_store_path=trust_store,
                repo_trusted="auto",
            )
            if blocked_activate.get("stage") != "activate_blocked":
                errors.append("guarded activate must block repo-scoped skills when repo is untrusted")
            if "instructions_markdown" in blocked_activate:
                errors.append("guarded blocked payload must not expose instructions_markdown")

            trust_result = trust_payload(
                repo_root,
                decision="trusted",
                reason="validation smoke",
                trust_store_path=trust_store,
            )
            if not trust_result.get("trust_status", {}).get("repo_trusted"):
                errors.append("guarded trust payload failed to mark repo trusted")

            trusted_discovery = discover_guarded_payload(
                repo_root,
                guarded_docs,
                trust_store_path=trust_store,
                repo_trusted="auto",
            )
            if trusted_discovery.get("count") != len(actual_names):
                errors.append("guarded discover must expose all skills after trusting repo")
            if trusted_discovery.get("blocked_count") != 0:
                errors.append("guarded discover blocked_count must be 0 after trusting repo")



def validate(repo_root: pathlib.Path) -> ValidationResult:
    skills_root = repo_root / ".agents" / "skills"
    errors: list[str] = []

    append_missing_files(errors, repo_root, REQUIRED_GENERATED_FILES)
    append_missing_files(errors, repo_root, REQUIRED_CONFIG_FILES)

    docs = load_export_surface_documents(repo_root)
    indexes = build_export_surface_indexes(docs)

    validate_profile_markers(docs, errors)
    actual_names = discover_exported_skill_names(skills_root, errors)
    validate_export_skill_sets(docs, indexes, actual_names, errors)

    validate_exported_skill_directories(repo_root, skills_root, docs, indexes, errors)

    validate_profile_set_surfaces(docs, errors)

    validate_project_core_kernel_surfaces(repo_root, skills_root, docs, indexes, errors)

    validate_project_core_outer_ring_surfaces(docs, indexes, errors)

    validate_project_risk_ring_surfaces(docs, indexes, actual_names, errors)

    validate_project_foundation_profile(docs, errors)

    validate_install_profile_surfaces(docs, actual_names, errors)

    validate_generated_evaluation_surfaces(docs, indexes, actual_names, errors)

    validate_release_relationship_surfaces(repo_root, docs, errors)

    validate_runtime_seam_surfaces(docs, errors)

    validate_runtime_guardrail_surfaces(repo_root, docs, indexes, actual_names, errors)

    return ValidationResult(errors, len(actual_names), skills_root)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root containing .agents/skills")
    args = parser.parse_args()

    result = validate(pathlib.Path(args.repo_root).resolve())
    if result.errors:
        for error in result.errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {result.validated_skill_count} skills in {result.skills_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
