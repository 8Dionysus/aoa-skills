from __future__ import annotations

import sys
import tempfile
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

    def test_contract_manifest_loads_required_doc_specs(self) -> None:
        specs = validate_nested_agents.default_contract(REPO_ROOT)
        self.assertEqual(len(specs), len(validate_nested_agents.REQUIRED_DOCS))
        self.assertIn(
            Path("mechanics") / "release-support" / "AGENTS.md",
            {spec.path for spec in specs},
        )

    def test_contract_manifest_rejects_duplicate_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            contract_path = Path(tmpdir) / "nested_agents_contract.json"
            contract_path.write_text(
                """
{
  "schema_version": 1,
  "docs": [
    {"path": "mechanics/AGENTS.md", "required_snippets": ["# AGENTS.md"]},
    {"path": "mechanics/AGENTS.md", "required_snippets": ["duplicate"]}
  ]
}
""".strip()
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                validate_nested_agents.load_contract(contract_path)


if __name__ == "__main__":
    unittest.main()
