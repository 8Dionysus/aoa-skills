from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MATURITY_MODEL_PATH = REPO_ROOT / "docs" / "MATURITY_MODEL.md"
REVIEW_DIR = REPO_ROOT / "docs" / "reviews" / "canonical-candidates"
TEMPLATE_PATH = REPO_ROOT / "templates" / "CANDIDATE_REVIEW.template.md"
REQUIRED_SECTIONS = [
    "Current status",
    "Canonical gate check",
    "Evidence reviewed",
    "Findings",
    "Gaps and blockers",
    "Recommendation",
]


def extract_first_canonical_candidates(text: str) -> list[str]:
    match = re.search(
        r"## First canonical candidates\s+(.*?)(?:\n## |\Z)",
        text,
        flags=re.DOTALL,
    )
    if not match:
        raise AssertionError("missing 'First canonical candidates' section")

    return re.findall(r"- `(aoa-[a-z0-9-]+)`", match.group(1))


class CandidateReviewRecordsTests(unittest.TestCase):
    def test_first_canonical_candidates_have_review_records(self) -> None:
        maturity_model_text = MATURITY_MODEL_PATH.read_text(encoding="utf-8")
        candidates = extract_first_canonical_candidates(maturity_model_text)
        self.assertTrue(candidates)

        for skill_name in candidates:
            with self.subTest(skill=skill_name):
                review_path = REVIEW_DIR / f"{skill_name}.md"
                self.assertTrue(review_path.is_file(), f"missing review record for {skill_name}")
                review_text = review_path.read_text(encoding="utf-8")
                self.assertIn(f"# {skill_name} candidate review", review_text)
                for section in REQUIRED_SECTIONS:
                    self.assertIn(f"## {section}", review_text)

    def test_candidate_review_template_contains_required_sections(self) -> None:
        template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            with self.subTest(section=section):
                self.assertIn(f"## {section}", template_text)
