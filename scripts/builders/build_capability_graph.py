#!/usr/bin/env python3
"""Build the derived capability graph from authored family contracts."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from skill_model import capability_system


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    try:
        outputs = capability_system.build_graph_outputs(repo_root)
        stale: list[str] = []
        for path, expected in outputs.items():
            if args.check:
                current = path.read_text(encoding="utf-8") if path.is_file() else None
                if current != expected:
                    stale.append(capability_system.relative_path(path, repo_root))
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8", newline="\n")
        if stale:
            print("capability graph is out of date:")
            for path in stale:
                print(f"- {path}")
            return 1
    except (OSError, ValueError) as exc:
        print(f"capability graph build failed: {exc}")
        return 1
    print("capability graph is current" if args.check else "capability graph rebuilt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
