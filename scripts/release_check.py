#!/usr/bin/env python3
"""Run the bounded release-prep validation flow for aoa-skills."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


RELEASE_CHECK_COMMAND_SEQUENCE = (
    ("python", "scripts/build_catalog.py"),
    ("python", "scripts/build_agent_skills.py", "--repo-root", "."),
    ("python", "-m", "unittest", "discover", "-s", "tests"),
    ("python", "scripts/validate_nested_agents.py"),
    ("python", "scripts/validate_skills.py"),
    ("python", "scripts/validate_agent_skills.py", "--repo-root", "."),
    ("python", "scripts/lint_trigger_evals.py", "--repo-root", "."),
    ("python", "scripts/lint_pack_profiles.py", "--repo-root", "."),
    ("python", "scripts/build_catalog.py", "--check"),
)
WORKTREE_SNAPSHOT_COMMAND = ("git", "status", "--porcelain=v1", "--untracked-files=all")
TRACKED_DIFF_SNAPSHOT_COMMAND = ("git", "diff", "--binary", "--no-ext-diff")
CACHED_DIFF_SNAPSHOT_COMMAND = ("git", "diff", "--cached", "--binary", "--no-ext-diff")
CLEAN_REPO_DIFF_COMMAND = ("git", "diff", "--exit-code")


@dataclass(frozen=True)
class RepoStateSnapshot:
    worktree_status: str
    tracked_diff: str
    cached_diff: str


def resolve_command(command: tuple[str, ...]) -> tuple[str, ...]:
    if command and command[0] == "python":
        return (sys.executable, *command[1:])
    return command


def run_command(command: tuple[str, ...], repo_root: Path) -> None:
    print(f"[run] {' '.join(command)}")
    subprocess.run(resolve_command(command), cwd=repo_root, check=True)


def capture_command_output(command: tuple[str, ...], repo_root: Path) -> str:
    result = subprocess.run(
        command,
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def capture_repo_state(repo_root: Path) -> RepoStateSnapshot:
    return RepoStateSnapshot(
        worktree_status=capture_command_output(WORKTREE_SNAPSHOT_COMMAND, repo_root),
        tracked_diff=capture_command_output(TRACKED_DIFF_SNAPSHOT_COMMAND, repo_root),
        cached_diff=capture_command_output(CACHED_DIFF_SNAPSHOT_COMMAND, repo_root),
    )


def repo_state_changed(before: RepoStateSnapshot, after: RepoStateSnapshot) -> bool:
    return before != after


def repo_started_without_tracked_diff(snapshot: RepoStateSnapshot) -> bool:
    return not snapshot.tracked_diff.strip() and not snapshot.cached_diff.strip()


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    before_state = capture_repo_state(repo_root)

    for command in RELEASE_CHECK_COMMAND_SEQUENCE:
        run_command(command, repo_root)

    after_state = capture_repo_state(repo_root)
    if repo_state_changed(before_state, after_state):
        print("[info] worktree changed during release check; rerunning once to confirm stable outputs")
        for command in RELEASE_CHECK_COMMAND_SEQUENCE:
            run_command(command, repo_root)

        stabilized_state = capture_repo_state(repo_root)
        if repo_state_changed(after_state, stabilized_state):
            print("[error] release check did not stabilize the worktree snapshot", file=sys.stderr)
            print("[after first pass]", file=sys.stderr)
            print(after_state, file=sys.stderr)
            print("[after second pass]", file=sys.stderr)
            print(stabilized_state, file=sys.stderr)
            return 1

    if repo_started_without_tracked_diff(before_state):
        run_command(CLEAN_REPO_DIFF_COMMAND, repo_root)

    print("[ok] release check completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
