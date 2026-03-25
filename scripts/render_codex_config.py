#!/usr/bin/env python3
"""Render Codex config snippets for disabling a resolved skill profile."""

from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument("--profile", required=True, help="Profile name from generated/codex_config_snippets.json")
    parser.add_argument("--format", choices=("toml", "json"), default="toml", help="Output format")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    snippets_doc = load_json(repo_root / "generated" / "codex_config_snippets.json")
    snippet = snippets_doc.get("snippets", {}).get(args.profile)
    if snippet is None:
        raise SystemExit(f"unknown profile: {args.profile}")

    if args.format == "json":
        print(json.dumps(snippet, indent=2))
        return 0

    print(snippet["disable_profile_toml"].rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
