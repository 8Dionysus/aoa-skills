from __future__ import annotations

from tests.support.validate_skills_case import *


class ValidateSkillsQuestbookContractTests(ValidateSkillsCase):
    def test_questbook_contract_manifest_loads_runtime_constants(self) -> None:
        contract = questbook_contract.load_contract()

        self.assertEqual(validate_skills.QUESTBOOK_PATH, contract.questbook_path)
        self.assertEqual(
            validate_skills.QUESTBOOK_REQUIRED_INDEX_TOKENS,
            contract.required_index_tokens,
        )
        self.assertEqual(
            validate_skills.CLOSED_QUEST_STATES, set(contract.closed_states)
        )
        self.assertEqual(
            validate_skills.QUEST_DISPATCH_REQUIRED_FIELDS,
            contract.quest_dispatch_required_fields,
        )

    def test_questbook_contract_rejects_absolute_paths(self) -> None:
        payload = json.loads(
            questbook_contract.DEFAULT_CONTRACT_PATH.read_text(encoding="utf-8")
        )
        payload["surface_paths"]["questbook"] = "/tmp/QUESTBOOK.md"

        with tempfile.TemporaryDirectory() as tmpdir:
            broken_contract = Path(tmpdir) / "questbook_contract.json"
            broken_contract.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "questbook must be repo-relative"):
                questbook_contract.load_contract(broken_contract)

    def test_questbook_surface_validator_stays_phase_split(self) -> None:
        source_lines = (
            Path(questbook_surface.__file__).read_text(encoding="utf-8").splitlines()
        )
        entrypoint = [
            line
            for line in source_lines
            if line.startswith("def validate_questbook_surface")
            or line.startswith("def validate_dispatch_surfaces")
            or line.startswith("def validate_catalog_surfaces")
        ]

        self.assertEqual(
            [
                "def validate_catalog_surfaces(",
                "def validate_dispatch_surfaces(",
                "def validate_questbook_surface(repo_root: Path) -> list[ValidationIssue]:",
            ],
            entrypoint,
        )

    def test_validator_modules_keep_bounded_function_sizes(self) -> None:
        module_limits = (
            (Path(validate_skills.__file__), 180),
            (Path(questbook_surface.__file__), 180),
            (Path(generated_surface.__file__), 230),
            (Path(skill_status_surface.__file__), 230),
        )

        for module_path, line_limit in module_limits:
            syntax_tree = ast.parse(module_path.read_text(encoding="utf-8"))
            for node in ast.walk(syntax_tree):
                if not isinstance(node, ast.FunctionDef):
                    continue
                line_count = node.end_lineno - node.lineno + 1
                self.assertLessEqual(
                    line_count,
                    line_limit,
                    f"{module_path.relative_to(REPO_ROOT)}:{node.lineno} "
                    f"{node.name} has {line_count} lines",
                )


if __name__ == "__main__":
    unittest.main()
