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


class Wave4RuntimeSeamToolchainTests(unittest.TestCase):
    def test_runtime_seam_builder_has_no_drift(self):
        completed = run_command([sys.executable, "scripts/build_runtime_seam.py", "--repo-root", ".", "--check"])
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )

    def test_discover_disclose_activate_contracts(self):
        discover = run_command(
            [
                sys.executable,
                "scripts/skill_runtime_seam.py",
                "discover",
                "--repo-root",
                ".",
                "--format",
                "json",
            ]
        )
        self.assertEqual(discover.returncode, 0, msg=discover.stderr)
        discover_payload = json.loads(discover.stdout)
        self.assertEqual(discover_payload["stage"], "discover")
        self.assertGreaterEqual(discover_payload["count"], 17)
        self.assertIn("behavioral_instructions", discover_payload)

        disclose = run_command(
            [
                sys.executable,
                "scripts/skill_runtime_seam.py",
                "disclose",
                "--repo-root",
                ".",
                "--skill-name",
                "aoa-change-protocol",
                "--format",
                "json",
            ]
        )
        self.assertEqual(disclose.returncode, 0, msg=disclose.stderr)
        disclose_payload = json.loads(disclose.stdout)
        self.assertEqual(disclose_payload["stage"], "disclose")
        self.assertEqual(disclose_payload["skill"]["name"], "aoa-change-protocol")
        self.assertIn("Trigger boundary", disclose_payload["skill"]["section_summaries"])
        self.assertNotIn("instructions_markdown", disclose_payload["skill"])

        with tempfile.TemporaryDirectory() as tmpdir:
            session_file = pathlib.Path(tmpdir) / "session.json"
            activate = run_command(
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
            self.assertEqual(activate.returncode, 0, msg=activate.stderr)
            activate_payload = json.loads(activate.stdout)
            self.assertEqual(activate_payload["stage"], "activate")
            self.assertEqual(activate_payload["skill"]["name"], "aoa-change-protocol")
            self.assertIn('<skill_content name="aoa-change-protocol">', activate_payload["structured_wrap"])
            self.assertIn("context_retention", activate_payload)
            self.assertIn("trust_policy", activate_payload)
            self.assertFalse(activate_payload["activation"]["already_active"])
            self.assertEqual(activate_payload["session"]["active_skills"][0]["name"], "aoa-change-protocol")


if __name__ == "__main__":
    unittest.main()
