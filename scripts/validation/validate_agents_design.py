#!/usr/bin/env python3
"""Validate the aoa-skills AGENTS.md design mesh."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]

CANONICAL_HEADINGS: tuple[str, ...] = (
    "## Applies to",
    "## Role",
    "## Read before editing",
    "## Boundaries",
    "## Validation",
    "## Closeout",
)

REQUIRED_OWNER_CARDS: tuple[Path, ...] = tuple(
    Path(path)
    for path in (
        "AGENTS.md",
        "capabilities/AGENTS.md",
        "config/AGENTS.md",
        "docs/AGENTS.md",
        "docs/decisions/AGENTS.md",
        "generated/AGENTS.md",
        "kag/AGENTS.md",
        "mechanics/AGENTS.md",
        "mechanics/questbook/AGENTS.md",
        "mechanics/release-support/AGENTS.md",
        "schemas/AGENTS.md",
        "scripts/AGENTS.md",
        "skills/AGENTS.md",
        "templates/AGENTS.md",
        "tests/AGENTS.md",
    )
)

IGNORED_PARTS = {".git", ".pytest_cache", ".ruff_cache", "__pycache__"}


def _display(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def iter_agent_cards(repo_root: Path) -> list[Path]:
    tracked_cards = _tracked_agent_cards(repo_root)
    if tracked_cards is not None:
        cards = [path for path in tracked_cards if path.exists()]
        for expected in REQUIRED_OWNER_CARDS:
            path = repo_root / expected
            if path.exists():
                cards.append(path)
        return sorted(set(cards))

    cards: list[Path] = []
    for path in repo_root.rglob("AGENTS.md"):
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        cards.append(path)
    return sorted(cards)


def _tracked_agent_cards(repo_root: Path) -> list[Path] | None:
    result = subprocess.run(
        ("git", "-C", repo_root.as_posix(), "ls-files", "-z"),
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        return None

    paths: list[Path] = []
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        path = Path(raw_path.decode())
        if path.name == "AGENTS.md":
            paths.append(repo_root / path)
    return sorted(paths)


def _section_body(lines: list[str], heading: str, next_heading: str | None) -> str:
    start = lines.index(heading) + 1
    if next_heading is None:
        end = len(lines)
    else:
        end = lines.index(next_heading)
    return "\n".join(lines[start:end]).strip()


def validate(repo_root: Path = REPO_ROOT) -> list[str]:
    issues: list[str] = []
    seen = {path.relative_to(repo_root) for path in iter_agent_cards(repo_root)}

    for expected in REQUIRED_OWNER_CARDS:
        if expected not in seen:
            issues.append(f"{expected.as_posix()}: expected AGENTS.md card is missing")

    for path in iter_agent_cards(repo_root):
        rel = _display(path, repo_root)
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        if not lines or lines[0] != "# AGENTS.md":
            issues.append(f"{rel}: must start with '# AGENTS.md'")
            continue

        headings = [line for line in lines if line.startswith("## ")][: len(CANONICAL_HEADINGS)]
        if tuple(headings) != CANONICAL_HEADINGS:
            issues.append(
                f"{rel}: first section headings must be "
                f"{', '.join(CANONICAL_HEADINGS)}"
            )
            continue

        for index, heading in enumerate(CANONICAL_HEADINGS):
            next_heading = (
                CANONICAL_HEADINGS[index + 1]
                if index + 1 < len(CANONICAL_HEADINGS)
                else None
            )
            if not _section_body(lines, heading, next_heading):
                issues.append(f"{rel}: section {heading!r} must not be empty")

    return issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the aoa-skills AGENTS.md design mesh."
    )
    parser.add_argument(
        "--repo-root",
        default=REPO_ROOT,
        type=Path,
        help="Repository root to validate. Defaults to the aoa-skills checkout.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = args.repo_root.resolve()
    issues = validate(repo_root)
    if issues:
        print("AGENTS design validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print(
        f"[ok] AGENTS design mesh is present and canonical: "
        f"{len(iter_agent_cards(repo_root))} cards"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
