from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RoadmapParityTestCase(unittest.TestCase):
    def test_roadmap_matches_current_v0_3_release_surfaces(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        runtime_index = json.loads(
            (REPO_ROOT / "generated" / "runtime_discovery_index.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertIn("v0.3.3", readme)
        self.assertIn("[0.3.3]", changelog)
        self.assertIn("v0.3.x", roadmap)
        self.assertIn("v0.3.3", roadmap)

        runtime_skill_names = {skill["name"] for skill in runtime_index["skills"]}
        for skill_name in (
            "aoa-checkpoint-closeout-bridge",
            "aoa-commit-growth-seam",
            "aoa-automation-opportunity-scan",
            "aoa-session-donor-harvest",
        ):
            self.assertIn(skill_name, runtime_skill_names)
            self.assertIn(skill_name, roadmap)

        for relative_path in (
            "generated/runtime_discovery_index.json",
            "mechanics/OWNER_REQUEST_RECEIPTS.md",
            "mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md",
            "mechanics/method-growth/docs/OWNER_STATUS_SURFACES.md",
            "mechanics/method-growth/docs/GOVERNED_FOLLOWTHROUGH.md",
            "generated/quest_catalog.min.json",
            "generated/quest_dispatch.min.json",
            "docs/CODEX_SKILL_MCP_WIRING.md",
            "docs/LOCAL_ADAPTER_CONTRACT.md",
            "docs/SESSION_COMPACTION.md",
            "generated/governance_backlog.md",
            "generated/overlay_readiness.md",
            "generated/skill_bundle_index.md",
            "generated/skill_graph.md",
            "generated/release_manifest.json",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())
            self.assertIn(relative_path, roadmap)

        self.assertIn("checkpoint follow-through", changelog)
        self.assertIn("candidate lineage", changelog)
        self.assertIn("local Codex/MCP disclosure", changelog)
        self.assertIn("roadmap drift", roadmap)

    def test_roadmap_names_agon_companion_bridge_surfaces(self) -> None:
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        for relative_path in (
            "mechanics/README.md",
            "mechanics/agon/README.md",
            "mechanics/agon/parts/workflow-candidate-bridge/README.md",
            "mechanics/agon/parts/candidate-validation-gate/README.md",
            "generated/agon_skill_binding_candidates.min.json",
            "config/agon_skill_binding_candidates.seed.json",
            "scripts/build_agon_skill_binding_candidates.py",
            "scripts/validate_agon_skill_binding_candidates.py",
            "tests/test_agon_skill_binding_candidates.py",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())

        self.assertIn("mechanics/agon/parts/workflow-candidate-bridge/README.md", roadmap)
        self.assertIn("generated/agon_skill_binding_candidates.min.json", roadmap)
        self.assertIn("requested_not_landed", roadmap)
        self.assertIn("mechanics/agon/parts/workflow-candidate-bridge/README.md", readme)


if __name__ == "__main__":
    unittest.main()
