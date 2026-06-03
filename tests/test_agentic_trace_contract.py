from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from skill_model import skill_layout


GOLDEN_PACK_PATH = REPO_ROOT / "tests" / "fixtures" / "golden_route_pack.yaml"


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def normalized(text: str) -> str:
    return " ".join(text.lower().split())


class AgenticTraceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pack = load_yaml(GOLDEN_PACK_PATH)
        cls.fixtures = load_yaml(REPO_ROOT / cls.pack["source_fixtures"])
        cls.snapshot_by_id = {
            case["case_id"]: case for case in cls.fixtures["snapshot_cases"]
        }
        cls.adjacency_by_id = {
            case["case_id"]: case for case in cls.fixtures["adjacency_cases"]
        }
        cls.tiny_router = {
            entry["name"]: entry
            for entry in json.loads(
                (REPO_ROOT / "generated" / "tiny_router_skill_signals.json").read_text(
                    encoding="utf-8"
                )
            )["skills"]
        }
        cls.activation_policy = json.loads(
            (REPO_ROOT / "config" / "skill_policy_matrix.json").read_text(
                encoding="utf-8"
            )
        )["skills"]

    def test_golden_pack_covers_every_skill_with_positive_and_negative_snapshot(
        self,
    ) -> None:
        counts: dict[str, dict[str, int]] = {}
        for case in self.fixtures["snapshot_cases"]:
            counts.setdefault(case["skill"], {"use": 0, "do_not_use": 0})[
                case["expected"]
            ] += 1

        for skill_name in skill_layout.discover_skill_names(REPO_ROOT):
            with self.subTest(skill=skill_name):
                self.assertGreaterEqual(counts.get(skill_name, {}).get("use", 0), 1)
                self.assertGreaterEqual(
                    counts.get(skill_name, {}).get("do_not_use", 0),
                    1,
                )

    def test_high_risk_adjacency_cases_are_present_and_snapshot_backed(self) -> None:
        for case_id in self.pack["coverage"]["high_risk_adjacency_cases"]:
            with self.subTest(case=case_id):
                case = self.adjacency_by_id[case_id]
                self.assertEqual("use", case["expected"])
                self.assertTrue((REPO_ROOT / case["snapshot_path"]).is_file())
                self.assertNotEqual(case["skill"], case["adjacent_skill"])

    def test_trace_contracts_match_snapshot_source_and_router_posture(self) -> None:
        for contract in self.pack["trace_contracts"]:
            with self.subTest(contract=contract["id"]):
                case = self.snapshot_by_id[contract["source_case_id"]]
                skill_name = contract["expected_skill"]
                self.assertEqual(skill_name, case["skill"])
                self.assertEqual("use", case["expected"])
                self.assertIn(skill_name, self.tiny_router)
                self.assertEqual(
                    self.tiny_router[skill_name]["implicit_activation_policy"],
                    self.activation_policy[skill_name]["implicit_activation_policy"],
                )

                snapshot_text = normalized(
                    (REPO_ROOT / case["snapshot_path"]).read_text(encoding="utf-8")
                )
                skill_text = normalized(
                    skill_layout.skill_md_path(REPO_ROOT, skill_name).read_text(
                        encoding="utf-8"
                    )
                )
                combined_text = f"{snapshot_text} {skill_text}"
                for term in contract["expected_terms"]:
                    self.assertIn(term.lower(), combined_text)


if __name__ == "__main__":
    unittest.main()
