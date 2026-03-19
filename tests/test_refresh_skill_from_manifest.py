from __future__ import annotations

import contextlib
import io
import shutil
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import refresh_skill_from_manifest


PUBLISHED_TECHNIQUE = {
    "id": "AOA-T-0001",
    "repo": "8Dionysus/aoa-techniques",
    "path": "techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md",
    "source_ref": "0123456789abcdef0123456789abcdef01234567",
    "use_sections": ["Intent", "Validation"],
}


class RefreshSkillFromManifestTests(unittest.TestCase):
    def make_repo(self) -> Path:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-refresh-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        skills_dir = repo_root / "skills"
        skills_dir.mkdir()

        skill_dir = skills_dir / "aoa-test-skill"
        skill_dir.mkdir()

        skill_md = textwrap.dedent(
            """\
            ---
            name: aoa-test-skill
            scope: core
            status: scaffold
            summary: Test skill summary.
            invocation_mode: explicit-preferred
            technique_dependencies: []
            ---

            # aoa-test-skill

            ## Intent

            Intent text.

            ## Trigger boundary

            Use this skill when:
            - needed

            Do not use this skill when:
            - not needed

            ## Inputs

            - input

            ## Outputs

            - output

            ## Procedure

            1. step

            ## Contracts

            - contract

            ## Risks and anti-patterns

            - risk

            ## Verification

            - verify

            ## Future traceability

            Traceability will be added later.

            ## Adaptation points

            - adapt
            """
        )
        (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

        manifest = {
            "skill_name": "aoa-test-skill",
            "composition_mode": "bounded",
            "techniques": [PUBLISHED_TECHNIQUE],
        }
        (skill_dir / "techniques.yaml").write_text(
            yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
        )
        return repo_root

    def run_main(self, repo_root: Path, argv: list[str] | None = None) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            return (
                refresh_skill_from_manifest.main(argv or [], repo_root=repo_root),
                stdout.getvalue(),
                stderr.getvalue(),
            )

    def test_dry_run_reports_diff_for_unaligned_skill(self) -> None:
        repo_root = self.make_repo()
        status, stdout, stderr = self.run_main(repo_root)
        self.assertEqual(0, status)
        self.assertEqual("", stderr)
        self.assertIn("Skill: aoa-test-skill", stdout)
        self.assertIn("Status: needs refresh", stdout)
        self.assertIn("-## Future traceability", stdout)
        self.assertIn("+## Technique traceability", stdout)
        self.assertIn("+  - AOA-T-0001", stdout)

    def test_aligned_skill_reports_already_aligned(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        proposed = refresh_skill_from_manifest.build_refresh_result(
            repo_root, "aoa-test-skill"
        )
        current_text = proposed.diff.splitlines()
        self.assertTrue(current_text)

        _, frontmatter_lines, body = refresh_skill_from_manifest.parse_skill_document(
            skill_md_path
        )
        manifest = yaml.safe_load(
            (repo_root / "skills" / "aoa-test-skill" / "techniques.yaml").read_text(
                encoding="utf-8"
            )
        )
        frontmatter_lines = refresh_skill_from_manifest.replace_technique_dependencies(
            frontmatter_lines, [PUBLISHED_TECHNIQUE["id"]]
        )
        body = refresh_skill_from_manifest.replace_traceability_section(
            body, manifest["techniques"]
        )
        skill_md_path.write_text(
            refresh_skill_from_manifest.render_skill_document(frontmatter_lines, body),
            encoding="utf-8",
        )

        status, stdout, stderr = self.run_main(repo_root)
        self.assertEqual(0, status)
        self.assertEqual("", stderr)
        self.assertIn("Status: already aligned", stdout)

    def test_write_flag_returns_error_and_does_not_mutate(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        original = skill_md_path.read_text(encoding="utf-8")

        status, stdout, stderr = self.run_main(repo_root, ["--write"])
        self.assertEqual(2, status)
        self.assertEqual("", stdout)
        self.assertIn("Write mode is intentionally unavailable", stderr)
        self.assertEqual(original, skill_md_path.read_text(encoding="utf-8"))
