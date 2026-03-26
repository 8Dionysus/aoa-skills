# Runtime seam, second path

This is the dedicated-tool path.

Instead of telling the runtime to read `SKILL.md` directly, the runtime exposes explicit tool-shaped seams around the existing Codex-facing export.

## Stages

### Discover

The runtime sees only a compact catalog:

- name
- description
- trust posture
- invocation mode
- mutation surface
- explicit handles

This stage is optimized for shortlist selection.

### Disclose

This is an AoA extension layer, not a replacement for the skill itself.

Disclosure returns:

- compatibility and metadata
- section headings
- section summaries
- UI/policy preview from `agents/openai.yaml`
- resource inventory
- collision-family context and nearby skills
- sample trigger and negative prompts

The point is to let a harness preview the skill before injecting the full body.

### Activate

Activation returns the full instruction body plus runtime wrapping:

- stripped or included frontmatter
- full `instructions_markdown`
- `structured_wrap` with `<skill_content ...>` and `<skill_resources>`
- allowlist paths
- runtime contract
- context-retention contract
- trust policy
- optional session-state update

## Session behavior

When a session file is provided:

- activations are deduplicated by skill name
- active skills are marked `protected_from_compaction`
- `must_keep` and `rehydration_hint` are persisted
- `compact` emits a packet suitable for long-running local agents

## Compatibility notes

- keep `.agents/skills/*` as the shared surface
- use `generated/runtime_prompt_blocks.json` to inject the catalog into a system prompt or tool description
- use `generated/runtime_tool_schemas.json` to wrap the seam as callable tools
- keep `scripts/activate_skill.py` only for older integrations
