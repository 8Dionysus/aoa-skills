#!/usr/bin/env python3
"""Validate one repository-owned capability home and its generated projections."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from skill_model import capability_home_port


CONTRACT_ROOT = Path(__file__).resolve().parents[2]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner-root", type=Path, required=True)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=capability_home_port.DEFAULT_MANIFEST,
    )
    parser.add_argument("--check-generated", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        port = capability_home_port.load_port(
            CONTRACT_ROOT,
            args.owner_root,
            args.manifest,
        )
        families = capability_home_port.validate_sources(port)
        stale = (
            capability_home_port.generated_issues(port)
            if args.check_generated
            else []
        )
        if stale:
            raise capability_home_port.CapabilityHomePortError(
                "generated owner capability projections are stale: "
                + ", ".join(stale)
            )
    except (OSError, ValueError) as exc:
        print(f"capability home validation failed: {exc}")
        return 1
    node_count = sum(len(family["nodes"]) for _, family in families)
    print(
        f"capability home valid: {port.owner_repo}, "
        f"{len(families)} families, {node_count} nodes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

