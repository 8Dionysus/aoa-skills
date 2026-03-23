from __future__ import annotations

import textwrap
import unittest
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import skill_review_surface


REVIEW_DIR = REPO_ROOT / "docs" / "reviews" / "status-promotions"
README_PATH = REVIEW_DIR / "README.md"
TEMPLATE_PATH = REPO_ROOT / "templates" / "STATUS_PROMOTION_REVIEW.template.md"
REQUIRED_SECTIONS = [
    "Current status",
    "Target status",
    "Evidence reviewed",
    "Findings",
    "Gaps and blockers",
    "Recommendation",
]


class StatusPromotionReviewRecordsTests(unittest.TestCase):
    def test_status_promotion_surface_readme_exists(self) -> None:
        self.assertTrue(README_PATH.is_file())
        readme_text = README_PATH.read_text(encoding="utf-8")
        self.assertIn("non-canonical status promotions", readme_text)
        self.assertIn("templates/STATUS_PROMOTION_REVIEW.template.md", readme_text)

    def test_status_promotion_template_contains_required_sections(self) -> None:
        template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            with self.subTest(section=section):
                self.assertIn(f"## {section}", template_text)

    def test_status_promotion_records_use_required_sections_when_present(self) -> None:
        review_paths = sorted(
            path for path in REVIEW_DIR.glob("*.md") if path.name.lower() != "readme.md"
        )

        for review_path in review_paths:
            with self.subTest(review=review_path.name):
                review_text = review_path.read_text(encoding="utf-8")
                self.assertIn(
                    f"# {review_path.stem} status promotion review",
                    review_text,
                )
                for section in REQUIRED_SECTIONS:
                    self.assertIn(f"## {section}", review_text)

    def test_status_promotion_review_parser_reads_labelled_bullets(self) -> None:
        review_text = textwrap.dedent(
            """\
            ---
            name: demo-skill
            ---

            # demo-skill status promotion review

            ## Current status

            - current maturity status: evaluated
            - current machine-checkable floor: pass
            - current governance lane decision: stay_evaluated
            - scope: core
            - current lineage: published
            - reviewed revision: abc123

            ## Target status

            - target maturity status: evaluated
            - machine-checkable floor result: pass
            - recorded governance outcome: stay_evaluated

            ## Evidence reviewed

            - `skills/demo-skill/SKILL.md`

            ## Findings

            - runtime skill.md meaning changed: yes

            ## Gaps and blockers

            - blockers for this target status: missing comparative rationale
            - blockers for the next status step: none

            ## Recommendation

            Keep the skill evaluated.
            """
        )

        record = skill_review_surface.parse_status_promotion_review_text(
            skill_name="demo-skill",
            review_path="docs/reviews/status-promotions/demo-skill.md",
            review_text=review_text,
        )

        self.assertEqual("evaluated", record.current_maturity_status)
        self.assertEqual("pass", record.current_machine_checkable_floor)
        self.assertEqual("stay_evaluated", record.current_governance_lane_decision)
        self.assertEqual("core", record.scope)
        self.assertEqual("published", record.current_lineage)
        self.assertEqual("abc123", record.reviewed_revision)
        self.assertEqual("evaluated", record.target_maturity_status)
        self.assertEqual("pass", record.machine_checkable_floor_result)
        self.assertEqual("stay_evaluated", record.recorded_governance_outcome)
        self.assertTrue(record.runtime_skill_md_meaning_changed)
        self.assertEqual(("missing comparative rationale",), record.blockers_for_target_status)
        self.assertEqual(("none",), record.blockers_for_next_status_step)


if __name__ == "__main__":
    unittest.main()
