#!/usr/bin/env python3
"""Report cross-repo technique drift between aoa-skills and aoa-techniques."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path
from typing import Sequence

import technique_bridge_tools


REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report technique drift against a local aoa-techniques checkout."
    )
    parser.add_argument(
        "--techniques-repo",
        default=str(technique_bridge_tools.DEFAULT_TECHNIQUES_REPO),
        help="Path to the local aoa-techniques checkout.",
    )
    parser.add_argument(
        "--target-ref",
        default="HEAD",
        help="Git ref in aoa-techniques to compare against. Defaults to HEAD.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        dest="skills",
        help="Limit reporting to the explicitly named skill. Repeatable.",
    )
    parser.add_argument(
        "--fail-on-drift",
        action="store_true",
        help="Exit with code 1 when any published technique ref has drifted.",
    )
    return parser.parse_args(argv)


def build_report(
    techniques_repo: Path,
    target_ref: str,
    records: list[technique_bridge_tools.TechniqueDriftRecord],
) -> str:
    lines = [
        f"Techniques repo: {techniques_repo}",
        f"Target ref: {target_ref}",
    ]
    if not records:
        lines.append("No skill bundles matched the current selection.")
        return "\n".join(lines)

    current_skill_name: str | None = None
    for record in records:
        if record.skill_name != current_skill_name:
            current_skill_name = record.skill_name
            lines.extend(["", f"Skill: {record.skill_name}"])
        lines.append(
            "- "
            f"{record.technique_id} | path={record.path} | "
            f"pinned_ref={record.pinned_ref} | target_ref={record.target_ref} | "
            f"state={record.state}"
        )

    counter = Counter(record.state for record in records)
    lines.extend(
        [
            "",
            (
                "Summary: "
                f"drifted={counter.get('drifted', 0)} "
                f"clean={counter.get('clean', 0)} "
                f"pending={counter.get('pending', 0)}"
            ),
        ]
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        techniques_repo = technique_bridge_tools.resolve_techniques_repo(
            Path(args.techniques_repo)
        )
        target_ref = technique_bridge_tools.resolve_git_ref(
            techniques_repo, args.target_ref
        )
        bundles = technique_bridge_tools.resolve_skill_bundles(repo_root, args.skills)
        records: list[technique_bridge_tools.TechniqueDriftRecord] = []
        for bundle in bundles:
            records.extend(
                technique_bridge_tools.collect_drift_records(
                    techniques_repo,
                    target_ref,
                    bundle,
                )
            )
    except (RuntimeError, ValueError, FileNotFoundError) as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2

    print(build_report(techniques_repo, target_ref, records))
    if args.fail_on_drift and any(record.state == "drifted" for record in records):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
