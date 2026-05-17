#!/usr/bin/env python3
"""Read-only Skill Intelligence registry, search, explain, and status CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

import skill_intelligence_surface


REPO_ROOT = Path(__file__).resolve().parents[1]


def print_json(data: object) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def load_registry(repo_root: Path) -> dict:
    path = repo_root / skill_intelligence_surface.SKILL_INTELLIGENCE_JSON_PATH
    if path.is_file():
        return skill_intelligence_surface.load_json(path)
    return skill_intelligence_surface.build_skill_intelligence_registry_payload(repo_root)


def write_registry(repo_root: Path) -> None:
    texts = skill_intelligence_surface.build_skill_intelligence_texts(repo_root)
    for rel_path, text in texts.items():
        target = repo_root / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")


def check_registry(repo_root: Path) -> int:
    texts = skill_intelligence_surface.build_skill_intelligence_texts(repo_root)
    problems: list[str] = []
    for rel_path, expected in texts.items():
        target = repo_root / rel_path
        if not target.is_file():
            problems.append(f"missing {rel_path.as_posix()}")
            continue
        if target.read_text(encoding="utf-8") != expected:
            problems.append(f"stale {rel_path.as_posix()}")
    if problems:
        print("Skill intelligence registry check failed.")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("Skill intelligence registry check passed.")
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="aoa-skills repository root.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--check", action="store_true")

    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("intent")
    query_parser.add_argument("--limit", type=int, default=8)
    query_parser.add_argument("--scope")
    query_parser.add_argument("--status")
    query_parser.add_argument("--invocation-policy")
    query_parser.add_argument("--mutation-surface")

    explain_parser = subparsers.add_parser("explain")
    explain_parser.add_argument("skill")
    explain_parser.add_argument("--intent", default="")
    explain_parser.add_argument("--limit", type=int, default=5)

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--workspace-root", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    if args.command == "build":
        if args.check:
            return check_registry(repo_root)
        write_registry(repo_root)
        print("Skill intelligence registry built.")
        return 0

    payload = load_registry(repo_root)
    if args.command == "query":
        print_json(
            {
                "intent": args.intent,
                "candidates": skill_intelligence_surface.sqlite_search(
                    payload,
                    args.intent,
                    limit=args.limit,
                    scope=args.scope,
                    status=args.status,
                    invocation_policy=args.invocation_policy,
                    mutation_surface=args.mutation_surface,
                ),
            }
        )
        return 0
    if args.command == "explain":
        try:
            print_json(
                skill_intelligence_surface.explain_candidate(
                    payload,
                    args.skill,
                    intent=args.intent,
                    limit=args.limit,
                )
            )
        except KeyError:
            print(f"unknown skill: {args.skill}", file=sys.stderr)
            return 2
        return 0
    if args.command == "status":
        print_json(
            skill_intelligence_surface.registry_status(
                repo_root,
                payload,
                workspace_root=args.workspace_root,
            )
        )
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
