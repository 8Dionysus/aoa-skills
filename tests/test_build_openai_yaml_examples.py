from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "build_openai_yaml_examples.py"


class BuildOpenaiYamlExamplesTests(unittest.TestCase):
    def test_build_emits_expected_files(self) -> None:
        mapping = {
            "schema_version": "1",
            "mcp_registry": {
                "aoa_workspace": {"description": "workspace", "transport": "stdio"}
            },
            "skill_wirings": [
                {
                    "slug": "workspace-orientation",
                    "display_name": "AoA workspace orientation",
                    "short_description": "Orient first.",
                    "default_prompt": "Orient before deeper work.",
                    "allow_implicit_invocation": True,
                    "mcp_dependencies": ["aoa_workspace"],
                }
            ],
        }
        with tempfile.TemporaryDirectory(prefix="aoa-skill-mcp-build-") as temp_dir:
            root = Path(temp_dir)
            map_path = root / "skill_mcp_wiring.map.json"
            map_path.write_text(json.dumps(mapping), encoding="utf-8")
            output_dir = root / "out"

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--map",
                    str(map_path),
                    "--output-dir",
                    str(output_dir),
                ],
                check=True,
            )

            result = output_dir / "openai.workspace-orientation.example.yaml"
            self.assertTrue(result.exists())
            text = result.read_text(encoding="utf-8")
            self.assertIn("display_name: AoA workspace orientation", text)
            self.assertIn("value: aoa_workspace", text)

    def test_build_check_mode_detects_drift(self) -> None:
        mapping = {
            "schema_version": "1",
            "mcp_registry": {
                "aoa_workspace": {"description": "workspace", "transport": "stdio"}
            },
            "skill_wirings": [
                {
                    "slug": "workspace-orientation",
                    "display_name": "AoA workspace orientation",
                    "short_description": "Orient first.",
                    "default_prompt": "Orient before deeper work.",
                    "allow_implicit_invocation": True,
                    "mcp_dependencies": ["aoa_workspace"],
                }
            ],
        }
        with tempfile.TemporaryDirectory(prefix="aoa-skill-mcp-build-") as temp_dir:
            root = Path(temp_dir)
            map_path = root / "skill_mcp_wiring.map.json"
            map_path.write_text(json.dumps(mapping), encoding="utf-8")
            output_dir = root / "out"
            output_dir.mkdir()
            generated = output_dir / "openai.workspace-orientation.example.yaml"
            generated.write_text("drifted: true\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--map",
                    str(map_path),
                    "--output-dir",
                    str(output_dir),
                    "--check",
                ],
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "Out of date file",
                f"{result.stdout}\n{result.stderr}",
            )


if __name__ == "__main__":
    unittest.main()
