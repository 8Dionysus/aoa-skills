# Codex config snippets

Wave 3 adds generated snippets for disabling whole install profiles cleanly.

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

- `examples/user-config.toml`
- `examples/project-config.toml`
- `examples/disable-risk-skills.toml`

These are examples only.
They are not authoritative repo config.
