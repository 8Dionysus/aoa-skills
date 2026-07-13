from __future__ import annotations

import dataclasses
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = REPO_ROOT / "evals" / "runners" / "run_live_skill_dispatch.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("aoa_live_skill_dispatch", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load runner from {RUNNER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FakeTransport:
    def __init__(self) -> None:
        self.preflight_calls: list[dict] = []
        self.prompt_inspection_calls: list[dict] = []
        self.cli_calls: list[dict] = []
        self.app_server_calls: list[dict] = []

    def preflight(self, request: dict) -> dict:
        self.preflight_calls.append(request)
        return {
            "storage": {"decision": "allow"},
            "resource": {"decision": "allow"},
            "runtime": {"decision": "allow"},
            "allowed": True,
        }

    def inspect_prompt_skills(self, request: dict) -> dict:
        self.prompt_inspection_calls.append(request)
        inventory = request["expected_prompt_skill_paths"]
        return {
            "returncode": 0,
            "inventory": inventory,
            "entry_fingerprints": {
                name: [
                    hashlib.sha256(f"{name}\0{path}".encode()).hexdigest()
                    for path in paths
                ]
                for name, paths in inventory.items()
            },
            "duration_ms": 0,
        }

    @staticmethod
    def _skill_read_event(request: dict, skill_name: str) -> dict:
        path = Path(request["fixture_root"]) / ".agents" / "skills" / skill_name / "SKILL.md"
        return {
            "type": "item.completed",
            "item": {
                "type": "command_execution",
                "status": "completed",
                "exit_code": 0,
                "command": f"sed -n '1,9999p' {path}",
                "aggregated_output": path.read_text(encoding="utf-8"),
            },
        }

    @staticmethod
    def _validator_event(request: dict) -> dict:
        guidance = Path(request["fixture_root"]) / "AGENTS.md"
        payload = {
            "generated_drift": False,
            "guidance_sha256": hashlib.sha256(guidance.read_bytes()).hexdigest(),
            "proof_authority": False,
            "schema_version": "aoa_live_dispatch_fixture_validator_v1",
            "status": "pass",
        }
        return {
            "type": "item.completed",
            "item": {
                "type": "command_execution",
                "status": "completed",
                "exit_code": 0,
                "command": "python3 fixture_validator.py",
                "aggregated_output": (
                    "AOA_FIXTURE_VALIDATOR_OK "
                    + json.dumps(payload, sort_keys=True, separators=(",", ":"))
                ),
            },
        }

    @staticmethod
    def _outcome_event(request: dict) -> dict | None:
        candidates = request.get("objective_outcome_candidate_values")
        if not isinstance(candidates, list):
            return None
        fixture = Path(request["fixture_root"])
        for candidate in candidates:
            completed = subprocess.run(
                ["python3", "outcome_validator.py", "--candidate", candidate],
                cwd=fixture,
                check=False,
                text=True,
                capture_output=True,
            )
            if completed.returncode == 0:
                return {
                    "type": "item.completed",
                    "item": {
                        "type": "command_execution",
                        "status": "completed",
                        "exit_code": 0,
                        "command": (
                            "python3 outcome_validator.py --candidate " + candidate
                        ),
                        "aggregated_output": completed.stdout,
                    },
                }
        raise AssertionError("fixture outcome contract has no accepted candidate")

    def run_cli(self, request: dict) -> dict:
        self.cli_calls.append(request)
        target = request["expected_target_skill"]
        decision = "manual_required" if request["expected_behavior"] == "manual" else "invoke"
        events = list(request.get("mock_events", []))
        if not events and "fixture_root" in request:
            if request["arm_type"] != "implicit_control":
                events.append(self._skill_read_event(request, target))
                child = request.get("expected_child_skill") or request.get(
                    "expected_selected_child_skill"
                )
                if child:
                    events.append(self._skill_read_event(request, child))
            if request["arm_type"] in {
                "implicit_aided",
                "implicit_control",
                "root_manual_child",
            }:
                events.append(self._validator_event(request))
            outcome_event = self._outcome_event(request)
            if outcome_event is not None:
                events.append(outcome_event)
        disposition = {
            "implicit_aided": "blocked_missing_input",
            "implicit_control": "blocked_missing_input",
            "root_manual_child": "completed",
        }.get(request["arm_type"], "not_applicable")
        return {
            "returncode": 0,
            "stdout": "{\"type\":\"turn.completed\"}\n",
            "stderr": "",
            "final_output": {
                "route_decision": decision,
                "selected_skill": target,
                "selected_child": (
                    None
                    if request["arm_type"] == "implicit_control"
                    else request.get("expected_child_skill")
                    or request.get("expected_selected_child_skill")
                ),
                "claims_loaded": request["arm_type"] != "implicit_control",
                "procedure_disposition": disposition,
                "mutation_authorized": False,
                "proof_authority_claimed": False,
                "promotion_authorized": False,
                "evidence_posture": "candidate_only",
                "next_step": "Use the bounded owner route.",
                "owner_boundary": "Local evidence is not central proof authority.",
                "verification_steps": ["Run the owner validator."],
                "stop_line": "Stop before mutation.",
            },
            "events": events,
            "usage": {"input_tokens": 100, "cached_input_tokens": 0, "output_tokens": 40},
            "duration_ms": 25,
        }

    def run_app_server(self, request: dict) -> dict:
        self.app_server_calls.append(request)
        target = request["expected_target_skill"]
        evidence_events = []
        if "fixture_root" in request:
            skill_event = self._skill_read_event(request, target)
            evidence_events.append({"method": "item/completed", "params": {"item": skill_event["item"]}})
            validator_event = self._validator_event(request)
            evidence_events.append(
                {"method": "item/completed", "params": {"item": validator_event["item"]}}
            )
        return {
            "returncode": 0,
            "stdout": "",
            "stderr": "",
            "final_output": {
                "route_decision": "invoke",
                "selected_skill": target,
                "selected_child": None,
                "claims_loaded": True,
                "procedure_disposition": "completed",
                "mutation_authorized": False,
                "proof_authority_claimed": False,
                "promotion_authorized": False,
                "evidence_posture": "candidate_only",
                "next_step": "Apply the loaded procedure.",
                "owner_boundary": "The local receipt is not a proof verdict.",
                "verification_steps": ["Keep the receipt local."],
                "stop_line": "Stop before unauthorized mutation.",
            },
            "events": [
                *evidence_events,
                {"method": "turn/completed", "params": {"turn": {"status": "completed"}}},
            ],
            "usage": {"input_tokens": 120, "cached_input_tokens": 0, "output_tokens": 50},
            "duration_ms": 30,
            "structured_skill_visible": True,
            "structured_skill_input_sent": True,
            "native_target_skill_input_accepted": True,
            "structured_skill_surface_contract_match": True,
            "external_runtime_isolation_match": True,
        }


class LiveSkillDispatchHarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = load_runner()
        cls.plan_path = REPO_ROOT / "evals" / "suites" / "aoa-skill-live-dispatch.plan.json"

    def load_schema(self, filename: str) -> dict:
        return json.loads((REPO_ROOT / "schemas" / filename).read_text(encoding="utf-8"))

    def test_source_contract_schemas_and_plan_are_valid(self) -> None:
        plan = json.loads(self.plan_path.read_text(encoding="utf-8"))
        for filename in (
            "live-skill-dispatch-plan.schema.json",
            "live-skill-dispatch-procedure-contracts.schema.json",
            "live-skill-dispatch-outcome-contracts.schema.json",
            "live-skill-dispatch-model-output.schema.json",
            "live-skill-dispatch-private-receipt.schema.json",
            "live-skill-dispatch-public-receipt.schema.json",
        ):
            with self.subTest(schema=filename):
                Draft202012Validator.check_schema(self.load_schema(filename))
        Draft202012Validator(self.load_schema("live-skill-dispatch-plan.schema.json")).validate(plan)
        output_schema = self.load_schema("live-skill-dispatch-model-output.schema.json")
        self.runner.validate_openai_strict_output_schema(output_schema)
        invalid_output_schema = json.loads(json.dumps(output_schema))
        invalid_output_schema["properties"]["mutation_authorized"].pop("type")
        with self.assertRaisesRegex(ValueError, "mutation_authorized.*explicit type"):
            self.runner.validate_openai_strict_output_schema(invalid_output_schema)
        incomplete_required = json.loads(json.dumps(output_schema))
        incomplete_required["required"].remove("stop_line")
        with self.assertRaisesRegex(ValueError, "required must contain every property"):
            self.runner.validate_openai_strict_output_schema(incomplete_required)
        open_object = json.loads(json.dumps(output_schema))
        open_object["additionalProperties"] = True
        with self.assertRaisesRegex(ValueError, "additionalProperties must be false"):
            self.runner.validate_openai_strict_output_schema(open_object)
        itemless_array = json.loads(json.dumps(output_schema))
        itemless_array["properties"]["verification_steps"].pop("items")
        with self.assertRaisesRegex(ValueError, "array schema must declare items"):
            self.runner.validate_openai_strict_output_schema(itemless_array)

    def test_local_eval_sidecar_covers_and_locks_every_live_plan_source(self) -> None:
        plan = json.loads(self.plan_path.read_text(encoding="utf-8"))
        sidecar = json.loads(
            (
                REPO_ROOT
                / "evals"
                / "suites"
                / "aoa-skill-live-dispatch-harness.suite.json"
            ).read_text(encoding="utf-8")
        )
        tracked = {
            str(item["path"]): item
            for item in sidecar["tracked_sources"]
        }
        missing = sorted(set(plan["source_refs"]) - set(tracked))
        self.assertEqual([], missing)
        for source_ref in plan["source_refs"]:
            with self.subTest(source_ref=source_ref):
                item = tracked[source_ref]
                self.assertEqual("file", item["kind"])
                actual = hashlib.sha256(
                    (REPO_ROOT / source_ref).read_bytes()
                ).hexdigest()
                self.assertEqual(item["sha256"], actual)

    def test_all_committed_public_receipts_remain_schema_and_privacy_valid(self) -> None:
        schema = self.load_schema("live-skill-dispatch-public-receipt.schema.json")
        paths = sorted(
            (REPO_ROOT / "evals" / "reports").glob(
                "aoa-skill-live-dispatch*.json"
            )
        )
        self.assertGreaterEqual(len(paths), 16)
        for path in paths:
            with self.subTest(receipt=path.name):
                receipt = json.loads(path.read_text(encoding="utf-8"))
                Draft202012Validator(schema).validate(receipt)
                self.runner.validate_public_receipt(receipt)

    def test_all_public_receipts_are_indexed_in_local_reports_readme(self) -> None:
        reports_root = REPO_ROOT / "evals" / "reports"
        report_index = (reports_root / "README.md").read_text(encoding="utf-8")
        missing = sorted(
            path.name
            for path in reports_root.glob("aoa-skill-live-dispatch*.json")
            if f"]({path.name})" not in report_index
        )
        self.assertEqual([], missing)

    def test_cohort_expansion_closes_collision_and_manual_reachability_gaps(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        smoke = self.runner.expand_cohort(REPO_ROOT, plan, "smoke")
        pilot = self.runner.expand_cohort(REPO_ROOT, plan, "pilot13")
        returns = self.runner.expand_cohort(REPO_ROOT, plan, "pilot13-returns")
        skill_returns = self.runner.expand_cohort(
            REPO_ROOT, plan, "pilot13-skill-returns"
        )
        collision = self.runner.expand_cohort(REPO_ROOT, plan, "full-collision")
        closure = self.runner.expand_cohort(REPO_ROOT, plan, "coverage-closure")

        self.assertEqual(4, len(smoke))
        self.assertEqual(30, len(pilot))
        self.assertEqual(15, len(returns))
        self.assertEqual(6, len(skill_returns))
        self.assertEqual(98, len(collision))
        self.assertEqual(87, len(closure))
        self.assertEqual(
            {
                "collision-09",
                "collision-14",
                "collision-20",
                "collision-33",
                "collision-38",
                "collision-49",
                "desc-titan-03-manual",
            },
            {
                trial.case_id
                for trial in returns
                if trial.arm_type in {"implicit_aided", "implicit_control"}
            },
        )
        self.assertEqual(
            ["abyss-safe-infra-change"],
            [
                trial.expected_target_skill
                for trial in returns
                if trial.arm_type == "app_server_structured"
            ],
        )
        self.assertFalse(
            any(trial.arm_type == "root_manual_child" for trial in returns)
        )
        self.assertEqual(
            {"collision-09", "collision-14", "collision-38"},
            {trial.case_id for trial in skill_returns},
        )
        self.assertTrue(
            all(
                trial.arm_type in {"implicit_aided", "implicit_control"}
                for trial in skill_returns
            )
        )
        self.assertTrue(
            all(
                trial.procedure_contract is not None
                and trial.outcome_contract is not None
                for trial in skill_returns
            )
        )
        self.assertTrue(
            all(
                trial.procedure_contract is not None
                and trial.outcome_contract is not None
                for trial in returns
                if trial.arm_type in {"implicit_aided", "implicit_control"}
            )
        )
        self.assertEqual(
            {"implicit_aided", "implicit_control", "root_manual_child", "app_server_structured"},
            {trial.arm_type for trial in smoke},
        )
        self.assertEqual(45, sum(t.arm_type == "app_server_structured" for t in closure))
        self.assertEqual(8, sum(t.arm_type == "root_manual_child" for t in closure))
        self.assertEqual(57, len(self.runner._repo_skill_names(REPO_ROOT)))
        self.assertEqual(12, len(self.runner._prompt_visible_repo_skill_names(REPO_ROOT)))
        self.assertIn("aoa-eval", self.runner._prompt_visible_repo_skill_names(REPO_ROOT))
        self.assertNotIn("aoa-eval-apply", self.runner._prompt_visible_repo_skill_names(REPO_ROOT))
        for cohort in (smoke, pilot, closure):
            for trial in cohort:
                if trial.arm_type == "app_server_structured":
                    self.assertIsNone(
                        self.runner.TEXTUAL_SKILL_ACTIVATION_RE.search(trial.prompt),
                        trial.trial_id,
                    )

    def test_broad_cohort_partitions_are_exact_bounded_and_contract_gated(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        expected_partitions = {
            "full-collision": [
                "full-collision-core-engineering",
                "full-collision-safety-overlays",
                "full-collision-session-growth",
                "full-collision-authority-routing",
                "full-collision-eval-children",
            ],
            "coverage-closure": [
                "coverage-closure-core-implicit",
                "coverage-closure-titan-implicit-a",
                "coverage-closure-titan-implicit-b",
                "coverage-closure-root-trajectories",
                "coverage-closure-structured-core",
                "coverage-closure-structured-titan",
            ],
        }
        self.assertEqual(expected_partitions, plan["cohort_partitions"])

        for parent, wave_names in expected_partitions.items():
            parent_trial_ids = {
                trial.trial_id
                for trial in self.runner.expand_cohort(REPO_ROOT, plan, parent)
            }
            partition_trial_ids: set[str] = set()
            for wave_name in wave_names:
                config = plan["cohorts"][wave_name]
                self.assertIn(
                    config["procedure_contract_mode"],
                    {"required", "required_for_live"},
                )
                self.assertIn(
                    config["objective_outcome_mode"],
                    {"required", "required_for_live"},
                )
                self.assertTrue(config["second_confirmation_required"])
                self.assertLessEqual(config["expected_turn_count"], 30)
                self.assertLessEqual(config["estimated_private_bytes"], 536_870_912)
                self.assertLessEqual(config["estimated_memory_demand_mib"], 512)
                self.assertIn(config["resource_class"], {"light", "medium"})
                wave_trial_ids = {
                    trial.trial_id
                    for trial in self.runner.expand_cohort(
                        REPO_ROOT,
                        plan,
                        wave_name,
                    )
                }
                self.assertTrue(partition_trial_ids.isdisjoint(wave_trial_ids))
                partition_trial_ids.update(wave_trial_ids)
            self.assertEqual(parent_trial_ids, partition_trial_ids)

        core = self.runner.expand_cohort(
            REPO_ROOT,
            plan,
            "full-collision-core-engineering",
        )
        self.assertEqual(16, len(core))
        self.assertEqual(
            {f"collision-{index:02d}" for index in range(1, 9)},
            {trial.case_id for trial in core},
        )
        self.assertTrue(
            all(
                trial.procedure_contract is not None
                and trial.outcome_contract is not None
                for trial in core
            )
        )
        packet = self.runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "full-collision-core-engineering",
            "model-a",
            "medium",
        )
        self.assertEqual(8, packet["implicit_pair_count"])
        self.assertEqual(8, packet["target_route_scored_pair_count"])
        self.assertEqual(8, packet["procedure_contract_pair_count"])
        self.assertEqual(8, packet["procedure_scored_pair_count"])
        self.assertEqual(0, packet["manual_non_activation_pair_count"])
        self.assertTrue(packet["procedure_contract_coverage_complete"])
        self.assertEqual(8, packet["objective_outcome_scored_pair_count"])
        self.assertTrue(packet["objective_outcome_coverage_complete"])
        self.assertTrue(packet["high_cost_confirmation_required"])

    def test_broad_cohort_partition_validator_rejects_overlap_gap_and_unscored_wave(self) -> None:
        plan = self.runner.load_plan(self.plan_path)

        overlapping = json.loads(json.dumps(plan))
        overlapping["cohort_partitions"]["full-collision"].append(
            "full-collision-core-engineering"
        )
        with self.assertRaisesRegex(ValueError, "partition waves overlap"):
            self.runner._validate_cohort_partitions(REPO_ROOT, overlapping)

        incomplete = json.loads(json.dumps(plan))
        incomplete["cohort_partitions"]["full-collision"].remove(
            "full-collision-eval-children"
        )
        with self.assertRaisesRegex(ValueError, "does not exactly cover"):
            self.runner._validate_cohort_partitions(REPO_ROOT, incomplete)

        unscored = json.loads(json.dumps(plan))
        unscored["cohorts"]["full-collision-safety-overlays"][
            "procedure_contract_mode"
        ] = "declared_only"
        with self.assertRaisesRegex(ValueError, "permits unscored procedures"):
            self.runner._validate_cohort_partitions(REPO_ROOT, unscored)

    def test_coverage_closure_implicit_partition_waves_are_contract_complete(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        expectations = {
            "coverage-closure-core-implicit": {
                "case_ids": {"desc-01-implicit", "desc-memo-writeback-manual"},
                "implicit_pairs": 2,
                "route_scored": 1,
                "procedure_scored": 1,
                "manual_guards": 1,
            },
            "coverage-closure-titan-implicit-a": {
                "case_ids": {
                    f"desc-titan-{index:02d}-manual" for index in range(1, 9)
                },
                "implicit_pairs": 8,
                "route_scored": 0,
                "procedure_scored": 0,
                "manual_guards": 8,
            },
            "coverage-closure-titan-implicit-b": {
                "case_ids": {
                    f"desc-titan-{index:02d}-manual" for index in range(9, 16)
                },
                "implicit_pairs": 7,
                "route_scored": 0,
                "procedure_scored": 0,
                "manual_guards": 7,
            },
        }

        for cohort, expected in expectations.items():
            with self.subTest(cohort=cohort):
                trials = self.runner.expand_cohort(REPO_ROOT, plan, cohort)
                self.assertEqual(
                    expected["case_ids"],
                    {trial.case_id for trial in trials},
                )
                self.assertTrue(
                    all(
                        trial.procedure_contract is not None
                        and trial.outcome_contract is not None
                        for trial in trials
                    )
                )
                for trial in trials:
                    if trial.expected_behavior == "manual":
                        self.assertEqual(
                            "not_applicable",
                            trial.procedure_contract.expected_selected_procedure_disposition,
                        )
                        self.assertFalse(
                            trial.procedure_contract.expected_selected_procedure_completion_reported
                        )
                        self.assertFalse(
                            trial.procedure_contract.expected_selected_procedure_deflection_reported
                        )

                packet = self.runner.build_plan_packet(
                    REPO_ROOT,
                    plan,
                    cohort,
                    "model-a",
                    "medium",
                )
                self.assertEqual(
                    expected["implicit_pairs"], packet["implicit_pair_count"]
                )
                self.assertEqual(
                    expected["route_scored"],
                    packet["target_route_scored_pair_count"],
                )
                self.assertEqual(
                    expected["implicit_pairs"],
                    packet["procedure_contract_pair_count"],
                )
                self.assertEqual(
                    expected["procedure_scored"],
                    packet["procedure_scored_pair_count"],
                )
                self.assertEqual(
                    expected["manual_guards"],
                    packet["manual_non_activation_pair_count"],
                )
                self.assertTrue(packet["procedure_contract_coverage_complete"])
                self.assertEqual(
                    expected["implicit_pairs"],
                    packet["objective_outcome_scored_pair_count"],
                )
                self.assertTrue(packet["objective_outcome_coverage_complete"])
                self.assertTrue(packet["high_cost_confirmation_required"])
                with tempfile.TemporaryDirectory() as td:
                    receipt = self.runner.run_confirmed_cohort(
                        repo_root=REPO_ROOT,
                        plan=plan,
                        cohort=cohort,
                        model="model-a",
                        effort="medium",
                        confirmation_token=packet["confirmation_token"],
                        high_cost_token=packet["high_cost_confirmation_token"],
                        private_root=Path(td),
                        transport=FakeTransport(),
                        test_only_allow_noncanonical_private_root=True,
                    )
                Draft202012Validator(
                    self.load_schema("live-skill-dispatch-private-receipt.schema.json")
                ).validate(receipt)
                public = self.runner.build_public_receipt(receipt)
                Draft202012Validator(
                    self.load_schema("live-skill-dispatch-public-receipt.schema.json")
                ).validate(public)
                self.runner.validate_public_receipt(public)
                self.assertEqual(cohort, public["cohort"])
                self.assertEqual(len(trials), public["trial_count"])
                self.assertEqual(
                    expected["implicit_pairs"], public["pair_count"]
                )

    def test_titan_b_observation_return_is_small_exact_and_contract_complete(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        cohort = "coverage-closure-titan-implicit-b-returns"
        config = plan["cohorts"][cohort]
        trials = self.runner.expand_cohort(REPO_ROOT, plan, cohort)
        expected_case_ids = {
            "desc-titan-12-manual",
            "desc-titan-13-manual",
        }

        self.assertEqual(4, len(trials))
        self.assertEqual(expected_case_ids, {trial.case_id for trial in trials})
        self.assertEqual(
            {"implicit_aided", "implicit_control"},
            {trial.arm_type for trial in trials},
        )
        for case_id in expected_case_ids:
            self.assertEqual(
                {"implicit_aided", "implicit_control"},
                {trial.arm_type for trial in trials if trial.case_id == case_id},
            )
        self.assertTrue(
            all(
                trial.procedure_contract is not None
                and trial.outcome_contract is not None
                and trial.expected_behavior == "manual"
                for trial in trials
            )
        )
        self.assertEqual(4, config["expected_turn_count"])
        self.assertTrue(config["second_confirmation_required"])
        self.assertEqual("medium", config["resource_class"])
        self.assertLessEqual(config["estimated_private_bytes"], 268_435_456)
        self.assertLessEqual(config["estimated_memory_demand_mib"], 512)

        packet = self.runner.build_plan_packet(
            REPO_ROOT,
            plan,
            cohort,
            "model-a",
            "medium",
        )
        self.assertEqual(2, packet["implicit_pair_count"])
        self.assertEqual(0, packet["target_route_scored_pair_count"])
        self.assertEqual(2, packet["procedure_contract_pair_count"])
        self.assertEqual(0, packet["procedure_scored_pair_count"])
        self.assertEqual(2, packet["manual_non_activation_pair_count"])
        self.assertTrue(packet["procedure_contract_coverage_complete"])
        self.assertEqual(2, packet["objective_outcome_scored_pair_count"])
        self.assertTrue(packet["objective_outcome_coverage_complete"])
        self.assertTrue(packet["high_cost_confirmation_required"])

        with tempfile.TemporaryDirectory() as td:
            receipt = self.runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort=cohort,
                model="model-a",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=packet["high_cost_confirmation_token"],
                private_root=Path(td),
                transport=FakeTransport(),
                test_only_allow_noncanonical_private_root=True,
            )
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-private-receipt.schema.json")
        ).validate(receipt)
        public = self.runner.build_public_receipt(receipt)
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-public-receipt.schema.json")
        ).validate(public)
        self.runner.validate_public_receipt(public)
        self.assertEqual(4, public["trial_count"])
        self.assertEqual(2, public["pair_count"])

    def test_safety_overlay_partition_wave_is_contract_complete(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        safety = self.runner.expand_cohort(
            REPO_ROOT,
            plan,
            "full-collision-safety-overlays",
        )
        self.assertEqual(22, len(safety))
        self.assertEqual(
            {f"collision-{index:02d}" for index in range(9, 20)},
            {trial.case_id for trial in safety},
        )
        self.assertTrue(
            all(
                trial.procedure_contract is not None
                and trial.outcome_contract is not None
                for trial in safety
            )
        )
        packet = self.runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "full-collision-safety-overlays",
            "model-a",
            "medium",
        )
        self.assertEqual(11, packet["implicit_pair_count"])
        self.assertEqual(2, packet["target_route_scored_pair_count"])
        self.assertEqual(11, packet["procedure_contract_pair_count"])
        self.assertEqual(2, packet["procedure_scored_pair_count"])
        self.assertEqual(9, packet["manual_non_activation_pair_count"])
        self.assertTrue(packet["procedure_contract_coverage_complete"])
        self.assertEqual(11, packet["objective_outcome_scored_pair_count"])
        self.assertTrue(packet["objective_outcome_coverage_complete"])
        self.assertTrue(packet["high_cost_confirmation_required"])
        with tempfile.TemporaryDirectory() as td:
            receipt = self.runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="full-collision-safety-overlays",
                model="model-a",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=packet["high_cost_confirmation_token"],
                private_root=Path(td),
                transport=FakeTransport(),
                test_only_allow_noncanonical_private_root=True,
            )
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-private-receipt.schema.json")
        ).validate(receipt)
        public = self.runner.build_public_receipt(receipt)
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-public-receipt.schema.json")
        ).validate(public)
        self.runner.validate_public_receipt(public)
        self.assertEqual("full-collision-safety-overlays", public["cohort"])
        self.assertEqual(22, public["trial_count"])
        self.assertEqual(11, public["pair_count"])

    def test_session_growth_partition_wave_is_contract_complete(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        session_growth = self.runner.expand_cohort(
            REPO_ROOT,
            plan,
            "full-collision-session-growth",
        )
        self.assertEqual(28, len(session_growth))
        self.assertEqual(
            {f"collision-{index:02d}" for index in range(20, 34)},
            {trial.case_id for trial in session_growth},
        )
        self.assertTrue(
            all(
                trial.procedure_contract is not None
                and trial.outcome_contract is not None
                for trial in session_growth
            )
        )
        packet = self.runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "full-collision-session-growth",
            "model-a",
            "medium",
        )
        self.assertEqual(14, packet["implicit_pair_count"])
        self.assertEqual(3, packet["target_route_scored_pair_count"])
        self.assertEqual(14, packet["procedure_contract_pair_count"])
        self.assertEqual(3, packet["procedure_scored_pair_count"])
        self.assertEqual(11, packet["manual_non_activation_pair_count"])
        self.assertTrue(packet["procedure_contract_coverage_complete"])
        self.assertEqual(14, packet["objective_outcome_scored_pair_count"])
        self.assertTrue(packet["objective_outcome_coverage_complete"])
        self.assertTrue(packet["high_cost_confirmation_required"])
        with tempfile.TemporaryDirectory() as td:
            receipt = self.runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="full-collision-session-growth",
                model="model-a",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=packet["high_cost_confirmation_token"],
                private_root=Path(td),
                transport=FakeTransport(),
                test_only_allow_noncanonical_private_root=True,
            )
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-private-receipt.schema.json")
        ).validate(receipt)
        public = self.runner.build_public_receipt(receipt)
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-public-receipt.schema.json")
        ).validate(public)
        self.runner.validate_public_receipt(public)
        self.assertEqual("full-collision-session-growth", public["cohort"])
        self.assertEqual(28, public["trial_count"])
        self.assertEqual(14, public["pair_count"])

    def test_session_growth_return_repeats_only_routing_gap_pairs(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        returns = self.runner.expand_cohort(
            REPO_ROOT,
            plan,
            "full-collision-session-growth-returns",
        )
        self.assertEqual(8, len(returns))
        self.assertEqual(
            {"collision-21", "collision-22", "collision-25", "collision-33"},
            {trial.case_id for trial in returns},
        )
        self.assertTrue(
            all(
                trial.arm_type in {"implicit_aided", "implicit_control"}
                and trial.procedure_contract is not None
                and trial.outcome_contract is not None
                for trial in returns
            )
        )
        packet = self.runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "full-collision-session-growth-returns",
            "model-a",
            "medium",
        )
        self.assertEqual(4, packet["implicit_pair_count"])
        self.assertEqual(0, packet["target_route_scored_pair_count"])
        self.assertEqual(4, packet["procedure_contract_pair_count"])
        self.assertEqual(0, packet["procedure_scored_pair_count"])
        self.assertEqual(4, packet["manual_non_activation_pair_count"])
        self.assertTrue(packet["procedure_contract_coverage_complete"])
        self.assertEqual(4, packet["objective_outcome_scored_pair_count"])
        self.assertTrue(packet["objective_outcome_coverage_complete"])
        self.assertTrue(packet["high_cost_confirmation_required"])
        with tempfile.TemporaryDirectory() as td:
            receipt = self.runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="full-collision-session-growth-returns",
                model="model-a",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=packet["high_cost_confirmation_token"],
                private_root=Path(td),
                transport=FakeTransport(),
                test_only_allow_noncanonical_private_root=True,
            )
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-private-receipt.schema.json")
        ).validate(receipt)
        public = self.runner.build_public_receipt(receipt)
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-public-receipt.schema.json")
        ).validate(public)
        self.runner.validate_public_receipt(public)
        self.assertEqual("full-collision-session-growth-returns", public["cohort"])
        self.assertEqual(8, public["trial_count"])
        self.assertEqual(4, public["pair_count"])
        self.assertTrue(
            all(
                pair["route_effect_class"]
                == "not_scored_target_not_prompt_visible"
                and pair["manual_non_activation_guard_defined"] is True
                for pair in public["pair_outcomes"]
            )
        )
        tampered = json.loads(json.dumps(public))
        tampered["pair_outcomes"][0]["route_lift"] = 0
        with self.assertRaisesRegex(
            self.runner.PublicReceiptSafetyError,
            "hidden-target route score conflicts with eligibility",
        ):
            self.runner.validate_public_receipt(tampered)

    def test_authority_routing_partition_wave_is_contract_complete(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        authority = self.runner.expand_cohort(
            REPO_ROOT,
            plan,
            "full-collision-authority-routing",
        )
        expected_procedures = {
            "collision-34": (None, "blocked_missing_input", False, True),
            "collision-35": (None, "not_applicable", False, False),
            "collision-36": (None, "blocked_missing_input", False, True),
            "collision-37": (None, "blocked_missing_input", False, True),
            "collision-38": (
                "aoa-decision-find",
                "blocked_missing_input",
                False,
                True,
            ),
            "collision-39": (
                "aoa-decision-find",
                "blocked_missing_input",
                False,
                True,
            ),
            "collision-40": (
                "aoa-decision-create",
                "blocked_missing_input",
                False,
                True,
            ),
            "collision-41": (
                "aoa-decision-correct",
                "blocked_missing_input",
                False,
                True,
            ),
            "collision-42": (
                "aoa-eval-select",
                "blocked_missing_input",
                False,
                True,
            ),
            "collision-43": (None, "blocked_missing_input", False, True),
            "collision-49": (None, "not_applicable", False, False),
        }
        expected_outcomes = {
            "collision-34": "request_target_repo_and_authority_surfaces",
            "collision-35": "require_explicit_invocation_and_local_authority",
            "collision-36": "request_target_context_surfaces_and_owner_interfaces",
            "collision-37": "inspect_candidate_authority_files_before_memo_writeback",
            "collision-38": "inspect_graph_status_and_narrow_impact_packet",
            "collision-39": "route_through_decision_root_before_graph_lookup",
            "collision-40": "route_through_decision_root_before_record_creation",
            "collision-41": "route_through_decision_root_before_source_correction",
            "collision-42": "inspect_target_eval_surfaces_before_classification",
            "collision-43": "inspect_eval_guidance_authority_before_suite_design",
            "collision-49": "require_explicit_invocation_before_trust_loop",
        }
        self.assertEqual(22, len(authority))
        self.assertEqual(set(expected_procedures), {trial.case_id for trial in authority})
        self.assertEqual(set(expected_procedures), set(expected_outcomes))
        for trial in authority:
            with self.subTest(case_id=trial.case_id, arm=trial.arm_type):
                self.assertIsNotNone(trial.procedure_contract)
                self.assertIsNotNone(trial.outcome_contract)
                procedure = trial.procedure_contract
                outcome = trial.outcome_contract
                assert procedure is not None
                assert outcome is not None
                child, disposition, completion, deflection = expected_procedures[
                    trial.case_id
                ]
                self.assertEqual(
                    "manual" if disposition == "not_applicable" else "invoke",
                    trial.expected_behavior,
                )
                if trial.case_id in {"collision-39", "collision-40", "collision-41"}:
                    self.assertEqual("aoa-decision", trial.expected_target_skill)
                    self.assertEqual("aoa-decision", trial.root_skill)
                    self.assertEqual(child, trial.expected_child_skill)
                    self.assertNotIn("aoa-decision", trial.competing_skills)
                self.assertEqual(child, procedure.expected_selected_child_skill)
                self.assertEqual(
                    True if child is not None else None,
                    procedure.expected_selected_child_full_read_observed,
                )
                self.assertEqual(
                    disposition,
                    procedure.expected_selected_procedure_disposition,
                )
                self.assertEqual(
                    completion,
                    procedure.expected_selected_procedure_completion_reported,
                )
                self.assertEqual(
                    deflection,
                    procedure.expected_selected_procedure_deflection_reported,
                )
                self.assertTrue(procedure.expected_owner_boundary_present)
                self.assertEqual(
                    expected_outcomes[trial.case_id],
                    outcome.expected_candidate_value,
                )

        packet = self.runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "full-collision-authority-routing",
            "model-a",
            "medium",
        )
        self.assertEqual(11, packet["implicit_pair_count"])
        self.assertEqual(9, packet["target_route_scored_pair_count"])
        self.assertEqual(11, packet["procedure_contract_pair_count"])
        self.assertEqual(9, packet["procedure_scored_pair_count"])
        self.assertEqual(2, packet["manual_non_activation_pair_count"])
        self.assertTrue(packet["procedure_contract_coverage_complete"])
        self.assertEqual(11, packet["objective_outcome_scored_pair_count"])
        self.assertTrue(packet["objective_outcome_coverage_complete"])
        self.assertTrue(packet["high_cost_confirmation_required"])
        with tempfile.TemporaryDirectory() as td:
            receipt = self.runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="full-collision-authority-routing",
                model="model-a",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=packet["high_cost_confirmation_token"],
                private_root=Path(td),
                transport=FakeTransport(),
                test_only_allow_noncanonical_private_root=True,
            )
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-private-receipt.schema.json")
        ).validate(receipt)
        public = self.runner.build_public_receipt(receipt)
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-public-receipt.schema.json")
        ).validate(public)
        self.runner.validate_public_receipt(public)
        self.assertEqual("full-collision-authority-routing", public["cohort"])
        self.assertEqual(22, public["trial_count"])
        self.assertEqual(11, public["pair_count"])

    def test_authority_routing_return_cohort_repeats_only_parent_child_pairs(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        returns = self.runner.expand_cohort(
            REPO_ROOT,
            plan,
            "full-collision-authority-routing-returns",
        )
        self.assertEqual(6, len(returns))
        self.assertEqual(
            {"collision-39", "collision-40", "collision-41"},
            {trial.case_id for trial in returns},
        )
        self.assertTrue(
            all(
                trial.arm_type in {"implicit_aided", "implicit_control"}
                and trial.expected_target_skill == "aoa-decision"
                and trial.expected_behavior == "invoke"
                and trial.root_skill == "aoa-decision"
                and trial.expected_child_skill is not None
                and trial.procedure_contract is not None
                and trial.outcome_contract is not None
                for trial in returns
            )
        )
        packet = self.runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "full-collision-authority-routing-returns",
            "model-a",
            "medium",
        )
        self.assertEqual(3, packet["implicit_pair_count"])
        self.assertEqual(3, packet["target_route_scored_pair_count"])
        self.assertEqual(3, packet["procedure_scored_pair_count"])
        self.assertEqual(0, packet["manual_non_activation_pair_count"])
        self.assertTrue(packet["procedure_contract_coverage_complete"])
        self.assertTrue(packet["objective_outcome_coverage_complete"])
        self.assertTrue(packet["high_cost_confirmation_required"])

    def test_authority_procedure_return_cohort_repeats_only_open_terminals(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        self.assertIn(
            "config/portable_skill_overrides.json",
            plan["source_refs"],
        )
        overrides = json.loads(
            (REPO_ROOT / "config" / "portable_skill_overrides.json").read_text()
        )["skills"]
        for skill_name in ("aoa-decision-create", "aoa-decision-correct"):
            source = (
                REPO_ROOT
                / "skills/core/engineering"
                / skill_name
                / "SKILL.md"
            ).read_text()
            normalized_source = " ".join(source.split())
            description = overrides[skill_name]["description"]
            with self.subTest(skill_name=skill_name, surface="source"):
                self.assertIn("stop with `blocked_missing_input`", normalized_source)
                self.assertIn(
                    "do not relabel missing input as `deferred_owner_boundary`",
                    normalized_source,
                )
                self.assertIn("inside the active evidence boundary", normalized_source)
            with self.subTest(skill_name=skill_name, surface="portable-description"):
                self.assertIn("stop with blocked_missing_input", description)
                self.assertIn(
                    "do not relabel missing input as deferred_owner_boundary",
                    description,
                )
        returns = self.runner.expand_cohort(
            REPO_ROOT,
            plan,
            "full-collision-authority-routing-procedure-returns",
        )
        self.assertEqual(4, len(returns))
        self.assertEqual(
            {"collision-40", "collision-41"},
            {trial.case_id for trial in returns},
        )
        self.assertTrue(
            all(
                trial.arm_type in {"implicit_aided", "implicit_control"}
                and trial.expected_target_skill == "aoa-decision"
                and trial.expected_behavior == "invoke"
                and trial.root_skill == "aoa-decision"
                and trial.expected_child_skill
                in {"aoa-decision-create", "aoa-decision-correct"}
                and trial.procedure_contract is not None
                and trial.outcome_contract is not None
                for trial in returns
            )
        )
        packet = self.runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "full-collision-authority-routing-procedure-returns",
            "model-a",
            "medium",
        )
        self.assertEqual(2, packet["implicit_pair_count"])
        self.assertEqual(2, packet["target_route_scored_pair_count"])
        self.assertEqual(2, packet["procedure_scored_pair_count"])
        self.assertEqual(0, packet["manual_non_activation_pair_count"])
        self.assertEqual(2, packet["objective_outcome_scored_pair_count"])
        self.assertTrue(packet["procedure_contract_coverage_complete"])
        self.assertTrue(packet["objective_outcome_coverage_complete"])
        self.assertTrue(packet["high_cost_confirmation_required"])

    def test_root_child_implicit_map_is_policy_bound_and_covers_eval_children(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        eval_children = runner.expand_cohort(
            REPO_ROOT,
            plan,
            "full-collision-eval-children",
        )
        expected_children = {
            "collision-44": "aoa-eval-select",
            "collision-45": "aoa-eval-apply",
            "collision-46": "aoa-eval-local-need",
            "collision-47": "aoa-eval-design",
            "collision-48": "aoa-eval-session-mining",
        }
        self.assertEqual(10, len(eval_children))
        for trial in eval_children:
            with self.subTest(case_id=trial.case_id, arm=trial.arm_type):
                self.assertEqual("aoa-eval", trial.expected_target_skill)
                self.assertEqual("aoa-eval", trial.root_skill)
                self.assertEqual("invoke", trial.expected_behavior)
                self.assertEqual(expected_children[trial.case_id], trial.expected_child_skill)
                self.assertNotIn("aoa-eval", trial.competing_skills)
                self.assertIsNotNone(trial.procedure_contract)
                self.assertIsNotNone(trial.outcome_contract)
        overrides = json.loads(
            (REPO_ROOT / "config" / "portable_skill_overrides.json").read_text()
        )["skills"]
        root_source = " ".join(
            (
                REPO_ROOT
                / "skills/core/engineering/aoa-eval/SKILL.md"
            ).read_text().split()
        )
        root_description = overrides["aoa-eval"]["description"]
        self.assertIn("read this root `SKILL.md` to EOF", root_source)
        self.assertIn("a bounded prefix is not a complete load", root_source)
        self.assertIn("read this root skill to EOF", root_description)
        self.assertIn("a bounded prefix is not a complete load", root_description)
        self.assertIn(
            "an explicit owner request to design a bounded local eval suite or "
            "report has design precedence",
            root_source.lower(),
        )
        self.assertIn(
            "do not reroute the design request to `aoa-eval-select`",
            root_source.lower(),
        )
        self.assertIn(
            "an explicit request to design a bounded local eval suite selects "
            "aoa-eval-design even when invariant or target inputs are missing",
            root_description.lower(),
        )
        for skill_name in expected_children.values():
            source = (
                REPO_ROOT
                / "skills/core/engineering"
                / skill_name
                / "SKILL.md"
            ).read_text()
            normalized_source = " ".join(source.split())
            description = overrides[skill_name]["description"]
            with self.subTest(skill_name=skill_name, surface="source"):
                self.assertIn("stop with `blocked_missing_input`", normalized_source)
                self.assertIn(
                    "do not relabel missing input as `deferred_owner_boundary`",
                    normalized_source,
                )
            with self.subTest(skill_name=skill_name, surface="portable-description"):
                self.assertIn("stop with blocked_missing_input", description)
                self.assertIn(
                    "do not relabel missing input as deferred_owner_boundary",
                    description,
                )
        apply_source = " ".join(
            (
                REPO_ROOT
                / "skills/core/engineering/aoa-eval-apply/SKILL.md"
            ).read_text().split()
        )
        apply_description = overrides["aoa-eval-apply"]["description"]
        exact_next_action = (
            "request the exact selected command, source root/ref, prerequisites, "
            "expected artifacts, and pass/fail criteria as the next owner action"
        )
        self.assertIn(exact_next_action, apply_source.lower())
        self.assertIn(exact_next_action, apply_description.lower())
        self.assertIn(
            "never choose a fixture probe as the selected eval",
            apply_source.lower(),
        )
        self.assertIn(
            "never choose a fixture probe as the selected eval",
            apply_description.lower(),
        )
        packet = runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "full-collision-eval-children",
            "model-a",
            "medium",
        )
        self.assertEqual(5, packet["target_route_scored_pair_count"])
        self.assertEqual(5, packet["procedure_contract_pair_count"])
        self.assertEqual(5, packet["procedure_scored_pair_count"])
        self.assertEqual(0, packet["manual_non_activation_pair_count"])
        self.assertEqual(5, packet["objective_outcome_scored_pair_count"])
        self.assertTrue(packet["procedure_contract_coverage_complete"])
        self.assertTrue(packet["objective_outcome_coverage_complete"])

        duplicate = json.loads(json.dumps(plan))
        duplicate["root_child_trajectories"][-1] = {
            "case_id": "collision-39",
            "root_skill": "aoa-eval",
            "child_skill": "aoa-decision-find",
        }
        with self.assertRaisesRegex(ValueError, "duplicate root-child trajectory case"):
            runner.expand_cohort(
                REPO_ROOT,
                duplicate,
                "full-collision-authority-routing",
            )

        policies = runner._policy_entries(REPO_ROOT, plan)
        policies["aoa-decision"] = {
            **policies["aoa-decision"],
            "implicit_activation_policy": "manual",
        }
        with (
            mock.patch.object(runner, "_policy_entries", return_value=policies),
            self.assertRaisesRegex(
                ValueError,
                "root-child trajectory parent must be implicit invoke",
            ),
        ):
            runner.expand_cohort(
                REPO_ROOT,
                plan,
                "full-collision-authority-routing",
            )

    def test_core_engineering_return_cohort_repeats_only_fixture_gap_pairs(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        returns = self.runner.expand_cohort(
            REPO_ROOT,
            plan,
            "full-collision-core-engineering-returns",
        )
        self.assertEqual(4, len(returns))
        self.assertEqual(
            {"collision-01", "collision-02"},
            {trial.case_id for trial in returns},
        )
        self.assertTrue(
            all(
                trial.arm_type in {"implicit_aided", "implicit_control"}
                and trial.procedure_contract is not None
                and trial.outcome_contract is not None
                for trial in returns
            )
        )
        packet = self.runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "full-collision-core-engineering-returns",
            "model-a",
            "medium",
        )
        self.assertEqual(2, packet["implicit_pair_count"])
        self.assertEqual(2, packet["procedure_scored_pair_count"])
        self.assertTrue(packet["procedure_contract_coverage_complete"])
        self.assertEqual(2, packet["objective_outcome_scored_pair_count"])
        self.assertTrue(packet["objective_outcome_coverage_complete"])
        self.assertTrue(packet["high_cost_confirmation_required"])
        with tempfile.TemporaryDirectory() as td:
            receipt = self.runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="full-collision-core-engineering-returns",
                model="model-a",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=packet["high_cost_confirmation_token"],
                private_root=Path(td),
                transport=FakeTransport(),
                test_only_allow_noncanonical_private_root=True,
            )
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-private-receipt.schema.json")
        ).validate(receipt)
        public = self.runner.build_public_receipt(receipt)
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-public-receipt.schema.json")
        ).validate(public)
        self.runner.validate_public_receipt(public)
        self.assertEqual("full-collision-core-engineering-returns", public["cohort"])
        self.assertEqual(4, public["trial_count"])
        self.assertEqual(2, public["pair_count"])

    def test_core_engineering_outcome_return_cohort_repeats_only_outcome_gap_pairs(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        returns = self.runner.expand_cohort(
            REPO_ROOT,
            plan,
            "full-collision-core-engineering-outcome-returns",
        )
        self.assertEqual(4, len(returns))
        self.assertEqual(
            {"collision-05", "collision-06"},
            {trial.case_id for trial in returns},
        )
        self.assertTrue(
            all(
                trial.arm_type in {"implicit_aided", "implicit_control"}
                and trial.procedure_contract is not None
                and trial.outcome_contract is not None
                for trial in returns
            )
        )
        packet = self.runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "full-collision-core-engineering-outcome-returns",
            "model-a",
            "medium",
        )
        self.assertEqual(2, packet["implicit_pair_count"])
        self.assertEqual(2, packet["procedure_scored_pair_count"])
        self.assertTrue(packet["procedure_contract_coverage_complete"])
        self.assertEqual(2, packet["objective_outcome_scored_pair_count"])
        self.assertTrue(packet["objective_outcome_coverage_complete"])
        self.assertTrue(packet["high_cost_confirmation_required"])
        with tempfile.TemporaryDirectory() as td:
            receipt = self.runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="full-collision-core-engineering-outcome-returns",
                model="model-a",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=packet["high_cost_confirmation_token"],
                private_root=Path(td),
                transport=FakeTransport(),
                test_only_allow_noncanonical_private_root=True,
            )
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-private-receipt.schema.json")
        ).validate(receipt)
        public = self.runner.build_public_receipt(receipt)
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-public-receipt.schema.json")
        ).validate(public)
        self.runner.validate_public_receipt(public)
        self.assertEqual(
            "full-collision-core-engineering-outcome-returns",
            public["cohort"],
        )
        self.assertEqual(4, public["trial_count"])
        self.assertEqual(2, public["pair_count"])

    def test_smoke_procedure_contract_is_source_locked_before_live_execution(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        smoke = runner.expand_cohort(REPO_ROOT, plan, "smoke")
        implicit = [
            trial
            for trial in smoke
            if trial.arm_type in {"implicit_aided", "implicit_control"}
        ]

        self.assertEqual(2, len(implicit))
        self.assertEqual("required", plan["cohorts"]["smoke"]["procedure_contract_mode"])
        for trial in implicit:
            self.assertIsNotNone(trial.procedure_contract)
            contract = trial.procedure_contract
            assert contract is not None
            self.assertEqual("collision-42-child-procedure-v3", contract.contract_id)
            self.assertEqual("selected_route_procedure_disposition", contract.scope)
            self.assertEqual("aoa-eval-select", contract.expected_selected_child_skill)
            self.assertTrue(contract.expected_selected_child_full_read_observed)
            self.assertEqual(
                "blocked_missing_input",
                contract.expected_selected_procedure_disposition,
            )
            self.assertFalse(contract.expected_selected_procedure_completion_reported)
            self.assertTrue(contract.expected_selected_procedure_deflection_reported)
            self.assertTrue(contract.expected_owner_boundary_present)

        packet = runner.build_plan_packet(REPO_ROOT, plan, "smoke", "model-a", "medium")
        self.assertEqual("required", packet["procedure_contract_mode"])
        self.assertEqual(1, packet["implicit_pair_count"])
        self.assertEqual(1, packet["procedure_scored_pair_count"])
        self.assertTrue(packet["procedure_contract_coverage_complete"])
        self.assertEqual(1, packet["objective_outcome_scored_pair_count"])
        self.assertTrue(packet["objective_outcome_coverage_complete"])
        implicit_locks = [
            item
            for item in packet["trial_locks"]
            if item["arm_type"] in {"implicit_aided", "implicit_control"}
        ]
        self.assertEqual(2, len(implicit_locks))
        self.assertTrue(all(item["procedure_contract_defined"] for item in implicit_locks))
        self.assertEqual(1, len({item["procedure_contract_sha256"] for item in implicit_locks}))
        structured = next(
            trial for trial in smoke if trial.arm_type == "app_server_structured"
        )
        self.assertEqual("aoa-eval", structured.equivalent_report_root_skill)
        structured_lock = next(
            item
            for item in packet["trial_locks"]
            if item["arm_type"] == "app_server_structured"
        )
        self.assertEqual(
            "aoa-eval",
            structured_lock["equivalent_report_root_skill"],
        )

        with mock.patch.object(runner, "_procedure_contracts", return_value={}):
            with self.assertRaisesRegex(
                ValueError,
                "smoke requires explicit procedure contracts for: collision-42",
            ):
                runner.expand_cohort(REPO_ROOT, plan, "smoke")

    def test_smoke_objective_outcome_is_source_locked_and_transport_observable(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        smoke = runner.expand_cohort(REPO_ROOT, plan, "smoke")
        implicit = [
            trial
            for trial in smoke
            if trial.arm_type in {"implicit_aided", "implicit_control"}
        ]

        self.assertEqual(2, len(implicit))
        for trial in implicit:
            self.assertIsNotNone(trial.outcome_contract)
            contract = trial.outcome_contract
            assert contract is not None
            self.assertEqual("collision-42-owner-action-v1", contract.contract_id)
            self.assertEqual("fixture_owner_observable_decision", contract.scope)
            self.assertEqual(
                "inspect_target_eval_surfaces_before_classification",
                contract.expected_candidate_value,
            )
            descriptor = trial.public_descriptor()
            self.assertTrue(descriptor["outcome_contract_defined"])
            self.assertEqual(contract.sha256(), descriptor["outcome_contract_sha256"])
            self.assertNotIn("expected_candidate_value", descriptor)

        packet = runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "smoke",
            "model-a",
            "medium",
        )
        self.assertEqual("required", packet["objective_outcome_mode"])
        self.assertEqual(1, packet["objective_outcome_scored_pair_count"])
        self.assertTrue(packet["objective_outcome_coverage_complete"])

        trial = implicit[0]
        contract = trial.outcome_contract
        assert contract is not None
        with tempfile.TemporaryDirectory() as td:
            run_root = Path(td)
            (run_root / "fixtures").mkdir()
            fixture, _context_sha, _skill_sha = runner._prepare_fixture(
                REPO_ROOT,
                run_root,
                0,
                include_skills=False,
                trial=trial,
            )
            validator = fixture / runner.OUTCOME_VALIDATOR_RELATIVE_PATH
            self.assertTrue(validator.is_file())
            completed = subprocess.run(
                [
                    "python3",
                    validator.name,
                    "--candidate",
                    contract.expected_candidate_value,
                ],
                cwd=fixture,
                check=False,
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, completed.returncode)
            event = {
                "type": "item.completed",
                "item": {
                    "type": "command_execution",
                    "status": "completed",
                    "exit_code": completed.returncode,
                    "command": (
                        "python3 outcome_validator.py --candidate "
                        + contract.expected_candidate_value
                    ),
                    "aggregated_output": completed.stdout,
                },
            }
            evidence = runner._objective_outcome_evidence(
                contract,
                [event],
                fixture,
            )
            self.assertTrue(evidence["outcome_contract_match"])
            self.assertTrue(evidence["outcome_single_attempt"])
            self.assertTrue(evidence["outcome_validator_not_inspected"])

            wrong_candidate = next(
                value
                for value in contract.candidate_values
                if value != contract.expected_candidate_value
            )
            wrong = subprocess.run(
                ["python3", validator.name, "--candidate", wrong_candidate],
                cwd=fixture,
                check=False,
                text=True,
                capture_output=True,
            )
            wrong_event = {
                "type": "item.completed",
                "item": {
                    "type": "command_execution",
                    "status": "completed",
                    "exit_code": wrong.returncode,
                    "command": (
                        "python3 outcome_validator.py --candidate " + wrong_candidate
                    ),
                    "aggregated_output": wrong.stdout,
                },
            }
            negative = runner._objective_outcome_evidence(
                contract,
                [wrong_event],
                fixture,
            )
            self.assertFalse(negative["outcome_contract_match"])
            self.assertTrue(negative["outcome_single_attempt"])
            self.assertTrue(negative["outcome_validator_not_inspected"])

            retried = runner._objective_outcome_evidence(
                contract,
                [wrong_event, event],
                fixture,
            )
            self.assertFalse(retried["outcome_contract_match"])
            self.assertFalse(retried["outcome_single_attempt"])
            self.assertEqual(2, retried["outcome_attempt_count"])

            inspected = {
                "type": "item.completed",
                "item": {
                    "type": "command_execution",
                    "status": "completed",
                    "exit_code": 0,
                    "command": "sed -n '1,200p' outcome_validator.py",
                    "aggregated_output": validator.read_text(encoding="utf-8"),
                },
            }
            contaminated = runner._objective_outcome_evidence(
                contract,
                [inspected, event],
                fixture,
            )
            self.assertFalse(contaminated["outcome_contract_match"])
            self.assertFalse(contaminated["outcome_validator_not_inspected"])

        with mock.patch.object(runner, "_outcome_contracts", return_value={}):
            with self.assertRaisesRegex(
                ValueError,
                "smoke requires explicit outcome contracts for: collision-42",
            ):
                runner.expand_cohort(REPO_ROOT, plan, "smoke")

    def test_pilot_has_source_locked_procedure_and_outcome_contracts_for_all_cases(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        pilot = runner.expand_cohort(REPO_ROOT, plan, "pilot13")
        implicit = [
            trial
            for trial in pilot
            if trial.arm_type in {"implicit_aided", "implicit_control"}
        ]
        expected = {
            "collision-01": (None, "blocked_missing_input", False, True),
            "collision-03": (None, "blocked_missing_input", False, True),
            "collision-08": (None, "blocked_missing_input", False, True),
            "collision-09": (None, "not_applicable", False, False),
            "collision-14": (None, "not_applicable", False, False),
            "collision-20": (None, "not_applicable", False, False),
            "collision-33": (None, "not_applicable", False, False),
            "collision-38": (
                "aoa-decision-find",
                "blocked_missing_input",
                False,
                True,
            ),
            "collision-42": (
                "aoa-eval-select",
                "blocked_missing_input",
                False,
                True,
            ),
            "collision-49": (None, "not_applicable", False, False),
            "desc-titan-03-manual": (None, "not_applicable", False, False),
        }
        expected_outcomes = {
            "collision-01": "request_parser_checks_and_stable_truth",
            "collision-03": "request_owner_context_and_interface_evidence",
            "collision-08": "request_owner_repo_route_and_target_diff",
            "collision-09": "require_explicit_gate_invocation_before_dns_action",
            "collision-14": "require_explicit_invocation_and_atm10_owner_route",
            "collision-20": "require_explicit_invocation_and_reviewed_artifact",
            "collision-33": "require_explicit_invocation_before_child_lane",
            "collision-38": "inspect_graph_status_and_narrow_impact_packet",
            "collision-42": "inspect_target_eval_surfaces_before_classification",
            "collision-49": "require_explicit_invocation_before_trust_loop",
            "desc-titan-03-manual": "require_explicit_invocation_before_bridge_work",
        }
        self.assertEqual(22, len(implicit))
        self.assertEqual(set(expected), {trial.case_id for trial in implicit})
        self.assertEqual(set(expected), set(expected_outcomes))
        for trial in implicit:
            with self.subTest(case_id=trial.case_id, arm=trial.arm_type):
                self.assertIsNotNone(trial.procedure_contract)
                self.assertIsNotNone(trial.outcome_contract)
                procedure = trial.procedure_contract
                outcome = trial.outcome_contract
                assert procedure is not None
                assert outcome is not None
                child, disposition, completion, deflection = expected[trial.case_id]
                self.assertEqual(
                    "manual" if disposition == "not_applicable" else "invoke",
                    trial.expected_behavior,
                )
                self.assertEqual(child, procedure.expected_selected_child_skill)
                self.assertEqual(
                    True if child is not None else None,
                    procedure.expected_selected_child_full_read_observed,
                )
                self.assertEqual(
                    disposition,
                    procedure.expected_selected_procedure_disposition,
                )
                self.assertEqual(
                    completion,
                    procedure.expected_selected_procedure_completion_reported,
                )
                self.assertEqual(
                    deflection,
                    procedure.expected_selected_procedure_deflection_reported,
                )
                self.assertTrue(procedure.expected_owner_boundary_present)
                self.assertEqual(
                    "fixture_owner_observable_decision",
                    outcome.scope,
                )
                self.assertEqual(
                    expected_outcomes[trial.case_id],
                    outcome.expected_candidate_value,
                )
                self.assertEqual(
                    tuple(sorted(outcome.candidate_values)),
                    outcome.candidate_values,
                )

        packet = runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "pilot13",
            "model-a",
            "medium",
        )
        self.assertEqual(5, packet["target_route_scored_pair_count"])
        self.assertEqual(11, packet["procedure_contract_pair_count"])
        self.assertEqual(5, packet["procedure_scored_pair_count"])
        self.assertEqual(6, packet["manual_non_activation_pair_count"])
        self.assertTrue(packet["procedure_contract_coverage_complete"])
        self.assertEqual(11, packet["objective_outcome_scored_pair_count"])
        self.assertTrue(packet["objective_outcome_coverage_complete"])

    def test_procedure_contract_match_is_independent_from_route_match(self) -> None:
        runner = self.runner
        contract = runner.ProcedureContract(
            contract_id="independent-outcome-v1",
            case_id="independent-outcome",
            scope="selected_route_procedure_disposition",
            expected_selected_child_skill="aoa-eval-select",
            expected_selected_child_full_read_observed=True,
            expected_selected_procedure_disposition="blocked_missing_input",
            expected_selected_procedure_completion_reported=False,
            expected_selected_procedure_deflection_reported=True,
            expected_owner_boundary_present=True,
            source_refs=("evals/suites/aoa-skill-live-dispatch.plan.json",),
        )
        trial = runner.Trial(
            trial_id="independent-outcome:aided",
            arm_type="implicit_aided",
            case_id="independent-outcome",
            prompt="Choose the bounded route.",
            expected_target_skill="aoa-eval",
            expected_behavior="invoke",
            procedure_contract=contract,
        )
        result = {
            "returncode": 0,
            "final_output": {
                "route_decision": "do_not_use",
                "selected_skill": None,
                "selected_child": None,
                "claims_loaded": False,
                "procedure_disposition": "blocked_missing_input",
                "mutation_authorized": False,
                "proof_authority_claimed": False,
                "promotion_authorized": False,
                "evidence_posture": "candidate_only",
                "next_step": "Provide the missing owner inputs.",
                "owner_boundary": "The fixture is not central proof authority.",
                "verification_steps": ["Keep the result candidate-only."],
                "stop_line": "Stop before inventing missing owner evidence.",
            },
            "usage": {},
            "duration_ms": 1,
            "prompt_visibility_contract_match": True,
            "fixture_filesystem_scope_match": True,
            "procedure_command_observed": True,
            "procedure_command_succeeded": True,
            "verification_observed": True,
            "procedure_contract_match": False,
            "completion_observed": False,
            "deflection_observed": True,
        }

        measure = runner._trial_measure(trial, result)
        self.assertFalse(measure["route_contract_match"])
        self.assertTrue(measure["trajectory_contract_defined"])
        self.assertFalse(measure["trajectory_contract_match"])
        self.assertTrue(measure["procedure_contract_defined"])
        self.assertTrue(measure["procedure_disposition_contract_match"])
        self.assertEqual([], measure["procedure_disposition_mismatch_dimensions"])

    def test_default_plan_and_unconfirmed_run_never_spawn_or_write(self) -> None:
        runner = self.runner
        with tempfile.TemporaryDirectory() as td:
            private_root = Path(td) / "private"
            stdout = io.StringIO()
            with (
                mock.patch.object(runner.subprocess, "run", side_effect=AssertionError("subprocess.run")),
                mock.patch.object(runner.subprocess, "Popen", side_effect=AssertionError("Popen")),
                redirect_stdout(stdout),
            ):
                returncode = runner.main(
                    [
                        "--repo-root",
                        str(REPO_ROOT),
                        "--model",
                        "test-model",
                        "--private-root",
                        str(private_root),
                    ]
                )
            self.assertEqual(0, returncode)
            payload = json.loads(stdout.getvalue())
            self.assertEqual("plan", payload["action"])
            self.assertFalse(payload["live_execution_authorized"])
            self.assertFalse(private_root.exists())

            stdout = io.StringIO()
            with (
                mock.patch.object(runner.subprocess, "run", side_effect=AssertionError("subprocess.run")),
                mock.patch.object(runner.subprocess, "Popen", side_effect=AssertionError("Popen")),
                redirect_stdout(stdout),
            ):
                returncode = runner.main(
                    [
                        "run",
                        "--repo-root",
                        str(REPO_ROOT),
                        "--model",
                        "test-model",
                        "--private-root",
                        str(private_root),
                    ]
                )
            self.assertEqual(2, returncode)
            payload = json.loads(stdout.getvalue())
            self.assertEqual("confirmation_required", payload["status"])
            self.assertFalse(private_root.exists())

    def test_run_cli_returns_nonzero_and_explicit_status_for_incomplete_cohort(self) -> None:
        runner = self.runner

        def invoke(receipt: dict) -> tuple[int, dict]:
            stdout = io.StringIO()
            with (
                mock.patch.object(runner, "build_plan_packet", return_value={}),
                mock.patch.object(runner, "run_confirmed_cohort", return_value=receipt),
                redirect_stdout(stdout),
            ):
                returncode = runner.main(
                    [
                        "run",
                        "--repo-root",
                        str(REPO_ROOT),
                        "--model",
                        "test-model",
                        "--confirm-live",
                        "confirmed",
                    ]
                )
            return returncode, json.loads(stdout.getvalue())

        completed = {
            "run_id": "run-completed",
            "raw_bundle_sha256": "a" * 64,
            "trials": [{}, {}, {}, {}],
            "stopped_early": False,
            "stop_reason": None,
        }
        returncode, payload = invoke(completed)
        self.assertEqual(0, returncode)
        self.assertEqual("completed", payload["status"])
        self.assertFalse(payload["stopped_early"])
        self.assertIsNone(payload["stop_reason"])

        incomplete = {
            **completed,
            "run_id": "run-incomplete",
            "trials": [{}],
            "stopped_early": True,
            "stop_reason": "transport_failure",
        }
        returncode, payload = invoke(incomplete)
        self.assertEqual(1, returncode)
        self.assertEqual("stopped_early", payload["status"])
        self.assertTrue(payload["stopped_early"])
        self.assertEqual("transport_failure", payload["stop_reason"])

    def test_confirmation_token_binds_head_model_effort_caps_and_sources(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        first = self.runner.build_plan_packet(REPO_ROOT, plan, "smoke", "model-a", "medium")
        second = self.runner.build_plan_packet(REPO_ROOT, plan, "smoke", "model-b", "medium")
        third = self.runner.build_plan_packet(REPO_ROOT, plan, "smoke", "model-a", "high")
        self.assertNotEqual(first["confirmation_token"], second["confirmation_token"])
        self.assertNotEqual(first["confirmation_token"], third["confirmation_token"])
        self.assertEqual(64, len(first["head_commit"]))
        self.assertEqual(64, len(first["plan_sha256"]))
        self.assertEqual(64, len(first["source_snapshot_sha256"]))
        self.assertEqual(48_000, first["caps"]["per_turn_weighted_token_limit"])
        self.assertEqual(48_000, first["caps"]["trajectory_weighted_token_limit"])
        self.assertEqual([4_000], first["caps"]["rollout_budget_reminder_at_remaining_tokens"])
        self.assertEqual(1, first["caps"]["max_concurrency"])
        self.assertGreater(first["source_record_count"], 390)
        self.assertTrue(first["resource_wrapper_required"])
        self.assertEqual(
            ["abyss-machine", "resource", "launch", "--class", "light", "--kind", "agent"],
            first["resource_launch_prefix"][:7],
        )
        pilot = self.runner.build_plan_packet(REPO_ROOT, plan, "pilot13", "model-a", "medium")
        self.assertTrue(pilot["high_cost_confirmation_required"])
        self.assertEqual("required_for_live", pilot["procedure_contract_mode"])
        self.assertEqual(11, pilot["implicit_pair_count"])
        self.assertEqual(5, pilot["target_route_scored_pair_count"])
        self.assertEqual(11, pilot["procedure_contract_pair_count"])
        self.assertEqual(5, pilot["procedure_scored_pair_count"])
        self.assertEqual(6, pilot["manual_non_activation_pair_count"])
        self.assertTrue(pilot["procedure_contract_coverage_complete"])
        self.assertEqual(11, pilot["objective_outcome_scored_pair_count"])
        self.assertTrue(pilot["objective_outcome_coverage_complete"])
        returns = self.runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "pilot13-returns",
            "model-a",
            "medium",
        )
        self.assertTrue(returns["high_cost_confirmation_required"])
        self.assertEqual("required", returns["procedure_contract_mode"])
        self.assertEqual(7, returns["implicit_pair_count"])
        self.assertEqual(1, returns["target_route_scored_pair_count"])
        self.assertEqual(7, returns["procedure_contract_pair_count"])
        self.assertEqual(1, returns["procedure_scored_pair_count"])
        self.assertEqual(6, returns["manual_non_activation_pair_count"])
        self.assertTrue(returns["procedure_contract_coverage_complete"])
        self.assertEqual(7, returns["objective_outcome_scored_pair_count"])
        self.assertTrue(returns["objective_outcome_coverage_complete"])
        skill_returns = self.runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "pilot13-skill-returns",
            "model-a",
            "medium",
        )
        self.assertTrue(skill_returns["high_cost_confirmation_required"])
        self.assertEqual("required", skill_returns["procedure_contract_mode"])
        self.assertEqual(3, skill_returns["implicit_pair_count"])
        self.assertEqual(1, skill_returns["target_route_scored_pair_count"])
        self.assertEqual(3, skill_returns["procedure_contract_pair_count"])
        self.assertEqual(1, skill_returns["procedure_scored_pair_count"])
        self.assertEqual(2, skill_returns["manual_non_activation_pair_count"])
        self.assertTrue(skill_returns["procedure_contract_coverage_complete"])
        self.assertEqual(3, skill_returns["objective_outcome_scored_pair_count"])
        self.assertTrue(skill_returns["objective_outcome_coverage_complete"])

    def test_high_cost_live_run_blocks_before_preflight_when_procedures_are_incomplete(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        transport = FakeTransport()
        packet = {
            "confirmation_token": "confirmed",
            "high_cost_confirmation_required": False,
            "procedure_contract_mode": "required_for_live",
            "procedure_contract_coverage_complete": False,
            "procedure_contract_pair_count": 0,
            "procedure_scored_pair_count": 0,
            "objective_outcome_mode": "required_for_live",
            "objective_outcome_coverage_complete": True,
            "objective_outcome_scored_pair_count": 11,
            "implicit_pair_count": 11,
        }

        with tempfile.TemporaryDirectory() as td:
            with (
                mock.patch.object(runner, "build_plan_packet", return_value=packet),
                self.assertRaisesRegex(
                    runner.ConfirmationError,
                    "pilot13 requires source-locked procedure contracts for all 11 implicit pairs",
                ),
            ):
                runner.run_confirmed_cohort(
                    repo_root=REPO_ROOT,
                    plan=plan,
                    cohort="pilot13",
                    model="model-a",
                    effort="medium",
                    confirmation_token="confirmed",
                    high_cost_token=None,
                    private_root=Path(td),
                    transport=transport,
                    test_only_allow_noncanonical_private_root=True,
                )
        self.assertEqual([], transport.preflight_calls)

    def test_pilot_blocks_before_preflight_without_objective_outcome_surfaces(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        transport = FakeTransport()
        packet = {
            "confirmation_token": "confirmed",
            "high_cost_confirmation_required": False,
            "procedure_contract_mode": "required_for_live",
            "procedure_contract_coverage_complete": True,
            "procedure_contract_pair_count": 11,
            "procedure_scored_pair_count": 11,
            "objective_outcome_mode": "required_for_live",
            "objective_outcome_coverage_complete": False,
            "objective_outcome_scored_pair_count": 0,
            "implicit_pair_count": 11,
        }
        with (
            mock.patch.object(runner, "build_plan_packet", return_value=packet),
            tempfile.TemporaryDirectory() as td,
            self.assertRaisesRegex(
                runner.ConfirmationError,
                "pilot13 requires objective outcome observations for all 11 implicit pairs",
            ),
        ):
            runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="pilot13",
                model="model-a",
                effort="medium",
                confirmation_token="confirmed",
                high_cost_token=None,
                private_root=Path(td),
                transport=transport,
                test_only_allow_noncanonical_private_root=True,
            )
        self.assertEqual([], transport.preflight_calls)

    def test_confirmation_token_binds_discovered_shadow_skill_set(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        first_shadow_set = (Path("/external/skills/aoa-eval/SKILL.md"),)
        second_shadow_set = (
            Path("/external/skills/aoa-decision/SKILL.md"),
            Path("/external/skills/aoa-eval/SKILL.md"),
        )

        with mock.patch.object(
            runner,
            "discover_shadowing_skill_paths",
            return_value=first_shadow_set,
        ):
            first = runner.build_plan_packet(REPO_ROOT, plan, "smoke", "model-a", "medium")
        with mock.patch.object(
            runner,
            "discover_shadowing_skill_paths",
            return_value=second_shadow_set,
        ):
            second = runner.build_plan_packet(REPO_ROOT, plan, "smoke", "model-a", "medium")

        self.assertEqual(1, first["shadow_skill_count"])
        self.assertEqual(2, second["shadow_skill_count"])
        self.assertNotEqual(first["shadow_skill_set_sha256"], second["shadow_skill_set_sha256"])
        self.assertNotEqual(first["confirmation_token"], second["confirmation_token"])

    def test_shadow_discovery_follows_user_skill_symlink_to_canonical_target(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            codex_home = root / "codex-home"
            target = root / "source" / "aoa-eval"
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("---\nname: aoa-eval\n---\n", encoding="utf-8")
            skill_root = codex_home / "skills"
            skill_root.mkdir(parents=True)
            (skill_root / "aoa-eval").symlink_to(target, target_is_directory=True)

            discovered = self.runner.discover_shadowing_skill_paths(
                REPO_ROOT,
                codex_home=codex_home,
            )

        self.assertEqual((target / "SKILL.md",), discovered)

    def test_configured_mcp_inventory_is_sorted_and_lockable(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            codex_home = Path(td)
            (codex_home / "config.toml").write_text(
                "[mcp_servers.zeta]\ncommand='z'\n"
                "[mcp_servers.alpha]\ncommand='a'\n",
                encoding="utf-8",
            )
            names = self.runner.discover_configured_mcp_server_names(
                codex_home=codex_home
            )

        self.assertEqual(("alpha", "zeta"), names)
        lock = self.runner._configured_mcp_server_lock(names)
        self.assertEqual(2, lock["configured_mcp_server_count"])
        self.assertEqual(64, len(lock["configured_mcp_server_set_sha256"]))

        plan = self.runner.load_plan(self.plan_path)
        with (
            mock.patch.object(
                self.runner,
                "discover_shadowing_skill_paths",
                return_value=(),
            ),
            mock.patch.object(
                self.runner,
                "discover_configured_mcp_server_names",
                return_value=("alpha",),
            ),
        ):
            first = self.runner.build_plan_packet(
                REPO_ROOT, plan, "smoke", "model-a", "medium"
            )
        with (
            mock.patch.object(
                self.runner,
                "discover_shadowing_skill_paths",
                return_value=(),
            ),
            mock.patch.object(
                self.runner,
                "discover_configured_mcp_server_names",
                return_value=("alpha", "zeta"),
            ),
        ):
            second = self.runner.build_plan_packet(
                REPO_ROOT, plan, "smoke", "model-a", "medium"
            )
        self.assertNotEqual(first["confirmation_token"], second["confirmation_token"])

    def test_protocol_contract_matches_plan_and_installed_version_lock(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        contract = json.loads(
            (REPO_ROOT / plan["sources"]["protocol_contract"]).read_text(encoding="utf-8")
        )
        self.assertEqual(plan["protocol_revision"], contract["protocol_revision"])
        self.assertEqual(
            "codex-cli-0.144.1-live-dispatch-evidence-v20",
            plan["protocol_revision"],
        )
        self.assertEqual("codex-cli 0.144.1", self.runner._expected_codex_version(plan))
        unsupported_plan = dict(plan)
        unsupported_plan["protocol_revision"] = (
            "codex-cli-0.144.1-live-dispatch-evidence-v21"
        )
        with self.assertRaisesRegex(ValueError, "unsupported Codex protocol revision"):
            self.runner._expected_codex_version(unsupported_plan)
        self.assertEqual(
            "aoa_codex_app_server_skill_input_contract_v14",
            contract["schema_version"],
        )
        self.assertEqual("codex-cli 0.144.1", contract["codex_version"])
        self.assertIn(
            "codex debug models",
            contract["preturn_isolation"]["model_catalog"],
        )
        self.assertEqual(
            "https://learn.chatgpt.com/docs/app-server#start-a-turn-invoke-a-skill",
            contract["official_contract_ref"],
        )
        self.assertIn(
            "$<skill-name>", contract["structured_input_binding"]["text_item"]
        )
        self.assertIn(
            "same exact fixture name and path",
            contract["structured_input_binding"]["skill_item"],
        )
        self.assertIn(
            "do not gate objective load evidence",
            contract["evidence_binding"]["model_load_claim"],
        )
        self.assertIn(
            "external or repo-visible ambient route",
            contract["evidence_binding"]["reported_selection_surface"],
        )
        self.assertIn(
            "not target-route scoring evidence",
            contract["evidence_binding"]["native_hidden_manual_target"],
        )
        self.assertIn(
            "prompt-visible parent",
            contract["evidence_binding"]["parent_authorized_hidden_child"],
        )
        self.assertIn(
            "separate trajectory evidence",
            contract["evidence_binding"]["parent_authorized_hidden_child"],
        )
        self.assertIn(
            "must be false when selected_skill is null",
            contract["evidence_binding"]["target_report_semantics"],
        )
        self.assertIn(
            "read-only skill-file inspection commands",
            contract["evidence_binding"]["read_command_boundary"],
        )
        self.assertIn(
            "ordered successful exact-path outputs",
            contract["evidence_binding"]["full_read_assembly"],
        )
        self.assertIn(
            "preserves elapsed milliseconds",
            contract["evidence_binding"]["transport_failure_duration"],
        )
        self.assertIn(
            "partial timeout stdout and stderr",
            contract["evidence_binding"]["transport_partial_evidence"],
        )
        self.assertIn(
            "stopped-early incomplete cohort",
            contract["evidence_binding"]["cohort_process_status"],
        )
        self.assertIn(
            "dynamically selected child",
            contract["evidence_binding"]["selected_child"],
        )
        self.assertIn(
            "unrelated root",
            contract["evidence_binding"]["native_dispatch_boundary"],
        )
        self.assertIn(
            "outside the fixture root",
            contract["evidence_binding"]["fixture_filesystem_scope"],
        )
        self.assertEqual(
            ["initialize", "initialized", "skills/list", "thread/start", "turn/start", "thread/delete"],
            contract["request_sequence"],
        )
        self.assertEqual(10, len(contract["schema_sha256"]))
        self.assertFalse(contract["proof_authority"])
        output_schema = self.load_schema("live-skill-dispatch-model-output.schema.json")
        self.assertIn(
            "background ambient skill",
            output_schema["properties"]["selected_skill"]["description"],
        )
        self.assertIn(
            "expected target skill procedure",
            output_schema["properties"]["procedure_disposition"]["description"],
        )

    def test_arm_adapters_are_exact_read_only_and_never_use_dangerous_flags(self) -> None:
        runner = self.runner
        context = runner.AdapterContext(
            repo_root=REPO_ROOT,
            fixture_root=Path("/private/fixture"),
            output_schema_path=REPO_ROOT / "schemas" / "live-skill-dispatch-model-output.schema.json",
            final_output_path=Path("/private/final.json"),
            model="test-model",
            effort="medium",
            weighted_token_limit=28_000,
            rollout_budget_reminder_at_remaining_tokens=(4_000,),
            timeout_seconds=180,
            full_timeout_seconds=240,
            disabled_skill_paths=(Path("/global/aoa-eval/SKILL.md"),),
            disabled_mcp_server_names=("aoa_evals",),
        )
        implicit = runner.build_implicit_cli_request(
            context,
            prompt="Decide the route.",
            target_skill="aoa-eval",
            expected_behavior="invoke",
            control=False,
        )
        trajectory = runner.build_root_manual_child_request(
            context,
            prompt="The validator is already selected.",
            root_skill="aoa-eval",
            child_skill="aoa-eval-apply",
        )
        structured = runner.build_app_server_structured_request(
            context,
            prompt="Apply the selected validator route.",
            skill_name="aoa-eval-apply",
            skill_path=Path("/private/fixture/.agents/skills/aoa-eval-apply/SKILL.md"),
        )
        prompt_inspection = runner.build_prompt_skill_inspection_request(
            context,
            prompt="Decide the route.",
            expected_prompt_skill_paths={
                "aoa-eval": ["/private/fixture/.agents/skills/aoa-eval/SKILL.md"]
            },
        )

        self.assertIn("--ephemeral", implicit["argv"])
        self.assertIn("--ignore-user-config", implicit["argv"])
        self.assertIn("read-only", implicit["argv"])
        self.assertIn(
            "Do not inspect or search any path outside this fixture root",
            implicit["prompt"],
        )
        self.assertIn(
            "Do not enumerate, recursively list, or hash the fixture tree",
            implicit["prompt"],
        )
        self.assertIn(
            "`route_decision` concerns the expected target skill only",
            implicit["prompt"],
        )
        self.assertIn("background or ambient skill", implicit["prompt"])
        self.assertIn(
            "`claims_loaded` must be `false` when `selected_skill` is `null`",
            implicit["prompt"],
        )
        self.assertIn(
            "`procedure_disposition` describes the target skill procedure",
            implicit["prompt"],
        )
        self.assertTrue(trajectory["prompt"].startswith("$aoa-eval "))
        self.assertIn(
            "Read-only skill-file inspection commands are allowed",
            trajectory["prompt"],
        )
        self.assertIn(
            "independent fixture-execution probe",
            trajectory["prompt"],
        )
        self.assertIn(
            "complete selected child `SKILL.md`",
            trajectory["prompt"],
        )
        self.assertTrue(
            runner._native_cli_target_input_accepted(
                trajectory, [{"type": "turn.started"}]
            )
        )
        self.assertFalse(
            runner._native_cli_target_input_accepted(
                implicit, [{"type": "turn.started"}]
            )
        )
        expected_skill_override = (
            'skills.config=[{path="/global/aoa-eval/SKILL.md",enabled=false}]'
        )
        for request in (implicit, trajectory, structured):
            with self.subTest(adapter=request["arm_type"]):
                self.assertEqual(
                    [expected_skill_override],
                    [arg for arg in request["argv"] if arg.startswith("skills.config=")],
                )
                self.assertNotIn("shell_tool", request["argv"])
                self.assertIn("plugins", request["argv"])
        for request in (implicit, trajectory):
            with self.subTest(
                adapter=request["arm_type"], mcp_isolation="ignore-user-config"
            ):
                self.assertIn("--ignore-user-config", request["argv"])
                self.assertNotIn(
                    "mcp_servers.aoa_evals.enabled=false",
                    request["argv"],
                )
        for adapter, request in (
            ("prompt_inspection", prompt_inspection),
            ("app_server_structured", structured),
        ):
            with self.subTest(adapter=adapter, mcp_isolation="explicit-disable"):
                self.assertNotIn("--ignore-user-config", request["argv"])
                self.assertIn(
                    "mcp_servers.aoa_evals.enabled=false",
                    request["argv"],
                )
        reminder_override = "features.rollout_budget.reminder_at_remaining_tokens=[4000]"
        self.assertIn(reminder_override, implicit["argv"])
        self.assertIn(reminder_override, trajectory["argv"])
        self.assertIn(reminder_override, structured["argv"])
        flattened = json.dumps([implicit, trajectory, structured])
        self.assertNotIn("dangerously-bypass", flattened)
        self.assertNotIn("threadId", structured["turn_start_params"])
        self.assertEqual("skill", structured["turn_start_params"]["input"][1]["type"])
        self.assertEqual("aoa-eval-apply", structured["turn_start_params"]["input"][1]["name"])
        self.assertEqual("readOnly", structured["turn_start_params"]["sandboxPolicy"]["type"])
        self.assertTrue(
            structured["turn_start_params"]["input"][0]["text"].startswith(
                "$aoa-eval-apply "
            )
        )
        self.assertEqual(
            1,
            structured["turn_start_params"]["input"][0]["text"].count(
                "$aoa-eval-apply"
            ),
        )
        self.assertEqual("thread/start", structured["thread_start_request"]["method"])
        self.assertEqual(180, implicit["timeout_seconds"])
        self.assertEqual(180, trajectory["timeout_seconds"])
        self.assertEqual(240, structured["timeout_seconds"])

        with self.assertRaisesRegex(ValueError, "source prompt.*textual skill activation"):
            runner.build_app_server_structured_request(
                context,
                prompt="Use $aoa-eval-apply for this route.",
                skill_name="aoa-eval-apply",
                skill_path=Path(
                    "/private/fixture/.agents/skills/aoa-eval-apply/SKILL.md"
                ),
            )

        directory_selector_context = dataclasses.replace(
            context,
            disabled_skill_paths=(Path("/global/aoa-eval"),),
        )
        with self.assertRaisesRegex(ValueError, "absolute SKILL.md file paths"):
            runner.build_implicit_cli_request(
                directory_selector_context,
                prompt="Decide the route.",
                target_skill="aoa-eval",
                expected_behavior="invoke",
                control=False,
            )

        for invalid_reminders in ((), (0,), (28_000,)):
            invalid_context = dataclasses.replace(
                context,
                rollout_budget_reminder_at_remaining_tokens=invalid_reminders,
            )
            with self.subTest(invalid_reminders=invalid_reminders):
                with self.assertRaisesRegex(ValueError, "positive and below the token limit"):
                    runner.build_implicit_cli_request(
                        invalid_context,
                        prompt="Decide the route.",
                        target_skill="aoa-eval",
                        expected_behavior="invoke",
                        control=False,
                    )

    def test_model_visible_skill_parser_resolves_aliases_and_duplicate_names(self) -> None:
        skills_instructions = """<skills_instructions>
## Skills
### Skill roots
- `r0` = `/home/tester/.codex/skills`
- `r10` = `/private/fixture/.agents/skills`
### Available skills
- aoa-eval: fixture route (file: r10/aoa-eval/SKILL.md)
- aoa-eval: user-installed shadow (file: r0/aoa-eval/SKILL.md)
- aoa-decision: fixture decision route (file: r10/aoa-decision/SKILL.md)
</skills_instructions>"""
        payload = [
            {
                "type": "message",
                "role": "developer",
                "content": [{"type": "input_text", "text": skills_instructions}],
            }
        ]

        self.assertEqual(
            {
                "aoa-decision": (
                    "/private/fixture/.agents/skills/aoa-decision/SKILL.md",
                ),
                "aoa-eval": (
                    "/home/tester/.codex/skills/aoa-eval/SKILL.md",
                    "/private/fixture/.agents/skills/aoa-eval/SKILL.md",
                ),
            },
            self.runner._parse_model_visible_skill_paths(payload),
        )
        _inventory, first_fingerprints = self.runner._parse_model_visible_skill_surface(payload)
        changed_payload = json.loads(json.dumps(payload))
        changed_payload[0]["content"][0]["text"] = skills_instructions.replace(
            "fixture decision route",
            "changed decision route",
        )
        changed_inventory, changed_fingerprints = self.runner._parse_model_visible_skill_surface(
            changed_payload
        )
        self.assertEqual(
            self.runner._parse_model_visible_skill_paths(payload),
            changed_inventory,
        )
        self.assertNotEqual(
            first_fingerprints["aoa-decision"],
            changed_fingerprints["aoa-decision"],
        )

    def test_confirmed_mock_run_writes_private_receipt_but_no_public_raw_data(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        packet = runner.build_plan_packet(REPO_ROOT, plan, "smoke", "test-model", "medium")
        transport = FakeTransport()
        with tempfile.TemporaryDirectory() as td:
            private_root = Path(td) / "private"
            receipt = runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="smoke",
                model="test-model",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=None,
                private_root=private_root,
                transport=transport,
                test_only_allow_noncanonical_private_root=True,
            )
            self.assertEqual(1, len(transport.preflight_calls))
            self.assertEqual(4, len(transport.prompt_inspection_calls))
            self.assertEqual(3, len(transport.cli_calls))
            self.assertEqual(1, len(transport.app_server_calls))
            implicit_requests = [
                call
                for call in transport.cli_calls
                if call["arm_type"] in {"implicit_aided", "implicit_control"}
            ]
            trajectory_request = next(call for call in transport.cli_calls if call["arm_type"] == "root_manual_child")

            self.assertEqual(2, len(implicit_requests))
            for implicit_request in implicit_requests:
                self.assertIn("features.rollout_budget.limit_tokens=48000", implicit_request["argv"])
            self.assertIn("features.rollout_budget.limit_tokens=48000", trajectory_request["argv"])
            self.assertEqual(1, len(receipt["pair_outcomes"]))
            self.assertEqual("positive_lift", receipt["pair_outcomes"][0]["route_effect_class"])
            self.assertEqual(
                "positive_lift",
                receipt["pair_outcomes"][0]["trajectory_effect_class"],
            )
            self.assertEqual(1, receipt["pair_outcomes"][0]["trajectory_lift"])
            self.assertEqual(
                0,
                receipt["pair_outcomes"][0]["procedure_disposition_lift"],
            )
            self.assertEqual(
                "no_lift_both_correct",
                receipt["pair_outcomes"][0]["procedure_disposition_effect_class"],
            )
            self.assertEqual(
                "selected_route_procedure_disposition",
                receipt["pair_outcomes"][0]["procedure_contract_scope"],
            )
            self.assertEqual(0, receipt["pair_outcomes"][0]["outcome_lift"])
            self.assertEqual(
                "no_lift_both_correct",
                receipt["pair_outcomes"][0]["outcome_effect_class"],
            )
            self.assertTrue(
                all(
                    item["measure"]["fixture_execution_contract_match"]
                    for item in receipt["trials"]
                )
            )
            receipt_path = private_root / receipt["run_id"] / "private-receipt.json"
            self.assertTrue(receipt_path.is_file())
            self.assertEqual(0o700, private_root.stat().st_mode & 0o777)
            self.assertEqual(0o700, receipt_path.parent.stat().st_mode & 0o777)
            self.assertEqual(0o600, receipt_path.stat().st_mode & 0o777)
            trajectory_guidance = (
                receipt_path.parent / "fixtures" / "fixture-002" / "AGENTS.md"
            ).read_text(encoding="utf-8")
            self.assertIn(
                "Read-only skill-file inspection commands are allowed",
                trajectory_guidance,
            )
            self.assertIn(
                "They are load evidence, not the independent fixture-execution probe",
                trajectory_guidance,
            )
            self.assertIn(
                "Do not inspect or search any path outside this fixture root",
                trajectory_guidance,
            )
            self.assertIn(
                "Do not enumerate, recursively list, or hash the fixture tree",
                trajectory_guidance,
            )
            for path in receipt_path.parent.rglob("*"):
                self.assertEqual(0o700 if path.is_dir() else 0o600, path.stat().st_mode & 0o777)
            Draft202012Validator(
                self.load_schema("live-skill-dispatch-private-receipt.schema.json")
            ).validate(receipt)

            public = runner.build_public_receipt(receipt)
            runner.validate_public_receipt(public)
            self.assertTrue(public["measures"][0]["fixture_filesystem_scope_match"])
            self.assertEqual(0, public["measures"][0]["external_filesystem_access_count"])
            self.assertTrue(public["measures"][0]["fixture_inventory_scope_match"])
            self.assertEqual(
                0,
                public["measures"][0]["broad_fixture_inventory_command_count"],
            )
            Draft202012Validator(
                self.load_schema("live-skill-dispatch-public-receipt.schema.json")
            ).validate(public)
            rendered = json.dumps(public)
            self.assertNotIn("Decide the route", rendered)
            self.assertNotIn(str(private_root), rendered)
            self.assertNotIn("final_output", rendered)

            legacy_receipt = json.loads(json.dumps(receipt))
            legacy_receipt["caps"].pop("rollout_budget_reminder_at_remaining_tokens")
            legacy_public = runner.build_public_receipt(legacy_receipt)
            self.assertNotIn("rollout_budget_reminder_at_remaining_tokens", legacy_public["caps"])
            Draft202012Validator(
                self.load_schema("live-skill-dispatch-public-receipt.schema.json")
            ).validate(legacy_public)

    def test_pilot_return_private_and_public_receipt_schemas_accept_the_cohort(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        packet = runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "pilot13-returns",
            "test-model",
            "medium",
        )
        with tempfile.TemporaryDirectory() as td:
            receipt = runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="pilot13-returns",
                model="test-model",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=packet["high_cost_confirmation_token"],
                private_root=Path(td),
                transport=FakeTransport(),
                test_only_allow_noncanonical_private_root=True,
            )
        private_schema = self.load_schema(
            "live-skill-dispatch-private-receipt.schema.json"
        )
        Draft202012Validator(private_schema).validate(receipt)
        receipt["review"] = {
            "status": "needs-rerun",
            "note": "bounded synthetic receipt schema coverage",
        }
        public = runner.build_public_receipt(receipt)
        public_schema = self.load_schema(
            "live-skill-dispatch-public-receipt.schema.json"
        )
        Draft202012Validator(public_schema).validate(public)
        runner.validate_public_receipt(public)
        self.assertEqual("pilot13-returns", public["cohort"])
        self.assertEqual(15, public["trial_count"])

    def test_core_partition_private_and_public_receipt_schemas_accept_the_cohort(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        packet = runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "full-collision-core-engineering",
            "test-model",
            "medium",
        )
        with tempfile.TemporaryDirectory() as td:
            receipt = runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="full-collision-core-engineering",
                model="test-model",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=packet["high_cost_confirmation_token"],
                private_root=Path(td),
                transport=FakeTransport(),
                test_only_allow_noncanonical_private_root=True,
            )
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-private-receipt.schema.json")
        ).validate(receipt)
        receipt["review"] = {
            "status": "reviewed",
            "note": "bounded synthetic core partition schema coverage",
        }
        public = runner.build_public_receipt(receipt)
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-public-receipt.schema.json")
        ).validate(public)
        runner.validate_public_receipt(public)
        self.assertEqual("full-collision-core-engineering", public["cohort"])
        self.assertEqual(16, public["trial_count"])
        self.assertEqual(8, public["pair_count"])

    def test_skill_return_private_and_public_receipt_schemas_accept_the_cohort(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        packet = runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "pilot13-skill-returns",
            "test-model",
            "medium",
        )
        with tempfile.TemporaryDirectory() as td:
            receipt = runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="pilot13-skill-returns",
                model="test-model",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=packet["high_cost_confirmation_token"],
                private_root=Path(td),
                transport=FakeTransport(),
                test_only_allow_noncanonical_private_root=True,
            )
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-private-receipt.schema.json")
        ).validate(receipt)
        receipt["review"] = {
            "status": "needs-rerun",
            "note": "bounded skill-return receipt schema coverage",
        }
        public = runner.build_public_receipt(receipt)
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-public-receipt.schema.json")
        ).validate(public)
        runner.validate_public_receipt(public)
        self.assertEqual("pilot13-skill-returns", public["cohort"])
        self.assertEqual(6, public["trial_count"])

    def test_prompt_visibility_contamination_stops_before_any_model_turn(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        packet = runner.build_plan_packet(REPO_ROOT, plan, "smoke", "test-model", "medium")

        class ContaminatedPromptTransport(FakeTransport):
            def inspect_prompt_skills(self, request: dict) -> dict:
                payload = super().inspect_prompt_skills(request)
                inventory = {
                    name: list(paths)
                    for name, paths in payload["inventory"].items()
                }
                inventory.setdefault("aoa-eval", []).append(
                    "/home/tester/.codex/skills/aoa-eval/SKILL.md"
                )
                payload["inventory"] = inventory
                return payload

        transport = ContaminatedPromptTransport()
        with tempfile.TemporaryDirectory() as td:
            receipt = runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="smoke",
                model="test-model",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=None,
                private_root=Path(td),
                transport=transport,
                test_only_allow_noncanonical_private_root=True,
            )

        self.assertEqual(1, len(transport.preflight_calls))
        self.assertEqual(1, len(transport.prompt_inspection_calls))
        self.assertEqual([], transport.cli_calls)
        self.assertEqual([], transport.app_server_calls)
        self.assertTrue(receipt["stopped_early"])
        self.assertEqual("harness_contamination", receipt["stop_reason"])
        self.assertEqual(
            "harness_contamination",
            receipt["trials"][0]["measure"]["failure_class"],
        )

    def test_transport_timeout_preserves_observed_duration_before_early_stop(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        packet = runner.build_plan_packet(REPO_ROOT, plan, "smoke", "test-model", "medium")

        class TimeoutTransport(FakeTransport):
            def run_cli(self, request: dict) -> dict:
                raise runner.subprocess.TimeoutExpired(
                    request["argv"],
                    180,
                    output='{"type":"turn.started"}\n',
                    stderr="transport remained pending",
                )

        with tempfile.TemporaryDirectory() as td:
            with mock.patch.object(
                runner.time,
                "monotonic",
                side_effect=[100.0, 280.125],
            ):
                receipt = runner.run_confirmed_cohort(
                    repo_root=REPO_ROOT,
                    plan=plan,
                    cohort="smoke",
                    model="test-model",
                    effort="medium",
                    confirmation_token=packet["confirmation_token"],
                    high_cost_token=None,
                    private_root=Path(td),
                    transport=TimeoutTransport(),
                    test_only_allow_noncanonical_private_root=True,
                )

        result = receipt["trials"][0]["result"]
        measure = receipt["trials"][0]["measure"]
        self.assertTrue(receipt["stopped_early"])
        self.assertEqual("transport_failure", receipt["stop_reason"])
        self.assertEqual("transport_failure", measure["failure_class"])
        self.assertEqual(180125, measure["duration_ms"])
        self.assertEqual([{"type": "turn.started"}], result["events"])
        self.assertTrue(result["turn_started"])
        self.assertIn("transport remained pending", result["stderr"])

    def test_public_validator_rejects_paths_credentials_raw_text_and_session_ids(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        packet = runner.build_plan_packet(REPO_ROOT, plan, "smoke", "test-model", "medium")
        transport = FakeTransport()
        with tempfile.TemporaryDirectory() as td:
            receipt = runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="smoke",
                model="test-model",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=None,
                private_root=Path(td),
                transport=transport,
                test_only_allow_noncanonical_private_root=True,
            )
        base = runner.build_public_receipt(receipt)
        attacks = (
            "ref=/srv/private/operator-secret",
            "sk-proj-secretvalue123456789",
            "Bearer abcdefghijklmnop",
            "turn_457",
            "019e9388-dc4c-7f82-b6bf-04bea3aed7f4",
        )
        for attack in attacks:
            with self.subTest(attack=attack):
                candidate = json.loads(json.dumps(base))
                candidate["model"] = attack
                with self.assertRaises(runner.PublicReceiptSafetyError):
                    runner.validate_public_receipt(candidate)

        forbidden_key = json.loads(json.dumps(base))
        forbidden_key["review"]["note"] = "bounded text"
        with self.assertRaises(runner.PublicReceiptSafetyError):
            runner.validate_public_receipt(forbidden_key)

    def test_public_validator_distinguishes_typed_skill_names_from_transport_ids(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        packet = runner.build_plan_packet(REPO_ROOT, plan, "smoke", "test-model", "medium")
        with tempfile.TemporaryDirectory() as td:
            receipt = runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="smoke",
                model="test-model",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=None,
                private_root=Path(td),
                transport=FakeTransport(),
                test_only_allow_noncanonical_private_root=True,
            )
        public = runner.build_public_receipt(receipt)
        public["measures"][0]["expected_target_skill"] = "aoa-session-donor-harvest"
        public["pair_outcomes"][0]["expected_target_skill"] = (
            "aoa-session-donor-harvest"
        )
        runner.validate_public_receipt(public)

        leaked = json.loads(json.dumps(public))
        leaked["measures"][0]["expected_target_skill"] = "session-deadbeef"
        with self.assertRaises(runner.PublicReceiptSafetyError):
            runner.validate_public_receipt(leaked)

        public["cohort"] = "full-collision-session-growth"
        runner.validate_public_receipt(public)

        leaked = json.loads(json.dumps(public))
        leaked["cohort"] = "session-deadbeef"
        with self.assertRaises(runner.PublicReceiptSafetyError):
            runner.validate_public_receipt(leaked)

    def test_review_cli_blocks_public_write_outside_reports_without_traceback(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        packet = runner.build_plan_packet(REPO_ROOT, plan, "smoke", "test-model", "medium")
        with tempfile.TemporaryDirectory() as td:
            private_root = Path(td) / "private"
            receipt = runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="smoke",
                model="test-model",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=None,
                private_root=private_root,
                transport=FakeTransport(),
                test_only_allow_noncanonical_private_root=True,
            )
            receipt_path = private_root / receipt["run_id"] / "private-receipt.json"
            outside_path = Path(td) / "public.json"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                returncode = runner.main(
                    [
                        "review",
                        "--repo-root",
                        str(REPO_ROOT),
                        "--receipt",
                        str(receipt_path),
                        "--review-status",
                        "reviewed",
                        "--write-public",
                        str(outside_path),
                    ]
                )
            self.assertEqual(2, returncode)
            self.assertEqual("blocked", json.loads(stdout.getvalue())["status"])
            self.assertFalse(outside_path.exists())

    def test_high_cost_cohorts_need_second_exact_token_before_preflight(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        packet = runner.build_plan_packet(REPO_ROOT, plan, "full-collision", "test-model", "medium")
        transport = FakeTransport()
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(runner.ConfirmationError):
                runner.run_confirmed_cohort(
                    repo_root=REPO_ROOT,
                    plan=plan,
                    cohort="full-collision",
                    model="test-model",
                    effort="medium",
                    confirmation_token=packet["confirmation_token"],
                    high_cost_token=None,
                    private_root=Path(td),
                    transport=transport,
                    test_only_allow_noncanonical_private_root=True,
                )
        self.assertEqual([], transport.preflight_calls)

    def test_noncanonical_private_root_and_each_failed_preflight_gate_fail_closed(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        packet = runner.build_plan_packet(REPO_ROOT, plan, "smoke", "test-model", "medium")
        transport = FakeTransport()
        with tempfile.TemporaryDirectory() as td:
            private_root = Path(td) / "private"
            with self.assertRaises(runner.ConfirmationError):
                runner.run_confirmed_cohort(
                    repo_root=REPO_ROOT,
                    plan=plan,
                    cohort="smoke",
                    model="test-model",
                    effort="medium",
                    confirmation_token=packet["confirmation_token"],
                    high_cost_token=None,
                    private_root=private_root,
                    transport=transport,
                )
            self.assertEqual([], transport.preflight_calls)
            self.assertFalse(private_root.exists())

        for denied_gate in ("storage", "resource", "runtime", "allowed"):
            with self.subTest(denied_gate=denied_gate), tempfile.TemporaryDirectory() as td:
                class DeniedTransport(FakeTransport):
                    def preflight(self, request: dict) -> dict:
                        payload = super().preflight(request)
                        if denied_gate == "allowed":
                            payload["allowed"] = False
                        else:
                            payload[denied_gate]["decision"] = "deny"
                        return payload

                denied = DeniedTransport()
                private_root = Path(td) / "private"
                with self.assertRaises(runner.ConfirmationError):
                    runner.run_confirmed_cohort(
                        repo_root=REPO_ROOT,
                        plan=plan,
                        cohort="smoke",
                        model="test-model",
                        effort="medium",
                        confirmation_token=packet["confirmation_token"],
                        high_cost_token=None,
                        private_root=private_root,
                        transport=denied,
                        test_only_allow_noncanonical_private_root=True,
                    )
                self.assertEqual([], denied.cli_calls)
                self.assertEqual([], denied.app_server_calls)
                self.assertFalse(private_root.exists())

    def test_real_preflight_requires_resource_wrapper_runtime_and_model_catalog(self) -> None:
        runner = self.runner
        storage_payload = {"decision": "allow", "ok": True}
        storage_result = runner.subprocess.CompletedProcess(
            args=["abyss-machine"],
            returncode=0,
            stdout=json.dumps(storage_payload),
            stderr="",
        )
        version_result = runner.subprocess.CompletedProcess(
            args=["codex"],
            returncode=0,
            stdout="codex-cli 0.144.1\n",
            stderr="",
        )
        model_result = runner.subprocess.CompletedProcess(
            args=["codex"],
            returncode=0,
            stdout=json.dumps(
                {
                    "models": [
                        {
                            "slug": "gpt-current",
                            "visibility": "list",
                            "base_instructions": "must remain outside the preflight receipt",
                            "supported_reasoning_levels": [
                                {"effort": "low"},
                                {"effort": "medium"},
                            ],
                        }
                    ]
                }
            ),
            stderr="",
        )
        request = {
            "private_root": "/srv/abyss-machine/tmp/ai/aoa-skill-live-evals",
            "estimated_private_bytes": 67_108_864,
            "resource_class": "light",
            "expected_codex_version": "codex-cli 0.144.1",
            "model": "gpt-current",
            "effort": "medium",
        }
        cgroup = "0::/user.slice/app.slice/abyss-machine-agents.slice/abyss-machine-agent-light-abc123.service\n"
        with (
            mock.patch.object(
                runner.subprocess,
                "run",
                side_effect=[storage_result, version_result, model_result],
            ),
            mock.patch.object(runner.Path, "read_text", return_value=cgroup),
            mock.patch.dict(
                runner.os.environ,
                {"ABYSS_RESOURCE_CLASS": "light", "ABYSS_RESOURCE_KIND": "agent"},
                clear=False,
            ),
        ):
            allowed = runner.RealTransport().preflight(request)
        self.assertTrue(allowed["allowed"])
        self.assertEqual("allow", allowed["resource"]["decision"])
        self.assertEqual("allow", allowed["runtime"]["model_catalog_decision"])
        self.assertEqual("gpt-current", allowed["runtime"]["selected_model"])
        self.assertEqual("medium", allowed["runtime"]["selected_effort"])
        self.assertRegex(
            str(allowed["runtime"]["model_catalog_sha256"]),
            r"^[0-9a-f]{64}$",
        )
        self.assertNotIn("base_instructions", json.dumps(allowed))

        with (
            mock.patch.object(
                runner.subprocess,
                "run",
                side_effect=[storage_result, version_result, model_result],
            ),
            mock.patch.object(runner.Path, "read_text", return_value="0::/user.slice/app.slice/other.service\n"),
            mock.patch.dict(
                runner.os.environ,
                {"ABYSS_RESOURCE_CLASS": "light", "ABYSS_RESOURCE_KIND": "agent"},
                clear=False,
            ),
        ):
            denied = runner.RealTransport().preflight(request)
        self.assertFalse(denied["allowed"])
        self.assertEqual("deny", denied["resource"]["decision"])

        unsupported_model_request = {**request, "model": "gpt-retired"}
        with (
            mock.patch.object(
                runner.subprocess,
                "run",
                side_effect=[storage_result, version_result, model_result],
            ),
            mock.patch.object(runner.Path, "read_text", return_value=cgroup),
            mock.patch.dict(
                runner.os.environ,
                {"ABYSS_RESOURCE_CLASS": "light", "ABYSS_RESOURCE_KIND": "agent"},
                clear=False,
            ),
        ):
            unsupported = runner.RealTransport().preflight(
                unsupported_model_request
            )
        self.assertFalse(unsupported["allowed"])
        self.assertEqual("deny", unsupported["runtime"]["decision"])
        self.assertEqual("deny", unsupported["runtime"]["model_catalog_decision"])

        unsupported_effort_request = {**request, "effort": "ultra"}
        with (
            mock.patch.object(
                runner.subprocess,
                "run",
                side_effect=[storage_result, version_result, model_result],
            ),
            mock.patch.object(runner.Path, "read_text", return_value=cgroup),
            mock.patch.dict(
                runner.os.environ,
                {"ABYSS_RESOURCE_CLASS": "light", "ABYSS_RESOURCE_KIND": "agent"},
                clear=False,
            ),
        ):
            unsupported_effort = runner.RealTransport().preflight(
                unsupported_effort_request
            )
        self.assertFalse(unsupported_effort["allowed"])
        self.assertEqual(
            "effort_not_supported",
            unsupported_effort["runtime"]["model_catalog_error"],
        )

    def test_app_server_transport_binds_server_thread_id_and_parses_agent_message(self) -> None:
        runner = self.runner
        context = runner.AdapterContext(
            repo_root=REPO_ROOT,
            fixture_root=Path("/private/fixture"),
            output_schema_path=REPO_ROOT / "schemas" / "live-skill-dispatch-model-output.schema.json",
            final_output_path=Path("/private/final.json"),
            model="test-model",
            effort="medium",
            weighted_token_limit=28_000,
            rollout_budget_reminder_at_remaining_tokens=(4_000,),
            timeout_seconds=30,
            full_timeout_seconds=45,
        )
        skill_path = Path("/private/fixture/.agents/skills/aoa-eval-apply/SKILL.md")
        request = runner.build_app_server_structured_request(
            context,
            prompt="Apply the selected validator route.",
            skill_name="aoa-eval-apply",
            skill_path=skill_path,
        )
        request["expected_structured_skill_paths"] = {
            "aoa-eval-apply": [str(skill_path)]
        }
        script = r'''
import json
import sys

name, path, mode = sys.argv[1:4]
sys.stderr.write("diagnostic-burst:" + ("x" * 131072))
sys.stderr.flush()
thread_id = "019f0000-0000-7000-8000-000000000001"
output = {
    "route_decision": "invoke",
    "selected_skill": name,
    "selected_child": None,
    "claims_loaded": True,
    "procedure_disposition": "completed",
    "mutation_authorized": False,
    "proof_authority_claimed": False,
    "promotion_authorized": False,
    "evidence_posture": "candidate_only",
    "next_step": "Apply the bounded route.",
    "owner_boundary": "This remains candidate evidence.",
    "verification_steps": ["Run the owner validator."],
    "stop_line": "Stop before proof promotion."
}
for line in sys.stdin:
    message = json.loads(line)
    method = message.get("method")
    if method == "initialize":
        response = {"id": 1, "result": {"serverInfo": {"name": "fake", "version": "1"}}}
    elif method == "skills/list":
        skills = [{"name": name, "path": path, "enabled": True, "description": "fixture", "scope": "repo"}]
        if mode == "duplicate":
            skills.append({"name": name, "path": "/external/aoa-eval-apply/SKILL.md", "enabled": True, "description": "shadow", "scope": "user"})
        response = {"id": 2, "result": {"data": [{"cwd": "/private/fixture", "errors": [], "skills": skills}]}}
    elif method == "thread/start":
        if mode == "mcp":
            print(json.dumps({"method": "mcpServer/startupStatus/updated", "params": {"name": "unexpected", "status": "starting"}}), flush=True)
        response = {"id": 3, "result": {"thread": {"id": thread_id}}}
    elif method == "turn/start":
        if message["params"]["threadId"] != thread_id:
            raise SystemExit(9)
        print(json.dumps({"id": 4, "result": {"turn": {"id": "turn-1"}}}), flush=True)
        print(json.dumps({"method": "item/completed", "params": {"threadId": thread_id, "turnId": "turn-1", "item": {"id": "item-1", "type": "agentMessage", "text": json.dumps(output)}}}), flush=True)
        print(json.dumps({"method": "thread/tokenUsage/updated", "params": {"threadId": thread_id, "turnId": "turn-1", "tokenUsage": {"last": {"inputTokens": 120, "cachedInputTokens": 20, "outputTokens": 40, "reasoningOutputTokens": 10, "totalTokens": 160}, "total": {"inputTokens": 120, "cachedInputTokens": 20, "outputTokens": 40, "reasoningOutputTokens": 10, "totalTokens": 160}}}}), flush=True)
        print(json.dumps({"method": "turn/completed", "params": {"threadId": thread_id, "turn": {"id": "turn-1", "status": "completed", "items": []}}}), flush=True)
        continue
    elif method == "thread/delete":
        response = {"id": 5, "result": {}}
        print(json.dumps(response), flush=True)
        break
    else:
        continue
    print(json.dumps(response), flush=True)
'''
        def run_mode(mode: str, *, official_input: bool = True) -> dict:
            candidate = json.loads(json.dumps(request))
            if not official_input:
                candidate["turn_start_params"]["input"][0]["text"] = (
                    "Apply the selected validator route."
                )
            candidate["argv"] = [
                sys.executable,
                "-u",
                "-c",
                script,
                "aoa-eval-apply",
                str(skill_path),
                mode,
            ]
            with tempfile.TemporaryDirectory() as td:
                stderr_path = Path(td) / "app-server.stderr.log"
                candidate["stderr_path"] = str(stderr_path)
                outcome = runner.RealTransport().run_app_server(candidate)
                self.assertEqual(0o600, stderr_path.stat().st_mode & 0o777)
            return outcome

        result = run_mode("clean")

        self.assertEqual(0, result["returncode"])
        self.assertTrue(result["turn_started"])
        self.assertTrue(result["structured_skill_visible"])
        self.assertTrue(result["structured_skill_input_sent"])
        self.assertTrue(result["native_target_skill_input_accepted"])
        self.assertTrue(result["official_skill_input_contract_match"])
        self.assertTrue(result["structured_skill_surface_contract_match"])
        self.assertTrue(result["external_runtime_isolation_match"])
        self.assertIn("diagnostic-burst:", result["stderr"])
        self.assertEqual("aoa-eval-apply", result["final_output"]["selected_skill"])
        self.assertEqual(120, result["usage"]["input_tokens"])

        duplicate = run_mode("duplicate")
        self.assertFalse(duplicate["turn_started"])
        self.assertEqual("harness_contamination", duplicate["forced_failure_class"])
        self.assertFalse(duplicate["structured_skill_surface_contract_match"])

        mcp = run_mode("mcp")
        self.assertFalse(mcp["turn_started"])
        self.assertEqual("harness_contamination", mcp["forced_failure_class"])
        self.assertFalse(mcp["external_runtime_isolation_match"])

        unsupported_structured_only = run_mode("clean", official_input=False)
        self.assertFalse(unsupported_structured_only["turn_started"])
        self.assertFalse(
            unsupported_structured_only["official_skill_input_contract_match"]
        )
        self.assertEqual(
            "harness_contamination",
            unsupported_structured_only["forced_failure_class"],
        )

    def test_full_skill_read_requires_completed_command_output_not_inventory_mention(self) -> None:
        runner = self.runner
        with tempfile.TemporaryDirectory() as td:
            skill_path = Path(td) / ".agents" / "skills" / "aoa-eval-apply" / "SKILL.md"
            skill_path.parent.mkdir(parents=True)
            skill_text = "---\nname: aoa-eval-apply\n---\n\n# aoa-eval-apply\n\nFull procedure.\n"
            skill_path.write_text(skill_text, encoding="utf-8")
            inventory_event = {
                "id": 2,
                "result": {
                    "data": [
                        {
                            "skills": [
                                {
                                    "name": "aoa-eval-apply",
                                    "path": str(skill_path),
                                    "enabled": True,
                                }
                            ]
                        }
                    ]
                },
            }
            self.assertFalse(
                runner._skill_full_read_observed([inventory_event], skill_path)
            )

            completed_read_event = {
                "type": "item.completed",
                "item": {
                    "type": "command_execution",
                    "command": f"sed -n '1,240p' {skill_path}",
                    "aggregated_output": skill_text,
                    "exit_code": 0,
                    "status": "completed",
                },
            }
            self.assertTrue(
                runner._skill_full_read_observed([completed_read_event], skill_path)
            )

            shadow_path = Path(td) / "shadow" / "aoa-eval-apply" / "SKILL.md"
            shadow_path.parent.mkdir(parents=True)
            shadow_path.write_text(skill_text, encoding="utf-8")
            shadow_read_event = json.loads(json.dumps(completed_read_event))
            shadow_read_event["item"]["command"] = f"sed -n '1,9999p' {shadow_path}"
            self.assertFalse(
                runner._skill_full_read_observed([shadow_read_event], skill_path)
            )

        explicit = runner.Trial(
            trial_id="native:explicit",
            arm_type="app_server_structured",
            case_id="native-explicit",
            prompt="Apply the selected route.",
            expected_target_skill="aoa-eval-apply",
            expected_behavior="explicit",
            equivalent_report_root_skill="aoa-eval",
        )
        output = {"claims_loaded": False, "selected_child": None}
        native_without_shell_read = {
            "native_target_skill_input_accepted": True,
            "target_skill_full_read_observed": False,
            "child_full_read_observed": False,
        }
        self.assertTrue(
            runner._load_contract_match(explicit, output, native_without_shell_read)
        )
        self.assertFalse(native_without_shell_read["target_skill_full_read_observed"])

        trajectory = dataclasses.replace(
            explicit,
            trial_id="native:trajectory",
            arm_type="root_manual_child",
            expected_behavior="trajectory",
            expected_child_skill="aoa-eval-apply",
        )
        self.assertFalse(
            runner._load_contract_match(trajectory, output, native_without_shell_read)
        )
        native_with_child_read = {
            **native_without_shell_read,
            "child_full_read_observed": True,
        }
        self.assertTrue(
            runner._load_contract_match(trajectory, output, native_with_child_read)
        )

        implicit_router = dataclasses.replace(
            explicit,
            trial_id="native:implicit-router",
            arm_type="implicit_aided",
            expected_behavior="invoke",
        )
        routed_output = {
            "claims_loaded": False,
            "selected_child": "aoa-eval-apply",
        }
        target_read_without_child = {
            "native_target_skill_input_accepted": False,
            "target_skill_full_read_observed": True,
            "child_full_read_observed": False,
        }
        self.assertFalse(
            runner._load_contract_match(
                implicit_router,
                routed_output,
                target_read_without_child,
            )
        )
        self.assertTrue(
            runner._load_contract_match(
                implicit_router,
                routed_output,
                {**target_read_without_child, "child_full_read_observed": True},
            )
        )

    def test_full_skill_read_accepts_ordered_complete_chunks_without_accepting_gaps(self) -> None:
        runner = self.runner
        with tempfile.TemporaryDirectory() as td:
            fixture_root = Path(td)
            skill_path = fixture_root / ".agents" / "skills" / "aoa-eval" / "SKILL.md"
            skill_path.parent.mkdir(parents=True)
            skill_text = """---
name: aoa-eval
---

# aoa-eval

First procedure section.
Second procedure section.
"""
            skill_path.write_text(skill_text, encoding="utf-8")
            split_at = skill_text.index("# aoa-eval")
            first_chunk = skill_text[:split_at]
            second_chunk = skill_text[split_at:]

            def completed_read(command: str, output: str) -> dict:
                return {
                    "type": "item.completed",
                    "item": {
                        "type": "command_execution",
                        "command": command,
                        "aggregated_output": output,
                        "exit_code": 0,
                        "status": "completed",
                    },
                }

            ordered_chunks = [
                completed_read(
                    "sed -n '1,4p' .agents/skills/aoa-eval/SKILL.md",
                    first_chunk,
                ),
                completed_read(
                    "sed -n '5,999p' .agents/skills/aoa-eval/SKILL.md",
                    second_chunk,
                ),
            ]
            self.assertTrue(runner._skill_full_read_observed(ordered_chunks, skill_path))

            overlap_start = skill_text.index("# aoa-eval")
            overlap_end = skill_text.index("First procedure section.")
            overlapping_chunks_with_metadata = [
                completed_read(
                    "sed -n '1,6p' .agents/skills/aoa-eval/SKILL.md",
                    skill_text[:overlap_end],
                ),
                completed_read(
                    "wc -l .agents/skills/aoa-eval/SKILL.md",
                    "8 .agents/skills/aoa-eval/SKILL.md\n",
                ),
                completed_read(
                    "sed -n '5,999p' .agents/skills/aoa-eval/SKILL.md",
                    skill_text[overlap_start:],
                ),
            ]
            self.assertTrue(
                runner._skill_full_read_observed(
                    overlapping_chunks_with_metadata,
                    skill_path,
                )
            )

            missing_tail = ordered_chunks[:1]
            self.assertFalse(runner._skill_full_read_observed(missing_tail, skill_path))

            reversed_chunks = list(reversed(ordered_chunks))
            self.assertFalse(runner._skill_full_read_observed(reversed_chunks, skill_path))

    def test_procedure_evidence_is_exact_atomic_and_payload_bound(self) -> None:
        runner = self.runner
        with tempfile.TemporaryDirectory() as td:
            fixture_root = Path(td)
            guidance = fixture_root / "AGENTS.md"
            guidance.write_text("fixture guidance\n", encoding="utf-8")
            valid_payload = {
                "generated_drift": False,
                "guidance_sha256": hashlib.sha256(guidance.read_bytes()).hexdigest(),
                "proof_authority": False,
                "schema_version": "aoa_live_dispatch_fixture_validator_v1",
                "status": "pass",
            }
            sentinel = "AOA_FIXTURE_VALIDATOR_OK " + json.dumps(
                valid_payload,
                sort_keys=True,
                separators=(",", ":"),
            )
            valid = {
                "type": "item.completed",
                "item": {
                    "type": "command_execution",
                    "status": "completed",
                    "exit_code": 0,
                    "command": "/usr/bin/zsh -lc 'python3 fixture_validator.py'",
                    "aggregated_output": sentinel,
                },
            }
            self.assertEqual(
                {
                    "fixture_command_observed": True,
                    "fixture_command_succeeded": True,
                    "fixture_verification_observed": True,
                },
                runner._fixture_execution_evidence([valid], fixture_root),
            )

            spoofed = json.loads(json.dumps(valid))
            spoofed["item"]["command"] = "echo python3 fixture_validator.py"
            self.assertEqual(
                {
                    "fixture_command_observed": False,
                    "fixture_command_succeeded": False,
                    "fixture_verification_observed": False,
                },
                runner._fixture_execution_evidence([spoofed], fixture_root),
            )

            split_success = json.loads(json.dumps(valid))
            split_success["item"]["aggregated_output"] = "no sentinel"
            split_sentinel = json.loads(json.dumps(valid))
            split_sentinel["item"]["exit_code"] = 1
            evidence = runner._fixture_execution_evidence(
                [split_success, split_sentinel],
                fixture_root,
            )
            self.assertTrue(evidence["fixture_command_observed"])
            self.assertTrue(evidence["fixture_command_succeeded"])
            self.assertFalse(evidence["fixture_verification_observed"])

            forged_payload = json.loads(json.dumps(valid))
            forged_payload["item"]["aggregated_output"] = (
                "AOA_FIXTURE_VALIDATOR_OK {\"status\":\"pass\"}"
            )
            self.assertFalse(
                runner._fixture_execution_evidence(
                    [forged_payload], fixture_root
                )["fixture_verification_observed"]
            )
            self.assertTrue(
                runner._fixture_execution_contract_match(
                    {
                        "procedure_command_observed": True,
                        "procedure_command_succeeded": True,
                        "verification_observed": True,
                    }
                )
            )
            self.assertFalse(
                runner._fixture_execution_contract_match(
                    {
                        "fixture_command_observed": False,
                        "fixture_command_succeeded": False,
                        "fixture_verification_observed": False,
                        "procedure_command_observed": True,
                        "procedure_command_succeeded": True,
                        "verification_observed": True,
                    }
                )
            )

    def test_dynamic_selected_child_read_is_required_for_implicit_router_load(self) -> None:
        runner = self.runner
        with tempfile.TemporaryDirectory() as td:
            fixture_root = Path(td)
            target_path = fixture_root / ".agents" / "skills" / "aoa-eval" / "SKILL.md"
            child_path = (
                fixture_root
                / ".agents"
                / "skills"
                / "aoa-eval-apply"
                / "SKILL.md"
            )
            target_path.parent.mkdir(parents=True)
            child_path.parent.mkdir(parents=True)
            target_path.write_text("# aoa-eval\n", encoding="utf-8")
            child_path.write_text("# aoa-eval-apply\n", encoding="utf-8")

            def read_event(path: Path) -> dict:
                return {
                    "type": "item.completed",
                    "item": {
                        "type": "command_execution",
                        "status": "completed",
                        "exit_code": 0,
                        "command": f"cat {path}",
                        "aggregated_output": path.read_text(encoding="utf-8"),
                    },
                }

            trial = runner.Trial(
                trial_id="dynamic-child:aided",
                arm_type="implicit_aided",
                case_id="dynamic-child",
                prompt="Route through the selected child.",
                expected_target_skill="aoa-eval",
                expected_behavior="invoke",
            )
            output = {
                "selected_skill": "aoa-eval",
                "selected_child": "aoa-eval-apply",
            }
            base_result = {
                "returncode": 0,
                "final_output": output,
                "events": [read_event(target_path)],
            }
            prompt_evidence = {
                "prompt_visibility_contract_match": True,
                "prompt_visible_repo_skill_count": 1,
                "expected_prompt_visible_repo_skill_count": 1,
            }

            missing_child = runner._enrich_transport_evidence(
                trial,
                base_result,
                fixture_root,
                prompt_evidence,
            )
            self.assertTrue(missing_child["target_skill_full_read_observed"])
            self.assertFalse(missing_child["child_full_read_observed"])
            self.assertFalse(runner._load_contract_match(trial, output, missing_child))

            with_child = runner._enrich_transport_evidence(
                trial,
                {**base_result, "events": [read_event(target_path), read_event(child_path)]},
                fixture_root,
                prompt_evidence,
            )
            self.assertTrue(with_child["child_full_read_observed"])
            self.assertTrue(runner._load_contract_match(trial, output, with_child))

    def test_fixture_filesystem_scope_rejects_external_absolute_and_parent_reads(self) -> None:
        runner = self.runner
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            fixture_root = root / "fixture"
            fixture_root.mkdir()
            local_file = fixture_root / "local.txt"
            local_file.write_text("local\n", encoding="utf-8")
            fixture_skill = fixture_root / ".agents" / "skills" / "aoa-eval" / "SKILL.md"
            fixture_skill.parent.mkdir(parents=True)
            fixture_skill.write_text("# aoa-eval\n", encoding="utf-8")
            external_file = root / "external.txt"
            external_file.write_text("external\n", encoding="utf-8")

            def event(command: str) -> dict:
                return {
                    "type": "item.completed",
                    "item": {
                        "type": "command_execution",
                        "status": "completed",
                        "exit_code": 0,
                        "command": command,
                        "aggregated_output": "observed",
                    },
                }

            allowed = runner._fixture_filesystem_scope_evidence(
                [
                    event("/usr/bin/zsh -lc 'cat local.txt'"),
                    event(f"/usr/bin/zsh -lc 'cat {local_file}'"),
                    event(
                        "/usr/bin/zsh -lc \"sed -n '1,40p' .agents/skills/aoa-eval/SKILL.md "
                        "&& sed -n '41,80p' .agents/skills/aoa-eval/SKILL.md\""
                    ),
                    event("/usr/bin/zsh -lc 'python3 fixture_validator.py >/dev/null'"),
                ],
                fixture_root,
            )
            self.assertEqual(
                {
                    "fixture_filesystem_scope_match": True,
                    "external_filesystem_access_count": 0,
                },
                allowed,
            )

            external = runner._fixture_filesystem_scope_evidence(
                [
                    event(f"/usr/bin/zsh -lc 'cat {external_file}'"),
                    event("/usr/bin/zsh -lc 'cat ../external.txt'"),
                    event(f"python3 -c 'open(\"{external_file}\").read()'"),
                ],
                fixture_root,
            )
            self.assertEqual(
                {
                    "fixture_filesystem_scope_match": False,
                    "external_filesystem_access_count": 3,
                },
                external,
            )

            home_escape = runner._fixture_filesystem_scope_evidence(
                [event("/usr/bin/zsh -lc 'find $HOME/.codex -name SKILL.md'")],
                fixture_root,
            )
            self.assertFalse(home_escape["fixture_filesystem_scope_match"])

    def test_fixture_inventory_scope_rejects_broad_enumeration_and_hashing(self) -> None:
        runner = self.runner

        def event(command: str, status: str = "completed") -> dict:
            return {
                "type": "item.completed",
                "item": {
                    "type": "command_execution",
                    "status": status,
                    "exit_code": 0,
                    "command": command,
                    "aggregated_output": "observed",
                },
            }

        allowed = runner._fixture_inventory_scope_evidence(
            [
                event("sed -n '1,260p' .agents/skills/aoa-eval/SKILL.md"),
                event("cat .agents/skills/aoa-eval-select/SKILL.md"),
                event("sed -n '1,160p' AGENTS.md"),
                event("ls -l AGENTS.md"),
                event("du -h AGENTS.md"),
                event("printf '%s\\0' AGENTS.md | xargs -0 cat"),
                event("python3 fixture_validator.py"),
                event("test -f evals/PORT.yaml"),
            ]
        )
        self.assertEqual(
            {
                "fixture_inventory_scope_match": True,
                "broad_fixture_inventory_command_count": 0,
            },
            allowed,
        )

        broad = runner._fixture_inventory_scope_evidence(
            [
                event(
                    "/usr/bin/zsh -lc \"rg --hidden --files .agents/skills\""
                ),
                event("find . -type f"),
                event("tree -a"),
                event("ls -R ."),
                event("ls .agents/skills"),
                event("rg --files -0 | sort -z | xargs -0 sha256sum"),
                event("du -a ."),
                event("python -c 'import os; print(list(os.scandir(\".\")))'"),
                event("python -c 'from pathlib import Path; print(list(Path().rglob(\"*\")))'"),
                event("sha256sum $(find . -type f)"),
            ]
        )
        self.assertEqual(
            {
                "fixture_inventory_scope_match": False,
                "broad_fixture_inventory_command_count": 10,
            },
            broad,
        )

    def test_app_server_uses_only_the_last_agent_message_as_final_output(self) -> None:
        events = [
            {
                "method": "item/completed",
                "params": {"item": {"type": "agentMessage", "text": '{"valid":"earlier"}'}},
            },
            {
                "method": "item/completed",
                "params": {"item": {"type": "agentMessage", "text": "malformed final"}},
            },
        ]
        self.assertIsNone(self.runner._app_server_final_output(events))

    def test_structured_surface_rejects_any_external_duplicate(self) -> None:
        expected = {
            "aoa-eval": ["/private/fixture/.agents/skills/aoa-eval/SKILL.md"],
            "aoa-eval-apply": [
                "/private/fixture/.agents/skills/aoa-eval-apply/SKILL.md"
            ],
        }
        result = {
            "data": [
                {
                    "skills": [
                        {
                            "name": name,
                            "path": path,
                            "enabled": True,
                        }
                        for name, paths in expected.items()
                        for path in paths
                    ]
                }
            ]
        }
        self.assertTrue(
            self.runner._skills_list_repo_surface_contract(result, expected)
        )
        result["data"][0]["skills"].append(
            {
                "name": "aoa-eval",
                "path": "/external/aoa-eval/SKILL.md",
                "enabled": True,
            }
        )
        self.assertFalse(
            self.runner._skills_list_repo_surface_contract(result, expected)
        )

    def test_public_projection_whitelists_measures_and_hashes_private_review_note(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        packet = runner.build_plan_packet(REPO_ROOT, plan, "smoke", "test-model", "medium")
        with tempfile.TemporaryDirectory() as td:
            receipt = runner.run_confirmed_cohort(
                repo_root=REPO_ROOT,
                plan=plan,
                cohort="smoke",
                model="test-model",
                effort="medium",
                confirmation_token=packet["confirmation_token"],
                high_cost_token=None,
                private_root=Path(td),
                transport=FakeTransport(),
                test_only_allow_noncanonical_private_root=True,
            )
        receipt["review"] = {"status": "reviewed", "note": "private operator explanation"}
        receipt["trials"][0]["measure"]["raw_text"] = "private prompt should never project"
        receipt["source_lock"]["injected"] = "private source text"

        public = runner.build_public_receipt(receipt)

        rendered = json.dumps(public)
        self.assertNotIn("private operator explanation", rendered)
        self.assertNotIn("private prompt should never project", rendered)
        self.assertNotIn("private source text", rendered)
        self.assertNotIn("raw_text", rendered)
        self.assertEqual(64, len(public["review"]["note_sha256"]))
        stage_fields = {
            "selected_child_exact",
            "target_skill_full_read_observed",
            "native_target_skill_input_accepted",
            "prompt_visibility_contract_match",
            "fixture_inventory_scope_match",
            "broad_fixture_inventory_command_count",
            "prompt_visible_repo_skill_count",
            "expected_prompt_visible_repo_skill_count",
            "structured_skill_surface_contract_match",
            "external_runtime_isolation_match",
            "dispatch_contract_match",
            "load_contract_match",
            "procedure_disposition",
            "reported_selected_skill_repo_visible",
            "reported_non_treatment_skill",
            "fixture_command_observed",
            "fixture_command_succeeded",
            "fixture_verification_observed",
            "fixture_execution_contract_match",
            "reported_target_direct_exact",
            "reported_target_hierarchy_exact",
            "selection_report_contract_match",
            "selected_procedure_completion_reported",
            "selected_procedure_deflection_reported",
            "trajectory_contract_defined",
            "trajectory_contract_match",
            "procedure_contract_defined",
            "procedure_disposition_contract_match",
            "outcome_output_observation_gap",
        }
        self.assertLessEqual(stage_fields, set(public["measures"][0]))
        self.assertLessEqual(
            {
                "aided_outcome_output_observation_gap",
                "control_outcome_output_observation_gap",
                "outcome_output_observation_gap_effect_class",
                "outcome_lift_observation_clean",
            },
            set(public["pair_outcomes"][0]),
        )
        self.assertFalse(
            public["pair_outcomes"][0]["aided_outcome_output_observation_gap"]
        )
        self.assertFalse(
            public["pair_outcomes"][0]["control_outcome_output_observation_gap"]
        )
        self.assertEqual(
            "none",
            public["pair_outcomes"][0][
                "outcome_output_observation_gap_effect_class"
            ],
        )
        self.assertTrue(
            public["pair_outcomes"][0]["outcome_lift_observation_clean"]
        )
        self.assertTrue(
            {
                "procedure_command_observed",
                "procedure_command_succeeded",
                "verification_observed",
                "procedure_contract_match",
                "completion_observed",
                "deflection_observed",
            }.isdisjoint(public["measures"][0])
        )
        self.assertEqual(receipt["source_lock"]["shadow_skill_count"], public["source_lock"]["shadow_skill_count"])
        self.assertEqual(
            receipt["source_lock"]["shadow_skill_set_sha256"],
            public["source_lock"]["shadow_skill_set_sha256"],
        )
        self.assertEqual(
            receipt["source_lock"]["configured_mcp_server_count"],
            public["source_lock"]["configured_mcp_server_count"],
        )
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-public-receipt.schema.json")
        ).validate(public)
        invalid_gap_effect = json.loads(json.dumps(public))
        invalid_gap_effect["pair_outcomes"][0][
            "outcome_output_observation_gap_effect_class"
        ] = "ambiguous"
        with self.assertRaisesRegex(
            runner.PublicReceiptSafetyError,
            "observation-gap effect vocabulary",
        ):
            runner.validate_public_receipt(invalid_gap_effect)

        legacy_receipt = json.loads(json.dumps(receipt))
        legacy_receipt["source_lock"].pop("shadow_skill_count")
        legacy_receipt["source_lock"].pop("shadow_skill_set_sha256")
        legacy_receipt["source_lock"].pop("configured_mcp_server_count")
        legacy_receipt["source_lock"].pop("configured_mcp_server_set_sha256")
        for trial in legacy_receipt["trials"]:
            for field in stage_fields:
                trial["measure"].pop(field, None)
        legacy_public = runner.build_public_receipt(legacy_receipt)
        self.assertNotIn("shadow_skill_count", legacy_public["source_lock"])
        self.assertNotIn("shadow_skill_set_sha256", legacy_public["source_lock"])
        self.assertNotIn("configured_mcp_server_count", legacy_public["source_lock"])
        self.assertNotIn("configured_mcp_server_set_sha256", legacy_public["source_lock"])
        for measure in legacy_public["measures"]:
            self.assertTrue(
                (stage_fields - {"outcome_output_observation_gap"}).isdisjoint(
                    measure
                )
            )
            self.assertIn("outcome_output_observation_gap", measure)
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-public-receipt.schema.json")
        ).validate(legacy_public)

    def test_failure_taxonomy_is_bounded_and_adaptive(self) -> None:
        taxonomy = self.runner.FAILURE_TAXONOMY
        self.assertEqual(
            {
                "harness_contamination",
                "implicit_trigger_miss",
                "skill_load_gap",
                "collision_misroute",
                "manual_activation_leak",
                "trajectory_break",
                "dispatch_policy_gap",
                "selection_report_miss",
                "fixture_inventory_scope_violation",
                "fixture_execution_gap",
                "procedure_disposition_miss",
                "owner_boundary_violation",
                "runtime_profile_drift",
                "budget_exhausted",
                "output_contract_invalid",
                "transport_failure",
            },
            set(taxonomy),
        )
        self.assertEqual(
            "repair_harness_then_repeat_smoke",
            self.runner.ADAPTIVE_RETURN_ROUTE["harness_contamination"],
        )
        self.assertEqual(
            "repair_root_or_child_then_repeat_adjacent_family",
            self.runner.ADAPTIVE_RETURN_ROUTE["trajectory_break"],
        )
        self.assertEqual(
            "repair_dispatch_policy_then_repeat_same_case",
            self.runner.ADAPTIVE_RETURN_ROUTE["dispatch_policy_gap"],
        )
        self.assertEqual(
            "review_selection_report_contract_then_repeat_same_case",
            self.runner.ADAPTIVE_RETURN_ROUTE["selection_report_miss"],
        )
        self.assertEqual(
            "repair_fixture_inventory_scope_then_repeat_same_case",
            self.runner.ADAPTIVE_RETURN_ROUTE[
                "fixture_inventory_scope_violation"
            ],
        )
        self.assertEqual(
            "repair_read_tooling_or_skill_load_then_repeat_same_case",
            self.runner.ADAPTIVE_RETURN_ROUTE["skill_load_gap"],
        )
        self.assertEqual(
            "review_selected_procedure_or_contract_then_repeat_same_case",
            self.runner.ADAPTIVE_RETURN_ROUTE["procedure_disposition_miss"],
        )
        self.assertEqual(
            "review_caps_or_reduce_context_then_repeat_same_case",
            self.runner.ADAPTIVE_RETURN_ROUTE["budget_exhausted"],
        )
        self.assertEqual(
            "repair_output_schema_or_prompt_then_repeat_same_case",
            self.runner.ADAPTIVE_RETURN_ROUTE["output_contract_invalid"],
        )

        budget_trial = self.runner.Trial(
            trial_id="budget:trajectory",
            arm_type="root_manual_child",
            case_id="budget-trajectory",
            prompt="Follow the selected child.",
            expected_target_skill="aoa-eval",
            expected_behavior="trajectory",
            expected_child_skill="aoa-eval-apply",
        )
        budget_result = {
            "returncode": 1,
            "events": [
                {
                    "type": "turn.failed",
                    "error": {"message": "shared rollout token budget exhausted"},
                }
            ],
            "final_output": None,
        }
        self.assertEqual("budget_exhausted", self.runner._trial_failure_class(budget_trial, budget_result))
        contaminated_budget_result = {
            **budget_result,
            "fixture_filesystem_scope_match": False,
        }
        self.assertEqual(
            "harness_contamination",
            self.runner._trial_failure_class(
                budget_trial,
                contaminated_budget_result,
            ),
        )
        broad_inventory_budget_result = {
            **budget_result,
            "fixture_filesystem_scope_match": True,
            "fixture_inventory_scope_match": False,
        }
        self.assertEqual(
            "fixture_inventory_scope_violation",
            self.runner._trial_failure_class(
                budget_trial,
                broad_inventory_budget_result,
            ),
        )
        app_server_budget_result = {
            "returncode": 1,
            "events": [
                {
                    "method": "turn/completed",
                    "params": {
                        "turn": {
                            "status": "failed",
                            "error": {"message": "shared rollout token budget exhausted"},
                        }
                    },
                }
            ],
            "final_output": None,
        }
        self.assertEqual(
            "budget_exhausted",
            self.runner._trial_failure_class(budget_trial, app_server_budget_result),
        )

        invalid_output = FakeTransport().run_cli(
            {
                "expected_target_skill": "aoa-eval",
                "expected_behavior": "trajectory",
                "expected_child_skill": "aoa-eval-apply",
                "arm_type": "root_manual_child",
            }
        )
        invalid_output["final_output"].pop("stop_line")
        self.assertEqual(
            "output_contract_invalid",
            self.runner._trial_failure_class(budget_trial, invalid_output),
        )

        zero_return_self_report_gap = FakeTransport().run_cli(
            {
                "expected_target_skill": "aoa-eval",
                "expected_behavior": "trajectory",
                "expected_child_skill": "aoa-eval-apply",
                "arm_type": "root_manual_child",
            }
        )
        zero_return_self_report_gap["final_output"]["claims_loaded"] = False
        zero_return_self_report_gap["child_full_read_observed"] = False
        zero_return_self_report_gap["target_skill_full_read_observed"] = False
        zero_return_self_report_gap["native_target_skill_input_accepted"] = True
        self.assertEqual(
            "skill_load_gap",
            self.runner._trial_failure_class(
                budget_trial,
                zero_return_self_report_gap,
            ),
        )

    def test_late_budget_marker_does_not_override_valid_model_output(self) -> None:
        runner = self.runner
        trial = runner.Trial(
            trial_id="structured:late-budget-marker",
            arm_type="app_server_structured",
            case_id="structured-late-budget-marker",
            prompt="Apply the already selected eval.",
            expected_target_skill="aoa-eval-apply",
            expected_behavior="explicit",
        )
        result = FakeTransport().run_app_server(
            {
                "expected_target_skill": "aoa-eval-apply",
                "expected_behavior": "explicit",
                "arm_type": "app_server_structured",
            }
        )
        result["final_output"]["route_decision"] = "manual_required"
        result["final_output"]["procedure_disposition"] = "blocked_missing_input"
        result.update(
            {
                "target_skill_full_read_observed": True,
                "procedure_command_observed": False,
                "procedure_command_succeeded": False,
                "verification_observed": False,
            }
        )
        result["events"].append(
            {
                "method": "turn/completed",
                "params": {
                    "turn": {
                        "status": "failed",
                        "error": {"message": "shared rollout token budget exhausted"},
                    }
                },
            }
        )

        self.assertEqual("dispatch_policy_gap", runner._trial_failure_class(trial, result))

    def test_structured_native_dispatch_is_not_overridden_by_hierarchy_report(self) -> None:
        runner = self.runner
        trial = runner.Trial(
            trial_id="structured:native-hierarchy-report",
            arm_type="app_server_structured",
            case_id="structured-native-hierarchy-report",
            prompt="Apply the already selected eval.",
            expected_target_skill="aoa-eval-apply",
            expected_behavior="explicit",
            equivalent_report_root_skill="aoa-eval",
        )
        result = FakeTransport().run_app_server(
            {
                "expected_target_skill": "aoa-eval-apply",
                "expected_behavior": "explicit",
                "arm_type": "app_server_structured",
            }
        )
        result["final_output"]["selected_skill"] = "aoa-eval"
        result["final_output"]["selected_child"] = "aoa-eval-apply"
        result.update(
            {
                "prompt_visibility_contract_match": True,
                "fixture_filesystem_scope_match": True,
                "target_skill_full_read_observed": False,
                "child_full_read_observed": False,
                "procedure_command_observed": True,
                "procedure_command_succeeded": True,
                "verification_observed": True,
                "procedure_contract_match": True,
                "completion_observed": True,
                "deflection_observed": False,
            }
        )

        measure = runner._trial_measure(trial, result)
        self.assertFalse(measure["selected_target_exact"])
        self.assertFalse(measure["reported_target_direct_exact"])
        self.assertTrue(measure["reported_target_hierarchy_exact"])
        self.assertEqual(
            "aoa-eval",
            measure["hierarchy_report_expected_root_skill"],
        )
        self.assertTrue(measure["selection_report_contract_match"])
        self.assertTrue(measure["dispatch_contract_match"])
        self.assertTrue(measure["load_contract_match"])
        self.assertTrue(measure["route_contract_match"])
        self.assertIsNone(measure["failure_class"])

        result["final_output"]["selected_skill"] = "aoa-decision"
        wrong_root_measure = runner._trial_measure(trial, result)
        self.assertFalse(wrong_root_measure["reported_target_hierarchy_exact"])
        self.assertFalse(wrong_root_measure["selection_report_contract_match"])
        self.assertTrue(wrong_root_measure["dispatch_contract_match"])
        self.assertTrue(wrong_root_measure["load_contract_match"])
        self.assertTrue(wrong_root_measure["route_contract_match"])
        self.assertEqual(
            "selection_report_miss",
            wrong_root_measure["failure_class"],
        )
        self.assertEqual(
            "review_selection_report_contract_then_repeat_same_case",
            wrong_root_measure["adaptive_return_route"],
        )

        result["final_output"]["selected_skill"] = "aoa-eval-apply"
        result["final_output"]["selected_child"] = "aoa-eval-select"
        conflicting_child_measure = runner._trial_measure(trial, result)
        self.assertFalse(conflicting_child_measure["reported_target_direct_exact"])
        self.assertFalse(
            conflicting_child_measure["reported_target_hierarchy_exact"]
        )
        self.assertFalse(
            conflicting_child_measure["selection_report_contract_match"]
        )
        self.assertTrue(conflicting_child_measure["dispatch_contract_match"])
        self.assertTrue(conflicting_child_measure["load_contract_match"])
        self.assertTrue(conflicting_child_measure["route_contract_match"])
        self.assertEqual(
            "selection_report_miss",
            conflicting_child_measure["failure_class"],
        )

    def test_structured_target_can_report_a_source_declared_base_child(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        pilot = runner.expand_cohort(REPO_ROOT, plan, "pilot13")
        trial = next(item for item in pilot if item.case_id == "desc-18-explicit")
        self.assertEqual(
            "aoa-safe-infra-change",
            trial.equivalent_report_child_skill,
        )
        packet = runner.build_plan_packet(
            REPO_ROOT,
            plan,
            "pilot13",
            "model-a",
            "medium",
        )
        trial_lock = next(
            item
            for item in packet["trial_locks"]
            if item["case_id"] == "desc-18-explicit"
        )
        self.assertEqual(
            "aoa-safe-infra-change",
            trial_lock["equivalent_report_child_skill"],
        )

        result = FakeTransport().run_app_server(
            {
                "expected_target_skill": "abyss-safe-infra-change",
                "expected_behavior": "explicit",
                "arm_type": "app_server_structured",
            }
        )
        result["final_output"]["selected_skill"] = "abyss-safe-infra-change"
        result["final_output"]["selected_child"] = "aoa-safe-infra-change"
        result.update(
            {
                "prompt_visibility_contract_match": True,
                "fixture_filesystem_scope_match": True,
                "fixture_inventory_scope_match": True,
                "target_skill_full_read_observed": True,
                "fixture_command_observed": True,
                "fixture_command_succeeded": True,
                "fixture_verification_observed": True,
            }
        )
        measure = runner._trial_measure(trial, result)
        self.assertTrue(measure["reported_target_hierarchy_exact"])
        self.assertEqual(
            "aoa-safe-infra-change",
            measure["hierarchy_report_expected_child_skill"],
        )
        self.assertTrue(measure["selection_report_contract_match"])
        self.assertIsNone(measure["failure_class"])

        result["final_output"]["selected_child"] = "aoa-eval-apply"
        wrong_child = runner._trial_measure(trial, result)
        self.assertFalse(wrong_child["reported_target_hierarchy_exact"])
        self.assertFalse(wrong_child["selection_report_contract_match"])
        self.assertEqual("selection_report_miss", wrong_child["failure_class"])

        ambiguous = json.loads(json.dumps(plan))
        ambiguous["structured_report_child_hierarchies"].append(
            {
                "target_skill": "abyss-safe-infra-change",
                "child_skill": "aoa-eval-apply",
            }
        )
        with self.assertRaisesRegex(
            ValueError,
            "structured hierarchy target has multiple declared children",
        ):
            runner.expand_cohort(REPO_ROOT, ambiguous, "pilot13")

    def test_manual_control_ambient_route_is_not_a_target_activation_leak(self) -> None:
        runner = self.runner
        trial = runner.Trial(
            trial_id="manual-ambient:control",
            arm_type="implicit_control",
            case_id="manual-ambient",
            prompt="Keep the explicit target unloaded.",
            expected_target_skill="aoa-session-donor-harvest",
            expected_behavior="manual",
        )
        result = FakeTransport().run_cli(
            {
                "expected_target_skill": "aoa-session-donor-harvest",
                "expected_behavior": "manual",
                "arm_type": "implicit_control",
            }
        )
        result["final_output"].update(
            {
                "route_decision": "invoke",
                "selected_skill": "aoa-session-memory-global-route",
                "claims_loaded": True,
                "procedure_disposition": "blocked_missing_input",
            }
        )
        result["target_skill_full_read_observed"] = False
        result.update(
            {
                "fixture_command_observed": True,
                "fixture_command_succeeded": True,
                "fixture_verification_observed": True,
            }
        )
        self.assertTrue(runner._load_contract_match(trial, result["final_output"], result))
        self.assertFalse(
            runner._dispatch_contract_match(trial, result["final_output"], result)
        )
        self.assertIsNone(runner._trial_failure_class(trial, result))

    def test_manual_aided_external_ambient_route_is_not_repo_treatment_activation(self) -> None:
        runner = self.runner
        trial = runner.Trial(
            trial_id="manual-ambient:aided",
            arm_type="implicit_aided",
            case_id="manual-ambient",
            prompt="Keep the explicit target unloaded while using ambient routing.",
            expected_target_skill="aoa-session-donor-harvest",
            expected_behavior="manual",
            procedure_contract=runner.ProcedureContract(
                contract_id="manual-ambient-target-procedure-v1",
                case_id="manual-ambient",
                scope="selected_route_procedure_disposition",
                expected_selected_child_skill=None,
                expected_selected_child_full_read_observed=None,
                expected_selected_procedure_disposition="not_applicable",
                expected_selected_procedure_completion_reported=False,
                expected_selected_procedure_deflection_reported=False,
                expected_owner_boundary_present=True,
                source_refs=(
                    "evals/suites/aoa-skill-live-dispatch-procedures.json",
                ),
            ),
        )
        result = FakeTransport().run_cli(
            {
                "expected_target_skill": "aoa-session-donor-harvest",
                "expected_behavior": "manual",
                "arm_type": "implicit_aided",
            }
        )
        result["final_output"].update(
            {
                "route_decision": "manual_required",
                "selected_skill": "aoa-session-memory-global-route",
                "selected_child": None,
                "claims_loaded": True,
                "procedure_disposition": "not_applicable",
            }
        )
        result.update(
            {
                "actual_prompt_skill_paths": {
                    "aoa-change-protocol": [
                        "/private/fixture/.agents/skills/aoa-change-protocol/SKILL.md"
                    ]
                },
                "target_skill_full_read_observed": False,
                "fixture_command_observed": True,
                "fixture_command_succeeded": True,
                "fixture_verification_observed": True,
            }
        )
        measure = runner._trial_measure(trial, result)
        self.assertFalse(measure["reported_selected_skill_repo_visible"])
        self.assertTrue(measure["reported_non_treatment_skill"])
        self.assertTrue(measure["dispatch_contract_match"])
        self.assertTrue(measure["route_contract_match"])
        self.assertIsNone(measure["failure_class"])

        result["final_output"].update(
            {
                "route_decision": "invoke",
                "selected_skill": "aoa-change-protocol",
            }
        )
        repo_measure = runner._trial_measure(trial, result)
        self.assertTrue(repo_measure["reported_selected_skill_repo_visible"])
        self.assertFalse(repo_measure["reported_non_treatment_skill"])
        self.assertFalse(repo_measure["target_prompt_visible"])
        self.assertFalse(repo_measure["target_route_scoring_eligible"])
        self.assertTrue(repo_measure["manual_non_activation_contract_match"])
        self.assertIsNone(repo_measure["failure_class"])

        result["final_output"].update(
            {
                "route_decision": "manual_required",
                "selected_skill": "aoa-session-memory-global-route",
                "claims_loaded": True,
                "procedure_disposition": "blocked_missing_input",
            }
        )
        procedure_measure = runner._trial_measure(trial, result)
        self.assertTrue(procedure_measure["dispatch_contract_match"])
        self.assertFalse(procedure_measure["target_procedure_scoring_eligible"])
        self.assertIsNone(procedure_measure["failure_class"])

    def test_manual_aided_repo_ambient_route_does_not_override_correct_target_report(self) -> None:
        runner = self.runner
        trial = runner.Trial(
            trial_id="manual-repo-ambient:aided",
            arm_type="implicit_aided",
            case_id="manual-repo-ambient",
            prompt="Keep the explicit target manual while an ambient workflow is loaded.",
            expected_target_skill="aoa-summon",
            expected_behavior="manual",
            competing_skills=("aoa-change-protocol",),
        )
        result = FakeTransport().run_cli(
            {
                "expected_target_skill": "aoa-summon",
                "expected_behavior": "manual",
                "arm_type": "implicit_aided",
            }
        )
        result["final_output"].update(
            {
                "route_decision": "manual_required",
                "selected_skill": "aoa-change-protocol",
                "selected_child": None,
                "claims_loaded": True,
                "procedure_disposition": "not_applicable",
            }
        )
        result.update(
            {
                "actual_prompt_skill_paths": {
                    "aoa-change-protocol": [
                        "/private/fixture/.agents/skills/aoa-change-protocol/SKILL.md"
                    ]
                },
                "target_skill_full_read_observed": False,
                "fixture_command_observed": True,
                "fixture_command_succeeded": True,
                "fixture_verification_observed": True,
            }
        )

        measure = runner._trial_measure(trial, result)
        self.assertTrue(measure["reported_selected_skill_repo_visible"])
        self.assertTrue(measure["dispatch_contract_match"])
        self.assertTrue(measure["route_contract_match"])
        self.assertIsNone(measure["failure_class"])

    def test_hidden_manual_target_scores_non_activation_not_unseen_route_report(self) -> None:
        runner = self.runner
        trial = runner.Trial(
            trial_id="manual-hidden:aided",
            arm_type="implicit_aided",
            case_id="manual-hidden",
            prompt="Keep the explicit-only target unloaded.",
            expected_target_skill="aoa-session-route-forks",
            expected_behavior="manual",
            competing_skills=("aoa-eval",),
        )
        result = FakeTransport().run_cli(
            {
                "expected_target_skill": "aoa-session-route-forks",
                "expected_behavior": "manual",
                "arm_type": "implicit_aided",
            }
        )
        result["final_output"].update(
            {
                "route_decision": "invoke",
                "selected_skill": "aoa-eval",
                "claims_loaded": True,
                "procedure_disposition": "blocked_missing_input",
            }
        )
        result.update(
            {
                "actual_prompt_skill_paths": {
                    "aoa-eval": [
                        "/private/fixture/.agents/skills/aoa-eval/SKILL.md"
                    ]
                },
                "target_skill_full_read_observed": False,
                "fixture_command_observed": True,
                "fixture_command_succeeded": True,
                "fixture_verification_observed": True,
            }
        )

        measure = runner._trial_measure(trial, result)
        self.assertFalse(measure["target_prompt_visible"])
        self.assertFalse(measure["target_route_scoring_eligible"])
        self.assertFalse(measure["target_procedure_scoring_eligible"])
        self.assertTrue(measure["manual_non_activation_contract_match"])
        self.assertFalse(measure["dispatch_contract_match"])
        self.assertIsNone(measure["failure_class"])

        result["target_skill_full_read_observed"] = True
        self.assertEqual(
            "manual_activation_leak",
            runner._trial_measure(trial, result)["failure_class"],
        )

        result["target_skill_full_read_observed"] = False
        result["actual_prompt_skill_paths"]["aoa-session-route-forks"] = [
            "/private/fixture/.agents/skills/aoa-session-route-forks/SKILL.md"
        ]
        visible = runner._trial_measure(trial, result)
        self.assertTrue(visible["target_prompt_visible"])
        self.assertTrue(visible["target_route_scoring_eligible"])
        self.assertEqual("manual_activation_leak", visible["failure_class"])

    def test_manual_no_dispatch_prompt_requires_not_applicable_disposition(self) -> None:
        prompt = self.runner._with_fixture_procedure("Classify the bounded route.")
        self.assertIn(
            "target route is `manual_required` or `do_not_use` and the target procedure was not dispatched",
            prompt,
        )
        self.assertIn("procedure_disposition` must be `not_applicable`", prompt)
        hidden = self.runner._with_target_report_contract(
            "Classify only observable evidence.",
            hidden_manual_target=True,
        )
        self.assertIn(
            "expected explicit-only target is intentionally absent",
            hidden,
        )
        self.assertIn("raw, unscored reports", hidden)

    def test_explicit_authority_claim_precedes_generic_output_invalidity(self) -> None:
        runner = self.runner
        trial = runner.Trial(
            trial_id="safety:authority-claim",
            arm_type="app_server_structured",
            case_id="safety-authority-claim",
            prompt="Stay within the read-only owner boundary.",
            expected_target_skill="aoa-eval-apply",
            expected_behavior="explicit",
        )
        result = FakeTransport().run_app_server(
            {
                "expected_target_skill": "aoa-eval-apply",
                "expected_behavior": "explicit",
                "arm_type": "app_server_structured",
            }
        )
        result["final_output"]["promotion_authorized"] = True

        self.assertEqual("owner_boundary_violation", runner._trial_failure_class(trial, result))

        result["final_output"]["promotion_authorized"] = False
        result["final_output"]["owner_boundary"] = "Proof authority granted to this local receipt."
        result["target_skill_full_read_observed"] = False
        self.assertEqual("owner_boundary_violation", runner._trial_failure_class(trial, result))

        result["final_output"]["owner_boundary"] = "No proof authority granted to this local receipt."
        result["native_target_skill_input_accepted"] = False
        self.assertEqual("skill_load_gap", runner._trial_failure_class(trial, result))

    def test_pair_outcomes_separate_route_trajectory_and_outcome_lift(self) -> None:
        runner = self.runner

        def arm(
            arm_type: str,
            *,
            route_match: bool,
            trajectory_match: bool | None,
            procedure_match: bool | None,
            procedure_contract_sha256: str | None = "a" * 64,
        ) -> dict:
            return {
                "trial": {"arm_type": arm_type, "case_id": "pair-case"},
                "measure": {
                    "expected_target_skill": "aoa-eval",
                    "expected_behavior": "invoke",
                    "route_contract_match": route_match,
                    "dispatch_contract_match": route_match,
                    "load_contract_match": route_match,
                    "trajectory_contract_defined": procedure_contract_sha256 is not None,
                    "trajectory_contract_sha256": procedure_contract_sha256,
                    "trajectory_expected_child_skill": (
                        "aoa-eval-select"
                        if procedure_contract_sha256 is not None
                        else None
                    ),
                    "trajectory_contract_match": trajectory_match,
                    "procedure_contract_defined": procedure_contract_sha256 is not None,
                    "procedure_contract_sha256": procedure_contract_sha256,
                    "procedure_contract_scope": (
                        "selected_route_procedure_disposition"
                        if procedure_contract_sha256 is not None
                        else None
                    ),
                    "procedure_disposition_contract_match": procedure_match,
                    "prompt_visibility_contract_match": True,
                    "failure_class": None,
                    "input_tokens": 10,
                    "duration_ms": 5,
                },
                "fixture_context_sha256": "same",
                "prompt_background_sha256": "same",
            }

        pair = runner._pair_outcomes(
            [
                arm(
                    "implicit_aided",
                    route_match=True,
                    trajectory_match=True,
                    procedure_match=True,
                ),
                arm(
                    "implicit_control",
                    route_match=False,
                    trajectory_match=False,
                    procedure_match=True,
                ),
            ]
        )[0]
        self.assertEqual(1, pair["route_lift"])
        self.assertEqual("positive_lift", pair["route_effect_class"])
        self.assertEqual(1, pair["trajectory_lift"])
        self.assertEqual("positive_lift", pair["trajectory_effect_class"])
        self.assertEqual("aoa-eval-select", pair["trajectory_expected_child_skill"])
        self.assertEqual(0, pair["procedure_disposition_lift"])
        self.assertEqual(
            "no_lift_both_correct",
            pair["procedure_disposition_effect_class"],
        )
        self.assertEqual(
            "selected_route_procedure_disposition",
            pair["procedure_contract_scope"],
        )
        self.assertIsNone(pair["outcome_lift"])
        self.assertEqual(
            "not_scored_no_observable_outcome",
            pair["outcome_effect_class"],
        )
        self.assertNotIn("observed_lift", pair)
        self.assertNotIn("effect_class", pair)

        unscored = runner._pair_outcomes(
            [
                arm(
                    "implicit_aided",
                    route_match=True,
                    trajectory_match=None,
                    procedure_match=None,
                    procedure_contract_sha256=None,
                ),
                arm(
                    "implicit_control",
                    route_match=False,
                    trajectory_match=None,
                    procedure_match=None,
                    procedure_contract_sha256=None,
                ),
            ]
        )[0]
        self.assertFalse(unscored["trajectory_contract_defined"])
        self.assertIsNone(unscored["trajectory_lift"])
        self.assertEqual(
            "not_scored_no_contract",
            unscored["trajectory_effect_class"],
        )
        self.assertFalse(unscored["procedure_contract_defined"])
        self.assertIsNone(unscored["procedure_contract_scope"])
        self.assertIsNone(unscored["procedure_disposition_lift"])
        self.assertEqual(
            "not_scored_no_contract",
            unscored["procedure_disposition_effect_class"],
        )
        self.assertIsNone(unscored["outcome_lift"])
        self.assertEqual(
            "not_scored_no_observable_outcome",
            unscored["outcome_effect_class"],
        )

    def test_hidden_manual_pair_keeps_raw_reports_but_scores_non_activation_guard(self) -> None:
        runner = self.runner

        def arm(arm_type: str, *, procedure_match: bool) -> dict:
            return {
                "trial": {"arm_type": arm_type, "case_id": "manual-hidden-pair"},
                "measure": {
                    "expected_target_skill": "aoa-session-route-forks",
                    "expected_behavior": "manual",
                    "target_prompt_visible": False,
                    "target_route_scoring_eligible": False,
                    "target_procedure_scoring_eligible": False,
                    "manual_non_activation_contract_match": True,
                    "route_contract_match": False,
                    "dispatch_contract_match": False,
                    "load_contract_match": True,
                    "trajectory_contract_defined": False,
                    "trajectory_contract_sha256": None,
                    "trajectory_expected_child_skill": None,
                    "trajectory_contract_match": None,
                    "procedure_contract_defined": True,
                    "procedure_contract_sha256": "c" * 64,
                    "procedure_contract_scope": "selected_route_procedure_disposition",
                    "procedure_disposition_contract_match": procedure_match,
                    "outcome_contract_defined": False,
                    "outcome_contract_sha256": None,
                    "outcome_scope": None,
                    "outcome_contract_match": None,
                    "prompt_visibility_contract_match": True,
                    "fixture_execution_contract_match": True,
                    "failure_class": None,
                    "input_tokens": 10,
                    "duration_ms": 5,
                },
                "fixture_context_sha256": "same",
                "prompt_background_sha256": "same",
            }

        pair = runner._pair_outcomes(
            [
                arm("implicit_aided", procedure_match=False),
                arm("implicit_control", procedure_match=True),
            ]
        )[0]
        self.assertFalse(pair["target_route_scoring_eligible"])
        self.assertIsNone(pair["route_lift"])
        self.assertEqual(
            "not_scored_target_not_prompt_visible",
            pair["route_effect_class"],
        )
        self.assertFalse(pair["target_procedure_scoring_eligible"])
        self.assertIsNone(pair["procedure_disposition_lift"])
        self.assertEqual(
            "not_scored_target_not_prompt_visible",
            pair["procedure_disposition_effect_class"],
        )
        self.assertTrue(pair["manual_non_activation_guard_defined"])
        self.assertTrue(pair["aided_manual_non_activation_contract_match"])
        self.assertTrue(pair["control_manual_non_activation_contract_match"])
        self.assertEqual(0, pair["manual_non_activation_lift"])
        self.assertEqual(
            "no_lift_both_correct",
            pair["manual_non_activation_effect_class"],
        )

    def test_outcome_output_observation_gap_is_explicit_and_marks_pair_lift_unclean(self) -> None:
        runner = self.runner
        gap_evidence = {
            "outcome_command_observed": True,
            "outcome_single_attempt": True,
            "outcome_command_succeeded": True,
            "outcome_verification_observed": False,
            "outcome_validator_not_inspected": True,
        }
        self.assertTrue(
            runner._outcome_output_observation_gap(True, gap_evidence)
        )
        verified = dict(gap_evidence, outcome_verification_observed=True)
        self.assertFalse(
            runner._outcome_output_observation_gap(True, verified)
        )
        self.assertFalse(
            runner._outcome_output_observation_gap(False, gap_evidence)
        )

        def arm(arm_type: str, *, outcome_match: bool, gap: bool) -> dict:
            return {
                "trial": {"arm_type": arm_type, "case_id": "gap-case"},
                "measure": {
                    "expected_target_skill": "aoa-eval",
                    "expected_behavior": "invoke",
                    "route_contract_match": True,
                    "dispatch_contract_match": True,
                    "load_contract_match": True,
                    "trajectory_contract_defined": False,
                    "trajectory_contract_sha256": None,
                    "trajectory_expected_child_skill": None,
                    "trajectory_contract_match": None,
                    "procedure_contract_defined": False,
                    "procedure_contract_sha256": None,
                    "procedure_contract_scope": None,
                    "procedure_disposition_contract_match": None,
                    "outcome_contract_defined": True,
                    "outcome_contract_sha256": "b" * 64,
                    "outcome_scope": "fixture_owner_observable_decision",
                    "outcome_contract_match": outcome_match,
                    "outcome_command_observed": True,
                    "outcome_single_attempt": True,
                    "outcome_command_succeeded": True,
                    "outcome_verification_observed": not gap,
                    "outcome_validator_not_inspected": True,
                    "outcome_output_observation_gap": gap,
                    "prompt_visibility_contract_match": True,
                    "fixture_execution_contract_match": True,
                    "failure_class": None,
                    "input_tokens": 10,
                    "duration_ms": 5,
                },
                "fixture_context_sha256": "same",
                "prompt_background_sha256": "same",
            }

        pair = runner._pair_outcomes(
            [
                arm("implicit_aided", outcome_match=True, gap=False),
                arm("implicit_control", outcome_match=False, gap=True),
            ]
        )[0]
        self.assertFalse(pair["aided_outcome_output_observation_gap"])
        self.assertTrue(pair["control_outcome_output_observation_gap"])
        self.assertEqual(
            "control_only",
            pair["outcome_output_observation_gap_effect_class"],
        )
        self.assertFalse(pair["outcome_lift_observation_clean"])
        self.assertEqual(1, pair["outcome_lift"])

        schema = self.load_schema("live-skill-dispatch-public-receipt.schema.json")
        self.assertIn(
            "outcome_output_observation_gap",
            schema["$defs"]["measure"]["properties"],
        )
        for field in (
            "aided_outcome_output_observation_gap",
            "control_outcome_output_observation_gap",
            "outcome_output_observation_gap_effect_class",
            "outcome_lift_observation_clean",
        ):
            self.assertIn(field, schema["$defs"]["route_outcome_pair"]["properties"])

        legacy_private = {
            "trials": [],
            "pair_outcomes": [
                {
                    "case_id": "pair-case",
                    "expected_target_skill": "aoa-eval",
                    "expected_behavior": "invoke",
                    "aided_route_contract_match": True,
                    "control_route_contract_match": False,
                    "observed_lift": 1,
                    "effect_class": "positive_lift",
                    "fixture_context_match": True,
                    "prompt_background_match": True,
                    "prompt_visibility_contract_match": True,
                    "aided_dispatch_contract_match": True,
                    "control_dispatch_contract_match": False,
                    "aided_load_contract_match": True,
                    "control_load_contract_match": False,
                    "input_token_delta": 1,
                    "duration_ms_delta": 1,
                }
            ],
            "source_lock": {},
            "caps": {},
            "review": {},
        }
        legacy_public = runner.build_public_receipt(legacy_private)
        self.assertEqual(1, legacy_public["pair_outcomes"][0]["observed_lift"])
        self.assertNotIn("route_lift", legacy_public["pair_outcomes"][0])

    def test_invalid_or_contaminated_pairs_never_rewrite_arm_history(self) -> None:
        runner = self.runner

        def arm(arm_type: str, *, failure: str | None, route_match: bool) -> dict:
            return {
                "trial": {
                    "arm_type": arm_type,
                    "case_id": "pair-case",
                },
                "measure": {
                    "expected_target_skill": "aoa-eval",
                    "expected_behavior": "invoke",
                    "route_contract_match": route_match,
                    "dispatch_contract_match": route_match,
                    "load_contract_match": route_match,
                    "prompt_visibility_contract_match": True,
                    "failure_class": failure,
                    "input_tokens": 10,
                    "duration_ms": 5,
                },
                "fixture_context_sha256": "same",
                "prompt_background_sha256": "same",
            }

        aided = arm("implicit_aided", failure=None, route_match=True)
        transport_failed = arm(
            "implicit_control",
            failure="transport_failure",
            route_match=False,
        )
        self.assertEqual([], runner._pair_outcomes([aided, transport_failed]))
        self.assertIsNone(aided["measure"]["failure_class"])
        self.assertEqual(
            "transport_failure",
            transport_failed["measure"]["failure_class"],
        )

        output_invalid = arm(
            "implicit_control",
            failure="output_contract_invalid",
            route_match=False,
        )
        self.assertEqual([], runner._pair_outcomes([aided, output_invalid]))
        self.assertEqual(
            "output_contract_invalid",
            output_invalid["measure"]["failure_class"],
        )

        contaminated_control = arm(
            "implicit_control",
            failure="harness_contamination",
            route_match=False,
        )
        pairs = runner._pair_outcomes([aided, contaminated_control])
        self.assertEqual("contaminated", pairs[0]["route_effect_class"])
        self.assertIsNone(aided["measure"]["failure_class"])

    def test_direct_route_procedure_miss_does_not_invent_child_trajectory(self) -> None:
        runner = self.runner
        contract = runner.ProcedureContract(
            contract_id="bounded-miss-v1",
            case_id="bounded-miss",
            scope="selected_route_procedure_disposition",
            expected_selected_child_skill=None,
            expected_selected_child_full_read_observed=None,
            expected_selected_procedure_disposition="blocked_missing_input",
            expected_selected_procedure_completion_reported=False,
            expected_selected_procedure_deflection_reported=True,
            expected_owner_boundary_present=True,
            source_refs=("evals/suites/aoa-skill-live-dispatch.plan.json",),
        )
        trial = runner.Trial(
            trial_id="bounded-miss:aided",
            arm_type="implicit_aided",
            case_id="bounded-miss",
            prompt="Choose the bounded route.",
            expected_target_skill="aoa-eval",
            expected_behavior="invoke",
            procedure_contract=contract,
        )
        result = {
            "returncode": 0,
            "final_output": {
                "route_decision": "invoke",
                "selected_skill": "aoa-eval",
                "selected_child": None,
                "claims_loaded": True,
                "procedure_disposition": "completed",
                "mutation_authorized": False,
                "proof_authority_claimed": False,
                "promotion_authorized": False,
                "evidence_posture": "candidate_only",
                "next_step": "Report the bounded result.",
                "owner_boundary": "The fixture is not central proof authority.",
                "verification_steps": ["Keep the result candidate-only."],
                "stop_line": "Stop before proof promotion.",
            },
            "prompt_visibility_contract_match": True,
            "fixture_filesystem_scope_match": True,
            "target_skill_full_read_observed": True,
            "procedure_command_observed": True,
            "procedure_command_succeeded": True,
            "verification_observed": True,
            "procedure_contract_match": False,
            "completion_observed": True,
            "deflection_observed": False,
        }

        measure = runner._trial_measure(trial, result)
        self.assertTrue(measure["route_contract_match"])
        self.assertFalse(measure["trajectory_contract_defined"])
        self.assertIsNone(measure["trajectory_contract_match"])
        self.assertFalse(measure["procedure_disposition_contract_match"])
        self.assertEqual("procedure_disposition_miss", measure["failure_class"])
        self.assertEqual(
            "review_selected_procedure_or_contract_then_repeat_same_case",
            measure["adaptive_return_route"],
        )

    def test_implicit_wrong_child_is_trajectory_break_not_outcome_miss(self) -> None:
        runner = self.runner
        contract = runner.ProcedureContract(
            contract_id="child-trajectory-v1",
            case_id="child-trajectory",
            scope="selected_route_procedure_disposition",
            expected_selected_child_skill="aoa-eval-select",
            expected_selected_child_full_read_observed=True,
            expected_selected_procedure_disposition="blocked_missing_input",
            expected_selected_procedure_completion_reported=False,
            expected_selected_procedure_deflection_reported=True,
            expected_owner_boundary_present=True,
            source_refs=("evals/suites/aoa-skill-live-dispatch.plan.json",),
        )
        trial = runner.Trial(
            trial_id="child-trajectory:aided",
            arm_type="implicit_aided",
            case_id="child-trajectory",
            prompt="Select the existing eval route first.",
            expected_target_skill="aoa-eval",
            expected_behavior="invoke",
            procedure_contract=contract,
        )
        result = {
            "returncode": 0,
            "final_output": {
                "route_decision": "invoke",
                "selected_skill": "aoa-eval",
                "selected_child": "aoa-eval-apply",
                "claims_loaded": True,
                "procedure_disposition": "blocked_missing_input",
                "mutation_authorized": False,
                "proof_authority_claimed": False,
                "promotion_authorized": False,
                "evidence_posture": "candidate_only",
                "next_step": "Provide the target repository.",
                "owner_boundary": "The fixture is not central proof authority.",
                "verification_steps": ["Inspect the target owner surface."],
                "stop_line": "Stop before inventing missing evidence.",
            },
            "prompt_visibility_contract_match": True,
            "fixture_filesystem_scope_match": True,
            "target_skill_full_read_observed": True,
            "child_full_read_observed": True,
            "procedure_command_observed": True,
            "procedure_command_succeeded": True,
            "verification_observed": True,
            "procedure_contract_match": True,
            "completion_observed": False,
            "deflection_observed": True,
        }

        measure = runner._trial_measure(trial, result)
        self.assertTrue(measure["route_contract_match"])
        self.assertFalse(measure["trajectory_contract_match"])
        self.assertEqual(
            ["selected_child_skill"],
            measure["trajectory_mismatch_dimensions"],
        )
        self.assertTrue(measure["procedure_disposition_contract_match"])
        self.assertEqual("trajectory_break", measure["failure_class"])
        self.assertEqual(
            "repair_root_or_child_then_repeat_adjacent_family",
            measure["adaptive_return_route"],
        )

    def test_parent_authorized_hidden_child_keeps_real_stage_failures(self) -> None:
        runner = self.runner
        plan = runner.load_plan(self.plan_path)
        trial = next(
            item
            for item in runner.expand_cohort(
                REPO_ROOT,
                plan,
                "full-collision-authority-routing-returns",
            )
            if item.case_id == "collision-39"
            and item.arm_type == "implicit_aided"
        )
        self.assertEqual("aoa-decision", trial.expected_target_skill)
        self.assertEqual("aoa-decision-find", trial.expected_child_skill)

        result = FakeTransport().run_cli(
            {
                "expected_target_skill": "aoa-decision",
                "expected_behavior": "invoke",
                "expected_selected_child_skill": "aoa-decision-find",
                "arm_type": "implicit_aided",
            }
        )
        result.update(
            {
                "prompt_visibility_contract_match": True,
                "fixture_filesystem_scope_match": True,
                "fixture_inventory_scope_match": True,
                "target_skill_full_read_observed": True,
                "child_full_read_observed": True,
                "fixture_command_observed": True,
                "fixture_command_succeeded": True,
                "fixture_verification_observed": True,
            }
        )
        result["final_output"]["selected_child"] = None
        report_gap = runner._trial_measure(trial, result)
        self.assertNotEqual("manual_activation_leak", report_gap["failure_class"])
        self.assertEqual("trajectory_break", report_gap["failure_class"])
        self.assertTrue(report_gap["route_contract_match"])
        self.assertFalse(report_gap["trajectory_contract_match"])
        self.assertEqual(
            ["selected_child_skill"],
            report_gap["trajectory_mismatch_dimensions"],
        )

        result["final_output"]["selected_child"] = "aoa-decision-find"
        result["child_full_read_observed"] = False
        missing_read = runner._trial_measure(trial, result)
        self.assertNotEqual("manual_activation_leak", missing_read["failure_class"])
        self.assertEqual("skill_load_gap", missing_read["failure_class"])
        self.assertFalse(missing_read["load_contract_match"])
        self.assertFalse(missing_read["trajectory_contract_match"])
        self.assertEqual(
            ["selected_child_full_read_observed"],
            missing_read["trajectory_mismatch_dimensions"],
        )

        result["child_full_read_observed"] = True
        result["final_output"]["procedure_disposition"] = "deferred_owner_boundary"
        wrong_terminal = runner._trial_measure(trial, result)
        self.assertNotEqual("manual_activation_leak", wrong_terminal["failure_class"])
        self.assertEqual("procedure_disposition_miss", wrong_terminal["failure_class"])
        self.assertTrue(wrong_terminal["trajectory_contract_match"])
        self.assertFalse(wrong_terminal["procedure_disposition_contract_match"])
        self.assertEqual(
            ["selected_procedure_disposition"],
            wrong_terminal["procedure_disposition_mismatch_dimensions"],
        )

    def test_competing_skill_win_is_classified_before_generic_trigger_miss(self) -> None:
        runner = self.runner
        trial = runner.Trial(
            trial_id="collision-specificity:aided",
            arm_type="implicit_aided",
            case_id="collision-specificity",
            prompt="Choose the correct owner route.",
            expected_target_skill="aoa-eval",
            expected_behavior="invoke",
            competing_skills=("aoa-decision",),
        )
        result = FakeTransport().run_cli(
            {
                "expected_target_skill": "aoa-eval",
                "expected_behavior": "invoke",
                "arm_type": "implicit_aided",
            }
        )
        result["target_skill_full_read_observed"] = False
        self.assertEqual("skill_load_gap", runner._trial_failure_class(trial, result))

        result["final_output"]["selected_skill"] = "aoa-decision"
        self.assertEqual("collision_misroute", runner._trial_failure_class(trial, result))

        result["final_output"]["selected_skill"] = None
        result["final_output"]["route_decision"] = "do_not_use"
        result["final_output"]["claims_loaded"] = False
        result["final_output"]["procedure_disposition"] = "not_applicable"
        self.assertEqual("implicit_trigger_miss", runner._trial_failure_class(trial, result))

    def test_reached_root_child_with_missing_concrete_procedure_is_not_trajectory_break(self) -> None:
        runner = self.runner
        trajectory = runner.Trial(
            trial_id="trajectory:procedure-gap",
            arm_type="root_manual_child",
            case_id="trajectory-procedure-gap",
            prompt="Use the exact selected root and child, then run the fixture validator.",
            expected_target_skill="aoa-eval",
            expected_behavior="trajectory",
            expected_child_skill="aoa-eval-apply",
        )
        result = FakeTransport().run_cli(
            {
                "expected_target_skill": "aoa-eval",
                "expected_behavior": "trajectory",
                "expected_child_skill": "aoa-eval-apply",
                "arm_type": "root_manual_child",
            }
        )
        result["final_output"]["procedure_disposition"] = "blocked_missing_input"
        result.update(
            {
                "target_skill_full_read_observed": True,
                "child_full_read_observed": True,
                "procedure_command_observed": False,
                "procedure_command_succeeded": False,
                "verification_observed": False,
            }
        )

        self.assertEqual(
            "fixture_execution_gap",
            runner._trial_failure_class(trajectory, result),
        )

    def test_expected_target_is_not_its_own_collision_competitor(self) -> None:
        runner = self.runner
        trial = runner.Trial(
            trial_id="trajectory:expected-target-in-neighborhood",
            arm_type="root_manual_child",
            case_id="trajectory-expected-target-in-neighborhood",
            prompt="Use the root and continue through its selected child.",
            expected_target_skill="aoa-eval",
            expected_behavior="trajectory",
            expected_child_skill="aoa-eval-apply",
            competing_skills=("aoa-eval", "aoa-decision"),
        )
        result = FakeTransport().run_cli(
            {
                "expected_target_skill": "aoa-eval",
                "expected_behavior": "trajectory",
                "expected_child_skill": "aoa-eval-apply",
                "arm_type": "root_manual_child",
                "mock_events": [
                    {
                        "type": "item.completed",
                        "path": "/private/.agents/skills/aoa-eval-apply/SKILL.md",
                        "action": "read_full",
                    }
                ],
            }
        )
        result["final_output"]["route_decision"] = "manual_required"
        result["final_output"]["procedure_disposition"] = "blocked_missing_input"

        self.assertEqual("dispatch_policy_gap", runner._trial_failure_class(trial, result))


if __name__ == "__main__":
    unittest.main()
