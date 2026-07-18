from __future__ import annotations

import json
import sys
from pathlib import Path
import tempfile

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from export import build_agent_skills
from skill_model import capability_system, skill_source_model
from validation import validate_skills
from validation.validators import agent_skills_export_surface


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_portable_surfaces_match_authored_disposition() -> None:
    assert validate_skills.validate_source_skills(REPO_ROOT) == []
    assert agent_skills_export_surface.validate_export(REPO_ROOT) == []

    source_names = {
        source.name for source in skill_source_model.load_skill_sources(REPO_ROOT)
    }
    catalog = load_json(REPO_ROOT / "generated/agent_skill_catalog.json")
    policies = load_json(REPO_ROOT / "config/skill_policy_matrix.json")["skills"]

    assert source_names == {entry["name"] for entry in catalog["skills"]}
    families = capability_system.validate_sources(REPO_ROOT)
    nodes = capability_system.node_map(families)
    advertised = {
        name
        for name in source_names
        if nodes[f"skill.{name}"]["lifecycle"]["visibility"] == "advertised"
    }
    assert {
        name
        for name, row in policies.items()
        if row["implicit_activation_policy"] == "invoke"
    } == advertised
    for source in skill_source_model.load_skill_sources(REPO_ROOT):
        policy = policies[source.name]["implicit_activation_policy"]
        openai = yaml.safe_load(source.policy_path.read_text(encoding="utf-8"))
        assert bool(openai["policy"]["allow_implicit_invocation"]) == (policy == "invoke")
    assert not list((REPO_ROOT / "skills").rglob("techniques.yaml"))
    assert not (REPO_ROOT / ".agents/skills").exists()


def test_release_manifest_is_reproducible_and_binds_portable_bytes() -> None:
    live = load_json(REPO_ROOT / "generated/release_manifest.json")
    with tempfile.TemporaryDirectory(prefix="aoa-skills-test-portable-") as temp_dir:
        portable_root = Path(temp_dir)
        inputs = build_agent_skills.load_export_build_inputs(REPO_ROOT)
        documents = build_agent_skills.build_portable_skill_exports(
            inputs,
            portable_root,
        )
        expected_generated = build_agent_skills.build_generated_file_texts(
            inputs,
            documents,
            portable_root,
        )
        rebuilt = json.loads(
            expected_generated[
                REPO_ROOT / "generated" / "release_manifest.json"
            ]
        )

    assert live == rebuilt
    source_count = len(skill_source_model.load_skill_sources(REPO_ROOT))
    assert live["skill_count"] == source_count
    assert live["advertised_skill_count"] + live["deferred_skill_count"] == source_count
    assert {
        "schemas/capability-home-port.schema.json",
        "schemas/task_local_dag_v2.schema.json",
    } <= set(live["source_files"])
    for revision in live["skill_bundle_revisions"]:
        assert revision["source_hash"] != ""
        assert revision["portable_hash"] != ""
