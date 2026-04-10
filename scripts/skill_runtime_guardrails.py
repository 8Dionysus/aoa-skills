#!/usr/bin/env python3
"""Governed runtime seam for AoA skills.

This layer wraps the raw runtime seam with repo trust gating, read-only
permission allowlists for bundled skill resources, and compaction-safe skill
context retention.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from datetime import datetime, timezone
from typing import Any

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from skill_runtime_seam import (  # noqa: E402
    DEFAULT_WRAP_MODE,
    activate_payload as raw_activate_payload,
    compact_payload as raw_compact_payload,
    disclose_payload as raw_disclose_payload,
    discover_payload as raw_discover_payload,
    dump_json,
    load_indexes,
    load_session,
    print_markdown_activate,
    print_markdown_disclose,
    print_markdown_discover,
    print_markdown_generic,
    save_session,
    status_payload as raw_status_payload,
)

PROFILE = "codex-facing-wave-6-runtime-guardrails"
TRUST_STORE_HINT = ".aoa/repo-trust-store.json"
SESSION_FILE_HINT = ".aoa/skill-runtime-session.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_optional_json(path: pathlib.Path, default: Any) -> Any:
    if path.exists():
        return load_json(path)
    return default


def find_repo_root_from_args(repo_root: str) -> pathlib.Path:
    return pathlib.Path(repo_root).resolve()


def default_trust_store_path(repo_root: pathlib.Path) -> pathlib.Path:
    return repo_root / TRUST_STORE_HINT


def empty_trust_store() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "entries": [],
    }


def load_trust_store(path: pathlib.Path) -> dict[str, Any]:
    if path.exists():
        return load_json(path)
    return empty_trust_store()


def save_trust_store(path: pathlib.Path, store: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_json(store), encoding="utf-8")


def resolve_git_dir(repo_root: pathlib.Path) -> pathlib.Path | None:
    dot_git = repo_root / ".git"
    if dot_git.is_dir():
        return dot_git
    if dot_git.is_file():
        first_line = dot_git.read_text(encoding="utf-8").splitlines()[0].strip()
        if first_line.startswith("gitdir:"):
            gitdir = first_line.split(":", 1)[1].strip()
            return (repo_root / gitdir).resolve()
    return None


def parse_git_origin(repo_root: pathlib.Path) -> str | None:
    git_dir = resolve_git_dir(repo_root)
    if git_dir is None:
        return None
    config_path = git_dir / "config"
    if not config_path.exists():
        return None
    current_remote = None
    for raw_line in config_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("[remote "):
            match = re.match(r'^\[remote "([^"]+)"\]$', line)
            current_remote = match.group(1) if match else None
            continue
        if current_remote == "origin" and line.startswith("url = "):
            return line.split("=", 1)[1].strip()
    return None


def repo_identity(repo_root: pathlib.Path) -> dict[str, Any]:
    git_origin_url = parse_git_origin(repo_root)
    repo_root_str = str(repo_root.resolve())
    raw_id = f"{repo_root_str}|{git_origin_url or ''}"
    repo_id = hashlib.sha256(raw_id.encode("utf-8")).hexdigest()[:24]
    return {
        "repo_root": repo_root_str,
        "repo_id": repo_id,
        "git_origin_url": git_origin_url,
    }


def find_matching_trust_entry(store: dict[str, Any], identity: dict[str, Any]) -> dict[str, Any] | None:
    entries = store.get("entries", [])
    repo_id = identity.get("repo_id")
    if repo_id:
        for entry in entries:
            if entry.get("repo_id") == repo_id:
                return entry
    repo_root = identity.get("repo_root")
    git_origin_url = identity.get("git_origin_url")
    if repo_root and git_origin_url:
        for entry in entries:
            if entry.get("repo_root") == repo_root and entry.get("git_origin_url") == git_origin_url:
                return entry
    if git_origin_url:
        for entry in entries:
            if entry.get("git_origin_url") == git_origin_url:
                if not entry.get("repo_root") or entry.get("repo_root") == repo_root:
                    return entry
    if repo_root and not git_origin_url:
        for entry in entries:
            if entry.get("repo_root") == repo_root and not entry.get("git_origin_url"):
                return entry
    return None


def resolve_repo_trust(
    repo_root: pathlib.Path,
    trust_store_path: pathlib.Path | None = None,
    repo_trusted: str = "auto",
) -> dict[str, Any]:
    identity = repo_identity(repo_root)
    trust_store = (trust_store_path or default_trust_store_path(repo_root)).resolve()
    effective: bool
    decision_source: str
    entry = None
    if repo_trusted == "true":
        effective = True
        decision_source = "cli-override"
    elif repo_trusted == "false":
        effective = False
        decision_source = "cli-override"
    else:
        store = load_trust_store(trust_store)
        entry = find_matching_trust_entry(store, identity)
        if entry and entry.get("decision") == "trusted":
            effective = True
            decision_source = "trust-store"
        elif entry and entry.get("decision") == "untrusted":
            effective = False
            decision_source = "trust-store"
        else:
            effective = False
            decision_source = "default-untrusted"
    return {
        "repo_trusted": effective,
        "decision_source": decision_source,
        "trust_store_path": str(trust_store),
        "repo_identity": identity,
        "matching_entry": entry,
        "blocked_source_scopes": [] if effective else ["repo"],
        "allowed_source_scopes": ["user", "admin", "system"] + (["repo"] if effective else []),
    }


def load_guardrails(repo_root: pathlib.Path) -> dict[str, Any]:
    generated_dir = repo_root / "generated"
    docs = load_indexes(repo_root)
    repo_trust_gate = load_optional_json(
        generated_dir / "repo_trust_gate_manifest.json",
        {"schema_version": 1, "skills": []},
    )
    permission_allowlist = load_optional_json(
        generated_dir / "permission_allowlist_manifest.json",
        {"schema_version": 1, "skills": []},
    )
    skill_context_guard = load_optional_json(
        generated_dir / "skill_context_guard_manifest.json",
        {"schema_version": 1, "skills": []},
    )
    runtime_guardrail_prompt_blocks = load_optional_json(
        generated_dir / "runtime_guardrail_prompt_blocks.json",
        {"schema_version": 1, "behavioral_instructions": []},
    )
    runtime_guardrail_tool_schemas = load_optional_json(
        generated_dir / "runtime_guardrail_tool_schemas.json",
        {"schema_version": 1, "tools": []},
    )
    runtime_guardrail_manifest = load_optional_json(
        generated_dir / "runtime_guardrail_manifest.json",
        {"schema_version": 1},
    )
    docs.update(
        {
            "repo_trust_gate": repo_trust_gate,
            "permission_allowlist": permission_allowlist,
            "skill_context_guard": skill_context_guard,
            "runtime_guardrail_prompt_blocks": runtime_guardrail_prompt_blocks,
            "runtime_guardrail_tool_schemas": runtime_guardrail_tool_schemas,
            "runtime_guardrail_manifest": runtime_guardrail_manifest,
            "trust_gate_by_name": {entry["name"]: entry for entry in repo_trust_gate.get("skills", [])},
            "allowlist_by_name": {entry["name"]: entry for entry in permission_allowlist.get("skills", [])},
            "context_guard_by_name": {entry["name"]: entry for entry in skill_context_guard.get("skills", [])},
        }
    )
    return docs


def skill_source_scope(docs: dict[str, Any], skill_name: str) -> str:
    trust_entry = docs.get("trust_gate_by_name", {}).get(skill_name)
    if trust_entry:
        return trust_entry.get("source_scope", "repo")
    discovery = docs.get("discovery_by_name", {}).get(skill_name, {})
    path = discovery.get("path", "")
    if path.startswith(".agents/skills/"):
        return "repo"
    return "repo"


def skill_allowed(docs: dict[str, Any], skill_name: str, trust_status: dict[str, Any]) -> bool:
    scope = skill_source_scope(docs, skill_name)
    if scope == "repo" and not trust_status["repo_trusted"]:
        return False
    return True


def resolve_scope_paths(repo_root: pathlib.Path, allowlist_entry: dict[str, Any]) -> dict[str, list[str]]:
    templates = allowlist_entry.get("path_templates", {})
    mapping = {
        "$REPO_ROOT": str(repo_root.resolve()),
        "$HOME": str(pathlib.Path.home()),
    }
    resolved: dict[str, list[str]] = {}
    for scope, paths in templates.items():
        resolved_paths = []
        for raw in paths:
            rendered = raw
            for key, value in mapping.items():
                rendered = rendered.replace(key, value)
            resolved_paths.append(rendered)
        resolved[scope] = resolved_paths
    return resolved


def guardrail_refs(skill_name: str) -> dict[str, str]:
    return {
        "trust_gate_ref": f"generated/repo_trust_gate_manifest.json#{skill_name}",
        "permission_allowlist_ref": f"generated/permission_allowlist_manifest.json#{skill_name}",
        "skill_context_guard_ref": f"generated/skill_context_guard_manifest.json#{skill_name}",
    }


def blocked_payload(stage: str, docs: dict[str, Any], skill_name: str, trust_status: dict[str, Any]) -> dict[str, Any]:
    discovery = docs["discovery_by_name"].get(skill_name)
    if discovery is None:
        raise SystemExit(f"unknown skill: {skill_name}")
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "layer": "guarded",
        "stage": f"{stage}_blocked",
        "skill": {
            "name": discovery["name"],
            "description": discovery["description"],
            "path": discovery["path"],
            "source_scope": skill_source_scope(docs, skill_name),
        },
        "blocked_reason": "Repo-scoped skills remain hidden until the repository is explicitly trusted.",
        "trust_status": trust_status,
        "trust_tool_call": {
            "name": "repo_trust_gate",
            "arguments": {
                "trust_store": trust_status["trust_store_path"],
                "decision": "trusted",
            },
        },
        "references": guardrail_refs(skill_name),
    }


def discover_guarded_payload(
    repo_root: pathlib.Path,
    docs: dict[str, Any],
    query: str | None = None,
    limit: int | None = None,
    include_blocked: bool = False,
    repo_trusted: str = "auto",
    trust_store_path: pathlib.Path | None = None,
) -> dict[str, Any]:
    raw = raw_discover_payload(docs, query=query, limit=limit)
    trust_status = resolve_repo_trust(repo_root, trust_store_path=trust_store_path, repo_trusted=repo_trusted)
    visible: list[dict[str, Any]] = []
    blocked_count = 0
    for skill in raw["skills"]:
        name = skill["name"]
        allowed = skill_allowed(docs, name, trust_status)
        allowlist_entry = docs["allowlist_by_name"].get(name, {})
        context_entry = docs["context_guard_by_name"].get(name, {})
        governed = dict(skill)
        governed["source_scope"] = skill_source_scope(docs, name)
        governed["guarded"] = {
            "blocked_by_trust_gate": not allowed,
            "trust_required": governed["source_scope"] == "repo",
            "allowlist_id": allowlist_entry.get("allowlist_id"),
            "dedupe_key": context_entry.get("dedupe_key"),
        }
        governed.update(guardrail_refs(name))
        if allowed:
            visible.append(governed)
        else:
            blocked_count += 1
            if include_blocked:
                visible.append(governed)
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "layer": "guarded",
        "stage": "discover",
        "behavioral_instructions": docs["runtime_guardrail_prompt_blocks"].get("behavioral_instructions", []),
        "trust_status": trust_status,
        "count": len(visible),
        "blocked_count": blocked_count,
        "skills": visible,
        "notes": [
            "Repo-scoped skills are hidden by default when the repository is untrusted.",
            "Use include_blocked=true only for debugging or UI explanation; do not expose blocked skills to the model as available actions.",
        ],
    }


def disclose_guarded_payload(
    repo_root: pathlib.Path,
    docs: dict[str, Any],
    skill_name: str,
    repo_trusted: str = "auto",
    trust_store_path: pathlib.Path | None = None,
) -> dict[str, Any]:
    trust_status = resolve_repo_trust(repo_root, trust_store_path=trust_store_path, repo_trusted=repo_trusted)
    if not skill_allowed(docs, skill_name, trust_status):
        return blocked_payload("disclose", docs, skill_name, trust_status)
    raw = raw_disclose_payload(docs, skill_name)
    raw["profile"] = PROFILE
    raw["layer"] = "guarded"
    raw["trust_status"] = trust_status
    raw["skill"]["source_scope"] = skill_source_scope(docs, skill_name)
    raw["skill"].update(guardrail_refs(skill_name))
    raw["skill"]["allowlist_id"] = docs["allowlist_by_name"].get(skill_name, {}).get("allowlist_id")
    raw["skill"]["dedupe_key"] = docs["context_guard_by_name"].get(skill_name, {}).get("dedupe_key")
    return raw


def update_guarded_session(
    session_file: pathlib.Path,
    skill_name: str,
    trust_status: dict[str, Any],
    allowlist_entry: dict[str, Any],
    context_entry: dict[str, Any],
    repo_root: pathlib.Path,
    already_active: bool,
) -> dict[str, Any]:
    session = load_session(session_file)
    scope = allowlist_entry.get("source_scope", "repo")
    resolved_paths = resolve_scope_paths(repo_root, allowlist_entry).get(scope, [])
    for record in session.get("active_skills", []):
        if record["name"] != skill_name:
            continue
        record["guarded"] = True
        record["source_scope"] = scope
        record["repo_trusted_at_activation"] = trust_status["repo_trusted"]
        record["repo_trust_source"] = trust_status["decision_source"]
        record["repo_identity"] = trust_status["repo_identity"]
        record["instruction_sha256"] = context_entry.get("instruction_sha256")
        record["dedupe_key"] = context_entry.get("dedupe_key")
        record["resolved_allowlist_paths"] = resolved_paths
        record["allowlist_id"] = allowlist_entry.get("allowlist_id")
        record["context_guard_ref"] = f"generated/skill_context_guard_manifest.json#{skill_name}"
        record["trust_gate_ref"] = f"generated/repo_trust_gate_manifest.json#{skill_name}"
        if already_active:
            record["dedupe_skip_count"] = record.get("dedupe_skip_count", 0) + 1
        break
    session["guardrail_profile"] = PROFILE
    session["trust_store_hint"] = trust_status["trust_store_path"]
    session["updated_at"] = now_iso()
    save_session(session_file, session)
    return session


def activate_guarded_payload(
    repo_root: pathlib.Path,
    docs: dict[str, Any],
    skill_name: str,
    session_file: pathlib.Path | None = None,
    explicit_handle: str | None = None,
    include_frontmatter: bool = False,
    wrap_mode: str = DEFAULT_WRAP_MODE,
    repo_trusted: str = "auto",
    trust_store_path: pathlib.Path | None = None,
) -> dict[str, Any]:
    trust_status = resolve_repo_trust(repo_root, trust_store_path=trust_store_path, repo_trusted=repo_trusted)
    if not skill_allowed(docs, skill_name, trust_status):
        return blocked_payload("activate", docs, skill_name, trust_status)
    raw = raw_activate_payload(
        repo_root,
        docs,
        skill_name=skill_name,
        session_file=session_file,
        explicit_handle=explicit_handle,
        include_frontmatter=include_frontmatter,
        wrap_mode=wrap_mode,
    )
    allowlist_entry = docs["allowlist_by_name"].get(skill_name, {})
    context_entry = docs["context_guard_by_name"].get(skill_name, {})
    raw["profile"] = PROFILE
    raw["layer"] = "guarded"
    raw["trust_status"] = trust_status
    raw["governance"] = {
        "repo_trust": trust_status,
        "permission_allowlist": {
            **allowlist_entry,
            "resolved_paths": resolve_scope_paths(repo_root, allowlist_entry),
        },
        "context_guard": context_entry,
        "recommended_injection_strategy": "reuse-existing-context" if raw["activation"]["already_active"] else "inject-full-skill",
        "dedupe_skipped_reinjection": bool(raw["activation"]["already_active"]),
    }
    raw["skill"]["source_scope"] = skill_source_scope(docs, skill_name)
    raw["skill"].update(guardrail_refs(skill_name))
    raw["activation"]["guarded"] = True
    raw["activation"]["instruction_sha256"] = context_entry.get("instruction_sha256")
    raw["activation"]["dedupe_key"] = context_entry.get("dedupe_key")
    if session_file is not None:
        raw["session"] = update_guarded_session(
            session_file=session_file,
            skill_name=skill_name,
            trust_status=trust_status,
            allowlist_entry=allowlist_entry,
            context_entry=context_entry,
            repo_root=repo_root,
            already_active=raw["activation"]["already_active"],
        )
    return raw


def status_guarded_payload(
    repo_root: pathlib.Path,
    docs: dict[str, Any],
    session_file: pathlib.Path,
    repo_trusted: str = "auto",
    trust_store_path: pathlib.Path | None = None,
) -> dict[str, Any]:
    raw = raw_status_payload(session_file)
    raw["profile"] = PROFILE
    raw["layer"] = "guarded"
    raw["trust_status"] = resolve_repo_trust(repo_root, trust_store_path=trust_store_path, repo_trusted=repo_trusted)
    raw["notes"] = [
        "Active skill records should carry instruction_sha256, dedupe_key, and resolved_allowlist_paths once activated through the governed seam.",
        "If a session was created through the raw seam, reactivate the skill through the governed seam to enrich the session state.",
    ]
    return raw


def trust_payload(
    repo_root: pathlib.Path,
    decision: str | None = None,
    reason: str | None = None,
    trust_store_path: pathlib.Path | None = None,
) -> dict[str, Any]:
    trust_store = trust_store_path or default_trust_store_path(repo_root)
    identity = repo_identity(repo_root)
    store = load_trust_store(trust_store)
    entry = find_matching_trust_entry(store, identity)
    if decision is not None:
        if decision == "clear":
            if entry is not None:
                store["entries"] = [item for item in store.get("entries", []) if item is not entry]
        else:
            new_entry = {
                "repo_root": identity["repo_root"],
                "repo_id": identity["repo_id"],
                "git_origin_url": identity["git_origin_url"],
                "decision": decision,
                "reason": reason,
                "updated_at": now_iso(),
            }
            if entry is None:
                store.setdefault("entries", []).append(new_entry)
            else:
                entry.update(new_entry)
        save_trust_store(trust_store, store)
    status = resolve_repo_trust(repo_root, trust_store_path=trust_store, repo_trusted="auto")
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "layer": "guarded",
        "stage": "trust",
        "trust_status": status,
        "trust_store_path": str(trust_store.resolve()),
        "entry_count": len(load_trust_store(trust_store).get("entries", [])),
    }


def allowlist_payload(
    repo_root: pathlib.Path,
    docs: dict[str, Any],
    skill_name: str | None = None,
    session_file: pathlib.Path | None = None,
    adapter: str = "generic",
) -> dict[str, Any]:
    selected: list[str] = []
    if session_file is not None:
        session = load_session(session_file)
        selected.extend(record["name"] for record in session.get("active_skills", []))
    if skill_name is not None and skill_name not in selected:
        selected.append(skill_name)
    if not selected:
        raise SystemExit("allowlist requires --skill or --session-file")
    skills = []
    merged_paths: list[str] = []
    for name in selected:
        allowlist_entry = docs["allowlist_by_name"].get(name)
        if allowlist_entry is None:
            continue
        resolved = resolve_scope_paths(repo_root, allowlist_entry)
        scope = allowlist_entry.get("source_scope", "repo")
        scope_paths = resolved.get(scope, resolved.get("repo", []))
        for path in scope_paths:
            if path not in merged_paths:
                merged_paths.append(path)
        skills.append(
            {
                "name": name,
                "allowlist_id": allowlist_entry.get("allowlist_id"),
                "source_scope": scope,
                "resolved_paths": resolved,
                "resource_inventory": allowlist_entry.get("resource_inventory", {}),
            }
        )
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "layer": "guarded",
        "stage": "allowlist",
        "adapter": adapter,
        "read_access": "read-only",
        "merge_strategy": "union-active-skills",
        "paths": merged_paths,
        "skills": skills,
        "notes": [
            "Grant read access to these skill directories before the model attempts to read bundled resources.",
            "Do not eagerly read all resources. Let the model request specific files on demand.",
        ],
    }


def compact_guarded_payload(repo_root: pathlib.Path, docs: dict[str, Any], session_file: pathlib.Path) -> dict[str, Any]:
    raw = raw_compact_payload(session_file)
    session = load_session(session_file)
    active_by_name = {record["name"]: record for record in session.get("active_skills", [])}
    packets = []
    for packet in raw.get("active_skill_packets", []):
        record = active_by_name.get(packet["name"], {})
        context_entry = docs["context_guard_by_name"].get(packet["name"], {})
        packets.append(
            {
                **packet,
                "instruction_sha256": record.get("instruction_sha256", context_entry.get("instruction_sha256")),
                "dedupe_key": record.get("dedupe_key", context_entry.get("dedupe_key")),
                "source_scope": record.get("source_scope", skill_source_scope(docs, packet["name"])),
                "repo_trusted_at_activation": record.get("repo_trusted_at_activation"),
                "resolved_allowlist_paths": record.get("resolved_allowlist_paths", []),
                "reactivation_call": context_entry.get("reactivation_call"),
            }
        )
    guarded = {
        **raw,
        "profile": PROFILE,
        "layer": "guarded",
        "active_skill_packets": packets,
        "session_guardrails": {
            "trust_store_hint": session.get("trust_store_hint"),
            "guardrail_profile": session.get("guardrail_profile"),
        },
    }
    session["last_guarded_compaction_at"] = now_iso()
    session["last_guarded_compaction_packet"] = guarded
    save_session(session_file, session)
    return guarded


def rehydrate_payload(
    repo_root: pathlib.Path,
    docs: dict[str, Any],
    session_file: pathlib.Path,
    skill_name: str | None = None,
    include_activation_call: bool = True,
) -> dict[str, Any]:
    session = load_session(session_file)
    records = session.get("active_skills", [])
    if skill_name is not None:
        records = [record for record in records if record["name"] == skill_name]
    packets = []
    activation_calls = []
    for record in records:
        context_entry = docs["context_guard_by_name"].get(record["name"], {})
        packet = {
            "name": record["name"],
            "instruction_sha256": record.get("instruction_sha256", context_entry.get("instruction_sha256")),
            "dedupe_key": record.get("dedupe_key", context_entry.get("dedupe_key")),
            "compact_summary": record.get("compact_summary", context_entry.get("compact_summary")),
            "must_keep": record.get("must_keep", context_entry.get("must_keep", [])),
            "retain_sections": record.get("retain_sections", context_entry.get("retain_sections", [])),
            "rehydration_hint": record.get("rehydration_hint", context_entry.get("rehydration_hint")),
            "resolved_allowlist_paths": record.get("resolved_allowlist_paths", []),
            "repo_trusted_at_activation": record.get("repo_trusted_at_activation"),
        }
        packets.append(packet)
        if include_activation_call:
            activation_calls.append(
                {
                    "name": "guarded_activate_skill",
                    "arguments": {
                        "skill_name": record["name"],
                        "session_file": str(session_file),
                        "explicit_handle": f"${record['name']}",
                    },
                }
            )
    session["last_rehydrated_at"] = now_iso()
    save_session(session_file, session)
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "layer": "guarded",
        "stage": "rehydrate",
        "session_id": session.get("session_id"),
        "skill_packets": packets,
        "activation_calls": activation_calls,
        "notes": [
            "If the skill body was pruned, call guarded_activate_skill before resuming the task.",
            "If the dedupe key is already present in active context, reuse the existing packet instead of reinjecting the full skill body.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    stage = payload.get("stage")
    if stage == "discover":
        return print_markdown_discover(payload)
    if stage == "disclose":
        return print_markdown_disclose(payload)
    if stage == "activate":
        base = print_markdown_activate(payload)
        lines = [base.rstrip(), "", "## Guardrails", ""]
        lines.append(f"- Repo trusted: {payload['trust_status']['repo_trusted']}")
        lines.append(f"- Decision source: {payload['trust_status']['decision_source']}")
        lines.append(f"- Dedupe key: {payload['activation'].get('dedupe_key')}")
        return "\n".join(lines).strip() + "\n"
    if stage in {"disclose_blocked", "activate_blocked"}:
        return (
            f"# {stage}\n\n"
            f"- Skill: {payload['skill']['name']}\n"
            f"- Reason: {payload['blocked_reason']}\n"
            f"- Trust store: {payload['trust_status']['trust_store_path']}\n"
        )
    return print_markdown_generic(payload)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover = subparsers.add_parser("discover")
    discover.add_argument("--repo-root", default=".")
    discover.add_argument("--query")
    discover.add_argument("--limit", type=int)
    discover.add_argument("--include-blocked", action="store_true")
    discover.add_argument("--trust-store")
    discover.add_argument("--repo-trusted", choices=("auto", "true", "false"), default="auto")
    discover.add_argument("--format", choices=("json", "markdown"), default="json")

    disclose = subparsers.add_parser("disclose")
    disclose.add_argument("--repo-root", default=".")
    disclose.add_argument("--skill", "--skill-name", dest="skill", required=True)
    disclose.add_argument("--trust-store")
    disclose.add_argument("--repo-trusted", choices=("auto", "true", "false"), default="auto")
    disclose.add_argument("--format", choices=("json", "markdown"), default="json")

    activate = subparsers.add_parser("activate")
    activate.add_argument("--repo-root", default=".")
    activate.add_argument("--skill", "--skill-name", dest="skill", required=True)
    activate.add_argument("--session-file")
    activate.add_argument("--explicit-handle")
    activate.add_argument("--include-frontmatter", action="store_true")
    activate.add_argument("--wrap-mode", choices=("structured", "markdown", "raw"), default=DEFAULT_WRAP_MODE)
    activate.add_argument("--trust-store")
    activate.add_argument("--repo-trusted", choices=("auto", "true", "false"), default="auto")
    activate.add_argument("--format", choices=("json", "markdown"), default="json")

    status = subparsers.add_parser("status")
    status.add_argument("--repo-root", default=".")
    status.add_argument("--session-file", required=True)
    status.add_argument("--trust-store")
    status.add_argument("--repo-trusted", choices=("auto", "true", "false"), default="auto")
    status.add_argument("--format", choices=("json", "markdown"), default="json")

    trust = subparsers.add_parser("trust")
    trust.add_argument("--repo-root", default=".")
    trust.add_argument("--trust-store")
    trust.add_argument("--decision", choices=("trusted", "untrusted", "clear"))
    trust.add_argument("--reason")
    trust.add_argument("--format", choices=("json", "markdown"), default="json")

    allowlist = subparsers.add_parser("allowlist")
    allowlist.add_argument("--repo-root", default=".")
    allowlist.add_argument("--skill", "--skill-name", dest="skill")
    allowlist.add_argument("--session-file")
    allowlist.add_argument("--adapter", choices=("generic", "local-shell", "codex-local", "codex-worktree"), default="generic")
    allowlist.add_argument("--format", choices=("json", "markdown"), default="json")

    compact = subparsers.add_parser("compact")
    compact.add_argument("--repo-root", default=".")
    compact.add_argument("--session-file", required=True)
    compact.add_argument("--format", choices=("json", "markdown"), default="json")

    rehydrate = subparsers.add_parser("rehydrate")
    rehydrate.add_argument("--repo-root", default=".")
    rehydrate.add_argument("--session-file", required=True)
    rehydrate.add_argument("--skill", "--skill-name", dest="skill")
    rehydrate.add_argument("--include-activation-call", action="store_true")
    rehydrate.add_argument("--format", choices=("json", "markdown"), default="json")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    repo_root = find_repo_root_from_args(getattr(args, "repo_root", "."))
    docs = load_guardrails(repo_root)
    trust_store_path = pathlib.Path(args.trust_store).resolve() if getattr(args, "trust_store", None) else None

    if args.command == "discover":
        payload = discover_guarded_payload(
            repo_root=repo_root,
            docs=docs,
            query=args.query,
            limit=args.limit,
            include_blocked=args.include_blocked,
            repo_trusted=args.repo_trusted,
            trust_store_path=trust_store_path,
        )
    elif args.command == "disclose":
        payload = disclose_guarded_payload(
            repo_root=repo_root,
            docs=docs,
            skill_name=args.skill,
            repo_trusted=args.repo_trusted,
            trust_store_path=trust_store_path,
        )
    elif args.command == "activate":
        session_file = pathlib.Path(args.session_file).resolve() if args.session_file else None
        payload = activate_guarded_payload(
            repo_root=repo_root,
            docs=docs,
            skill_name=args.skill,
            session_file=session_file,
            explicit_handle=args.explicit_handle,
            include_frontmatter=args.include_frontmatter,
            wrap_mode=args.wrap_mode,
            repo_trusted=args.repo_trusted,
            trust_store_path=trust_store_path,
        )
    elif args.command == "status":
        payload = status_guarded_payload(
            repo_root=repo_root,
            docs=docs,
            session_file=pathlib.Path(args.session_file).resolve(),
            repo_trusted=args.repo_trusted,
            trust_store_path=trust_store_path,
        )
    elif args.command == "trust":
        payload = trust_payload(
            repo_root=repo_root,
            decision=args.decision,
            reason=args.reason,
            trust_store_path=trust_store_path,
        )
    elif args.command == "allowlist":
        session_file = pathlib.Path(args.session_file).resolve() if args.session_file else None
        payload = allowlist_payload(
            repo_root=repo_root,
            docs=docs,
            skill_name=args.skill,
            session_file=session_file,
            adapter=args.adapter,
        )
    elif args.command == "compact":
        payload = compact_guarded_payload(
            repo_root=repo_root,
            docs=docs,
            session_file=pathlib.Path(args.session_file).resolve(),
        )
    elif args.command == "rehydrate":
        payload = rehydrate_payload(
            repo_root=repo_root,
            docs=docs,
            session_file=pathlib.Path(args.session_file).resolve(),
            skill_name=args.skill,
            include_activation_call=args.include_activation_call,
        )
    else:
        raise SystemExit(f"unknown command: {args.command}")

    if args.format == "json":
        print(dump_json(payload), end="")
    else:
        print(render_markdown(payload), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
