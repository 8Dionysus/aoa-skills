# Root Charter Boundary

- Decision ID: AOA-SK-D-0024

## Index Metadata

- Original date: 2026-05-18
- Surface classes: authority/charter, root/topology
- Skill lanes: none
- Mechanic parents: none
- Guard families: docs route, source topology
- Posture: accepted charter boundary

## Status

Accepted.

## Context

`aoa-skills` now has enough root surfaces that authority language can drift if
each file restates the same owner boundary in its own way.

Before this decision, the authority boundary for the skill system lived across
`README.md`, `DESIGN.md`, `DESIGN.AGENTS.md`, `AGENTS.md`, and
`docs/ARCHITECTURE.md`. That made `README.md` and `AGENTS.md` more likely to
carry charter-like claims while also trying to stay readable and operational.

The AoA center and `aoa-techniques` already use a root `CHARTER.md` to answer
what the repository may claim without replacing design, route, or architecture
surfaces.

## Decision

Add root `CHARTER.md` to `aoa-skills`.

The charter owns the repository authority boundary for the skill layer:

- what `aoa-skills` may claim about canonical skill workflow meaning
- what generated, portable, mechanic, review, and policy surfaces may carry
  without becoming source authority
- which adjacent object classes route to stronger owner repositories

Keep operational commands in `AGENTS.md`, local `AGENTS.md` cards, scripts,
validators, and release-support docs. Keep system form in `DESIGN.md`, agent
surface form in `DESIGN.AGENTS.md`, and technical source/generated/export
detail in `docs/ARCHITECTURE.md`.

## Consequences

- Root `README.md` can stay a public entry route instead of becoming an
  authority essay.
- Root `AGENTS.md` can route work and validation without carrying the full
  charter.
- `DESIGN.md` and `DESIGN.AGENTS.md` can describe form instead of repository
  permission.
- Future root posture, owner-boundary, public-claim, generated/export, or
  sibling-owner changes should review `CHARTER.md` first.
- The charter does not promote generated surfaces, portable exports, mechanics,
  review records, or downstream installs into source truth.
