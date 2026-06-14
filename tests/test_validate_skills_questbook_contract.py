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

    def test_questbook_surface_reports_missing_index(self) -> None:
        repo_root = self.make_repo()
        (repo_root / "QUESTBOOK.md").unlink()

        issues = questbook_surface.validate_questbook_surface(repo_root)

        self.assertIn(
            ("QUESTBOOK.md", "file is missing"),
            {(issue.location, issue.message) for issue in issues},
        )

    def test_questbook_surface_reports_duplicate_quest_ids(self) -> None:
        repo_root = self.make_repo()
        quest_id = questbook_surface.FOUNDATION_QUEST_IDS[0]
        source = quest_fixture_path(repo_root, quest_id)
        duplicate = repo_root / "quests" / "duplicate-fixture" / source.name
        write_text(duplicate, source.read_text(encoding="utf-8"))

        issues = questbook_surface.validate_questbook_surface(repo_root)

        self.assertTrue(
            any(
                issue.location == f"quests/**/{quest_id}.yaml"
                and "duplicate quest id files are not allowed" in issue.message
                for issue in issues
            ),
            [issue.message for issue in issues],
        )

    def test_questbook_surface_reports_quest_schema_failures(self) -> None:
        repo_root = self.make_repo()
        quest_id = questbook_surface.FOUNDATION_QUEST_IDS[0]
        quest_path = quest_fixture_path(repo_root, quest_id)
        payload = yaml.safe_load(quest_path.read_text(encoding="utf-8"))
        payload.pop("activation")
        quest_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

        issues = questbook_surface.validate_questbook_surface(repo_root)

        self.assertTrue(
            any(
                issue.location == quest_path.relative_to(repo_root).as_posix()
                and "schema violation" in issue.message
                for issue in issues
            ),
            [issue.message for issue in issues],
        )

    def test_questbook_surface_reports_stale_live_catalog(self) -> None:
        repo_root = self.make_repo()
        catalog_path = repo_root / "generated" / "quest_catalog.min.json"
        payload = json.loads(catalog_path.read_text(encoding="utf-8"))
        payload[0]["title"] = "Stale generated title"
        catalog_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        issues = questbook_surface.validate_questbook_surface(repo_root)

        self.assertIn(
            (
                "generated/quest_catalog.min.json",
                "live catalog must stay aligned with quests/**/AOA-SK-Q-*.yaml",
            ),
            {(issue.location, issue.message) for issue in issues},
        )

    def test_questbook_surface_reports_stale_live_dispatch(self) -> None:
        repo_root = self.make_repo()
        dispatch_path = repo_root / "generated" / "quest_dispatch.min.json"
        payload = json.loads(dispatch_path.read_text(encoding="utf-8"))
        payload[0]["requires_artifacts"].append("stale_extra_artifact")
        dispatch_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        issues = questbook_surface.validate_questbook_surface(repo_root)

        self.assertTrue(
            any(
                issue.location == "generated/quest_dispatch.min.json"
                and issue.message.startswith("dispatch entry '")
                and "must stay aligned with quests/**/AOA-SK-Q-*.yaml"
                in issue.message
                for issue in issues
            ),
            [issue.message for issue in issues],
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
