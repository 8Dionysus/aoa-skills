#!/usr/bin/env python3
"""Discover or compose capabilities from one owner capability home."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from skill_model import capability_home_port, capability_system


CONTRACT_ROOT = Path(__file__).resolve().parents[2]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner-root", type=Path, required=True)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=capability_home_port.DEFAULT_MANIFEST,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    discover = subparsers.add_parser("discover")
    discover.add_argument("query")
    discover.add_argument("--limit", type=int, default=8)
    plan = subparsers.add_parser("plan")
    plan.add_argument("query")
    plan.add_argument("--select", action="append", required=True)
    plan.add_argument("--input", action="append", default=[])
    return parser.parse_args(argv)


def parse_inputs(values: Sequence[str]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for value in values:
        if "=" not in value:
            raise ValueError("--input must use TYPE=REF or NODE::PORT=REF")
        selector, ref = value.split("=", 1)
        selector = selector.strip()
        ref = ref.strip()
        if not selector or not ref:
            raise ValueError(
                "--input must use non-empty TYPE=REF or NODE::PORT=REF"
            )
        if "::" in selector:
            target, port = selector.split("::", 1)
            if not target or not port:
                raise ValueError(
                    "targeted --input must use NODE::PORT=REF"
                )
            result.append({"target": target, "port": port, "ref": ref})
        else:
            result.append({"type": selector, "ref": ref})
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        port = capability_home_port.load_port(
            CONTRACT_ROOT,
            args.owner_root,
            args.manifest,
        )
        graph = capability_home_port.load_owner_graph(port)
        if args.command == "discover":
            payload = capability_system.discover_two_stage(
                graph,
                args.query,
                candidate_limit=args.limit,
                rerank_limit=args.limit,
            )
            payload["source_hash"] = graph["source"]["content_hash"]
        else:
            payload = capability_system.build_task_dag(
                graph,
                query=args.query,
                selected_capabilities=args.select,
                external_inputs=parse_inputs(args.input),
            )
            issues = capability_home_port.validate_task_dag(port, graph, payload)
            if issues:
                raise capability_home_port.CapabilityHomePortError("\n".join(issues))
    except (OSError, ValueError) as exc:
        print(f"capability home runtime failed: {exc}")
        return 1
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
    if args.command == "plan":
        return 0 if payload["status"] == "ready" else 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
