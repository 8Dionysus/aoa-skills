# Codex config snippets

This document describes generated snippets for disabling whole install profiles cleanly.

## Generated file

`generated/codex_config_snippets.json`

It contains:

- one disable snippet per resolved install profile
- a small `project_root_markers` example

## Helper script

Render one profile's disable snippet:

```bash
python scripts/render_codex_config.py --repo-root . --profile repo-risk-explicit
```

## Example artifacts

- `mechanics/release-support/examples/user-config.toml`
- `mechanics/release-support/examples/project-config.toml`
- `mechanics/release-support/examples/disable-risk-skills.toml`
- `mechanics/boundary-bridge/examples/skill_mcp_wiring.map.json`
- `mechanics/boundary-bridge/examples/openai.*.example.yaml`

These are examples only.
They are not authoritative repo config.

The MCP wiring examples assume stable workspace server names:

- `aoa_workspace`
- `aoa_stats`
- `dionysus`
