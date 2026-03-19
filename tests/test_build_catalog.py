from __future__ import annotations

import contextlib
import io
import json
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

import build_catalog


PRIMARY_PUBLISHED_TECHNIQUE = {
    "id": "AOA-T-0001",
    "repo": "8Dionysus/aoa-techniques",
    "path": "techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md",
    "source_ref": "0123456789abcdef0123456789abcdef01234567",
    "use_sections": [
        "Intent",
        "When to use",
        "Inputs",
        "Outputs",
        "Core procedure",
        "Contracts",
        "Risks",
        "Validation",
    ],
}


class BuildCatalogTests(unittest.TestCase):
    def make_repo(self) -> Path:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-catalog-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        (repo_root / "skills").mkdir()
        skill_dir = repo_root / "skills" / "aoa-test-skill"
        skill_dir.mkdir()
        (skill_dir / "examples").mkdir()
        (skill_dir / "examples" / "example.md").write_text(
            "# Example\n\nSupport artifact.\n",
            encoding="utf-8",
        )
        (repo_root / "SKILL_INDEX.md").write_text(
            "# SKILL_INDEX\n\n| name | scope | status | summary |\n|---|---|---|---|\n"
            "| aoa-test-skill | core | scaffold | Test summary. |\n",
            encoding="utf-8",
        )
        (skill_dir / "SKILL.md").write_text(
            textwrap.dedent(
                """\
                ---
                name: aoa-test-skill
                scope: core
                status: scaffold
                summary: Test skill summary.
                invocation_mode: explicit-preferred
                technique_dependencies:
                  - AOA-T-0001
                ---

                # aoa-test-skill

                ## Intent

                Intent text.

                ## Trigger boundary

                Use this skill when:
                - needed

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

                ## Technique traceability

                Traceability text.

                ## Adaptation points

                - adapt
                """
            ),
            encoding="utf-8",
        )
        (skill_dir / "techniques.yaml").write_text(
            yaml.safe_dump(
                {
                    "skill_name": "aoa-test-skill",
                    "composition_mode": "bounded",
                    "techniques": [PRIMARY_PUBLISHED_TECHNIQUE],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        return repo_root

    def run_main(self, repo_root: Path, argv: list[str] | None = None) -> int:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            return build_catalog.main(argv or [], repo_root=repo_root)

    def test_write_catalogs_generates_full_and_min_projection(self) -> None:
        repo_root = self.make_repo()

        full_path, min_path = build_catalog.write_catalogs(repo_root)

        full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
        min_catalog = json.loads(min_path.read_text(encoding="utf-8"))
        self.assertEqual(1, full_catalog["catalog_version"])
        self.assertEqual(
            {
                "skill_markdown": "skills/*/SKILL.md",
                "technique_manifest": "skills/*/techniques.yaml",
            },
            full_catalog["source_of_truth"],
        )
        self.assertEqual(
            build_catalog.project_min_catalog(full_catalog),
            min_catalog,
        )
        self.assertEqual(
            "skills/aoa-test-skill/SKILL.md",
            min_catalog["skills"][0]["skill_path"],
        )
        self.assertEqual(
            "aoa-techniques",
            full_catalog["skills"][0]["technique_refs"][0]["repo"],
        )

    def test_check_mode_passes_after_write(self) -> None:
        repo_root = self.make_repo()
        build_catalog.write_catalogs(repo_root)

        self.assertEqual(0, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_catalog_is_stale(self) -> None:
        repo_root = self.make_repo()
        build_catalog.write_catalogs(repo_root)
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "Test skill summary.",
                "Changed summary.",
            ),
            encoding="utf-8",
        )

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))


if __name__ == "__main__":
    unittest.main()
