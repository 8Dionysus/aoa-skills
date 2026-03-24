from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"
DOCS_README_PATH = REPO_ROOT / "docs" / "README.md"
RELEASING_PATH = REPO_ROOT / "docs" / "RELEASING.md"


class ReleaseDocsTests(unittest.TestCase):
    def test_changelog_tracks_unreleased_and_v010_entry(self) -> None:
        changelog = CHANGELOG_PATH.read_text(encoding="utf-8")

        self.assertIn("## [Unreleased]", changelog)
        self.assertIn("## [0.1.0] - 2026-03-23", changelog)

    def test_docs_readme_links_releasing_doc(self) -> None:
        docs_readme = DOCS_README_PATH.read_text(encoding="utf-8")

        self.assertIn("RELEASING.md", docs_readme)

    def test_releasing_doc_mentions_release_check_tag_and_github_release(self) -> None:
        releasing = RELEASING_PATH.read_text(encoding="utf-8")

        self.assertIn("scripts/release_check.py", releasing)
        self.assertIn("Create a Git tag", releasing)
        self.assertIn("GitHub release", releasing)


if __name__ == "__main__":
    unittest.main()
