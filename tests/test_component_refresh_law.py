from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = REPO_ROOT / "examples" / "skills_export_refresh_law.example.json"
ALLOWED_ROUTE_CLASSES = {
    "observe",
    "revalidate",
    "rebuild",
    "reexport",
    "regenerate",
    "reproject",
    "repair",
    "defer",
}


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_pattern(pattern: str) -> list[Path]:
    return list(REPO_ROOT.glob(pattern))


class ComponentRefreshLawTests(unittest.TestCase):
    def test_component_refresh_law_is_linked_and_bounded(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        docs_readme = (REPO_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        portable = (REPO_ROOT / "docs" / "CODEX_PORTABLE_LAYER.md").read_text(encoding="utf-8")
        law = (REPO_ROOT / "docs" / "COMPONENT_REFRESH_LAW.md").read_text(encoding="utf-8")

        self.assertIn("docs/COMPONENT_REFRESH_LAW.md", readme)
        self.assertIn("docs/COMPONENT_REFRESH_LAW.md", agents)
        self.assertIn("COMPONENT_REFRESH_LAW.md", docs_readme)
        self.assertIn("COMPONENT_REFRESH_LAW.md", portable)

        for token in (
            "component:skills-export:foundation",
            "It does not make `aoa-skills`",
            "Do not hand-edit `.agents/skills/*`",
            "Do not turn repeated refresh work into hidden automatic mutation.",
        ):
            self.assertIn(token, law)

    def test_skills_export_refresh_example_tracks_live_surfaces(self) -> None:
        payload = _load_json(EXAMPLE_PATH)

        self.assertEqual(payload["schema_version"], "aoa_component_refresh_law_v1")
        self.assertEqual(payload["component_ref"], "component:skills-export:foundation")
        self.assertEqual(payload["owner_repo"], "aoa-skills")
        self.assertEqual(payload["followthrough_home"], "aoa-playbooks:component-refresh-cycle")

        for key in (
            "source_authored_inputs",
            "generated_surfaces",
            "projected_or_installed_surfaces",
            "drift_signals",
            "proof_commands",
            "rollback_anchors",
        ):
            self.assertTrue(payload[key], msg=f"{key} must not be empty")

        for pattern in payload["source_authored_inputs"]:
            matches = _resolve_pattern(pattern)
            self.assertTrue(matches, msg=f"expected matches for source pattern {pattern!r}")

        for pattern in payload["generated_surfaces"]:
            matches = _resolve_pattern(pattern)
            self.assertTrue(matches, msg=f"expected matches for generated pattern {pattern!r}")

        refresh_window = payload["refresh_window"]
        self.assertEqual(refresh_window["stale_after_days"], 7)
        self.assertEqual(refresh_window["repeat_trigger_threshold"], 2)
        self.assertEqual(refresh_window["open_window_days"], 5)

        routes = payload["refresh_routes"]
        self.assertIn("python scripts/build_catalog.py --check", routes["check"])
        self.assertIn("python scripts/build_catalog.py", routes["execute"])
        self.assertIn(
            "python scripts/validate_agent_skills.py --repo-root .",
            routes["validate"],
        )

        proof_commands = set(payload["proof_commands"])
        self.assertIn("python scripts/build_catalog.py --check", proof_commands)
        self.assertIn("python -m pytest -q tests", proof_commands)

        for signal in payload["drift_signals"]:
            self.assertIn(signal["recommended_route_class"], ALLOWED_ROUTE_CLASSES)

        for anchor in payload["rollback_anchors"]:
            self.assertTrue((REPO_ROOT / anchor).exists(), msg=f"missing rollback anchor {anchor}")


if __name__ == "__main__":
    unittest.main()
