from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import ci_gate


class CiGateTests(unittest.TestCase):
    def test_source_fast_runs_no_generated_or_release_commands(self) -> None:
        calls: list[tuple[str, ...]] = []

        def fake_run(command: tuple[str, ...], repo_root: Path = ci_gate.REPO_ROOT) -> None:
            calls.append(command)

        with mock.patch.object(ci_gate, "run_command", side_effect=fake_run):
            ci_gate.run_source_fast()

        self.assertEqual(
            [
                ("python", "scripts/validation/validate_agents_design.py"),
                ("python", "scripts/validation/validate_nested_agents.py"),
                (
                    "python",
                    "scripts/validation/validate_skills.py",
                    "--skip-generated",
                    "--fail-on-review-truth-sync",
                ),
            ],
            calls,
        )

    def test_generated_mode_scopes_catalog_group(self) -> None:
        calls: list[tuple[str, ...]] = []

        def fake_run(command: tuple[str, ...], repo_root: Path = ci_gate.REPO_ROOT) -> None:
            calls.append(command)

        with mock.patch.object(ci_gate, "run_command", side_effect=fake_run):
            ci_gate.run_generated("reader")

        self.assertEqual(
            [("python", "scripts/builders/build_catalog.py", "--check", "--group", "reader")],
            calls,
        )

    def test_generated_governance_checks_decision_indexes(self) -> None:
        calls: list[tuple[str, ...]] = []

        def fake_run(command: tuple[str, ...], repo_root: Path = ci_gate.REPO_ROOT) -> None:
            calls.append(command)

        with mock.patch.object(ci_gate, "run_command", side_effect=fake_run):
            ci_gate.run_generated("governance")

        self.assertIn(("python", "scripts/decisions/generate_decision_indexes.py", "--check"), calls)

    def test_generated_export_group_runs_export_generated_checks(self) -> None:
        calls: list[tuple[str, ...]] = []

        def fake_run(command: tuple[str, ...], repo_root: Path = ci_gate.REPO_ROOT) -> None:
            calls.append(command)

        with mock.patch.object(ci_gate, "run_command", side_effect=fake_run):
            ci_gate.run_generated("export")

        self.assertEqual(("python", "scripts/export/build_agent_skills.py", "--repo-root", "."), calls[0])
        self.assertIn(("python", "scripts/validation/validate_agent_skills.py", "--repo-root", "."), calls)
        self.assertEqual(
            ("git", "diff", "--exit-code", "--", *ci_gate.EXPORT_GENERATED_DRIFT_PATHS),
            calls[-1],
        )
        self.assertNotIn(
            ("python", "scripts/runtime/build_runtime_seam.py", "--repo-root", ".", "--check"),
            calls,
        )

    def test_generated_runtime_group_runs_runtime_generated_checks(self) -> None:
        calls: list[tuple[str, ...]] = []

        def fake_run(command: tuple[str, ...], repo_root: Path = ci_gate.REPO_ROOT) -> None:
            calls.append(command)

        with mock.patch.object(ci_gate, "run_command", side_effect=fake_run):
            ci_gate.run_generated("runtime")

        self.assertEqual(
            [
                ("python", "scripts/runtime/build_runtime_seam.py", "--repo-root", ".", "--check"),
                ("python", "scripts/runtime/build_runtime_guardrails.py", "--repo-root", ".", "--check"),
                ("git", "diff", "--exit-code", "--", *ci_gate.RUNTIME_GENERATED_DRIFT_PATHS),
            ],
            calls,
        )

    def test_generated_all_includes_export_runtime_and_decision_indexes(self) -> None:
        calls: list[tuple[str, ...]] = []

        def fake_run(command: tuple[str, ...], repo_root: Path = ci_gate.REPO_ROOT) -> None:
            calls.append(command)

        with mock.patch.object(ci_gate, "run_command", side_effect=fake_run):
            ci_gate.run_generated("all")

        self.assertIn(("python", "scripts/builders/build_catalog.py", "--check", "--group", "all"), calls)
        self.assertIn(("git", "diff", "--exit-code", "--", *ci_gate.EXPORT_GENERATED_DRIFT_PATHS), calls)
        self.assertIn(("git", "diff", "--exit-code", "--", *ci_gate.RUNTIME_GENERATED_DRIFT_PATHS), calls)
        self.assertEqual(("python", "scripts/decisions/generate_decision_indexes.py", "--check"), calls[-1])

    def test_export_changed_only_skips_non_export_paths(self) -> None:
        with (
            mock.patch.object(ci_gate, "changed_files", return_value=["skills/core/foo/SKILL.md"]),
            mock.patch.object(ci_gate, "run_command") as run_command,
        ):
            ci_gate.run_export(changed_only=True, base_ref="abc123")

        run_command.assert_not_called()

    def test_export_changed_only_runs_for_export_paths(self) -> None:
        calls: list[tuple[str, ...]] = []

        def fake_run(command: tuple[str, ...], repo_root: Path = ci_gate.REPO_ROOT) -> None:
            calls.append(command)

        with (
            mock.patch.object(ci_gate, "changed_files", return_value=["generated/release_manifest.json"]),
            mock.patch.object(ci_gate, "run_command", side_effect=fake_run),
        ):
            ci_gate.run_export(changed_only=True, base_ref="abc123")

        self.assertEqual(("python", "scripts/builders/build_catalog.py", "--group", "all"), calls[0])
        self.assertEqual(("git", "diff", "--exit-code", "--", *ci_gate.EXPORT_DRIFT_PATHS), calls[-1])

    def test_export_changed_only_runs_for_export_gate_logic(self) -> None:
        for path in (
            ".github/workflows/codex-portable-export.yml",
            "config/validation_lanes.json",
            "requirements-dev.txt",
            "scripts/lanes/ci_gate.py",
            "scripts/lanes/validation_lanes.py",
            "scripts/builders/build_catalog.py",
            "scripts/builders/build_trigger_eval_cases.py",
            "scripts/export/release_manifest_contract.py",
        ):
            with self.subTest(path=path):
                self.assertTrue(ci_gate.export_relevant([path]))

    def test_release_mode_uses_packaging_smoke_release_check(self) -> None:
        with mock.patch.object(ci_gate, "run_command") as run_command:
            ci_gate.run_release()

        self.assertEqual(
            [
                ("python", "scripts/validation/validate_agents_design.py"),
                ("python", "scripts/validation/validate_nested_agents.py"),
                (
                    "python",
                    "scripts/validation/validate_skills.py",
                    "--skip-generated",
                    "--fail-on-review-truth-sync",
                ),
                ("python", "scripts/lanes/release_check.py", "--include-packaging-smoke"),
            ],
            [call.args[0] for call in run_command.call_args_list],
        )


if __name__ == "__main__":
    unittest.main()
