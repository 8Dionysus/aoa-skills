from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from export import release_manifest_contract
from skill_model import skill_source_model
from validation import validate_skills
from validation.validators import agent_skills_export_surface


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_portable_surfaces_match_the_seven_family_disposition() -> None:
    assert validate_skills.validate_source_skills(REPO_ROOT) == []
    assert agent_skills_export_surface.validate_export(REPO_ROOT) == []

    source_names = {
        source.name for source in skill_source_model.load_skill_sources(REPO_ROOT)
    }
    catalog = load_json(REPO_ROOT / "generated/agent_skill_catalog.json")
    policies = load_json(REPO_ROOT / "config/skill_policy_matrix.json")["skills"]

    assert len(source_names) == 7
    assert source_names == {entry["name"] for entry in catalog["skills"]}
    assert [name for name, row in policies.items() if row["implicit_activation_policy"] == "invoke"] == [
        "aoa-decision"
    ]
    for source in skill_source_model.load_skill_sources(REPO_ROOT):
        policy = policies[source.name]["implicit_activation_policy"]
        mode = source.metadata["invocation_mode"]
        assert (policy == "invoke") == (mode == "implicit-friendly")
    assert not list((REPO_ROOT / "skills").rglob("techniques.yaml"))
    assert not list((REPO_ROOT / ".agents/skills").rglob("techniques.yaml"))


def test_release_manifest_is_reproducible_and_binds_portable_bytes() -> None:
    live = load_json(REPO_ROOT / "generated/release_manifest.json")
    rebuilt = release_manifest_contract.build_release_manifest(REPO_ROOT)

    assert live == rebuilt
    assert live["skill_count"] == 7
    assert live["advertised_skill_count"] == 1
    assert live["deferred_skill_count"] == 6
    for revision in live["skill_bundle_revisions"]:
        assert revision["source_hash"] != ""
        assert revision["portable_hash"] != ""
