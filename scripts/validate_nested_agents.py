#!/usr/bin/env python3
"""Validate required nested AGENTS.md documents for aoa-skills."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class AgentsDocSpec:
    path: Path
    required_snippets: tuple[str, ...]


REQUIRED_DOCS: tuple[AgentsDocSpec, ...] = (
    AgentsDocSpec(
        Path("skills") / "AGENTS.md",
        (
            "# AGENTS.md",
            "`SKILL.md`",
            "`techniques.yaml`",
            "`agents/openai.yaml`",
            "Do not add per-bundle `AGENTS.md` by default",
            "`python scripts/validate_nested_agents.py`",
        ),
    ),
    AgentsDocSpec(
        Path("generated") / "AGENTS.md",
        (
            "# AGENTS.md",
            "Do not hand-author files in `generated/`",
            "`skill_catalog.json`",
            "`python scripts/build_catalog.py`",
            "`python scripts/build_catalog.py --check`",
        ),
    ),
    AgentsDocSpec(
        Path("templates") / "AGENTS.md",
        (
            "# AGENTS.md",
            "`SKILL.template.md`",
            "`PROJECT_OVERLAY.template.md`",
            "Preserve placeholder intent",
            "`python scripts/validate_skills.py`",
        ),
    ),
    AgentsDocSpec(
        Path("docs") / "overlays" / "AGENTS.md",
        (
            "# AGENTS.md",
            "`PROJECT_OVERLAY.md`",
            "`REVIEW.md`",
            "`skills/<family>-*`",
            "thin overlay",
            "downstream integration",
        ),
    ),
)


def validate(repo_root: Path) -> list[str]:
    issues: list[str] = []
    for spec in REQUIRED_DOCS:
        path = repo_root / spec.path
        if not path.is_file():
            issues.append(f"{spec.path.as_posix()}: file is missing")
            continue

        text = path.read_text(encoding="utf-8")
        for snippet in spec.required_snippets:
            if snippet not in text:
                issues.append(
                    f"{spec.path.as_posix()}: missing required snippet {snippet!r}"
                )
    return issues


def main() -> int:
    issues = validate(REPO_ROOT)
    if issues:
        print("Nested AGENTS validation failed.")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(f"Nested AGENTS validation passed for {len(REQUIRED_DOCS)} documents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
