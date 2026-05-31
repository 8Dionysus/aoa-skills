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

import validate_agent_skills
from validators import agent_skills_export_contract, agent_skills_export_surface


class ValidateAgentSkillsEntrypointTests(unittest.TestCase):
    def test_cli_adapter_stays_thin(self) -> None:
        script_text = (SCRIPTS_DIR / "validate_agent_skills.py").read_text(
            encoding="utf-8"
        )

        self.assertIn("validators.agent_skills_export_surface", script_text)
        self.assertLessEqual(len(script_text.splitlines()), 80)
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
