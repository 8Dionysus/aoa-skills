from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_PATH = REPO_ROOT / "tests" / "fixtures" / "skill_evaluation_cases.yaml"
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
