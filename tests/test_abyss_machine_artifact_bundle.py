from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validation" / "validate_abyss_machine_artifact_bundle.py"
MANIFEST_PATH = REPO_ROOT / "mechanics" / "release-support" / "manifests" / "release_manifest.bundle.json"
MANIFEST_README_PATH = REPO_ROOT / "mechanics" / "release-support" / "manifests" / "README.md"


def load_validator_module() -> Any:
    spec = importlib.util.spec_from_file_location("aoa_skills_artifact_bundle_validator", VALIDATOR_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeArtifactBundles:
    ABI_SIDECAR = "artifact.abi.json"

    def __init__(self, trust_gate_response: dict[str, Any]) -> None:
        self.trust_gate_response = trust_gate_response
        self.trust_gate_calls: list[dict[str, Any]] = []
        self.materialize_calls: list[dict[str, Any]] = []
        self.records: list[dict[str, Any]] = []

    def trust_gate(self, registry_dir: Path, **kwargs: Any) -> dict[str, Any]:
        self.trust_gate_calls.append({"registry_dir": registry_dir, **kwargs})
        return self.trust_gate_response

    def write_bundle_registry_record(self, bundle_dir: Path, registry_dir: Path, **kwargs: Any) -> dict[str, Any]:
        state = str(kwargs.get("lifecycle_state") or "")
        record = {
            "record_id": f"record-{len(self.records) + 1}",
            "subject_digest": "sha256:" + "1" * 64,
            "lifecycle_state": state,
        }
        self.records.append(record)
        return {"ok": True, "record": record}

    def read_bundle_registry(self, registry_dir: Path, *, artifact_class: str) -> dict[str, Any]:
        release_ready = [record for record in self.records if record.get("lifecycle_state") == "release-ready"]
        latest_record = release_ready[-1] if release_ready else None
        if self.records and self.records[-1].get("lifecycle_state") == "revoked":
            latest_record = None
        if latest_record and os.environ.get("ABYSS_MACHINE_ARTIFACT_SUBJECT_STORE_ROOT"):
            latest_record["artifact_subject_store"] = {"ok": True}
        return {"latest_by_artifact_class": {artifact_class: latest_record} if latest_record else {}}

    def materialize_artifact_subjects(
        self,
        bundle_dir: Path,
        *,
        store_root: Path,
        registry_dir: Path,
        manifest_ref: Path,
        consumer_intent: str,
        expected_source_repo: str,
    ) -> dict[str, Any]:
        self.materialize_calls.append(
            {
                "bundle_dir": bundle_dir,
                "store_root": store_root,
                "registry_dir": registry_dir,
                "manifest_ref": manifest_ref,
                "consumer_intent": consumer_intent,
                "expected_source_repo": expected_source_repo,
            }
        )
        return {"ok": True, "aggregate_digest": "sha256:" + "3" * 64}


def allow_gate_response() -> dict[str, Any]:
    return {
        "ok": True,
        "verdict": "allow",
        "decision": {"model": "fail_closed_consumer_admission", "allow": True},
        "inspected_claims": {
            "registry_latest": {"selected_record_is_latest": True},
            "controls": {"required_controls_missing": []},
            "source": {"source_repo_matched": True},
        },
    }


def deny_terminal_gate_response() -> dict[str, Any]:
    return {
        "ok": True,
        "verdict": "deny",
        "decision": {"model": "fail_closed_consumer_admission", "allow": False},
        "inspected_claims": {"lifecycle": {"terminal_state": True}},
    }


def test_release_manifest_declares_materialized_consumer_trust_gate_path() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    readme = MANIFEST_README_PATH.read_text(encoding="utf-8")
    commands = "\n".join(manifest["consumer_command"])

    assert manifest["artifact_subjects"] == [
        {"path": "generated/release_manifest.json", "role": "generated_release_manifest"}
    ]
    assert manifest["consumer_contract"]["registry_required"] is True
    assert "trust-gate allow/warn" in manifest["consumer_contract"]["consumer_expectation"]
    assert "abyss-machine artifacts bundle-register" in commands
    assert "abyss-machine artifacts materialize-subjects" in commands
    assert "abyss-machine artifacts trust-gate" in commands
    assert "abyss-machine artifacts registry-latest" in commands
    assert "--consumer-ref aoa-skills:release-manifest" in commands
    assert "--source-repo aoa-skills" in commands
    assert "materializes the release-manifest subject store" in readme
    assert "revoked-record" in readme
    assert "denial" in readme


def test_release_manifest_trust_gate_requires_fail_closed_latest_controls_and_source(tmp_path: Path) -> None:
    validator = load_validator_module()
    fake = FakeArtifactBundles(allow_gate_response())
    registry = {"registered": {"record": {"subject_digest": "sha256:" + "2" * 64}}}

    result = validator.trust_gate_allow_latest(fake, tmp_path, registry)

    assert result["ok"] is True
    assert fake.trust_gate_calls == [
        {
            "registry_dir": tmp_path,
            "artifact_class": "aoa_skills_release_manifest",
            "subject_digest": "sha256:" + "2" * 64,
            "consumer_intent": "agent",
            "expected_source_repo": "aoa-skills",
        }
    ]

    for mutated_claim in (
        {"decision": {"model": "shape_only", "allow": True}},
        {"inspected_claims": {"registry_latest": {"selected_record_is_latest": False}}},
        {"inspected_claims": {"controls": {"required_controls_missing": ["abi_signature"]}}},
        {"inspected_claims": {"source": {"source_repo_matched": False}}},
    ):
        response = allow_gate_response()
        for key, value in mutated_claim.items():
            if key == "inspected_claims":
                response[key].update(value)
            else:
                response[key] = value
        assert validator.trust_gate_allow_latest(FakeArtifactBundles(response), tmp_path, registry)["ok"] is False


def test_release_manifest_terminal_registry_state_requires_revoked_gate_deny(tmp_path: Path) -> None:
    validator = load_validator_module()

    denied = validator.verify_terminal_registry_state(
        FakeArtifactBundles(deny_terminal_gate_response()),
        tmp_path,
        tmp_path,
    )
    assert denied["ok"] is True
    assert denied["revoked_trust_gate"]["verdict"] == "deny"

    allowed = validator.verify_terminal_registry_state(
        FakeArtifactBundles(allow_gate_response()),
        tmp_path,
        tmp_path,
    )
    assert allowed["ok"] is False
    assert allowed["revoked_trust_gate"]["verdict"] == "allow"


def test_release_manifest_materialized_subject_store_requires_trusted_source_scoped_subject(
    tmp_path: Path,
) -> None:
    validator = load_validator_module()
    fake = FakeArtifactBundles(allow_gate_response())

    result = validator.verify_materialized_subject_store(
        fake,
        MANIFEST_PATH,
        tmp_path,
        tmp_path / "registry",
        tmp_path,
    )

    assert result["ok"] is True
    assert fake.materialize_calls == [
        {
            "bundle_dir": tmp_path,
            "store_root": tmp_path / "subject-store",
            "registry_dir": tmp_path / "registry",
            "manifest_ref": MANIFEST_PATH,
            "consumer_intent": "agent",
            "expected_source_repo": "aoa-skills",
        }
    ]
    assert fake.trust_gate_calls[-1] == {
        "registry_dir": tmp_path / "registry",
        "artifact_class": "aoa_skills_release_manifest",
        "subject_digest": "sha256:" + "3" * 64,
        "consumer_intent": "agent",
        "expected_source_repo": "aoa-skills",
    }

    fake = FakeArtifactBundles({**allow_gate_response(), "verdict": "warn"})
    assert (
        validator.verify_materialized_subject_store(
            fake,
            MANIFEST_PATH,
            tmp_path,
            tmp_path / "registry",
            tmp_path,
        )["ok"]
        is False
    )
