from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


class DownstreamFeedContractsTests(unittest.TestCase):
    def test_expected_runtime_and_router_feeds_exist(self) -> None:
        for relative_path in (
            "generated/runtime_discovery_index.json",
            "generated/runtime_disclosure_index.json",
            "generated/runtime_activation_aliases.json",
            "generated/runtime_tool_schemas.json",
            "generated/runtime_session_contract.json",
            "generated/skill_capsules.json",
            "generated/skill_sections.full.json",
            "generated/tiny_router_skill_signals.json",
            "generated/tiny_router_candidate_bands.json",
            "generated/tiny_router_capsules.min.json",
        ):
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

    def test_runtime_and_router_feeds_share_the_same_skill_names(self) -> None:
        discovery = load_json("generated/runtime_discovery_index.json")
        disclosure = load_json("generated/runtime_disclosure_index.json")
        capsules = load_json("generated/skill_capsules.json")
        sections = load_json("generated/skill_sections.full.json")
        tiny_signals = load_json("generated/tiny_router_skill_signals.json")
        tiny_capsules = load_json("generated/tiny_router_capsules.min.json")
        aliases = load_json("generated/runtime_activation_aliases.json")

        expected_names = [entry["name"] for entry in discovery["skills"]]
        self.assertEqual(discovery["schema_version"], 1)
        self.assertEqual(disclosure["schema_version"], 1)
        self.assertEqual(capsules["capsule_version"], 1)
        self.assertEqual(sections["section_version"], 1)
        self.assertEqual(tiny_signals["schema_version"], 1)
        self.assertEqual(tiny_capsules["schema_version"], 1)
        self.assertEqual(aliases["schema_version"], 1)

        self.assertEqual(expected_names, [entry["name"] for entry in disclosure["skills"]])
        self.assertEqual(expected_names, [entry["name"] for entry in capsules["skills"]])
        self.assertEqual(expected_names, [entry["name"] for entry in sections["skills"]])
        self.assertEqual(expected_names, [entry["name"] for entry in tiny_signals["skills"]])
        self.assertEqual(expected_names, [entry["name"] for entry in tiny_capsules["skills"]])
        self.assertEqual(expected_names, [entry["name"] for entry in aliases["aliases"]])

    def test_runtime_support_surfaces_publish_strict_expected_shapes(self) -> None:
        tool_schemas = load_json("generated/runtime_tool_schemas.json")
        session_contract = load_json("generated/runtime_session_contract.json")

        self.assertEqual(tool_schemas["schema_version"], 1)
        self.assertEqual(
            [entry["name"] for entry in tool_schemas["tools"]],
            [
                "discover_skills",
                "disclose_skill",
                "activate_skill",
                "skill_session_status",
                "deactivate_skill",
                "compact_skill_session",
            ],
        )
        self.assertEqual(session_contract["schema_version"], 1)
        self.assertEqual(
            sorted(session_contract["state_schema"].keys()),
            ["active_skill_record", "required"],
        )
        self.assertIn("active_skills", session_contract["state_schema"]["required"])
        self.assertIn("activation_log", session_contract["state_schema"]["required"])
        self.assertIn(
            "rehydration_hint",
            session_contract["state_schema"]["active_skill_record"]["required"],
        )

    def test_tiny_router_bands_reference_known_skills_only(self) -> None:
        tiny_signals = load_json("generated/tiny_router_skill_signals.json")
        tiny_bands = load_json("generated/tiny_router_candidate_bands.json")

        known_skills = {entry["name"] for entry in tiny_signals["skills"]}

        self.assertEqual(tiny_bands["schema_version"], 1)
        self.assertEqual(tiny_bands["band_count"], len(tiny_bands["bands"]))

        for band in tiny_bands["bands"]:
            for key in ("skills", "manual_only_skills", "overlay_skills"):
                with self.subTest(band=band["id"], key=key):
                    self.assertTrue(set(band[key]).issubset(known_skills))


if __name__ == "__main__":
    unittest.main()
