from __future__ import annotations

import json
from copy import deepcopy
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent
SDK_FIXTURE_PATH = (
    WORKSPACE_ROOT / "aoa-sdk" / "examples" / "a2a" / "summon_return_checkpoint_e2e.fixture.json"
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class AoaSummonE2EFixtureTests(unittest.TestCase):
    def test_aoa_summon_runtime_example_points_to_sdk_e2e_fixture(self) -> None:
        skill_text = (REPO_ROOT / "skills" / "aoa-summon" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        runtime_text = (
            REPO_ROOT / "skills" / "aoa-summon" / "examples" / "runtime.md"
        ).read_text(encoding="utf-8")

        for text in (skill_text, runtime_text):
            self.assertIn(
                "repo:aoa-sdk/examples/a2a/summon_return_checkpoint_e2e.fixture.json",
                text,
            )

    def test_sdk_e2e_fixture_validates_aoa_summon_v3_contracts(self) -> None:
        if not SDK_FIXTURE_PATH.exists():
            self.skipTest("live aoa-sdk E2E fixture is unavailable")

        request_schema = load_json(
            REPO_ROOT
            / "skills"
            / "aoa-summon"
            / "references"
            / "summon-request-v3.schema.json"
        )
        result_schema = load_json(
            REPO_ROOT
            / "skills"
            / "aoa-summon"
            / "references"
            / "summon-result-v3.schema.json"
        )
        fixture = load_json(SDK_FIXTURE_PATH)

        request_errors = sorted(
            Draft202012Validator(request_schema).iter_errors(fixture["summon_request"]),
            key=lambda error: list(error.absolute_path),
        )
        result_errors = sorted(
            Draft202012Validator(result_schema).iter_errors(fixture["summon_result"]),
            key=lambda error: list(error.absolute_path),
        )

        self.assertEqual(request_errors, [])
        self.assertEqual(result_errors, [])
        self.assertEqual(fixture["summon_decision"]["lane"], "codex_local_reviewed")
        self.assertIs(fixture["dry_run"], True)
        self.assertIs(fixture["live_automation"], False)

        request_validator = Draft202012Validator(request_schema)
        anchorless_request = deepcopy(fixture["summon_request"])
        anchorless_request["quest_passport"].pop("route_anchor", None)
        anchorless_request["summon_request"].pop("parent_task_id", None)
        anchorless_request["summon_request"].pop("session_ref", None)
        self.assertFalse(request_validator.is_valid(anchorless_request))

        empty_outputs_request = deepcopy(fixture["summon_request"])
        empty_outputs_request["expected_outputs"] = []
        self.assertFalse(request_validator.is_valid(empty_outputs_request))


if __name__ == "__main__":
    unittest.main()
