from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


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


if __name__ == "__main__":
    unittest.main()
