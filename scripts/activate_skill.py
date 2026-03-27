#!/usr/bin/env python3
"""Backward-compatible activation shim for the wave-6 governed runtime seam."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from skill_runtime_guardrails import activate_guarded_payload, load_guardrails, render_markdown


def legacy_payload(runtime_payload: dict[str, Any], docs: dict[str, Any], skill_name: str) -> dict[str, Any]:
    stage = runtime_payload["stage"]
    if stage.endswith("_blocked"):
        discovery = docs["discovery_by_name"].get(skill_name, {})
        skill = runtime_payload["skill"]
        return {
            "skill": {
                "name": skill["name"],
                "description": skill["description"],
                "path": skill["path"],
                "invocation_mode": discovery.get("invocation_mode"),
                "allow_implicit_invocation": discovery.get("allow_implicit_invocation"),
                "metadata": {},
                "compatibility": None,
                "skill_dir": None,
                "source_scope": skill.get("source_scope"),
            },
            "resources": {
                "allowlist_paths": [],
                "inventory": {},
            },
            "runtime_contract": None,
            "context_retention": None,
            "trust_policy": None,
            "openai": None,
            "instructions_markdown": None,
            "schema_version": runtime_payload["schema_version"],
            "profile": runtime_payload["profile"],
            "stage": runtime_payload["stage"],
            "activation": {
                "tool": "activate_skill",
                "guarded": True,
                "blocked": True,
                "legacy_tool_alias": "scripts/activate_skill.py",
            },
            "disclosure_preview": None,
            "router_hints": None,
            "structured_wrap": None,
            "rendered_content": None,
            "section_summaries": {},
            "blocked_reason": runtime_payload.get("blocked_reason"),
            "trust_status": runtime_payload.get("trust_status"),
            "references": runtime_payload.get("references"),
        }

    skill = runtime_payload["skill"]
    relative_allowlist = [skill["skill_dir"]]
    payload: dict[str, Any] = {
        "skill": {
            "name": skill["name"],
            "description": skill["description"],
            "path": skill["path"],
            "invocation_mode": skill["invocation_mode"],
            "allow_implicit_invocation": skill["allow_implicit_invocation"],
            "metadata": skill["metadata"],
            "compatibility": skill.get("compatibility"),
            "skill_dir": skill.get("skill_dir"),
            "source_scope": skill.get("source_scope"),
        },
        "resources": {
            "allowlist_paths": relative_allowlist,
            "inventory": runtime_payload["resources"]["inventory"],
        },
        "runtime_contract": runtime_payload["runtime_contract"],
        "context_retention": runtime_payload["context_retention"],
        "trust_policy": runtime_payload["trust_policy"],
        "openai": runtime_payload["openai"],
        "instructions_markdown": runtime_payload["instructions_markdown"],
        "schema_version": runtime_payload["schema_version"],
        "profile": runtime_payload["profile"],
        "stage": runtime_payload["stage"],
        "activation": runtime_payload["activation"],
        "disclosure_preview": runtime_payload["disclosure_preview"],
        "router_hints": runtime_payload["router_hints"],
        "structured_wrap": runtime_payload["structured_wrap"],
        "rendered_content": runtime_payload["rendered_content"],
        "section_summaries": runtime_payload["section_summaries"],
        "trust_status": runtime_payload.get("trust_status"),
        "governance": runtime_payload.get("governance"),
        "references": runtime_payload.get("references"),
    }
    if "frontmatter" in runtime_payload:
        payload["frontmatter"] = runtime_payload["frontmatter"]
    if "session" in runtime_payload:
        payload["session"] = runtime_payload["session"]
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root containing .agents/skills")
    parser.add_argument("--skill", required=True, help="Skill name to activate")
    parser.add_argument("--session-file", help="Optional JSON session file path")
    parser.add_argument("--explicit-handle", help="Optional explicit handle such as $skill-name")
    parser.add_argument("--include-frontmatter", action="store_true", help="Include parsed frontmatter in the payload")
    parser.add_argument("--wrap-mode", choices=("structured", "markdown", "raw"), default="structured")
    parser.add_argument("--trust-store", help="Optional repo trust store path")
    parser.add_argument("--repo-trusted", choices=("auto", "true", "false"), default="auto")
    parser.add_argument("--format", choices=("json", "markdown"), default="json", help="Output format")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    docs = load_guardrails(repo_root)
    session_file = pathlib.Path(args.session_file).resolve() if args.session_file else None
    trust_store = pathlib.Path(args.trust_store).resolve() if args.trust_store else None
    runtime_payload = activate_guarded_payload(
        repo_root,
        docs,
        skill_name=args.skill,
        session_file=session_file,
        explicit_handle=args.explicit_handle,
        include_frontmatter=args.include_frontmatter,
        wrap_mode=args.wrap_mode,
        repo_trusted=args.repo_trusted,
        trust_store_path=trust_store,
    )

    if args.format == "json":
        print(json.dumps(legacy_payload(runtime_payload, docs, args.skill), indent=2))
        return 0

    print(render_markdown(runtime_payload), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
