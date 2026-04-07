from __future__ import annotations

import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILD_SCRIPT_PATH = REPO_ROOT / "scripts" / "build_agent_skills.py"
PUBLISH_SCRIPT_PATH = REPO_ROOT / "scripts" / "publish_core_skill_receipts.py"
VALIDATE_SCRIPT_PATH = REPO_ROOT / "scripts" / "validate_agent_skills.py"


def load_module(name: str, path: pathlib.Path):
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


def build_core_skill_receipt(
    *,
    detail_event_kind: str,
    surface_detection_context: dict[str, object] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "kernel_id": "project-core-session-growth-v1",
        "skill_name": "aoa-session-donor-harvest",
        "application_stage": "finish",
        "detail_event_kind": detail_event_kind,
        "detail_receipt_ref": "repo:aoa-skills/tmp/HARVEST_PACKET_RECEIPT.json",
    }
    if surface_detection_context is not None:
        payload["surface_detection_context"] = surface_detection_context
    return {
        "event_kind": "core_skill_application_receipt",
        "event_id": "evt-core-kernel-001",
        "observed_at": "2026-04-06T20:20:00Z",
        "run_ref": "run-core-kernel-001",
        "session_ref": "session:test-core-kernel",
        "actor_ref": {
            "repo": "aoa-skills",
            "kind": "skill",
            "id": "aoa-session-donor-harvest",
        },
        "object_ref": {
            "repo": "aoa-skills",
            "kind": "skill",
            "id": "aoa-session-donor-harvest",
        },
        "evidence_refs": [{"kind": "receipt", "ref": "repo:aoa-skills/tmp/HARVEST_PACKET_RECEIPT.json"}],
        "payload": payload,
    }


class ProjectCoreKernelGovernanceTests(unittest.TestCase):
    def test_publish_core_skill_receipts_rejects_cross_skill_detail_kind(self) -> None:
        module = load_module("publish_core_skill_receipts", PUBLISH_SCRIPT_PATH)

        with self.assertRaises(module.ReceiptPublishError) as exc:
            module.validate_receipt(
                build_core_skill_receipt(detail_event_kind="quest_promotion_receipt"),
                location="memory",
            )

        self.assertIn("must equal 'harvest_packet_receipt'", str(exc.exception))

    def test_publish_core_skill_receipts_accepts_surface_detection_context(self) -> None:
        module = load_module("publish_core_skill_receipts", PUBLISH_SCRIPT_PATH)

        receipt = build_core_skill_receipt(
            detail_event_kind="harvest_packet_receipt",
            surface_detection_context={
                "activation_truth": "activated",
                "adjacent_owner_repos": ["aoa-playbooks", "aoa-techniques"],
                "owner_layer_ambiguity": True,
                "shortlist_confidence": "medium",
                "detail_to_closeout_ref": "closeout:item:playbook-candidate",
                "surface_detection_report_ref": "repo:aoa-sdk/.aoa/surface-detection/aoa-sdk.closeout.latest.json",
                "surface_closeout_handoff_ref": "repo:aoa-sdk/.aoa/surface-detection/aoa-sdk.closeout-handoff.latest.json",
                "family_entry_refs": [
                    "aoa-playbooks.playbook_registry.min",
                    "aoa-techniques.technique_promotion_readiness.min",
                ],
                "candidate_counts": {
                    "candidate_now": 1,
                    "candidate_later": 2,
                },
                "suggested_handoff_targets": [
                    "aoa-session-donor-harvest",
                    "aoa-quest-harvest",
                ],
                "repeated_pattern_signal": True,
                "promotion_discussion_required": True,
            },
        )

        module.validate_receipt(receipt, location="memory")

    def test_publish_core_skill_receipts_rejects_invalid_surface_detection_context(self) -> None:
        module = load_module("publish_core_skill_receipts", PUBLISH_SCRIPT_PATH)

        receipt = build_core_skill_receipt(
            detail_event_kind="harvest_packet_receipt",
            surface_detection_context={
                "activation_truth": "candidate-now",
            },
        )

        with self.assertRaises(module.ReceiptPublishError) as exc:
            module.validate_receipt(receipt, location="memory")

        self.assertIn("activation_truth", str(exc.exception))

    def test_validate_agent_skills_reports_alias_type_error_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_repo = pathlib.Path(tmpdir) / "aoa-skills"
            shutil.copytree(
                REPO_ROOT,
                temp_repo,
                ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"),
            )
            kernel_path = temp_repo / "config" / "project_core_skill_kernel.json"
            kernel_doc = json.loads(kernel_path.read_text(encoding="utf-8"))
            kernel_doc["backward_compatible_aliases"] = "repo-session-harvest-family"
            kernel_path.write_text(json.dumps(kernel_doc, indent=2) + "\n", encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATE_SCRIPT_PATH),
                    "--repo-root",
                    str(temp_repo),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        combined_output = completed.stdout + completed.stderr
        self.assertEqual(1, completed.returncode, msg=combined_output)
        self.assertIn(
            "config/project_core_skill_kernel.json backward_compatible_aliases must be a list",
            completed.stderr,
        )
        self.assertNotIn("Traceback", combined_output)

    def test_build_agent_skills_governance_uses_selected_output_root(self) -> None:
        module = load_module("build_agent_skills", BUILD_SCRIPT_PATH)
        kernel_doc = json.loads(
            (REPO_ROOT / "config" / "project_core_skill_kernel.json").read_text(encoding="utf-8")
        )
        export_map = json.loads(
            (REPO_ROOT / "generated" / "portable_export_map.json").read_text(encoding="utf-8")
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = pathlib.Path(tmpdir)
            temp_repo = temp_root / "repo"
            skills_root = temp_root / "portable-skills"
            core_ref = kernel_doc["governance_contract"]["core_receipt_schema_ref"]

            for contract in kernel_doc["skill_contracts"]:
                skill_name = contract["skill_name"]
                for ref in {core_ref, contract["detail_receipt_schema_ref"]}:
                    source_path = REPO_ROOT / "skills" / skill_name / ref
                    source_dest = temp_repo / "skills" / skill_name / ref
                    export_dest = skills_root / skill_name / ref
                    source_dest.parent.mkdir(parents=True, exist_ok=True)
                    export_dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_path, source_dest)
                    shutil.copy2(source_path, export_dest)

            governance = module.build_project_core_kernel_governance_doc(
                repo_root=temp_repo,
                skills_root=skills_root,
                kernel_doc=kernel_doc,
                export_map=export_map,
            )

        self.assertFalse((temp_repo / ".agents" / "skills").exists())
        self.assertTrue(
            all(entry["gate_passed"] for entry in governance["skills"]),
            msg=json.dumps(governance, indent=2),
        )


if __name__ == "__main__":
    unittest.main()
