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
        Path("mechanics") / "AGENTS.md",
        (
            "# AGENTS.md",
            "`mechanics/` owns skill-layer movement surfaces",
            "`skills/` owns executable skill content",
            "Package README cards use `Local owns`",
            "`python scripts/validate_nested_agents.py`",
        ),
    ),
    AgentsDocSpec(
        Path("mechanics") / "agon" / "AGENTS.md",
        (
            "# AGENTS.md",
            "`mechanics/agon/`",
            "requested-only",
            "`python mechanics/agon/parts/workflow-candidate-bridge/scripts/build_agon_skill_binding_candidates.py --check`",
            "`tests/test_mechanics_topology.py`",
        ),
    ),
    AgentsDocSpec(
        Path("mechanics") / "method-growth" / "AGENTS.md",
        (
            "# AGENTS.md",
            "`mechanics/method-growth/`",
            "candidate lineage",
            "python -m pytest -q tests/test_session_checkpoint_note.py tests/test_session_growth_kernel_maturity.py",
        ),
    ),
    AgentsDocSpec(
        Path("mechanics") / "growth-cycle" / "AGENTS.md",
        (
            "# AGENTS.md",
            "`mechanics/growth-cycle/`",
            "adaptive skill",
            "python -m pytest -q tests/test_session_growth_kernel_maturity.py tests/test_session_checkpoint_note.py",
        ),
    ),
    AgentsDocSpec(
        Path("mechanics") / "checkpoint" / "AGENTS.md",
        (
            "# AGENTS.md",
            "`mechanics/checkpoint/`",
            "checkpoint-note",
            "python -m pytest -q tests/test_session_checkpoint_note.py tests/test_session_growth_kernel_maturity.py",
        ),
    ),
    AgentsDocSpec(
        Path("mechanics") / "questbook" / "AGENTS.md",
        (
            "# AGENTS.md",
            "`mechanics/questbook/`",
            "questbook integration",
            "python -m pytest -q tests/test_validate_skills.py tests/test_session_checkpoint_note.py",
        ),
    ),
    AgentsDocSpec(
        Path("mechanics") / "recurrence" / "AGENTS.md",
        (
            "# AGENTS.md",
            "`mechanics/recurrence/`",
            "recurrence observation",
            "python -m pytest -q tests/test_roadmap_parity.py tests/test_current_direction_routes.py",
        ),
    ),
    AgentsDocSpec(
        Path("mechanics") / "rpg" / "AGENTS.md",
        (
            "# AGENTS.md",
            "`mechanics/rpg/`",
            "ability-reader",
            "python -m pytest -q tests/test_generated_surface_schemas.py tests/test_roadmap_parity.py",
        ),
    ),
    AgentsDocSpec(
        Path("mechanics") / "antifragility" / "AGENTS.md",
        (
            "# AGENTS.md",
            "`mechanics/antifragility/`",
            "collision-stress",
            "python -m pytest -q tests/test_mechanics_topology.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py",
        ),
    ),
    AgentsDocSpec(
        Path("mechanics") / "audit" / "AGENTS.md",
        (
            "# AGENTS.md",
            "Audit package guidance",
            "skill-layer audit posture",
            "docs/AUDIT_CONTRACT.md",
            "python scripts/report_skill_evaluation.py --fail-on-canonical-gaps",
        ),
    ),
    AgentsDocSpec(
        Path("mechanics") / "boundary-bridge" / "AGENTS.md",
        (
            "# AGENTS.md",
            "Boundary-bridge package guidance",
            "skill-layer boundary bridges",
            "overlays/AGENTS.md",
            "python scripts/validate_tiny_router_inputs.py --repo-root .",
        ),
    ),
    AgentsDocSpec(
        Path("mechanics") / "experience" / "AGENTS.md",
        (
            "# AGENTS.md",
            "Experience package guidance",
            "adoption consent",
            "rollback",
            "python scripts/validate_skills.py --fail-on-review-truth-sync",
        ),
    ),
    AgentsDocSpec(
        Path("mechanics") / "release-support" / "AGENTS.md",
        (
            "# AGENTS.md",
            "Release-support package guidance",
            "portable export",
            "legacy/waves/",
            "python scripts/release_check.py",
        ),
    ),
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
        Path("mechanics") / "boundary-bridge" / "overlays" / "AGENTS.md",
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
