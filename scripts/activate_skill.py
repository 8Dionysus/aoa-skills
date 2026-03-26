#!/usr/bin/env python3
"""Backward-compatible activation shim for the wave-4 runtime seam."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from skill_runtime_seam import activate_payload, load_indexes, print_markdown_activate


def legacy_payload(runtime_payload: dict[str, Any]) -> dict[str, Any]:
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
    parser.add_argument("--format", choices=("json", "markdown"), default="json", help="Output format")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    indexes = load_indexes(repo_root)
    runtime_payload = activate_payload(repo_root, indexes, skill_name=args.skill, wrap_mode="structured")

    if args.format == "json":
        print(json.dumps(legacy_payload(runtime_payload), indent=2))
        return 0

    print(print_markdown_activate(runtime_payload), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
