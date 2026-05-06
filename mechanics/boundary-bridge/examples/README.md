# Boundary-Bridge Examples

Public-safe examples for MCP wiring and Codex-facing OpenAI YAML scaffolds.

These examples demonstrate route-family shape only. Real per-skill metadata
belongs in `config/openai_skill_extensions.json` and generated exports, not in
the example scaffold.

Regenerate with:

```bash
python scripts/build_openai_yaml_examples.py --map mechanics/boundary-bridge/examples/skill_mcp_wiring.map.json --output-dir mechanics/boundary-bridge/examples
```
