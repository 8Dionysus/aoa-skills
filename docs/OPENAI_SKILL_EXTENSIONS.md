# Optional OpenAI skill extensions

`config/openai_skill_extensions.json` is the repo-owned seam for optional `agents/openai.yaml` metadata that should not live in the canonical AoA authoring surface.

## Intended use

Use this file for optional Codex-facing metadata such as:

- interface polish
- icon overrides
- brand color overrides
- MCP tool dependencies
- future OpenAI-specific metadata that should stay outside the canonical AoA layer

Keep canonical routing and risk posture elsewhere:

- trigger text stays in `config/portable_skill_overrides.json`
- invocation policy stays derived from canonical invocation mode
- pack/profile and trust posture stay in `config/skill_pack_profiles.json` and `config/skill_policy_matrix.json`
- canonical authoring still lives in `skills/*/SKILL.md` and the generated AoA catalogs

For named MCP dependency wiring in this repository:

- keep `skills/*/agents/openai.yaml` policy-only
- author generated-export MCP dependencies here
- rebuild `.agents/skills/*/agents/openai.yaml` through `scripts/build_agent_skills.py`
- use `docs/CODEX_SKILL_MCP_WIRING.md` for the workspace-facing discipline and example route families

## Shape

```json
{
  "schema_version": 1,
  "global": {
    "interface": {},
    "dependencies": {
      "tools": []
    }
  },
  "skills": {
    "example-skill": {
      "dependencies": {
        "tools": [
          {
            "type": "mcp",
            "value": "openaiDeveloperDocs",
            "description": "OpenAI Docs MCP server",
            "transport": "streamable_http",
            "url": "https://developers.openai.com/mcp"
          }
        ]
      }
    }
  }
}
```

## Merge rules

- global metadata is merged first
- per-skill metadata is merged second
- generated default icons and brand colors are written before extensions merge
- canonical `allow_implicit_invocation` always wins over extension attempts
