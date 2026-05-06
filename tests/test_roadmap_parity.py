from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


class RoadmapParityTestCase(unittest.TestCase):
    def test_mechanics_roadmap_routes_to_package_roadmaps(self) -> None:
        readme = read("README.md")
        changelog = read("CHANGELOG.md")
        router = read("mechanics/ROADMAP.md")

        self.assertIn("v0.3.3", readme)
        self.assertIn("[0.3.3]", changelog)
        self.assertIn("This file routes future skill-layer pressure", router)
        self.assertIn("nearest package `ROADMAP.md` owns", router)
        self.assertIn("mechanics/README.md", router)
        self.assertIn("mechanics/OWNER_REQUEST_RECEIPTS.md", router)
        self.assertNotIn("## v0.7 packaging and distribution", router)

    def test_release_and_governance_pressure_is_distributed(self) -> None:
        audit = read("mechanics/audit/ROADMAP.md")
        method_growth = read("mechanics/method-growth/ROADMAP.md")
        boundary_bridge = read("mechanics/boundary-bridge/ROADMAP.md")
        release_support = read("mechanics/release-support/ROADMAP.md")

        for token in (
            "v0.3.x",
            "v0.4",
            "generated/governance_backlog.md",
            "generated/skill_evaluation_matrix.md",
            "generated/overlay_readiness.md",
        ):
            self.assertIn(token, audit)

        for token in (
            "v0.5",
            "mechanics/OWNER_REQUEST_RECEIPTS.md",
            "generated/project_core_outer_ring_readiness.min.json",
            "default-reference rationale",
        ):
            self.assertIn(token, method_growth)

        for token in (
            "v0.6",
            "mechanics/boundary-bridge/docs/CODEX_SKILL_MCP_WIRING.md",
            "generated/overlay_readiness.md",
            "downstream repos consume new meaning from `main`",
        ):
            self.assertIn(token, boundary_bridge)

        for token in (
            "v0.7",
            "generated/runtime_discovery_index.json",
            "generated/skill_bundle_index.md",
            "generated/skill_graph.md",
            "generated/release_manifest.json",
            "mechanics/release-support/docs/LOCAL_ADAPTER_CONTRACT.md",
            "mechanics/release-support/docs/SESSION_COMPACTION.md",
        ):
            self.assertIn(token, release_support)

    def test_growth_checkpoint_and_quest_surfaces_keep_owner_routes(self) -> None:
        runtime_index = json.loads(read("generated/runtime_discovery_index.json"))
        checkpoint = read("mechanics/checkpoint/ROADMAP.md")
        growth_cycle = read("mechanics/growth-cycle/ROADMAP.md")
        questbook = read("mechanics/questbook/ROADMAP.md")
        root_questbook = read("QUESTBOOK.md")

        runtime_skill_names = {skill["name"] for skill in runtime_index["skills"]}
        for skill_name in (
            "aoa-checkpoint-closeout-bridge",
            "aoa-commit-growth-seam",
            "aoa-automation-opportunity-scan",
            "aoa-session-donor-harvest",
        ):
            self.assertIn(skill_name, runtime_skill_names)

        self.assertIn("aoa-checkpoint-closeout-bridge", checkpoint)
        self.assertIn("aoa-commit-growth-seam", checkpoint)
        self.assertIn("aoa-automation-opportunity-scan", growth_cycle)
        self.assertIn("aoa-session-donor-harvest", growth_cycle)
        self.assertIn("generated/quest_catalog.min.json", questbook)
        self.assertIn("generated/quest_dispatch.min.json", questbook)
        self.assertIn("promote to memo surface", questbook)
        self.assertIn("AOA-SK-Q-0008", root_questbook)

    def test_agon_companion_bridge_surfaces_remain_routable(self) -> None:
        agon = read("mechanics/agon/ROADMAP.md")
        readme = read("README.md")

        for relative_path in (
            "mechanics/README.md",
            "mechanics/agon/README.md",
            "mechanics/agon/parts/workflow-candidate-bridge/README.md",
            "mechanics/agon/parts/candidate-validation-gate/README.md",
            "generated/agon_skill_binding_candidates.min.json",
            "mechanics/agon/parts/workflow-candidate-bridge/config/agon_skill_binding_candidates.seed.json",
            "mechanics/agon/parts/workflow-candidate-bridge/scripts/build_agon_skill_binding_candidates.py",
            "mechanics/agon/parts/workflow-candidate-bridge/scripts/validate_agon_skill_binding_candidates.py",
            "mechanics/agon/parts/workflow-candidate-bridge/tests/test_agon_skill_binding_candidates.py",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())

        self.assertIn("generated/agon_skill_binding_candidates.min.json", agon)
        self.assertIn("requested_not_landed", agon)
        self.assertIn(
            "mechanics/agon/parts/workflow-candidate-bridge/README.md",
            readme,
        )


if __name__ == "__main__":
    unittest.main()
