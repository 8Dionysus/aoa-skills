#!/usr/bin/env python3
"""Discover capability candidates and build explicit task-local DAG plans."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from skill_model import capability_system


def parse_external_input(raw: str) -> dict[str, str]:
    if "=" not in raw:
        raise argparse.ArgumentTypeError("external input must use TYPE=REF")
    selector, ref = raw.split("=", 1)
    if not selector.strip() or not ref.strip():
        raise argparse.ArgumentTypeError("external input must use non-empty TYPE=REF")
    selector = selector.strip()
    if "::" in selector:
        target, port = selector.split("::", 1)
        if not target or not port:
            raise argparse.ArgumentTypeError("targeted input must use NODE::PORT=REF")
        return {"target": target, "port": port, "ref": ref.strip()}
    return {"type": selector, "ref": ref.strip()}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover_parser = subparsers.add_parser("discover", help="deep-search full capability contracts")
    discover_parser.add_argument("query")
    discover_parser.add_argument("--limit", type=int, default=8)
    discover_parser.add_argument("--advertised-only", action="store_true")
    discover_parser.add_argument(
        "--all-objects",
        action="store_true",
        help="include skill, workflow, tool, guard, adapter, and human-gate implementations",
    )

    plan_parser = subparsers.add_parser("plan", help="build a task-local DAG from explicit selections")
    plan_parser.add_argument("--query", required=True)
    plan_parser.add_argument("--select", action="append", required=True, dest="selected")
    plan_parser.add_argument("--input", action="append", default=[], type=parse_external_input, dest="inputs")
    plan_parser.add_argument("--format", choices=("json", "markdown"), default="json")
    plan_parser.add_argument("--out", type=Path)

    validate_parser = subparsers.add_parser("validate-plan", help="validate an existing task-local DAG")
    validate_parser.add_argument("path", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = args.repo_root.resolve()
    try:
        if args.command == "discover":
            graph = capability_system.load_graph(repo_root)
            rows = capability_system.discover(
                graph,
                args.query,
                limit=args.limit,
                include_internal=not args.advertised_only,
                kinds=None if args.all_objects or args.advertised_only else {"capability", "mode"},
                visibilities={"advertised"} if args.advertised_only else None,
            )
            print(capability_system.dump_json({"query": args.query, "candidates": rows}), end="")
            return 0
        if args.command == "plan":
            graph = capability_system.load_graph(repo_root)
            payload = capability_system.build_task_dag(
                graph,
                query=args.query,
                selected_capabilities=args.selected,
                external_inputs=args.inputs,
            )
            issues = capability_system.validate_task_dag(repo_root, payload)
            if issues:
                raise capability_system.CapabilityContractError("\n".join(issues))
            text = (
                capability_system.dump_json(payload)
                if args.format == "json"
                else capability_system.render_task_dag_markdown(payload)
            )
            if args.out:
                args.out.parent.mkdir(parents=True, exist_ok=True)
                args.out.write_text(text, encoding="utf-8", newline="\n")
            else:
                print(text, end="")
            return 0 if payload["status"] == "ready" else 2
        payload = json.loads(args.path.read_text(encoding="utf-8"))
        issues = capability_system.validate_task_dag(repo_root, payload)
        if issues:
            print("task-local DAG invalid:")
            for issue in issues:
                print(f"- {issue}")
            return 1
        print(f"task-local DAG valid: {payload['plan_id']} ({payload['status']})")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"capability DAG command failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
