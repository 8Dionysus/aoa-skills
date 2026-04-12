from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLISH_SCRIPT_PATH = REPO_ROOT / "scripts" / "publish_core_skill_receipts.py"

PACKET_PATHS = {
    "decision_fork": "examples/session_growth_artifacts/decision_fork.wave4.json",
    "diagnosis_packet": "examples/session_growth_artifacts/diagnosis_packet.wave4.json",
    "repair_cycle": "examples/session_growth_artifacts/repair_cycle.wave4.json",
    "progression_delta": "examples/session_growth_artifacts/progression_delta.wave4.json",
    "automation_candidate": "examples/session_growth_artifacts/automation_candidate.wave4.json",
}

DETAIL_RECEIPT_CASES = {
    "decision_fork": (
        "examples/session_growth_artifacts/decision_fork_receipt.wave4.json",
        "skills/aoa-session-route-forks/references/decision-fork-receipt-schema.yaml",
        PACKET_PATHS["decision_fork"],
    ),
    "diagnosis_packet": (
        "examples/session_growth_artifacts/diagnosis_packet_receipt.wave4.json",
        "skills/aoa-session-self-diagnose/references/diagnosis-packet-receipt-schema.yaml",
        PACKET_PATHS["diagnosis_packet"],
    ),
    "repair_cycle": (
        "examples/session_growth_artifacts/repair_cycle_receipt.wave4.json",
        "skills/aoa-session-self-repair/references/repair-cycle-receipt-schema.yaml",
        PACKET_PATHS["repair_cycle"],
    ),
    "progression_delta": (
        "examples/session_growth_artifacts/progression_delta_receipt.wave4.json",
        "skills/aoa-session-progression-lift/references/progression-delta-receipt-schema.yaml",
        PACKET_PATHS["progression_delta"],
    ),
    "automation_candidate": (
        "examples/session_growth_artifacts/automation_candidate_receipt.wave4.json",
        "skills/aoa-automation-opportunity-scan/references/automation-candidate-receipt-schema.yaml",
        PACKET_PATHS["automation_candidate"],
    ),
}

SOURCE_REVIEWED_ARTIFACT_REF = "repo:aoa-sdk/examples/closeout_followthrough_decision.example.json"


def _load_json(relative_path: str):
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def _load_receipt_contract(relative_path: str) -> dict[str, object]:
    text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
    event_kind: str | None = None
    required_payload_fields: list[str] = []
    in_required_fields = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("event_kind:"):
            event_kind = line.split(":", 1)[1].strip()
            in_required_fields = False
            continue
        if line.startswith("required_payload_fields:"):
            in_required_fields = True
            continue
        if in_required_fields:
            stripped = line.strip()
            if stripped.startswith("- "):
                required_payload_fields.append(stripped[2:].strip())
                continue
            if stripped:
                in_required_fields = False

    assert event_kind is not None
    return {
        "event_kind": event_kind,
        "required_payload_fields": required_payload_fields,
    }


def _load_module(name: str, path: Path):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    try:
        spec.loader.exec_module(module)
        return module
    finally:
        if sys.path and sys.path[0] == str(path.parent):
            sys.path.pop(0)


def test_session_growth_kernel_maturity_docs_route_to_live_wave4_family() -> None:
    doc = (REPO_ROOT / "docs" / "SESSION_GROWTH_KERNEL_MATURITY.md").read_text(encoding="utf-8")
    docs_map = (REPO_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    candidate_doc = (REPO_ROOT / "docs" / "CANDIDATE_REF_REFINERY.md").read_text(encoding="utf-8")

    assert "examples/session_growth_artifacts/" in doc
    assert "examples/session-growth-kernel/" in doc
    assert "SESSION_GROWTH_KERNEL_MATURITY.md" in docs_map
    assert "SESSION_GROWTH_KERNEL_MATURITY.md" in readme
    assert "SESSION_GROWTH_KERNEL_MATURITY.md" in candidate_doc
    assert "must not mint `seed_ref` or `object_ref`" in doc


def test_wave4_kernel_packets_keep_reviewed_source_and_one_lineage_chain() -> None:
    cluster_refs = set()
    candidate_refs = set()

    for relative_path in PACKET_PATHS.values():
        packet = _load_json(relative_path)
        assert packet["source_reviewed_artifact_ref"] == SOURCE_REVIEWED_ARTIFACT_REF
        assert packet["status_posture"] in {"early", "reanchor", "thin-evidence", "stable"}
        lineage_refs = packet["lineage_refs"]
        cluster_refs.add(lineage_refs["cluster_ref"])
        candidate_refs.add(lineage_refs["candidate_ref"])
        assert any(
            field in packet
            for field in (
                "owner_hints",
                "owner_targets",
                "owner_target",
                "owner_layer",
                "target_owner_repo",
            )
        )
        assert (
            "defer_condition" in packet
            or "stop_conditions" in packet
            or any("stop_condition" in card for card in packet.get("cards", []))
        )

    assert cluster_refs == {"cluster:route:aoa-playbooks-playbook-registry-min"}
    assert candidate_refs == {"candidate:aoa-skills:2026-04-11:reviewed-automation-followthrough"}


def test_wave4_detail_receipts_follow_skill_contracts_and_point_back_to_packets() -> None:
    for receipt_path, schema_path, packet_path in DETAIL_RECEIPT_CASES.values():
        receipt = _load_json(receipt_path)
        packet = _load_json(packet_path)
        schema = _load_receipt_contract(schema_path)

        assert receipt["event_kind"] == schema["event_kind"]
        assert receipt["object_ref"]["repo"] == "aoa-skills"
        assert receipt["object_ref"]["kind"] == "skill"
        assert all(field in receipt["payload"] for field in schema["required_payload_fields"])
        assert any(
            ref.get("role") == "primary" and ref.get("ref") == f"repo:aoa-skills/{packet_path}"
            for ref in receipt["evidence_refs"]
        )
        assert len(json.dumps(receipt["payload"], sort_keys=True)) < len(
            json.dumps(packet, sort_keys=True)
        )


def test_wave4_core_receipts_validate_against_live_kernel_publisher() -> None:
    module = _load_module("publish_core_skill_receipts", PUBLISH_SCRIPT_PATH)
    receipts = _load_json("examples/session_growth_artifacts/core_skill_application_receipts.wave4.json")
    detail_receipt_refs = {
        f"repo:aoa-skills/{receipt_path}" for receipt_path, _, _ in DETAIL_RECEIPT_CASES.values()
    }

    assert isinstance(receipts, list)
    assert len(receipts) == 5

    for index, receipt in enumerate(receipts):
        module.validate_receipt(receipt, location=f"wave4[{index}]")
        assert receipt["payload"]["detail_receipt_ref"] in detail_receipt_refs
