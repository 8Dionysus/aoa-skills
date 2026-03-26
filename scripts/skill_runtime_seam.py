#!/usr/bin/env python3
"""Dedicated-tool runtime seam for AoA skills.

This script sits downstream of the shared `.agents/skills/*` export and offers a
stable discover -> disclose -> activate flow for local-friendly runtimes.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import uuid
from datetime import datetime, timezone
from typing import Any

import yaml

PROFILE = "codex-facing-wave-4-runtime-seam"
ROOT = ".agents/skills"
RESOURCE_DIR_NAMES = ("scripts", "references", "assets")
DEFAULT_WRAP_MODE = "structured"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


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


def parse_sections(body: str) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    current_heading: str | None = None
    buffer: list[str] = []
    for raw_line in body.splitlines():
        if raw_line.startswith("## "):
            if current_heading is not None:
                sections.append({"heading": current_heading, "content": "\n".join(buffer).strip()})
            current_heading = raw_line[3:].strip()
            buffer = []
            continue
        if raw_line.startswith("# "):
            continue
        if current_heading is not None:
            buffer.append(raw_line)
    if current_heading is not None:
        sections.append({"heading": current_heading, "content": "\n".join(buffer).strip()})
    return sections


def inventory_resources(skill_dir: pathlib.Path) -> dict[str, list[str]]:
    inventory: dict[str, list[str]] = {}
    for resource_dir_name in RESOURCE_DIR_NAMES:
        resource_dir = skill_dir / resource_dir_name
        if not resource_dir.exists():
            inventory[resource_dir_name] = []
            continue
        inventory[resource_dir_name] = sorted(
            str(path.relative_to(skill_dir).as_posix())
            for path in resource_dir.rglob("*")
            if path.is_file()
        )
    return inventory


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def section_summary_map(sections: list[dict[str, str]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for section in sections:
        lines = [line.strip() for line in section["content"].splitlines() if line.strip()]
        bullets = []
        for line in lines:
            if line.startswith("- "):
                bullets.append(normalize_space(line[2:]))
            else:
                match = re.match(r"^(\d+)\.\s+(.*)$", line)
                if match:
                    bullets.append(normalize_space(match.group(2)))
        if bullets:
            summary = "; ".join(bullets[:2])
        else:
            summary = normalize_space(" ".join(lines))
        if len(summary) > 280:
            summary = summary[:277].rstrip() + "..."
        out[section["heading"]] = summary
    return out


def load_indexes(repo_root: pathlib.Path) -> dict[str, Any]:
    generated_dir = repo_root / "generated"
    docs = {
        "discovery": load_json(generated_dir / "runtime_discovery_index.json"),
        "disclosure": load_json(generated_dir / "runtime_disclosure_index.json"),
        "aliases": load_json(generated_dir / "runtime_activation_aliases.json"),
        "tool_schemas": load_json(generated_dir / "runtime_tool_schemas.json"),
        "session_contract": load_json(generated_dir / "runtime_session_contract.json"),
        "prompt_blocks": load_json(generated_dir / "runtime_prompt_blocks.json"),
        "router_hints": load_json(generated_dir / "runtime_router_hints.json"),
        "runtime_contracts": load_json(generated_dir / "skill_runtime_contracts.json"),
        "context_retention": load_json(generated_dir / "context_retention_manifest.json"),
        "trust_policy": load_json(generated_dir / "trust_policy_matrix.json"),
    }
    docs["discovery_by_name"] = {entry["name"]: entry for entry in docs["discovery"]["skills"]}
    docs["disclosure_by_name"] = {entry["name"]: entry for entry in docs["disclosure"]["skills"]}
    docs["alias_by_name"] = {entry["name"]: entry for entry in docs["aliases"]["aliases"]}
    docs["runtime_by_name"] = {entry["name"]: entry for entry in docs["runtime_contracts"].get("skills", [])}
    docs["context_by_name"] = {entry["name"]: entry for entry in docs["context_retention"].get("skills", [])}
    docs["trust_by_name"] = {entry["name"]: entry for entry in docs["trust_policy"].get("skills", [])}
    docs["router_by_name"] = {entry["name"]: entry for entry in docs["router_hints"]["skills"]}
    return docs


def session_template(session_file: pathlib.Path | None = None) -> dict[str, Any]:
    now = now_iso()
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "session_id": str(uuid.uuid4()),
        "created_at": now,
        "updated_at": now,
        "session_file": str(session_file) if session_file else None,
        "active_skills": [],
        "activation_log": [],
    }


def load_session(session_file: pathlib.Path) -> dict[str, Any]:
    if session_file.exists():
        return load_json(session_file)
    return session_template(session_file=session_file)


def save_session(session_file: pathlib.Path, session: dict[str, Any]) -> None:
    session["updated_at"] = now_iso()
    session_file.parent.mkdir(parents=True, exist_ok=True)
    session_file.write_text(dump_json(session), encoding="utf-8")


def wrapped_skill_content(name: str, body: str, skill_dir: pathlib.Path, inventory: dict[str, list[str]]) -> str:
    lines = [f'<skill_content name="{name}">', body.strip(), "", f"Skill directory: {skill_dir}", "Relative paths in this skill are relative to the skill directory."]
    lines.append("<skill_resources>")
    for group_name in RESOURCE_DIR_NAMES:
        for item in inventory.get(group_name, []):
            lines.append(f"  <file>{item}</file>")
    lines.append("</skill_resources>")
    lines.append("</skill_content>")
    return "\n".join(lines)


def discover_payload(indexes: dict[str, Any], query: str | None = None, trust_posture: str | None = None, invocation_mode: str | None = None, mutation_surface: str | None = None, allow_implicit_invocation: bool | None = None, limit: int | None = None) -> dict[str, Any]:
    skills = indexes["discovery"]["skills"]
    query_lc = query.lower() if query else None
    matches: list[dict[str, Any]] = []
    for entry in skills:
        haystack = " ".join(
            [
                entry["name"],
                entry["description"],
                entry.get("short_description", ""),
                " ".join(entry.get("keywords", [])),
            ]
        ).lower()
        if query_lc and query_lc not in haystack:
            continue
        if trust_posture and entry["trust_posture"] != trust_posture:
            continue
        if invocation_mode and entry["invocation_mode"] != invocation_mode:
            continue
        if mutation_surface and entry["mutation_surface"] != mutation_surface:
            continue
        if allow_implicit_invocation is not None and entry["allow_implicit_invocation"] != allow_implicit_invocation:
            continue
        matches.append(entry)
    if limit is not None:
        matches = matches[:limit]
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "stage": "discover",
        "behavioral_instructions": indexes["discovery"].get("behavioral_instructions", []),
        "count": len(matches),
        "skills": matches,
    }


def disclose_payload(indexes: dict[str, Any], skill_name: str) -> dict[str, Any]:
    disclosure = indexes["disclosure_by_name"].get(skill_name)
    if disclosure is None:
        raise SystemExit(f"unknown skill: {skill_name}")
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "stage": "disclose",
        "skill": disclosure,
        "related_router_hints": indexes["router_by_name"].get(skill_name),
    }


def update_session_for_activation(session: dict[str, Any], activation_record: dict[str, Any], explicit_handle: str | None, session_file: pathlib.Path) -> tuple[dict[str, Any], bool]:
    active_skills = session.setdefault("active_skills", [])
    existing = None
    for record in active_skills:
        if record["name"] == activation_record["name"]:
            existing = record
            break
    already_active = existing is not None
    if existing is None:
        existing = activation_record
        active_skills.append(existing)
    else:
        existing["activation_count"] += 1
        existing["last_activated_at"] = now_iso()
        if explicit_handle:
            existing["last_explicit_handle"] = explicit_handle
    session.setdefault("activation_log", []).append(
        {
            "skill_name": activation_record["name"],
            "activated_at": now_iso(),
            "explicit_handle": explicit_handle,
            "already_active": already_active,
            "session_file": str(session_file),
        }
    )
    return session, already_active


def activate_payload(repo_root: pathlib.Path, indexes: dict[str, Any], skill_name: str, session_file: pathlib.Path | None = None, explicit_handle: str | None = None, include_frontmatter: bool = False, wrap_mode: str = DEFAULT_WRAP_MODE) -> dict[str, Any]:
    discovery = indexes["discovery_by_name"].get(skill_name)
    disclosure = indexes["disclosure_by_name"].get(skill_name)
    if discovery is None or disclosure is None:
        raise SystemExit(f"unknown skill: {skill_name}")

    skill_path = repo_root / discovery["path"]
    skill_dir = skill_path.parent
    frontmatter, body = parse_frontmatter(skill_path)
    sections = parse_sections(body)
    inventory = inventory_resources(skill_dir)
    allowlist_paths = [str(skill_dir.relative_to(repo_root).as_posix()), str(skill_dir)]
    structured_wrap = wrapped_skill_content(skill_name, body, skill_dir, inventory)
    rendered_content = structured_wrap if wrap_mode == "structured" else body.strip()
    if wrap_mode == "markdown":
        rendered_content = body.strip()
    elif wrap_mode == "raw":
        rendered_content = body

    payload: dict[str, Any] = {
        "schema_version": 1,
        "profile": PROFILE,
        "stage": "activate",
        "skill": {
            "name": frontmatter["name"],
            "description": frontmatter["description"],
            "path": discovery["path"],
            "skill_dir": str(skill_dir.relative_to(repo_root).as_posix()),
            "compatibility": frontmatter.get("compatibility"),
            "metadata": frontmatter.get("metadata", {}),
            "allow_implicit_invocation": discovery["allow_implicit_invocation"],
            "invocation_mode": discovery["invocation_mode"],
        },
        "activation": {
            "tool": "activate_skill",
            "explicit_handle": explicit_handle,
            "already_active": False,
            "protected_from_compaction": True,
            "wrap_mode": wrap_mode,
            "legacy_tool_alias": "scripts/activate_skill.py",
        },
        "resources": {
            "allowlist_paths": allowlist_paths,
            "inventory": inventory,
        },
        "openai": yaml.safe_load((skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")) or {},
        "runtime_contract": indexes["runtime_by_name"].get(skill_name),
        "context_retention": indexes["context_by_name"].get(skill_name),
        "trust_policy": indexes["trust_by_name"].get(skill_name),
        "disclosure_preview": disclosure,
        "router_hints": indexes["router_by_name"].get(skill_name),
        "instructions_markdown": body.strip(),
        "structured_wrap": structured_wrap,
        "rendered_content": rendered_content,
        "section_summaries": section_summary_map(sections),
    }
    if include_frontmatter:
        payload["frontmatter"] = frontmatter

    if session_file is not None:
        session = load_session(session_file)
        compact_summary = payload["context_retention"].get("compact_summary") if payload["context_retention"] else discovery.get("short_description")
        must_keep = payload["context_retention"].get("must_keep", []) if payload["context_retention"] else []
        rehydration_hint = payload["context_retention"].get("rehydration_hint") if payload["context_retention"] else "Reload the skill before resuming."
        activation_record = {
            "name": skill_name,
            "activated_at": now_iso(),
            "last_activated_at": now_iso(),
            "activation_count": 1,
            "protected_from_compaction": True,
            "allowlist_paths": allowlist_paths,
            "compact_summary": compact_summary,
            "must_keep": must_keep,
            "rehydration_hint": rehydration_hint,
            "retain_sections": payload["context_retention"].get("retain_sections", []) if payload["context_retention"] else [],
            "explicit_handles": discovery.get("explicit_handles", {}),
            "last_explicit_handle": explicit_handle,
        }
        session, already_active = update_session_for_activation(session, activation_record, explicit_handle, session_file)
        save_session(session_file, session)
        payload["activation"]["already_active"] = already_active
        payload["session"] = session
    return payload


def status_payload(session_file: pathlib.Path) -> dict[str, Any]:
    session = load_session(session_file)
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "stage": "status",
        "session": session,
    }


def deactivate_payload(session_file: pathlib.Path, skill_name: str) -> dict[str, Any]:
    session = load_session(session_file)
    before = len(session.get("active_skills", []))
    session["active_skills"] = [record for record in session.get("active_skills", []) if record["name"] != skill_name]
    removed = before != len(session["active_skills"])
    session.setdefault("activation_log", []).append(
        {
            "skill_name": skill_name,
            "activated_at": now_iso(),
            "event": "deactivate",
            "removed": removed,
            "session_file": str(session_file),
        }
    )
    save_session(session_file, session)
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "stage": "deactivate",
        "removed": removed,
        "session": session,
    }


def compact_payload(session_file: pathlib.Path) -> dict[str, Any]:
    session = load_session(session_file)
    packets = []
    for record in session.get("active_skills", []):
        packets.append(
            {
                "name": record["name"],
                "compact_summary": record.get("compact_summary"),
                "must_keep": record.get("must_keep", []),
                "retain_sections": record.get("retain_sections", []),
                "rehydration_hint": record.get("rehydration_hint"),
                "allowlist_paths": record.get("allowlist_paths", []),
                "protected_from_compaction": True,
            }
        )
    payload = {
        "schema_version": 1,
        "profile": PROFILE,
        "stage": "compact",
        "session_id": session["session_id"],
        "active_skill_packets": packets,
        "reactivation_instructions": [
            "Keep the active skill packets outside normal pruning.",
            "If the agent loses the skill body, reactivate the relevant skill before resuming the task.",
        ],
    }
    session["last_compaction_at"] = now_iso()
    session["last_compaction_packet"] = payload
    save_session(session_file, session)
    return payload


def print_markdown_discover(payload: dict[str, Any]) -> str:
    lines = ["# Discover skills", ""]
    for item in payload["skills"]:
        lines.extend([
            f"## {item['name']}",
            f"- {item['description']}",
            f"- Trust posture: {item['trust_posture']}",
            f"- Invocation mode: {item['invocation_mode']}",
            f"- Explicit handle: {item['explicit_handles']['codex']['mention']}",
            "",
        ])
    return "\n".join(lines).strip() + "\n"


def print_markdown_disclose(payload: dict[str, Any]) -> str:
    skill = payload["skill"]
    lines = [f"# Disclose skill: {skill['name']}", "", skill["disclose_card_markdown"], "## Section summaries", ""]
    for heading, summary in skill["section_summaries"].items():
        lines.append(f"- {heading}: {summary}")
    return "\n".join(lines).strip() + "\n"


def print_markdown_activate(payload: dict[str, Any]) -> str:
    lines = [
        f"# Activate skill: {payload['skill']['name']}",
        "",
        f"Description: {payload['skill']['description']}",
        f"Path: {payload['skill']['path']}",
        f"Implicit invocation allowed: {payload['skill']['allow_implicit_invocation']}",
        f"Already active in session: {payload['activation']['already_active']}",
        "",
        "## Allowlist paths",
        *[f"- {path}" for path in payload['resources']['allowlist_paths']],
        "",
        "## Bundled resources",
    ]
    for group_name in RESOURCE_DIR_NAMES:
        lines.append(f"### {group_name}")
        files = payload["resources"]["inventory"].get(group_name, [])
        if files:
            lines.extend(f"- {item}" for item in files)
        else:
            lines.append("- (none)")
        lines.append("")
    lines.extend([
        "## Structured wrap",
        "",
        "```xml",
        payload["structured_wrap"],
        "```",
    ])
    return "\n".join(lines).strip() + "\n"


def print_markdown_generic(payload: dict[str, Any]) -> str:
    return dump_json(payload)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover = subparsers.add_parser("discover")
    discover.add_argument("--repo-root", default=".")
    discover.add_argument("--query")
    discover.add_argument("--trust-posture")
    discover.add_argument("--invocation-mode")
    discover.add_argument("--mutation-surface")
    discover.add_argument("--allow-implicit-invocation", choices=("true", "false"))
    discover.add_argument("--limit", type=int)
    discover.add_argument("--format", choices=("json", "markdown"), default="json")

    disclose = subparsers.add_parser("disclose")
    disclose.add_argument("--repo-root", default=".")
    disclose.add_argument("--skill", required=True)
    disclose.add_argument("--format", choices=("json", "markdown"), default="json")

    activate = subparsers.add_parser("activate")
    activate.add_argument("--repo-root", default=".")
    activate.add_argument("--skill", required=True)
    activate.add_argument("--session-file")
    activate.add_argument("--explicit-handle")
    activate.add_argument("--include-frontmatter", action="store_true")
    activate.add_argument("--wrap-mode", choices=("structured", "markdown", "raw"), default=DEFAULT_WRAP_MODE)
    activate.add_argument("--format", choices=("json", "markdown"), default="json")

    status = subparsers.add_parser("status")
    status.add_argument("--session-file", required=True)
    status.add_argument("--format", choices=("json", "markdown"), default="json")

    deactivate = subparsers.add_parser("deactivate")
    deactivate.add_argument("--session-file", required=True)
    deactivate.add_argument("--skill", required=True)
    deactivate.add_argument("--format", choices=("json", "markdown"), default="json")

    compact = subparsers.add_parser("compact")
    compact.add_argument("--session-file", required=True)
    compact.add_argument("--format", choices=("json", "markdown"), default="json")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command in {"discover", "disclose", "activate"}:
        repo_root = pathlib.Path(args.repo_root).resolve()
        indexes = load_indexes(repo_root)

    if args.command == "discover":
        allow_implicit = None
        if args.allow_implicit_invocation == "true":
            allow_implicit = True
        elif args.allow_implicit_invocation == "false":
            allow_implicit = False
        payload = discover_payload(
            indexes,
            query=args.query,
            trust_posture=args.trust_posture,
            invocation_mode=args.invocation_mode,
            mutation_surface=args.mutation_surface,
            allow_implicit_invocation=allow_implicit,
            limit=args.limit,
        )
        if args.format == "json":
            print(dump_json(payload), end="")
        else:
            print(print_markdown_discover(payload), end="")
        return 0

    if args.command == "disclose":
        payload = disclose_payload(indexes, args.skill)
        if args.format == "json":
            print(dump_json(payload), end="")
        else:
            print(print_markdown_disclose(payload), end="")
        return 0

    if args.command == "activate":
        session_file = pathlib.Path(args.session_file).resolve() if args.session_file else None
        payload = activate_payload(
            repo_root,
            indexes,
            skill_name=args.skill,
            session_file=session_file,
            explicit_handle=args.explicit_handle,
            include_frontmatter=args.include_frontmatter,
            wrap_mode=args.wrap_mode,
        )
        if args.format == "json":
            print(dump_json(payload), end="")
        else:
            print(print_markdown_activate(payload), end="")
        return 0

    if args.command == "status":
        payload = status_payload(pathlib.Path(args.session_file).resolve())
        if args.format == "json":
            print(dump_json(payload), end="")
        else:
            print(print_markdown_generic(payload), end="")
        return 0

    if args.command == "deactivate":
        payload = deactivate_payload(pathlib.Path(args.session_file).resolve(), args.skill)
        if args.format == "json":
            print(dump_json(payload), end="")
        else:
            print(print_markdown_generic(payload), end="")
        return 0

    if args.command == "compact":
        payload = compact_payload(pathlib.Path(args.session_file).resolve())
        if args.format == "json":
            print(dump_json(payload), end="")
        else:
            print(print_markdown_generic(payload), end="")
        return 0

    raise SystemExit(f"unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
