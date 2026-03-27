#!/usr/bin/env python3
"""Build wave-6 runtime guardrail artifacts.

This layer wraps the raw runtime seam with three quiet constraints:
- trust-gate repo-scoped skills before disclosure or activation
- resolve read-only allowlists for bundled skill resources
- protect active skill context from compaction and duplicate reinjection
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from datetime import datetime, timezone
from typing import Any

import yaml

PROFILE = "codex-facing-wave-6-runtime-guardrails"
TRUST_STORE_HINT = ".aoa/repo-trust-store.json"
SESSION_FILE_HINT = ".aoa/skill-runtime-session.json"
JSON_INDENT = 2
GUARDRAIL_GENERATED_FILES = [
    "generated/repo_trust_gate_manifest.json",
    "generated/permission_allowlist_manifest.json",
    "generated/skill_context_guard_manifest.json",
    "generated/runtime_guardrail_tool_schemas.json",
    "generated/runtime_guardrail_prompt_blocks.json",
    "generated/runtime_guardrail_manifest.json",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(data: Any) -> str:
    return json.dumps(data, indent=JSON_INDENT, ensure_ascii=False) + "\n"


def render_or_check(path: pathlib.Path, text: str, check: bool) -> None:
    if check:
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != text:
            raise SystemExit(f"wave-6 guardrail drift: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


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


def source_scope_for_path(path: str) -> str:
    if path.startswith(".agents/skills/"):
        return "repo"
    if path.startswith("/etc/codex/skills/"):
        return "admin"
    if path.startswith("$HOME/.agents/skills/") or path.startswith("~/.agents/skills/"):
        return "user"
    return "repo"


def instruction_digest(skill_md: pathlib.Path) -> str:
    _, body = parse_frontmatter(skill_md)
    return hashlib.sha256(body.strip().encode("utf-8")).hexdigest()


def allowlist_templates(name: str) -> dict[str, list[str]]:
    rel_base = f".agents/skills/{name}"
    repo_base = f"$REPO_ROOT/{rel_base}"
    user_base = f"$HOME/.agents/skills/{name}"
    admin_base = f"/etc/codex/skills/{name}"
    suffixes = ["", "/scripts", "/references", "/assets"]
    return {
        "repo": [repo_base + suffix for suffix in suffixes],
        "user": [user_base + suffix for suffix in suffixes],
        "admin": [admin_base + suffix for suffix in suffixes],
    }


def trust_gate_entry(entry: dict[str, Any], source_scope: str) -> dict[str, Any]:
    return {
        "name": entry["name"],
        "display_name": entry["display_name"],
        "description": entry["description"],
        "source_scope": source_scope,
        "trust_posture": entry["trust_posture"],
        "mutation_surface": entry["mutation_surface"],
        "invocation_mode": entry["invocation_mode"],
        "recommended_install_scopes": entry.get("recommended_install_scopes", []),
        "scope_policy": {
            "repo": "require-trusted-repo",
            "user": "allow",
            "admin": "allow",
            "system": "allow",
        },
        "default_behavior_when_untrusted": "hide-on-discover block-on-disclose block-on-activate",
        "notes": (
            "Repo-scoped skills stay dark until the repository is explicitly trusted. "
            "The same skill may be installed at user/admin scope without repo trust gating."
        ),
    }


def allowlist_entry(entry: dict[str, Any], source_scope: str) -> dict[str, Any]:
    templates = allowlist_templates(entry["name"])
    rel_base = f".agents/skills/{entry['name']}"
    return {
        "name": entry["name"],
        "display_name": entry["display_name"],
        "source_scope": source_scope,
        "allowlist_id": f"skill:{entry['name']}",
        "read_access": "read-only",
        "merge_strategy": "union-active-skills",
        "path_templates": templates,
        "repo_relative_paths": [
            rel_base,
            f"{rel_base}/scripts",
            f"{rel_base}/references",
            f"{rel_base}/assets",
        ],
        "resource_inventory": entry.get("resource_inventory", {}),
        "notes": (
            "List bundled resources without eager reads. Local wrappers should allow read access "
            "to these directories so scripts, references, and assets do not trigger per-file permission prompts."
        ),
    }


def context_guard_entry(
    entry: dict[str, Any],
    source_scope: str,
    digest: str,
    context_entry: dict[str, Any],
    alias_doc: dict[str, Any],
) -> dict[str, Any]:
    codex_mention = alias_doc.get("codex_mention", f"${entry['name']}")
    return {
        "name": entry["name"],
        "display_name": entry["display_name"],
        "source_scope": source_scope,
        "instruction_sha256": digest,
        "dedupe_key": f"{entry['name']}:{digest}",
        "protect_from_compaction": True,
        "pin_strategy": "protected-tool-output",
        "reactivation_strategy": "compact-packet-then-activate",
        "compact_summary": context_entry.get("compact_summary", entry["short_description"]),
        "must_keep": context_entry.get("must_keep", []),
        "retain_sections": context_entry.get("retain_sections", []),
        "rehydration_hint": context_entry.get("rehydration_hint", "Reload the skill before resuming."),
        "activation_card_markdown": context_entry.get("activation_card_markdown"),
        "reactivation_call": {
            "name": "guarded_activate_skill",
            "arguments": {
                "skill_name": entry["name"],
                "explicit_handle": codex_mention,
                "session_file": SESSION_FILE_HINT,
            },
        },
    }


def build_prompt_blocks(discovery_min: list[dict[str, Any]]) -> dict[str, Any]:
    lines_xml = ["<available_guarded_skills>"]
    lines_md = ["Available guarded AoA skills:"]
    for entry in discovery_min:
        lines_xml.extend(
            [
                "  <skill>",
                f"    <name>{entry['name']}</name>",
                f"    <description>{entry['description']}</description>",
                "    <repo_scope_requires_trust>true</repo_scope_requires_trust>",
                "  </skill>",
            ]
        )
        lines_md.append(f"- {entry['name']}: {entry['description']}")
    lines_xml.append("</available_guarded_skills>")

    behavior = [
        "Before exposing repo-scoped skills, check whether the repository is trusted.",
        "If the repository is untrusted, do not disclose or activate repo-scoped skills. Ask the user to trust the repo explicitly first.",
        "When a skill activates, carry forward a read-only allowlist for its bundled resource directories.",
        "Treat activated skill packets as protected during context compaction.",
        "Deduplicate reinjection by skill name plus instruction digest. If the same skill is already active, reuse the existing context packet.",
        "Use rehydrate_skill_context or guarded_activate_skill to restore skill context after compaction or long-running sessions.",
        "",
        *lines_md,
    ]
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "behavioral_instructions": behavior,
        "catalog_xml": "\n".join(lines_xml),
        "catalog_markdown": "\n".join(lines_md),
        "system_prompt_block": "\n".join(behavior + ["", *lines_xml]),
        "tool_description_block": "\n".join(
            [
                "Governed AoA runtime seam with repo trust gating, read-only permission allowlists, and compaction-safe skill context.",
                "Use guarded_discover_skills and guarded_activate_skill instead of the raw runtime seam when the repo may be untrusted or the session is long-lived.",
                "",
                *lines_md,
            ]
        ),
    }


def build_tool_schemas(skill_names: list[str]) -> dict[str, Any]:
    tools = [
        {
            "name": "guarded_discover_skills",
            "description": "Discover AoA skills through a trust-gated catalog. Repo-scoped skills stay hidden until the repository is trusted.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "trust_store": {"type": "string"},
                    "repo_trusted": {"type": "string", "enum": ["auto", "true", "false"]},
                    "include_blocked": {"type": "boolean"},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 100},
                },
                "additionalProperties": False,
            },
            "output_ref": "scripts/skill_runtime_guardrails.py discover",
        },
        {
            "name": "guarded_disclose_skill",
            "description": "Preview a skill through the trust gate. Returns a blocked payload instead of disclosing skill internals when the repo is untrusted.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "skill_name": {"type": "string", "enum": skill_names},
                    "trust_store": {"type": "string"},
                    "repo_trusted": {"type": "string", "enum": ["auto", "true", "false"]},
                },
                "required": ["skill_name"],
                "additionalProperties": False,
            },
            "output_ref": "scripts/skill_runtime_guardrails.py disclose",
        },
        {
            "name": "guarded_activate_skill",
            "description": "Activate a skill with repo trust enforcement, read-only allowlist resolution, and compaction-safe session tracking.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "skill_name": {"type": "string", "enum": skill_names},
                    "session_file": {"type": "string"},
                    "explicit_handle": {"type": "string"},
                    "trust_store": {"type": "string"},
                    "repo_trusted": {"type": "string", "enum": ["auto", "true", "false"]},
                    "include_frontmatter": {"type": "boolean"},
                    "wrap_mode": {"type": "string", "enum": ["structured", "markdown", "raw"]},
                },
                "required": ["skill_name"],
                "additionalProperties": False,
            },
            "output_ref": "scripts/skill_runtime_guardrails.py activate",
        },
        {
            "name": "guarded_skill_session_status",
            "description": "Show the current governed skill session, including trust state, pinned skill packets, and allowlist coverage.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "session_file": {"type": "string"},
                    "trust_store": {"type": "string"},
                    "repo_trusted": {"type": "string", "enum": ["auto", "true", "false"]},
                },
                "required": ["session_file"],
                "additionalProperties": False,
            },
            "output_ref": "scripts/skill_runtime_guardrails.py status",
        },
        {
            "name": "repo_trust_gate",
            "description": "Read or update the trust decision for the current repository before repo-scoped skills become visible.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "trust_store": {"type": "string"},
                    "decision": {"type": "string", "enum": ["trusted", "untrusted", "clear"]},
                    "reason": {"type": "string"},
                },
                "additionalProperties": False,
            },
            "output_ref": "scripts/skill_runtime_guardrails.py trust",
        },
        {
            "name": "resolve_skill_allowlist",
            "description": "Resolve the read-only allowlist paths for one skill or the currently active governed skill session.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "skill_name": {"type": "string", "enum": skill_names},
                    "session_file": {"type": "string"},
                    "adapter": {"type": "string", "enum": ["generic", "local-shell", "codex-local", "codex-worktree"]},
                },
                "additionalProperties": False,
            },
            "output_ref": "scripts/skill_runtime_guardrails.py allowlist",
        },
        {
            "name": "guarded_compact_skill_session",
            "description": "Emit protected compaction packets for the governed skill session, carrying trust state, allowlist paths, and dedupe keys.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "session_file": {"type": "string"},
                },
                "required": ["session_file"],
                "additionalProperties": False,
            },
            "output_ref": "scripts/skill_runtime_guardrails.py compact",
        },
        {
            "name": "rehydrate_skill_context",
            "description": "Rebuild the minimal rehydration packets and suggested activation calls for active governed skills after compaction.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "session_file": {"type": "string"},
                    "skill_name": {"type": "string", "enum": skill_names},
                    "include_activation_call": {"type": "boolean"},
                },
                "required": ["session_file"],
                "additionalProperties": False,
            },
            "output_ref": "scripts/skill_runtime_guardrails.py rehydrate",
        },
    ]
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "tools": tools,
    }


def build_release_manifest(
    existing: dict[str, Any],
    generated_files: list[str],
    skill_count: int,
    explicit_only_count: int,
    profile_count: int,
) -> dict[str, Any]:
    waves: list[int] = []
    for wave in existing.get("included_waves", []):
        if wave == 5:
            continue
        if wave not in waves:
            waves.append(wave)
    if 6 not in waves:
        waves.append(6)
    return {
        "schema_version": 1,
        "profile": existing.get("profile", "codex-facing-wave-3"),
        "included_waves": waves,
        "skill_root": existing.get("skill_root", ".agents/skills"),
        "skill_count": skill_count,
        "explicit_only_count": explicit_only_count,
        "profile_count": profile_count,
        "authoring_inputs": existing.get(
            "authoring_inputs",
            [
                "generated/skill_sections.full.json",
                "generated/skill_catalog.min.json",
                "config/portable_skill_overrides.json",
                "config/openai_skill_extensions.json",
                "config/skill_pack_profiles.json",
                "config/skill_policy_matrix.json",
            ],
        ),
        "generated_files": generated_files,
        "release_identity": existing.get(
            "release_identity",
            {
                "changelog": "CHANGELOG.md",
                "releasing_doc": "docs/RELEASING.md",
            },
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    generated_dir = repo_root / "generated"
    config_dir = repo_root / "config"

    catalog = load_json(generated_dir / "agent_skill_catalog.json")
    runtime_discovery = load_json(generated_dir / "runtime_discovery_index.json")
    runtime_aliases = load_json(generated_dir / "runtime_activation_aliases.json")
    context_retention = load_json(generated_dir / "context_retention_manifest.json")
    release_existing = load_json(generated_dir / "release_manifest.json")
    guardrail_policy = load_json(config_dir / "runtime_guardrail_policy.json")
    profile_count = len(load_json(config_dir / "skill_pack_profiles.json").get("profiles", []))

    alias_by_name = {entry["name"]: entry for entry in runtime_aliases.get("aliases", [])}
    context_by_name = {entry["name"]: entry for entry in context_retention.get("skills", [])}

    trust_entries: list[dict[str, Any]] = []
    allowlist_entries: list[dict[str, Any]] = []
    context_entries: list[dict[str, Any]] = []
    discovery_min = runtime_discovery.get("skills", [])

    for entry in catalog.get("skills", []):
        skill_md = repo_root / entry["path"]
        digest = instruction_digest(skill_md)
        source_scope = source_scope_for_path(entry["path"])
        trust_entries.append(trust_gate_entry(entry, source_scope))
        allowlist_entries.append(allowlist_entry(entry, source_scope))
        context_entries.append(
            context_guard_entry(
                entry,
                source_scope,
                digest,
                context_by_name.get(entry["name"], {}),
                alias_by_name.get(entry["name"], {}),
            )
        )

    trust_gate_doc = {
        "schema_version": 1,
        "profile": PROFILE,
        "trust_store_hint": TRUST_STORE_HINT,
        "description": "Repo trust gate for AoA skills. Repo-scoped skills are hidden and blocked until the repository is explicitly trusted.",
        "matching": {
            "repo_identity_fields": ["repo_root", "git_origin_url"],
            "decision_values": ["trusted", "untrusted"],
            "default_decision": "untrusted",
        },
        "default_scope_policy": guardrail_policy["trust_gate"],
        "skills": trust_entries,
    }

    allowlist_doc = {
        "schema_version": 1,
        "profile": PROFILE,
        "description": "Read-only path allowlists for skill resource directories. Union the paths for active skills and keep them readable without per-file prompts.",
        "adapter_notes": guardrail_policy["permission_allowlist"],
        "skills": allowlist_entries,
    }

    context_guard_doc = {
        "schema_version": 1,
        "profile": PROFILE,
        "description": "Compaction-safe skill packets and reinjection dedupe rules for long-running local sessions.",
        "policy": guardrail_policy["context_guard"],
        "skills": context_entries,
    }

    prompt_blocks_doc = build_prompt_blocks(discovery_min)
    tool_schemas_doc = build_tool_schemas([entry["name"] for entry in catalog.get("skills", [])])
    guardrail_manifest_doc = {
        "schema_version": 1,
        "profile": PROFILE,
        "common_surface": ".agents/skills",
        "downstream_of": {
            "runtime_seam": "scripts/skill_runtime_seam.py",
            "legacy_activation_shim": "scripts/activate_skill.py",
        },
        "tools": {
            "discover": "scripts/skill_runtime_guardrails.py discover",
            "disclose": "scripts/skill_runtime_guardrails.py disclose",
            "activate": "scripts/skill_runtime_guardrails.py activate",
            "status": "scripts/skill_runtime_guardrails.py status",
            "trust": "scripts/skill_runtime_guardrails.py trust",
            "allowlist": "scripts/skill_runtime_guardrails.py allowlist",
            "compact": "scripts/skill_runtime_guardrails.py compact",
            "rehydrate": "scripts/skill_runtime_guardrails.py rehydrate",
        },
        "generated": {
            "repo_trust_gate": "generated/repo_trust_gate_manifest.json",
            "permission_allowlist": "generated/permission_allowlist_manifest.json",
            "skill_context_guard": "generated/skill_context_guard_manifest.json",
            "tool_schemas": "generated/runtime_guardrail_tool_schemas.json",
            "prompt_blocks": "generated/runtime_guardrail_prompt_blocks.json",
            "manifest": "generated/runtime_guardrail_manifest.json",
        },
        "trust_store_hint": TRUST_STORE_HINT,
        "session_file_hint": SESSION_FILE_HINT,
        "notes": [
            "Use this governance layer for local-friendly adapters that need repo trust, permission allowlists, and compaction-safe skill retention.",
            "The raw runtime seam remains available for debugging and backward compatibility.",
        ],
    }

    generated_files = list(dict.fromkeys(list(release_existing.get("generated_files", [])) + GUARDRAIL_GENERATED_FILES))
    release_doc = build_release_manifest(
        existing=release_existing,
        generated_files=generated_files,
        skill_count=len(catalog.get("skills", [])),
        explicit_only_count=sum(1 for entry in catalog.get("skills", []) if entry["invocation_mode"] == "explicit-only"),
        profile_count=profile_count,
    )

    example_trust_store = {
        "schema_version": 1,
        "description": "Example trust store for guarded AoA runtime skill loading.",
        "entries": [
            {
                "repo_root": "/absolute/path/to/repository",
                "git_origin_url": "git@github.com:8Dionysus/aoa-skills.git",
                "repo_id": "replace-with-runtime-computed-id",
                "decision": "trusted",
                "reason": "Reviewed repo-local skills and accepted them for activation.",
                "updated_at": "2026-03-26T00:00:00Z",
            }
        ],
    }

    example_allowlist = {
        "schema_version": 1,
        "description": "Example merged read-only allowlist for two active skills.",
        "adapter": "generic",
        "skills": ["aoa-change-protocol", "aoa-contract-test"],
        "paths": [
            "$REPO_ROOT/.agents/skills/aoa-change-protocol",
            "$REPO_ROOT/.agents/skills/aoa-change-protocol/scripts",
            "$REPO_ROOT/.agents/skills/aoa-change-protocol/references",
            "$REPO_ROOT/.agents/skills/aoa-contract-test",
            "$REPO_ROOT/.agents/skills/aoa-contract-test/scripts",
            "$REPO_ROOT/.agents/skills/aoa-contract-test/references",
        ],
        "read_access": "read-only",
    }

    example_runtime_config = {
        "schema_version": 1,
        "description": "Example local adapter config for the governed seam.",
        "repo_trust_store": TRUST_STORE_HINT,
        "skill_session_file": SESSION_FILE_HINT,
        "trust_gate_mode": "enforce",
        "allowlist_mode": "read-only",
        "context_guard_mode": "protect-and-rehydrate",
    }

    file_map = {
        generated_dir / "repo_trust_gate_manifest.json": dump_json(trust_gate_doc),
        generated_dir / "permission_allowlist_manifest.json": dump_json(allowlist_doc),
        generated_dir / "skill_context_guard_manifest.json": dump_json(context_guard_doc),
        generated_dir / "runtime_guardrail_tool_schemas.json": dump_json(tool_schemas_doc),
        generated_dir / "runtime_guardrail_prompt_blocks.json": dump_json(prompt_blocks_doc),
        generated_dir / "runtime_guardrail_manifest.json": dump_json(guardrail_manifest_doc),
        generated_dir / "release_manifest.json": dump_json(release_doc),
        repo_root / "examples" / "repo-trust-store.json": dump_json(example_trust_store),
        repo_root / "examples" / "permission-allowlist.json": dump_json(example_allowlist),
        repo_root / "examples" / "guardrailed-runtime-config.json": dump_json(example_runtime_config),
    }

    for path, text in file_map.items():
        render_or_check(path, text, args.check)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
