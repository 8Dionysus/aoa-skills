from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "generated" / "description_trigger_eval_manifest.json"
CATALOG_PATH = REPO_ROOT / "generated" / "skill_catalog.min.json"
PACKET_PATH = REPO_ROOT / (
    "stats/packets/description-trigger-contract-coverage-ratio.reference.json"
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def coverage_census() -> tuple[int, int, int]:
    manifest = load_json(MANIFEST_PATH)
    records = manifest["skills"]
    catalog_names = {entry["name"] for entry in load_json(CATALOG_PATH)["skills"]}
    record_names = {entry["name"] for entry in records}

    assert manifest["skill_count"] == len(records)
    assert catalog_names == record_names, "stats population must match the skill catalog"
    covered = sum(record["coverage_ok"] is True for record in records)
    return covered, len(records), manifest["total_cases"]


def assert_packet_matches_owner_coverage(packet: dict) -> None:
    covered, population_size, _ = coverage_census()

    assert population_size > 0, "owner description-trigger population must not be empty"
    assert packet["population"]["size"] == population_size
    assert packet["sample"]["size"] == population_size
    assert packet["value"]["numerator"] == covered, (
        "packet numerator must match coverage_ok skill records"
    )
    assert packet["value"]["denominator"] == population_size, (
        "packet denominator must count skills, not trigger cases"
    )
    assert packet["value"]["number"] == covered / population_size
    assert packet["progress"] == {
        "state": "terminal",
        "completed": population_size,
        "total": population_size,
    }


class LocalStatsPortTests(unittest.TestCase):
    def test_reference_ratio_matches_current_owner_trigger_manifest(self) -> None:
        assert_packet_matches_owner_coverage(load_json(PACKET_PATH))

    def test_false_coverage_numerator_is_rejected(self) -> None:
        false_packet = deepcopy(load_json(PACKET_PATH))
        covered, population_size, _ = coverage_census()
        false_numerator = (covered + 1) % (population_size + 1)
        false_packet["value"]["numerator"] = false_numerator
        false_packet["value"]["number"] = false_numerator / population_size

        with self.assertRaisesRegex(
            AssertionError,
            "packet numerator must match coverage_ok skill records",
        ):
            assert_packet_matches_owner_coverage(false_packet)

    def test_trigger_case_count_denominator_is_rejected(self) -> None:
        false_packet = deepcopy(load_json(PACKET_PATH))
        covered, _, case_count = coverage_census()
        false_packet["value"]["denominator"] = case_count
        false_packet["value"]["number"] = covered / case_count

        with self.assertRaisesRegex(
            AssertionError,
            "packet denominator must count skills, not trigger cases",
        ):
            assert_packet_matches_owner_coverage(false_packet)


if __name__ == "__main__":
    unittest.main()
