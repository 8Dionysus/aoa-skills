from __future__ import annotations

import ast
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validation_lanes


INVENTORY_PATH = REPO_ROOT / "docs" / "validation" / "validator_inventory.json"
TOPOLOGY_PATH = REPO_ROOT / "docs" / "validation" / "VALIDATOR_TOPOLOGY.md"
THIN_ROOT_ADAPTERS = (
    "scripts/validate_agent_skills.py",
    "scripts/validate_tiny_router_inputs.py",
    "scripts/validate_support_resources.py",
    "scripts/lint_trigger_evals.py",
    "scripts/lint_description_trigger_evals.py",
    "scripts/lint_pack_profiles.py",
    "scripts/lint_support_resources.py",
)
OWNER_MODULE_LIMITS = {
    "scripts/validators/tiny_router_surface.py": 180,
    "scripts/validators/support_resource_surface.py": 180,
    "scripts/validators/trigger_eval_surface.py": 180,
    "scripts/validators/pack_profile_surface.py": 120,
}


def load_inventory() -> dict:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def python_script_paths_from(commands: tuple[tuple[str, ...], ...]) -> set[str]:
    paths: set[str] = set()
    for command in commands:
        if len(command) >= 2 and command[0] == "python" and command[1].endswith(".py"):
            paths.add(command[1])
    return paths


class ValidatorTopologyTests(unittest.TestCase):
    def test_topology_doc_names_operational_route(self) -> None:
        text = TOPOLOGY_PATH.read_text(encoding="utf-8")

        for required in (
            "role",
            "input",
            "output",
            "owner",
            "lane",
            "failure route",
            "source-fast",
            "generated",
            "export",
            "release",
            "advisory",
        ):
            self.assertIn(required, text)

    def test_inventory_entries_are_complete_and_paths_exist(self) -> None:
        inventory = load_inventory()
        required_fields = set(inventory["required_fields"])
        self.assertGreater(len(inventory["entries"]), 20)

        paths: set[str] = set()
        for entry in inventory["entries"]:
            with self.subTest(path=entry.get("path")):
                self.assertTrue(required_fields.issubset(entry))
                self.assertNotIn(entry["path"], paths)
                paths.add(entry["path"])
                self.assertTrue((REPO_ROOT / entry["path"]).exists(), entry["path"])
                self.assertTrue(entry["failure_route"])
                self.assertIn(entry["decision"], {"keep", "split", "fold", "wire", "add", "keep-advisory"})

    def test_validation_lane_commands_are_in_inventory(self) -> None:
        inventory_paths = {entry["path"] for entry in load_inventory()["entries"]}
        lane_script_paths = set()
        for command_sequence in (
            validation_lanes.SOURCE_FAST_COMMAND_SEQUENCE,
            validation_lanes.EXPORT_GENERATED_CHECK_COMMAND_SEQUENCE,
            validation_lanes.RUNTIME_GENERATED_CHECK_COMMAND_SEQUENCE,
            validation_lanes.EXPORT_FULL_COMMAND_SEQUENCE,
            validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE,
            (validation_lanes.PACKAGING_SMOKE_COMMAND,),
        ):
            lane_script_paths.update(python_script_paths_from(command_sequence))

        missing = sorted(lane_script_paths - inventory_paths)
        self.assertEqual([], missing)

    def test_validation_like_entrypoints_are_not_orphaned(self) -> None:
        inventory_paths = {entry["path"] for entry in load_inventory()["entries"]}
        discovered = {
            path.relative_to(REPO_ROOT).as_posix()
            for pattern in (
                "validate_*.py",
                "lint_*.py",
                "audit_*.py",
                "report_*.py",
                "run_skill_reality_trials.py",
                "run_skills_ref_validation.py",
            )
            for path in SCRIPTS_DIR.glob(pattern)
        }
        discovered.update(
            {
                "scripts/ci_gate.py",
                "scripts/release_check.py",
                "scripts/smoke_skill_pack_handoff.py",
                "scripts/verify_skill_pack.py",
                ".agents/spark/scripts/validate_spark_lane.py",
            }
        )

        missing = sorted(discovered - inventory_paths)
        self.assertEqual([], missing)

    def test_known_root_adapters_stay_thin(self) -> None:
        for rel_path in THIN_ROOT_ADAPTERS:
            with self.subTest(path=rel_path):
                text = (REPO_ROOT / rel_path).read_text(encoding="utf-8")
                self.assertLessEqual(len(text.splitlines()), 40)
                self.assertIn("validators.", text)

    def test_retired_semantic_agents_validator_stays_folded(self) -> None:
        self.assertFalse((SCRIPTS_DIR / "validate_semantic_agents.py").exists())
        contract = json.loads(
            (SCRIPTS_DIR / "validators" / "nested_agents_contract.json").read_text(
                encoding="utf-8"
            )
        )
        paths = {entry["path"] for entry in contract["docs"]}
        for rel_path in (
            "config/AGENTS.md",
            "examples/AGENTS.md",
            "schemas/AGENTS.md",
            "scripts/AGENTS.md",
            "tests/AGENTS.md",
        ):
            self.assertIn(rel_path, paths)

    def test_owner_validator_modules_keep_bounded_function_sizes(self) -> None:
        for rel_path, line_limit in OWNER_MODULE_LIMITS.items():
            module_path = REPO_ROOT / rel_path
            syntax_tree = ast.parse(module_path.read_text(encoding="utf-8"))
            for node in ast.walk(syntax_tree):
                if not isinstance(node, ast.FunctionDef):
                    continue
                line_count = node.end_lineno - node.lineno + 1
                self.assertLessEqual(
                    line_count,
                    line_limit,
                    f"{rel_path}:{node.lineno} {node.name} has {line_count} lines",
                )


if __name__ == "__main__":
    unittest.main()
