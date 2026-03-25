# Context retention support

Codex already uses progressive disclosure for skills.
Wave 3 adds a generated support layer so other runtimes or wrappers can hold onto the right fragments without re-reading everything blindly.

## Generated file

`generated/context_retention_manifest.json`

Per skill it records:

- `compact_summary`
- `activation_card_markdown`
- `must_keep`
- `retain_sections`
- `metadata_keys`
- `rehydration_hint`

## Intended use

- compact discovery surfaces
- wrapper-level memory retention
- rehydration after context compaction
- guardrails for smaller local models later

## Non-goals

This manifest does not replace:

- the full `SKILL.md`
- `description`-based triggering
- policy in `agents/openai.yaml`

It is support metadata around the export, not a substitute for the export.
