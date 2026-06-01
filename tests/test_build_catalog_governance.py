from __future__ import annotations

from tests.support.build_catalog_case import *


class BuildCatalogGovernanceTests(BuildCatalogCase):
    def test_write_public_surface_marks_published_evaluated_skill_as_candidate_ready(
        self,
    ) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_public_surface(repo_root)

        payload = self.load_public_surface(repo_root)
        skill_entry = payload["skills"][0]
        self.assertEqual("published", skill_entry["lineage_state"])
        self.assertEqual("evaluated", skill_entry["maturity_status"])
        self.assertEqual("ready", skill_entry["default_reference_readiness"])
        self.assertEqual([], skill_entry["default_reference_readiness_blockers"])
        self.assertTrue(skill_entry["canonical_candidate_ready"])
        self.assertEqual(
            ["aoa-test-skill"],
            payload["cohorts"]["default_reference_ready"],
        )
        self.assertEqual(
            ["aoa-test-skill"],
            payload["cohorts"]["candidate_ready"],
        )

    def test_write_public_surface_preserves_candidate_ready_while_recording_stay_evaluated(
        self,
    ) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_governance_lanes(
            repo_root,
            [
                {
                    "id": "test_lane",
                    "title": "Test lane",
                    "scope": "core",
                    "state": "comparative_pending",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "stay_evaluated",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#test_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        build_catalog.write_public_surface(repo_root)

        payload = self.load_public_surface(repo_root)
        skill_entry = payload["skills"][0]
        self.assertEqual("ready", skill_entry["default_reference_readiness"])
        self.assertTrue(skill_entry["canonical_candidate_ready"])
        self.assertEqual("stay_evaluated", skill_entry["governance_decision"])
        self.assertEqual(["test_lane"], skill_entry["governance_lane_ids"])
        self.assertEqual([], skill_entry["governance_evidence_case_ids"])
        self.assertFalse(skill_entry["is_default_reference"])
        self.assertEqual(
            ["aoa-test-skill"], payload["cohorts"]["default_reference_ready"]
        )
        self.assertEqual(["aoa-test-skill"], payload["cohorts"]["candidate_ready"])

    def test_public_surface_markdown_reflects_candidate_ready_cohort(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_public_surface(repo_root)

        markdown = self.load_public_surface_markdown(repo_root)
        self.assertIn("## Default-reference ready cohort", markdown)
        self.assertIn(
            "| aoa-test-skill | evaluated | ready | core | explicit-preferred | published | - | - | - | - | `docs/reviews/status-promotions/aoa-test-skill.md` | - |",
            markdown,
        )

    def test_governance_backlog_renders_comparative_pending_cohort(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_governance_lanes(
            repo_root,
            [
                {
                    "id": "test_lane",
                    "title": "Test lane",
                    "scope": "core",
                    "state": "comparative_pending",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "stay_evaluated",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#test_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        build_catalog.write_governance_backlog(repo_root)

        payload = self.load_governance_backlog(repo_root)
        markdown = self.load_governance_backlog_markdown(repo_root)
        self.assertEqual(["aoa-test-skill"], payload["cohorts"]["comparative_pending"])
        self.assertEqual(["aoa-test-skill"], payload["cohorts"]["review_truth_sync"])
        self.assertFalse(payload["review_truth_sync"][0]["truth_synced"])
        self.assertEqual("stay_evaluated", payload["skills"][0]["governance_decision"])
        self.assertEqual(["test_lane"], payload["skills"][0]["governance_lane_ids"])
        self.assertIn("comparative pending cohort: 1", markdown)
        self.assertIn("## Review truth sync", markdown)
        self.assertIn("`comparative_pending`: aoa-test-skill", markdown)

    def test_write_skill_composition_audit_marks_multi_technique_skill(self) -> None:
        repo_root = self.make_repo(
            techniques=[PRIMARY_PUBLISHED_TECHNIQUE, SECONDARY_PUBLISHED_TECHNIQUE],
        )

        audit_json_path, audit_markdown_path = (
            build_catalog.write_skill_composition_audit(repo_root)
        )

        payload = self.load_skill_composition_audit(repo_root)
        markdown = self.load_skill_composition_audit_markdown(repo_root)
        self.assertEqual(
            build_catalog.SKILL_COMPOSITION_AUDIT_VERSION,
            payload["skill_composition_version"],
        )
        self.assertEqual(
            build_catalog.skill_composition_audit.SKILL_COMPOSITION_SOURCE_OF_TRUTH,
            payload["source_of_truth"],
        )
        self.assertEqual(
            repo_root / build_catalog.SKILL_COMPOSITION_AUDIT_JSON_PATH,
            audit_json_path,
        )
        self.assertEqual(
            repo_root / build_catalog.SKILL_COMPOSITION_AUDIT_MARKDOWN_PATH,
            audit_markdown_path,
        )
        self.assertEqual(
            {
                "total_skill_count": 1,
                "multi_technique_skill_count": 1,
                "single_technique_skill_count": 0,
                "approved_exception_count": 0,
                "needs_reframe_count": 0,
            },
            payload["summary"],
        )
        self.assertEqual(
            {
                "name": "aoa-test-skill",
                "technique_count": 2,
                "technique_ids": ["AOA-T-0001", "AOA-T-0002"],
                "composition_class": "multi_technique",
                "exception_review_path": None,
                "recommended_action": "keep_multi_technique",
            },
            payload["skills"][0],
        )
        self.assertIn("# Skill composition audit", markdown)
        self.assertIn(
            "| aoa-test-skill | 2 | multi_technique | keep_multi_technique | - |",
            markdown,
        )

    def test_write_skill_composition_audit_marks_reviewed_exception(self) -> None:
        repo_root = self.make_repo()
        self.write_skill_composition_exception_review(repo_root)

        build_catalog.write_skill_composition_audit(repo_root)

        payload = self.load_skill_composition_audit(repo_root)
        self.assertEqual(
            {
                "total_skill_count": 1,
                "multi_technique_skill_count": 0,
                "single_technique_skill_count": 1,
                "approved_exception_count": 1,
                "needs_reframe_count": 0,
            },
            payload["summary"],
        )
        self.assertEqual(
            "single_technique_exception",
            payload["skills"][0]["composition_class"],
        )
        self.assertEqual(
            "docs/reviews/skill-composition-exceptions/aoa-test-skill.md",
            payload["skills"][0]["exception_review_path"],
        )
        self.assertEqual(
            "keep_exception",
            payload["skills"][0]["recommended_action"],
        )

    def test_check_mode_fails_when_skill_composition_audit_is_stale(self) -> None:
        repo_root = self.make_repo()
        self.write_skill_composition_exception_review(repo_root)
        self.write_all_surfaces(repo_root)

        audit_markdown_path = (
            repo_root / build_catalog.SKILL_COMPOSITION_AUDIT_MARKDOWN_PATH
        )
        audit_markdown_path.write_text("stale composition audit\n", encoding="utf-8")

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))


if __name__ == "__main__":
    unittest.main()
