from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_support_resources


def run_json(*args: str) -> dict:
    completed = subprocess.run(
        [sys.executable, *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(completed.stdout)


class SupportBundleScriptTests(unittest.TestCase):
    def make_support_repo_copy(self) -> Path:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-support-validate-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        for rel_path in validate_support_resources.REQUIRED_GENERATED_FILES:
            target_path = repo_root / rel_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO_ROOT / rel_path, target_path)
        for skill in validate_support_resources.TARGETED_SKILLS:
            shutil.copytree(
                REPO_ROOT / "skills" / skill,
                repo_root / "skills" / skill,
            )
            shutil.copytree(
                REPO_ROOT / ".agents" / "skills" / skill,
                repo_root / ".agents" / "skills" / skill,
            )
        return repo_root

    def test_dry_run_contract(self) -> None:
        payload = REPO_ROOT / "skills/aoa-dry-run-first/assets/dry_run_contract.template.json"
        result = run_json("skills/aoa-dry-run-first/scripts/dry_run_contract.py", str(payload))
        self.assertEqual(result["skill"], "aoa-dry-run-first")
        self.assertEqual(result["workflow_state"], "ready_for_confirmation")
        self.assertEqual(result["preview_verdict"], "ok")

    def test_preview_gap_check(self) -> None:
        payload = REPO_ROOT / "skills/aoa-dry-run-first/assets/dry_run_contract.template.json"
        result = run_json("skills/aoa-dry-run-first/scripts/preview_gap_check.py", str(payload))
        self.assertEqual(result["status"], "ok")
        self.assertFalse(result["gaps"])

    def test_infra_change_contract(self) -> None:
        payload = REPO_ROOT / "skills/aoa-safe-infra-change/assets/infra_change_contract.template.json"
        result = run_json("skills/aoa-safe-infra-change/scripts/infra_change_contract.py", str(payload))
        self.assertEqual(result["skill"], "aoa-safe-infra-change")
        self.assertIn(result["risk_band"], {"medium", "high"})
        self.assertTrue(result["rollback_ready"])

    def test_risk_surface_scan(self) -> None:
        payload = REPO_ROOT / "skills/aoa-safe-infra-change/assets/infra_change_contract.template.json"
        result = run_json("skills/aoa-safe-infra-change/scripts/risk_surface_scan.py", str(payload))
        self.assertEqual(result["status"], "ok")
        self.assertGreaterEqual(len(result["detected"]), 1)

    def test_bringup_contract(self) -> None:
        payload = REPO_ROOT / "skills/aoa-local-stack-bringup/assets/local_stack_bringup.template.json"
        result = run_json("skills/aoa-local-stack-bringup/scripts/bringup_contract.py", str(payload))
        self.assertEqual(result["skill"], "aoa-local-stack-bringup")
        self.assertEqual(result["verdict"], "ready_for_confirmation")
        self.assertEqual(result["blocker_count"], 0)

    def test_readiness_summary(self) -> None:
        payload = REPO_ROOT / "skills/aoa-local-stack-bringup/assets/local_stack_bringup.template.json"
        result = run_json("skills/aoa-local-stack-bringup/scripts/readiness_summary.py", str(payload))
        self.assertEqual(result["overall"], "warn")
        self.assertEqual(result["counts"]["warn"], 1)

    def test_bringup_contract_treats_unknown_readiness_severity_as_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            payload_path = Path(tmpdir) / "bringup.json"
            payload_path.write_text(
                json.dumps(
                    {
                        "runtime_name": "compose",
                        "selector": "dev",
                        "rendered_services": ["api"],
                        "readiness_items": [
                            {"severity": "error", "label": "runtime probe failed"},
                        ],
                        "launch_command": "docker compose up -d",
                        "stop_command": "docker compose down",
                        "confirmation_required": True,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            result = run_json(
                "skills/aoa-local-stack-bringup/scripts/bringup_contract.py",
                str(payload_path),
            )
            self.assertEqual("hold", result["verdict"])
            self.assertEqual(1, result["blocker_count"])
            self.assertTrue(
                any("Unknown readiness severity" in warning for warning in result["warnings"])
            )

    def test_dry_run_contract_rejects_non_object_preview_step_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            payload_path = Path(tmpdir) / "dry-run.json"
            payload_path.write_text(
                json.dumps(
                    {
                        "requested_action": "Switch current symlink",
                        "preview_steps": ["readlink current"],
                        "apply_step": {
                            "label": "switch symlink",
                            "command": "ln -sfn previous current",
                            "touches_state": True,
                        },
                        "touched_surfaces": ["application symlink"],
                        "limitations": ["preview does not prove runtime health"],
                        "confirmation_required": True,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    "skills/aoa-dry-run-first/scripts/dry_run_contract.py",
                    str(payload_path),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, completed.returncode, msg=completed.stderr)
            result = json.loads(completed.stdout)
            self.assertIn("preview step 1 must be an object.", result["errors"])
            self.assertEqual("", completed.stderr)

    def test_validate_support_resources_rejects_manifest_digest_drift(self) -> None:
        repo_root = self.make_support_repo_copy()
        manifest_path = repo_root / "generated" / "deterministic_resource_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["skills"][0]["legacy_dirs"]["agents"][0]["sha256"] = "0" * 64
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

        result = validate_support_resources.validate(repo_root, check_portable=True)

        self.assertEqual("fail", result["status"])
        self.assertTrue(
            any("deterministic_resource_manifest legacy agents/ digest mismatch" in error for error in result["errors"])
        )


if __name__ == "__main__":
    unittest.main()
