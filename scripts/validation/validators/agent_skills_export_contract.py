"""Load the portable Agent Skills export validation contract."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_CONTRACT_PATH = Path(__file__).with_name("agent_skills_export_contract.json")


@dataclass(frozen=True)
class AgentSkillsExportContract:
    export_profile: str
    runtime_profile: str
    guardrail_profile: str
    description_trigger_profile: str
    skills_ref_profile: str
    support_resource_profile: str
    tiny_router_profile: str
    targeted_support_skills: tuple[str, ...]
    support_standard_dirs: tuple[str, ...]
    support_legacy_dirs: tuple[str, ...]
    portable_resource_dirs: tuple[str, ...]
    required_metadata: tuple[str, ...]
    required_generated_files: tuple[str, ...]
    required_config_files: tuple[str, ...]
    expected_outer_ring_skills: tuple[str, ...]
    expected_outer_ring_clusters: tuple[dict[str, Any], ...]
    expected_risk_ring_skills: tuple[str, ...]
    expected_risk_ring_clusters: tuple[dict[str, Any], ...]
    expected_risk_ring_adjacent_overlays: tuple[dict[str, str], ...]
    expected_foundation_profile_skills: tuple[str, ...]


def _require_mapping(payload: dict[str, Any], key: str, path: Path) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: {key} must be an object")
    return value


def _require_string(payload: dict[str, Any], key: str, path: Path) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{path}: {key} must be a non-empty string")
    return value


def _require_string_list(payload: dict[str, Any], key: str, path: Path) -> tuple[str, ...]:
    value = payload.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{path}: {key} must be a non-empty list")
    if any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"{path}: {key} must contain non-empty strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{path}: {key} must not contain duplicates")
    return tuple(value)


def _require_clusters(payload: dict[str, Any], key: str, path: Path) -> tuple[dict[str, Any], ...]:
    value = payload.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{path}: {key} must be a non-empty list")
    cluster_ids: set[str] = set()
    clusters: list[dict[str, Any]] = []
    for index, cluster in enumerate(value):
        if not isinstance(cluster, dict):
            raise ValueError(f"{path}: {key}[{index}] must be an object")
        cluster_id = cluster.get("cluster_id")
        skills = cluster.get("skills")
        if not isinstance(cluster_id, str) or not cluster_id:
            raise ValueError(f"{path}: {key}[{index}].cluster_id must be a non-empty string")
        if cluster_id in cluster_ids:
            raise ValueError(f"{path}: {key}[{index}].cluster_id must be unique")
        cluster_ids.add(cluster_id)
        if not isinstance(skills, list) or not skills:
            raise ValueError(f"{path}: {key}[{index}].skills must be a non-empty list")
        if any(not isinstance(skill, str) or not skill for skill in skills):
            raise ValueError(f"{path}: {key}[{index}].skills must contain non-empty strings")
        clusters.append({"cluster_id": cluster_id, "skills": list(skills)})
    return tuple(clusters)


def _require_adjacent_overlays(
    payload: dict[str, Any],
    key: str,
    path: Path,
) -> tuple[dict[str, str], ...]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise ValueError(f"{path}: {key} must be a list")
    overlays: list[dict[str, str]] = []
    for index, overlay in enumerate(value):
        if not isinstance(overlay, dict):
            raise ValueError(f"{path}: {key}[{index}] must be an object")
        base = overlay.get("base_skill_name")
        projected = overlay.get("overlay_skill_name")
        if not isinstance(base, str) or not base:
            raise ValueError(f"{path}: {key}[{index}].base_skill_name must be a non-empty string")
        if not isinstance(projected, str) or not projected:
            raise ValueError(f"{path}: {key}[{index}].overlay_skill_name must be a non-empty string")
        overlays.append({"base_skill_name": base, "overlay_skill_name": projected})
    return tuple(overlays)


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> AgentSkillsExportContract:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: contract must be a JSON object")
    if payload.get("schema_version") != 1:
        raise ValueError(f"{path}: schema_version must be 1")

    profiles = _require_mapping(payload, "profiles", path)
    support = _require_mapping(payload, "support_resources", path)
    project_core = _require_mapping(payload, "project_core", path)
    outer_ring = _require_mapping(project_core, "outer_ring", path)
    risk_ring = _require_mapping(project_core, "risk_ring", path)
    foundation_profile = _require_mapping(project_core, "foundation_profile", path)

    return AgentSkillsExportContract(
        export_profile=_require_string(profiles, "export", path),
        runtime_profile=_require_string(profiles, "runtime", path),
        guardrail_profile=_require_string(profiles, "guardrail", path),
        description_trigger_profile=_require_string(profiles, "description_trigger", path),
        skills_ref_profile=_require_string(profiles, "skills_ref", path),
        support_resource_profile=_require_string(profiles, "support_resource", path),
        tiny_router_profile=_require_string(profiles, "tiny_router", path),
        targeted_support_skills=_require_string_list(support, "targeted_skills", path),
        support_standard_dirs=_require_string_list(support, "standard_dirs", path),
        support_legacy_dirs=_require_string_list(support, "legacy_dirs", path),
        portable_resource_dirs=_require_string_list(support, "portable_resource_dirs", path),
        required_metadata=_require_string_list(payload, "required_metadata", path),
        required_generated_files=_require_string_list(payload, "required_generated_files", path),
        required_config_files=_require_string_list(payload, "required_config_files", path),
        expected_outer_ring_skills=_require_string_list(outer_ring, "skills", path),
        expected_outer_ring_clusters=_require_clusters(outer_ring, "clusters", path),
        expected_risk_ring_skills=_require_string_list(risk_ring, "skills", path),
        expected_risk_ring_clusters=_require_clusters(risk_ring, "clusters", path),
        expected_risk_ring_adjacent_overlays=_require_adjacent_overlays(
            risk_ring,
            "adjacent_overlays",
            path,
        ),
        expected_foundation_profile_skills=_require_string_list(
            foundation_profile,
            "skills",
            path,
        ),
    )
