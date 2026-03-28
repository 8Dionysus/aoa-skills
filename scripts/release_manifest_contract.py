from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping

import skill_relationship_contract


EXPORT_PROFILE = "codex-facing-wave-3"
SKILL_ROOT = ".agents/skills"
RELEASE_MANIFEST_PATH = "generated/release_manifest.json"
CHANGELOG_PATH = "CHANGELOG.md"
RELEASING_DOC_PATH = "docs/RELEASING.md"
TEXT_FILE_SUFFIXES = {
    ".csv",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".svg",
    ".txt",
    ".yaml",
    ".yml",
}
AUTHORING_INPUTS = [
    "generated/skill_sections.full.json",
    "generated/skill_catalog.min.json",
    "config/portable_skill_overrides.json",
    "config/openai_skill_extensions.json",
    "config/skill_pack_profiles.json",
    "config/skill_policy_matrix.json",
    "config/runtime_guardrail_policy.json",
    "config/description_trigger_eval_policy.json",
    "config/tiny_router_skill_bands.json",
]
ARTIFACT_GROUPS = (
    {
        "id": "portable_export",
        "profile": "codex-facing-wave-3",
        "wave": 3,
        "files": [
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
        ],
    },
    {
        "id": "runtime_seam",
        "profile": "codex-facing-wave-4-runtime-seam",
        "wave": 4,
        "files": [
            "generated/runtime_discovery_index.json",
            "generated/runtime_discovery_index.min.json",
            "generated/runtime_disclosure_index.json",
            "generated/runtime_activation_aliases.json",
            "generated/runtime_tool_schemas.json",
            "generated/runtime_session_contract.json",
            "generated/runtime_prompt_blocks.json",
            "generated/runtime_router_hints.json",
            "generated/runtime_seam_manifest.json",
        ],
    },
    {
        "id": "runtime_guardrails",
        "profile": "codex-facing-wave-6-runtime-guardrails",
        "wave": 6,
        "files": [
            "generated/repo_trust_gate_manifest.json",
            "generated/permission_allowlist_manifest.json",
            "generated/skill_context_guard_manifest.json",
            "generated/runtime_guardrail_tool_schemas.json",
            "generated/runtime_guardrail_prompt_blocks.json",
            "generated/runtime_guardrail_manifest.json",
        ],
    },
    {
        "id": "description_trigger",
        "profile": "codex-facing-wave-7-description-trigger-evals",
        "wave": 7,
        "files": [
            "generated/skill_description_signals.json",
            "generated/description_trigger_eval_cases.jsonl",
            "generated/description_trigger_eval_cases.csv",
            "generated/description_trigger_eval_manifest.json",
            "generated/skills_ref_validation_manifest.json",
        ],
    },
    {
        "id": "support_resources",
        "profile": "codex-facing-wave-8-support-bundles",
        "wave": 8,
        "files": [
            "generated/deterministic_resource_manifest.json",
            "generated/support_resource_index.json",
            "generated/structured_output_schema_index.json",
            "generated/support_resource_bridge_map.json",
            "generated/deterministic_resource_eval_cases.jsonl",
            "generated/expected_existing_aoa_support_dirs.json",
        ],
    },
    {
        "id": "tiny_router",
        "profile": "codex-facing-wave-9-tiny-router-inputs",
        "wave": 9,
        "files": [
            "generated/tiny_router_skill_signals.json",
            "generated/tiny_router_candidate_bands.json",
            "generated/tiny_router_capsules.min.json",
            "generated/tiny_router_eval_cases.jsonl",
            "generated/tiny_router_overlay_manifest.json",
        ],
    },
)
ALL_GENERATED_FILES = [
    *(file_path for group in ARTIFACT_GROUPS for file_path in group["files"]),
    *skill_relationship_contract.RELATIONSHIP_VIEW_PATHS,
    RELEASE_MANIFEST_PATH,
]
VERSION_HEADING_RE = re.compile(
    r"^## \[(?P<version>[^\]]+)\](?: - (?P<date>\d{4}-\d{2}-\d{2}))?\s*$",
    re.MULTILINE,
)


def _normalize_override_map(
    repo_root: Path,
    file_overrides: Mapping[str | Path, str] | None,
) -> dict[str, str]:
    normalized: dict[str, str] = {}
    if not file_overrides:
        return normalized
    for raw_path, text in file_overrides.items():
        path = Path(raw_path)
        if path.is_absolute():
            rel_path = path.relative_to(repo_root).as_posix()
        else:
            rel_path = path.as_posix()
        normalized[rel_path] = text
    return normalized


def normalized_file_bytes(path: Path) -> bytes:
    if path.suffix.lower() in TEXT_FILE_SUFFIXES:
        normalized_text = (
            path.read_text(encoding="utf-8")
            .replace("\r\n", "\n")
            .replace("\r", "\n")
        )
        return normalized_text.encode("utf-8")
    return path.read_bytes()


def normalized_text_bytes(text: str) -> bytes:
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def path_bytes(
    repo_root: Path,
    rel_path: str,
    overrides: Mapping[str, str],
) -> bytes:
    if rel_path in overrides:
        return normalized_text_bytes(overrides[rel_path])
    return normalized_file_bytes(repo_root / rel_path)


def load_json_document(
    repo_root: Path,
    rel_path: str,
    overrides: Mapping[str, str],
) -> dict[str, Any]:
    if rel_path in overrides:
        return json.loads(overrides[rel_path])
    return json.loads((repo_root / rel_path).read_text(encoding="utf-8"))


def file_digest_record(
    repo_root: Path,
    rel_path: str,
    overrides: Mapping[str, str],
) -> dict[str, Any]:
    data = path_bytes(repo_root, rel_path, overrides)
    return {
        "path": rel_path,
        "sha256": sha256_bytes(data),
        "bytes": len(data),
    }


def parse_changelog_release_identity(changelog_text: str) -> dict[str, Any]:
    matches = list(VERSION_HEADING_RE.finditer(changelog_text))
    if not matches:
        raise ValueError("CHANGELOG.md has no release headings")

    latest_tagged_version: str | None = None
    latest_tagged_date: str | None = None
    unreleased_start: int | None = None
    unreleased_end: int | None = None

    for index, match in enumerate(matches):
        version = match.group("version")
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(changelog_text)
        if version == "Unreleased":
            unreleased_start = match.end()
            unreleased_end = next_start
            continue
        latest_tagged_version = version
        latest_tagged_date = match.group("date")
        break

    if latest_tagged_version is None or latest_tagged_date is None:
        raise ValueError("CHANGELOG.md is missing a dated tagged release heading")

    unreleased_body = ""
    if unreleased_start is not None and unreleased_end is not None:
        unreleased_body = changelog_text[unreleased_start:unreleased_end].strip()

    return {
        "changelog": CHANGELOG_PATH,
        "releasing_doc": RELEASING_DOC_PATH,
        "latest_tagged_version": latest_tagged_version,
        "latest_tagged_date": latest_tagged_date,
        "has_unreleased_changes": bool(unreleased_body),
    }


def build_skill_bundle_revisions(bundle_index: Mapping[str, Any]) -> list[dict[str, Any]]:
    skills = bundle_index.get("skills", [])
    if not isinstance(skills, list):
        raise ValueError("generated/skill_bundle_index.json field 'skills' must be a list")
    revisions: list[dict[str, Any]] = []
    for entry in skills:
        if not isinstance(entry, Mapping):
            continue
        revisions.append(
            {
                "name": entry["name"],
                "skill_revision": entry["skill_revision"],
                "content_hash": entry["content_hash"],
            }
        )
    return sorted(revisions, key=lambda entry: entry["name"])


def build_install_profile_revisions(
    resolved_profiles: Mapping[str, Any],
    skill_bundle_revisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    profiles = resolved_profiles.get("profiles", {})
    if not isinstance(profiles, Mapping):
        raise ValueError(
            "generated/skill_pack_profiles.resolved.json field 'profiles' must be a mapping"
        )
    revision_by_skill = {
        entry["name"]: entry["skill_revision"] for entry in skill_bundle_revisions
    }
    profile_entries: list[dict[str, Any]] = []
    for profile_name in sorted(profiles):
        profile = profiles[profile_name]
        if not isinstance(profile, Mapping):
            continue
        skills = profile.get("skills", [])
        if not isinstance(skills, list):
            raise ValueError(f"profile {profile_name!r} field 'skills' must be a list")
        skill_names = [entry["name"] for entry in skills if isinstance(entry, Mapping)]
        revision_seed = {
            "name": profile_name,
            "skill_names": skill_names,
            "skill_revisions": [
                {"name": skill_name, "skill_revision": revision_by_skill[skill_name]}
                for skill_name in skill_names
            ],
        }
        profile_entries.append(
            {
                "name": profile_name,
                "skill_count": len(skill_names),
                "skill_names": skill_names,
                "profile_revision": sha256_bytes(
                    json.dumps(
                        revision_seed,
                        ensure_ascii=False,
                        separators=(",", ":"),
                    ).encode("utf-8")
                ),
            }
        )
    return profile_entries


def build_release_manifest(
    repo_root: Path,
    *,
    file_overrides: Mapping[str | Path, str] | None = None,
) -> dict[str, Any]:
    overrides = _normalize_override_map(repo_root, file_overrides)
    agent_catalog = load_json_document(
        repo_root,
        "generated/agent_skill_catalog.json",
        overrides,
    )
    resolved_profiles = load_json_document(
        repo_root,
        "generated/skill_pack_profiles.resolved.json",
        overrides,
    )
    bundle_index = load_json_document(
        repo_root,
        "generated/skill_bundle_index.json",
        overrides,
    )
    changelog_text = (repo_root / CHANGELOG_PATH).read_text(encoding="utf-8")
    skill_entries = agent_catalog.get("skills", [])
    if not isinstance(skill_entries, list):
        raise ValueError("generated/agent_skill_catalog.json field 'skills' must be a list")
    skill_bundle_revisions = build_skill_bundle_revisions(bundle_index)
    install_profile_revisions = build_install_profile_revisions(
        resolved_profiles,
        skill_bundle_revisions,
    )
    return {
        "schema_version": 3,
        "profile": EXPORT_PROFILE,
        "included_waves": [1, 2, *(group["wave"] for group in ARTIFACT_GROUPS)],
        "skill_root": SKILL_ROOT,
        "skill_count": len(skill_entries),
        "explicit_only_count": sum(
            1 for entry in skill_entries if not entry["allow_implicit_invocation"]
        ),
        "profile_count": len((resolved_profiles.get("profiles") or {}).keys()),
        "authoring_inputs": list(AUTHORING_INPUTS),
        "generated_files": list(ALL_GENERATED_FILES),
        "relationship_views": list(skill_relationship_contract.RELATIONSHIP_VIEW_PATHS),
        "artifact_groups": [
            {
                "id": group["id"],
                "profile": group["profile"],
                "wave": group["wave"],
                "files": list(group["files"]),
            }
            for group in ARTIFACT_GROUPS
        ],
        "authoring_input_digests": [
            file_digest_record(repo_root, rel_path, overrides)
            for rel_path in AUTHORING_INPUTS
        ],
        "generated_file_digests": [
            file_digest_record(repo_root, rel_path, overrides)
            for rel_path in ALL_GENERATED_FILES
            if rel_path != RELEASE_MANIFEST_PATH
        ],
        "skill_bundle_revisions": skill_bundle_revisions,
        "install_profile_revisions": install_profile_revisions,
        "release_identity": parse_changelog_release_identity(changelog_text),
    }
