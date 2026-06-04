from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

from tests.support.cli import command_env
from tests.support.source_catalog import source_skill_count


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class SkillQualityAuditTests(unittest.TestCase):
    def run_audit(self) -> dict:
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/audit/audit_skill_quality.py",
                "--repo-root",
                ".",
                "--format",
                "json",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
            env=command_env(),
        )
        self.assertEqual(
            0, completed.returncode, msg=completed.stderr or completed.stdout
        )
        return json.loads(completed.stdout)

    def test_quality_audit_covers_every_skill(self) -> None:
        report = self.run_audit()
        expected_skill_count = source_skill_count(REPO_ROOT)

        self.assertEqual(expected_skill_count, report["skill_count"])
        self.assertEqual(expected_skill_count, len(report["skills"]))
        self.assertEqual(
            {
                "generated/governance_backlog.json",
                "generated/agent_skill_catalog.json",
                "generated/local_adapter_manifest.json",
                "generated/portable_export_map.json",
                "generated/public_surface.json",
                "generated/runtime_discovery_index.json",
                "generated/skill_bundle_index.json",
                "generated/skill_evaluation_matrix.json",
                "config/skill_policy_matrix.json",
                "skills/**/SKILL.md",
                "skills/**/techniques.yaml",
                "tests/fixtures/skill_evaluation_cases.yaml",
                "local aoa-techniques drift check",
            },
            set(report["source_of_truth"]),
        )

    def test_quality_audit_exposes_known_real_gaps(self) -> None:
        report = self.run_audit()
        by_name = {entry["name"]: entry for entry in report["skills"]}

        self.assertEqual([], by_name["aoa-session-self-repair"]["findings"])
        self.assertEqual("healthy", by_name["aoa-session-self-repair"]["verdict"])
        self.assertNotIn("pending_technique_lineage", by_name["aoa-summon"]["findings"])
        self.assertEqual([], by_name["aoa-summon"]["findings"])
        self.assertEqual("healthy", by_name["aoa-summon"]["verdict"])
        self.assertNotIn(
            "pending_markers_in_skill_body", by_name["aoa-summon"]["findings"]
        )
        self.assertEqual([], by_name["titan-console"]["findings"])
        self.assertEqual("published", by_name["titan-console"]["lineage_state"])
        self.assertNotIn("missing_autonomy_check", by_name["titan-console"]["findings"])
        self.assertEqual("healthy", by_name["aoa-change-protocol"]["verdict"])
        self.assertEqual([], by_name["aoa-local-stack-bringup"]["findings"])
        self.assertEqual("healthy", by_name["aoa-local-stack-bringup"]["verdict"])
        self.assertEqual([], by_name["atm10-change-protocol"]["findings"])
        self.assertEqual("healthy", by_name["atm10-change-protocol"]["verdict"])
        self.assertEqual([], by_name["atm10-source-of-truth-check"]["findings"])
        self.assertEqual("healthy", by_name["atm10-source-of-truth-check"]["verdict"])
        self.assertNotIn(
            "drifted", report["summary"]["technique_drift"]["state_counts"]
        )
        self.assertEqual(
            0,
            report["summary"]["technique_drift"]["state_counts"].get("pending", 0),
        )

    def test_quality_audit_keeps_stable_drift_summary_when_techniques_repo_is_missing(
        self,
    ) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/audit/audit_skill_quality.py",
                "--repo-root",
                ".",
                "--techniques-repo",
                str(REPO_ROOT / ".missing-aoa-techniques-for-test"),
                "--format",
                "json",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
            env=command_env(),
        )

        self.assertEqual(
            0, completed.returncode, msg=completed.stderr or completed.stdout
        )
        drift_summary = json.loads(completed.stdout)["summary"]["technique_drift"]
        self.assertFalse(drift_summary["available"])
        self.assertEqual({}, drift_summary["state_counts"])

    def test_quality_audit_markdown_has_upgrade_targets_and_matrix(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/audit/audit_skill_quality.py",
                "--repo-root",
                ".",
                "--format",
                "markdown",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
            env=command_env(),
        )

        self.assertEqual(0, completed.returncode, msg=completed.stderr)
        self.assertIn("## Upgrade Targets", completed.stdout)
        self.assertIn("## Skill Matrix", completed.stdout)
        self.assertIn("`aoa-summon`", completed.stdout)


if __name__ == "__main__":
    unittest.main()
