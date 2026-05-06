from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class MechanicsTopologyTests(unittest.TestCase):
    def test_mechanics_root_and_packages_are_routable(self) -> None:
        expected_paths = (
            "config/README.md",
            "examples/README.md",
            "generated/README.md",
            "QUESTBOOK.md",
            "manifests/AGENTS.md",
            "manifests/README.md",
            "quests/AGENTS.md",
            "quests/README.md",
            "schemas/README.md",
            "mechanics/README.md",
            "mechanics/AGENTS.md",
            "mechanics/ARTIFACT_TOPOLOGY.md",
            "mechanics/ROADMAP.md",
            "mechanics/OWNER_REQUEST_RECEIPTS.md",
            "mechanics/method-growth/README.md",
            "mechanics/method-growth/AGENTS.md",
            "mechanics/method-growth/DIRECTION.md",
            "mechanics/method-growth/PARTS.md",
            "mechanics/method-growth/PROVENANCE.md",
            "mechanics/method-growth/LANDING_LOG.md",
            "mechanics/method-growth/ROADMAP.md",
            "mechanics/method-growth/docs/README.md",
            "mechanics/method-growth/docs/CANDIDATE_LINEAGE_CONTRACT.md",
            "mechanics/method-growth/docs/CANDIDATE_REF_REFINERY.md",
            "mechanics/method-growth/docs/OWNER_STATUS_SURFACES.md",
            "mechanics/method-growth/docs/GOVERNED_FOLLOWTHROUGH.md",
            "mechanics/method-growth/examples/README.md",
            "mechanics/method-growth/parts/adoption-boundary/README.md",
            "mechanics/method-growth/parts/adoption-evidence-receipts/README.md",
            "mechanics/method-growth/parts/retention-regression-retirement/README.md",
            "mechanics/method-growth/parts/pattern-adoption-handoff/README.md",
            "mechanics/method-growth/legacy/README.md",
            "mechanics/method-growth/legacy/adoption-wave/INDEX.md",
            "mechanics/method-growth/legacy/adoption-wave/DISTILLATION_LOG.md",
            "mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_COMPATIBILITY.md",
            "mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_RECEIPTS.md",
            "mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_REGRESSION.md",
            "mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_RETIREMENT.md",
            "mechanics/method-growth/legacy/adoption-wave/raw/SKILL_PATTERN_ADOPTION.md",
            "mechanics/growth-cycle/README.md",
            "mechanics/growth-cycle/AGENTS.md",
            "mechanics/growth-cycle/DIRECTION.md",
            "mechanics/growth-cycle/PARTS.md",
            "mechanics/growth-cycle/PROVENANCE.md",
            "mechanics/growth-cycle/LANDING_LOG.md",
            "mechanics/growth-cycle/ROADMAP.md",
            "mechanics/growth-cycle/docs/README.md",
            "mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md",
            "mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md",
            "mechanics/growth-cycle/examples/README.md",
            "mechanics/questbook/README.md",
            "mechanics/questbook/AGENTS.md",
            "mechanics/questbook/DIRECTION.md",
            "mechanics/questbook/PARTS.md",
            "mechanics/questbook/PROVENANCE.md",
            "mechanics/questbook/LANDING_LOG.md",
            "mechanics/questbook/ROADMAP.md",
            "mechanics/questbook/docs/README.md",
            "mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md",
            "mechanics/recurrence/README.md",
            "mechanics/recurrence/AGENTS.md",
            "mechanics/recurrence/DIRECTION.md",
            "mechanics/recurrence/PARTS.md",
            "mechanics/recurrence/PROVENANCE.md",
            "mechanics/recurrence/LANDING_LOG.md",
            "mechanics/recurrence/ROADMAP.md",
            "mechanics/recurrence/parts/live-observation-producers/README.md",
            "mechanics/recurrence/parts/review-decision-closure/README.md",
            "mechanics/recurrence/manifests/README.md",
            "mechanics/antifragility/README.md",
            "mechanics/antifragility/AGENTS.md",
            "mechanics/antifragility/DIRECTION.md",
            "mechanics/antifragility/PARTS.md",
            "mechanics/antifragility/PROVENANCE.md",
            "mechanics/antifragility/LANDING_LOG.md",
            "mechanics/antifragility/ROADMAP.md",
            "mechanics/antifragility/parts/fallback-authoring-posture/README.md",
            "mechanics/antifragility/parts/via-negativa-pruning/README.md",
            "mechanics/antifragility/parts/collision-stress-program/README.md",
            "mechanics/rpg/README.md",
            "mechanics/rpg/AGENTS.md",
            "mechanics/rpg/DIRECTION.md",
            "mechanics/rpg/PARTS.md",
            "mechanics/rpg/PROVENANCE.md",
            "mechanics/rpg/LANDING_LOG.md",
            "mechanics/rpg/ROADMAP.md",
            "mechanics/rpg/parts/ability-reader-boundary/README.md",
            "mechanics/rpg/parts/loadout-posture/README.md",
            "mechanics/checkpoint/README.md",
            "mechanics/checkpoint/AGENTS.md",
            "mechanics/checkpoint/DIRECTION.md",
            "mechanics/checkpoint/PARTS.md",
            "mechanics/checkpoint/PROVENANCE.md",
            "mechanics/checkpoint/LANDING_LOG.md",
            "mechanics/checkpoint/ROADMAP.md",
            "mechanics/checkpoint/docs/README.md",
            "mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md",
            "mechanics/checkpoint/examples/README.md",
            "mechanics/agon/README.md",
            "mechanics/agon/AGENTS.md",
            "mechanics/agon/DIRECTION.md",
            "mechanics/agon/PARTS.md",
            "mechanics/agon/PROVENANCE.md",
            "mechanics/agon/LANDING_LOG.md",
            "mechanics/agon/ROADMAP.md",
            "mechanics/agon/legacy/README.md",
            "mechanics/agon/legacy/INDEX.md",
            "mechanics/agon/legacy/DISTILLATION_LOG.md",
            "mechanics/agon/legacy/raw/README.md",
            "mechanics/agon/examples/README.md",
            "mechanics/agon/parts/workflow-candidate-bridge/config/README.md",
            "mechanics/agon/parts/workflow-candidate-bridge/schemas/agon-skill-binding-candidate.schema.json",
            "mechanics/agon/parts/workflow-candidate-bridge/scripts/build_agon_skill_binding_candidates.py",
            "mechanics/agon/parts/workflow-candidate-bridge/scripts/validate_agon_skill_binding_candidates.py",
            "mechanics/agon/parts/workflow-candidate-bridge/tests/test_agon_skill_binding_candidates.py",
            "mechanics/agon/parts/workflow-candidate-bridge/examples/agon_skill_binding_candidate.example.json",
            "mechanics/agon/parts/epistemic-candidate-boundary/config/README.md",
            "mechanics/agon/parts/epistemic-candidate-boundary/schemas/agon-epistemic-skill-candidate.schema.json",
            "mechanics/agon/parts/epistemic-candidate-boundary/schemas/agon-epistemic-skill-candidate-registry.schema.json",
            "mechanics/agon/parts/epistemic-candidate-boundary/scripts/build_agon_epistemic_skill_candidates.py",
            "mechanics/agon/parts/epistemic-candidate-boundary/scripts/validate_agon_epistemic_skill_candidates.py",
            "mechanics/agon/parts/epistemic-candidate-boundary/tests/test_agon_epistemic_skill_candidates.py",
            "mechanics/agon/parts/epistemic-candidate-boundary/examples/agon_epistemic_skill_candidate.example.json",
            "mechanics/agon/parts/recurrence-observation/manifests/README.md",
            "mechanics/audit/README.md",
            "mechanics/audit/AGENTS.md",
            "mechanics/audit/DIRECTION.md",
            "mechanics/audit/PARTS.md",
            "mechanics/audit/PROVENANCE.md",
            "mechanics/audit/LANDING_LOG.md",
            "mechanics/audit/ROADMAP.md",
            "mechanics/audit/docs/README.md",
            "mechanics/audit/docs/AUDIT_CONTRACT.md",
            "mechanics/audit/docs/EVALUATION_PATH.md",
            "mechanics/audit/docs/PUBLIC_SURFACE.md",
            "mechanics/audit/docs/TRIGGER_EVALS.md",
            "mechanics/audit/docs/DESCRIPTION_TRIGGER_EVALS.md",
            "mechanics/audit/docs/SKILLS_REF_VALIDATION.md",
            "mechanics/experience/README.md",
            "mechanics/experience/AGENTS.md",
            "mechanics/experience/DIRECTION.md",
            "mechanics/experience/PARTS.md",
            "mechanics/experience/PROVENANCE.md",
            "mechanics/experience/LANDING_LOG.md",
            "mechanics/experience/ROADMAP.md",
            "mechanics/experience/docs/README.md",
            "mechanics/experience/examples/README.md",
            "mechanics/boundary-bridge/README.md",
            "mechanics/boundary-bridge/AGENTS.md",
            "mechanics/boundary-bridge/DIRECTION.md",
            "mechanics/boundary-bridge/PARTS.md",
            "mechanics/boundary-bridge/PROVENANCE.md",
            "mechanics/boundary-bridge/LANDING_LOG.md",
            "mechanics/boundary-bridge/ROADMAP.md",
            "mechanics/boundary-bridge/docs/README.md",
            "mechanics/boundary-bridge/docs/LAYER_POSITION.md",
            "mechanics/boundary-bridge/docs/BRIDGE_SPEC.md",
            "mechanics/boundary-bridge/docs/OVERLAY_SPEC.md",
            "mechanics/boundary-bridge/examples/README.md",
            "mechanics/boundary-bridge/overlays/AGENTS.md",
            "mechanics/release-support/README.md",
            "mechanics/release-support/AGENTS.md",
            "mechanics/release-support/DIRECTION.md",
            "mechanics/release-support/PARTS.md",
            "mechanics/release-support/PROVENANCE.md",
            "mechanics/release-support/LANDING_LOG.md",
            "mechanics/release-support/ROADMAP.md",
            "mechanics/release-support/docs/README.md",
            "mechanics/release-support/docs/RUNTIME_PATH.md",
            "mechanics/release-support/docs/CODEX_PORTABLE_LAYER.md",
            "mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md",
            "mechanics/release-support/docs/RELEASING.md",
            "mechanics/release-support/examples/README.md",
            "mechanics/release-support/legacy/waves/README.md",
        )
        for relative_path in expected_paths:
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

    def test_root_companion_districts_do_not_keep_mechanic_records(self) -> None:
        route_only_files = ["AGENTS.md", "README.md"]

        for root_district in ("examples", "manifests"):
            with self.subTest(root_district=root_district):
                files = sorted(
                    str(path.relative_to(REPO_ROOT / root_district))
                    for path in (REPO_ROOT / root_district).rglob("*")
                    if path.is_file()
                )
                self.assertEqual(route_only_files, files)

        config_files = {path.name for path in (REPO_ROOT / "config").iterdir()}
        for moved_seed in (
            "agon_skill_binding_candidates.seed.json",
            "agon_epistemic_skill_candidates.seed.json",
        ):
            with self.subTest(moved_seed=moved_seed):
                self.assertNotIn(moved_seed, config_files)

        root_schemas = {path.name for path in (REPO_ROOT / "schemas").iterdir()}
        for moved_schema in (
            "agon-skill-binding-candidate.schema.json",
            "agon-epistemic-skill-candidate.schema.json",
            "agon-epistemic-skill-candidate-registry.schema.json",
            "session_checkpoint_note.schema.json",
            "reviewed_owner_landing_bundle.schema.json",
            "route_followthrough_decision.schema.json",
            "skill_adoption_compatibility_report_v1.json",
            "skill_adoption_owner_decision_v1.json",
            "skill_adoption_receipt_v1.json",
            "skill_adoption_regression_case_v1.json",
            "skill_adoption_retirement_v1.json",
            "skill_pattern_adoption_patch_v1.json",
            "governance_runtime_skill_invocation_v1.json",
            "installation_skill_invocation_v1.json",
            "office_task_skill_boundary_v1.json",
            "receipt_generation_skill_patch_v1.json",
            "rollback_drill_skill_invocation_v1.json",
            "service_handoff_skill_patch_v1.json",
            "skill_governance_patch_v1.json",
            "skill_policy_hold_v1.json",
            "quest.schema.json",
            "quest_dispatch.schema.json",
        ):
            with self.subTest(moved_schema=moved_schema):
                self.assertNotIn(moved_schema, root_schemas)

        root_scripts = {path.name for path in (REPO_ROOT / "scripts").iterdir()}
        for moved_script in (
            "build_agon_skill_binding_candidates.py",
            "validate_agon_skill_binding_candidates.py",
            "build_agon_epistemic_skill_candidates.py",
            "validate_agon_epistemic_skill_candidates.py",
        ):
            with self.subTest(moved_script=moved_script):
                self.assertNotIn(moved_script, root_scripts)

        root_tests = {path.name for path in (REPO_ROOT / "tests").iterdir()}
        for moved_test in (
            "test_agon_skill_binding_candidates.py",
            "test_agon_epistemic_skill_candidates.py",
        ):
            with self.subTest(moved_test=moved_test):
                self.assertNotIn(moved_test, root_tests)

        top_level_quest_files = sorted(
            path.name for path in (REPO_ROOT / "quests").iterdir() if path.is_file()
        )
        self.assertEqual(route_only_files, top_level_quest_files)

        for flat_quest in (
            "AOA-SK-Q-0001.yaml",
            "AOA-SK-Q-0002.yaml",
            "AOA-SK-Q-0003.yaml",
            "AOA-SK-Q-0004.yaml",
            "AOA-SK-Q-0005.yaml",
            "AOA-SK-Q-0006.yaml",
            "AOA-SK-Q-0007.yaml",
            "AOA-SK-Q-0008.yaml",
            "AOS-Q-AGON-0001-skill-binding-candidates.md",
            "AOS-Q-AGON-0002-epistemic-skill-candidates.md",
        ):
            with self.subTest(flat_quest=flat_quest):
                self.assertFalse((REPO_ROOT / "quests" / flat_quest).exists())

    def test_owner_request_receipts_keep_center_statuses_honest(self) -> None:
        receipts = (REPO_ROOT / "mechanics" / "OWNER_REQUEST_RECEIPTS.md").read_text(
            encoding="utf-8"
        )
        mechanics_readme = (REPO_ROOT / "mechanics" / "README.md").read_text(
            encoding="utf-8"
        )

        expected_statuses = {
            "ORQ-METHOD-SKILLS-001": "landed",
            "ORQ-DISTILLATION-SKILLS-001": "accepted",
            "ORQ-GROWTHCYCLE-SKILLS-001": "landed",
            "ORQ-CHECKPOINT-SKILLS-001": "landed",
            "ORQ-EXPERIENCE-SKILLS-001": "accepted",
            "ORQ-RPG-SKILLS-001": "landed",
            "ORQ-AUDIT-SKILLS-001": "accepted",
        }
        for request_id, status in expected_statuses.items():
            with self.subTest(request_id=request_id):
                self.assertIn(f"## {request_id}", receipts)
                self.assertIn(f"Owner-local status: `{status}`", receipts)

        for phrase in (
            "This is the owner-local receipt surface",
            "do not treat `accepted` as `landed`",
            "do not treat `landed` as proof",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, receipts)

        self.assertIn("OWNER_REQUEST_RECEIPTS.md", mechanics_readme)

    def test_mechanics_card_standard_is_declared(self) -> None:
        mechanics_readme = (REPO_ROOT / "mechanics" / "README.md").read_text(
            encoding="utf-8"
        )
        agon_readme = (REPO_ROOT / "mechanics" / "agon" / "README.md").read_text(
            encoding="utf-8"
        )
        method_growth_readme = (
            REPO_ROOT / "mechanics" / "method-growth" / "README.md"
        ).read_text(encoding="utf-8")
        growth_cycle_readme = (
            REPO_ROOT / "mechanics" / "growth-cycle" / "README.md"
        ).read_text(encoding="utf-8")
        checkpoint_readme = (
            REPO_ROOT / "mechanics" / "checkpoint" / "README.md"
        ).read_text(encoding="utf-8")
        questbook_readme = (
            REPO_ROOT / "mechanics" / "questbook" / "README.md"
        ).read_text(encoding="utf-8")
        recurrence_readme = (
            REPO_ROOT / "mechanics" / "recurrence" / "README.md"
        ).read_text(encoding="utf-8")
        antifragility_readme = (
            REPO_ROOT / "mechanics" / "antifragility" / "README.md"
        ).read_text(encoding="utf-8")
        rpg_readme = (REPO_ROOT / "mechanics" / "rpg" / "README.md").read_text(
            encoding="utf-8"
        )
        for heading in (
            "## Mechanic card",
            "### Trigger",
            "### Local owns",
            "### Stronger owner split",
            "### Inputs",
            "### Outputs",
            "### Must not claim",
            "### Validation",
            "### Next route",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, mechanics_readme)
                self.assertIn(heading, agon_readme)
                self.assertIn(heading, method_growth_readme)
                self.assertIn(heading, growth_cycle_readme)
                self.assertIn(heading, checkpoint_readme)
                self.assertIn(heading, questbook_readme)
                self.assertIn(heading, recurrence_readme)
                self.assertIn(heading, antifragility_readme)
                self.assertIn(heading, rpg_readme)

    def test_method_growth_lineage_surfaces_moved_out_of_flat_docs(self) -> None:
        moved_paths = (
            "docs/CANDIDATE_LINEAGE_CONTRACT.md",
            "docs/CANDIDATE_REF_REFINERY.md",
            "docs/OWNER_STATUS_SURFACES.md",
            "docs/GOVERNED_FOLLOWTHROUGH.md",
        )
        for relative_path in moved_paths:
            with self.subTest(path=relative_path):
                self.assertFalse((REPO_ROOT / relative_path).exists())

        active_docs = (
            "mechanics/method-growth/docs/CANDIDATE_LINEAGE_CONTRACT.md",
            "mechanics/method-growth/docs/CANDIDATE_REF_REFINERY.md",
            "mechanics/method-growth/docs/OWNER_STATUS_SURFACES.md",
            "mechanics/method-growth/docs/GOVERNED_FOLLOWTHROUGH.md",
        )
        for relative_path in active_docs:
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

        active_parts = (
            "mechanics/method-growth/parts/candidate-lineage/README.md",
            "mechanics/method-growth/parts/owner-status-landing/README.md",
            "mechanics/method-growth/parts/governed-followthrough/README.md",
            "mechanics/method-growth/parts/adoption-boundary/README.md",
            "mechanics/method-growth/parts/adoption-evidence-receipts/README.md",
            "mechanics/method-growth/parts/retention-regression-retirement/README.md",
            "mechanics/method-growth/parts/pattern-adoption-handoff/README.md",
        )
        for relative_path in active_parts:
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

    def test_method_growth_provenance_accounts_for_moved_docs(self) -> None:
        provenance = (
            REPO_ROOT / "mechanics" / "method-growth" / "PROVENANCE.md"
        ).read_text(encoding="utf-8")

        for source_name in (
            "CANDIDATE_LINEAGE_CONTRACT.md",
            "CANDIDATE_REF_REFINERY.md",
            "OWNER_STATUS_SURFACES.md",
            "GOVERNED_FOLLOWTHROUGH.md",
        ):
            with self.subTest(source_name=source_name):
                self.assertIn(f"docs/{source_name}", provenance)
                self.assertIn(f"mechanics/method-growth/docs/{source_name}", provenance)

        self.assertIn("skills/core/session-growth/aoa-session-donor-harvest/SKILL.md", provenance)
        self.assertIn(
            "mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md",
            provenance,
        )
        self.assertIn("mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md", provenance)

    def test_method_growth_adoption_surfaces_moved_out_of_flat_docs(self) -> None:
        moved_paths = (
            "docs/SKILL_ADOPTION_COMPATIBILITY.md",
            "docs/SKILL_ADOPTION_RECEIPTS.md",
            "docs/SKILL_ADOPTION_REGRESSION.md",
            "docs/SKILL_ADOPTION_RETIREMENT.md",
            "docs/SKILL_PATTERN_ADOPTION.md",
        )
        for relative_path in moved_paths:
            with self.subTest(path=relative_path):
                self.assertFalse((REPO_ROOT / relative_path).exists())

        raw_paths = (
            "mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_COMPATIBILITY.md",
            "mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_RECEIPTS.md",
            "mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_REGRESSION.md",
            "mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_RETIREMENT.md",
            "mechanics/method-growth/legacy/adoption-wave/raw/SKILL_PATTERN_ADOPTION.md",
        )
        for relative_path in raw_paths:
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

        self.assertTrue(
            (
                REPO_ROOT
                / "mechanics"
                / "experience"
                / "docs"
                / "GOVERNANCE_SKILL_ADOPTION.md"
            ).is_file()
        )

    def test_method_growth_adoption_provenance_accounts_for_raw_sources(self) -> None:
        provenance = (
            REPO_ROOT / "mechanics" / "method-growth" / "PROVENANCE.md"
        ).read_text(encoding="utf-8")
        index = (
            REPO_ROOT
            / "mechanics"
            / "method-growth"
            / "legacy"
            / "adoption-wave"
            / "INDEX.md"
        ).read_text(encoding="utf-8")

        for source_name in (
            "SKILL_ADOPTION_COMPATIBILITY.md",
            "SKILL_ADOPTION_RECEIPTS.md",
            "SKILL_ADOPTION_REGRESSION.md",
            "SKILL_ADOPTION_RETIREMENT.md",
            "SKILL_PATTERN_ADOPTION.md",
        ):
            with self.subTest(source_name=source_name):
                self.assertIn(f"docs/{source_name}", provenance)
                self.assertIn(f"raw/{source_name}", index)

        for active_part in (
            "parts/adoption-boundary/README.md",
            "parts/adoption-evidence-receipts/README.md",
            "parts/retention-regression-retirement/README.md",
            "parts/pattern-adoption-handoff/README.md",
        ):
            with self.subTest(active_part=active_part):
                self.assertIn(active_part, provenance)
                self.assertIn(active_part, index)

        self.assertIn("mechanics/experience/docs/GOVERNANCE_SKILL_ADOPTION.md", provenance)

    def test_growth_cycle_surfaces_moved_out_of_flat_docs(self) -> None:
        moved_paths = (
            "docs/ADAPTIVE_SKILL_ORCHESTRATION.md",
            "docs/SESSION_GROWTH_KERNEL_MATURITY.md",
        )
        for relative_path in moved_paths:
            with self.subTest(path=relative_path):
                self.assertFalse((REPO_ROOT / relative_path).exists())

        active_paths = (
            "mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md",
            "mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md",
            "mechanics/growth-cycle/parts/adaptive-orchestration/README.md",
            "mechanics/growth-cycle/parts/session-kernel-maturity/README.md",
            "mechanics/growth-cycle/parts/harvest-note-boundary/README.md",
        )
        for relative_path in active_paths:
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

    def test_growth_cycle_provenance_accounts_for_moved_docs(self) -> None:
        provenance = (
            REPO_ROOT / "mechanics" / "growth-cycle" / "PROVENANCE.md"
        ).read_text(encoding="utf-8")

        for source_name in (
            "ADAPTIVE_SKILL_ORCHESTRATION.md",
            "SESSION_GROWTH_KERNEL_MATURITY.md",
        ):
            with self.subTest(source_name=source_name):
                self.assertIn(f"docs/{source_name}", provenance)
                self.assertIn(f"mechanics/growth-cycle/docs/{source_name}", provenance)

        self.assertIn("docs/session-harvests/", provenance)
        self.assertIn(
            "mechanics/recurrence/manifests/component.skills.bundle-and-activation-beacons.json",
            provenance,
        )

    def test_checkpoint_note_surface_moved_out_of_flat_docs(self) -> None:
        self.assertFalse((REPO_ROOT / "docs" / "CHECKPOINT_NOTE_PATH.md").exists())

        active_paths = (
            "mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md",
            "mechanics/checkpoint/parts/checkpoint-note-lane/README.md",
            "mechanics/checkpoint/parts/closeout-bridge-boundary/README.md",
        )
        for relative_path in active_paths:
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

    def test_checkpoint_provenance_accounts_for_moved_doc(self) -> None:
        provenance = (
            REPO_ROOT / "mechanics" / "checkpoint" / "PROVENANCE.md"
        ).read_text(encoding="utf-8")

        self.assertIn("docs/CHECKPOINT_NOTE_PATH.md", provenance)
        self.assertIn("mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md", provenance)
        self.assertIn("skills/core/session-growth/aoa-checkpoint-closeout-bridge/SKILL.md", provenance)
        self.assertIn("mechanics/checkpoint/schemas/session_checkpoint_note.schema.json", provenance)
        self.assertIn(
            "mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md",
            provenance,
        )

    def test_questbook_integration_surface_moved_out_of_flat_docs(self) -> None:
        self.assertFalse(
            (REPO_ROOT / "docs" / "QUESTBOOK_SKILL_INTEGRATION.md").exists()
        )

        active_paths = (
            "mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md",
            "mechanics/questbook/parts/source-index-boundary/README.md",
            "mechanics/questbook/parts/session-harvest-posture/README.md",
            "mechanics/questbook/parts/dispatch-projection/README.md",
        )
        for relative_path in active_paths:
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

        self.assertTrue((REPO_ROOT / "QUESTBOOK.md").is_file())
        self.assertFalse((REPO_ROOT / "mechanics/questbook/QUESTBOOK.md").exists())
        self.assertTrue((REPO_ROOT / "quests").is_dir())

    def test_questbook_provenance_accounts_for_moved_doc(self) -> None:
        provenance = (
            REPO_ROOT / "mechanics" / "questbook" / "PROVENANCE.md"
        ).read_text(encoding="utf-8")

        self.assertIn("docs/QUESTBOOK_SKILL_INTEGRATION.md", provenance)
        self.assertIn(
            "mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md",
            provenance,
        )
        self.assertIn("QUESTBOOK.md", provenance)
        self.assertIn("quests/**/AOA-SK-Q-*.yaml", provenance)
        self.assertIn("generated/quest_catalog.min.json", provenance)
        self.assertIn("skills/core/session-growth/aoa-quest-harvest/SKILL.md", provenance)

    def test_recurrence_surfaces_moved_out_of_flat_docs(self) -> None:
        moved_paths = (
            "docs/RECURRENCE_LIVE_OBSERVATION_PRODUCERS.md",
            "docs/RECURRENCE_REVIEW_DECISION_CLOSURE.md",
        )
        for relative_path in moved_paths:
            with self.subTest(path=relative_path):
                self.assertFalse((REPO_ROOT / relative_path).exists())

        active_paths = (
            "mechanics/recurrence/parts/live-observation-producers/README.md",
            "mechanics/recurrence/parts/review-decision-closure/README.md",
        )
        for relative_path in active_paths:
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

    def test_recurrence_provenance_accounts_for_moved_docs(self) -> None:
        provenance = (
            REPO_ROOT / "mechanics" / "recurrence" / "PROVENANCE.md"
        ).read_text(encoding="utf-8")

        self.assertIn("docs/RECURRENCE_LIVE_OBSERVATION_PRODUCERS.md", provenance)
        self.assertIn("docs/RECURRENCE_REVIEW_DECISION_CLOSURE.md", provenance)
        self.assertIn(
            "mechanics/recurrence/parts/live-observation-producers/README.md",
            provenance,
        )
        self.assertIn(
            "mechanics/recurrence/parts/review-decision-closure/README.md",
            provenance,
        )
        self.assertIn(
            "mechanics/recurrence/manifests/component.skills.bundle-and-activation-beacons.json",
            provenance,
        )
        self.assertIn(
            "mechanics/agon/parts/recurrence-observation/README.md",
            provenance,
        )

    def test_rpg_reader_surfaces_moved_out_of_flat_docs(self) -> None:
        moved_paths = (
            "docs/SKILL_ABILITY_MODEL.md",
            "docs/ABILITY_LOADOUT_POSTURE.md",
        )
        for relative_path in moved_paths:
            with self.subTest(path=relative_path):
                self.assertFalse((REPO_ROOT / relative_path).exists())

        active_paths = (
            "mechanics/rpg/parts/ability-reader-boundary/README.md",
            "mechanics/rpg/parts/loadout-posture/README.md",
        )
        for relative_path in active_paths:
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

    def test_rpg_provenance_accounts_for_moved_docs(self) -> None:
        provenance = (REPO_ROOT / "mechanics" / "rpg" / "PROVENANCE.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/SKILL_ABILITY_MODEL.md", provenance)
        self.assertIn("docs/ABILITY_LOADOUT_POSTURE.md", provenance)
        self.assertIn(
            "mechanics/rpg/parts/ability-reader-boundary/README.md",
            provenance,
        )
        self.assertIn("mechanics/rpg/parts/loadout-posture/README.md", provenance)
        self.assertIn("generated/skill_ability_cards.min.example.json", provenance)
        self.assertIn("schemas/skill_ability_catalog.schema.json", provenance)

    def test_antifragility_surfaces_moved_out_of_flat_docs(self) -> None:
        moved_paths = (
            "docs/ANTIFRAGILITY_SKILL_ADDENDUM.md",
            "docs/VIA_NEGATIVA_CHECKLIST.md",
            "docs/SKILL_COLLISION_CHAOS_WAVE1.md",
        )
        for relative_path in moved_paths:
            with self.subTest(path=relative_path):
                self.assertFalse((REPO_ROOT / relative_path).exists())

        active_paths = (
            "mechanics/antifragility/parts/fallback-authoring-posture/README.md",
            "mechanics/antifragility/parts/via-negativa-pruning/README.md",
            "mechanics/antifragility/parts/collision-stress-program/README.md",
        )
        for relative_path in active_paths:
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

        self.assertTrue(
            (
                REPO_ROOT
                / "mechanics"
                / "experience"
                / "docs"
                / "ROLLBACK_DRILL_SKILL.md"
            ).is_file()
        )

    def test_antifragility_provenance_accounts_for_moved_docs(self) -> None:
        provenance = (
            REPO_ROOT / "mechanics" / "antifragility" / "PROVENANCE.md"
        ).read_text(encoding="utf-8")

        for source_name in (
            "ANTIFRAGILITY_SKILL_ADDENDUM.md",
            "VIA_NEGATIVA_CHECKLIST.md",
            "SKILL_COLLISION_CHAOS_WAVE1.md",
        ):
            with self.subTest(source_name=source_name):
                self.assertIn(f"docs/{source_name}", provenance)

        self.assertIn(
            "mechanics/antifragility/parts/fallback-authoring-posture/README.md",
            provenance,
        )
        self.assertIn(
            "mechanics/antifragility/parts/via-negativa-pruning/README.md",
            provenance,
        )
        self.assertIn(
            "mechanics/antifragility/parts/collision-stress-program/README.md",
            provenance,
        )
        self.assertIn("mechanics/experience/docs/ROLLBACK_DRILL_SKILL.md", provenance)
        self.assertIn("generated/skill_trigger_collision_matrix.json", provenance)
        self.assertIn("config/project_risk_guard_ring.json", provenance)

    def test_agon_flat_docs_surfaces_moved_to_parts(self) -> None:
        moved_paths = (
            "docs/AGON_MOVE_SKILL_BRIDGE.md",
            "docs/AGON_WAVE4_SKILL_LANDING.md",
            "docs/AGON_RECURRENCE_ADAPTER.md",
            "docs/AGON_WAVE15_SKILLS_LANDING.md",
            "docs/AGON_EPISTEMIC_WORKFLOW_BOUNDARY.md",
            "docs/AGON_EPISTEMIC_SKILL_CANDIDATES.md",
        )
        for relative_path in moved_paths:
            with self.subTest(path=relative_path):
                self.assertFalse((REPO_ROOT / relative_path).exists())

        legacy_snapshots = (
            "mechanics/agon/legacy/raw/AGON_MOVE_SKILL_BRIDGE.md",
            "mechanics/agon/legacy/raw/AGON_WAVE4_SKILL_LANDING.md",
            "mechanics/agon/legacy/raw/AGON_RECURRENCE_ADAPTER.md",
            "mechanics/agon/legacy/raw/AGON_WAVE15_SKILLS_LANDING.md",
            "mechanics/agon/legacy/raw/AGON_EPISTEMIC_WORKFLOW_BOUNDARY.md",
            "mechanics/agon/legacy/raw/AGON_EPISTEMIC_SKILL_CANDIDATES.md",
        )
        for relative_path in legacy_snapshots:
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

        self.assertFalse((REPO_ROOT / "mechanics/agon/legacy/docs-root").exists())

        legacy_part_paths = (
            "mechanics/agon/parts/move-skill-bridge/README.md",
            "mechanics/agon/parts/wave4-skill-landing/README.md",
            "mechanics/agon/parts/recurrence-adapter/README.md",
            "mechanics/agon/parts/wave15-skills-landing/README.md",
            "mechanics/agon/parts/epistemic-workflow-boundary/README.md",
            "mechanics/agon/parts/epistemic-skill-candidates/README.md",
        )
        for relative_path in legacy_part_paths:
            with self.subTest(path=relative_path):
                self.assertFalse((REPO_ROOT / relative_path).exists())

        active_parts = (
            "mechanics/agon/parts/workflow-candidate-bridge/README.md",
            "mechanics/agon/parts/candidate-validation-gate/README.md",
            "mechanics/agon/parts/recurrence-observation/README.md",
            "mechanics/agon/parts/epistemic-candidate-boundary/README.md",
        )
        for relative_path in active_parts:
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

    def test_agon_legacy_has_source_to_active_accounting(self) -> None:
        index = (
            REPO_ROOT / "mechanics" / "agon" / "legacy" / "INDEX.md"
        ).read_text(encoding="utf-8")
        log = (
            REPO_ROOT / "mechanics" / "agon" / "legacy" / "DISTILLATION_LOG.md"
        ).read_text(encoding="utf-8")

        for source_name in (
            "AGON_MOVE_SKILL_BRIDGE.md",
            "AGON_WAVE4_SKILL_LANDING.md",
            "AGON_RECURRENCE_ADAPTER.md",
            "AGON_WAVE15_SKILLS_LANDING.md",
            "AGON_EPISTEMIC_WORKFLOW_BOUNDARY.md",
            "AGON_EPISTEMIC_SKILL_CANDIDATES.md",
        ):
            with self.subTest(source_name=source_name):
                self.assertIn(f"raw/{source_name}", index)
                self.assertIn(source_name, log)

        self.assertIn("workflow-candidate-bridge", index)
        self.assertIn("candidate-validation-gate", index)
        self.assertIn("recurrence-observation", index)
        self.assertIn("epistemic-candidate-boundary", index)

    def test_agon_active_parts_use_functional_names(self) -> None:
        active_surfaces = (
            REPO_ROOT / "mechanics" / "agon" / "README.md",
            REPO_ROOT / "mechanics" / "agon" / "PARTS.md",
        )
        forbidden_active_terms = (
            "Wave IV",
            "Wave 4",
            "Wave15",
            "Wave 15",
            "wave4-skill-landing",
            "wave15-skills-landing",
            "epistemic-workflow-boundary",
            "epistemic-skill-candidates",
        )
        for surface in active_surfaces:
            text = surface.read_text(encoding="utf-8")
            for term in forbidden_active_terms:
                with self.subTest(surface=surface.name, term=term):
                    self.assertNotIn(term, text)

    def test_entrypoints_reference_mechanics_route(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        docs_readme = (REPO_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        roadmap = (REPO_ROOT / "mechanics" / "ROADMAP.md").read_text(
            encoding="utf-8"
        )

        for text in (readme, docs_readme, agents, roadmap):
            with self.subTest(surface=text[:24]):
                self.assertIn("mechanics/README.md", text)


if __name__ == "__main__":
    unittest.main()
