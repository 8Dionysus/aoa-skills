from __future__ import annotations

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

    def run_cli(self, request: dict) -> dict:
        self.cli_calls.append(request)
        target = request["expected_target_skill"]
        decision = "manual_required" if request["expected_behavior"] == "manual" else "invoke"
        return {
            "returncode": 0,
            "stdout": "{\"type\":\"turn.completed\"}\n",
            "stderr": "",
            "final_output": {
                "route_decision": decision,
                "selected_skill": target,
                "selected_child": request.get("expected_child_skill"),
                "claims_loaded": request["arm_type"] != "implicit_control",
                "mutation_authorized": False,
                "proof_authority_claimed": False,
                "promotion_authorized": False,
                "evidence_posture": "candidate_only",
                "next_step": "Use the bounded owner route.",
                "owner_boundary": "Local evidence is not central proof authority.",
                "verification_steps": ["Run the owner validator."],
                "stop_line": "Stop before mutation.",
            },
            "events": request.get("mock_events", []),
            "usage": {"input_tokens": 100, "cached_input_tokens": 0, "output_tokens": 40},
            "duration_ms": 25,
        }

    def run_app_server(self, request: dict) -> dict:
        self.app_server_calls.append(request)
        target = request["expected_target_skill"]
        return {
            "returncode": 0,
            "stdout": "",
            "stderr": "",
            "final_output": {
                "route_decision": "invoke",
                "selected_skill": target,
                "selected_child": None,
                "claims_loaded": True,
                "mutation_authorized": False,
                "proof_authority_claimed": False,
                "promotion_authorized": False,
                "evidence_posture": "candidate_only",
                "next_step": "Apply the loaded procedure.",
                "owner_boundary": "The local receipt is not a proof verdict.",
                "verification_steps": ["Keep the receipt local."],
                "stop_line": "Stop before unauthorized mutation.",
            },
            "events": [{"method": "turn/completed", "params": {"turn": {"status": "completed"}}}],
            "usage": {"input_tokens": 120, "cached_input_tokens": 0, "output_tokens": 50},
            "duration_ms": 30,
            "structured_skill_visible": True,
            "structured_skill_input_sent": True,
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
        self.assertEqual(1, first["caps"]["max_concurrency"])
        self.assertGreater(first["source_record_count"], 390)
        self.assertTrue(first["resource_wrapper_required"])
        self.assertEqual(
            ["abyss-machine", "resource", "launch", "--class", "light", "--kind", "agent"],
            first["resource_launch_prefix"][:7],
        )
        pilot = self.runner.build_plan_packet(REPO_ROOT, plan, "pilot13", "model-a", "medium")
        self.assertTrue(pilot["high_cost_confirmation_required"])

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
            timeout_seconds=180,
            full_timeout_seconds=240,
            disabled_skill_paths=(Path("/global/aoa-eval"),),
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
        self.assertIn("shell_tool", implicit["argv"])
        self.assertTrue(trajectory["prompt"].startswith("$aoa-eval "))
        self.assertNotIn("shell_tool", trajectory["argv"])
        flattened = json.dumps([implicit, trajectory, structured])
        self.assertNotIn("dangerously-bypass", flattened)
        self.assertNotIn("threadId", structured["turn_start_params"])
        self.assertEqual("skill", structured["turn_start_params"]["input"][1]["type"])
        self.assertEqual("aoa-eval-apply", structured["turn_start_params"]["input"][1]["name"])
        self.assertEqual("readOnly", structured["turn_start_params"]["sandboxPolicy"]["type"])
        self.assertEqual("thread/start", structured["thread_start_request"]["method"])
        self.assertEqual(180, implicit["timeout_seconds"])
        self.assertEqual(180, trajectory["timeout_seconds"])
        self.assertEqual(240, structured["timeout_seconds"])

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
            self.assertEqual(3, len(transport.cli_calls))
            self.assertEqual(1, len(transport.app_server_calls))
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
            "/home/dionysus/private.json",
            "sk-proj-secretvalue123456789",
            "Bearer abcdefghijklmnop",
            "turn_457",
            "019e9388-dc4c-7f82-b6bf-04bea3aed7f4",
        )
        for attack in attacks:
            with self.subTest(attack=attack):
                candidate = json.loads(json.dumps(base))
                candidate["review"]["note"] = attack
                with self.assertRaises(runner.PublicReceiptSafetyError):
                    runner.validate_public_receipt(candidate)

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
        script = r'''
import json
import sys

name, path = sys.argv[1:3]
sys.stderr.write("diagnostic-burst:" + ("x" * 131072))
sys.stderr.flush()
thread_id = "019f0000-0000-7000-8000-000000000001"
output = {
    "route_decision": "invoke",
    "selected_skill": name,
    "selected_child": None,
    "claims_loaded": True,
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
        response = {"id": 2, "result": {"data": [{"cwd": "/private/fixture", "errors": [], "skills": [{"name": name, "path": path, "enabled": True, "description": "fixture", "scope": "repo"}]}]}}
    elif method == "thread/start":
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
        request["argv"] = [sys.executable, "-u", "-c", script, "aoa-eval-apply", str(skill_path)]
        with tempfile.TemporaryDirectory() as td:
            stderr_path = Path(td) / "app-server.stderr.log"
            request["stderr_path"] = str(stderr_path)
            result = runner.RealTransport().run_app_server(request)
            self.assertEqual(0o600, stderr_path.stat().st_mode & 0o777)

        self.assertEqual(0, result["returncode"])
        self.assertTrue(result["turn_started"])
        self.assertTrue(result["structured_skill_visible"])
        self.assertTrue(result["structured_skill_input_sent"])
        self.assertIn("diagnostic-burst:", result["stderr"])
        self.assertEqual("aoa-eval-apply", result["final_output"]["selected_skill"])
        self.assertEqual(120, result["usage"]["input_tokens"])

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
        Draft202012Validator(
            self.load_schema("live-skill-dispatch-public-receipt.schema.json")
        ).validate(public)

    def test_failure_taxonomy_is_bounded_and_adaptive(self) -> None:
        taxonomy = self.runner.FAILURE_TAXONOMY
        self.assertEqual(
            {
                "harness_contamination",
                "implicit_trigger_miss",
                "collision_misroute",
                "manual_activation_leak",
                "trajectory_break",
                "direct_procedure_gap",
                "owner_boundary_violation",
                "runtime_profile_drift",
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


if __name__ == "__main__":
    unittest.main()
