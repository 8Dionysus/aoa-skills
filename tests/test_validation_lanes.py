from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from decisions import decision_indexes
from lanes import validation_lanes


def test_lane_commands_point_to_live_scripts_and_exclude_retired_ontology() -> None:
    manifest_text = (REPO_ROOT / "config/validation_lanes.json").read_text(
        encoding="utf-8"
    )
    manifest = json.loads(manifest_text)
    retired_tokens = (
        "build_catalog.py",
        "tiny_router",
        "runtime_seam",
        "runtime_guardrail",
        "description_trigger",
        "technique",
        "project_core",
        "risk_guard",
    )

    assert manifest["schema_version"] == 2
    assert not any(token in manifest_text for token in retired_tokens)
    for sequence in manifest["command_sequences"].values():
        for command in sequence:
            if command[0] == "python" and command[1].endswith(".py"):
                assert (REPO_ROOT / command[1]).is_file(), command


def test_source_lane_is_structural_and_decision_indexes_remain_current() -> None:
    commands = validation_lanes.SOURCE_FAST_COMMAND_SEQUENCE

    assert all("generated" not in " ".join(command) for command in commands)
    assert all("pytest" not in command for command in commands)
    assert decision_indexes.validate_decision_index_surfaces(REPO_ROOT) == []


def test_agents_mesh_keeps_inherited_ancestor_cards_implicit() -> None:
    from validation import validate_agents_design

    assert validate_agents_design._ancestor_agent_cards(
        Path("skills/core/engineering/AGENTS.md")
    ) == (
        Path("AGENTS.md"),
        Path("skills/AGENTS.md"),
        Path("skills/core/AGENTS.md"),
    )
    assert validate_agents_design._mentions_path(
        "Read `skills/AGENTS.md` first.", Path("skills/AGENTS.md")
    )
    assert not validate_agents_design._mentions_path(
        "Use `DESIGN.AGENTS.md` for card shape.", Path("AGENTS.md")
    )
    assert validate_agents_design.validate(REPO_ROOT) == []
