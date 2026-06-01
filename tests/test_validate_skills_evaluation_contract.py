from __future__ import annotations

from tests.support.validate_skills_case import *


class ValidateSkillsEvaluationContractTests(ValidateSkillsCase):
    def test_canonical_status_allows_pending_technique_bridge_lineage(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
            techniques=[PENDING_TECHNIQUE],
            notes=[PENDING_NOTE],
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertNotIn(
            "status 'canonical' cannot use pending technique_dependencies", messages
        )
        self.assertNotIn(
            "status 'canonical' cannot use pending techniques in techniques.yaml",
            messages,
        )

    def test_canonical_status_rejects_legacy_future_traceability(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            traceability_heading="Future traceability",
            review_record_surface="canonical-candidates",
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("missing required section 'Technique traceability'", messages)
        self.assertIn("unexpected top-level section 'Future traceability'", messages)

    def test_canonical_status_rejects_tbd_traceability_values(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
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
            "published techniques cannot use source_ref 'TBD'",
            messages,
        )

    def test_evaluated_status_requires_evaluation_fixture_file(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("file is missing", messages)

    def test_evaluated_status_with_only_autonomy_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(
            repo_root,
            include_autonomy=True,
            use_cases=0,
            do_not_use_cases=0,
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "skill 'aoa-test-skill' with status 'evaluated' requires at least one 'use' trigger case",
            messages,
        )
        self.assertIn(
            "skill 'aoa-test-skill' with status 'evaluated' requires at least one 'do_not_use' trigger case",
            messages,
        )

    def test_evaluated_status_with_one_trigger_side_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(
            repo_root,
            include_autonomy=True,
            use_cases=1,
            do_not_use_cases=0,
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "skill 'aoa-test-skill' with status 'evaluated' requires at least one 'do_not_use' trigger case",
            messages,
        )

    def test_canonical_status_requires_evaluation_fixture_file(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("file is missing", messages)

    def test_evaluated_status_passes_with_full_evaluation_coverage(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_canonical_status_passes_with_full_evaluation_coverage(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_evaluated_status_allows_reportable_snapshot_gaps(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(
            repo_root,
            use_snapshots=0,
            do_not_use_snapshots=0,
        )
        self.write_catalogs(repo_root)

        self.assertEqual([], validate_skills.run_validation(repo_root))
        matrix = self.load_evaluation_matrix(repo_root)
        self.assertEqual(
            [
                "missing_use_snapshot",
                "missing_do_not_use_snapshot",
            ],
            matrix["skills"][0]["canonical_eval_blockers"],
        )

    def test_canonical_status_requires_use_snapshot(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
        )
        self.write_evaluation_fixtures_for_skill(
            repo_root,
            use_snapshots=0,
            do_not_use_snapshots=1,
        )
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "status 'canonical' requires at least one 'use' snapshot case",
            messages,
        )

    def test_canonical_status_requires_do_not_use_snapshot(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
        )
        self.write_evaluation_fixtures_for_skill(
            repo_root,
            use_snapshots=1,
            do_not_use_snapshots=0,
        )
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "status 'canonical' requires at least one 'do_not_use' snapshot case",
            messages,
        )

    def test_invalid_snapshot_headings_fail(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        snapshot_path = (
            repo_root
            / "tests"
            / "fixtures"
            / "skill_evaluation_snapshots"
            / "aoa-test-skill"
            / "aoa_test_skill_use_1.md"
        )
        snapshot_path.write_text(
            snapshot_path.read_text(encoding="utf-8").replace(
                "## Expected object\n\n- output\n\n",
                "",
            ),
            encoding="utf-8",
        )
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "evaluation snapshot missing required section 'Expected object'",
            messages,
        )
        self.assertIn(
            "evaluation snapshot top-level sections must match the canonical order exactly",
            messages,
        )

    def test_snapshot_missing_required_phrase_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        snapshot_path = (
            repo_root
            / "tests"
            / "fixtures"
            / "skill_evaluation_snapshots"
            / "aoa-test-skill"
            / "aoa_test_skill_use_1.md"
        )
        snapshot_path.write_text(
            snapshot_path.read_text(encoding="utf-8").replace(
                "Decision: use `aoa-test-skill`.",
                "Decision: inspect `aoa-test-skill`.",
            ),
            encoding="utf-8",
        )
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "evaluation snapshot is missing required output phrase 'Decision: use `aoa-test-skill`.'",
            messages,
        )

    def test_snapshot_forbidden_phrase_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        snapshot_path = (
            repo_root
            / "tests"
            / "fixtures"
            / "skill_evaluation_snapshots"
            / "aoa-test-skill"
            / "aoa_test_skill_do_not_use_1.md"
        )
        snapshot_path.write_text(
            snapshot_path.read_text(encoding="utf-8").replace(
                "- confirm the deflection is explicit",
                "- confirm the deflection is explicit\n- Decision: use `aoa-test-skill`.",
            ),
            encoding="utf-8",
        )
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "evaluation snapshot contains forbidden output phrase 'Decision: use `aoa-test-skill`.'",
            messages,
        )

    def test_stale_generated_evaluation_matrix_json_fails(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)

        matrix = self.load_evaluation_matrix(repo_root)
        matrix["skills"][0]["use_snapshot_count"] = 0
        self.write_evaluation_matrix(repo_root, matrix)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated evaluation matrix is out of date; run python scripts/build_catalog.py",
            messages,
        )

    def test_stale_generated_evaluation_matrix_markdown_fails(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)

        matrix_markdown_path = repo_root / "generated" / "skill_evaluation_matrix.md"
        matrix_markdown_path.write_text(
            "stale evaluation matrix markdown\n", encoding="utf-8"
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated evaluation matrix markdown is out of date; run python scripts/build_catalog.py",
            messages,
        )


if __name__ == "__main__":
    unittest.main()
