# Root Design And Agent Surface Split

- Decision ID: AOA-SK-D-0020

## Index Metadata

- Original date: 2026-05-16
- Surface classes: root/topology, agent route, docs route
- Skill lanes: none
- Mechanic parents: none
- Guard families: AGENTS/mesh, docs route
- Posture: accepted root surface split

## Status

Accepted.

## Context

The AoA center uses a three-surface root pattern:

- `DESIGN.md` describes the system form.
- `DESIGN.AGENTS.md` describes the agent-facing guidance form.
- `AGENTS.md` routes active agent work.

`aoa-skills` already had strong owner boundaries in `AGENTS.md`,
`docs/ARCHITECTURE.md`, and mechanics surfaces, but it lacked the same
root-level separation of system design, agent-surface design, and operational
route law. That made future root edits more likely to bloat `README.md`,
`docs/ARCHITECTURE.md`, or `AGENTS.md` with overlapping authority.

## Decision

Add root `DESIGN.md` and `DESIGN.AGENTS.md` for `aoa-skills`, adapted to the
bounded execution canon instead of copied from the AoA center.

Refactor root `AGENTS.md` into the canonical six-section route-card shell before
repo-specific sections, preserving current owner boundaries, GitHub landing
workflow, validation posture, and generated/export stop-lines.

## Consequences

- `DESIGN.md` now owns the skill-layer system form.
- `DESIGN.AGENTS.md` now owns the form of agent-facing guidance.
- `AGENTS.md` remains the active operational route law.
- `docs/ARCHITECTURE.md` remains the technical model, not the root design
  compass.
- Generated and exported surfaces remain weaker than authored skill sources and
  the builders/config that produce them.

Future changes that alter card shape, route modes, closeout, source/export
posture, adapter vocabulary, or root guidance should review this decision and
the root trio together.
