from __future__ import annotations

from tests.support.build_catalog_case import *


class BuildCatalogOverlayProfilesTests(BuildCatalogCase):
    def test_project_overlay_stays_out_of_candidate_ready_without_governance_lane(
        self,
    ) -> None:
        repo_root = self.make_repo(
            scope="project",
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_public_surface(repo_root)
        build_catalog.write_governance_backlog(repo_root)
        build_catalog.write_bundle_index(repo_root)

        public_payload = self.load_public_surface(repo_root)
        backlog_payload = self.load_governance_backlog(repo_root)
        bundle_payload = self.load_bundle_index(repo_root)

        public_entry = public_payload["skills"][0]
        backlog_entry = backlog_payload["skills"][0]
        bundle_entry = bundle_payload["skills"][0]

        self.assertEqual("not_applicable", public_entry["default_reference_readiness"])
        self.assertEqual([], public_entry["default_reference_readiness_blockers"])
        self.assertFalse(public_entry["canonical_candidate_ready"])
        self.assertEqual([], public_entry["canonical_candidate_blockers"])
        self.assertEqual([], public_payload["cohorts"]["default_reference_ready"])
        self.assertEqual([], public_payload["cohorts"]["candidate_ready"])
        self.assertEqual(
            [], backlog_payload["cohorts"]["candidate_ready_without_review"]
        )
        self.assertFalse(backlog_entry["canonical_candidate_ready"])
        self.assertFalse(bundle_entry["canonical_candidate_ready"])

    def test_project_overlay_backlog_marks_eval_ready_without_governance_lane(
        self,
    ) -> None:
        repo_root = self.make_repo(
            scope="project",
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_governance_backlog(repo_root)

        payload = self.load_governance_backlog(repo_root)
        markdown = self.load_governance_backlog_markdown(repo_root)
        skill_entry = payload["skills"][0]

        self.assertFalse(skill_entry["canonical_candidate_ready"])
        self.assertTrue(skill_entry["canonical_eval_ready"])
        self.assertEqual(
            "project_overlay_eval_ready",
            skill_entry["readiness_reconciliation"],
        )
        self.assertIn("project_overlay_eval_ready", markdown)

    def test_project_overlay_backlog_uses_governance_reconciliation_when_lane_present(
        self,
    ) -> None:
        repo_root = self.make_repo(
            scope="project",
            status="evaluated",
            review_surfaces=("status-promotions", "canonical-candidates"),
            include_evaluation_fixtures=True,
        )
        self.write_governance_lanes(
            repo_root,
            [
                {
                    "id": "project_lane",
                    "title": "Project lane",
                    "scope": "project",
                    "state": "candidate_ready",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "default_reference",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#project_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        build_catalog.write_governance_backlog(repo_root)

        payload = self.load_governance_backlog(repo_root)
        skill_entry = payload["skills"][0]
        self.assertEqual(5, payload["governance_backlog_version"])
        self.assertEqual(
            "governance_and_eval_ready", skill_entry["readiness_reconciliation"]
        )

    def test_project_overlay_backlog_marks_reviewable_family_as_federation_ready(
        self,
    ) -> None:
        repo_root = self.make_repo()
        skill_names = [
            "cinder-change-protocol",
            "cinder-source-of-truth-check",
        ]
        for skill_name in skill_names:
            self.add_skill_bundle(
                repo_root,
                skill_name=skill_name,
                scope="project",
                status="evaluated",
                techniques=[PRIMARY_PUBLISHED_TECHNIQUE],
                policy_allow_implicit=True,
                include_review_check=True,
            )
        self.write_evaluation_fixtures_for_skills(repo_root, skill_names)
        self.write_live_overlay_pack(
            repo_root,
            family="cinder",
            skill_names=skill_names,
        )

        build_catalog.write_governance_backlog(repo_root)

        payload = self.load_governance_backlog(repo_root)
        markdown = self.load_governance_backlog_markdown(repo_root)
        readiness_by_skill = {
            entry["name"]: entry["readiness_reconciliation"]
            for entry in payload["skills"]
        }

        self.assertEqual(
            "project_overlay_federation_ready",
            readiness_by_skill["cinder-change-protocol"],
        )
        self.assertEqual(
            "project_overlay_federation_ready",
            readiness_by_skill["cinder-source-of-truth-check"],
        )
        self.assertIn("project_overlay_federation_ready", markdown)

    def test_project_overlay_backlog_marks_eval_blocked_as_needs_evidence(self) -> None:
        repo_root = self.make_repo(
            scope="project",
            status="evaluated",
            review_surfaces=("status-promotions",),
        )

        build_catalog.write_governance_backlog(repo_root)

        payload = self.load_governance_backlog(repo_root)
        markdown = self.load_governance_backlog_markdown(repo_root)
        skill_entry = payload["skills"][0]

        self.assertFalse(skill_entry["canonical_candidate_ready"])
        self.assertFalse(skill_entry["canonical_eval_ready"])
        self.assertEqual(
            "project_overlay_needs_evidence",
            skill_entry["readiness_reconciliation"],
        )
        self.assertIn("project_overlay_needs_evidence", markdown)

    def test_skill_graph_includes_profile_and_artifact_group_edges(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_skill_graph(repo_root)

        payload = self.load_skill_graph(repo_root)
        node_types = {entry["type"] for entry in payload["nodes"]}
        edge_kinds = {entry["kind"] for entry in payload["edges"]}
        self.assertIn("profile", node_types)
        self.assertIn("artifact_group", node_types)
        self.assertIn("included_in_profile", edge_kinds)
        self.assertIn("available_in_artifact_group", edge_kinds)

    def test_write_overlay_readiness_generates_reviewable_family_surface(self) -> None:
        repo_root = self.make_repo()
        skill_names = [
            "cinder-change-protocol",
            "cinder-source-of-truth-check",
        ]
        family = "cinder"
        for skill_name in skill_names:
            self.add_skill_bundle(
                repo_root,
                skill_name=skill_name,
                scope="project",
                techniques=[PRIMARY_PUBLISHED_TECHNIQUE],
                policy_allow_implicit=True,
                include_review_check=True,
            )
        self.write_evaluation_fixtures_for_skills(repo_root, skill_names)
        self.write_live_overlay_pack(
            repo_root,
            family=family,
            skill_names=skill_names,
        )

        overlay_json_path, overlay_markdown_path = (
            build_catalog.write_overlay_readiness(repo_root)
        )

        payload = self.load_overlay_readiness(repo_root)
        markdown = self.load_overlay_readiness_markdown(repo_root)
        self.assertEqual(
            build_catalog.OVERLAY_READINESS_VERSION,
            payload["overlay_readiness_version"],
        )
        self.assertEqual(
            build_catalog.skill_overlay_contract.OVERLAY_READINESS_SOURCE_OF_TRUTH,
            payload["source_of_truth"],
        )
        self.assertEqual(
            repo_root / build_catalog.OVERLAY_READINESS_JSON_PATH,
            overlay_json_path,
        )
        self.assertEqual(
            repo_root / build_catalog.OVERLAY_READINESS_MARKDOWN_PATH,
            overlay_markdown_path,
        )
        self.assertEqual(
            {
                "live_overlay_family_count": 1,
                "reviewable_family_count": 1,
                "project_skill_count": 2,
                "project_skill_review_check_count": 2,
                "eval_ready_project_skill_count": 2,
            },
            payload["summary"],
        )
        self.assertEqual(1, len(payload["families"]))
        self.assertEqual(
            {
                "family": family,
                "project_overlay_path": f"mechanics/boundary-bridge/overlays/{family}/PROJECT_OVERLAY.md",
                "review_path": f"mechanics/boundary-bridge/overlays/{family}/REVIEW.md",
                "project_skill_names": skill_names,
                "listed_skill_names": skill_names,
                "listed_matches_actual": True,
                "project_skill_count": 2,
                "bundle_review_check_count": 2,
                "eval_ready_skill_count": 2,
                "boundary_statement_present": True,
                "repo_relative_statement_present": True,
                "authority_section_present": True,
                "review_mentions_all_skills": True,
                "readiness_state": "reviewable",
            },
            payload["families"][0],
        )
        self.assertEqual(
            skill_names,
            [entry["name"] for entry in payload["skills"]],
        )
        self.assertTrue(all(entry["eval_ready"] for entry in payload["skills"]))
        self.assertIn("# Overlay readiness", markdown)
        self.assertIn(
            "`reviewable` is the current mature exemplar target for a live project-overlay family in this repo.",
            markdown,
        )
        self.assertIn(
            "Use this surface for family maturity and `generated/governance_backlog.md` for per-skill maintenance readout.",
            markdown,
        )
        self.assertIn(
            f"| {family} | 2 | true | mechanics/boundary-bridge/overlays/{family}/REVIEW.md | 2 | 2 | true | true | reviewable |",
            markdown,
        )
        self.assertIn(
            "skills/cinder-change-protocol/checks/review.md",
            markdown,
        )

    def test_write_overlay_readiness_requires_authority_section_for_reviewable_family(
        self,
    ) -> None:
        repo_root = self.make_repo()
        skill_names = [
            "cinder-change-protocol",
            "cinder-source-of-truth-check",
        ]
        family = "cinder"
        for skill_name in skill_names:
            self.add_skill_bundle(
                repo_root,
                skill_name=skill_name,
                scope="project",
                techniques=[PRIMARY_PUBLISHED_TECHNIQUE],
                policy_allow_implicit=True,
                include_review_check=True,
            )
        self.write_evaluation_fixtures_for_skills(repo_root, skill_names)
        self.write_live_overlay_pack(
            repo_root,
            family=family,
            skill_names=skill_names,
            include_authority_section=False,
        )

        build_catalog.write_overlay_readiness(repo_root)

        payload = self.load_overlay_readiness(repo_root)
        self.assertEqual(0, payload["summary"]["reviewable_family_count"])
        self.assertFalse(payload["families"][0]["authority_section_present"])
        self.assertEqual("baseline", payload["families"][0]["readiness_state"])

    def test_write_overlay_readiness_keeps_docs_only_family_out_of_reviewable(
        self,
    ) -> None:
        repo_root = self.make_repo()
        self.write_live_overlay_pack(
            repo_root,
            family="cinder",
            skill_names=[],
            listed_skill_names=[],
        )

        build_catalog.write_overlay_readiness(repo_root)

        payload = self.load_overlay_readiness(repo_root)
        self.assertEqual(1, payload["summary"]["live_overlay_family_count"])
        self.assertEqual(0, payload["summary"]["reviewable_family_count"])
        self.assertEqual([], payload["families"][0]["project_skill_names"])
        self.assertFalse(payload["families"][0]["review_mentions_all_skills"])
        self.assertEqual("baseline", payload["families"][0]["readiness_state"])

    def test_write_overlay_readiness_discovers_synthetic_live_families_from_repo_state(
        self,
    ) -> None:
        repo_root = self.make_repo()
        families = {
            "cinder": [
                "cinder-change-protocol",
                "cinder-source-of-truth-check",
            ],
            "harbor": [
                "harbor-safe-infra-change",
                "harbor-sanitized-share",
            ],
        }
        all_skill_names = [
            skill_name
            for skill_names in families.values()
            for skill_name in skill_names
        ]
        for skill_name in all_skill_names:
            self.add_skill_bundle(
                repo_root,
                skill_name=skill_name,
                scope="project",
                techniques=[PRIMARY_PUBLISHED_TECHNIQUE],
                policy_allow_implicit=False,
                include_review_check=True,
            )
        self.write_evaluation_fixtures_for_skills(repo_root, all_skill_names)
        for family, skill_names in families.items():
            self.write_live_overlay_pack(
                repo_root,
                family=family,
                skill_names=skill_names,
            )

        build_catalog.write_overlay_readiness(repo_root)

        payload = self.load_overlay_readiness(repo_root)
        markdown = self.load_overlay_readiness_markdown(repo_root)
        self.assertEqual(
            {
                "live_overlay_family_count": 2,
                "reviewable_family_count": 2,
                "project_skill_count": 4,
                "project_skill_review_check_count": 4,
                "eval_ready_project_skill_count": 4,
            },
            payload["summary"],
        )
        readiness_by_family = {
            entry["family"]: entry["readiness_state"] for entry in payload["families"]
        }
        self.assertEqual(
            {
                "cinder": "reviewable",
                "harbor": "reviewable",
            },
            readiness_by_family,
        )
        self.assertCountEqual(
            all_skill_names,
            [entry["name"] for entry in payload["skills"]],
        )
        self.assertTrue(all(entry["eval_ready"] for entry in payload["skills"]))
        self.assertIn(
            "| cinder | 2 | true | mechanics/boundary-bridge/overlays/cinder/REVIEW.md | 2 | 2 | true | true | reviewable |",
            markdown,
        )
        self.assertIn(
            "| harbor | 2 | true | mechanics/boundary-bridge/overlays/harbor/REVIEW.md | 2 | 2 | true | true | reviewable |",
            markdown,
        )


if __name__ == "__main__":
    unittest.main()
