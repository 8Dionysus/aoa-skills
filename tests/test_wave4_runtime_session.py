import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class Wave4RuntimeSessionTests(unittest.TestCase):
    def test_session_deduplication_and_compaction(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            session_file = pathlib.Path(tmpdir) / "session.json"

            first = run_command(
                [
                    sys.executable,
                    "scripts/skill_runtime_seam.py",
                    "activate",
                    "--repo-root",
                    ".",
                    "--skill",
                    "aoa-change-protocol",
                    "--session-file",
                    str(session_file),
                    "--explicit-handle",
                    "$aoa-change-protocol",
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(first.returncode, 0, msg=first.stderr)
            first_payload = json.loads(first.stdout)
            self.assertFalse(first_payload["activation"]["already_active"])

            second = run_command(
                [
                    sys.executable,
                    "scripts/skill_runtime_seam.py",
                    "activate",
                    "--repo-root",
                    ".",
                    "--skill",
                    "aoa-change-protocol",
                    "--session-file",
                    str(session_file),
                    "--explicit-handle",
                    "$aoa-change-protocol",
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(second.returncode, 0, msg=second.stderr)
            second_payload = json.loads(second.stdout)
            self.assertTrue(second_payload["activation"]["already_active"])

            status = run_command(
                [
                    sys.executable,
                    "scripts/skill_runtime_seam.py",
                    "status",
                    "--session-file",
                    str(session_file),
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(status.returncode, 0, msg=status.stderr)
            status_payload = json.loads(status.stdout)
            self.assertEqual(len(status_payload["session"]["active_skills"]), 1)
            self.assertEqual(status_payload["session"]["active_skills"][0]["activation_count"], 2)

            compact = run_command(
                [
                    sys.executable,
                    "scripts/skill_runtime_seam.py",
                    "compact",
                    "--session-file",
                    str(session_file),
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(compact.returncode, 0, msg=compact.stderr)
            compact_payload = json.loads(compact.stdout)
            self.assertEqual(compact_payload["stage"], "compact")
            self.assertEqual(compact_payload["active_skill_packets"][0]["name"], "aoa-change-protocol")
            self.assertTrue(compact_payload["active_skill_packets"][0]["protected_from_compaction"])
            self.assertGreaterEqual(len(compact_payload["active_skill_packets"][0]["must_keep"]), 1)

            deactivate = run_command(
                [
                    sys.executable,
                    "scripts/skill_runtime_seam.py",
                    "deactivate",
                    "--session-file",
                    str(session_file),
                    "--skill",
                    "aoa-change-protocol",
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(deactivate.returncode, 0, msg=deactivate.stderr)
            deactivate_payload = json.loads(deactivate.stdout)
            self.assertTrue(deactivate_payload["removed"])
            self.assertEqual(len(deactivate_payload["session"]["active_skills"]), 0)


if __name__ == "__main__":
    unittest.main()
