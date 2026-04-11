#!/usr/bin/env python3
"""Build example Codex-facing openai.yaml files from an AoA wiring map."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


HEADER_LINES = (
    "# Example generated Codex-facing openai.yaml scaffold.",
    "# Do not copy this into skills/*/agents/openai.yaml unchanged.",
    "# In aoa-skills, named MCP dependencies belong in config/openai_skill_extensions.json",
    "# and then flow into the generated export under .agents/skills/*/agents/openai.yaml.",
)


def load_map(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Wiring map must be a JSON object.")
    if "mcp_registry" not in data or "skill_wirings" not in data:
        raise ValueError("Wiring map must contain 'mcp_registry' and 'skill_wirings'.")
    if not isinstance(data["mcp_registry"], dict):
        raise ValueError("'mcp_registry' must be an object.")
    if not isinstance(data["skill_wirings"], list):
        raise ValueError("'skill_wirings' must be a list.")
    return data


def build_yaml_payload(entry: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    missing = [name for name in entry.get("mcp_dependencies", []) if name not in registry]
    if missing:
        raise ValueError(f"Unknown MCP dependencies for {entry.get('slug')}: {missing}")

    tools = []
    for name in entry["mcp_dependencies"]:
        server = registry[name]
        tools.append(
            {
                "type": "mcp",
                "value": name,
                "description": server["description"],
                "transport": server.get("transport", "stdio"),
            }
        )

    return {
        "interface": {
            "display_name": entry["display_name"],
            "short_description": entry["short_description"],
            "default_prompt": entry["default_prompt"],
        },
        "policy": {
            "allow_implicit_invocation": bool(entry["allow_implicit_invocation"]),
        },
        "dependencies": {
            "tools": tools,
        },
    }


def emit_yaml_text(entry: dict[str, Any], payload: dict[str, Any]) -> str:
    header = list(HEADER_LINES)
    header.insert(1, f"# slug: {entry['slug']}")
    return "\n".join(header) + "\n" + yaml.safe_dump(
        payload,
        sort_keys=False,
        allow_unicode=True,
    )


def output_filename(slug: str) -> str:
    return f"openai.{slug}.example.yaml"


def write_outputs(mapping: dict[str, Any], output_dir: Path, *, check: bool = False) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    registry = mapping["mcp_registry"]
    for entry in mapping["skill_wirings"]:
        payload = build_yaml_payload(entry, registry)
        text = emit_yaml_text(entry, payload)
        path = output_dir / output_filename(entry["slug"])
        if check:
            if not path.exists():
                raise SystemExit(f"Missing expected file in check mode: {path}")
            current = path.read_text(encoding="utf-8")
            if current != text:
                raise SystemExit(f"Out of date file: {path}")
        else:
            path.write_text(text, encoding="utf-8")
        written.append(path)
    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--map",
        required=True,
        type=Path,
        help="Path to examples/skill_mcp_wiring.map.json",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for generated example YAML files",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check that generated files are up to date",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mapping = load_map(args.map)
    paths = write_outputs(mapping, args.output_dir, check=args.check)
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
