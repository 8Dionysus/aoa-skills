from __future__ import annotations

import json
from copy import deepcopy
import unittest
from pathlib import Path
import sys

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from skill_model import skill_layout

WORKSPACE_ROOT = REPO_ROOT.parent
SDK_FIXTURE_PATH = (
    WORKSPACE_ROOT / "aoa-sdk" / "examples" / "a2a" / "summon_return_checkpoint_e2e.fixture.json"
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class AoaSummonE2EFixtureTests(unittest.TestCase):
    def test_aoa_summon_docs_use_v3_contract_tokens(self) -> None:
        skill_dir = skill_layout.skill_dir_path(REPO_ROOT, "aoa-summon")
        exported_dir = REPO_ROOT / ".agents" / "skills" / "aoa-summon"
        request_schema = load_json(
            skill_dir / "references" / "summon-request-v3.schema.json"
        )
        result_schema = load_json(
            skill_dir / "references" / "summon-result-v3.schema.json"
        )

        lane_tokens = set(result_schema["properties"]["lane"]["enum"])
        self.assertEqual(
            lane_tokens,
            {
                "codex_local_leaf",
                "codex_local_reviewed",
                "remote_reviewed",
                "split_required",
                "human_gate",
            },
        )
        self.assertEqual(
            request_schema["properties"]["summon_request"]["properties"][
                "transport_preference"
            ]["enum"],
            ["codex_local", "a2a_remote", "either"],
        )
        self.assertIn("codex_local_target", result_schema["properties"])

        for path in (skill_dir / "SKILL.md", exported_dir / "SKILL.md"):
            text = path.read_text(encoding="utf-8")
            for token in lane_tokens:
                self.assertIn(f"`{token}`", text)
            self.assertIn("`transport_preference` to `codex_local`", text)
            self.assertIn("`codex_local_target`", text)
            for stale_phrase in (
                "local leaf execution",
                "local reviewed execution",
                "local child target",
                "`transport_preference` to local execution",
            ):
                self.assertNotIn(stale_phrase, text)

    def test_aoa_summon_runtime_example_points_to_sdk_e2e_fixture(self) -> None:
        skill_dir = skill_layout.skill_dir_path(REPO_ROOT, "aoa-summon")
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        runtime_text = (skill_dir / "examples" / "runtime.md").read_text(encoding="utf-8")

        for text in (skill_text, runtime_text):
            self.assertIn(
                "repo:aoa-sdk/examples/a2a/summon_return_checkpoint_e2e.fixture.json",
                text,
            )

    def test_sdk_e2e_fixture_validates_aoa_summon_v3_contracts(self) -> None:
        if not SDK_FIXTURE_PATH.exists():
            self.skipTest("live aoa-sdk E2E fixture is unavailable")

        skill_dir = skill_layout.skill_dir_path(REPO_ROOT, "aoa-summon")
        request_schema = load_json(
            skill_dir / "references" / "summon-request-v3.schema.json"
        )
        result_schema = load_json(
            skill_dir / "references" / "summon-result-v3.schema.json"
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
