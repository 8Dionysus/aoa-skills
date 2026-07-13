from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

from tests.support.cli import command_env
from tests.support.source_catalog import source_skill_count


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from reports import report_skill_promotion_pressure


class SkillPromotionPressureTests(unittest.TestCase):
    def run_report(self) -> dict:
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/reports/report_skill_promotion_pressure.py",
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
            env=command_env(),
        )
        self.assertEqual(
            0, completed.returncode, msg=completed.stderr or completed.stdout
        )
        return json.loads(completed.stdout)

    def test_report_covers_every_skill_and_sources(self) -> None:
        report = self.run_report()
        expected_skill_count = source_skill_count(REPO_ROOT)

        self.assertEqual(expected_skill_count, report["skill_count"])
        self.assertEqual(expected_skill_count, len(report["skills"]))
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
            self.assertEqual(
                "revisit_stay_evaluated", self_repair["promotion_pressure"]
            )
            self.assertGreater(self_repair["usage_evidence"]["usage_score"], 0)
        else:
            self.assertEqual("candidate_ready_watch", self_repair["promotion_pressure"])
            self.assertLess(self_repair["usage_evidence"]["usage_score"], 5)
        self.assertNotEqual("blocked", self_repair["quality_verdict"])
        self.assertNotEqual("blockers_first", self_repair["promotion_pressure"])

    def test_technique_drift_is_maintenance_not_a_hard_promotion_blocker(self) -> None:
        pressure, reason = report_skill_promotion_pressure.pressure_classification(
            status="evaluated",
            scope="core",
            quality_verdict="working_with_maintenance_findings",
            quality_findings=["technique_source_drift"],
            default_reference_readiness="ready",
            governance_decision="stay_evaluated",
            repeated_usage=True,
        )

        self.assertEqual("revisit_stay_evaluated", pressure)
        self.assertIn("revisiting", reason)

    def test_workspace_root_drives_default_hook_and_dispatch_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = pathlib.Path(temp_dir)
            hooks_root = workspace_root / ".codex" / "generated" / "codex" / "hooks"
            dispatch_root = workspace_root / "aoa-sdk" / ".aoa" / "skill-dispatch"
            hooks_root.mkdir(parents=True)
            dispatch_root.mkdir(parents=True)
            (hooks_root / "hook.json").write_text(
                json.dumps({"event": {"prompt": "aoa-session-self-repair"}}),
                encoding="utf-8",
            )
            (dispatch_root / "dispatch.json").write_text(
                json.dumps(
                    {
                        "report": {
                            "suggest_next": [{"skill_name": "aoa-session-self-repair"}]
                        }
                    }
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    "scripts/reports/report_skill_promotion_pressure.py",
                    "--repo-root",
                    ".",
                    "--workspace-root",
                    str(workspace_root),
                    "--skip-session-scan",
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
        report = json.loads(completed.stdout)
        self.assertEqual(1, report["scan_summary"]["hook_files_scanned"])
        self.assertEqual(1, report["scan_summary"]["dispatch_files_scanned"])
        by_name = {entry["name"]: entry for entry in report["skills"]}
        self.assertEqual(
            1,
            by_name["aoa-session-self-repair"]["usage_evidence"][
                "hook_prompt_mention_count"
            ],
        )
        self.assertEqual(
            1,
            by_name["aoa-session-self-repair"]["usage_evidence"][
                "dispatch_event_count"
            ],
        )

    def test_markdown_has_review_and_blocker_sections(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/reports/report_skill_promotion_pressure.py",
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
            env=command_env(),
        )

        self.assertEqual(0, completed.returncode, msg=completed.stderr)
        self.assertIn("## Review Pressure", completed.stdout)
        self.assertIn("## Blockers First", completed.stdout)
        self.assertIn("`aoa-session-self-repair`", completed.stdout)


if __name__ == "__main__":
    unittest.main()
