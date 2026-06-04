from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
import contextlib
import io
from unittest import mock
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from decisions import decision_indexes, generate_decision_indexes


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

    def test_generate_check_uses_full_contract_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            shutil.copytree(REPO_ROOT / "docs" / "decisions", temp_root / "docs" / "decisions")
            contract_path = temp_root / "docs" / "decisions" / "indexes" / "index_contract.yaml"
            contract_text = contract_path.read_text(encoding="utf-8")
            contract_path.write_text(
                contract_text.replace("decision_id_prefix: AOA-SK-D", "decision_id_prefix: AOA-BAD-D"),
                encoding="utf-8",
            )

            stdout = io.StringIO()
            with (
                mock.patch.object(
                    sys,
                    "argv",
                    [
                        "generate_decision_indexes.py",
                        "--check",
                        "--repo-root",
                        temp_root.as_posix(),
                    ],
                ),
                contextlib.redirect_stdout(stdout),
            ):
                exit_code = generate_decision_indexes.main()

        self.assertEqual(1, exit_code)
        self.assertIn("decision_id_prefix must be AOA-SK-D", stdout.getvalue())

    def test_index_contract_validation_covers_parser_contract_fields(self) -> None:
        contract, issues = decision_indexes.load_index_contract(REPO_ROOT)
        self.assertEqual([], issues)
        assert contract is not None

        drifted = dict(contract)
        drifted["path_policy"] = "date_prefixed_filename"
        drifted["source_glob"] = "docs/decisions/*.md"
        drifted["required_metadata"] = ["Original date"]

        contract_issues = decision_indexes.validate_index_contract_payload(drifted)

        self.assertIn(
            (
                "docs/decisions/indexes/index_contract.yaml",
                "path_policy must be full_canonical_id_filename",
            ),
            contract_issues,
        )
        self.assertIn(
            (
                "docs/decisions/indexes/index_contract.yaml",
                "source_glob must be docs/decisions/AOA-SK-D-*.md",
            ),
            contract_issues,
        )
        self.assertIn(
            (
                "docs/decisions/indexes/index_contract.yaml",
                "required_metadata must match the parsed decision metadata fields",
            ),
            contract_issues,
        )


if __name__ == "__main__":
    unittest.main()
