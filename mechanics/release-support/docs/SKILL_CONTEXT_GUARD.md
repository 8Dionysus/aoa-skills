# Skill context guard

The context guard exists because losing a skill after activation looks like nothing happened, but behavior quietly decays.

## Rules

- activated skills are marked as protected from compaction
- each skill carries an `instruction_sha256`
- each skill carries a `dedupe_key = skill-name + instruction-sha256`
- if the same skill is already active with the same digest, the governed seam recommends reuse instead of reinjection
- compaction packets carry must-keep items, retained sections, rehydration hints, allowlist paths, and trust state

## Rehydration

Use:

- `scripts/skill_runtime_guardrails.py compact`
- `scripts/skill_runtime_guardrails.py rehydrate`

`compact` emits guarded packets.
`rehydrate` rebuilds the minimal packets and, optionally, the suggested activation calls to restore full instructions.

## Session enrichment

When a skill is activated through the governed seam, the session record is enriched with:

- `source_scope`
- `repo_trusted_at_activation`
- `repo_identity`
- `instruction_sha256`
- `dedupe_key`
- `resolved_allowlist_paths`
- `allowlist_id`

That enriched record lets a local wrapper survive long sessions without forgetting what the skill was supposed to be doing.
