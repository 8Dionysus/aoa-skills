from __future__ import annotations

from tests.support.build_catalog_case import *


class BuildCatalogEvaluationMatrixTests(BuildCatalogCase):
    def test_write_evaluation_matrix_generates_snapshot_backed_surface(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_surfaces=("canonical-candidates",),
            include_evaluation_fixtures=True,
        )

        matrix_json_path, matrix_markdown_path = build_catalog.write_evaluation_matrix(
            repo_root
        )

        payload = self.load_evaluation_matrix(repo_root)
        markdown = self.load_evaluation_matrix_markdown(repo_root)
        self.assertEqual(
            build_catalog.EVALUATION_MATRIX_VERSION,
            payload["evaluation_matrix_version"],
        )
        self.assertEqual(
            build_catalog.EVALUATION_MATRIX_SOURCE_OF_TRUTH,
            payload["source_of_truth"],
        )
        self.assertEqual(
            matrix_json_path,
            repo_root / build_catalog.EVALUATION_MATRIX_JSON_PATH,
        )
        self.assertEqual(
            matrix_markdown_path,
            repo_root / build_catalog.EVALUATION_MATRIX_MARKDOWN_PATH,
        )
        self.assertEqual(
            {
                "name": "aoa-test-skill",
                "status": "canonical",
                "scope": "core",
                "invocation_mode": "explicit-preferred",
                "skill_path": "skills/aoa-test-skill/SKILL.md",
                "autonomy_check_count": 1,
                "use_case_count": 1,
                "do_not_use_case_count": 1,
                "use_snapshot_count": 1,
                "do_not_use_snapshot_count": 1,
                "selected_runtime_artifact_path": "skills/aoa-test-skill/examples/example.md",
                "promotion_review_path": None,
                "candidate_review_path": "docs/reviews/canonical-candidates/aoa-test-skill.md",
                "canonical_eval_ready": True,
                "canonical_eval_blockers": [],
            },
            payload["skills"][0],
        )
        self.assertIn("# Skill evaluation matrix", markdown)
        self.assertIn(
            "| aoa-test-skill | canonical | core | explicit-preferred |", markdown
        )

    def test_evaluation_matrix_rejects_existing_absolute_snapshot_path(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_surfaces=("canonical-candidates",),
            include_evaluation_fixtures=True,
        )
        external_dir = Path(tempfile.mkdtemp(prefix="aoa-skills-external-snapshot-"))
        self.addCleanup(shutil.rmtree, external_dir, True)
        external_snapshot = external_dir / "aoa_test_skill_use_snapshot_1.md"
        external_snapshot.write_text(
            textwrap.dedent(
                """\
                # Evaluation Snapshot

                ## Prompt

                use case

                ## Expected selection

                Decision: use `aoa-test-skill`.

                ## Why

                - the bounded trigger is needed

                ## Expected object

                - output

                ## Boundary notes

                - keep the scope bounded

                ## Verification hooks

                - verify the output
                """
            ),
            encoding="utf-8",
        )
        fixtures_path = repo_root / "tests" / "fixtures" / "skill_evaluation_cases.yaml"
        fixtures = yaml.safe_load(fixtures_path.read_text(encoding="utf-8"))
        fixtures["snapshot_cases"][0]["snapshot_path"] = external_snapshot.as_posix()
        fixtures_path.write_text(
            yaml.safe_dump(fixtures, sort_keys=False),
            encoding="utf-8",
        )

        payload = build_catalog.build_evaluation_matrix_payload(repo_root)

        self.assertFalse(payload["skills"][0]["canonical_eval_ready"])
        self.assertIn(
            skill_evaluation_contract.BLOCKER_MISSING_SNAPSHOT_FILE,
            payload["skills"][0]["canonical_eval_blockers"],
        )

    def test_check_mode_fails_when_evaluation_matrix_is_stale(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_surfaces=("canonical-candidates",),
            include_evaluation_fixtures=True,
        )
        self.write_all_surfaces(repo_root)

        matrix_markdown_path = repo_root / build_catalog.EVALUATION_MATRIX_MARKDOWN_PATH
        matrix_markdown_path.write_text("stale matrix markdown\n", encoding="utf-8")

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))


if __name__ == "__main__":
    unittest.main()
