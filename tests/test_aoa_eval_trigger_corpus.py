from __future__ import annotations

import re
import unittest
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SUITE_PATH = REPO_ROOT / "evals" / "suites" / "aoa-eval-trigger-corpus.suite.md"
REPORT_PATH = REPO_ROOT / "evals" / "reports" / "aoa-eval-session-mining.report.md"
PORT_PATH = REPO_ROOT / "evals" / "PORT.yaml"


def load_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        raise AssertionError(f"{path} must start with YAML frontmatter")
    payload = yaml.safe_load(match.group(1))
    if not isinstance(payload, dict):
        raise AssertionError(f"{path} frontmatter must be a mapping")
    return payload, match.group(2)


class AoaEvalTriggerCorpusTests(unittest.TestCase):
    def test_local_eval_port_is_active_with_expected_notes(self) -> None:
        port = yaml.safe_load(PORT_PATH.read_text(encoding="utf-8"))

        self.assertEqual(port["schema_version"], "local_eval_port_v1")
        self.assertEqual(port["owner_repo"], "aoa-skills")
        self.assertEqual(port["status"], "active")
        self.assertEqual(port["proof_owner_repo"], "aoa-evals")
        self.assertTrue(SUITE_PATH.is_file())
        self.assertTrue(REPORT_PATH.is_file())

    def test_suite_frontmatter_and_trigger_taxonomy(self) -> None:
        frontmatter, body = load_frontmatter(SUITE_PATH)

        self.assertEqual(frontmatter["schema_version"], "local_eval_suite_note_v1")
        self.assertEqual(frontmatter["owner_repo"], "aoa-skills")
        self.assertEqual(frontmatter["status"], "draft")
        self.assertEqual(
            frontmatter["authority_boundary"],
            "no verdict, scoring, regression, or proof doctrine authority",
        )

        for trigger_class in (
            "should_use_aoa_eval_router",
            "should_use_existing_eval_select_or_apply",
            "should_design_missing_or_local_need",
            "should_run_validator_or_test",
            "should_not_trigger_eval",
            "owner_boundary_unclear",
            "session_mining_after_gates",
            "trigger_eval_regression",
        ):
            self.assertIn(trigger_class, body)

    def test_suite_preserves_candidate_session_refs(self) -> None:
        _, body = load_frontmatter(SUITE_PATH)

        for expected in (
            "019eb8c7-a7b5-76f0-b66a-0eb3791305ff",
            "019e5c96-3c6b-7382-a17d-4d76a4d4c079",
            "019e9388-dc4c-7f82-b6bf-04bea3aed7f4",
            "019e8f02-62ef-7931-ab39-631e4bde80a8",
            "019dfb8e-2e54-7f92-9eb2-f26b13eeaa2d",
            "raw:line:7511",
            "raw:line:6805",
            "raw:line:7506",
            "segment_index_live_check: fresh",
            "eval_router_plain_unit_test",
        ):
            self.assertIn(expected, body)

    def test_report_records_mining_method_and_proof_limits(self) -> None:
        frontmatter, body = load_frontmatter(REPORT_PATH)

        self.assertEqual(frontmatter["schema_version"], "local_eval_report_note_v1")
        self.assertEqual(frontmatter["owner_repo"], "aoa-skills")
        self.assertEqual(frontmatter["status"], "draft")
        self.assertEqual(
            frontmatter["authority_boundary"],
            "no verdict, scoring, regression, or proof doctrine authority",
        )

        for expected in (
            "portable_sqlite",
            "ready_with_deferred_live_updates",
            "segment_index_live_check: fresh",
            "raw:line:7511",
            "raw:line:11361",
            "candidate evidence",
            "not proof",
            "Central adoption, scoring, verdicts",
        ):
            self.assertIn(expected, body)


if __name__ == "__main__":
    unittest.main()
