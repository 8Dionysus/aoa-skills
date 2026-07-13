# Mechanics Growth-Cycle Orchestration

- Decision ID: AOA-SK-D-0007

## Index Metadata

- Original date: 2026-05-06
- Surface classes: mechanic package
- Skill lanes: none
- Mechanic parents: growth-cycle
- Guard families: source topology
- Posture: accepted orchestration posture

Date: 2026-05-06

Status: accepted

## Context

After Checkpoint and Method-growth were separated, the remaining closeout and
harvest guidance was still flat in `docs/`. Direct reading showed two active
docs belong to the local Growth Cycle route:

- adaptive skill orchestration separates task execution, closeout, and harvest
- session-growth kernel maturity keeps reviewed packet and receipt examples
  bounded after `candidate_ref` already exists

The session-harvest notes directory is related evidence, but moving it would
pull note history, external evidence refs, and skill text references into the
same slice. That is a separate decision.

## Decision

Create `mechanics/growth-cycle/` and land only the orchestration and kernel
maturity slice:

- `docs/ADAPTIVE_SKILL_ORCHESTRATION.md` -> `mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md`
- `docs/SESSION_GROWTH_KERNEL_MATURITY.md` -> `mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md`

Add a package card, direction, parts, provenance, landing log, roadmap, active
docs map, and active parts for adaptive orchestration, session kernel maturity,
and harvest-note boundary.

At this decision point, keep `docs/session-harvests/` in place for this slice.

## Consequences

- The docs root no longer owns orchestration and kernel maturity guidance.
- Growth-cycle now has a local package route without absorbing checkpoint or
  method-growth truth.
- Recurrence component decision-surface refs follow the package-local adaptive
  orchestration path.
- Session-harvest notes remain bounded evidence below promotion authority.

## Verification

Verification covered session-growth orchestration, checkpoint behavior,
mechanics routes and topology, nested agent cards, and the repository test
suite.
