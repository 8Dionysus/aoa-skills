from __future__ import annotations

from tests.support.validate_skills_case import *


class ValidateSkillsReviewStatusTests(ValidateSkillsCase):
    def test_canonical_status_floor_validation_is_phase_split(self) -> None:
        self.assertTrue(hasattr(skill_status_surface, "validate_canonical_status_floors"))
        source = inspect.getsource(validate_skills.validate_canonical_status_floors)

        self.assertIn("skill_status_surface.validate_canonical_status_floors(", source)
        self.assertNotIn("derive_canonical_candidate_blockers", source)

    def test_single_technique_skill_without_exception_review_fails(self) -> None:
        repo_root = self.make_repo(include_composition_exception_review=False)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "single-technique skill requires a valid docs/reviews/skill-composition-exceptions/aoa-test-skill.md review record",
            messages,
        )

    def test_malformed_skill_composition_exception_review_fails(self) -> None:
        repo_root = self.make_repo(include_composition_exception_review=False)
        self.write_skill_composition_exception_review(
            repo_root,
            malformed=True,
        )
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "skill composition exception review missing required section 'Package rationale'",
            messages,
        )
        self.assertIn(
            "skill composition exception review top-level sections must match the canonical order exactly",
            messages,
        )

    def test_governance_lane_unknown_skill_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
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
                            "name": "aoa-ghost-skill",
                            "decision": "stay_evaluated",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#test_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "governance lane references unknown skill 'aoa-ghost-skill'",
            messages,
        )

    def test_governance_lane_overlay_skill_fails(self) -> None:
        repo_root = self.make_repo()
        self.write_skill_index(repo_root, ["aoa-test-skill", "atm10-test-skill"])
        self.add_skill_bundle(
            repo_root,
            skill_name="atm10-test-skill",
            scope="project",
            status="scaffold",
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
                            "name": "atm10-test-skill",
                            "decision": "stay_evaluated",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#test_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "governance lanes may only reference aoa-* public skills, not 'atm10-test-skill'",
            messages,
        )

    def test_governance_lane_missing_review_path_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
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
                    "review_path": "docs/governance/missing.md#test_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "governance lane review_path 'docs/governance/missing.md#test_lane' must reference an existing file",
            messages,
        )

    def test_governance_lane_absolute_review_path_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
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
                    "review_path": "/tmp/test_lane.md#test_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "governance lane review_path '/tmp/test_lane.md#test_lane' must be repo-relative",
            messages,
        )

    def test_governance_lane_missing_adjacency_case_id_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
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
                    "evidence_case_ids": ["missing_case"],
                }
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "governance lane evidence_case_id 'missing_case' must reference an existing adjacency case",
            messages,
        )

    def test_governance_lane_conflicting_decisions_fail(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_governance_lanes(
            repo_root,
            [
                {
                    "id": "lane_one",
                    "title": "Lane one",
                    "scope": "core",
                    "state": "comparative_pending",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "stay_evaluated",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#lane_one",
                    "evidence_case_ids": [],
                },
                {
                    "id": "lane_two",
                    "title": "Lane two",
                    "scope": "core",
                    "state": "stable_defaults",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "default_reference",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#lane_two",
                    "evidence_case_ids": [],
                },
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "skill 'aoa-test-skill' has conflicting governance decisions ('stay_evaluated' vs 'default_reference') across lanes",
            messages,
        )

    def test_governance_lane_duplicate_ids_fail(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_governance_lanes(
            repo_root,
            [
                {
                    "id": "shared_lane",
                    "title": "Lane one",
                    "scope": "core",
                    "state": "comparative_pending",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "stay_evaluated",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#shared_lane",
                    "evidence_case_ids": [],
                },
                {
                    "id": "shared_lane",
                    "title": "Lane two",
                    "scope": "core",
                    "state": "comparative_pending",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "stay_evaluated",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#shared_lane_two",
                    "evidence_case_ids": [],
                },
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "governance lane id 'shared_lane' must be unique",
            messages,
        )

    def test_governance_lane_decision_status_mismatch_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_governance_lanes(
            repo_root,
            [
                {
                    "id": "test_lane",
                    "title": "Test lane",
                    "scope": "core",
                    "state": "stable_defaults",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "default_reference",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#test_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "skill 'aoa-test-skill' uses decision 'default_reference' but is not currently 'canonical'",
            messages,
        )

    def test_governance_lane_missing_coverage_for_evaluated_skill_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_governance_lanes(repo_root, [])

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "skill 'aoa-test-skill' with status 'evaluated' requires governance lane coverage",
            messages,
        )

    def test_reviewed_status_requires_review_evidence(self) -> None:
        repo_root = self.make_repo(status="reviewed")
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "status 'reviewed' requires review evidence via checks/review.md or a public review record",
            messages,
        )

    def test_reviewed_status_passes_with_in_bundle_review_check(self) -> None:
        repo_root = self.make_repo(status="reviewed")
        review_check = repo_root / "skills" / "aoa-test-skill" / "checks" / "review.md"
        review_check.parent.mkdir(parents=True, exist_ok=True)
        review_check.write_text(
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
        self.write_catalogs(repo_root)
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_reviewed_status_passes_with_status_promotion_review_record(self) -> None:
        repo_root = self.make_repo(
            status="reviewed",
            review_record_surface="status-promotions",
        )
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_review_truth_sync_can_be_strictly_validated(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)
        review_path = (
            repo_root / "docs" / "reviews" / "status-promotions" / "aoa-test-skill.md"
        )
        review_path.write_text(
            textwrap.dedent(
                f"""\
                ---
                name: aoa-test-skill
                ---

                # aoa-test-skill status promotion review

                ## Current status

                - current maturity status: evaluated
                - current machine-checkable floor: pass
                - current governance lane decision: stay_evaluated
                - scope: core
                - current lineage: published
                - reviewed revision: placeholder

                ## Target status

                - target maturity status: evaluated
                - machine-checkable floor result: pass
                - recorded governance outcome: stay_evaluated

                ## Evidence reviewed

                - `skills/aoa-test-skill/SKILL.md`

                ## Findings

                - runtime skill.md meaning changed: no

                ## Gaps and blockers

                - blockers for this target status: none
                - blockers for the next status step: none

                ## Recommendation

                Stay evaluated.
                """
            ),
            encoding="utf-8",
        )

        first_pass = validate_skills.run_validation(
            repo_root,
            fail_on_review_truth_sync=True,
        )
        mismatch_issue = next(
            issue
            for issue in first_pass
            if issue.message.startswith("reviewed_revision_mismatch(expected=")
        )
        expected_revision = re.search(
            r"expected=([^,]+), recorded=",
            mismatch_issue.message,
        ).group(1)
        review_path.write_text(
            review_path.read_text(encoding="utf-8").replace(
                "- reviewed revision: placeholder",
                f"- reviewed revision: {expected_revision}",
            ),
            encoding="utf-8",
        )
        self.write_catalogs(repo_root)

        self.assertEqual(
            [],
            validate_skills.run_validation(
                repo_root,
                fail_on_review_truth_sync=True,
            ),
        )

    def test_project_overlay_review_truth_sync_accepts_not_applicable_governance(
        self,
    ) -> None:
        repo_root = self.make_repo(
            skill_name="abyss-test-skill",
            scope="project",
            status="evaluated",
            review_record_surface="status-promotions",
            policy_allow_implicit=True,
        )
        self.write_live_overlay_pack(
            repo_root,
            family="abyss",
            skill_names=["abyss-test-skill"],
        )
        self.write_evaluation_fixtures_for_skill(
            repo_root,
            skill_name="abyss-test-skill",
        )
        self.write_catalogs(repo_root)
        review_path = (
            repo_root / "docs" / "reviews" / "status-promotions" / "abyss-test-skill.md"
        )
        review_path.write_text(
            textwrap.dedent(
                """\
                ---
                name: abyss-test-skill
                ---

                # abyss-test-skill status promotion review

                ## Current status

                - current maturity status: evaluated
                - current machine-checkable floor: pass
                - current governance lane decision: not applicable
                - scope: project
                - current lineage: published
                - reviewed revision: placeholder

                ## Target status

                - target maturity status: evaluated
                - machine-checkable floor result: pass
                - recorded governance outcome: not applicable

                ## Evidence reviewed

                - `skills/abyss-test-skill/SKILL.md`

                ## Findings

                - runtime skill.md meaning changed: no

                ## Gaps and blockers

                - blockers for this target status: none
                - blockers for the next status step: overlay-model follow-up

                ## Recommendation

                Keep the overlay evaluated.
                """
            ),
            encoding="utf-8",
        )

        first_pass = validate_skills.run_validation(
            repo_root,
            fail_on_review_truth_sync=True,
        )
        mismatch_issue = next(
            issue
            for issue in first_pass
            if issue.message.startswith("reviewed_revision_mismatch(expected=")
        )
        expected_revision = re.search(
            r"expected=([^,]+), recorded=",
            mismatch_issue.message,
        ).group(1)
        review_path.write_text(
            review_path.read_text(encoding="utf-8").replace(
                "- reviewed revision: placeholder",
                f"- reviewed revision: {expected_revision}",
            ),
            encoding="utf-8",
        )
        self.write_catalogs(repo_root)

        self.assertEqual(
            [],
            validate_skills.run_validation(
                repo_root,
                fail_on_review_truth_sync=True,
            ),
        )

    def test_project_overlay_evaluated_status_does_not_require_candidate_adjacency_without_lane(
        self,
    ) -> None:
        repo_root = self.make_repo(
            skill_name="abyss-test-skill",
            scope="project",
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_live_overlay_pack(
            repo_root,
            family="abyss",
            skill_names=["abyss-test-skill"],
        )
        self.write_evaluation_fixtures_for_skill(
            repo_root,
            skill_name="abyss-test-skill",
        )
        self.write_catalogs(repo_root)

        self.assertEqual(
            [],
            validate_skills.validate_required_adjacency_coverage(
                repo_root, ["abyss-test-skill"]
            ),
        )

    def test_review_truth_sync_reports_malformed_review_doc_as_issue(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)
        review_path = (
            repo_root / "docs" / "reviews" / "status-promotions" / "aoa-test-skill.md"
        )
        review_path.write_text(
            textwrap.dedent(
                """\
                ---
                name: aoa-test-skill
                """
            ),
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(
            repo_root,
            fail_on_review_truth_sync=True,
        )
        malformed_issue = next(
            issue
            for issue in issues
            if issue.location == "docs/reviews/status-promotions/aoa-test-skill.md"
        )
        self.assertIn(
            "missing a closing frontmatter delimiter", malformed_issue.message
        )

    def test_review_truth_sync_revision_excludes_review_surface_files(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        review_path = (
            repo_root / "docs" / "reviews" / "status-promotions" / "aoa-test-skill.md"
        )
        revision_before = skill_review_surface.current_bundle_revision(
            repo_root,
            "aoa-test-skill",
        )
        review_path.write_text(
            "# aoa-test-skill status promotion review\n\n## Findings\n\n- changed.\n",
            encoding="utf-8",
        )
        revision_after = skill_review_surface.current_bundle_revision(
            repo_root,
            "aoa-test-skill",
        )
        self.assertEqual(revision_before, revision_after)

    def test_reviewed_status_passes_with_canonical_candidate_review_record(
        self,
    ) -> None:
        repo_root = self.make_repo(
            status="reviewed",
            review_record_surface="canonical-candidates",
        )
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_atm10_skill_passes(self) -> None:
        repo_root = self.make_repo(skill_name="atm10-perception-tests")
        self.assertEqual([], validate_skills.run_validation(repo_root))
        self.assertEqual(
            0, self.run_main(repo_root, ["--skill", "atm10-perception-tests"])
        )

    def test_abyss_skill_passes(self) -> None:
        repo_root = self.make_repo(skill_name="abyss-port-exposure-guard")
        self.assertEqual([], validate_skills.run_validation(repo_root))
        self.assertEqual(
            0,
            self.run_main(repo_root, ["--skill", "abyss-port-exposure-guard"]),
        )

    def test_mixed_family_index_passes(self) -> None:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-validator-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        (repo_root / "skills").mkdir()
        skill_names = [
            "aoa-test-skill",
            "atm10-perception-tests",
            "abyss-port-exposure-guard",
        ]
        self.write_skill_index(repo_root, skill_names)
        for skill_name in skill_names:
            self.add_skill_bundle(repo_root, skill_name=skill_name)
        self.write_catalogs(repo_root)

        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_live_overlay_pack_passes_for_allowed_family(self) -> None:
        repo_root = self.make_live_overlay_repo(
            overlay_specs=[
                {
                    "family": "atm10",
                    "skill_names": [
                        "atm10-change-protocol",
                        "atm10-source-of-truth-check",
                    ],
                    "skill_specs": [
                        {
                            "skill_name": "atm10-change-protocol",
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                        {
                            "skill_name": "atm10-source-of-truth-check",
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PENDING_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                            "notes": [PENDING_NOTE],
                        },
                    ],
                }
            ]
        )
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_live_overlay_contract_parity_passes_for_multiple_families(self) -> None:
        repo_root = self.make_live_overlay_repo(
            overlay_specs=[
                {
                    "family": "atm10",
                    "skill_names": [
                        "atm10-change-protocol",
                        "atm10-source-of-truth-check",
                    ],
                    "skill_specs": [
                        {
                            "skill_name": "atm10-change-protocol",
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                        {
                            "skill_name": "atm10-source-of-truth-check",
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                    ],
                },
                {
                    "family": "abyss",
                    "skill_names": [
                        "abyss-safe-infra-change",
                        "abyss-sanitized-share",
                    ],
                    "skill_specs": [
                        {
                            "skill_name": "abyss-safe-infra-change",
                            "scope": "project",
                            "invocation_mode": "explicit-only",
                            "status": "scaffold",
                            "policy_allow_implicit": False,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                        {
                            "skill_name": "abyss-sanitized-share",
                            "scope": "project",
                            "invocation_mode": "explicit-only",
                            "status": "scaffold",
                            "policy_allow_implicit": False,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                    ],
                },
            ]
        )
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_live_project_overlay_requires_repo_relative_language(self) -> None:
        family = "atm10"
        repo_root = self.make_live_overlay_repo(
            overlay_specs=[
                {
                    "family": family,
                    "skill_names": ["atm10-change-protocol"],
                    "repo_relative_language": False,
                    "skill_specs": [
                        {
                            "skill_name": "atm10-change-protocol",
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        }
                    ],
                }
            ]
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "live project overlay must explicitly keep paths or commands repository-relative",
            messages,
        )

    def test_live_project_overlay_requires_family_review_doc(self) -> None:
        family = "atm10"
        repo_root = self.make_live_overlay_repo(
            overlay_specs=[
                {
                    "family": family,
                    "skill_names": ["atm10-change-protocol"],
                    "include_review_doc": False,
                    "skill_specs": [
                        {
                            "skill_name": "atm10-change-protocol",
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        }
                    ],
                }
            ]
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            f"live overlay family '{family}' is missing mechanics/boundary-bridge/overlays/{family}/REVIEW.md",
            messages,
        )

    def test_live_project_overlay_requires_bundle_review_checklist(self) -> None:
        family = "atm10"
        missing_skill = "atm10-source-of-truth-check"
        repo_root = self.make_live_overlay_repo(
            overlay_specs=[
                {
                    "family": family,
                    "skill_names": [
                        "atm10-change-protocol",
                        missing_skill,
                    ],
                    "review_check_skill_names": ["atm10-change-protocol"],
                    "skill_specs": [
                        {
                            "skill_name": "atm10-change-protocol",
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                        {
                            "skill_name": missing_skill,
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                    ],
                }
            ]
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            f"live overlay family '{family}' requires skills/{missing_skill}/checks/review.md",
            messages,
        )

    def test_live_project_overlay_requires_listed_skill_parity(self) -> None:
        family = "abyss"
        missing_skill = "abyss-sanitized-share"
        repo_root = self.make_live_overlay_repo(
            overlay_specs=[
                {
                    "family": family,
                    "skill_names": [
                        "abyss-safe-infra-change",
                        missing_skill,
                    ],
                    "listed_skill_names": ["abyss-safe-infra-change"],
                    "skill_specs": [
                        {
                            "skill_name": "abyss-safe-infra-change",
                            "scope": "project",
                            "invocation_mode": "explicit-only",
                            "status": "scaffold",
                            "policy_allow_implicit": False,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                        {
                            "skill_name": missing_skill,
                            "scope": "project",
                            "invocation_mode": "explicit-only",
                            "status": "scaffold",
                            "policy_allow_implicit": False,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                    ],
                }
            ]
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            f"live project overlay '{family}' must list matching skill bundle(s): {missing_skill}",
            messages,
        )

    def test_mixed_family_index_duplicate_fails(self) -> None:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-validator-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        (repo_root / "skills").mkdir()
        skill_names = [
            "aoa-test-skill",
            "atm10-perception-tests",
            "abyss-port-exposure-guard",
            "atm10-perception-tests",
        ]
        self.write_skill_index(repo_root, skill_names)
        for skill_name in {
            "aoa-test-skill",
            "atm10-perception-tests",
            "abyss-port-exposure-guard",
        }:
            self.add_skill_bundle(repo_root, skill_name=skill_name)
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "skill 'atm10-perception-tests' appears 2 times in the index", messages
        )

    def test_invalid_review_checklist_headings_fail(self) -> None:
        repo_root = self.make_repo(include_support_artifact=False)
        review_path = repo_root / "skills" / "aoa-test-skill" / "checks" / "review.md"
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_text(
            textwrap.dedent(
                """\
                # Review Checklist

                ## Purpose

                Review purpose.

                ## Checklist

                - [ ] confirm scope
                """
            ),
            encoding="utf-8",
        )
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "review checklist missing required section 'When it applies'",
            messages,
        )
        self.assertIn(
            "review checklist top-level sections must match the canonical order exactly",
            messages,
        )


if __name__ == "__main__":
    unittest.main()
