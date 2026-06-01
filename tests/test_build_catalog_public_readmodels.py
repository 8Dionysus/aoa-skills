from __future__ import annotations

from tests.support.build_catalog_case import *


class BuildCatalogPublicReadmodelsTests(BuildCatalogCase):
    def test_write_sections_generates_source_owned_section_surface(self) -> None:
        repo_root = self.make_repo()

        sections_path = build_catalog.write_sections(repo_root)

        sections_payload = json.loads(sections_path.read_text(encoding="utf-8"))
        assert_entry = sections_payload["skills"][0]
        self.assertEqual(1, sections_payload["section_version"])
        self.assertEqual(
            {
                "skill_markdown": "skills/**/SKILL.md",
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
        self.assertEqual(
            "Intent text.", assert_entry["sections"][0]["content_markdown"]
        )
        self.assertIn("1. step", assert_entry["sections"][4]["content_markdown"])

    def test_write_walkthroughs_generates_runtime_inspect_surface(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        walkthrough_json_path, walkthrough_markdown_path = (
            build_catalog.write_walkthroughs(repo_root)
        )

        payload = self.load_walkthroughs(repo_root)
        markdown = self.load_walkthroughs_markdown(repo_root)
        self.assertEqual(
            build_catalog.WALKTHROUGH_VERSION, payload["walkthrough_version"]
        )
        self.assertEqual(
            build_catalog.WALKTHROUGH_SOURCE_OF_TRUTH,
            payload["source_of_truth"],
        )
        self.assertEqual(
            walkthrough_json_path, repo_root / build_catalog.WALKTHROUGHS_JSON_PATH
        )
        self.assertEqual(
            walkthrough_markdown_path,
            repo_root / build_catalog.WALKTHROUGHS_MARKDOWN_PATH,
        )
        self.assertEqual(
            {
                "name": "aoa-test-skill",
                "scope": "core",
                "status": "evaluated",
                "invocation_mode": "explicit-preferred",
                "skill_path": "skills/aoa-test-skill/SKILL.md",
                "pick_summary": "Test skill summary.",
                "use_when": ["needed"],
                "do_not_use_when": ["not needed"],
                "inspection_order": ["capsule", "sections", "full", "evidence"],
                "expand_sections": [
                    "Procedure",
                    "Contracts",
                    "Risks and anti-patterns",
                    "Verification",
                ],
                "object_use_shape": ["output"],
                "support_artifacts": [
                    {
                        "type": "runtime_example",
                        "path": "skills/aoa-test-skill/examples/example.md",
                        "selected_for_runtime_inspection": True,
                    },
                    {
                        "type": "promotion_review",
                        "path": "docs/reviews/status-promotions/aoa-test-skill.md",
                        "selected_for_runtime_inspection": False,
                    },
                ],
            },
            payload["skills"][0],
        )
        self.assertIn("## Shared inspection path", markdown)
        self.assertIn("## aoa-test-skill", markdown)
        self.assertIn("`runtime_example` (selected)", markdown)

    def test_walkthrough_support_artifact_precedence_prefers_runtime_example_then_review(
        self,
    ) -> None:
        repo_root = self.make_repo()
        skill_dir = repo_root / "skills" / "aoa-test-skill"
        checks_dir = skill_dir / "checks"
        checks_dir.mkdir()
        (checks_dir / "review.md").write_text(
            textwrap.dedent(
                """\
                # Review Checklist

                ## Purpose

                Review purpose.

                ## When it applies

                - when bounded review is needed

                ## Review checklist

                - [ ] confirm scope

                ## Not a fit

                - not for unrelated rewrites
                """
            ),
            encoding="utf-8",
        )
        (skill_dir / "examples" / "runtime.md").write_text(
            textwrap.dedent(
                """\
                # Runtime Example

                ## Scenario

                Runtime scenario.

                ## Why this skill fits

                - explicit runtime example

                ## Expected inputs

                - input

                ## Expected outputs

                - output

                ## Boundary notes

                - keep scope bounded

                ## Verification notes

                - verify the outcome
                """
            ),
            encoding="utf-8",
        )

        payload = build_catalog.build_walkthrough_payload(repo_root)
        support_artifacts = payload["skills"][0]["support_artifacts"]
        selected_paths = [
            artifact["path"]
            for artifact in support_artifacts
            if artifact["selected_for_runtime_inspection"]
        ]
        self.assertEqual(
            ["skills/aoa-test-skill/examples/runtime.md"],
            selected_paths,
        )

        (skill_dir / "examples" / "runtime.md").unlink()
        payload = build_catalog.build_walkthrough_payload(repo_root)
        support_artifacts = payload["skills"][0]["support_artifacts"]
        selected_paths = [
            artifact["path"]
            for artifact in support_artifacts
            if artifact["selected_for_runtime_inspection"]
        ]
        self.assertEqual(
            ["skills/aoa-test-skill/examples/example.md"],
            selected_paths,
        )

        shutil.rmtree(skill_dir / "examples")
        payload = build_catalog.build_walkthrough_payload(repo_root)
        support_artifacts = payload["skills"][0]["support_artifacts"]
        selected_paths = [
            artifact["path"]
            for artifact in support_artifacts
            if artifact["selected_for_runtime_inspection"]
        ]
        self.assertEqual(
            ["skills/aoa-test-skill/checks/review.md"],
            selected_paths,
        )

    def test_write_public_surface_marks_canonical_skill_as_default_reference(
        self,
    ) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_surfaces=("canonical-candidates",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_public_surface(repo_root)

        payload = self.load_public_surface(repo_root)
        skill_entry = payload["skills"][0]
        self.assertTrue(skill_entry["is_default_reference"])
        self.assertEqual("canonical", skill_entry["maturity_status"])
        self.assertEqual("ready", skill_entry["default_reference_readiness"])
        self.assertEqual([], skill_entry["default_reference_readiness_blockers"])
        self.assertTrue(skill_entry["canonical_candidate_ready"])
        self.assertEqual([], skill_entry["canonical_candidate_blockers"])
        self.assertEqual(
            ["aoa-test-skill"],
            payload["cohorts"]["default_references"],
        )

    def test_write_public_surface_keeps_pending_lineage_as_bridge_finding(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            techniques=[PENDING_TECHNIQUE],
            review_surfaces=("status-promotions", "canonical-candidates"),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_public_surface(repo_root)

        payload = self.load_public_surface(repo_root)
        skill_entry = payload["skills"][0]
        self.assertEqual("ready", skill_entry["default_reference_readiness"])
        self.assertEqual("pending", skill_entry["lineage_state"])
        self.assertTrue(skill_entry["canonical_candidate_ready"])
        self.assertEqual([], skill_entry["default_reference_readiness_blockers"])
        self.assertEqual([], skill_entry["canonical_candidate_blockers"])
        self.assertIn(
            "pending_technique_dependencies",
            skill_entry["technique_bridge_findings"],
        )
        self.assertIn(
            "pending_technique_entries",
            skill_entry["technique_bridge_findings"],
        )
        self.assertIn("tbd_technique_refs", skill_entry["technique_bridge_findings"])
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

    def test_write_public_surface_does_not_flag_valid_explicit_only_policy(
        self,
    ) -> None:
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

    def test_check_mode_passes_after_write(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_all_surfaces(repo_root)

        self.assertEqual(0, self.run_main(repo_root, ["--check"]))
        self.assertEqual(0, self.run_main(repo_root, ["--check", "--group", "reader"]))
        self.assertEqual(0, self.run_main(repo_root, ["--check", "--group", "public"]))
        self.assertEqual(
            0, self.run_main(repo_root, ["--check", "--group", "evaluation"])
        )
        self.assertEqual(
            0, self.run_main(repo_root, ["--check", "--group", "governance"])
        )

    def test_check_mode_fails_when_catalog_is_stale(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_all_surfaces(repo_root)
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
        self.write_all_surfaces(repo_root)
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
        self.write_all_surfaces(repo_root)
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
        self.write_all_surfaces(repo_root)

        public_surface_markdown_path = (
            repo_root / build_catalog.PUBLIC_SURFACE_MARKDOWN_PATH
        )
        public_surface_markdown_path.write_text(
            public_surface_markdown_path.read_text(encoding="utf-8").replace(
                "default-reference ready skills: 1",
                "default-reference ready skills: 0",
            ),
            encoding="utf-8",
        )

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))
        self.assertEqual(1, self.run_main(repo_root, ["--check", "--group", "public"]))
        self.assertEqual(0, self.run_main(repo_root, ["--check", "--group", "reader"]))

    def test_check_mode_fails_when_walkthroughs_are_stale(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_all_surfaces(repo_root)
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "- output",
                "- output\n- output detail",
            ),
            encoding="utf-8",
        )

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_walkthroughs_are_missing(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_all_surfaces(repo_root)

        (repo_root / build_catalog.WALKTHROUGHS_JSON_PATH).unlink()
        (repo_root / build_catalog.WALKTHROUGHS_MARKDOWN_PATH).unlink()

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

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
