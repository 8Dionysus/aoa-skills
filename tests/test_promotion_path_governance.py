from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
DOCS_README_PATH = REPO_ROOT / "docs" / "README.md"
PROMOTION_PATH = REPO_ROOT / "docs" / "PROMOTION_PATH.md"
STATUS_PROMOTION_DIR = REPO_ROOT / "docs" / "reviews" / "status-promotions"
CANONICAL_REVIEW_DIR = REPO_ROOT / "docs" / "reviews" / "canonical-candidates"


def load_skill_statuses() -> dict[str, str]:
    statuses: dict[str, str] = {}
    for skill_dir in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        skill_md_path = skill_dir / "SKILL.md"
        text = skill_md_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            raise AssertionError(f"{skill_md_path} is missing frontmatter")

        closing_index = None
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                closing_index = index
                break

        if closing_index is None:
            raise AssertionError(f"{skill_md_path} is missing a closing frontmatter delimiter")

        metadata = yaml.safe_load("\n".join(lines[1:closing_index])) or {}
        if not isinstance(metadata, dict):
            raise AssertionError(f"{skill_md_path} frontmatter must parse to a mapping")

        status = metadata.get("status")
        if not isinstance(status, str):
            raise AssertionError(f"{skill_md_path} is missing a string status")
        statuses[skill_dir.name] = status
    return statuses


class PromotionPathGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_statuses = load_skill_statuses()

    def test_promotion_path_doc_exists_and_is_linked_from_docs_map(self) -> None:
        self.assertTrue(PROMOTION_PATH.is_file())
        docs_readme = DOCS_README_PATH.read_text(encoding="utf-8")
        self.assertIn("PROMOTION_PATH.md", docs_readme)

    def test_evaluated_skills_have_status_promotion_review_records(self) -> None:
        evaluated_skills = sorted(
            skill_name
            for skill_name, status in self.skill_statuses.items()
            if status == "evaluated"
        )
        self.assertTrue(evaluated_skills)

        for skill_name in evaluated_skills:
            with self.subTest(skill=skill_name):
                review_path = STATUS_PROMOTION_DIR / f"{skill_name}.md"
                self.assertTrue(
                    review_path.is_file(),
                    f"missing status-promotion review record for evaluated skill {skill_name}",
                )

    def test_canonical_skills_have_canonical_candidate_review_records(self) -> None:
        canonical_skills = sorted(
            skill_name
            for skill_name, status in self.skill_statuses.items()
            if status == "canonical"
        )
        self.assertTrue(canonical_skills)

        for skill_name in canonical_skills:
            with self.subTest(skill=skill_name):
                review_path = CANONICAL_REVIEW_DIR / f"{skill_name}.md"
                self.assertTrue(
                    review_path.is_file(),
                    f"missing canonical review record for canonical skill {skill_name}",
                )

    def test_public_review_records_reference_existing_skills(self) -> None:
        known_skills = set(self.skill_statuses)

        status_review_paths = sorted(
            path for path in STATUS_PROMOTION_DIR.glob("*.md") if path.name.lower() != "readme.md"
        )
        for review_path in status_review_paths:
            with self.subTest(surface="status-promotions", review=review_path.name):
                self.assertIn(review_path.stem, known_skills)

        candidate_review_paths = sorted(CANONICAL_REVIEW_DIR.glob("*.md"))
        for review_path in candidate_review_paths:
            with self.subTest(surface="canonical-candidates", review=review_path.name):
                self.assertIn(review_path.stem, known_skills)


if __name__ == "__main__":
    unittest.main()
