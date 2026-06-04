from __future__ import annotations

import inspect
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validation import validate_agent_skills
from validation.validators import (
    agent_skills_catalog_surface,
    agent_skills_export_contract,
    agent_skills_export_surface,
    agent_skills_local_adapter_surface,
    agent_skills_project_surface,
)


class ValidateAgentSkillsEntrypointTests(unittest.TestCase):
    def test_cli_adapter_stays_thin(self) -> None:
        script_text = (SCRIPTS_DIR / "validate_agent_skills.py").read_text(
            encoding="utf-8"
        )

        self.assertIn("from _ingress import expose", script_text)
        self.assertIn('expose("validation.validate_agent_skills", globals())', script_text)
        self.assertLessEqual(len(script_text.splitlines()), 4)
        self.assertNotIn("load_json(generated_dir", script_text)

    def test_validate_returns_structured_result(self) -> None:
        result = validate_agent_skills.validate(REPO_ROOT)

        self.assertEqual([], result.errors)
        self.assertGreater(result.validated_skill_count, 0)
        self.assertEqual(REPO_ROOT / ".agents" / "skills", result.skills_root)

    def test_export_surface_validator_stays_phase_split(self) -> None:
        for helper_name in (
            "load_export_surface_documents",
            "build_export_surface_indexes",
            "validate_profile_markers",
            "validate_export_skill_sets",
            "validate_exported_skill_directory",
            "validate_project_core_kernel_surfaces",
            "validate_project_core_outer_ring_surfaces",
            "validate_project_risk_ring_surfaces",
            "validate_generated_evaluation_surfaces",
            "validate_runtime_guardrail_surfaces",
        ):
            self.assertTrue(hasattr(agent_skills_export_surface, helper_name), helper_name)

        validate_lines = inspect.getsource(agent_skills_export_surface.validate).splitlines()
        skill_lines = inspect.getsource(
            agent_skills_export_surface.validate_exported_skill_directory
        ).splitlines()

        self.assertLessEqual(len(validate_lines), 80)
        self.assertLessEqual(len(skill_lines), 180)

    def test_local_adapter_validation_is_phase_split(self) -> None:
        self.assertTrue(hasattr(agent_skills_local_adapter_surface, "validate_local_adapter_entry"))
        self.assertTrue(hasattr(agent_skills_local_adapter_surface, "validate_local_adapter_skill_sets"))

        export_source = inspect.getsource(agent_skills_export_surface.validate_exported_skill_directory)
        catalog_source = inspect.getsource(agent_skills_catalog_surface.validate_export_catalog_entries)
        adapter_source = inspect.getsource(agent_skills_local_adapter_surface.validate_local_adapter_entry)

        self.assertIn("agent_skills_catalog_surface.validate_export_catalog_entries(", export_source)
        self.assertIn("validate_local_adapter_entry(", catalog_source)
        self.assertNotIn("allowlist path does not exist", export_source)
        self.assertIn("allowlist path does not exist", adapter_source)

    def test_project_surface_validation_is_phase_split(self) -> None:
        self.assertTrue(hasattr(agent_skills_project_surface, "validate_project_core_kernel_surfaces"))
        self.assertTrue(hasattr(agent_skills_project_surface, "validate_project_core_outer_ring_surfaces"))
        self.assertTrue(hasattr(agent_skills_project_surface, "validate_project_risk_ring_surfaces"))
        self.assertTrue(hasattr(agent_skills_project_surface, "validate_project_foundation_profile"))

        validate_source = inspect.getsource(agent_skills_export_surface.validate)
        export_wrapper_source = inspect.getsource(agent_skills_export_surface.validate_project_core_kernel_surfaces)
        project_source = inspect.getsource(agent_skills_project_surface.validate_project_core_kernel_surfaces)

        self.assertIn("agent_skills_project_surface.validate_project_core_kernel_surfaces(", validate_source)
        self.assertIn("agent_skills_project_surface.validate_project_core_kernel_surfaces(", export_wrapper_source)
        self.assertNotIn("config/project_core_skill_kernel.json schema_version must be 1", export_wrapper_source)
        self.assertIn("config/project_core_skill_kernel.json schema_version must be 1", project_source)

    def test_export_contract_manifest_loads_runtime_constants(self) -> None:
        contract = agent_skills_export_contract.load_contract()

        self.assertEqual(validate_agent_skills.EXPORT_PROFILE, contract.export_profile)
        self.assertEqual(validate_agent_skills.REQUIRED_GENERATED_FILES, list(contract.required_generated_files))
        self.assertEqual(validate_agent_skills.EXPECTED_OUTER_RING_SKILLS, list(contract.expected_outer_ring_skills))
        self.assertEqual(
            validate_agent_skills.EXPECTED_RISK_RING_ADJACENT_OVERLAYS,
            list(contract.expected_risk_ring_adjacent_overlays),
        )

    def test_export_contract_rejects_duplicate_contract_lists(self) -> None:
        contract_path = agent_skills_export_contract.DEFAULT_CONTRACT_PATH
        payload = json.loads(contract_path.read_text(encoding="utf-8"))
        payload["required_config_files"].append(payload["required_config_files"][0])

        with tempfile.TemporaryDirectory() as tmpdir:
            broken_contract = Path(tmpdir) / "agent_skills_export_contract.json"
            broken_contract.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "required_config_files must not contain duplicates"):
                agent_skills_export_contract.load_contract(broken_contract)


if __name__ == "__main__":
    unittest.main()
