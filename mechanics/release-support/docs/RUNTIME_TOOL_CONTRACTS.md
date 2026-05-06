# Runtime tool contracts

The wave-4 seam exposes six tool-shaped operations.

## discover_skills

Purpose: shortlist candidate skills before activation.

Inputs:

- `query`
- `trust_posture`
- `invocation_mode`
- `mutation_surface`
- `allow_implicit_invocation`
- `limit`

Output source:

- `generated/runtime_discovery_index.json`

## disclose_skill

Purpose: preview one skill without injecting the full body.

Inputs:

- `skill_name`

Output source:

- `generated/runtime_disclosure_index.json`

## activate_skill

Purpose: inject the full skill body with runtime wrappers and optional session tracking.

Inputs:

- `skill_name`
- `session_file`
- `explicit_handle`
- `include_frontmatter`
- `wrap_mode`

Runtime implementation:

- `scripts/skill_runtime_seam.py activate`

## skill_session_status

Purpose: inspect active-skill state for the current local session.

## deactivate_skill

Purpose: drop one active skill from session state without touching the export.

## compact_skill_session

Purpose: emit a compaction-safe rehydration packet for long-running sessions.

## Generated references

- `generated/runtime_tool_schemas.json`
- `generated/runtime_session_contract.json`
- `generated/runtime_seam_manifest.json`
