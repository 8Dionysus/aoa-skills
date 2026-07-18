from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence


EXPORT_PROFILE = "codex-facing-v2"
SKILL_ROOT = ".agents/skills"
RELEASE_MANIFEST_PATH = "generated/release_manifest.json"
CHANGELOG_PATH = "CHANGELOG.md"
RELEASING_DOC_PATH = "mechanics/release-support/docs/RELEASING.md"
RELEASE_MANIFEST_SCHEMA_VERSION = 5
RELEASE_MANIFEST_ABI_EPOCH = "aoa_skills_release_manifest_v1"
RELEASE_MANIFEST_TRUST_LAYER = [
    "abi_contract_signature",
    "local_release_provenance",
    "w3c_prov_lineage",
]
STATIC_SOURCE_PATHS = (
    "config/portable_skill_overrides.json",
    "config/openai_skill_extensions.json",
    "config/skill_pack_profiles.json",
    "config/skill_policy_matrix.json",
    "capabilities/legacy-skill-migration.yaml",
    "schemas/capability-home-port.schema.json",
    "schemas/capability_family.schema.json",
    "schemas/capability_graph.schema.json",
    "schemas/skill_migration.schema.json",
    "schemas/task_local_dag.schema.json",
    "schemas/task_local_dag_v2.schema.json",
    "schemas/release_manifest.schema.json",
)
GENERATED_FILES = (
    "generated/agent_skill_catalog.json",
    "generated/agent_skill_catalog.min.json",
    "generated/portable_export_map.json",
    "generated/skill_pack_profiles.resolved.json",
    "generated/mcp_dependency_manifest.json",
    "generated/capability_graph.json",
    "generated/capability_graph.md",
    RELEASE_MANIFEST_PATH,
)
VERSION_HEADING_RE = re.compile(
    r"^## \[(?P<version>[^\]]+)\](?: - (?P<date>\d{4}-\d{2}-\d{2}))?\s*$",
    re.MULTILINE,
)


def has_meaningful_markdown_content(section_text: str) -> bool:
    for raw_line in section_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("<!--") or line.startswith("-->"):
            continue
        if line.startswith("### ") or line in {"-", "*"}:
            continue
        return True
    return False


def _normalize_override_map(
    repo_root: Path,
    file_overrides: Mapping[str | Path, str] | None,
) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for raw_path, text in (file_overrides or {}).items():
        path = Path(raw_path)
        if path.is_absolute():
            path = path.resolve().relative_to(repo_root.resolve())
        normalized[path.as_posix()] = text
    return normalized


def normalized_file_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw
    return normalized_text_bytes(text)


def normalized_text_bytes(text: str) -> bytes:
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def path_bytes(repo_root: Path, rel_path: str, overrides: Mapping[str, str]) -> bytes:
    if rel_path in overrides:
        return normalized_text_bytes(overrides[rel_path])
    return normalized_file_bytes(repo_root / rel_path)


def load_json_document(
    repo_root: Path,
    rel_path: str,
    overrides: Mapping[str, str],
) -> dict[str, Any]:
    payload = json.loads(path_bytes(repo_root, rel_path, overrides).decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{rel_path} must contain a JSON object")
    return payload


def file_digest_record(
    repo_root: Path,
    rel_path: str,
    overrides: Mapping[str, str],
) -> dict[str, Any]:
    data = path_bytes(repo_root, rel_path, overrides)
    return {"path": rel_path, "sha256": sha256_bytes(data), "bytes": len(data)}


def parse_changelog_release_identity(changelog_text: str) -> dict[str, Any]:
    matches = list(VERSION_HEADING_RE.finditer(changelog_text))
    latest_tagged_version: str | None = None
    latest_tagged_date: str | None = None
    unreleased_body = ""
    for index, match in enumerate(matches):
        version = match.group("version")
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(changelog_text)
        if version.lower() == "unreleased":
            unreleased_body = changelog_text[match.end() : next_start].strip()
            continue
        if latest_tagged_version is None:
            latest_tagged_version = version.lstrip("v")
            latest_tagged_date = match.group("date")
    if latest_tagged_version is None or latest_tagged_date is None:
        raise ValueError("CHANGELOG.md must contain a dated tagged release heading")
    return {
        "changelog": CHANGELOG_PATH,
        "releasing_doc": RELEASING_DOC_PATH,
        "latest_tagged_version": latest_tagged_version,
        "latest_tagged_date": latest_tagged_date,
        "has_unreleased_changes": has_meaningful_markdown_content(unreleased_body),
    }


def source_paths(repo_root: Path) -> list[str]:
    paths = list(STATIC_SOURCE_PATHS)
    paths.extend(
        path.relative_to(repo_root).as_posix()
        for path in sorted((repo_root / "capabilities" / "families").glob("*.yaml"))
    )
    for skill_md in sorted((repo_root / "skills").glob("**/SKILL.md")):
        skill_dir = skill_md.parent
        paths.extend(
            path.relative_to(repo_root).as_posix()
            for path in sorted(skill_dir.rglob("*"))
            if path.is_file()
        )
    return sorted(set(paths))


def portable_paths(portable_root: Path) -> list[str]:
    if not portable_root.is_dir():
        return []
    return [
        f"{SKILL_ROOT}/{path.relative_to(portable_root).as_posix()}"
        for path in sorted(portable_root.rglob("*"))
        if path.is_file()
    ]


def _hash_path_set(repo_root: Path, paths: Sequence[str]) -> str:
    digest = hashlib.sha256()
    for rel_path in sorted(paths):
        digest.update(rel_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(normalized_file_bytes(repo_root / rel_path))
        digest.update(b"\0")
    return digest.hexdigest()


def _hash_portable_tree(portable_root: Path, bundle_name: str) -> str:
    bundle_root = portable_root / bundle_name
    digest = hashlib.sha256()
    for path in sorted(bundle_root.rglob("*")):
        if not path.is_file():
            continue
        logical_path = (
            Path(SKILL_ROOT) / bundle_name / path.relative_to(bundle_root)
        ).as_posix()
        digest.update(logical_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(normalized_file_bytes(path))
        digest.update(b"\0")
    return digest.hexdigest()


def portable_file_digest_record(
    portable_root: Path,
    logical_path: str,
) -> dict[str, Any]:
    relative = Path(logical_path).relative_to(SKILL_ROOT)
    data = normalized_file_bytes(portable_root / relative)
    return {"path": logical_path, "sha256": sha256_bytes(data), "bytes": len(data)}


def build_skill_bundle_revisions(
    repo_root: Path,
    agent_catalog: Mapping[str, Any],
    portable_root: Path,
) -> list[dict[str, Any]]:
    skills = agent_catalog.get("skills", [])
    if not isinstance(skills, list):
        raise ValueError("generated/agent_skill_catalog.json field 'skills' must be a list")
    revisions: list[dict[str, Any]] = []
    for entry in skills:
        if not isinstance(entry, Mapping):
            continue
        name = str(entry["name"])
        source_skill_path = str(entry["source_skill_path"])
        source_dir = (repo_root / source_skill_path).parent
        source_files = [
            path.relative_to(repo_root).as_posix()
            for path in sorted(source_dir.rglob("*"))
            if path.is_file()
        ]
        source_hash = _hash_path_set(repo_root, source_files)
        portable_hash = _hash_portable_tree(portable_root, name)
        revisions.append(
            {
                "name": name,
                "skill_revision": source_hash[:12],
                "source_hash": source_hash,
                "portable_hash": portable_hash,
            }
        )
    return sorted(revisions, key=lambda item: item["name"])


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
    result: list[dict[str, Any]] = []
    for profile_name in sorted(profiles):
        profile = profiles[profile_name]
        if not isinstance(profile, Mapping):
            continue
        skill_names = sorted(
            str(entry["name"])
            for entry in profile.get("skills", [])
            if isinstance(entry, Mapping)
        )
        seed = {
            "name": profile_name,
            "skill_revisions": [
                {"name": name, "skill_revision": revision_by_skill[name]}
                for name in skill_names
            ],
        }
        result.append(
            {
                "name": profile_name,
                "skill_count": len(skill_names),
                "skill_names": skill_names,
                "profile_revision": sha256_bytes(
                    json.dumps(seed, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
                        "utf-8"
                    )
                ),
            }
        )
    return result


def release_manifest_artifact_identity() -> dict[str, Any]:
    return {
        "artifact_class": "aoa_skills_release_manifest",
        "surface_state": "generated_portable_skill_export_release_contract",
        "owner_repo": "aoa-skills",
        "authority_ref": "mechanics/release-support/docs/CODEX_PORTABLE_LAYER.md",
        "producer": "scripts/export/build_agent_skills.py from authored skill, capability, profile, and export sources",
        "consumer_expectation": "Verify schema, source and generated digests, portable bundle hashes, profile revisions, and release identity before admission.",
        "privacy_boundary": "Public-safe owner source and deterministic export metadata only; no session evidence or live runtime state.",
        "content_identity": "generated/release_manifest.json validated by schemas/release_manifest.schema.json",
        "abi_epoch": RELEASE_MANIFEST_ABI_EPOCH,
        "contract_version": (
            "schemas/release_manifest.schema.json@"
            f"{RELEASE_MANIFEST_ABI_EPOCH}#artifact_identity"
        ),
        "trust_layer": list(RELEASE_MANIFEST_TRUST_LAYER),
        "verification": [
            "PYTHONPATH=scripts python scripts/builders/build_capability_graph.py --repo-root .",
            "PYTHONPATH=scripts python scripts/export/build_agent_skills.py --repo-root .",
            "PYTHONPATH=scripts python scripts/validation/validate_agent_skills.py --repo-root .",
        ],
        "action": "VERIFY_BEFORE_ADMISSION",
    }


def build_release_manifest(
    repo_root: Path,
    *,
    portable_root: Path,
    file_overrides: Mapping[str | Path, str] | None = None,
) -> dict[str, Any]:
    overrides = _normalize_override_map(repo_root, file_overrides)
    agent_catalog = load_json_document(
        repo_root, "generated/agent_skill_catalog.json", overrides
    )
    resolved_profiles = load_json_document(
        repo_root, "generated/skill_pack_profiles.resolved.json", overrides
    )
    graph = load_json_document(repo_root, "generated/capability_graph.json", overrides)
    skill_entries = agent_catalog.get("skills", [])
    if not isinstance(skill_entries, list):
        raise ValueError("generated/agent_skill_catalog.json field 'skills' must be a list")
    portable_root = portable_root.resolve()
    revisions = build_skill_bundle_revisions(repo_root, agent_catalog, portable_root)
    profiles = build_install_profile_revisions(resolved_profiles, revisions)
    authored = source_paths(repo_root)
    portable = portable_paths(portable_root)
    generated = list(GENERATED_FILES)
    artifact_groups = [
        {
            "id": "portable-skill-pack",
            "profile": EXPORT_PROFILE,
            "files": sorted(
                portable
                + [
                    "generated/agent_skill_catalog.json",
                    "generated/agent_skill_catalog.min.json",
                    "generated/portable_export_map.json",
                    "generated/skill_pack_profiles.resolved.json",
                    "generated/mcp_dependency_manifest.json",
                ]
            ),
        },
        {
            "id": "capability-model",
            "profile": str(graph.get("schema_version", "aoa-capability-graph-v1")),
            "files": [
                "generated/capability_graph.json",
                "generated/capability_graph.md",
            ],
        },
    ]
    changelog_text = (repo_root / CHANGELOG_PATH).read_text(encoding="utf-8")
    return {
        "schema_version": RELEASE_MANIFEST_SCHEMA_VERSION,
        "artifact_identity": release_manifest_artifact_identity(),
        "profile": EXPORT_PROFILE,
        "skill_root": SKILL_ROOT,
        "skill_count": len(skill_entries),
        "advertised_skill_count": sum(
            1 for entry in skill_entries if entry.get("implicit_activation_policy") == "invoke"
        ),
        "deferred_skill_count": sum(
            1 for entry in skill_entries if entry.get("implicit_activation_policy") == "suggest"
        ),
        "profile_count": len((resolved_profiles.get("profiles") or {}).keys()),
        "source_files": authored,
        "portable_files": portable,
        "generated_files": generated,
        "artifact_groups": artifact_groups,
        "source_file_digests": [
            file_digest_record(repo_root, path, overrides) for path in authored
        ],
        "portable_file_digests": [
            portable_file_digest_record(portable_root, path) for path in portable
        ],
        "generated_file_digests": [
            file_digest_record(repo_root, path, overrides)
            for path in generated
            if path != RELEASE_MANIFEST_PATH
        ],
        "skill_bundle_revisions": revisions,
        "install_profile_revisions": profiles,
        "release_identity": parse_changelog_release_identity(changelog_text),
    }
