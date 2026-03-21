from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "schemas"
GENERATED_DIR = REPO_ROOT / "generated"


class GeneratedSurfaceSchemaTests(unittest.TestCase):
    def load_schema(self, filename: str) -> dict:
        return json.loads((SCHEMAS_DIR / filename).read_text(encoding="utf-8"))

    def validate(self, schema_filename: str, payload: dict) -> None:
        schema = self.load_schema(schema_filename)
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(payload)

    def test_current_generated_surfaces_validate(self) -> None:
        for schema_filename, generated_filename in [
            ("public_surface.schema.json", "public_surface.json"),
            ("skill_walkthroughs.schema.json", "skill_walkthroughs.json"),
            ("skill_evaluation_matrix.schema.json", "skill_evaluation_matrix.json"),
            ("skill_lineage_surface.schema.json", "skill_lineage_surface.json"),
            ("skill_boundary_matrix.schema.json", "skill_boundary_matrix.json"),
            ("governance_backlog.schema.json", "governance_backlog.json"),
            ("skill_bundle_index.schema.json", "skill_bundle_index.json"),
            ("skill_graph.schema.json", "skill_graph.json"),
        ]:
            with self.subTest(schema=schema_filename):
                self.validate(
                    schema_filename,
                    json.loads((GENERATED_DIR / generated_filename).read_text(encoding="utf-8")),
                )

    def test_schema_files_have_expected_titles(self) -> None:
        for schema_path in sorted(SCHEMAS_DIR.glob("*.schema.json")):
            with self.subTest(schema=schema_path.name):
                payload = json.loads(schema_path.read_text(encoding="utf-8"))
                self.assertIn("title", payload)
                self.assertTrue(payload["title"].startswith("aoa-skills "))


if __name__ == "__main__":
    unittest.main()
