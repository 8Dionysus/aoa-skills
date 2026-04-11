from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "validate_skill_mcp_wiring.py"


def write_workspace_config(path: Path) -> None:
    path.write_text(
        textwrap.dedent(
            """\
            [mcp_servers.aoa_workspace]
            command = "python"
            args = ["scripts/aoa_workspace_mcp_server.py"]

            [mcp_servers.aoa_stats]
            command = "python"
            args = ["scripts/aoa_stats_mcp_server.py"]

            [mcp_servers.dionysus]
            command = "python"
            args = ["scripts/dionysus_mcp_server.py"]
            """
        ),
        encoding="utf-8",
    )


class ValidateSkillMcpWiringTests(unittest.TestCase):
    def test_validate_reports_success(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aoa-skill-mcp-validate-") as temp_dir:
            root = Path(temp_dir)
            workspace_config = root / "config.toml"
            write_workspace_config(workspace_config)

            yaml_path = root / "openai.stats-observability.example.yaml"
            yaml_path.write_text(
                textwrap.dedent(
                    """\
                    interface:
                      display_name: "AoA stats observability"
                      short_description: "Inspect derived views."
                      default_prompt: "Read the summary surfaces."
                    policy:
                      allow_implicit_invocation: false
                    dependencies:
                      tools:
                        - type: "mcp"
                          value: "aoa_workspace"
                          transport: "stdio"
                        - type: "mcp"
                          value: "aoa_stats"
                          transport: "stdio"
                    """
                ),
                encoding="utf-8",
            )

            manifest = root / "local_adapter_manifest.min.json"
            manifest.write_text(
                json.dumps(
                    [
                        {
                            "name": "stats-observability",
                            "allow_implicit_invocation": False,
                        }
                    ]
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--workspace-config",
                    str(workspace_config),
                    "--local-adapter-manifest",
                    str(manifest),
                    "--paths",
                    str(yaml_path),
                    "--format",
                    "json",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["skills"][0]["errors"], [])

    def test_validate_catches_unknown_mcp(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aoa-skill-mcp-validate-") as temp_dir:
            root = Path(temp_dir)
            workspace_config = root / "config.toml"
            write_workspace_config(workspace_config)

            yaml_path = root / "openai.seed-route.example.yaml"
            yaml_path.write_text(
                textwrap.dedent(
                    """\
                    policy:
                      allow_implicit_invocation: false
                    dependencies:
                      tools:
                        - type: "mcp"
                          value: "missing_server"
                          transport: "stdio"
                    """
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--workspace-config",
                    str(workspace_config),
                    "--paths",
                    str(yaml_path),
                    "--format",
                    "json",
                ],
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ok"])
            self.assertTrue(
                any(
                    "unknown MCP dependency" in error
                    for error in payload["skills"][0]["errors"]
                )
            )

    def test_validate_catches_invocation_mismatch(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aoa-skill-mcp-validate-") as temp_dir:
            root = Path(temp_dir)
            workspace_config = root / "config.toml"
            write_workspace_config(workspace_config)

            yaml_path = root / "openai.workspace-orientation.example.yaml"
            yaml_path.write_text(
                textwrap.dedent(
                    """\
                    policy:
                      allow_implicit_invocation: true
                    dependencies:
                      tools:
                        - type: "mcp"
                          value: "aoa_workspace"
                          transport: "stdio"
                    """
                ),
                encoding="utf-8",
            )

            manifest = root / "local_adapter_manifest.min.json"
            manifest.write_text(
                json.dumps(
                    [
                        {
                            "name": "workspace-orientation",
                            "allow_implicit_invocation": False,
                        }
                    ]
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--workspace-config",
                    str(workspace_config),
                    "--local-adapter-manifest",
                    str(manifest),
                    "--paths",
                    str(yaml_path),
                    "--format",
                    "json",
                ],
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ok"])
            self.assertTrue(
                any(
                    "allow_implicit_invocation mismatch" in error
                    for error in payload["skills"][0]["errors"]
                )
            )

    def test_validate_discovers_generated_export_by_default(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aoa-skill-mcp-validate-") as temp_dir:
            root = Path(temp_dir)
            workspace_config = root / "config.toml"
            write_workspace_config(workspace_config)

            export_yaml = root / ".agents" / "skills" / "aoa-change-protocol" / "agents" / "openai.yaml"
            export_yaml.parent.mkdir(parents=True)
            export_yaml.write_text(
                textwrap.dedent(
                    """\
                    interface:
                      display_name: "AoA Change Protocol"
                      short_description: "Bound a meaningful change."
                      default_prompt: "Plan, change, verify, report."
                    policy:
                      allow_implicit_invocation: true
                    dependencies:
                      tools:
                        - type: "mcp"
                          value: "aoa_workspace"
                          transport: "stdio"
                    """
                ),
                encoding="utf-8",
            )

            generated_dir = root / "generated"
            generated_dir.mkdir()
            (generated_dir / "local_adapter_manifest.min.json").write_text(
                json.dumps(
                    {
                        "skills": [
                            {
                                "name": "aoa-change-protocol",
                                "allow_implicit_invocation": True,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--repo-root",
                    str(root),
                    "--workspace-config",
                    str(workspace_config),
                    "--format",
                    "json",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["path_count"], 1)
            self.assertEqual(payload["skills"][0]["skill_name"], "aoa-change-protocol")


if __name__ == "__main__":
    unittest.main()
