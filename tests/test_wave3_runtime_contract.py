import json
import pathlib
import subprocess
import sys
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class Wave3RuntimeContractTests(unittest.TestCase):
    def test_activate_skill_includes_runtime_and_context_contracts(self):
        command = [
            sys.executable,
            "scripts/activate_skill.py",
            "--repo-root",
            ".",
            "--skill",
            "aoa-change-protocol",
            "--format",
            "json",
        ]
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["skill"]["name"], "aoa-change-protocol")
        self.assertIn("runtime_contract", payload)
        self.assertIn("context_retention", payload)
        self.assertIn("trust_policy", payload)
        self.assertEqual(payload["runtime_contract"]["name"], "aoa-change-protocol")


if __name__ == "__main__":
    unittest.main()
