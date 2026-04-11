# Codex skill ↔ MCP wiring in `aoa-skills`

## Why this seam belongs here

`aoa-skills` already owns canonical skill meaning, the local extension seam, and
the generated Codex-facing export. That makes it the right repository for the
small metadata seam that tells Codex which named MCP servers a route depends on.

This seam must stay subordinate to `SKILL.md`.
It is a routing aid, not a second doctrine layer.

## Important repo-local adaptation

This repository already has two different `agents/openai.yaml` surfaces:

- `skills/*/agents/openai.yaml` is the source policy seam. Keep it narrow and
  policy-only.
- `.agents/skills/*/agents/openai.yaml` is the generated full Codex-facing
  export.
- `config/openai_skill_extensions.json` is the repo-owned seam for optional
  generated-export metadata such as named MCP dependencies.

That means the first honest place to author named MCP dependencies here is
`config/openai_skill_extensions.json`, not the source policy file under
`skills/*/agents/openai.yaml`.

## What to keep where

### Keep in `SKILL.md`

- the bounded workflow
- the execution law
- evidence posture
- fallbacks and guardrails
- resource contracts for `scripts/`, `references/`, and `assets/`

### Keep in `skills/*/agents/openai.yaml`

- source invocation policy
- narrow notes about policy posture

### Keep in `config/openai_skill_extensions.json`

- named MCP tool dependencies for the generated export
- optional UI metadata overrides that belong only to the Codex-facing layer

### Keep in `.agents/skills/*/agents/openai.yaml`

- the generated full Codex-facing metadata
- the merged view of interface, policy, and named tool dependencies

### Keep elsewhere

- workspace `.codex/config.toml` owns server installation and enablement
- workspace `.codex/agents/*.toml` owns custom role-bearing agents
- workspace or repo `AGENTS.md` owns durable route discipline

## First route families to wire

Start narrow:

1. workspace orientation
2. stats observability
3. seed route and planting navigation

The examples in `examples/skill_mcp_wiring.map.json` and
`examples/openai.*.example.yaml` describe those route families as scaffolds.
They are not new skill canon by themselves.

## Source alignment rule

If `generated/local_adapter_manifest.min.json` already advertises
`allow_implicit_invocation` for a real skill, the generated
`.agents/skills/*/agents/openai.yaml` surface should agree.

Use these layers together:

- `python scripts/build_agent_skills.py --repo-root .`
- `python scripts/validate_agent_skills.py --repo-root .`
- `python scripts/validate_skill_mcp_wiring.py --workspace-config /path/to/.codex/config.toml`

## Suggested merge path

1. keep the workspace server names stable: `aoa_workspace`, `aoa_stats`,
   `dionysus`
2. maintain route-family examples in `examples/skill_mcp_wiring.map.json`
3. author real per-skill MCP dependencies in `config/openai_skill_extensions.json`
4. rebuild the generated export
5. validate the generated export and optional workspace config alignment
6. only then land real skill-family wiring changes

## Practical advice

- start with a few real routes, not a blanket dependency fan-out
- prefer `aoa_workspace` first when owner-fit is unclear
- keep `aoa_stats` derived and non-sovereign
- keep `dionysus` seed-facing and non-sovereign
- do not move long doctrine, proof logic, or role prompts into generated
  `openai.yaml`
