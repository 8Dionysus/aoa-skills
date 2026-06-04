from __future__ import annotations

from tests.support.validate_skills_case import *


class ValidateSkillsGeneratedDriftTests(ValidateSkillsCase):
    def test_build_catalog_projects_routing_surface(self) -> None:
        repo_root = self.make_repo(
            techniques=[PRIMARY_PUBLISHED_TECHNIQUE, SECONDARY_PUBLISHED_TECHNIQUE],
        )

        full_catalog = build_catalog.build_full_catalog(repo_root)
        min_catalog = build_catalog.project_min_catalog(full_catalog)

        self.assertEqual(1, full_catalog["catalog_version"])
        self.assertEqual(
            {
                "skill_markdown": "skills/**/SKILL.md",
                "technique_manifest": "skills/**/techniques.yaml",
            },
            full_catalog["source_of_truth"],
        )
        self.assertEqual(
            {
                "name": "aoa-test-skill",
                "scope": "core",
                "status": "scaffold",
                "summary": "Test skill summary.",
                "invocation_mode": "explicit-preferred",
                "technique_dependencies": ["AOA-T-0001", "AOA-T-0002"],
                "skill_path": "skills/aoa-test-skill/SKILL.md",
                "composition_mode": "bounded",
                "technique_refs": [
                    {
                        "id": "AOA-T-0001",
                        "repo": "aoa-techniques",
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
                    },
                    {
                        "id": "AOA-T-0002",
                        "repo": "aoa-techniques",
                        "path": "techniques/docs/source-of-truth-layout/TECHNIQUE.md",
                        "source_ref": "0123456789abcdef0123456789abcdef01234567",
                        "use_sections": ["summary"],
                    },
                ],
            },
            full_catalog["skills"][0],
        )
        self.assertEqual(
            {
                "catalog_version": 1,
                "source_of_truth": {
                    "skill_markdown": "skills/**/SKILL.md",
                    "technique_manifest": "skills/**/techniques.yaml",
                },
                "skills": [
                    {
                        "name": "aoa-test-skill",
                        "scope": "core",
                        "status": "scaffold",
                        "summary": "Test skill summary.",
                        "invocation_mode": "explicit-preferred",
                        "technique_dependencies": ["AOA-T-0001", "AOA-T-0002"],
                        "skill_path": "skills/aoa-test-skill/SKILL.md",
                    }
                ],
            },
            min_catalog,
        )

        capsules = build_catalog.build_capsules_payload(repo_root)
        self.assertEqual(1, capsules["capsule_version"])
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
                "technique_dependencies": ["AOA-T-0001", "AOA-T-0002"],
                "skill_path": "skills/aoa-test-skill/SKILL.md",
            },
            capsules["skills"][0],
        )

    def test_single_skill_validation_skips_generated_surfaces_by_default(self) -> None:
        repo_root = self.make_repo()
        self.write_catalogs(repo_root)

        lineage_path = repo_root / "generated" / "skill_lineage_surface.json"
        payload = json.loads(lineage_path.read_text(encoding="utf-8"))
        payload["skills"][0]["pending_technique_count"] = 99
        lineage_path.write_text(
            json.dumps(payload, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root, skill_name="aoa-test-skill")
        self.assertFalse(
            any(
                issue.message
                == "generated lineage surface artifact is out of date; run PYTHONPATH=scripts python scripts/builders/build_catalog.py"
                for issue in issues
            )
        )
        self.assertEqual(0, self.run_main(repo_root, ["--skill", "aoa-test-skill"]))

    def test_single_skill_validation_can_include_generated_surfaces(self) -> None:
        repo_root = self.make_repo()
        self.write_catalogs(repo_root)

        lineage_path = repo_root / "generated" / "skill_lineage_surface.json"
        payload = json.loads(lineage_path.read_text(encoding="utf-8"))
        payload["skills"][0]["pending_technique_count"] = 99
        lineage_path.write_text(
            json.dumps(payload, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(
            repo_root,
            skill_name="aoa-test-skill",
            validate_generated=True,
        )
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated lineage surface artifact is out of date; run PYTHONPATH=scripts python scripts/builders/build_catalog.py",
            messages,
        )
        self.assertEqual(
            1,
            self.run_main(repo_root, ["--skill", "aoa-test-skill", "--with-generated"]),
        )

    def test_stale_skill_composition_audit_surface_fails(self) -> None:
        repo_root = self.make_repo()
        self.write_catalogs(repo_root)

        audit = self.load_skill_composition_audit(repo_root)
        audit["summary"]["approved_exception_count"] = 99
        self.write_skill_composition_audit(repo_root, audit)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated skill composition audit artifact is out of date; run PYTHONPATH=scripts python scripts/builders/build_catalog.py",
            messages,
        )

    def test_empty_capsule_source_section_fails(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Verification\n\n- verify\n\n",
                "## Verification\n\n",
            ),
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "capsule source section 'Verification' must not be empty", messages
        )

    def test_missing_generated_catalogs_fail(self) -> None:
        repo_root = self.make_repo()
        shutil.rmtree(repo_root / "generated")

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("generated catalog is missing", messages)
        self.assertIn("generated capsules are missing", messages)
        self.assertIn("generated sections are missing", messages)
        self.assertIn("generated walkthrough surface is missing", messages)
        self.assertIn("generated walkthrough markdown is missing", messages)
        self.assertIn("generated public surface is missing", messages)
        self.assertIn("generated public surface markdown is missing", messages)
        self.assertIn("generated evaluation matrix is missing", messages)
        self.assertIn("generated evaluation matrix markdown is missing", messages)

    def test_stale_generated_catalogs_fail(self) -> None:
        repo_root = self.make_repo()
        frontmatter = self.load_skill_frontmatter(repo_root)
        frontmatter["summary"] = "Changed without rebuilding catalog."
        self.write_skill_frontmatter(repo_root, frontmatter)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated catalog is out of date; run PYTHONPATH=scripts python scripts/builders/build_catalog.py",
            messages,
        )

    def test_targeted_validation_catches_stale_generated_catalog_for_selected_skill(
        self,
    ) -> None:
        repo_root = self.make_repo()
        frontmatter = self.load_skill_frontmatter(repo_root)
        frontmatter["summary"] = "Changed without rebuilding catalog."
        self.write_skill_frontmatter(repo_root, frontmatter)

        issues = validate_skills.run_validation(
            repo_root,
            skill_name="aoa-test-skill",
            validate_generated=True,
        )
        messages = [issue.message for issue in issues]

        self.assertIn(
            "generated catalog entry for 'aoa-test-skill' is out of date; run PYTHONPATH=scripts python scripts/builders/build_catalog.py",
            messages,
        )
        self.assertIn(
            "generated min catalog entry for 'aoa-test-skill' is out of date; run PYTHONPATH=scripts python scripts/builders/build_catalog.py",
            messages,
        )
        self.assertIn(
            "generated capsule entry for 'aoa-test-skill' is out of date; run PYTHONPATH=scripts python scripts/builders/build_catalog.py",
            messages,
        )

    def test_min_catalog_must_match_full_projection(self) -> None:
        repo_root = self.make_repo()
        min_path = repo_root / "generated" / "skill_catalog.min.json"
        min_catalog = json.loads(min_path.read_text(encoding="utf-8"))
        min_catalog["skills"][0]["summary"] = "tampered"
        min_path.write_text(json.dumps(min_catalog), encoding="utf-8")

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "min catalog must be an exact projection of the full catalog",
            messages,
        )

    def test_malformed_full_catalog_reports_projection_issue_without_crashing(
        self,
    ) -> None:
        repo_root = self.make_repo()
        full_path = repo_root / "generated" / "skill_catalog.json"
        full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
        del full_catalog["skills"]
        full_path.write_text(json.dumps(full_catalog), encoding="utf-8")

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated catalog is malformed; min projection could not be computed",
            messages,
        )

    def test_targeted_validation_reports_malformed_catalog_entry_projection(
        self,
    ) -> None:
        repo_root = self.make_repo()
        full_path = repo_root / "generated" / "skill_catalog.json"
        full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
        del full_catalog["skills"][0]["summary"]
        full_path.write_text(json.dumps(full_catalog), encoding="utf-8")

        issues = validate_skills.run_validation(
            repo_root,
            skill_name="aoa-test-skill",
            validate_generated=True,
        )
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated catalog entry for 'aoa-test-skill' is malformed; min projection could not be computed",
            messages,
        )

    def test_stale_generated_capsules_fail(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "- verify",
                "- verify harder",
            ),
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated capsules are out of date; run PYTHONPATH=scripts python scripts/builders/build_catalog.py",
            messages,
        )

    def test_generated_capsules_must_align_with_full_catalog(self) -> None:
        repo_root = self.make_repo()
        capsules = self.load_capsules(repo_root)
        capsules["skills"][0]["scope"] = "risk"
        self.write_capsules(repo_root, capsules)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated capsule entry for 'aoa-test-skill' must align with full catalog field 'scope'",
            messages,
        )

    def test_stale_generated_sections_fail(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Adaptation points\n\n- adapt\n",
                "## Adaptation points\n\n- adapt\n- adapt more\n",
            ),
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated sections are out of date; run PYTHONPATH=scripts python scripts/builders/build_catalog.py",
            messages,
        )

    def test_generated_sections_must_align_with_full_catalog(self) -> None:
        repo_root = self.make_repo()
        sections = self.load_sections(repo_root)
        sections["skills"][0]["status"] = "promoted"
        self.write_sections(repo_root, sections)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated section entry for 'aoa-test-skill' must align with full catalog field 'status'",
            messages,
        )

    def test_targeted_validation_catches_stale_generated_section_for_selected_skill(
        self,
    ) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Adaptation points\n\n- adapt\n",
                "## Adaptation points\n\n- adapt\n- adapt more\n",
            ),
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(
            repo_root,
            skill_name="aoa-test-skill",
            validate_generated=True,
        )
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated section entry for 'aoa-test-skill' is out of date; run PYTHONPATH=scripts python scripts/builders/build_catalog.py",
            messages,
        )

    def test_stale_generated_public_surface_json_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)

        public_surface = self.load_public_surface(repo_root)
        public_surface["skills"][0]["summary"] = "tampered"
        self.write_public_surface(repo_root, public_surface)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated public surface is out of date; run PYTHONPATH=scripts python scripts/builders/build_catalog.py",
            messages,
        )

    def test_stale_generated_public_surface_markdown_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)

        public_surface_markdown_path = repo_root / "generated" / "public_surface.md"
        public_surface_markdown_path.write_text(
            "stale markdown\n",
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated public surface markdown is out of date; run PYTHONPATH=scripts python scripts/builders/build_catalog.py",
            messages,
        )

    def test_stale_generated_walkthrough_surface_fails(self) -> None:
        repo_root = self.make_repo()
        walkthroughs = self.load_walkthroughs(repo_root)
        walkthroughs["skills"][0]["pick_summary"] = "tampered"
        self.write_walkthroughs(repo_root, walkthroughs)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated walkthrough surface is out of date; run PYTHONPATH=scripts python scripts/builders/build_catalog.py",
            messages,
        )

    def test_stale_generated_walkthrough_markdown_fails(self) -> None:
        repo_root = self.make_repo()
        walkthrough_markdown_path = repo_root / "generated" / "skill_walkthroughs.md"
        walkthrough_markdown_path.write_text(
            "stale walkthrough markdown\n",
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated walkthrough markdown is out of date; run PYTHONPATH=scripts python scripts/builders/build_catalog.py",
            messages,
        )


if __name__ == "__main__":
    unittest.main()
