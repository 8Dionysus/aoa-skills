#!/usr/bin/env python3
"""Validate the cumulative Codex-facing Agent Skills export and wave-3 support artifacts."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import tempfile
from typing import Any

import yaml

from skill_runtime_guardrails import (
    activate_guarded_payload,
    discover_guarded_payload,
    load_guardrails,
    trust_payload,
)

EXPORT_PROFILE = "codex-facing-wave-3"
RUNTIME_PROFILE = "codex-facing-wave-4-runtime-seam"
GUARDRAIL_PROFILE = "codex-facing-wave-6-runtime-guardrails"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
REQUIRED_METADATA = {
    "aoa_scope",
    "aoa_status",
    "aoa_invocation_mode",
    "aoa_source_skill_path",
    "aoa_source_repo",
    "aoa_technique_dependencies",
    "aoa_portable_profile",
}
REQUIRED_GENERATED_FILES = [
    "generated/skill_catalog.min.json",
    "generated/skill_sections.full.json",
    "generated/agent_skill_catalog.json",
    "generated/agent_skill_catalog.min.json",
    "generated/portable_export_map.json",
    "generated/local_adapter_manifest.json",
    "generated/local_adapter_manifest.min.json",
    "generated/skill_handoff_contracts.json",
    "generated/context_retention_manifest.json",
    "generated/trust_policy_matrix.json",
    "generated/skill_runtime_contracts.json",
    "generated/skill_pack_profiles.resolved.json",
    "generated/codex_config_snippets.json",
    "generated/mcp_dependency_manifest.json",
    "generated/runtime_discovery_index.json",
    "generated/runtime_discovery_index.min.json",
    "generated/runtime_disclosure_index.json",
    "generated/runtime_activation_aliases.json",
    "generated/runtime_tool_schemas.json",
    "generated/runtime_session_contract.json",
    "generated/runtime_prompt_blocks.json",
    "generated/runtime_router_hints.json",
    "generated/runtime_seam_manifest.json",
    "generated/repo_trust_gate_manifest.json",
    "generated/permission_allowlist_manifest.json",
    "generated/skill_context_guard_manifest.json",
    "generated/runtime_guardrail_tool_schemas.json",
    "generated/runtime_guardrail_prompt_blocks.json",
    "generated/runtime_guardrail_manifest.json",
    "generated/release_manifest.json",
]
RELEASE_MANIFEST_GENERATED_FILES = [
    "generated/agent_skill_catalog.json",
    "generated/agent_skill_catalog.min.json",
    "generated/portable_export_map.json",
    "generated/local_adapter_manifest.json",
    "generated/local_adapter_manifest.min.json",
    "generated/skill_handoff_contracts.json",
    "generated/context_retention_manifest.json",
    "generated/trust_policy_matrix.json",
    "generated/skill_runtime_contracts.json",
    "generated/skill_pack_profiles.resolved.json",
    "generated/codex_config_snippets.json",
    "generated/mcp_dependency_manifest.json",
    "generated/runtime_discovery_index.json",
    "generated/runtime_discovery_index.min.json",
    "generated/runtime_disclosure_index.json",
    "generated/runtime_activation_aliases.json",
    "generated/runtime_tool_schemas.json",
    "generated/runtime_session_contract.json",
    "generated/runtime_prompt_blocks.json",
    "generated/runtime_router_hints.json",
    "generated/runtime_seam_manifest.json",
    "generated/repo_trust_gate_manifest.json",
    "generated/permission_allowlist_manifest.json",
    "generated/skill_context_guard_manifest.json",
    "generated/runtime_guardrail_tool_schemas.json",
    "generated/runtime_guardrail_prompt_blocks.json",
    "generated/runtime_guardrail_manifest.json",
    "generated/release_manifest.json",
]
REQUIRED_CONFIG_FILES = [
    "config/portable_skill_overrides.json",
    "config/openai_skill_extensions.json",
    "config/skill_pack_profiles.json",
    "config/skill_policy_matrix.json",
    "config/runtime_guardrail_policy.json",
]


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


def append_missing_files(errors: list[str], repo_root: pathlib.Path, rel_paths: list[str]) -> None:
    for rel_path in rel_paths:
        if not (repo_root / rel_path).exists():
            errors.append(f"missing required file: {rel_path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root containing .agents/skills")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    skills_root = repo_root / ".agents" / "skills"
    generated_dir = repo_root / "generated"
    config_dir = repo_root / "config"
    errors: list[str] = []

    append_missing_files(errors, repo_root, REQUIRED_GENERATED_FILES)
    append_missing_files(errors, repo_root, REQUIRED_CONFIG_FILES)

    source_catalog = load_json(generated_dir / "skill_catalog.min.json")
    agent_catalog = load_json(generated_dir / "agent_skill_catalog.json")
    agent_catalog_min = load_json(generated_dir / "agent_skill_catalog.min.json")
    export_map = load_json(generated_dir / "portable_export_map.json")
    local_manifest = load_json(generated_dir / "local_adapter_manifest.json")
    local_manifest_min = load_json(generated_dir / "local_adapter_manifest.min.json")
    handoff_doc = load_json(generated_dir / "skill_handoff_contracts.json")
    runtime_doc = load_json(generated_dir / "skill_runtime_contracts.json")
    trust_doc = load_json(generated_dir / "trust_policy_matrix.json")
    context_doc = load_json(generated_dir / "context_retention_manifest.json")
    resolved_profiles = load_json(generated_dir / "skill_pack_profiles.resolved.json")
    snippets_doc = load_json(generated_dir / "codex_config_snippets.json")
    mcp_doc = load_json(generated_dir / "mcp_dependency_manifest.json")
    runtime_discovery = load_json(generated_dir / "runtime_discovery_index.json")
    runtime_discovery_min = load_json(generated_dir / "runtime_discovery_index.min.json")
    runtime_disclosure = load_json(generated_dir / "runtime_disclosure_index.json")
    runtime_aliases = load_json(generated_dir / "runtime_activation_aliases.json")
    runtime_tool_schemas = load_json(generated_dir / "runtime_tool_schemas.json")
    runtime_session_contract = load_json(generated_dir / "runtime_session_contract.json")
    runtime_prompt_blocks = load_json(generated_dir / "runtime_prompt_blocks.json")
    runtime_router_hints = load_json(generated_dir / "runtime_router_hints.json")
    runtime_seam_manifest = load_json(generated_dir / "runtime_seam_manifest.json")
    guardrail_trust_gate = load_json(generated_dir / "repo_trust_gate_manifest.json")
    guardrail_allowlist = load_json(generated_dir / "permission_allowlist_manifest.json")
    guardrail_context = load_json(generated_dir / "skill_context_guard_manifest.json")
    guardrail_tool_schemas = load_json(generated_dir / "runtime_guardrail_tool_schemas.json")
    guardrail_prompt_blocks = load_json(generated_dir / "runtime_guardrail_prompt_blocks.json")
    guardrail_manifest = load_json(generated_dir / "runtime_guardrail_manifest.json")
    release_manifest = load_json(generated_dir / "release_manifest.json")
    overrides_doc = load_json(config_dir / "portable_skill_overrides.json")
    profile_doc = load_json(config_dir / "skill_pack_profiles.json")
    policy_doc = load_json(config_dir / "skill_policy_matrix.json")
    guardrail_policy = load_json(config_dir / "runtime_guardrail_policy.json")

    source_by_name = {entry["name"]: entry for entry in source_catalog.get("skills", [])}
    agent_by_name = {entry["name"]: entry for entry in agent_catalog.get("skills", [])}
    agent_min_by_name = {entry["name"]: entry for entry in agent_catalog_min.get("skills", [])}
    export_by_name = {entry["name"]: entry for entry in export_map.get("exports", [])}
    manifest_by_name = {entry["name"]: entry for entry in local_manifest.get("skills", [])}
    manifest_min_by_name = {entry["name"]: entry for entry in local_manifest_min.get("skills", [])}
    handoff_by_name = {entry["name"]: entry for entry in handoff_doc.get("skills", [])}
    runtime_by_name = {entry["name"]: entry for entry in runtime_doc.get("skills", [])}
    trust_by_name = {entry["name"]: entry for entry in trust_doc.get("skills", [])}
    context_by_name = {entry["name"]: entry for entry in context_doc.get("skills", [])}
    mcp_by_name = {entry["name"]: entry for entry in mcp_doc.get("skills", [])}
    discovery_by_name = {entry["name"]: entry for entry in runtime_discovery.get("skills", [])}
    discovery_min_by_name = {entry["name"]: entry for entry in runtime_discovery_min.get("skills", [])}
    disclosure_by_name = {entry["name"]: entry for entry in runtime_disclosure.get("skills", [])}
    router_by_name = {entry["name"]: entry for entry in runtime_router_hints.get("skills", [])}
    alias_by_name = {entry["name"]: entry for entry in runtime_aliases.get("aliases", [])}
    guardrail_trust_by_name = {entry["name"]: entry for entry in guardrail_trust_gate.get("skills", [])}
    guardrail_allowlist_by_name = {entry["name"]: entry for entry in guardrail_allowlist.get("skills", [])}
    guardrail_context_by_name = {entry["name"]: entry for entry in guardrail_context.get("skills", [])}

    if overrides_doc.get("profile") != EXPORT_PROFILE:
        errors.append(f"config/portable_skill_overrides.json profile must be {EXPORT_PROFILE!r}")
    if resolved_profiles.get("profile") != EXPORT_PROFILE:
        errors.append(f"generated/skill_pack_profiles.resolved.json profile must be {EXPORT_PROFILE!r}")
    if snippets_doc.get("profile") != EXPORT_PROFILE:
        errors.append(f"generated/codex_config_snippets.json profile must be {EXPORT_PROFILE!r}")
    if release_manifest.get("profile") != EXPORT_PROFILE:
        errors.append(f"generated/release_manifest.json profile must be {EXPORT_PROFILE!r}")
    if handoff_doc.get("profile") != EXPORT_PROFILE:
        errors.append(f"generated/skill_handoff_contracts.json profile must be {EXPORT_PROFILE!r}")
    for label, doc in {
        "generated/runtime_discovery_index.json": runtime_discovery,
        "generated/runtime_discovery_index.min.json": runtime_discovery_min,
        "generated/runtime_disclosure_index.json": runtime_disclosure,
        "generated/runtime_activation_aliases.json": runtime_aliases,
        "generated/runtime_tool_schemas.json": runtime_tool_schemas,
        "generated/runtime_session_contract.json": runtime_session_contract,
        "generated/runtime_prompt_blocks.json": runtime_prompt_blocks,
        "generated/runtime_router_hints.json": runtime_router_hints,
        "generated/runtime_seam_manifest.json": runtime_seam_manifest,
    }.items():
        if doc.get("profile") != RUNTIME_PROFILE:
            errors.append(f"{label} profile must be {RUNTIME_PROFILE!r}")
    for label, doc in {
        "config/runtime_guardrail_policy.json": guardrail_policy,
        "generated/repo_trust_gate_manifest.json": guardrail_trust_gate,
        "generated/permission_allowlist_manifest.json": guardrail_allowlist,
        "generated/skill_context_guard_manifest.json": guardrail_context,
        "generated/runtime_guardrail_tool_schemas.json": guardrail_tool_schemas,
        "generated/runtime_guardrail_prompt_blocks.json": guardrail_prompt_blocks,
        "generated/runtime_guardrail_manifest.json": guardrail_manifest,
    }.items():
        if doc.get("profile") != GUARDRAIL_PROFILE:
            errors.append(f"{label} profile must be {GUARDRAIL_PROFILE!r}")

    if not skills_root.exists():
        errors.append(f"missing skills root: {skills_root}")
        actual_names: set[str] = set()
    else:
        actual_names = {path.name for path in skills_root.iterdir() if path.is_dir()}

    expected_sets = {
        "generated/skill_catalog.min.json": set(source_by_name),
        "generated/agent_skill_catalog.json": set(agent_by_name),
        "generated/agent_skill_catalog.min.json": set(agent_min_by_name),
        "generated/portable_export_map.json": set(export_by_name),
        "generated/local_adapter_manifest.json": set(manifest_by_name),
        "generated/local_adapter_manifest.min.json": set(manifest_min_by_name),
        "generated/skill_handoff_contracts.json": set(handoff_by_name),
        "generated/skill_runtime_contracts.json": set(runtime_by_name),
        "generated/trust_policy_matrix.json": set(trust_by_name),
        "generated/context_retention_manifest.json": set(context_by_name),
        "generated/mcp_dependency_manifest.json": set(mcp_by_name),
        "generated/runtime_discovery_index.json": set(discovery_by_name),
        "generated/runtime_discovery_index.min.json": set(discovery_min_by_name),
        "generated/runtime_disclosure_index.json": set(disclosure_by_name),
        "generated/runtime_router_hints.json": set(router_by_name),
        "generated/runtime_activation_aliases.json": set(alias_by_name),
        "generated/repo_trust_gate_manifest.json": set(guardrail_trust_by_name),
        "generated/permission_allowlist_manifest.json": set(guardrail_allowlist_by_name),
        "generated/skill_context_guard_manifest.json": set(guardrail_context_by_name),
        "config/skill_policy_matrix.json": set((policy_doc.get("skills") or {}).keys()),
    }
    for label, names in expected_sets.items():
        if names != actual_names:
            errors.append(f"{label} skill set {sorted(names)!r} does not match export {sorted(actual_names)!r}")

    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        openai_yaml = skill_dir / "agents" / "openai.yaml"
        small_icon = skill_dir / "assets" / "small-logo.svg"
        large_icon = skill_dir / "assets" / "large-logo.svg"
        if not skill_md.exists():
            errors.append(f"{skill_dir}: missing SKILL.md")
            continue
        if not openai_yaml.exists():
            errors.append(f"{skill_dir}: missing agents/openai.yaml")
            continue
        if not small_icon.exists() or not large_icon.exists():
            errors.append(f"{skill_dir}: missing icon assets")
            continue

        try:
            frontmatter, body = parse_frontmatter(skill_md)
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))
            continue

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
            continue
        if not isinstance(openai_doc, dict):
            errors.append(f"{openai_yaml}: top-level YAML must be a mapping")
            continue

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

        source_entry = source_by_name.get(skill_dir.name)
        if source_entry is not None:
            expected_allow = source_entry.get("invocation_mode") != "explicit-only"
            if allow_implicit != expected_allow:
                errors.append(
                    f"{openai_yaml}: policy.allow_implicit_invocation={allow_implicit} does not match "
                    f"canonical invocation_mode={source_entry.get('invocation_mode')!r}"
                )

        agent_entry = agent_by_name.get(skill_dir.name)
        if agent_entry is None:
            errors.append(f"generated/agent_skill_catalog.json missing {skill_dir.name}")
        else:
            if agent_entry.get("path") != skill_md.relative_to(repo_root).as_posix():
                errors.append(f"generated/agent_skill_catalog.json path mismatch for {skill_dir.name}")
            if agent_entry.get("openai_config_path") != openai_yaml.relative_to(repo_root).as_posix():
                errors.append(f"generated/agent_skill_catalog.json openai_config_path mismatch for {skill_dir.name}")
            if agent_entry.get("allow_implicit_invocation") != allow_implicit:
                errors.append(f"generated/agent_skill_catalog.json allow_implicit_invocation mismatch for {skill_dir.name}")

        export_entry = export_by_name.get(skill_dir.name)
        if export_entry is None:
            errors.append(f"generated/portable_export_map.json missing {skill_dir.name}")
        else:
            if export_entry.get("target_skill_path") != skill_md.relative_to(repo_root).as_posix():
                errors.append(f"generated/portable_export_map.json target_skill_path mismatch for {skill_dir.name}")

        manifest_entry = manifest_by_name.get(skill_dir.name)
        if manifest_entry is None:
            errors.append(f"generated/local_adapter_manifest.json missing {skill_dir.name}")
        else:
            if manifest_entry.get("allow_implicit_invocation") != allow_implicit:
                errors.append(f"generated/local_adapter_manifest.json allow_implicit_invocation mismatch for {skill_dir.name}")
            if manifest_entry.get("trust_posture") != runtime_by_name.get(skill_dir.name, {}).get("trust_posture"):
                errors.append(f"generated/local_adapter_manifest.json trust_posture mismatch for {skill_dir.name}")
            for allowlist_path in manifest_entry.get("allowlist_paths", []):
                if not (repo_root / allowlist_path).exists():
                    errors.append(f"generated/local_adapter_manifest.json allowlist path does not exist: {allowlist_path}")

        handoff_entry = handoff_by_name.get(skill_dir.name)
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

        runtime_entry = runtime_by_name.get(skill_dir.name)
        if runtime_entry is None:
            errors.append(f"generated/skill_runtime_contracts.json missing {skill_dir.name}")
        else:
            if runtime_entry.get("allow_implicit_invocation") != allow_implicit:
                errors.append(f"generated/skill_runtime_contracts.json allow_implicit_invocation mismatch for {skill_dir.name}")
            if runtime_entry.get("context_retention_ref") != f"generated/context_retention_manifest.json#{skill_dir.name}":
                errors.append(f"generated/skill_runtime_contracts.json context_retention_ref mismatch for {skill_dir.name}")

        trust_entry = trust_by_name.get(skill_dir.name)
        if trust_entry is None:
            errors.append(f"generated/trust_policy_matrix.json missing {skill_dir.name}")
        else:
            if source_entry and trust_entry.get("invocation_mode") != source_entry.get("invocation_mode"):
                errors.append(f"generated/trust_policy_matrix.json invocation_mode mismatch for {skill_dir.name}")
            requires_manual = source_entry and source_entry.get("invocation_mode") == "explicit-only"
            if trust_entry.get("requires_manual_invocation") != requires_manual:
                errors.append(f"generated/trust_policy_matrix.json requires_manual_invocation mismatch for {skill_dir.name}")

        context_entry = context_by_name.get(skill_dir.name)
        if context_entry is None:
            errors.append(f"generated/context_retention_manifest.json missing {skill_dir.name}")
        else:
            if not context_entry.get("retain_sections"):
                errors.append(f"generated/context_retention_manifest.json retain_sections missing for {skill_dir.name}")

        guardrail_trust_entry = guardrail_trust_by_name.get(skill_dir.name)
        if guardrail_trust_entry is None:
            errors.append(f"generated/repo_trust_gate_manifest.json missing {skill_dir.name}")
        else:
            if source_entry and guardrail_trust_entry.get("invocation_mode") != source_entry.get("invocation_mode"):
                errors.append(f"generated/repo_trust_gate_manifest.json invocation_mode mismatch for {skill_dir.name}")
            if trust_entry is not None and guardrail_trust_entry.get("trust_posture") != trust_entry.get("trust_posture"):
                errors.append(f"generated/repo_trust_gate_manifest.json trust_posture mismatch for {skill_dir.name}")
            if guardrail_trust_entry.get("source_scope") != "repo":
                errors.append(f"generated/repo_trust_gate_manifest.json source_scope mismatch for {skill_dir.name}")

        guardrail_allowlist_entry = guardrail_allowlist_by_name.get(skill_dir.name)
        if guardrail_allowlist_entry is None:
            errors.append(f"generated/permission_allowlist_manifest.json missing {skill_dir.name}")
        else:
            if guardrail_allowlist_entry.get("source_scope") != "repo":
                errors.append(f"generated/permission_allowlist_manifest.json source_scope mismatch for {skill_dir.name}")
            if guardrail_allowlist_entry.get("resource_inventory") != manifest_entry.get("resource_inventory"):
                errors.append(f"generated/permission_allowlist_manifest.json resource_inventory mismatch for {skill_dir.name}")
            if guardrail_allowlist_entry.get("allowlist_id") != f"skill:{skill_dir.name}":
                errors.append(f"generated/permission_allowlist_manifest.json allowlist_id mismatch for {skill_dir.name}")

        guardrail_context_entry = guardrail_context_by_name.get(skill_dir.name)
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

        mcp_entry = mcp_by_name.get(skill_dir.name)
        if mcp_entry is None:
            errors.append(f"generated/mcp_dependency_manifest.json missing {skill_dir.name}")
        else:
            if mcp_entry.get("tools", []) != dependency_tools:
                errors.append(f"generated/mcp_dependency_manifest.json tools mismatch for {skill_dir.name}")

        discovery_entry = discovery_by_name.get(skill_dir.name)
        if discovery_entry is None:
            errors.append(f"generated/runtime_discovery_index.json missing {skill_dir.name}")
        else:
            if discovery_entry.get("path") != skill_md.relative_to(repo_root).as_posix():
                errors.append(f"generated/runtime_discovery_index.json path mismatch for {skill_dir.name}")
            if discovery_entry.get("allow_implicit_invocation") != allow_implicit:
                errors.append(f"generated/runtime_discovery_index.json allow_implicit_invocation mismatch for {skill_dir.name}")
            if discovery_entry.get("invocation_mode") != frontmatter.get("metadata", {}).get("aoa_invocation_mode"):
                errors.append(f"generated/runtime_discovery_index.json invocation_mode mismatch for {skill_dir.name}")
            if "instructions_markdown" in discovery_entry:
                errors.append(f"generated/runtime_discovery_index.json must not expose instructions_markdown for {skill_dir.name}")
            if discovery_entry.get("explicit_handles", {}).get("codex", {}).get("mention") != f"${skill_dir.name}":
                errors.append(f"generated/runtime_discovery_index.json explicit handle mismatch for {skill_dir.name}")

        discovery_min_entry = discovery_min_by_name.get(skill_dir.name)
        if discovery_min_entry is None:
            errors.append(f"generated/runtime_discovery_index.min.json missing {skill_dir.name}")
        else:
            if discovery_min_entry.get("allow_implicit_invocation") != allow_implicit:
                errors.append(f"generated/runtime_discovery_index.min.json allow_implicit_invocation mismatch for {skill_dir.name}")

        disclosure_entry = disclosure_by_name.get(skill_dir.name)
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

        router_entry = router_by_name.get(skill_dir.name)
        if router_entry is None:
            errors.append(f"generated/runtime_router_hints.json missing {skill_dir.name}")
        else:
            if router_entry.get("description") != description:
                errors.append(f"generated/runtime_router_hints.json description mismatch for {skill_dir.name}")

        alias_entry = alias_by_name.get(skill_dir.name)
        if alias_entry is None:
            errors.append(f"generated/runtime_activation_aliases.json missing {skill_dir.name}")
        else:
            if alias_entry.get("codex_mention") != f"${skill_dir.name}":
                errors.append(f"generated/runtime_activation_aliases.json codex_mention mismatch for {skill_dir.name}")
            if alias_entry.get("tool_call", {}).get("arguments", {}).get("skill_name") != skill_dir.name:
                errors.append(f"generated/runtime_activation_aliases.json tool_call mismatch for {skill_dir.name}")

    config_profile_names = set((profile_doc.get("profiles") or {}).keys())
    resolved_profile_names = set((resolved_profiles.get("profiles") or {}).keys())
    snippet_profile_names = set((snippets_doc.get("snippets") or {}).keys())
    if config_profile_names != resolved_profile_names:
        errors.append("resolved profile set does not match config profile set")
    if config_profile_names != snippet_profile_names:
        errors.append("config snippet profile set does not match config profile set")

    for profile_name, profile in (profile_doc.get("profiles") or {}).items():
        seen: set[str] = set()
        for skill_name in profile.get("skills", []):
            if skill_name not in actual_names:
                errors.append(f"config/skill_pack_profiles.json: unknown skill {skill_name!r} in {profile_name}")
            if skill_name in seen:
                errors.append(f"config/skill_pack_profiles.json: duplicate skill {skill_name!r} in {profile_name}")
            seen.add(skill_name)

    for profile_name, profile in (resolved_profiles.get("profiles") or {}).items():
        for entry in profile.get("skills", []):
            if entry.get("name") not in actual_names:
                errors.append(f"generated/skill_pack_profiles.resolved.json: unknown skill {entry.get('name')!r} in {profile_name}")
        snippet = (snippets_doc.get("snippets") or {}).get(profile_name, {})
        disable_profile_toml = snippet.get("disable_profile_toml", "")
        for entry in profile.get("skills", []):
            if entry["target_path"] not in disable_profile_toml:
                errors.append(f"generated/codex_config_snippets.json missing {entry['target_path']!r} in {profile_name}")

    expected_generated_files = set(RELEASE_MANIFEST_GENERATED_FILES)
    if set(release_manifest.get("generated_files", [])) != expected_generated_files:
        errors.append("generated/release_manifest.json generated_files mismatch")
    if release_manifest.get("skill_count") != len(actual_names):
        errors.append("generated/release_manifest.json skill_count mismatch")
    expected_explicit_only = sum(1 for entry in source_by_name.values() if entry.get("invocation_mode") == "explicit-only")
    if release_manifest.get("explicit_only_count") != expected_explicit_only:
        errors.append("generated/release_manifest.json explicit_only_count mismatch")
    if release_manifest.get("profile_count") != len(config_profile_names):
        errors.append("generated/release_manifest.json profile_count mismatch")
    release_identity = release_manifest.get("release_identity", {})
    if release_identity.get("changelog") != "CHANGELOG.md":
        errors.append("generated/release_manifest.json must reference CHANGELOG.md")
    if release_identity.get("releasing_doc") != "docs/RELEASING.md":
        errors.append("generated/release_manifest.json must reference docs/RELEASING.md")
    if release_manifest.get("included_waves") != [1, 2, 3, 4, 6]:
        errors.append("generated/release_manifest.json included_waves must be [1, 2, 3, 4, 6]")

    if runtime_discovery.get("root") != ".agents/skills":
        errors.append("generated/runtime_discovery_index.json root mismatch")
    if runtime_discovery_min.get("root") != ".agents/skills":
        errors.append("generated/runtime_discovery_index.min.json root mismatch")
    if runtime_disclosure.get("root") != ".agents/skills":
        errors.append("generated/runtime_disclosure_index.json root mismatch")

    tool_names = [tool.get("name") for tool in runtime_tool_schemas.get("tools", [])]
    if tool_names != [
        "discover_skills",
        "disclose_skill",
        "activate_skill",
        "skill_session_status",
        "deactivate_skill",
        "compact_skill_session",
    ]:
        errors.append("generated/runtime_tool_schemas.json tool set mismatch")
    if not runtime_prompt_blocks.get("system_prompt_block"):
        errors.append("generated/runtime_prompt_blocks.json missing system_prompt_block")
    if not runtime_prompt_blocks.get("tool_description_block"):
        errors.append("generated/runtime_prompt_blocks.json missing tool_description_block")
    if runtime_session_contract.get("session_file_hint") != ".aoa/skill-runtime-session.json":
        errors.append("generated/runtime_session_contract.json session_file_hint mismatch")

    manifest_tools = runtime_seam_manifest.get("tools", {})
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
    if runtime_seam_manifest.get("common_surface") != ".agents/skills":
        errors.append("generated/runtime_seam_manifest.json common_surface mismatch")
    if runtime_seam_manifest.get("backward_compatibility", {}).get("legacy_activation_tool") != "scripts/activate_skill.py":
        errors.append("generated/runtime_seam_manifest.json legacy activation tool mismatch")
    generated_refs = runtime_seam_manifest.get("generated", {})
    if generated_refs.get("discovery_index") != "generated/runtime_discovery_index.json":
        errors.append("generated/runtime_seam_manifest.json discovery_index mismatch")
    if generated_refs.get("disclosure_index") != "generated/runtime_disclosure_index.json":
        errors.append("generated/runtime_seam_manifest.json disclosure_index mismatch")

    guardrail_tool_names = [tool.get("name") for tool in guardrail_tool_schemas.get("tools", [])]
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
    if not guardrail_prompt_blocks.get("system_prompt_block"):
        errors.append("generated/runtime_guardrail_prompt_blocks.json missing system_prompt_block")
    if not guardrail_prompt_blocks.get("tool_description_block"):
        errors.append("generated/runtime_guardrail_prompt_blocks.json missing tool_description_block")
    if guardrail_manifest.get("common_surface") != ".agents/skills":
        errors.append("generated/runtime_guardrail_manifest.json common_surface mismatch")
    if guardrail_manifest.get("trust_store_hint") != ".aoa/repo-trust-store.json":
        errors.append("generated/runtime_guardrail_manifest.json trust_store_hint mismatch")
    if guardrail_manifest.get("session_file_hint") != ".aoa/skill-runtime-session.json":
        errors.append("generated/runtime_guardrail_manifest.json session_file_hint mismatch")
    if guardrail_manifest.get("downstream_of", {}).get("runtime_seam") != "scripts/skill_runtime_seam.py":
        errors.append("generated/runtime_guardrail_manifest.json runtime_seam mismatch")
    if guardrail_manifest.get("downstream_of", {}).get("legacy_activation_shim") != "scripts/activate_skill.py":
        errors.append("generated/runtime_guardrail_manifest.json legacy_activation_shim mismatch")

    repo_scoped_skills = sorted(
        name for name, entry in guardrail_trust_by_name.items() if entry.get("source_scope") == "repo"
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

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {len(actual_names)} skills in {skills_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
