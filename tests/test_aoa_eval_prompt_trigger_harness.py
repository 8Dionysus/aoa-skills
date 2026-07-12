from __future__ import annotations

import re
import unittest
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_PATH = REPO_ROOT / "tests" / "fixtures" / "skill_evaluation_cases.yaml"
SUITE_PATH = REPO_ROOT / "evals" / "suites" / "aoa-eval-trigger-corpus.suite.md"
SKILL_PATH = REPO_ROOT / "skills" / "core" / "engineering" / "aoa-eval" / "SKILL.md"
RUNTIME_EXAMPLE_PATH = (
    REPO_ROOT / "skills" / "core" / "engineering" / "aoa-eval" / "examples" / "runtime.md"
)
APPLY_SKILL_PATH = (
    REPO_ROOT / "skills" / "core" / "engineering" / "aoa-eval-apply" / "SKILL.md"
)
APPLY_RUNTIME_EXAMPLE_PATH = (
    REPO_ROOT
    / "skills"
    / "core"
    / "engineering"
    / "aoa-eval-apply"
    / "examples"
    / "runtime.md"
)

AOA_EVAL_SKILLS = {
    "aoa-eval",
    "aoa-eval-select",
    "aoa-eval-apply",
    "aoa-eval-local-need",
    "aoa-eval-design",
    "aoa-eval-session-mining",
}

REQUIRED_TRIGGER_CLASSES = {
    "existing eval select/apply": {
        "eval_router_existing_or_missing_eval_route",
        "eval_select_existing_surface",
        "eval_apply_selected_validator",
    },
    "session front door": {"eval_router_session_front_door"},
    "route signs without keywords": {
        "eval_router_route_sign_without_eval_keyword",
        "eval_router_keyword_only_noise",
    },
    "local eval need/design": {
        "eval_local_need_no_existing_fit",
        "eval_design_local_suite",
    },
    "validator/test route": {"eval_apply_selected_validator"},
    "local suite JIT apply": {"eval_apply_selected_local_suite_sidecar"},
    "session mining after gates": {"eval_session_mining_missed_triggers"},
    "negative non-eval prompts": {
        "eval_router_plain_unit_test",
        "eval_router_source_authority_only",
    },
    "unclear owner boundary": {
        "eval_router_active_vs_stale_cleanup_boundary",
        "eval_router_workspace_inventory_route",
    },
}

SUBSKILL_USE_CASES = {
    "aoa-eval-select": "eval_select_existing_surface",
    "aoa-eval-apply": "eval_apply_selected_validator",
    "aoa-eval-local-need": "eval_local_need_no_existing_fit",
    "aoa-eval-design": "eval_design_local_suite",
    "aoa-eval-session-mining": "eval_session_mining_missed_triggers",
}

EXPECTED_DEFLECTIONS = {
    "eval_select_apply_already_chosen": "aoa-eval-apply",
    "eval_apply_no_selection_yet": "aoa-eval-select",
    "eval_local_need_existing_eval_available": "existing eval",
    "eval_design_apply_existing": "existing eval",
    "eval_session_mining_hook_repair_only": "raw .aoa maintenance",
}


def load_fixtures() -> dict[str, Any]:
    payload = yaml.safe_load(FIXTURES_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise AssertionError("skill evaluation fixture must be a mapping")
    return payload


def section_cases(fixtures: dict[str, Any], section: str) -> dict[str, dict[str, Any]]:
    cases = fixtures[section]
    if not isinstance(cases, list):
        raise AssertionError(f"{section} must be a list")
    return {case["case_id"]: case for case in cases if case["skill"] in AOA_EVAL_SKILLS}


def normalize(text: str) -> str:
    return " ".join(text.split())


def parse_snapshot(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^## (.+)$", text, flags=re.MULTILINE))
    sections: dict[str, str] = {}

    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[heading] = text[start:end].strip()

    return sections


class AoaEvalPromptTriggerHarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures = load_fixtures()
        cls.trigger_cases = section_cases(cls.fixtures, "trigger_cases")
        cls.snapshot_cases = section_cases(cls.fixtures, "snapshot_cases")
        cls.suite_text = SUITE_PATH.read_text(encoding="utf-8")

    def test_harness_covers_required_prompt_classes(self) -> None:
        available_cases = set(self.trigger_cases) | set(self.snapshot_cases)

        for label, required_cases in REQUIRED_TRIGGER_CLASSES.items():
            with self.subTest(prompt_class=label):
                self.assertTrue(
                    required_cases.issubset(available_cases),
                    msg=f"missing prompt-trigger cases: {sorted(required_cases - available_cases)}",
                )

        for trigger_class in (
            "should_use_existing_eval_select_or_apply",
            "should_design_missing_or_local_need",
            "should_run_validator_or_test",
            "should_not_trigger_eval",
            "owner_boundary_unclear",
            "session_front_door_first",
            "route_signs_without_keywords",
            "keyword_only_reject",
            "session_mining_after_gates",
            "trigger_eval_regression",
        ):
            with self.subTest(trigger_class=trigger_class):
                self.assertIn(trigger_class, self.suite_text)

    def test_route_signs_not_keyword_mentions_control_eval_router_trigger(self) -> None:
        positive = self.trigger_cases["eval_router_route_sign_without_eval_keyword"]
        negative = self.trigger_cases["eval_router_keyword_only_noise"]

        self.assertEqual("use", positive["expected"])
        self.assertEqual("do_not_use", negative["expected"])
        self.assertNotIn("eval", positive["prompt"].lower())
        self.assertIn("eval", negative["prompt"].lower())

        positive_required = " ".join(positive["required_phrases"])
        negative_required = " ".join(negative["required_phrases"])
        self.assertIn(
            "route signs can trigger this skill even when the user never says `eval`",
            positive_required,
        )
        self.assertIn(
            "keywords alone such as `eval`, `test`, `landing`, or `done` are not sufficient without route pressure",
            negative_required,
        )

        for expected in (
            "aoa-eval-keyword-mining-blindspot",
            "route_signs_without_keywords",
            "keyword_only_reject",
            "keywords alone",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.suite_text)

    def test_front_door_skill_raises_readiness_packet_before_subskill_choice(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        for expected in (
            "aoa_eval_session_start.py --json",
            "eval_forge_front_door",
            "EVAL_FORGE_OPERATING_PATH.md",
            "SESSION_MINING_CRITERIA.md",
            "LOCAL_PORT_DECISION_MATRIX.md",
            "validate_eval_candidate_packets.py --schema-only",
            "before choosing a subskill",
            "read-only routing aids, not proof objects",
            "references are routing aids, not proof authority",
            "candidate packets must remain candidate-only",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, skill_text)

        runtime_example = RUNTIME_EXAMPLE_PATH.read_text(encoding="utf-8")
        normalized_runtime_example = normalize(runtime_example)
        for expected in (
            "eval_forge_front_door",
            "EVAL_FORGE_OPERATING_PATH.md",
            "SESSION_MINING_CRITERIA.md",
            "LOCAL_PORT_DECISION_MATRIX.md",
            "routing aids, not proof acceptance",
        ):
            with self.subTest(runtime_example=expected):
                self.assertIn(normalize(expected), normalized_runtime_example)

        normalized_suite_text = normalize(self.suite_text)
        for expected in (
            "EVAL_FORGE_OPERATING_PATH.md",
            "SESSION_MINING_CRITERIA.md",
            "LOCAL_PORT_DECISION_MATRIX.md",
            "worksheet example",
            "exact route commands",
            "cannot score, promote, or accept proof",
        ):
            with self.subTest(suite=expected):
                self.assertIn(normalize(expected), normalized_suite_text)

    def test_router_loads_selected_child_before_following_its_procedure(self) -> None:
        skill_text = normalize(SKILL_PATH.read_text(encoding="utf-8"))

        for expected in (
            "read the selected subskill's complete `SKILL.md`",
            "the selected child name is selection evidence only, not load or handoff evidence",
            "do not apply the child procedure or report it loaded until that read is complete",
            "keep every unselected subskill out of context unless the route changes",
            "confirm the selected subskill's complete `SKILL.md` was read before its procedure",
        ):
            with self.subTest(expected=expected):
                self.assertIn(normalize(expected), skill_text)

        runtime_example = normalize(RUNTIME_EXAMPLE_PATH.read_text(encoding="utf-8"))
        for expected in (
            "read the selected child's complete `SKILL.md` before applying its procedure",
            "a returned child name proves selection, not load",
        ):
            with self.subTest(runtime_example=expected):
                self.assertIn(normalize(expected), runtime_example)

    def test_router_separates_live_workspace_readiness_from_exact_source_evidence(self) -> None:
        skill_text = normalize(SKILL_PATH.read_text(encoding="utf-8"))

        for expected in (
            "record the reported source root, Git commit, and dirty or divergent posture",
            "live-workspace packet",
            "exact merged or published evidence",
            "run the owner validator from the exact source tree or commit",
            "do not fast-forward, reset, or rewrite a dirty canonical checkout",
        ):
            with self.subTest(expected=expected):
                self.assertIn(normalize(expected), skill_text)

        runtime_example = normalize(RUNTIME_EXAMPLE_PATH.read_text(encoding="utf-8"))
        for expected in (
            "live-workspace routing evidence",
            "exact source tree or commit",
            "preserve a dirty canonical checkout",
        ):
            with self.subTest(runtime_example=expected):
                self.assertIn(normalize(expected), runtime_example)

    def test_router_selects_before_local_need_when_fit_is_unknown(self) -> None:
        skill_text = normalize(SKILL_PATH.read_text(encoding="utf-8"))

        for expected in (
            "`aoa-eval-select` is the default while fit is unknown",
            "Missing target-repository evidence is not evidence that no eval fits",
            "`aoa-eval-local-need` is allowed only after",
            "an explicit no-fit result",
            "stop inside `aoa-eval-select` with the missing input",
        ):
            with self.subTest(expected=expected):
                self.assertIn(normalize(expected), skill_text)

        runtime_example = normalize(RUNTIME_EXAMPLE_PATH.read_text(encoding="utf-8"))
        for expected in (
            "unknown fit routes to `aoa-eval-select`",
            "missing repository evidence does not authorize `aoa-eval-local-need`",
        ):
            with self.subTest(runtime_example=expected):
                self.assertIn(normalize(expected), runtime_example)

    def test_apply_skill_jit_revalidates_local_suite_execution_contract(self) -> None:
        skill_text = normalize(APPLY_SKILL_PATH.read_text(encoding="utf-8"))

        for expected in (
            "`evals/suites/<slug>.suite.json`",
            "`source-contract-ready`",
            "JIT-revalidate",
            "`runner.argv`, `runner.cwd`, timeout, and accepted exit codes",
            "inventory, readiness, dashboard, and MCP surfaces may inspect the sidecar but must not execute it",
            "interpreter, dependency inventory digest, ambient pytest plugins, config, and selected environment",
            "execution receipt linked to the source head and sidecar digest",
            "runtime reproducibility remains false",
            "passed candidate evidence",
        ):
            with self.subTest(expected=expected):
                self.assertIn(normalize(expected), skill_text)

        self.assertNotIn("green proof", skill_text.lower())

        runtime_example = normalize(APPLY_RUNTIME_EXAMPLE_PATH.read_text(encoding="utf-8"))
        for expected in (
            "JIT source validation",
            "exact validated argv",
            "environment capture",
            "private execution receipt",
            "not central proof acceptance",
        ):
            with self.subTest(runtime_example=expected):
                self.assertIn(normalize(expected), runtime_example)

    def test_snapshot_prompt_route_decisions_match_fixture_contract(self) -> None:
        for case_id, case in self.snapshot_cases.items():
            with self.subTest(case=case_id, skill=case["skill"]):
                snapshot_path = REPO_ROOT / case["snapshot_path"]
                snapshot = parse_snapshot(snapshot_path)

                self.assertEqual(case["prompt"], snapshot["Prompt"])
                self.assertEqual(case["expected"], snapshot["Expected selection"])
                self.assertIn(
                    f"Decision: {case['expected']} `{case['skill']}`",
                    snapshot["Why"],
                )

                normalized_snapshot = normalize("\n".join(snapshot.values())).lower()
                for phrase in case["required_output_phrases"]:
                    self.assertIn(normalize(phrase).lower(), normalized_snapshot)
                for phrase in case["forbidden_output_phrases"]:
                    self.assertNotIn(normalize(phrase).lower(), normalized_snapshot)

    def test_front_door_router_selects_one_next_route_or_deflects(self) -> None:
        positive = self.snapshot_cases["eval_router_existing_or_missing_eval_route"]
        positive_snapshot = parse_snapshot(REPO_ROOT / positive["snapshot_path"])

        expected_object = positive_snapshot["Expected object"]
        for route_name in (
            "select",
            "apply",
            "local-need",
            "design",
            "session-mining",
        ):
            self.assertIn(route_name, expected_object)
        self.assertIn("owner boundaries", expected_object)
        self.assertIn("not a proof owner", positive_snapshot["Boundary notes"].lower())

        negative = self.snapshot_cases["eval_router_plain_unit_test"]
        negative_snapshot = parse_snapshot(REPO_ROOT / negative["snapshot_path"])
        self.assertEqual("do_not_use", negative["expected"])
        self.assertIn("no eval-lane routing pressure", negative_snapshot["Why"])
        self.assertIn("Not every test is an eval-lane event", negative_snapshot["Boundary notes"])
        self.assertIn("no local eval intake", negative_snapshot["Verification hooks"])

    def test_subskill_pairs_cover_use_and_deflection_routes(self) -> None:
        for skill_name, use_case_id in SUBSKILL_USE_CASES.items():
            with self.subTest(skill=skill_name, route="use"):
                case = self.snapshot_cases[use_case_id]
                snapshot = parse_snapshot(REPO_ROOT / case["snapshot_path"])
                self.assertEqual(skill_name, case["skill"])
                self.assertEqual("use", case["expected"])
                self.assertIn(f"Decision: use `{skill_name}`", snapshot["Why"])
                boundary_notes = snapshot["Boundary notes"].lower()
                self.assertTrue(
                    any(
                        phrase in boundary_notes
                        for phrase in (
                            "proof",
                            "candidate-only",
                            "read-first",
                            "central",
                            "without a write",
                        )
                    ),
                    msg=f"{skill_name} use snapshot must name a proof or owner-boundary limit",
                )

        for case_id, expected_deflection in EXPECTED_DEFLECTIONS.items():
            with self.subTest(case=case_id, route="deflect"):
                case = self.snapshot_cases[case_id]
                snapshot = parse_snapshot(REPO_ROOT / case["snapshot_path"])
                self.assertEqual("do_not_use", case["expected"])
                combined = normalize("\n".join(snapshot.values())).lower()
                self.assertIn(expected_deflection.lower(), combined)

    def test_owner_boundary_unclear_stops_before_mcp_or_local_proof_promotion(self) -> None:
        boundary_case = self.trigger_cases["eval_router_active_vs_stale_cleanup_boundary"]
        inventory_case = self.trigger_cases["eval_router_workspace_inventory_route"]

        self.assertEqual("use", boundary_case["expected"])
        self.assertEqual("use", inventory_case["expected"])
        self.assertIn("route must separate proof authority", " ".join(boundary_case["required_phrases"]))
        self.assertIn("missing/skeleton/active/invalid", " ".join(inventory_case["required_phrases"]))

        for required in (
            "owner_boundary_unclear",
            "`aoa-evals-mcp` is an access plane",
            "must not create central proof truth",
            "stop before treating MCP output as central proof authority",
            "Local files remain candidate evidence until reviewed by the proper owner",
        ):
            with self.subTest(required=required):
                self.assertIn(required, self.suite_text)


if __name__ == "__main__":
    unittest.main()
