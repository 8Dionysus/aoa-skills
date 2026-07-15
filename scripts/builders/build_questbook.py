#!/usr/bin/env python3
"""Build or check the small questbook read-model surface."""

from __future__ import annotations

import argparse
from pathlib import Path

from skill_model import questbook_model


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    outputs = questbook_model.build_outputs(repo_root)
    stale: list[str] = []
    for rel_path, text in outputs.items():
        path = repo_root / rel_path
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != text:
                stale.append(rel_path.as_posix())
        else:
            path.write_text(text, encoding="utf-8")
    if stale:
        print("questbook read models are stale: " + ", ".join(stale))
        return 1
    print(f"questbook read models {'current' if args.check else 'built'}: {len(outputs)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
