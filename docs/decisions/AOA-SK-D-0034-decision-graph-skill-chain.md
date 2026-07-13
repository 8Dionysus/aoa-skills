# Decision Graph Skill Chain

- Decision ID: AOA-SK-D-0034
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `skills/core/engineering/aoa-decision/`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: skill source, agent route, export/runtime
- Skill lanes: core/engineering, portable/export
- Mechanic parents: boundary-bridge
- Guard families: decision graph, source topology, export/runtime, evaluation/public surface
- Posture: accepted decision-graph skill-chain route

## Context

AoA repositories now carry repo-local `docs/decisions/` lanes. A workspace
decision graph and `aoa_decisions` MCP server make cross-repo lookup cheaper,
but an agent working in another repository still needs to know that the graph is
the right first read path and that source decision files remain stronger than
graph nodes.

Putting all find/create/correct behavior into one large skill would make common
lookups more expensive and increase the chance that a create or correction
workflow is loaded when the user only needs prior rationale.

## Options Considered

- Keep using `aoa-adr-write` and rely on memory to remember graph lookup.
- Add one large `aoa-decision` skill with all find, create, and correct details
  inline.
- Add a small `aoa-decision` router that uses the decision graph first, then
  routes to bounded find, create, or correct subskills.

## Decision

Choose the router chain.

Add these core engineering skill bundles:

- `aoa-decision`
- `aoa-decision-find`
- `aoa-decision-create`
- `aoa-decision-correct`

`aoa-decision` is the implicit front door for clear decision-lane prompts. It
selects one subskill and instructs the agent to use `aoa_decisions` first when
the MCP is available. The subskills stay manual so they do not all compete for
implicit activation.

Codex-facing export metadata declares `aoa_decisions` as an MCP dependency for
the router and subskills through `config/openai_skill_extensions.json`. Install
profiles and the project-core engineering ring include the chain so repo-local
agents can discover it.

## Rationale

The chain makes graph use discoverable without making graph output
authoritative. It also keeps the common find path cheap while preserving clear
write workflows for record creation and correction.

The router/subskill split matches how decision-lane work actually branches:
finding rationale, creating new rationale, and correcting existing rationale
have different risks, validations, and stop lines.

## Consequences

- Positive: agents can discover the decision graph route from skill metadata and
  generated `agents/openai.yaml` dependencies.
- Positive: only the router is implicit; subskills are selected deliberately.
- Positive: source decision notes, repo-local generated indexes, and local
  validators remain stronger than graph packets.
- Tradeoff: the chain adds four skills to core engineering profiles and
  generated export surfaces.
- Follow-up: if decision-lane audit becomes a repeated distinct workflow, add a
  separate audit subskill instead of overloading find or correct.

## Current Applicability

As of 2026-06-04:

- Still valid: decision graph lookup is the first read path when available.
- Still valid: `aoa_decisions` is a dependency, not a decision authority.
- Still valid: create/correct workflows write repo-local source notes and
  rebuild repo-local indexes before refreshing the graph.
- Not superseded.

## Review Log

### 2026-06-04 - Initial chain

- Previous assumption: agents could rely on existing ADR/source-of-truth skills
  plus manual graph knowledge.
- New reality: cross-repo decision-lane work needs an explicit agent-facing
  graph route.
- Reason: graph-backed lookup should improve speed and accuracy without
  collapsing generated read models into source truth.
- Source surfaces updated: `skills/core/engineering/aoa-decision*`,
  `config/skill_pack_profiles.json`, `config/project_core_outer_ring.json`,
  `config/skill_policy_matrix.json`, `config/portable_skill_overrides.json`,
  `config/openai_skill_extensions.json`, `tests/fixtures/skill_evaluation_cases.yaml`,
  and `mechanics/boundary-bridge/examples/skill_mcp_wiring.map.json`.
- Validation: skill validators, catalog/export rebuilds, MCP wiring checks, and
  decision-index checks should run after generated surfaces are refreshed.

## Boundaries

This decision does not make `aoa-skills` the owner of repository decisions. It
does not make the MCP graph a write surface. It does not replace repo-local
decision route cards, templates, generated indexes, or validation commands.

## Validation

Validation covered skill source, catalog parity, portable agent skills,
workspace MCP-wiring compatibility, and decision-index parity.
