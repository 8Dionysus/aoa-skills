from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))

import validate_nested_agents


class NestedAgentsDocsTests(unittest.TestCase):
    def test_required_nested_agents_docs_are_present_and_shaped(self) -> None:
        issues = validate_nested_agents.validate(REPO_ROOT)
        self.assertEqual([], issues)


if __name__ == "__main__":
    unittest.main()
