from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validation.validators import skill_effectiveness_family_review_surface


REVIEW_PATH = (
    REPO_ROOT
    / "docs"
    / "reviews"
    / "skill-effectiveness"
    / "aoa-family-current.json"
)
SCHEMA_PATH = (
    REPO_ROOT
    / "mechanics"
    / "method-growth"
    / "schemas"
    / "skill_effectiveness_family_review_v1.json"
)


def load_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise AssertionError(f"{path} must contain an object")
    return payload


class SkillEffectivenessFamilyReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.review = load_json(REVIEW_PATH)

    def assert_invalid(self, payload: dict[str, object], message: str) -> None:
        summary = skill_effectiveness_family_review_surface.validate_document(
            REPO_ROOT,
            payload,
        )
        self.assertTrue(summary.issues, message)

    def test_schema_and_current_review_are_valid(self) -> None:
        schema = load_json(SCHEMA_PATH)
        Draft202012Validator.check_schema(schema)
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(self.review)))

        summary = skill_effectiveness_family_review_surface.validate_summary(REPO_ROOT)
        self.assertEqual(57, summary.expected_skill_count)
        self.assertEqual(57, summary.reviewed_skill_count)
        self.assertEqual((), summary.issues)

    def test_review_keeps_authority_and_episode_stages_separate(self) -> None:
        authority = self.review["authority"]
        self.assertIsInstance(authority, dict)
        for field in (
            "proof_authority",
            "promotion_authority",
            "runtime_authority",
            "raw_session_content_included",
            "private_evidence_included",
        ):
            self.assertIs(authority[field], False)

        entries = self.review["entries"]
        self.assertIsInstance(entries, list)
        for entry in entries:
            with self.subTest(skill=entry["name"]):
                evidence = entry["evidence"]
                self.assertEqual("reviewed_candidate_only", evidence["evidence_posture"])
                self.assertEqual("not_used_as_effectiveness_proof", evidence["cooccurrence_signal"])
                self.assertIn("prompt_visibility", evidence)
                self.assertIn("selection", evidence)
                self.assertIn("load_read", evidence)
                self.assertIn("procedure", evidence)
                self.assertIn("verification", evidence)
                self.assertIn("outcome", evidence)
                self.assertIn("mention_signal", evidence)

    def test_review_has_exactly_one_disposition_per_current_skill(self) -> None:
        entries = self.review["entries"]
        names = [entry["name"] for entry in entries]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(
            {
                "improve": 4,
                "split": 0,
                "merge": 0,
                "promote": 7,
                "retain": 46,
                "retire": 0,
            },
            self.review["decision_counts"],
        )

    def test_membership_status_scope_and_paths_are_source_exact(self) -> None:
        mutated = copy.deepcopy(self.review)
        mutated["entries"][0]["source_status"] = "deprecated"
        self.assert_invalid(mutated, "source-status drift must fail")

        mutated = copy.deepcopy(self.review)
        mutated["entries"][0]["scope"] = "risk"
        self.assert_invalid(mutated, "scope drift must fail")

        mutated = copy.deepcopy(self.review)
        mutated["entries"][0]["skill_path"] = "skills/not-real/SKILL.md"
        self.assert_invalid(mutated, "skill-path drift must fail")

        mutated = copy.deepcopy(self.review)
        mutated["entries"].pop()
        self.assert_invalid(mutated, "family omission must fail")

    def test_decision_counts_and_disposition_details_are_constrained(self) -> None:
        mutated = copy.deepcopy(self.review)
        mutated["decision_counts"]["retain"] -= 1
        self.assert_invalid(mutated, "decision-count drift must fail")

        promote_entry = next(
            entry for entry in self.review["entries"] if entry["disposition"] == "promote"
        )
        mutated = copy.deepcopy(self.review)
        target = next(entry for entry in mutated["entries"] if entry["name"] == promote_entry["name"])
        target.pop("target_status")
        self.assert_invalid(mutated, "promotion without target status must fail")

        retain_entry = next(
            entry for entry in self.review["entries"] if entry["disposition"] == "retain"
        )
        mutated = copy.deepcopy(self.review)
        target = next(entry for entry in mutated["entries"] if entry["name"] == retain_entry["name"])
        target["target_status"] = "canonical"
        self.assert_invalid(mutated, "retain must not smuggle a promotion target")

    def test_private_absolute_and_raw_session_refs_are_rejected(self) -> None:
        for unsafe_ref in (
            "/srv/AbyssOS/private.json",
            "/home/dionysus/.codex/sessions/raw.jsonl",
            ".aoa/sessions/raw.jsonl",
            "../outside/review.json",
            "file:///tmp/raw.json",
        ):
            with self.subTest(ref=unsafe_ref):
                mutated = copy.deepcopy(self.review)
                mutated["entries"][0]["evidence"]["episode_refs"] = [unsafe_ref]
                self.assert_invalid(mutated, f"unsafe ref must fail: {unsafe_ref}")

    def test_live_gaps_remain_visible_for_eval_children(self) -> None:
        by_name = {entry["name"]: entry for entry in self.review["entries"]}
        for name in ("aoa-eval-design", "aoa-eval-local-need"):
            with self.subTest(skill=name):
                entry = by_name[name]
                self.assertEqual("promote", entry["disposition"])
                self.assertEqual("not_observed", entry["evidence"]["selection"])
                self.assertEqual("not_observed", entry["evidence"]["outcome"])
                self.assertIn("direct live selection", entry["next_review_condition"])


if __name__ == "__main__":
    unittest.main()
