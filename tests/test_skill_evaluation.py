from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_PATH = REPO_ROOT / "tests" / "fixtures" / "skill_evaluation_cases.yaml"
SNAPSHOTS_DIR = REPO_ROOT / "tests" / "fixtures" / "skill_evaluation_snapshots"
RUNTIME_SECTIONS = [
    "Intent",
    "Trigger boundary",
    "Inputs",
    "Outputs",
    "Procedure",
    "Contracts",
    "Risks and anti-patterns",
    "Verification",
]
SNAPSHOT_SECTIONS = [
    "Prompt",
    "Expected selection",
    "Why",
    "Expected object",
    "Boundary notes",
    "Verification hooks",
]
ADJACENCY_EXPECTATIONS = {
    "aoa-bounded-context-map": [
        "aoa-contract-test",
        "aoa-core-logic-boundary",
        "aoa-port-adapter-refactor",
    ],
    "aoa-change-protocol": ["aoa-tdd-slice"],
    "aoa-contract-test": ["aoa-bounded-context-map"],
    "aoa-tdd-slice": ["aoa-change-protocol"],
    "aoa-core-logic-boundary": [
        "aoa-bounded-context-map",
        "aoa-port-adapter-refactor",
    ],
    "aoa-port-adapter-refactor": [
        "aoa-bounded-context-map",
        "aoa-core-logic-boundary",
    ],
    "aoa-approval-gate-check": [
        "aoa-dry-run-first",
        "aoa-safe-infra-change",
        "aoa-sanitized-share",
    ],
    "aoa-dry-run-first": [
        "aoa-approval-gate-check",
        "aoa-safe-infra-change",
        "aoa-sanitized-share",
    ],
    "aoa-safe-infra-change": [
        "aoa-approval-gate-check",
        "aoa-dry-run-first",
        "aoa-sanitized-share",
    ],
    "aoa-local-stack-bringup": [
        "aoa-approval-gate-check",
        "aoa-safe-infra-change",
    ],
    "aoa-sanitized-share": [
        "aoa-approval-gate-check",
        "aoa-dry-run-first",
        "aoa-safe-infra-change",
    ],
    "aoa-source-of-truth-check": ["aoa-adr-write"],
    "aoa-adr-write": ["aoa-source-of-truth-check"],
    "aoa-invariant-coverage-audit": ["aoa-property-invariants"],
    "aoa-property-invariants": ["aoa-invariant-coverage-audit"],
    "atm10-change-protocol": ["atm10-source-of-truth-check"],
    "atm10-source-of-truth-check": ["atm10-change-protocol"],
}


def load_fixtures() -> dict:
    return yaml.safe_load(FIXTURES_PATH.read_text(encoding="utf-8"))


def load_skill_text(skill_name: str) -> str:
    skill_path = REPO_ROOT / "skills" / skill_name / "SKILL.md"
    return skill_path.read_text(encoding="utf-8")


def extract_section(skill_text: str, heading: str) -> str:
    lines = skill_text.splitlines()
    start_index = None
    end_index = len(lines)
    target = f"## {heading}"

    for index, line in enumerate(lines):
        if line.strip() == target:
            start_index = index + 1
            for next_index in range(index + 1, len(lines)):
                if lines[next_index].startswith("## "):
                    end_index = next_index
                    break
            break

    if start_index is None:
        raise AssertionError(f"missing section '{heading}'")
    return "\n".join(lines[start_index:end_index]).strip()


def extract_trigger_bullets(skill_text: str) -> dict[str, list[str]]:
    section_text = extract_section(skill_text, "Trigger boundary")
    groups = {"use": [], "do_not_use": []}
    current_group: str | None = None

    for raw_line in section_text.splitlines():
        line = raw_line.strip()
        if line == "Use this skill when:":
            current_group = "use"
            continue
        if line == "Do not use this skill when:":
            current_group = "do_not_use"
            continue
        if current_group and line.startswith("- "):
            groups[current_group].append(line[2:].strip())

    return groups


class SkillEvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures = load_fixtures()

    def test_selected_skills_are_runtime_self_contained(self) -> None:
        for check in self.fixtures["autonomy_checks"]:
            with self.subTest(skill=check["skill"]):
                skill_text = load_skill_text(check["skill"])
                runtime_text = "\n".join(
                    extract_section(skill_text, section) for section in RUNTIME_SECTIONS
                ).lower()
                for forbidden_term in check["forbidden_runtime_terms"]:
                    self.assertNotIn(forbidden_term.lower(), runtime_text)

    def test_trigger_boundary_fixtures_match_skill_guidance(self) -> None:
        for case in self.fixtures["trigger_cases"]:
            with self.subTest(case=case["case_id"], skill=case["skill"]):
                bullets = extract_trigger_bullets(load_skill_text(case["skill"]))
                target_group = "use" if case["expected"] == "use" else "do_not_use"
                combined = " ".join(bullets[target_group]).lower()
                self.assertTrue(case["prompt"].strip())
                self.assertIn(case["expected"], {"use", "do_not_use"})
                for phrase in case["required_phrases"]:
                    self.assertIn(phrase.lower(), combined)

    def test_snapshot_cases_cover_every_skill_in_both_directions(self) -> None:
        counts: dict[str, dict[str, int]] = {}
        for case in self.fixtures["snapshot_cases"]:
            counts.setdefault(case["skill"], {"use": 0, "do_not_use": 0})[case["expected"]] += 1

        skill_dirs = sorted(path for path in (REPO_ROOT / "skills").iterdir() if path.is_dir())
        self.assertEqual(len(skill_dirs) * 2, len(self.fixtures["snapshot_cases"]))
        for skill_dir in skill_dirs:
            with self.subTest(skill=skill_dir.name):
                self.assertGreaterEqual(counts.get(skill_dir.name, {}).get("use", 0), 1)
                self.assertGreaterEqual(counts.get(skill_dir.name, {}).get("do_not_use", 0), 1)

    def test_snapshot_files_follow_heading_contract_and_exist(self) -> None:
        for case in self.fixtures["snapshot_cases"]:
            with self.subTest(case=case["case_id"], skill=case["skill"]):
                snapshot_path = REPO_ROOT / case["snapshot_path"]
                self.assertTrue(snapshot_path.is_file())
                self.assertEqual(
                    SNAPSHOTS_DIR / case["skill"],
                    snapshot_path.parent,
                )
                snapshot_text = snapshot_path.read_text(encoding="utf-8")
                for heading in SNAPSHOT_SECTIONS:
                    self.assertIn(f"## {heading}", snapshot_text)

                normalized = " ".join(snapshot_text.lower().split())
                for phrase in case["required_output_phrases"]:
                    self.assertIn(" ".join(phrase.lower().split()), normalized)
                for phrase in case["forbidden_output_phrases"]:
                    self.assertNotIn(" ".join(phrase.lower().split()), normalized)

    def test_adjacency_cases_cover_requested_cohorts(self) -> None:
        adjacency_cases = self.fixtures["adjacency_cases"]
        actual_by_skill: dict[str, list[dict]] = {}
        for case in adjacency_cases:
            actual_by_skill.setdefault(case["skill"], []).append(case)

        self.assertEqual(set(ADJACENCY_EXPECTATIONS), set(actual_by_skill))
        self.assertEqual(
            sum(len(adjacent_skills) for adjacent_skills in ADJACENCY_EXPECTATIONS.values()),
            len(adjacency_cases),
        )

        for skill_name, adjacent_skills in ADJACENCY_EXPECTATIONS.items():
            with self.subTest(skill=skill_name):
                skill_cases = actual_by_skill[skill_name]
                self.assertEqual(
                    sorted(adjacent_skills),
                    sorted(case["adjacent_skill"] for case in skill_cases),
                )
                for case in skill_cases:
                    self.assertTrue(case["case_id"])
                    self.assertTrue(case["prompt"].strip())
                    self.assertEqual("use", case["expected"])
                    self.assertTrue(case["snapshot_path"].endswith(".md"))

    def test_adjacency_snapshots_follow_heading_contract_and_exist(self) -> None:
        for case in self.fixtures["adjacency_cases"]:
            with self.subTest(case=case["case_id"], skill=case["skill"]):
                snapshot_path = REPO_ROOT / case["snapshot_path"]
                self.assertTrue(snapshot_path.is_file())
                self.assertEqual(
                    SNAPSHOTS_DIR / case["skill"],
                    snapshot_path.parent,
                )
                snapshot_text = snapshot_path.read_text(encoding="utf-8")
                for heading in SNAPSHOT_SECTIONS:
                    self.assertIn(f"## {heading}", snapshot_text)

                normalized = " ".join(snapshot_text.lower().split())
                for phrase in case["required_output_phrases"]:
                    self.assertIn(" ".join(phrase.lower().split()), normalized)
                for phrase in case["forbidden_output_phrases"]:
                    self.assertNotIn(" ".join(phrase.lower().split()), normalized)
