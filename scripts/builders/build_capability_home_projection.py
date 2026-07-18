#!/usr/bin/env python3
"""Build one owner's deterministic capability graph and routing card."""

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
    parser.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        port = capability_home_port.load_port(
            CONTRACT_ROOT,
            args.owner_root,
            args.manifest,
        )
        if args.check:
            stale = capability_home_port.generated_issues(port)
            if stale:
                print("owner capability projections are out of date:")
                for path in stale:
                    print(f"- {path}")
                return 1
        else:
            capability_home_port.write_outputs(port)
    except (OSError, ValueError) as exc:
        print(f"capability home build failed: {exc}")
        return 1
    print(
        "owner capability projections are current"
        if args.check
        else "owner capability projections rebuilt"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

