# Optional OpenAI skill extensions

`config/openai_skill_extensions.json` is the Wave 2 seam for optional `agents/openai.yaml` metadata that should not live in the canonical AoA authoring surface.

## Intended use

Use this file for optional Codex-facing metadata such as:

- interface polish
- icons
- brand color
- MCP tool dependencies
- future OpenAI-specific metadata that should stay outside the canonical AoA layer

Keep canonical routing and risk posture elsewhere:

- trigger text stays in `config/portable_skill_overrides.json`
- invocation policy stays derived from canonical invocation mode
- canonical authoring still lives in `skills/*/SKILL.md` and the generated AoA catalogs

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
- canonical `allow_implicit_invocation` always wins over extension attempts
