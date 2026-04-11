from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_json(relative_path: str) -> dict:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def _load_yaml(relative_path: str) -> dict:
    return yaml.safe_load((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_session_checkpoint_note_schema_validates_example() -> None:
    schema = _load_json("schemas/session_checkpoint_note.schema.json")
    example = _load_json("examples/session_checkpoint_note.example.json")

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(example)


def test_checkpoint_docs_keep_pre_harvest_boundary_explicit() -> None:
    checkpoint_doc = (REPO_ROOT / "docs" / "CHECKPOINT_NOTE_PATH.md").read_text(encoding="utf-8")
    questbook_doc = (REPO_ROOT / "docs" / "QUESTBOOK_SKILL_INTEGRATION.md").read_text(encoding="utf-8")

    assert "checkpoint capture is not harvest verdict" in checkpoint_doc
    assert "checkpoint capture does not mint `candidate_ref`" in checkpoint_doc
    assert "pre-harvest reviewed note" in questbook_doc
    assert "not a replacement for the reviewed session-harvest family" in questbook_doc
    assert "first candidate-ref minting seam" in questbook_doc


def test_candidate_lineage_receipt_schema_validates_example() -> None:
    schema = _load_yaml(
        "skills/aoa-session-donor-harvest/references/candidate-lineage-receipt-schema.yaml"
    )
    example = _load_json("examples/session_growth_artifacts/candidate_lineage_receipt.alpha.json")

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(example)


def test_candidate_lineage_receipt_schema_requires_posture_context() -> None:
    schema = _load_yaml(
        "skills/aoa-session-donor-harvest/references/candidate-lineage-receipt-schema.yaml"
    )
    example = _load_json("examples/session_growth_artifacts/candidate_lineage_receipt.alpha.json")
    del example["nearest_wrong_target"]

    errors = [error.message for error in Draft202012Validator(schema).iter_errors(example)]

    assert "'nearest_wrong_target' is a required property" in errors


def test_harvest_packet_receipt_allows_candidate_lineage_entries_without_seed_or_object_refs() -> None:
    schema = _load_yaml(
        "skills/aoa-session-donor-harvest/references/harvest-packet-receipt-schema.yaml"
    )
    receipt_family = json.loads(
        (REPO_ROOT / "examples" / "session_harvest_family.receipts.example.json").read_text(
            encoding="utf-8"
        )
    )
    harvest_receipt = receipt_family[0]
    lineage_entries = harvest_receipt["payload"]["candidate_lineage_entries"]

    assert "candidate_lineage_entries" in schema["optional_payload_fields"]
    assert lineage_entries
    assert all("seed_ref" not in entry for entry in lineage_entries)
    assert all("object_ref" not in entry for entry in lineage_entries)
    assert any("must not carry seed_ref or object_ref" in rule for rule in schema["rules"])


def test_core_ring_skills_remain_explicit_only() -> None:
    catalog = _load_json("generated/skill_catalog.min.json")
    expected = {
        "aoa-session-donor-harvest",
        "aoa-session-route-forks",
        "aoa-session-self-diagnose",
        "aoa-session-self-repair",
        "aoa-session-progression-lift",
        "aoa-automation-opportunity-scan",
        "aoa-quest-harvest",
    }
    modes = {
        entry["name"]: entry["invocation_mode"]
        for entry in catalog["skills"]
        if entry["name"] in expected
    }

    assert set(modes) == expected
    assert all(mode == "explicit-only" for mode in modes.values())


def test_kernel_stage_and_live_receipt_family_do_not_expand_for_checkpoints() -> None:
    kernel = _load_json("config/project_core_skill_kernel.json")
    publish_script = (REPO_ROOT / "scripts" / "publish_live_receipts.py").read_text(encoding="utf-8")

    assert kernel["governance_contract"]["application_stage"] == "finish"
    assert "checkpoint_note_receipt" not in publish_script
    assert "session_checkpoint_note_v1" not in publish_script
