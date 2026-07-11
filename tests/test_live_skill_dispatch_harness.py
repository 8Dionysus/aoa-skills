from __future__ import annotations

import dataclasses
import hashlib
import importlib.util
import io
import json
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

    def run_cli(self, request: dict) -> dict:
        self.cli_calls.append(request)
        target = request["expected_target_skill"]
        decision = "manual_required" if request["expected_behavior"] == "manual" else "invoke"
        events = list(request.get("mock_events", []))
        if request["arm_type"] != "implicit_control" and not events and "fixture_root" in request:
            events.append(self._skill_read_event(request, target))
            child = request.get("expected_child_skill")
            if child:
                events.append(self._skill_read_event(request, child))
                events.append(self._validator_event(request))
        return {
            "returncode": 0,
            "stdout": "{\"type\":\"turn.completed\"}\n",
            "stderr": "",
            "final_output": {
                "route_decision": decision,
                "selected_skill": target,
                "selected_child": request.get("expected_child_skill"),
                "claims_loaded": request["arm_type"] != "implicit_control",
                "procedure_disposition": (
                    "completed" if request["arm_type"] == "root_manual_child" else "not_applicable"
                ),
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

    def test_cohort_expansion_closes_collision_and_manual_reachability_gaps(self) -> None:
        plan = self.runner.load_plan(self.plan_path)
        smoke = self.runner.expand_cohort(REPO_ROOT, plan, "smoke")
        pilot = self.runner.expand_cohort(REPO_ROOT, plan, "pilot13")
        collision = self.runner.expand_cohort(REPO_ROOT, plan, "full-collision")
        closure = self.runner.expand_cohort(REPO_ROOT, plan, "coverage-closure")

        self.assertEqual(4, len(smoke))
        self.assertEqual(30, len(pilot))
        self.assertEqual(98, len(collision))
        self.assertEqual(87, len(closure))
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
        self.assertEqual(28_000, first["caps"]["per_turn_weighted_token_limit"])
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
        self.assertEqual("codex-cli 0.144.1", contract["codex_version"])
        self.assertEqual(
            ["initialize", "initialized", "skills/list", "thread/start", "turn/start", "thread/delete"],
            contract["request_sequence"],
        )
        self.assertEqual(10, len(contract["schema_sha256"]))
        self.assertFalse(contract["proof_authority"])

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

        self.assertIn("--ephemeral", implicit["argv"])
        self.assertIn("--ignore-user-config", implicit["argv"])
        self.assertIn("read-only", implicit["argv"])
        self.assertTrue(trajectory["prompt"].startswith("$aoa-eval "))
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
                self.assertIn(
                    "mcp_servers.aoa_evals.enabled=false",
                    request["argv"],
                )
                self.assertIn("plugins", request["argv"])
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
        self.assertNotIn(
            "$aoa-eval-apply",
            structured["turn_start_params"]["input"][0]["text"],
        )
        self.assertEqual("thread/start", structured["thread_start_request"]["method"])
        self.assertEqual(180, implicit["timeout_seconds"])
        self.assertEqual(180, trajectory["timeout_seconds"])
        self.assertEqual(240, structured["timeout_seconds"])

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
            implicit_request = next(call for call in transport.cli_calls if call["arm_type"] == "implicit_aided")
            trajectory_request = next(call for call in transport.cli_calls if call["arm_type"] == "root_manual_child")
            self.assertIn("features.rollout_budget.limit_tokens=28000", implicit_request["argv"])
            self.assertIn("features.rollout_budget.limit_tokens=48000", trajectory_request["argv"])
            self.assertEqual(1, len(receipt["pair_outcomes"]))
            self.assertEqual("positive_lift", receipt["pair_outcomes"][0]["effect_class"])
            receipt_path = private_root / receipt["run_id"] / "private-receipt.json"
            self.assertTrue(receipt_path.is_file())
            self.assertEqual(0o700, private_root.stat().st_mode & 0o777)
            self.assertEqual(0o700, receipt_path.parent.stat().st_mode & 0o777)
            self.assertEqual(0o600, receipt_path.stat().st_mode & 0o777)
            for path in receipt_path.parent.rglob("*"):
                self.assertEqual(0o700 if path.is_dir() else 0o600, path.stat().st_mode & 0o777)
            Draft202012Validator(
                self.load_schema("live-skill-dispatch-private-receipt.schema.json")
            ).validate(receipt)

            public = runner.build_public_receipt(receipt)
            runner.validate_public_receipt(public)
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

    def test_real_preflight_requires_resource_wrapper_cgroup_and_exact_codex_version(self) -> None:
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
        request = {
            "private_root": "/srv/abyss-machine/tmp/ai/aoa-skill-live-evals",
            "estimated_private_bytes": 67_108_864,
            "resource_class": "light",
            "expected_codex_version": "codex-cli 0.144.1",
        }
        cgroup = "0::/user.slice/app.slice/abyss-machine-agents.slice/abyss-machine-agent-light-abc123.service\n"
        with (
            mock.patch.object(runner.subprocess, "run", side_effect=[storage_result, version_result]),
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

        with (
            mock.patch.object(runner.subprocess, "run", side_effect=[storage_result, version_result]),
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
        def run_mode(mode: str) -> dict:
            candidate = json.loads(json.dumps(request))
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
                    "procedure_command_observed": True,
                    "procedure_command_succeeded": True,
                    "verification_observed": True,
                },
                runner._procedure_execution_evidence([valid], fixture_root),
            )

            spoofed = json.loads(json.dumps(valid))
            spoofed["item"]["command"] = "echo python3 fixture_validator.py"
            self.assertEqual(
                {
                    "procedure_command_observed": False,
                    "procedure_command_succeeded": False,
                    "verification_observed": False,
                },
                runner._procedure_execution_evidence([spoofed], fixture_root),
            )

            split_success = json.loads(json.dumps(valid))
            split_success["item"]["aggregated_output"] = "no sentinel"
            split_sentinel = json.loads(json.dumps(valid))
            split_sentinel["item"]["exit_code"] = 1
            evidence = runner._procedure_execution_evidence(
                [split_success, split_sentinel],
                fixture_root,
            )
            self.assertTrue(evidence["procedure_command_observed"])
            self.assertTrue(evidence["procedure_command_succeeded"])
            self.assertFalse(evidence["verification_observed"])

            forged_payload = json.loads(json.dumps(valid))
            forged_payload["item"]["aggregated_output"] = (
                "AOA_FIXTURE_VALIDATOR_OK {\"status\":\"pass\"}"
            )
            self.assertFalse(
                runner._procedure_execution_evidence(
                    [forged_payload], fixture_root
                )["verification_observed"]
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
            "prompt_visibility_contract_match",
            "prompt_visible_repo_skill_count",
            "expected_prompt_visible_repo_skill_count",
            "structured_skill_surface_contract_match",
            "external_runtime_isolation_match",
            "dispatch_contract_match",
            "load_contract_match",
            "procedure_disposition",
            "procedure_command_observed",
            "procedure_command_succeeded",
            "verification_observed",
            "procedure_contract_match",
            "completion_observed",
            "deflection_observed",
        }
        self.assertLessEqual(stage_fields, set(public["measures"][0]))
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
            self.assertTrue(stage_fields.isdisjoint(measure))
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
                "direct_procedure_gap",
                "owner_boundary_violation",
                "runtime_profile_drift",
                "budget_exhausted",
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
            "repair_read_tooling_or_skill_load_then_repeat_same_case",
            self.runner.ADAPTIVE_RETURN_ROUTE["skill_load_gap"],
        )
        self.assertEqual(
            "review_caps_or_reduce_context_then_repeat_same_case",
            self.runner.ADAPTIVE_RETURN_ROUTE["budget_exhausted"],
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
        self.assertEqual("skill_load_gap", runner._trial_failure_class(trial, result))

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

        contaminated_control = arm(
            "implicit_control",
            failure="harness_contamination",
            route_match=False,
        )
        pairs = runner._pair_outcomes([aided, contaminated_control])
        self.assertEqual("contaminated", pairs[0]["effect_class"])
        self.assertIsNone(aided["measure"]["failure_class"])

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
            "direct_procedure_gap",
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
