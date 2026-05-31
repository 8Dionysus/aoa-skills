from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import decision_indexes


class DecisionIndexTests(unittest.TestCase):
    def test_current_decision_indexes_are_fresh(self) -> None:
        issues = decision_indexes.validate_decision_index_surfaces(REPO_ROOT)
        self.assertEqual([], issues)

    def test_canonical_filename_must_match_decision_id(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            shutil.copytree(REPO_ROOT / "docs" / "decisions", temp_root / "docs" / "decisions")
            wrong_path = (
                temp_root
                / "docs"
                / "decisions"
                / "AOA-SK-D-9999-canonical-decision-ids-and-indexes.md"
            )
            source_path = (
                temp_root
                / "docs"
                / "decisions"
                / "AOA-SK-D-0027-canonical-decision-ids-and-indexes.md"
            )
            source_path.rename(wrong_path)

            records, issues = decision_indexes.collect_decision_records(temp_root)

        self.assertTrue(records)
        self.assertIn(
            (
                "docs/decisions/AOA-SK-D-9999-canonical-decision-ids-and-indexes.md",
                "decision path canonical ID must match the note Decision ID",
            ),
            issues,
        )

    def test_generated_index_contract_names_expected_outputs(self) -> None:
        contract, issues = decision_indexes.load_index_contract(REPO_ROOT)

        self.assertEqual([], issues)
        self.assertIsNotNone(contract)
        assert contract is not None
        self.assertEqual("AOA-SK-D", contract["decision_id_prefix"])
        self.assertEqual(
            [path.as_posix() for path in decision_indexes.GENERATED_INDEX_PATHS],
            contract["generated_indexes"],
        )


if __name__ == "__main__":
    unittest.main()
