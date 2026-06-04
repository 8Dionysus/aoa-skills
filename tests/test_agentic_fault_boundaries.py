from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.support.cli import run_python
from tests.support.generated_fixtures import REPO_ROOT, copy_repo_paths

import sys


SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lanes import validation_lanes
from validation.validators import tiny_router_surface, trigger_eval_surface


DESCRIPTION_TRIGGER_FILES = [
    "generated/skill_description_signals.json",
    "generated/description_trigger_eval_manifest.json",
    "generated/description_trigger_eval_cases.jsonl",
    "config/description_trigger_eval_policy.json",
    "config/skill_policy_matrix.json",
]


class AgenticFaultBoundariesTests(unittest.TestCase):
    def test_validation_lane_loader_rejects_malformed_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "validation_lanes.json"
            manifest_path.write_text("{not-json", encoding="utf-8")
            with mock.patch.object(
                validation_lanes, "VALIDATION_LANES_PATH", manifest_path
            ):
                with self.assertRaises(json.JSONDecodeError):
                    validation_lanes._load_manifest()

    def test_tiny_router_validator_reports_missing_generated_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            (repo_root / "config").mkdir()
            (repo_root / "config" / "tiny_router_skill_bands.json").write_text(
                "{}\n",
                encoding="utf-8",
            )
            errors: list[str] = []

            self.assertFalse(
                tiny_router_surface.validate_required_files(repo_root, errors)
            )
            self.assertIn(
                "Missing wave-9 generated file: generated/tiny_router_skill_signals.json",
                errors,
            )

    def test_description_trigger_validator_reports_stale_manifest_totals(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            copy_repo_paths(repo_root, DESCRIPTION_TRIGGER_FILES)
            manifest_path = (
                repo_root / "generated" / "description_trigger_eval_manifest.json"
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["case_class_totals"] = {}
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
            )

            errors, _case_count, _skill_count = (
                trigger_eval_surface.lint_description_trigger_evals(repo_root)
            )

        self.assertIn(
            "description_trigger_eval_manifest.json case_class_totals drift", errors
        )

    def test_external_skills_ref_missing_binary_is_soft_skip(self) -> None:
        env = os.environ.copy()
        env["PATH"] = ""
        env.pop("SKILLS_REF_BIN", None)
        completed = run_python(
            "scripts/validation/run_skills_ref_validation.py",
            "--repo-root",
            ".",
            "--format",
            "json",
            env=env,
        )

        payload = json.loads(completed.stdout)
        self.assertEqual(0, completed.returncode, msg=completed.stderr)
        self.assertEqual("skipped", payload["status"])

    def test_export_builder_refuses_nonempty_external_output_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir) / "external-output"
            output_root.mkdir()
            (output_root / "keep.txt").write_text("do not delete\n", encoding="utf-8")

            completed = run_python(
                "scripts/export/build_agent_skills.py",
                "--repo-root",
                ".",
                "--output-root",
                str(output_root),
            )
            kept_file_exists = (output_root / "keep.txt").exists()

        self.assertNotEqual(0, completed.returncode)
        self.assertIn("refusing to delete existing external contents", completed.stderr)
        self.assertTrue(kept_file_exists)


if __name__ == "__main__":
    unittest.main()
