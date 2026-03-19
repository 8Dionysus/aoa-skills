from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_SCHEMA_PATH = REPO_ROOT / "schemas" / "skill-frontmatter.schema.json"
SKILL_INDEX_PATH = REPO_ROOT / "SKILL_INDEX.md"
MATURITY_MODEL_PATH = REPO_ROOT / "docs" / "MATURITY_MODEL.md"


class MaturityModelDocsTests(unittest.TestCase):
    def test_maturity_ladder_is_consistent_across_schema_and_docs(self) -> None:
        schema = json.loads(SKILL_SCHEMA_PATH.read_text(encoding="utf-8"))
        statuses = schema["properties"]["status"]["enum"]
        index_text = SKILL_INDEX_PATH.read_text(encoding="utf-8")
        maturity_model_text = MATURITY_MODEL_PATH.read_text(encoding="utf-8")

        for status in statuses:
            with self.subTest(status=status):
                self.assertIn(f"`{status}`", index_text)
                self.assertIn(f"`{status}`", maturity_model_text)
