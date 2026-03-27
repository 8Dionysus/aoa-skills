from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TARGETS = (
    ("aoa-dry-run-first", "dry_run_report.schema.json", "dry_run_contract.template.json"),
    ("aoa-safe-infra-change", "infra_change_report.schema.json", "infra_change_contract.template.json"),
    ("aoa-local-stack-bringup", "local_stack_report.schema.json", "local_stack_bringup.template.json"),
)


class SupportResourceSchemaTests(unittest.TestCase):
    def test_schemas_and_templates_exist_and_parse(self) -> None:
        for skill, schema_name, template_name in TARGETS:
            assets = REPO_ROOT / "skills" / skill / "assets"
            schema = json.loads((assets / schema_name).read_text(encoding="utf-8"))
            template = json.loads((assets / template_name).read_text(encoding="utf-8"))
            self.assertEqual(schema["type"], "object")
            self.assertIn("title", schema)
            self.assertIsInstance(template, dict)

    def test_required_keys_are_declared(self) -> None:
        for skill, schema_name, _ in TARGETS:
            assets = REPO_ROOT / "skills" / skill / "assets"
            schema = json.loads((assets / schema_name).read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(schema.get("required", [])), 5)

    def test_manifest_builder_outputs_expected_files(self) -> None:
        generated = REPO_ROOT / "generated"
        self.assertTrue((generated / "deterministic_resource_manifest.json").exists())
        self.assertTrue((generated / "support_resource_index.json").exists())
        self.assertTrue((generated / "structured_output_schema_index.json").exists())
        self.assertTrue((generated / "support_resource_bridge_map.json").exists())
        self.assertTrue((generated / "expected_existing_aoa_support_dirs.json").exists())


if __name__ == "__main__":
    unittest.main()
