from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class CurrentDirectionRoutesTestCase(unittest.TestCase):
    def test_root_entrypoints_route_to_roadmap(self) -> None:
        roadmap_path = REPO_ROOT / "ROADMAP.md"
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")

        self.assertTrue(roadmap_path.is_file())
        self.assertIn("ROADMAP.md", readme)
        self.assertIn("ROADMAP.md", agents)

    def test_agon_wave4_skill_bridge_is_routable(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        docs_readme = (REPO_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        bridge_spec = (REPO_ROOT / "docs" / "BRIDGE_SPEC.md").read_text(encoding="utf-8")

        self.assertIn("docs/AGON_MOVE_SKILL_BRIDGE.md", readme)
        self.assertIn("AGON_MOVE_SKILL_BRIDGE.md", docs_readme)
        self.assertIn("agon_skill_binding_candidates", bridge_spec)


if __name__ == "__main__":
    unittest.main()
