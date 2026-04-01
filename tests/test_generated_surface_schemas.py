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
            ("skill_composition_audit.schema.json", "skill_composition_audit.json"),
            ("overlay_readiness.schema.json", "overlay_readiness.json"),
            ("skill_bundle_index.schema.json", "skill_bundle_index.json"),
            ("skill_graph.schema.json", "skill_graph.json"),
            ("release_manifest.schema.json", "release_manifest.json"),
        ]:
            with self.subTest(schema=schema_filename):
                self.validate(
                    schema_filename,
                    json.loads((GENERATED_DIR / generated_filename).read_text(encoding="utf-8")),
                )

    def test_skill_ability_example_surface_validates(self) -> None:
        self.validate(
            "skill_ability_catalog.schema.json",
            json.loads(
                (GENERATED_DIR / "skill_ability_cards.min.example.json").read_text(
                    encoding="utf-8"
                )
            ),
        )

    def test_schema_files_have_expected_titles(self) -> None:
        for schema_path in sorted(SCHEMAS_DIR.glob("*.schema.json")):
            with self.subTest(schema=schema_path.name):
                payload = json.loads(schema_path.read_text(encoding="utf-8"))
                self.assertIn("title", payload)
                self.assertTrue(payload["title"].startswith("aoa-skills "))

    def test_governance_backlog_schema_allows_project_overlay_reconciliation_values(self) -> None:
        payload = self.load_schema("governance_backlog.schema.json")
        self.assertEqual(payload["properties"]["governance_backlog_version"]["const"], 5)
        enum_values = payload["properties"]["skills"]["items"]["properties"][
            "readiness_reconciliation"
        ]["enum"]
        self.assertIn("project_overlay_eval_ready", enum_values)
        self.assertIn("project_overlay_federation_ready", enum_values)
        self.assertIn("project_overlay_needs_evidence", enum_values)

    def test_bundle_index_and_skill_graph_schemas_allow_relationship_depth(self) -> None:
        bundle_schema = self.load_schema("skill_bundle_index.schema.json")
        skill_properties = bundle_schema["properties"]["skills"]["items"]["properties"]
        self.assertEqual(bundle_schema["properties"]["bundle_index_version"]["minimum"], 2)
        self.assertIn("install_profiles", skill_properties)
        self.assertIn("artifact_group_coverage", skill_properties)
        self.assertIn("technique_lineage", skill_properties)

        graph_schema = self.load_schema("skill_graph.schema.json")
        node_enum = graph_schema["properties"]["nodes"]["items"]["properties"]["type"]["enum"]
        edge_enum = graph_schema["properties"]["edges"]["items"]["properties"]["kind"]["enum"]
        self.assertEqual(graph_schema["properties"]["skill_graph_version"]["minimum"], 2)
        self.assertIn("profile", node_enum)
        self.assertIn("artifact_group", node_enum)
        self.assertIn("included_in_profile", edge_enum)
        self.assertIn("available_in_artifact_group", edge_enum)

    def test_release_manifest_schema_allows_relationship_views(self) -> None:
        payload = self.load_schema("release_manifest.schema.json")
        self.assertEqual(payload["properties"]["schema_version"]["const"], 3)
        self.assertIn("relationship_views", payload["required"])
        self.assertIn("relationship_views", payload["properties"])


if __name__ == "__main__":
    unittest.main()
