from __future__ import annotations

import contextlib
import io
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
TESTS_DIR = REPO_ROOT / "tests"
for path in (SCRIPTS_DIR, TESTS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import refresh_skill_from_techniques
from bridge_cli_test_support import BridgeCliTestCase, DEFAULT_REPO


class RefreshSkillFromTechniquesTests(BridgeCliTestCase):
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
            status = refresh_skill_from_techniques.main(argv, repo_root=repo_root)
        return status, stdout.getvalue(), stderr.getvalue()

    def make_changed_techniques_repo(self) -> tuple[Path, str, str]:
        techniques_repo = self.make_techniques_repo()
        initial_sha = self.commit_files(
            techniques_repo,
            "Initial techniques",
            {"techniques/changed/TECHNIQUE.md": "# Changed\n\nold\n"},
        )
        target_sha = self.commit_files(
            techniques_repo,
            "Refresh changed technique",
            {"techniques/changed/TECHNIQUE.md": "# Changed\n\nnew\n"},
        )
        return techniques_repo, initial_sha, target_sha

    def test_refresh_requires_explicit_skill_list(self) -> None:
        repo_root = self.make_repo_root("aoa-skills-refresh-")
        status, stdout, stderr = self.run_main(repo_root, [])
        self.assertEqual(2, status)
        self.assertEqual("", stdout)
        self.assertIn("refresh requires --skill", stderr)

    def test_preview_reports_manifest_and_skill_diffs(self) -> None:
        techniques_repo, initial_sha, target_sha = self.make_changed_techniques_repo()
        repo_root = self.make_repo_root("aoa-skills-refresh-")
        self.write_skill_index(repo_root, ["aoa-test-skill"])
        self.add_skill_bundle(
            repo_root,
            skill_name="aoa-test-skill",
            techniques=[
                self.technique_ref(
                    technique_id="AOA-T-0001",
                    path="techniques/changed/TECHNIQUE.md",
                    source_ref=initial_sha,
                )
            ],
        )

        status, stdout, stderr = self.run_main(
            repo_root,
            [
                "--skill",
                "aoa-test-skill",
                "--techniques-repo",
                str(techniques_repo),
                "--target-ref",
                target_sha,
            ],
        )
        self.assertEqual(0, status)
        self.assertEqual("", stderr)
        self.assertIn("Refresh status: needs refresh", stdout)
        self.assertIn("Upstream commits:", stdout)
        self.assertIn("--- current/skills/aoa-test-skill/techniques.yaml", stdout)
        self.assertIn("--- current/skills/aoa-test-skill/SKILL.md", stdout)
        self.assertIn(f"new_ref={target_sha}", stdout)

    def test_write_updates_only_named_skill_and_keeps_pending_refs(self) -> None:
        techniques_repo, initial_sha, target_sha = self.make_changed_techniques_repo()
        repo_root = self.make_repo_root("aoa-skills-refresh-")
        self.write_skill_index(repo_root, ["aoa-first-skill", "aoa-second-skill"])
        self.add_skill_bundle(
            repo_root,
            skill_name="aoa-first-skill",
            techniques=[
                self.technique_ref(
                    technique_id="AOA-T-0001",
                    path="techniques/changed/TECHNIQUE.md",
                    source_ref=initial_sha,
                ),
                self.technique_ref(
                    technique_id="AOA-T-PENDING-TEST",
                    path="TBD",
                    source_ref="TBD",
                ),
            ],
        )
        self.add_skill_bundle(
            repo_root,
            skill_name="aoa-second-skill",
            techniques=[
                self.technique_ref(
                    technique_id="AOA-T-0002",
                    path="techniques/changed/TECHNIQUE.md",
                    source_ref=initial_sha,
                )
            ],
        )

        status, stdout, stderr = self.run_main(
            repo_root,
            [
                "--skill",
                "aoa-first-skill",
                "--techniques-repo",
                str(techniques_repo),
                "--target-ref",
                target_sha,
                "--write",
            ],
        )
        self.assertEqual(0, status)
        self.assertEqual("", stderr)
        self.assertIn("Write result: refreshed", stdout)
        self.assertIn("Updated manifest: skills/aoa-first-skill/techniques.yaml", stdout)
        self.assertIn("Updated skill: skills/aoa-first-skill/SKILL.md", stdout)

        first_manifest = self.load_manifest(repo_root, "aoa-first-skill")
        self.assertEqual(target_sha, first_manifest["techniques"][0]["source_ref"])
        self.assertEqual("TBD", first_manifest["techniques"][1]["source_ref"])

        second_manifest = self.load_manifest(repo_root, "aoa-second-skill")
        self.assertEqual(initial_sha, second_manifest["techniques"][0]["source_ref"])

        first_skill_text = (
            repo_root / "skills" / "aoa-first-skill" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn(target_sha, first_skill_text)
        self.assertIn("AOA-T-PENDING-TEST", first_skill_text)
        self.assertIn("`TBD`", first_skill_text)

    def test_write_reports_bridge_coverage_gaps_without_inventing_sections(self) -> None:
        techniques_repo, initial_sha, target_sha = self.make_changed_techniques_repo()
        repo_root = self.make_repo_root("aoa-skills-refresh-")
        self.write_skill_index(repo_root, ["aoa-test-skill"])
        self.add_skill_bundle(
            repo_root,
            skill_name="aoa-test-skill",
            techniques=[
                self.technique_ref(
                    technique_id="AOA-T-0001",
                    path="techniques/changed/TECHNIQUE.md",
                    source_ref=initial_sha,
                    use_sections=["Intent", "Contracts"],
                )
            ],
            include_contracts_section=False,
        )

        status, stdout, stderr = self.run_main(
            repo_root,
            [
                "--skill",
                "aoa-test-skill",
                "--techniques-repo",
                str(techniques_repo),
                "--target-ref",
                target_sha,
                "--write",
            ],
        )
        self.assertEqual(0, status)
        self.assertEqual("", stderr)
        self.assertIn("Bridge coverage: gaps detected", stdout)
        self.assertIn(
            "missing `Contracts` coverage via `## Contracts`",
            stdout,
        )

        updated_skill_text = (
            repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("## Contracts", updated_skill_text)
        self.assertIn(target_sha, updated_skill_text)
