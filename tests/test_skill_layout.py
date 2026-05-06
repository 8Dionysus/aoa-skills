from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import skill_layout


class SkillLayoutTests(unittest.TestCase):
    def test_discovers_recursive_skill_bundle_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            skill_dir = repo_root / "skills" / "core" / "engineering" / "aoa-test-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("---\nname: aoa-test-skill\n---\n")

            entries = skill_layout.discover_skill_bundle_paths(repo_root)

        self.assertEqual(["aoa-test-skill"], [entry.name for entry in entries])
        self.assertEqual(
            "skills/core/engineering/aoa-test-skill/SKILL.md",
            entries[0].skill_md_path.relative_to(repo_root).as_posix(),
        )

    def test_rejects_duplicate_bundle_names_across_lanes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            first = repo_root / "skills" / "core" / "engineering" / "aoa-test-skill"
            second = repo_root / "skills" / "risk" / "aoa-test-skill"
            first.mkdir(parents=True)
            second.mkdir(parents=True)
            (first / "SKILL.md").write_text("---\nname: aoa-test-skill\n---\n")
            (second / "SKILL.md").write_text("---\nname: aoa-test-skill\n---\n")

            with self.assertRaisesRegex(ValueError, "duplicate skill bundle"):
                skill_layout.discover_skill_bundle_paths(repo_root)


if __name__ == "__main__":
    unittest.main()
