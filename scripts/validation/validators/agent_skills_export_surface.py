"""Validate the durable source -> portable-export contract for AoA skills."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

import yaml
from jsonschema import Draft202012Validator

from export import portable_skill_export, release_manifest_contract
from skill_model import capability_system, skill_source_model


REQUIRED_GENERATED_FILES = (
    "generated/agent_skill_catalog.json",
    "generated/agent_skill_catalog.min.json",
    "generated/portable_export_map.json",
    "generated/skill_pack_profiles.resolved.json",
    "generated/mcp_dependency_manifest.json",
    "generated/capability_graph.json",
    "generated/capability_graph.md",
    "generated/release_manifest.json",
)
REQUIRED_CONFIG_FILES = (
    "config/portable_skill_overrides.json",
    "config/openai_skill_extensions.json",
    "config/skill_pack_profiles.json",
    "config/skill_policy_matrix.json",
)


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return payload


def parse_skill(path: Path) -> tuple[dict[str, Any], dict[str, str]]:
    metadata, body = skill_source_model.parse_skill_document(path)
    return metadata, skill_source_model.parse_skill_sections(body)


def by_name(rows: Any, *, label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(rows, list):
        raise ValueError(f"{label} must be a list")
    result: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or not isinstance(row.get("name"), str):
            raise ValueError(f"{label}[{index}] must contain a string name")
        name = row["name"]
        if name in result:
            raise ValueError(f"{label} contains duplicate name {name!r}")
        result[name] = row
    return result


def set_difference(label: str, expected: set[str], actual: set[str]) -> str | None:
    if expected == actual:
        return None
    return f"{label} membership mismatch: expected {sorted(expected)!r}, got {sorted(actual)!r}"


def validate_release_schema(repo_root: Path, payload: Mapping[str, Any]) -> list[str]:
    schema = load_json(repo_root / "schemas" / "release_manifest.schema.json")
    return [
        "generated/release_manifest.json "
        + ("/".join(str(part) for part in error.absolute_path) or "<root>")
        + f": {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(payload),
            key=lambda item: list(item.absolute_path),
        )
    ]


def validate_export(repo_root: Path) -> list[str]:
    errors: list[str] = []
    for rel_path in (*REQUIRED_CONFIG_FILES, *REQUIRED_GENERATED_FILES):
        if not (repo_root / rel_path).is_file():
            errors.append(f"missing required file: {rel_path}")
    if errors:
        return errors

    try:
        capability_system.validate_sources(repo_root)
        graph = load_json(repo_root / "generated" / "capability_graph.json")
        overrides = load_json(repo_root / "config" / "portable_skill_overrides.json")
        policies = load_json(repo_root / "config" / "skill_policy_matrix.json")
        profiles = load_json(repo_root / "config" / "skill_pack_profiles.json")
        extensions = load_json(repo_root / "config" / "openai_skill_extensions.json")
        catalog = load_json(repo_root / "generated" / "agent_skill_catalog.json")
        catalog_min = load_json(repo_root / "generated" / "agent_skill_catalog.min.json")
        export_map = load_json(repo_root / "generated" / "portable_export_map.json")
        resolved_profiles = load_json(
            repo_root / "generated" / "skill_pack_profiles.resolved.json"
        )
        mcp_manifest = load_json(repo_root / "generated" / "mcp_dependency_manifest.json")
        release_manifest = load_json(repo_root / "generated" / "release_manifest.json")
    except (OSError, ValueError, capability_system.CapabilityContractError) as exc:
        return [str(exc)]

    sources = {source.name: source for source in skill_source_model.load_skill_sources(repo_root)}
    source_names = set(sources)
    portable_root = repo_root / ".agents" / "skills"
    portable_names = {
        path.name for path in portable_root.iterdir() if path.is_dir()
    } if portable_root.is_dir() else set()

    try:
        catalog_by_name = by_name(catalog.get("skills"), label="agent catalog skills")
        min_by_name = by_name(catalog_min.get("skills"), label="min agent catalog skills")
        export_by_name = by_name(export_map.get("exports"), label="portable export map")
        mcp_by_name = by_name(mcp_manifest.get("skills"), label="MCP dependency manifest")
    except ValueError as exc:
        return [str(exc)]

    memberships = {
        "portable overrides": set((overrides.get("skills") or {}).keys()),
        "policy matrix": set((policies.get("skills") or {}).keys()),
        "agent catalog": set(catalog_by_name),
        "min agent catalog": set(min_by_name),
        "portable export map": set(export_by_name),
        "MCP dependency manifest": set(mcp_by_name),
        ".agents/skills": portable_names,
    }
    for label, actual in memberships.items():
        mismatch = set_difference(label, source_names, actual)
        if mismatch:
            errors.append(mismatch)

    if overrides.get("profile") != portable_skill_export.EXPORT_PROFILE:
        errors.append("portable override profile does not match export builder profile")
    if catalog.get("profile") != portable_skill_export.EXPORT_PROFILE:
        errors.append("agent catalog profile does not match export builder profile")
    if extensions.get("skills") not in ({}, None):
        unknown_extensions = set(extensions.get("skills", {})) - source_names
        if unknown_extensions:
            errors.append(f"OpenAI extensions contain unknown skills: {sorted(unknown_extensions)!r}")

    graph_skill_nodes: dict[str, dict[str, Any]] = {}
    for node in graph.get("nodes", []):
        if not isinstance(node, dict) or node.get("kind") != "skill":
            continue
        binding = node.get("binding")
        if not isinstance(binding, dict):
            continue
        ref = binding.get("ref")
        if isinstance(ref, str) and ref.startswith("skills/"):
            graph_skill_nodes[str(node["id"]).removeprefix("skill.")] = node
    mismatch = set_difference("local capability skill nodes", source_names, set(graph_skill_nodes))
    if mismatch:
        errors.append(mismatch)

    for name, source in sorted(sources.items()):
        override = (overrides.get("skills") or {}).get(name, {})
        policy = (policies.get("skills") or {}).get(name, {})
        if source.metadata.get("description") != override.get("description"):
            errors.append(f"{name}: source and portable routing descriptions differ")

        node = graph_skill_nodes.get(name, {})
        visibility = (node.get("lifecycle") or {}).get("visibility")
        expected_activation = "invoke" if visibility == "advertised" else "suggest"
        invocation_mode = source.metadata.get("invocation_mode")
        if expected_activation == "invoke" and invocation_mode != "implicit-friendly":
            errors.append(
                f"{name}: advertised invocation policy requires implicit-friendly source metadata"
            )
        if expected_activation == "suggest" and invocation_mode == "implicit-friendly":
            errors.append(
                f"{name}: deferred invocation policy cannot use implicit-friendly source metadata"
            )
        if policy.get("implicit_activation_policy") != expected_activation:
            errors.append(
                f"{name}: capability visibility {visibility!r} requires activation policy {expected_activation!r}"
            )

        source_openai_path = source.skill_dir / "agents" / "openai.yaml"
        portable_skill_path = portable_root / name / "SKILL.md"
        portable_openai_path = portable_root / name / "agents" / "openai.yaml"
        if not source_openai_path.is_file() or not portable_skill_path.is_file() or not portable_openai_path.is_file():
            errors.append(f"{name}: missing source or portable package file")
            continue
        source_openai = load_yaml(source_openai_path)
        portable_openai = load_yaml(portable_openai_path)
        source_policy = source_openai.get("policy") or {}
        portable_policy = portable_openai.get("policy") or {}
        expected_allow = expected_activation == "invoke"
        prompt_visible_override = portable_skill_export.with_prompt_visible_activation_policy(
            override,
            policy,
            name,
        )
        if source_policy.get("implicit_activation_policy") != expected_activation:
            errors.append(f"{source_openai_path.relative_to(repo_root)} activation policy drift")
        if source_policy.get("allow_implicit_invocation") != expected_allow:
            errors.append(f"{source_openai_path.relative_to(repo_root)} implicit invocation drift")
        if portable_policy != source_policy:
            errors.append(f"{portable_openai_path.relative_to(repo_root)} policy differs from source")

        portable_metadata, portable_sections = parse_skill(portable_skill_path)
        if portable_metadata.get("name") != name:
            errors.append(f"{portable_skill_path.relative_to(repo_root)} name mismatch")
        if portable_metadata.get("description") != prompt_visible_override.get("description"):
            errors.append(f"{portable_skill_path.relative_to(repo_root)} description mismatch")
        metadata = portable_metadata.get("metadata") or {}
        if "aoa_technique_dependencies" in metadata:
            errors.append(f"{portable_skill_path.relative_to(repo_root)} carries retired technique dependency metadata")
        if metadata.get("aoa_source_skill_path") != source.skill_md_path.relative_to(repo_root).as_posix():
            errors.append(f"{portable_skill_path.relative_to(repo_root)} source path mismatch")
        if portable_sections != source.sections:
            errors.append(f"{portable_skill_path.relative_to(repo_root)} procedure sections differ from source")

        agent_entry = catalog_by_name.get(name, {})
        if agent_entry.get("source_skill_path") != source.skill_md_path.relative_to(repo_root).as_posix():
            errors.append(f"{name}: agent catalog source path mismatch")
        if agent_entry.get("implicit_activation_policy") != expected_activation:
            errors.append(f"{name}: agent catalog activation policy mismatch")
        if bool(agent_entry.get("allow_implicit_invocation")) != expected_allow:
            errors.append(f"{name}: agent catalog implicit invocation mismatch")
        if mcp_by_name.get(name, {}).get("tools"):
            errors.append(f"{name}: portable bundle unexpectedly declares mandatory MCP tools")

    profile_skill_sets: dict[str, list[str]] = {}
    for profile_name, profile in (profiles.get("profiles") or {}).items():
        skill_names = profile.get("skills", [])
        profile_skill_sets[profile_name] = list(skill_names)
        if len(skill_names) != len(set(skill_names)):
            errors.append(f"profile {profile_name!r} contains duplicate skills")
        unknown = set(skill_names) - source_names
        if unknown:
            errors.append(f"profile {profile_name!r} contains unknown skills: {sorted(unknown)!r}")
    if profile_skill_sets.get("repo-default") != ["aoa-decision"]:
        errors.append("repo-default must expose only the advertised aoa-decision family")
    if profile_skill_sets.get("user-default") != ["aoa-decision"]:
        errors.append("user-default must expose only the advertised aoa-decision family")
    source_profiles = profiles.get("profiles") or {}
    if (source_profiles.get("user-default") or {}).get("scope") != "user":
        errors.append("user-default must resolve through the user install scope")
    if (
        (resolved_profiles.get("profiles") or {}).get("user-default", {}).get("install_root")
        != "$HOME/.codex/skills"
    ):
        errors.append("user-default must resolve to the standard Codex user skill root")
    if set(profile_skill_sets.get("repo-capability-sources", [])) != source_names:
        errors.append("repo-capability-sources must contain all seven source bundles")
    resolved_names = set((resolved_profiles.get("profiles") or {}).keys())
    if resolved_names != set(profile_skill_sets):
        errors.append("resolved profile names differ from source profiles")

    errors.extend(validate_release_schema(repo_root, release_manifest))
    try:
        expected_release = release_manifest_contract.build_release_manifest(repo_root)
    except (OSError, ValueError) as exc:
        errors.append(f"could not rebuild release manifest: {exc}")
    else:
        if release_manifest != expected_release:
            errors.append("generated/release_manifest.json is stale")

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = args.repo_root.resolve()
    try:
        errors = validate_export(repo_root)
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"Agent Skills export validation failed: {exc}")
        return 1
    if errors:
        print("Agent Skills export validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Agent Skills export valid: 7 source bundles, 1 advertised, 6 deferred")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
