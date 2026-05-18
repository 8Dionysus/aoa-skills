from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"
README_PATH = REPO_ROOT / "README.md"
DOCS_README_PATH = REPO_ROOT / "docs" / "README.md"
RELEASING_PATH = (
    REPO_ROOT / "mechanics" / "release-support" / "docs" / "RELEASING.md"
)


class ReleaseDocsTests(unittest.TestCase):
    def test_changelog_tracks_unreleased_and_latest_release_entry(self) -> None:
        changelog = CHANGELOG_PATH.read_text(encoding="utf-8")

        self.assertIn("## [Unreleased]", changelog)
        self.assertIn("## [0.3.3] - 2026-04-23", changelog)
        self.assertIn("## [0.3.0] - 2026-04-10", changelog)
        self.assertIn("## [0.2.0] - 2026-04-01", changelog)

    def test_docs_readme_links_releasing_doc(self) -> None:
        docs_readme = DOCS_README_PATH.read_text(encoding="utf-8")

        self.assertIn("RELEASING.md", docs_readme)

    def test_readme_routes_release_claim_gates_without_owning_commands(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("mechanics/release-support/docs/RELEASING.md", readme)
        self.assertIn("AGENTS.md", readme)
        self.assertNotIn("--fail-on-review-truth-sync", readme)
        self.assertNotIn("--fail-on-drift", readme)

    def test_releasing_doc_mentions_release_check_tag_and_github_release(self) -> None:
        releasing = RELEASING_PATH.read_text(encoding="utf-8")

        self.assertIn("scripts/release_check.py", releasing)
        self.assertIn("--include-packaging-smoke", releasing)
        self.assertIn("Create a Git tag", releasing)
        self.assertIn("GitHub release", releasing)


if __name__ == "__main__":
    unittest.main()
