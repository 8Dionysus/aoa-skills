#!/usr/bin/env python3
"""Validate one canonical owner skill home and its declared exposure boundary."""

from __future__ import annotations

import argparse
import json
import sys

from export import home_skill_port


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate owner source shape and either deprecated v1 repository "
            "projection parity or v2 OS-profile exposure."
        )
    )
    parser.add_argument("--owner-root", default=".")
    parser.add_argument("--manifest", default=home_skill_port.DEFAULT_MANIFEST.as_posix())
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        port = home_skill_port.load_port_definition(args.owner_root, args.manifest)
        plan = home_skill_port.validation_plan(port)
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

    if args.format == "json":
        result_key = (
            "projection"
            if plan["schema_version"] == "aoa_skill_home_projection_plan_v1"
            else "source"
        )
        print(
            json.dumps(
                {"ok": bool(plan["clean"]), result_key: plan},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(home_skill_port.format_plan(plan))
    return 0 if plan["clean"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
