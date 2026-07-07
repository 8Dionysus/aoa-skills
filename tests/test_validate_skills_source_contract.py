from __future__ import annotations

from tests.support.validate_skills_case import *


class ValidateSkillsSourceContractTests(ValidateSkillsCase):
    def test_clean_fixture_passes(self) -> None:
        repo_root = self.make_repo()
        issues = validate_skills.run_validation(repo_root)
        self.assertEqual([], issues)
        self.assertEqual(0, self.run_main(repo_root))
        self.assertEqual(0, self.run_main(repo_root, ["--skill", "aoa-test-skill"]))

    def test_pending_technique_count_deduplicates_manifest_and_frontmatter_ids(
        self,
    ) -> None:
        published_count, pending_count, tbd_ref_count = (
            skill_lineage_surface.technique_counts(
                ["AOA-T-PENDING-TEST"],
                [
                    {"id": "AOA-T-PENDING-TEST", "path": "TBD", "source_ref": "TBD"},
                    PRIMARY_PUBLISHED_TECHNIQUE,
                ],
            )
        )

        self.assertEqual(1, published_count)
        self.assertEqual(1, pending_count)
        self.assertEqual(1, tbd_ref_count)

    def test_future_traceability_heading_is_rejected(self) -> None:
        repo_root = self.make_repo(traceability_heading="Future traceability")

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("missing required section 'Technique traceability'", messages)
        self.assertIn("unexpected top-level section 'Future traceability'", messages)

    def test_linked_status_is_allowed(self) -> None:
        repo_root = self.make_repo(status="linked")
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_linked_status_with_unpinned_source_ref_fails(self) -> None:
        repo_root = self.make_repo(
            status="linked",
            techniques=[
                {
                    "id": "AOA-T-0009",
                    "repo": "8Dionysus/aoa-techniques",
                    "path": "techniques/test/TECHNIQUE.md",
                    "source_ref": "TBD",
                    "use_sections": ["Intent"],
                }
            ],
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "status 'linked' requires published techniques to use concrete source_ref values",
            messages,
        )

    def test_frontmatter_schema_violation_fails(self) -> None:
        repo_root = self.make_repo()
        frontmatter = self.load_skill_frontmatter(repo_root)
        frontmatter["summary"] = ["not", "a", "string"]
        self.write_skill_frontmatter(repo_root, frontmatter)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertTrue(any("schema violation" in message for message in messages))

    def test_manifest_schema_violation_fails(self) -> None:
        repo_root = self.make_repo()
        manifest = self.load_manifest(repo_root)
        manifest["unexpected"] = True
        self.write_manifest(repo_root, manifest)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertTrue(any("schema violation" in message for message in messages))

    def test_policy_schema_violation_fails(self) -> None:
        repo_root = self.make_repo(policy_allow_implicit=False)
        self.write_policy(
            repo_root,
            {
                "policy": {"allow_implicit_invocation": "sometimes"},
                "notes": ["Invalid policy fixture."],
            },
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertTrue(any("schema violation" in message for message in messages))

    def test_missing_techniques_yaml_fails(self) -> None:
        repo_root = self.make_repo(include_techniques_manifest=False)
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("file is missing", messages)
        self.assertEqual(1, self.run_main(repo_root))

    def test_missing_support_artifact_fails(self) -> None:
        repo_root = self.make_repo(include_support_artifact=False)
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "missing support artifact under examples/*.md, checks/review.md, or docs/reviews/*",
            messages,
        )

    def test_explicit_only_without_policy_fails(self) -> None:
        repo_root = self.make_repo(invocation_mode="explicit-only")
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("explicit-only skills require agents/openai.yaml", messages)

    def test_explicit_only_with_implicit_policy_fails(self) -> None:
        repo_root = self.make_repo(
            invocation_mode="explicit-only",
            policy_allow_implicit=True,
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "explicit-only skills must set 'policy.allow_implicit_invocation' to false",
            messages,
        )

    def test_pending_technique_with_non_tbd_path_fails(self) -> None:
        repo_root = self.make_repo(
            techniques=[
                {
                    **PENDING_TECHNIQUE,
                    "path": "techniques/test/TECHNIQUE.md",
                }
            ],
            notes=[PENDING_NOTE],
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("pending techniques must use path 'TBD'", messages)

    def test_published_technique_with_tbd_path_fails(self) -> None:
        repo_root = self.make_repo(
            techniques=[
                {
                    "id": "AOA-T-0009",
                    "repo": "8Dionysus/aoa-techniques",
                    "path": "TBD",
                    "source_ref": "0123456789abcdef0123456789abcdef01234567",
                    "use_sections": ["Intent"],
                }
            ]
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("published techniques cannot use path 'TBD'", messages)

    def test_pending_technique_with_non_tbd_source_ref_fails(self) -> None:
        repo_root = self.make_repo(
            techniques=[
                {
                    **PENDING_TECHNIQUE,
                    "source_ref": "0123456789abcdef0123456789abcdef01234567",
                }
            ],
            notes=[PENDING_NOTE],
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("pending techniques must use source_ref 'TBD'", messages)

    def test_published_technique_with_tbd_source_ref_fails(self) -> None:
        repo_root = self.make_repo(
            techniques=[
                {
                    "id": "AOA-T-0009",
                    "repo": "8Dionysus/aoa-techniques",
                    "path": "techniques/test/TECHNIQUE.md",
                    "source_ref": "TBD",
                    "use_sections": ["Intent"],
                }
            ]
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("published techniques cannot use source_ref 'TBD'", messages)

    def test_skill_index_mismatch_fails(self) -> None:
        repo_root = self.make_repo(index_names=["aoa-other-skill"])
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("skill 'aoa-test-skill' is missing from the index", messages)
        self.assertIn(
            "index lists 'aoa-other-skill' but no matching skill directory exists",
            messages,
        )

    def test_skill_index_accepts_os_project_overlay_names(self) -> None:
        repo_root = self.make_repo(skill_name="os-test-skill", scope="project")
        self.assertEqual([], validate_skills.validate_skill_index(repo_root))

    def test_pending_technique_with_tbd_refs_passes_for_scaffold_skill(self) -> None:
        repo_root = self.make_repo(
            techniques=[PENDING_TECHNIQUE],
            notes=[PENDING_NOTE],
        )
        self.write_catalogs(repo_root)
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_invalid_runtime_example_headings_fail(self) -> None:
        repo_root = self.make_repo()
        example_path = (
            repo_root / "skills" / "aoa-test-skill" / "examples" / "example.md"
        )
        example_path.write_text(
            textwrap.dedent(
                """\
                # Example

                ## Scenario

                Example scenario.

                ## Inputs

                - input
                """
            ),
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "runtime example missing required section 'Why this skill fits'",
            messages,
        )
        self.assertIn(
            "runtime example top-level sections must match the canonical order exactly",
            messages,
        )

    def test_technique_dependencies_must_match_manifest_order(self) -> None:
        repo_root = self.make_repo(
            techniques=[PRIMARY_PUBLISHED_TECHNIQUE, SECONDARY_PUBLISHED_TECHNIQUE],
        )
        frontmatter = self.load_skill_frontmatter(repo_root)
        frontmatter["technique_dependencies"] = [
            SECONDARY_PUBLISHED_TECHNIQUE["id"],
            PRIMARY_PUBLISHED_TECHNIQUE["id"],
        ]
        self.write_skill_frontmatter(repo_root, frontmatter)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "frontmatter 'technique_dependencies' must exactly match techniques.yaml technique IDs in order",
            messages,
        )

    def test_manifest_repo_mismatch_fails_directly(self) -> None:
        repo_root = self.make_repo()
        manifest = self.load_manifest(repo_root)
        manifest["techniques"][0]["repo"] = "example/other-repo"
        self.write_manifest(repo_root, manifest)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("repo must resolve to 'aoa-techniques'", messages)

    def test_malformed_manifest_techniques_list_reports_issue_without_crashing(
        self,
    ) -> None:
        repo_root = self.make_repo()
        manifest = self.load_manifest(repo_root)
        manifest["techniques"] = "broken"
        self.write_manifest(repo_root, manifest)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("techniques.yaml must contain a techniques list", messages)

    def test_published_technique_requires_repo_relative_path(self) -> None:
        repo_root = self.make_repo()
        manifest = self.load_manifest(repo_root)
        manifest["techniques"][0]["path"] = "../techniques/test/TECHNIQUE.md"
        self.write_manifest(repo_root, manifest)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "published techniques must use concrete repo-relative paths",
            messages,
        )


if __name__ == "__main__":
    unittest.main()
