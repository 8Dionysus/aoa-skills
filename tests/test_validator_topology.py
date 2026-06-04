from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lanes import validation_lanes


INVENTORY_PATH = REPO_ROOT / "docs" / "validation" / "validator_inventory.json"
TOPOLOGY_PATH = REPO_ROOT / "docs" / "validation" / "VALIDATOR_TOPOLOGY.md"
VALIDATION_LANES_MANIFEST_PATH = REPO_ROOT / "config" / "validation_lanes.json"
AGENTS_VALIDATION_PREAMBLE = (
    "Full lane command sequences live in `config/validation_lanes.json`; "
    "this local card may name only focused owner checks, lane ids, or the "
    "nearest route for the changed surface."
)
VALIDATION_COMMAND_BLOCK_RE = re.compile(
    r"```(?:bash|sh)?\n(?:(?!```).)*(?:python scripts/|python -m|"
    r"git diff --check|git diff --exit-code|scripts/ci_gate.py|"
    r"scripts/release_check.py)",
    re.S,
)
NON_AGENTS_COMMAND_BLOCK_ALLOWED_PREFIXES = (
    "docs/decisions/AOA-SK-D-",
    "mechanics/agon/legacy/",
    "mechanics/boundary-bridge/legacy/",
    "mechanics/growth-cycle/legacy/",
    "mechanics/release-support/legacy/",
)
NON_AGENTS_COMMAND_BLOCK_ALLOWED_FILES = {
    "mechanics/audit/docs/SKILLS_REF_VALIDATION.md",
    "mechanics/method-growth/docs/PROMOTION_PRESSURE.md",
    "mechanics/release-support/docs/CODEX_CONFIG_SNIPPETS.md",
    "mechanics/release-support/docs/INSTALL_AND_PROFILES.md",
    "mechanics/release-support/docs/LOCAL_ADAPTER_CONTRACT.md",
    "mechanics/release-support/docs/RUNTIME_GOVERNANCE_LAYER.md",
}
THIN_VALIDATION_CLI_ADAPTERS = (
    "scripts/validation/validate_agent_skills.py",
    "scripts/validation/validate_tiny_router_inputs.py",
    "scripts/validation/validate_support_resources.py",
    "scripts/validation/lint_trigger_evals.py",
    "scripts/validation/lint_description_trigger_evals.py",
    "scripts/validation/lint_pack_profiles.py",
    "scripts/validation/lint_support_resources.py",
)
OWNER_MODULE_LIMITS = {
    "scripts/validation/validators/agent_skills_project_surface.py": 180,
    "scripts/validation/validators/tiny_router_surface.py": 180,
    "scripts/validation/validators/support_resource_surface.py": 180,
    "scripts/validation/validators/trigger_eval_surface.py": 180,
    "scripts/validation/validators/pack_profile_surface.py": 120,
}


def load_inventory() -> dict:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def python_script_paths_from(commands: tuple[tuple[str, ...], ...]) -> set[str]:
    paths: set[str] = set()
    for command in commands:
        if len(command) >= 2 and command[0] == "python" and command[1].endswith(".py"):
            paths.add(command[1])
    return paths


def command_sequence_from_manifest(manifest: dict, name: str) -> tuple[tuple[str, ...], ...]:
    return tuple(tuple(command) for command in manifest["command_sequences"][name])


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

    def test_validation_lane_manifest_is_command_authority(self) -> None:
        manifest = json.loads(VALIDATION_LANES_MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual(VALIDATION_LANES_MANIFEST_PATH, validation_lanes.VALIDATION_LANES_PATH)
        self.assertEqual(command_sequence_from_manifest(manifest, "source_fast"), validation_lanes.SOURCE_FAST_COMMAND_SEQUENCE)
        self.assertEqual(
            command_sequence_from_manifest(manifest, "export_generated_check"),
            validation_lanes.EXPORT_GENERATED_CHECK_COMMAND_SEQUENCE,
        )
        self.assertEqual(
            command_sequence_from_manifest(manifest, "runtime_generated_check"),
            validation_lanes.RUNTIME_GENERATED_CHECK_COMMAND_SEQUENCE,
        )
        self.assertEqual(command_sequence_from_manifest(manifest, "export_full"), validation_lanes.EXPORT_FULL_COMMAND_SEQUENCE)
        self.assertEqual(command_sequence_from_manifest(manifest, "release_check"), validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE)
        self.assertEqual(tuple(manifest["drift_paths"]["export_generated"]), validation_lanes.EXPORT_GENERATED_DRIFT_PATHS)
        self.assertEqual(tuple(manifest["drift_paths"]["runtime_generated"]), validation_lanes.RUNTIME_GENERATED_DRIFT_PATHS)
        self.assertEqual(tuple(manifest["single_commands"]["packaging_smoke"]), validation_lanes.PACKAGING_SMOKE_COMMAND)

        loader_text = (SCRIPTS_DIR / "validation_lanes.py").read_text(encoding="utf-8")
        self.assertNotIn("scripts/export/build_agent_skills.py", loader_text)
        self.assertNotIn("generated/runtime_discovery_index.json", loader_text)

    def test_validation_lanes_root_ingress_is_safe_manifest_cli(self) -> None:
        help_result = subprocess.run(
            (sys.executable, "scripts/validation_lanes.py", "--help"),
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, help_result.returncode, help_result.stderr)
        self.assertIn("usage:", help_result.stdout)
        self.assertIn("config/validation_lanes.json", help_result.stdout)

        inspect_result = subprocess.run(
            (sys.executable, "scripts/validation_lanes.py"),
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, inspect_result.returncode, inspect_result.stderr)
        self.assertIn("validation lanes: config/validation_lanes.json", inspect_result.stdout)
        self.assertIn("- source_fast:", inspect_result.stdout)

    def test_all_agents_cards_name_validation_command_storage_balance(self) -> None:
        missing = []
        for path in sorted(REPO_ROOT.rglob("AGENTS.md")):
            text = path.read_text(encoding="utf-8")
            if "## Validation" in text and AGENTS_VALIDATION_PREAMBLE not in text:
                missing.append(path.relative_to(REPO_ROOT).as_posix())
        self.assertEqual([], missing)

    def test_github_workflows_do_not_inline_validation_lane_commands(self) -> None:
        workflow_dir = REPO_ROOT / ".github" / "workflows"
        forbidden = re.compile(
            r"python scripts/(?:validate_|lint_|build_|run_skills_ref_validation|"
            r"smoke_skill_pack|generate_decision)"
        )
        allowed = re.compile(r"python scripts/(?:ci_gate|release_check|report_technique_drift)\.py")
        offenders: list[str] = []
        for path in sorted(workflow_dir.glob("*.yml")):
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if forbidden.search(line) and not allowed.search(line):
                    rel = path.relative_to(REPO_ROOT).as_posix()
                    offenders.append(f"{rel}:{lineno}: {line.strip()}")
        self.assertEqual([], offenders)

    def test_active_non_agents_docs_do_not_store_validation_command_blocks(self) -> None:
        offenders: list[str] = []
        for path in sorted(REPO_ROOT.rglob("*.md")):
            rel = path.relative_to(REPO_ROOT).as_posix()
            if rel == "AGENTS.md" or rel.endswith("/AGENTS.md"):
                continue
            if rel in NON_AGENTS_COMMAND_BLOCK_ALLOWED_FILES:
                continue
            if any(rel.startswith(prefix) for prefix in NON_AGENTS_COMMAND_BLOCK_ALLOWED_PREFIXES):
                continue
            text = path.read_text(encoding="utf-8")
            if VALIDATION_COMMAND_BLOCK_RE.search(text):
                offenders.append(rel)

        self.assertEqual([], offenders)

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
            for path in SCRIPTS_DIR.rglob(pattern)
            if path.parent != SCRIPTS_DIR and "/__pycache__/" not in path.as_posix()
        }
        discovered.update(
            {
                "scripts/lanes/ci_gate.py",
                "scripts/lanes/release_check.py",
                "scripts/bundles/smoke_skill_pack_handoff.py",
                "scripts/bundles/verify_skill_pack.py",
                ".agents/spark/scripts/validate_spark_lane.py",
            }
        )
        discovered -= {
            "scripts/validators/__init__.py",
            "scripts/validation/validators/__init__.py",
        }

        missing = sorted(discovered - inventory_paths)
        self.assertEqual([], missing)

    def test_validation_cli_adapters_stay_thin(self) -> None:
        for rel_path in THIN_VALIDATION_CLI_ADAPTERS:
            with self.subTest(path=rel_path):
                text = (REPO_ROOT / rel_path).read_text(encoding="utf-8")
                self.assertLessEqual(len(text.splitlines()), 40)
                self.assertIn("from validation.validators.", text)
                self.assertIn("raise SystemExit(main())", text)

    def test_retired_semantic_agents_validator_stays_folded(self) -> None:
        self.assertFalse((SCRIPTS_DIR / "validate_semantic_agents.py").exists())
        contract = json.loads(
            (SCRIPTS_DIR / "validation" / "validators" / "nested_agents_contract.json").read_text(
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
