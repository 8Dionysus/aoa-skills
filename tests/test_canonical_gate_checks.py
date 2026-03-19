from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
FIXTURES_PATH = REPO_ROOT / "tests" / "fixtures" / "skill_evaluation_cases.yaml"


def parse_skill_document(skill_md_path: Path) -> tuple[dict, str]:
    text = skill_md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise AssertionError(f"{skill_md_path} is missing frontmatter")

    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        raise AssertionError(f"{skill_md_path} is missing a closing frontmatter delimiter")

    metadata = yaml.safe_load("\n".join(lines[1:closing_index])) or {}
    if not isinstance(metadata, dict):
        raise AssertionError(f"{skill_md_path} frontmatter must parse to a mapping")

    body = "\n".join(lines[closing_index + 1 :])
    return metadata, body


def load_evaluation_fixtures() -> dict:
    return yaml.safe_load(FIXTURES_PATH.read_text(encoding="utf-8"))


class CanonicalGateChecksTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures = load_evaluation_fixtures()

    def test_canonical_skills_meet_gate_requirements(self) -> None:
        canonical_skills: list[str] = []
        for skill_dir in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
            metadata, _ = parse_skill_document(skill_dir / "SKILL.md")
            if metadata.get("status") == "canonical":
                canonical_skills.append(skill_dir.name)

        if not canonical_skills:
            return

        autonomy_skills = {
            check["skill"] for check in self.fixtures.get("autonomy_checks", [])
        }
        trigger_case_counts: dict[str, dict[str, int]] = {}
        for case in self.fixtures.get("trigger_cases", []):
            skill_name = case["skill"]
            expected = case["expected"]
            counts = trigger_case_counts.setdefault(skill_name, {"use": 0, "do_not_use": 0})
            counts[expected] += 1

        for skill_name in canonical_skills:
            with self.subTest(skill=skill_name):
                skill_dir = SKILLS_DIR / skill_name
                metadata, body = parse_skill_document(skill_dir / "SKILL.md")
                self.assertIn("## Technique traceability", body)
                self.assertNotIn("## Future traceability", body)

                dependencies = metadata.get("technique_dependencies")
                self.assertIsInstance(dependencies, list)
                self.assertTrue(dependencies)
                for dependency in dependencies:
                    self.assertFalse(dependency.startswith("AOA-T-PENDING-"))

                manifest = yaml.safe_load(
                    (skill_dir / "techniques.yaml").read_text(encoding="utf-8")
                )
                techniques = manifest.get("techniques", [])
                self.assertTrue(techniques)
                for technique in techniques:
                    self.assertFalse(technique["id"].startswith("AOA-T-PENDING-"))
                    self.assertNotEqual("TBD", technique["path"])
                    self.assertNotEqual("TBD", technique["source_ref"])

                self.assertIn(skill_name, autonomy_skills)
                self.assertGreaterEqual(trigger_case_counts.get(skill_name, {}).get("use", 0), 1)
                self.assertGreaterEqual(
                    trigger_case_counts.get(skill_name, {}).get("do_not_use", 0), 1
                )
