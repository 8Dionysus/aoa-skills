from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import smoke_skill_pack_handoff


class SmokeSkillPackHandoffTests(unittest.TestCase):
    def run_smoke(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "scripts/smoke_skill_pack_handoff.py", *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_smoke_dir_transport_passes(self) -> None:
        completed = self.run_smoke("--repo-root", ".", "--transport", "dir", "--format", "json")
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["verified"])
        self.assertEqual("dir", payload["transport"])
        self.assertIsNotNone(payload["steps"]["inspect_dir"])
        self.assertIsNone(payload["steps"]["inspect_archive"])

    def test_smoke_zip_transport_passes(self) -> None:
        completed = self.run_smoke("--repo-root", ".", "--transport", "zip", "--format", "json")
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["verified"])
        self.assertEqual("zip", payload["transport"])
        self.assertIsNone(payload["steps"]["inspect_dir"])
        self.assertIsNotNone(payload["steps"]["inspect_archive"])

    def test_smoke_both_transport_passes(self) -> None:
        completed = self.run_smoke("--repo-root", ".", "--transport", "both", "--format", "json")
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["verified"])
        self.assertIsNotNone(payload["steps"]["inspect_dir"])
        self.assertIsNotNone(payload["steps"]["inspect_archive"])
        self.assertIsNotNone(payload["steps"]["verify_dir"])
        self.assertIsNotNone(payload["steps"]["verify_archive"])

    def test_execute_smoke_stops_on_inspect_failure(self) -> None:
        calls: list[list[str]] = []

        def fake_run_step(command: list[str], *, repo_root: pathlib.Path) -> dict[str, object]:
            calls.append(command)
            if len(calls) == 1:
                return {"command": "stage", "status": "ok", "returncode": 0, "result": {}, "stderr": None}
            return {
                "command": "inspect_dir",
                "status": "failed",
                "returncode": 1,
                "result": None,
                "stderr": "inspect failed",
            }

        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch.object(smoke_skill_pack_handoff, "run_step", side_effect=fake_run_step):
                report = smoke_skill_pack_handoff.execute_smoke(
                    repo_root=REPO_ROOT,
                    profile="repo-core-only",
                    transport="dir",
                    work_root=pathlib.Path(tmpdir),
                )

        self.assertFalse(report["verified"])
        self.assertEqual("failed", report["steps"]["inspect_dir"]["status"])
        self.assertIsNone(report["steps"]["install_dir"])
        self.assertIsNone(report["steps"]["verify_dir"])

    def test_execute_smoke_stops_on_verify_failure(self) -> None:
        statuses = iter(
            [
                {"command": "stage", "status": "ok", "returncode": 0, "result": {}, "stderr": None},
                {"command": "inspect_dir", "status": "ok", "returncode": 0, "result": {}, "stderr": None},
                {"command": "install_dir", "status": "ok", "returncode": 0, "result": {}, "stderr": None},
                {
                    "command": "verify_dir",
                    "status": "failed",
                    "returncode": 1,
                    "result": {"verified": False},
                    "stderr": "verify failed",
                },
            ]
        )

        def fake_run_step(command: list[str], *, repo_root: pathlib.Path) -> dict[str, object]:
            return next(statuses)

        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch.object(smoke_skill_pack_handoff, "run_step", side_effect=fake_run_step):
                report = smoke_skill_pack_handoff.execute_smoke(
                    repo_root=REPO_ROOT,
                    profile="repo-core-only",
                    transport="dir",
                    work_root=pathlib.Path(tmpdir),
                )

        self.assertFalse(report["verified"])
        self.assertEqual("failed", report["steps"]["verify_dir"]["status"])
        self.assertIsNone(report["steps"]["install_archive"])
        self.assertIsNone(report["steps"]["verify_archive"])


if __name__ == "__main__":
    unittest.main()
