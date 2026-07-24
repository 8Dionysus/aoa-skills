from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    REPO_ROOT
    / "scripts"
    / "validation"
    / "validate_abyss_machine_artifact_bundle.py"
)


def load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "validate_abyss_machine_artifact_bundle",
        VALIDATOR_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_gate() -> dict:
    return {
        "ok": True,
        "verdict": "allow",
        "decision": {
            "model": "fail_closed_consumer_admission",
            "allow": True,
        },
        "inspected_claims": {
            "registry_latest": {"selected_record_is_latest": True},
            "controls": {"required_controls_missing": []},
            "source": {"source_repo_matched": True},
            "trust_root": {"trust_root_mode_matched": True},
            "artifact_subject_store": {"ok": True},
        },
    }


def test_consumer_admission_fails_closed_on_every_required_claim() -> None:
    validator = load_validator()
    gate = valid_gate()

    assert validator.consumer_admission_status(gate)["ok"] is True

    invalid_gates = [
        {**gate, "ok": False},
        {**gate, "verdict": "deny"},
        {
            **gate,
            "decision": {
                "model": "fail_closed_consumer_admission",
                "allow": False,
            },
        },
        {
            **gate,
            "inspected_claims": {
                **gate["inspected_claims"],
                "registry_latest": {"selected_record_is_latest": False},
            },
        },
        {
            **gate,
            "inspected_claims": {
                **gate["inspected_claims"],
                "controls": {"required_controls_missing": ["abi_signature"]},
            },
        },
        {
            **gate,
            "inspected_claims": {
                **gate["inspected_claims"],
                "source": {"source_repo_matched": False},
            },
        },
        {
            **gate,
            "inspected_claims": {
                **gate["inspected_claims"],
                "trust_root": {"trust_root_mode_matched": False},
            },
        },
        {
            **gate,
            "inspected_claims": {
                **gate["inspected_claims"],
                "artifact_subject_store": {"ok": False},
            },
        },
    ]

    for invalid_gate in invalid_gates:
        status = validator.consumer_admission_status(invalid_gate)
        assert status["ok"] is False
        assert status["failed_checks"]

    for malformed_group in (
        "registry_latest",
        "controls",
        "source",
        "trust_root",
        "artifact_subject_store",
    ):
        malformed_gate = {
            **gate,
            "inspected_claims": {
                **gate["inspected_claims"],
                malformed_group: None,
            },
        }
        status = validator.consumer_admission_status(malformed_gate)
        assert status["ok"] is False
        assert status["failed_checks"]


def test_expected_control_drift_is_a_structured_failure() -> None:
    validator = load_validator()

    status = validator.expected_controls_status(
        {
            "required_controls": ["abi_signature", "sbom"],
            "verified_controls": ["abi_signature"],
        }
    )

    assert status["ok"] is False
    assert status["expected_required_controls"] == ["abi_signature"]
    assert status["errors"] == [
        "unexpected required controls: ['abi_signature', 'sbom']"
    ]


def test_compact_failure_keeps_public_safe_diagnostics() -> None:
    validator = load_validator()

    output = validator.compact_payload(
        {
            "ok": False,
            "schema": "aoa_skills_abyss_machine_artifact_bundle_validation_v1",
            "error": "manual_failure",
            "detail": "diagnostic detail needed by caller",
            "checked_roots": [str(validator.REPO_ROOT)],
        }
    )

    assert output["error"] == "manual_failure"
    assert output["detail"] == "diagnostic detail needed by caller"
    assert output["checked_roots"] == ["."]
