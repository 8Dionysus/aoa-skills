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

    def test_write_capsules_generates_runtime_cards(self) -> None:
        repo_root = self.make_repo()

        capsule_path = build_catalog.write_capsules(repo_root)

        capsules = json.loads(capsule_path.read_text(encoding="utf-8"))
        self.assertEqual(1, capsules["capsule_version"])
        self.assertEqual(
            {
                "skill_markdown": "skills/*/SKILL.md",
                "frontmatter_fields": [
                    "name",
                    "scope",
                    "status",
                    "summary",
                    "invocation_mode",
                    "technique_dependencies",
                ],
                "sections": [
                    "Intent",
                    "Trigger boundary",
                    "Inputs",
                    "Outputs",
                    "Procedure",
                    "Risks and anti-patterns",
                    "Verification",
                ],
            },
            capsules["source_of_truth"],
        )
        self.assertEqual(
            {
                "name": "aoa-test-skill",
                "scope": "core",
                "status": "scaffold",
                "summary": "Test skill summary.",
                "trigger_boundary_short": "Use when needed.",
                "inputs_short": "Needs: input.",
                "outputs_short": "Produces: output.",
                "workflow_short": "Purpose: Intent text. Flow: step.",
                "main_anti_patterns_short": "Avoid: risk.",
                "verification_short": "Checks: verify.",
                "invocation_mode": "explicit-preferred",
                "technique_dependencies": ["AOA-T-0001"],
                "skill_path": "skills/aoa-test-skill/SKILL.md",
            },
            capsules["skills"][0],
        )

    def test_write_sections_generates_source_owned_section_surface(self) -> None:
        repo_root = self.make_repo()

        sections_path = build_catalog.write_sections(repo_root)

        sections_payload = json.loads(sections_path.read_text(encoding="utf-8"))
        assert_entry = sections_payload["skills"][0]
        self.assertEqual(1, sections_payload["section_version"])
        self.assertEqual(
            {
                "skill_markdown": "skills/*/SKILL.md",
                "sections": [
                    "Intent",
                    "Trigger boundary",
                    "Inputs",
                    "Outputs",
                    "Procedure",
                    "Contracts",
                    "Risks and anti-patterns",
                    "Verification",
                    "Technique traceability",
                    "Adaptation points",
                ],
            },
            sections_payload["source_of_truth"],
        )
        self.assertEqual("aoa-test-skill", assert_entry["name"])
        self.assertEqual("skills/aoa-test-skill/SKILL.md", assert_entry["skill_path"])
        self.assertEqual(
            [
                "intent",
                "trigger_boundary",
                "inputs",
                "outputs",
                "procedure",
                "contracts",
                "risks_and_anti_patterns",
                "verification",
                "technique_traceability",
                "adaptation_points",
            ],
            [section["key"] for section in assert_entry["sections"]],
        )
        self.assertEqual("Intent text.", assert_entry["sections"][0]["content_markdown"])
        self.assertIn("1. step", assert_entry["sections"][4]["content_markdown"])

    def test_check_mode_passes_after_write(self) -> None:
        repo_root = self.make_repo()
        build_catalog.write_catalogs(repo_root)
        build_catalog.write_capsules(repo_root)
        build_catalog.write_sections(repo_root)

        self.assertEqual(0, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_catalog_is_stale(self) -> None:
        repo_root = self.make_repo()
        build_catalog.write_catalogs(repo_root)
        build_catalog.write_capsules(repo_root)
        build_catalog.write_sections(repo_root)
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "Test skill summary.",
                "Changed summary.",
            ),
            encoding="utf-8",
        )

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_capsules_are_stale(self) -> None:
        repo_root = self.make_repo()
        build_catalog.write_catalogs(repo_root)
        build_catalog.write_capsules(repo_root)
        build_catalog.write_sections(repo_root)
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "- verify",
                "- verify harder",
            ),
            encoding="utf-8",
        )

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_sections_are_stale(self) -> None:
        repo_root = self.make_repo()
        build_catalog.write_catalogs(repo_root)
        build_catalog.write_capsules(repo_root)
        build_catalog.write_sections(repo_root)
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Adaptation points\n\n- adapt\n",
                "## Adaptation points\n\n- adapt\n- adapt more\n",
            ),
            encoding="utf-8",
        )

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_write_catalogs_rejects_invalid_routing_contract(self) -> None:
        repo_root = self.make_repo()
        manifest_path = repo_root / "skills" / "aoa-test-skill" / "techniques.yaml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["techniques"][0]["repo"] = "aoa-evals"
        manifest["techniques"][0]["path"] = "../bad/path.md"
        manifest_path.write_text(
            yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "repo must resolve to 'aoa-techniques'",
        ):
            build_catalog.write_catalogs(repo_root)

    def test_check_mode_reports_invalid_routing_contract(self) -> None:
        repo_root = self.make_repo()
        manifest_path = repo_root / "skills" / "aoa-test-skill" / "techniques.yaml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["techniques"][0]["repo"] = "aoa-evals"
        manifest["techniques"][0]["path"] = "../bad/path.md"
        manifest_path.write_text(
            yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
        )

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_write_capsules_rejects_missing_required_source_section(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Verification\n\n- verify\n\n",
                "",
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "capsule source section 'Verification' is missing",
        ):
            build_catalog.write_capsules(repo_root)

    def test_write_capsules_ignores_indented_fake_heading(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Verification\n\n- verify\n\n",
                "## Procedure\n\n1. step\n\n    ## Verification\n\n    - example only\n\n",
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "capsule source section 'Verification' is missing",
        ):
            build_catalog.write_capsules(repo_root)

    def test_write_sections_rejects_reordered_top_level_sections(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Outputs\n\n- output\n\n## Procedure\n\n1. step\n",
                "## Procedure\n\n1. step\n\n## Outputs\n\n- output\n",
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "top-level sections must match the canonical order exactly",
        ):
            build_catalog.write_sections(repo_root)


if __name__ == "__main__":
    unittest.main()
