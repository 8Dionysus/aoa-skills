from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class SkillPromotionPressureTests(unittest.TestCase):
    def run_report(self) -> dict:
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/report_skill_promotion_pressure.py",
                "--repo-root",
                ".",
                "--workspace-root",
                "/srv/AbyssOS",
                "--skip-session-scan",
                "--skip-hooks-scan",
                "--skip-dispatch-scan",
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

    def test_report_covers_every_skill_and_sources(self) -> None:
        report = self.run_report()

        self.assertEqual(45, report["skill_count"])
        self.assertEqual(45, len(report["skills"]))
        self.assertEqual(
            "generated/public_surface.json",
            report["source_of_truth"]["status_and_governance"],
        )
        self.assertEqual(
            "generated/skill_quality_audit.json",
            report["source_of_truth"]["skill_quality"],
        )

    def test_report_routes_skill_by_available_usage_evidence(self) -> None:
        report = self.run_report()
        by_name = {entry["name"]: entry for entry in report["skills"]}
        self_repair = by_name["aoa-session-self-repair"]

        self.assertEqual(
            "canonical_monitor",
            by_name["aoa-change-protocol"]["promotion_pressure"],
        )
        if self_repair["repeated_usage_signal"]:
            self.assertEqual("promotion_review_now", self_repair["promotion_pressure"])
            self.assertGreater(self_repair["usage_evidence"]["usage_score"], 0)
        else:
            self.assertEqual("watch", self_repair["promotion_pressure"])
            self.assertEqual(0, self_repair["usage_evidence"]["usage_score"])
        self.assertIn(
            "missing_autonomy_check",
            self_repair["quality_findings"],
        )
        self.assertNotIn(
            "technique_source_drift",
            self_repair["quality_findings"],
        )

    def test_markdown_has_review_and_blocker_sections(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/report_skill_promotion_pressure.py",
                "--repo-root",
                ".",
                "--workspace-root",
                "/srv/AbyssOS",
                "--skip-session-scan",
                "--skip-hooks-scan",
                "--skip-dispatch-scan",
                "--format",
                "markdown",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(0, completed.returncode, msg=completed.stderr)
        self.assertIn("## Review Pressure", completed.stdout)
        self.assertIn("## Blockers First", completed.stdout)
        self.assertIn("`aoa-session-self-repair`", completed.stdout)


if __name__ == "__main__":
    unittest.main()
