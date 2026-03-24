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

import skill_bundle_surface


class SkillBundleSurfaceTests(unittest.TestCase):
    def make_repo_root(self) -> Path:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-bundle-hash-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        return repo_root

    def test_hash_files_normalizes_line_endings(self) -> None:
        repo_root = self.make_repo_root()
        skill_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_path.parent.mkdir(parents=True, exist_ok=True)

        skill_path.write_text("# aoa-test-skill\n\nLine one.\nLine two.\n", encoding="utf-8", newline="\n")
        lf_hash = skill_bundle_surface.hash_files(repo_root, [skill_path])

        skill_path.write_bytes(b"# aoa-test-skill\r\n\r\nLine one.\r\nLine two.\r\n")
        crlf_hash = skill_bundle_surface.hash_files(repo_root, [skill_path])

        self.assertEqual(lf_hash, crlf_hash)


if __name__ == "__main__":
    unittest.main()
