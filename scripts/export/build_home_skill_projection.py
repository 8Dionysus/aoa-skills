#!/usr/bin/env python3
"""Preview, check, or build one repository-owned skill projection."""

from __future__ import annotations

import argparse
import json
import sys

from export import home_skill_port


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a repo-scoped .agents/skills projection from an admitted owner skill home."
        )
    )
    parser.add_argument(
        "--owner-root",
        default=".",
        help="Repository that owns skills/port.manifest.json",
    )
    parser.add_argument(
        "--manifest",
        default=home_skill_port.DEFAULT_MANIFEST.as_posix(),
        help="Manifest path relative to the owner repository",
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--check", action="store_true", help="Exit nonzero when projection drift exists"
    )
    action.add_argument("--execute", action="store_true", help="Write the declared projection")
    parser.add_argument(
        "--prune",
        action="store_true",
        help="With --execute, remove undeclared entries from the projection root",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args()


def _emit(payload: dict[str, object], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(home_skill_port.format_plan(payload))


def main() -> int:
    args = parse_args()
    if args.prune and not args.execute:
        print("--prune requires --execute", file=sys.stderr)
        return 2
    try:
        port = home_skill_port.load_port_definition(args.owner_root, args.manifest)
        plan = (
            home_skill_port.apply_projection(port, prune=args.prune)
            if args.execute
            else home_skill_port.projection_plan(port)
        )
    except home_skill_port.PortContractError as exc:
        if args.format == "json":
            print(
                json.dumps(
                    {"ok": False, "errors": list(exc.errors)},
                    ensure_ascii=False,
                    indent=2,
                )
            )
        else:
            for error in exc.errors:
                print(f"[error] {error}", file=sys.stderr)
        return 1
    _emit(plan, args.format)
    return 1 if args.check and not plan["clean"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
