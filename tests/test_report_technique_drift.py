from __future__ import annotations

import contextlib
import io
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
TESTS_DIR = REPO_ROOT / "tests"
for path in (SCRIPTS_DIR, TESTS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import report_technique_drift
from bridge_cli_test_support import BridgeCliTestCase, DEFAULT_REPO


class ReportTechniqueDriftTests(BridgeCliTestCase):
    def technique_ref(
        self,
        *,
        technique_id: str,
        path: str,
        source_ref: str,
        use_sections: list[str] | None = None,
    ) -> dict:
        return {
            "id": technique_id,
            "repo": DEFAULT_REPO,
            "path": path,
            "source_ref": source_ref,
            "use_sections": use_sections or ["Intent"],
        }

    def run_main(self, repo_root: Path, argv: list[str]) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            status = report_technique_drift.main(argv, repo_root=repo_root)
        return status, stdout.getvalue(), stderr.getvalue()

    def make_changed_techniques_repo(self) -> tuple[Path, str, str]:
        techniques_repo = self.make_techniques_repo()
        initial_sha = self.commit_files(
            techniques_repo,
            "Initial techniques",
            {
                "techniques/changed/TECHNIQUE.md": "# Changed\n\nold\n",
                "techniques/stable/TECHNIQUE.md": "# Stable\n\nsame\n",
            },
        )
        target_sha = self.commit_files(
            techniques_repo,
            "Update changed technique",
            {
                "techniques/changed/TECHNIQUE.md": "# Changed\n\nnew\n",
                "techniques/stable/TECHNIQUE.md": "# Stable\n\nsame\n",
            },
        )
        return techniques_repo, initial_sha, target_sha

    def test_report_handles_clean_drifted_pending_and_fail_on_drift(self) -> None:
        techniques_repo, initial_sha, target_sha = self.make_changed_techniques_repo()
        repo_root = self.make_repo_root("aoa-skills-report-")
        self.write_skill_index(repo_root, ["aoa-test-skill"])
        self.add_skill_bundle(
            repo_root,
            skill_name="aoa-test-skill",
            techniques=[
                self.technique_ref(
                    technique_id="AOA-T-0001",
                    path="techniques/changed/TECHNIQUE.md",
                    source_ref=initial_sha,
                ),
                self.technique_ref(
                    technique_id="AOA-T-0002",
                    path="techniques/stable/TECHNIQUE.md",
                    source_ref=initial_sha,
                ),
                self.technique_ref(
                    technique_id="AOA-T-PENDING-TEST",
                    path="TBD",
                    source_ref="TBD",
                ),
            ],
        )

        status, stdout, stderr = self.run_main(
            repo_root,
            [
                "--techniques-repo",
                str(techniques_repo),
                "--target-ref",
                target_sha,
                "--skill",
                "aoa-test-skill",
            ],
        )
        self.assertEqual(0, status)
        self.assertEqual("", stderr)
        self.assertIn("Skill: aoa-test-skill", stdout)
        self.assertIn("state=drifted", stdout)
        self.assertIn("state=clean", stdout)
        self.assertIn("state=pending", stdout)
        self.assertIn(f"Target ref: {target_sha}", stdout)

        status, stdout, stderr = self.run_main(
            repo_root,
            [
                "--techniques-repo",
                str(techniques_repo),
                "--target-ref",
                target_sha,
                "--skill",
                "aoa-test-skill",
                "--fail-on-drift",
            ],
        )
        self.assertEqual(1, status)
        self.assertEqual("", stderr)
        self.assertIn("state=drifted", stdout)

    def test_skill_filter_limits_report_scope(self) -> None:
        techniques_repo, initial_sha, target_sha = self.make_changed_techniques_repo()
        repo_root = self.make_repo_root("aoa-skills-report-")
        self.write_skill_index(repo_root, ["aoa-first-skill", "aoa-second-skill"])
        shared_technique = self.technique_ref(
            technique_id="AOA-T-0001",
            path="techniques/changed/TECHNIQUE.md",
            source_ref=initial_sha,
        )
        self.add_skill_bundle(
            repo_root,
            skill_name="aoa-first-skill",
            techniques=[shared_technique],
        )
        self.add_skill_bundle(
            repo_root,
            skill_name="aoa-second-skill",
            techniques=[shared_technique],
        )

        status, stdout, stderr = self.run_main(
            repo_root,
            [
                "--techniques-repo",
                str(techniques_repo),
                "--target-ref",
                target_sha,
                "--skill",
                "aoa-first-skill",
            ],
        )
        self.assertEqual(0, status)
        self.assertEqual("", stderr)
        self.assertIn("Skill: aoa-first-skill", stdout)
        self.assertNotIn("Skill: aoa-second-skill", stdout)

    def test_missing_source_ref_commit_returns_error(self) -> None:
        techniques_repo, _, target_sha = self.make_changed_techniques_repo()
        repo_root = self.make_repo_root("aoa-skills-report-")
        self.write_skill_index(repo_root, ["aoa-test-skill"])
        self.add_skill_bundle(
            repo_root,
            skill_name="aoa-test-skill",
            techniques=[
                self.technique_ref(
                    technique_id="AOA-T-0001",
                    path="techniques/changed/TECHNIQUE.md",
                    source_ref="0123456789abcdef0123456789abcdef01234567",
                )
            ],
        )

        status, stdout, stderr = self.run_main(
            repo_root,
            [
                "--techniques-repo",
                str(techniques_repo),
                "--target-ref",
                target_sha,
                "--skill",
                "aoa-test-skill",
            ],
        )
        self.assertEqual(2, status)
        self.assertEqual("", stdout)
        self.assertIn("missing git commit", stderr)

    def test_missing_path_at_target_ref_returns_error(self) -> None:
        techniques_repo, initial_sha, target_sha = self.make_changed_techniques_repo()
        repo_root = self.make_repo_root("aoa-skills-report-")
        self.write_skill_index(repo_root, ["aoa-test-skill"])
        self.add_skill_bundle(
            repo_root,
            skill_name="aoa-test-skill",
            techniques=[
                self.technique_ref(
                    technique_id="AOA-T-0001",
                    path="techniques/missing/TECHNIQUE.md",
                    source_ref=initial_sha,
                )
            ],
        )

        status, stdout, stderr = self.run_main(
            repo_root,
            [
                "--techniques-repo",
                str(techniques_repo),
                "--target-ref",
                target_sha,
                "--skill",
                "aoa-test-skill",
            ],
        )
        self.assertEqual(2, status)
        self.assertEqual("", stdout)
        self.assertIn("missing path 'techniques/missing/TECHNIQUE.md'", stderr)
