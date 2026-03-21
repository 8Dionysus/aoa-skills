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
PENDING_TECHNIQUE = {
    "id": "AOA-T-PENDING-TEST",
    "repo": "8Dionysus/aoa-techniques",
    "path": "TBD",
    "source_ref": "TBD",
    "use_sections": ["Intent"],
}


class BuildCatalogTests(unittest.TestCase):
    def make_repo(
        self,
        *,
        status: str = "scaffold",
        invocation_mode: str = "explicit-preferred",
        traceability_heading: str = "Technique traceability",
        techniques: list[dict] | None = None,
        review_surfaces: tuple[str, ...] = (),
        include_evaluation_fixtures: bool = False,
        policy_allow_implicit: bool | None = None,
        scope: str = "core",
    ) -> Path:
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

        techniques = techniques or [PRIMARY_PUBLISHED_TECHNIQUE]
        technique_ids = [entry["id"] for entry in techniques]

        (repo_root / "SKILL_INDEX.md").write_text(
            "# SKILL_INDEX\n\n| name | scope | status | summary |\n|---|---|---|---|\n"
            f"| aoa-test-skill | {scope} | {status} | Test summary. |\n",
            encoding="utf-8",
        )
        (skill_dir / "SKILL.md").write_text(
            textwrap.dedent(
                f"""\
                ---
                name: aoa-test-skill
                scope: {scope}
                status: {status}
                summary: Test skill summary.
                invocation_mode: {invocation_mode}
                technique_dependencies:
                """
            )
            + "".join(f"  - {technique_id}\n" for technique_id in technique_ids)
            + textwrap.dedent(
                f"""\

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

                ## {traceability_heading}

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
                    "techniques": techniques,
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )

        if policy_allow_implicit is not None:
            agents_dir = skill_dir / "agents"
            agents_dir.mkdir()
            (agents_dir / "openai.yaml").write_text(
                yaml.safe_dump(
                    {
                        "policy": {
                            "allow_implicit_invocation": policy_allow_implicit,
                        },
                        "notes": ["Test policy."],
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )

        for surface in review_surfaces:
            if surface == "status-promotions":
                review_dir = repo_root / "docs" / "reviews" / "status-promotions"
                title = "# aoa-test-skill status promotion review\n"
            elif surface == "canonical-candidates":
                review_dir = repo_root / "docs" / "reviews" / "canonical-candidates"
                title = "# aoa-test-skill canonical candidate review\n"
            else:
                raise ValueError(f"unknown review surface '{surface}'")
            review_dir.mkdir(parents=True, exist_ok=True)
            (review_dir / "aoa-test-skill.md").write_text(
                title + "\n## Findings\n\n- Evidence exists.\n",
                encoding="utf-8",
            )

        if include_evaluation_fixtures:
            fixtures_dir = repo_root / "tests" / "fixtures"
            fixtures_dir.mkdir(parents=True, exist_ok=True)
            (fixtures_dir / "skill_evaluation_cases.yaml").write_text(
                yaml.safe_dump(
                    {
                        "autonomy_checks": [
                            {
                                "skill": "aoa-test-skill",
                                "forbidden_runtime_terms": ["aoa-techniques"],
                            }
                        ],
                        "trigger_cases": [
                            {
                                "skill": "aoa-test-skill",
                                "case_id": "aoa_test_skill_use_1",
                                "prompt": "use case",
                                "expected": "use",
                                "required_phrases": ["needed"],
                            },
                            {
                                "skill": "aoa-test-skill",
                                "case_id": "aoa_test_skill_do_not_use_1",
                                "prompt": "do not use case",
                                "expected": "do_not_use",
                                "required_phrases": ["not needed"],
                            },
                        ],
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

    def load_public_surface(self, repo_root: Path) -> dict:
        path = repo_root / build_catalog.PUBLIC_SURFACE_JSON_PATH
        return json.loads(path.read_text(encoding="utf-8"))

    def load_public_surface_markdown(self, repo_root: Path) -> str:
        path = repo_root / build_catalog.PUBLIC_SURFACE_MARKDOWN_PATH
        return path.read_text(encoding="utf-8")

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
                "trigger_boundary_short": "Use when needed; Avoid when not needed.",
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

    def test_write_public_surface_marks_canonical_skill_as_default_reference(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_surfaces=("canonical-candidates",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_public_surface(repo_root)

        payload = self.load_public_surface(repo_root)
        skill_entry = payload["skills"][0]
        self.assertTrue(skill_entry["is_default_reference"])
        self.assertTrue(skill_entry["canonical_candidate_ready"])
        self.assertEqual([], skill_entry["canonical_candidate_blockers"])
        self.assertEqual(
            ["aoa-test-skill"],
            payload["cohorts"]["default_references"],
        )

    def test_write_public_surface_marks_published_evaluated_skill_as_candidate_ready(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_public_surface(repo_root)

        payload = self.load_public_surface(repo_root)
        skill_entry = payload["skills"][0]
        self.assertEqual("published", skill_entry["lineage_state"])
        self.assertTrue(skill_entry["canonical_candidate_ready"])
        self.assertEqual(
            ["aoa-test-skill"],
            payload["cohorts"]["candidate_ready"],
        )

    def test_write_public_surface_marks_pending_lineage_and_resolves_both_review_paths(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            techniques=[PENDING_TECHNIQUE],
            review_surfaces=("status-promotions", "canonical-candidates"),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_public_surface(repo_root)

        payload = self.load_public_surface(repo_root)
        skill_entry = payload["skills"][0]
        self.assertEqual("pending", skill_entry["lineage_state"])
        self.assertFalse(skill_entry["canonical_candidate_ready"])
        self.assertIn(
            "pending_technique_dependencies",
            skill_entry["canonical_candidate_blockers"],
        )
        self.assertIn(
            "pending_technique_entries",
            skill_entry["canonical_candidate_blockers"],
        )
        self.assertIn(
            "tbd_technique_refs",
            skill_entry["canonical_candidate_blockers"],
        )
        self.assertEqual(
            "docs/reviews/status-promotions/aoa-test-skill.md",
            skill_entry["promotion_review_path"],
        )
        self.assertEqual(
            "docs/reviews/canonical-candidates/aoa-test-skill.md",
            skill_entry["candidate_review_path"],
        )
        self.assertEqual(
            ["aoa-test-skill"],
            payload["cohorts"]["blocked_by_pending_lineage"],
        )

    def test_write_public_surface_does_not_flag_valid_explicit_only_policy(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            invocation_mode="explicit-only",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
            policy_allow_implicit=False,
            scope="risk",
        )

        build_catalog.write_public_surface(repo_root)

        payload = self.load_public_surface(repo_root)
        skill_entry = payload["skills"][0]
        self.assertNotIn(
            "explicit_only_policy_violation",
            skill_entry["canonical_candidate_blockers"],
        )
        self.assertEqual(["aoa-test-skill"], payload["cohorts"]["risk_surfaces"])

    def test_public_surface_markdown_reflects_candidate_ready_cohort(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_public_surface(repo_root)

        markdown = self.load_public_surface_markdown(repo_root)
        self.assertIn("## Candidate-ready cohort", markdown)
        self.assertIn("| aoa-test-skill | evaluated | core | explicit-preferred | published | - |", markdown)

    def test_check_mode_passes_after_write(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        build_catalog.write_catalogs(repo_root)
        build_catalog.write_capsules(repo_root)
        build_catalog.write_sections(repo_root)
        build_catalog.write_public_surface(repo_root)

        self.assertEqual(0, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_catalog_is_stale(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        build_catalog.write_catalogs(repo_root)
        build_catalog.write_capsules(repo_root)
        build_catalog.write_sections(repo_root)
        build_catalog.write_public_surface(repo_root)
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
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        build_catalog.write_catalogs(repo_root)
        build_catalog.write_capsules(repo_root)
        build_catalog.write_sections(repo_root)
        build_catalog.write_public_surface(repo_root)
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
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        build_catalog.write_catalogs(repo_root)
        build_catalog.write_capsules(repo_root)
        build_catalog.write_sections(repo_root)
        build_catalog.write_public_surface(repo_root)
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Adaptation points\n\n- adapt\n",
                "## Adaptation points\n\n- adapt\n- adapt more\n",
            ),
            encoding="utf-8",
        )

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_public_surface_is_stale(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        build_catalog.write_catalogs(repo_root)
        build_catalog.write_capsules(repo_root)
        build_catalog.write_sections(repo_root)
        build_catalog.write_public_surface(repo_root)

        public_surface_markdown_path = repo_root / build_catalog.PUBLIC_SURFACE_MARKDOWN_PATH
        public_surface_markdown_path.write_text(
            public_surface_markdown_path.read_text(encoding="utf-8").replace(
                "candidate-ready skills: 1",
                "candidate-ready skills: 0",
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
