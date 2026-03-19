from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
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


if __name__ == "__main__":
    unittest.main()
