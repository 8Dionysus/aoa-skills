import json
import pathlib
import subprocess
import sys
import unittest

from tests.support.cli import command_env


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class DescriptionTriggerBuilderTests(unittest.TestCase):
    def test_live_return_boundaries_are_prompt_visible(self):
        overrides = json.loads(
            (REPO_ROOT / "config" / "portable_skill_overrides.json").read_text()
        )["skills"]
        decision = overrides["aoa-decision"]["description"]
        decision_find = overrides["aoa-decision-find"]["description"]
        change = overrides["aoa-change-protocol"]["description"]

        self.assertIn("select and fully read exactly one", decision)
        self.assertIn(
            "no graph status, changed paths, target records, or owner repository packet",
            decision_find,
        )
        self.assertIn("blocked_missing_input", decision_find)
        self.assertIn("production or sensitive action is allowed", change)
        self.assertIn("project-specific manual overlay is the semantic owner", change)
        self.assertIn("names an `atm10-*` repository", change)
        self.assertIn(
            "repo-relative paths, local commands, or local approval notes", change
        )
        self.assertIn("without loading this generic skill or the explicit overlay", change)

    def test_second_live_return_source_contracts_are_explicit(self):
        decision_find = (
            REPO_ROOT / "skills/core/engineering/aoa-decision-find/SKILL.md"
        ).read_text()
        change = (
            REPO_ROOT / "skills/core/engineering/aoa-change-protocol/SKILL.md"
        ).read_text()

        self.assertIn("stop with `blocked_missing_input`", decision_find)
        self.assertIn(
            "do not relabel missing input as `deferred_owner_boundary`", decision_find
        )
        self.assertIn("names an `atm10-*` repository", change)
        self.assertIn(
            "repo-relative paths, local commands, or local approval notes", change
        )
        self.assertIn("without loading this generic skill or the explicit overlay", change)

    def test_builder_has_no_drift(self):
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/builders/build_description_trigger_evals.py",
                "--repo-root",
                ".",
                "--check",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
            env=command_env(),
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )

    def test_generated_description_eval_artifacts_exist(self):
        manifest = json.loads(
            (
                REPO_ROOT / "generated" / "description_trigger_eval_manifest.json"
            ).read_text()
        )
        signals = json.loads(
            (REPO_ROOT / "generated" / "skill_description_signals.json").read_text()
        )
        skills_ref = json.loads(
            (
                REPO_ROOT / "generated" / "skills_ref_validation_manifest.json"
            ).read_text()
        )
        source_catalog = json.loads(
            (REPO_ROOT / "generated" / "skill_catalog.min.json").read_text()
        )
        expected_skill_count = len(source_catalog["skills"])

        self.assertEqual(
            manifest["profile"], "codex-facing-wave-7-description-trigger-evals"
        )
        self.assertGreaterEqual(manifest["total_cases"], 70)
        self.assertEqual(len(signals["skills"]), expected_skill_count)
        self.assertEqual(len(skills_ref["targets"]), expected_skill_count)
        self.assertEqual(skills_ref["mode"], "export-required-conformance-lane")
        self.assertTrue(
            any("--require-skills-ref" in step for step in skills_ref["ci_steps"])
        )
        self.assertFalse(
            any("Missing validator should skip cleanly" in step for step in skills_ref["ci_steps"])
        )
        self.assertTrue(all(entry["coverage_ok"] for entry in manifest["skills"]))
        self.assertEqual(
            skills_ref["upstream"]["ref"],
            "2e8b3265237b2e5f255d6e675f89ae83be572329",
        )


if __name__ == "__main__":
    unittest.main()
