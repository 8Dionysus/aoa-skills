# Decision Graph Impact And Issue-Aware Skills

- Decision ID: AOA-SK-D-0035
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `skills/core/engineering/aoa-decision/`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: skill source, agent route, export/runtime
- Skill lanes: core/engineering, portable/export
- Mechanic parents: boundary-bridge
- Guard families: decision graph, source topology, export/runtime, evaluation/public surface
- Posture: accepted issue-aware decision-graph skill route

## Context

The decision graph skill chain already routes decision-lane work through
`aoa_decisions` before repo-local source reads. The MCP surface now exposes
impact and issue packets for changed paths, source surfaces, owner surfaces,
repo coverage posture, and unknown decision-lane surfaces.

The skills need to name those routes explicitly so agents do not fall back to
broad manual scans or create/correct records while the graph is reporting
coverage issues.

## Options Considered

- Leave the skills at generic graph-first guidance and rely on MCP tool names.
- Add one new audit skill for graph issues.
- Keep the current router chain and make find/create/correct issue-aware and
  impact-packet-aware.

## Decision

Choose the third option.

Update `aoa-decision` and its find/create/correct subskills to check graph
status and issues first, use the narrowest impact packet available, and block
target-repo create/correct writes when unresolved graph issues exist for that
repo.

The router still selects exactly one subskill. The graph remains a read model;
source decision notes and repo-local validators remain authoritative.

## Rationale

The existing chain shape is still right. The missing part was stronger runtime
behavior when the graph can answer impact questions directly or when graph
coverage says the decision lane is not healthy.

Issue-aware behavior protects quality without adding a background daemon, write
MCP route, or forced symmetry requirement.

## Consequences

- Positive: touched paths can route through changed-path packets before broad
  decision-lane scans.
- Positive: source-surface and owner-surface questions have direct graph-first
  paths.
- Positive: create/correct workflows stop in affected repos when graph issues
  indicate unknown or unmodeled decision-lane surfaces.
- Tradeoff: skill descriptions and generated router inputs need regeneration.
- Follow-up: if graph issue triage becomes a large repeated workflow, consider
  a separate audit subskill later.

## Current Applicability

As of 2026-06-04:

- Still valid: graph packets are lookup aids, not decision authority.
- Still valid: subskills remain bounded and selected deliberately.
- Changed: impact packets and graph issue posture are now part of the skill
  route contract.
- Not superseded.

## Review Log

### 2026-06-04 - Impact packet and issue posture

- Previous assumption: generic graph-first guidance was enough.
- New reality: `aoa_decisions` exposes specific impact and issue packets.
- Reason: agents need the fastest accurate route and a stop line when graph
  coverage is not clean.
- Source surfaces updated: `skills/core/engineering/aoa-decision*`,
  `config/portable_skill_overrides.json`, and router cue config.
- Validation: skill validators, export builders, MCP wiring checks, and
  decision-index checks should run after generated surfaces are refreshed.

## Boundaries

This decision does not add a write-capable MCP tool, hook, timer, daemon, or
background refresh service. It does not require identical decision-lane shape
across repos.

## Validation

Validation covered skill source with generated projections, catalog parity,
portable agent skills, workspace MCP-wiring compatibility, and decision-index
parity.
