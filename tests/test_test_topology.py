from __future__ import annotations

import configparser
import json
import re
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validation_lanes


TOPOLOGY_PATH = REPO_ROOT / "docs" / "testing" / "TEST_TOPOLOGY.md"
INVENTORY_PATH = REPO_ROOT / "docs" / "testing" / "test_inventory.json"
PYTEST_INI_PATH = REPO_ROOT / "pytest.ini"
REQUIRED_MARKERS = {
    "source",
    "generated",
    "export",
    "router",
    "release",
    "advisory",
    "live",
    "slow",
}
REQUIRED_INVENTORY_FIELDS = {
    "path",
    "family",
    "protects",
    "owner_surface",
    "lane",
    "mode",
    "runtime_cost",
    "focused_target",
    "failure_route",
}


def load_inventory() -> dict:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def discovered_test_files() -> set[str]:
    paths = set()
    paths.update(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "tests").glob("test*.py")
    )
    paths.update(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / ".agents" / "spark" / "tests").glob("test*.py")
    )
    paths.update(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "mechanics").glob("**/tests/test*.py")
    )
    return paths


class TestTopologyTests(unittest.TestCase):
    def test_topology_doc_names_agentic_route_shape(self) -> None:
        text = TOPOLOGY_PATH.read_text(encoding="utf-8")
        for required in (
            "family -> protects -> owner source -> lane ->",
            "`source/skill-contract`",
            "`router/*`",
            "`export/*`",
            "`advisory/*`",
            "semantic/model evals belong in the eval organ",
        ):
            self.assertIn(required, text)

    def test_test_inventory_covers_all_test_files(self) -> None:
        inventory = load_inventory()
        required_fields = set(inventory["required_fields"])
        self.assertEqual(REQUIRED_INVENTORY_FIELDS, required_fields)
        inventory_paths = [entry["path"] for entry in inventory["entries"]]
        self.assertEqual(len(inventory_paths), len(set(inventory_paths)))
        self.assertEqual(discovered_test_files(), set(inventory_paths))

        for entry in inventory["entries"]:
            with self.subTest(path=entry["path"]):
                self.assertTrue(required_fields.issubset(entry))
                self.assertTrue((REPO_ROOT / entry["path"]).is_file())
                self.assertIn(
                    entry["lane"],
                    {
                        "source",
                        "generated",
                        "export",
                        "router",
                        "release",
                        "advisory",
                        "live",
                    },
                )
                self.assertIn(
                    entry["mode"],
                    {
                        "blocking",
                        "blocking-in-tests",
                        "advisory",
                        "soft-live",
                        "soft-external",
                    },
                )
                self.assertIn(entry["runtime_cost"], {"fast", "medium", "slow"})
                self.assertFalse(
                    re.match(r"^(python|git|bash|sh)\b", entry["focused_target"]),
                    msg=f"{entry['path']} stores a command instead of a target",
                )

    def test_pytest_markers_cover_test_lanes(self) -> None:
        parser = configparser.ConfigParser()
        parser.read(PYTEST_INI_PATH)
        markers = {
            marker.split(":", 1)[0].strip()
            for marker in parser.get("pytest", "markers").splitlines()
            if marker.strip()
        }
        self.assertTrue(REQUIRED_MARKERS.issubset(markers))

    def test_release_lane_uses_pytest_for_tests_directory(self) -> None:
        self.assertIn(
            ("python", "-m", "pytest", "-q", "tests"),
            validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE,
        )
        self.assertNotIn(
            ("python", "-m", "unittest", "discover", "-s", "tests"),
            validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE,
        )

    def test_tests_do_not_replay_release_validator_sequence(self) -> None:
        offenders: list[str] = []
        release_validator_names = {
            "scripts/validate_agent_skills.py",
            "scripts/validate_support_resources.py",
            "scripts/validate_tiny_router_inputs.py",
            "scripts/lint_trigger_evals.py",
            "scripts/lint_description_trigger_evals.py",
            "scripts/lint_pack_profiles.py",
            "scripts/lint_support_resources.py",
            "scripts/run_skills_ref_validation.py",
        }
        allowed = {
            "tests/test_agentic_fault_boundaries.py",
            "tests/test_release_check.py",
            "tests/test_test_topology.py",
            "tests/test_validator_topology.py",
            "tests/test_skills_ref_validation.py",
        }
        for path in sorted((REPO_ROOT / "tests").glob("test*.py")):
            rel = path.relative_to(REPO_ROOT).as_posix()
            if rel in allowed:
                continue
            text = path.read_text(encoding="utf-8")
            if sum(name in text for name in release_validator_names) >= 3:
                offenders.append(rel)
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
