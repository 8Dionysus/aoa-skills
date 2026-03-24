from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import release_check


class ReleaseCheckTests(unittest.TestCase):
    def test_resolve_command_uses_current_python_executable(self) -> None:
        self.assertEqual(
            (sys.executable, "scripts/build_catalog.py"),
            release_check.resolve_command(("python", "scripts/build_catalog.py")),
        )
        self.assertEqual(
            ("git", "status"),
            release_check.resolve_command(("git", "status")),
        )

    def test_repo_state_changed_compares_full_snapshot(self) -> None:
        before = release_check.RepoStateSnapshot(" M file\n", "tracked-a", "cached-a")
        same = release_check.RepoStateSnapshot(" M file\n", "tracked-a", "cached-a")
        changed = release_check.RepoStateSnapshot(" M file\n", "tracked-b", "cached-a")

        self.assertFalse(release_check.repo_state_changed(before, same))
        self.assertTrue(release_check.repo_state_changed(before, changed))

    def test_main_runs_release_commands_in_order_and_enforces_clean_diff(self) -> None:
        before = release_check.RepoStateSnapshot("", "", "")
        after = release_check.RepoStateSnapshot("", "", "")
        calls: list[tuple[str, ...]] = []

        def fake_run(command: tuple[str, ...], repo_root: Path) -> None:
            calls.append(command)

        stdout = io.StringIO()
        with (
            mock.patch.object(release_check, "capture_repo_state", side_effect=[before, after]),
            mock.patch.object(release_check, "run_command", side_effect=fake_run),
            contextlib.redirect_stdout(stdout),
        ):
            exit_code = release_check.main()

        self.assertEqual(0, exit_code)
        self.assertEqual(
            [
                *release_check.RELEASE_CHECK_COMMAND_SEQUENCE,
                release_check.CLEAN_REPO_DIFF_COMMAND,
            ],
            calls,
        )

    def test_main_reruns_once_when_worktree_changes_then_stabilizes(self) -> None:
        before = release_check.RepoStateSnapshot(" M file\n", "tracked-a", "")
        after_first_pass = release_check.RepoStateSnapshot(" M file\n", "tracked-b", "")
        after_second_pass = release_check.RepoStateSnapshot(" M file\n", "tracked-b", "")
        calls: list[tuple[str, ...]] = []

        def fake_run(command: tuple[str, ...], repo_root: Path) -> None:
            calls.append(command)

        stdout = io.StringIO()
        with (
            mock.patch.object(
                release_check,
                "capture_repo_state",
                side_effect=[before, after_first_pass, after_second_pass],
            ),
            mock.patch.object(release_check, "run_command", side_effect=fake_run),
            contextlib.redirect_stdout(stdout),
        ):
            exit_code = release_check.main()

        self.assertEqual(0, exit_code)
        self.assertEqual(
            [
                *release_check.RELEASE_CHECK_COMMAND_SEQUENCE,
                *release_check.RELEASE_CHECK_COMMAND_SEQUENCE,
            ],
            calls,
        )

    def test_main_fails_when_second_pass_does_not_stabilize(self) -> None:
        before = release_check.RepoStateSnapshot(" M file\n", "tracked-a", "")
        after_first_pass = release_check.RepoStateSnapshot(" M file\n", "tracked-b", "")
        after_second_pass = release_check.RepoStateSnapshot(" M file\n", "tracked-c", "")
        stdout = io.StringIO()
        stderr = io.StringIO()

        with (
            mock.patch.object(
                release_check,
                "capture_repo_state",
                side_effect=[before, after_first_pass, after_second_pass],
            ),
            mock.patch.object(release_check, "run_command"),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            exit_code = release_check.main()

        self.assertEqual(1, exit_code)
        self.assertIn("release check did not stabilize the worktree snapshot", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
