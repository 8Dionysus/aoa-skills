from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class WorkspaceSkillAdoptionAuditTests(unittest.TestCase):
    def install_profile(self, profile: str, dest_root: pathlib.Path) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/install_skill_pack.py",
                "--repo-root",
                ".",
                "--profile",
                profile,
                "--dest-root",
                str(dest_root),
                "--mode",
                "copy",
                "--execute",
                "--format",
                "json",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, msg=completed.stderr or completed.stdout)

    def test_audit_discovers_workspace_root_and_repo_targets(self) -> None:
        profile = "repo-session-donor-harvest-only"
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = pathlib.Path(tmpdir)
            repo_a = workspace_root / "repo-a"
            repo_b = workspace_root / "repo-b"
            repo_a.mkdir()
            repo_b.mkdir()
            (repo_a / "AGENTS.md").write_text("# repo-a\n", encoding="utf-8")
            (repo_b / "AGENTS.md").write_text("# repo-b\n", encoding="utf-8")

            self.install_profile(profile, workspace_root / ".agents" / "skills")
            self.install_profile(profile, repo_a / ".agents" / "skills")

            completed = subprocess.run(
                [
                    sys.executable,
                    "scripts/audit_workspace_skill_adoption.py",
                    "--repo-root",
                    ".",
                    "--workspace-root",
                    str(workspace_root),
                    "--profile",
                    profile,
                    "--format",
                    "json",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, completed.returncode, msg=completed.stderr)
            report = json.loads(completed.stdout)
            by_target = {entry["target"]: entry for entry in report["targets"]}

            self.assertEqual(report["target_count"], 3)
            self.assertEqual("verified", by_target["workspace-root"]["state"])
            self.assertEqual("verified", by_target["repo-a"]["state"])
            self.assertEqual("not_installed", by_target["repo-b"]["state"])
            self.assertEqual(["aoa-session-donor-harvest"], by_target["repo-b"]["missing_skills"])

    def test_markdown_report_states_read_only_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = pathlib.Path(tmpdir)
            completed = subprocess.run(
                [
                    sys.executable,
                    "scripts/audit_workspace_skill_adoption.py",
                    "--repo-root",
                    ".",
                    "--workspace-root",
                    str(workspace_root),
                    "--profile",
                    "repo-session-donor-harvest-only",
                    "--format",
                    "markdown",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, completed.returncode, msg=completed.stderr)
            self.assertIn("This read-only report verifies", completed.stdout)
            self.assertIn("does not install, approve, or", completed.stdout)


if __name__ == "__main__":
    unittest.main()
