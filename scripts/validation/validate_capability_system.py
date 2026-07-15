#!/usr/bin/env python3
"""Validate authored capability families and the derived graph contract."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from skill_model import capability_system


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--check-generated", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    try:
        families = capability_system.validate_sources(repo_root)
        if args.check_generated:
            expected = capability_system.build_graph_outputs(repo_root)
            stale = [
                capability_system.relative_path(path, repo_root)
                for path, text in expected.items()
                if not path.is_file() or path.read_text(encoding="utf-8") != text
            ]
            if stale:
                raise capability_system.CapabilityContractError(
                    "generated capability surfaces are stale: " + ", ".join(stale)
                )
    except (OSError, ValueError) as exc:
        print(f"capability system validation failed: {exc}")
        return 1
    node_count = sum(len(family["nodes"]) for _, family in families)
    print(f"capability system valid: {len(families)} families, {node_count} nodes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
