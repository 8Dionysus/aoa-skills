import json
import pathlib
import subprocess
import sys
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class Wave7DescriptionTriggerBuilderTests(unittest.TestCase):
    def test_builder_has_no_drift(self):
        completed = subprocess.run(
            [sys.executable, "scripts/build_description_trigger_evals.py", "--repo-root", ".", "--check"],
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

    def test_generated_description_eval_artifacts_exist(self):
        manifest = json.loads((REPO_ROOT / "generated" / "description_trigger_eval_manifest.json").read_text())
        signals = json.loads((REPO_ROOT / "generated" / "skill_description_signals.json").read_text())
        skills_ref = json.loads((REPO_ROOT / "generated" / "skills_ref_validation_manifest.json").read_text())

        self.assertEqual(manifest["profile"], "codex-facing-wave-7-description-trigger-evals")
        self.assertGreaterEqual(manifest["total_cases"], 70)
        self.assertEqual(len(signals["skills"]), 19)
        self.assertEqual(len(skills_ref["targets"]), 19)
        self.assertTrue(all(entry["coverage_ok"] for entry in manifest["skills"]))


if __name__ == "__main__":
    unittest.main()
