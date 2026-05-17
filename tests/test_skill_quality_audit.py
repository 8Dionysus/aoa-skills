from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class SkillQualityAuditTests(unittest.TestCase):
    def run_audit(self) -> dict:
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/audit_skill_quality.py",
                "--repo-root",
                ".",
                "--format",
                "json",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, msg=completed.stderr or completed.stdout)
        return json.loads(completed.stdout)

    def test_quality_audit_covers_every_skill(self) -> None:
        report = self.run_audit()

        self.assertEqual(45, report["skill_count"])
        self.assertEqual(45, len(report["skills"]))
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

        self.assertIn("technique_source_drift", by_name["aoa-session-self-repair"]["findings"])
        self.assertNotIn("pending_technique_lineage", by_name["aoa-summon"]["findings"])
        self.assertIn("technique_source_drift", by_name["aoa-summon"]["findings"])
        self.assertEqual("working_with_maintenance_findings", by_name["aoa-summon"]["verdict"])
        self.assertNotIn("pending_markers_in_skill_body", by_name["aoa-summon"]["findings"])
        self.assertIn("pending_technique_lineage", by_name["titan-console"]["findings"])
        self.assertNotIn("missing_autonomy_check", by_name["titan-console"]["findings"])
        self.assertEqual("healthy", by_name["aoa-change-protocol"]["verdict"])
        self.assertIn("technique_source_drift", by_name["aoa-local-stack-bringup"]["findings"])
        self.assertEqual([], by_name["atm10-change-protocol"]["findings"])
        self.assertEqual("healthy", by_name["atm10-change-protocol"]["verdict"])
        self.assertEqual([], by_name["atm10-source-of-truth-check"]["findings"])
        self.assertEqual("healthy", by_name["atm10-source-of-truth-check"]["verdict"])
        self.assertGreaterEqual(report["summary"]["technique_drift"]["state_counts"].get("drifted", 0), 1)

    def test_quality_audit_markdown_has_upgrade_targets_and_matrix(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/audit_skill_quality.py",
                "--repo-root",
                ".",
                "--format",
                "markdown",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(0, completed.returncode, msg=completed.stderr)
        self.assertIn("## Upgrade Targets", completed.stdout)
        self.assertIn("## Skill Matrix", completed.stdout)
        self.assertIn("`aoa-summon`", completed.stdout)


if __name__ == "__main__":
    unittest.main()
