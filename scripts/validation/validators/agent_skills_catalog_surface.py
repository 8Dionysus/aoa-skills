"""Catalog-entry validation phase for Agent Skills export."""

from __future__ import annotations

import pathlib
from dataclasses import dataclass
from typing import Any

from validation.validators import agent_skills_local_adapter_surface


@dataclass(frozen=True)
class CatalogEntryValidationResult:
    source_entry: Any
    source_scope: Any
    source_invocation_mode: Any
    agent_entry: Any
    export_entry: Any
    manifest_entry: Any


def validate_export_catalog_entries(
    *,
    repo_root: pathlib.Path,
    skill_name: str,
    skill_md: pathlib.Path,
    openai_yaml: pathlib.Path,
    source_by_name: dict[str, Any],
    agent_by_name: dict[str, Any],
    export_by_name: dict[str, Any],
    manifest_by_name: dict[str, Any],
    runtime_by_name: dict[str, Any],
    allow_implicit: Any,
    activation_policy: str,
    expected_allow: bool,
    errors: list[str],
) -> CatalogEntryValidationResult:
    source_entry = source_by_name.get(skill_name)
    source_scope = source_entry.get("scope") if source_entry else None
    source_invocation_mode = source_entry.get("invocation_mode") if source_entry else None
    if source_entry is None:
        errors.append(f"generated/skill_catalog.min.json missing {skill_name}")
    elif allow_implicit != expected_allow:
        errors.append(
            f"{openai_yaml}: policy.allow_implicit_invocation={allow_implicit} does not match "
            f"implicit_activation_policy={activation_policy!r}"
        )

    agent_entry = agent_by_name.get(skill_name)
    if agent_entry is None:
        errors.append(f"generated/agent_skill_catalog.json missing {skill_name}")
    else:
        if agent_entry.get("path") != skill_md.relative_to(repo_root).as_posix():
            errors.append(f"generated/agent_skill_catalog.json path mismatch for {skill_name}")
        if agent_entry.get("openai_config_path") != openai_yaml.relative_to(repo_root).as_posix():
            errors.append(f"generated/agent_skill_catalog.json openai_config_path mismatch for {skill_name}")
        if agent_entry.get("allow_implicit_invocation") != allow_implicit:
            errors.append(f"generated/agent_skill_catalog.json allow_implicit_invocation mismatch for {skill_name}")
        if agent_entry.get("implicit_activation_policy") != activation_policy:
            errors.append(f"generated/agent_skill_catalog.json implicit_activation_policy mismatch for {skill_name}")
        if agent_entry.get("candidate_only") != (activation_policy == "suggest"):
            errors.append(f"generated/agent_skill_catalog.json candidate_only mismatch for {skill_name}")

    export_entry = export_by_name.get(skill_name)
    if export_entry is None:
        errors.append(f"generated/portable_export_map.json missing {skill_name}")
    else:
        if export_entry.get("target_skill_path") != skill_md.relative_to(repo_root).as_posix():
            errors.append(f"generated/portable_export_map.json target_skill_path mismatch for {skill_name}")
        if export_entry.get("implicit_activation_policy") != activation_policy:
            errors.append(
                f"generated/portable_export_map.json implicit_activation_policy mismatch for {skill_name}"
            )
        if export_entry.get("allow_implicit_invocation") != allow_implicit:
            errors.append(f"generated/portable_export_map.json allow_implicit_invocation mismatch for {skill_name}")
        if export_entry.get("candidate_only") != (activation_policy == "suggest"):
            errors.append(f"generated/portable_export_map.json candidate_only mismatch for {skill_name}")

    manifest_entry = manifest_by_name.get(skill_name)
    agent_skills_local_adapter_surface.validate_local_adapter_entry(
        repo_root=repo_root,
        skill_name=skill_name,
        manifest_entry=manifest_entry,
        runtime_entry=runtime_by_name.get(skill_name, {}),
        allow_implicit=allow_implicit,
        activation_policy=activation_policy,
        errors=errors,
    )
    return CatalogEntryValidationResult(
        source_entry=source_entry,
        source_scope=source_scope,
        source_invocation_mode=source_invocation_mode,
        agent_entry=agent_entry,
        export_entry=export_entry,
        manifest_entry=manifest_entry,
    )
