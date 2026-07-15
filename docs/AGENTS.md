# AGENTS.md

## Applies to

This card applies to `docs/` unless a nearer card narrows the lane.

## Role

`docs/` explains current architecture, topology, validation, testing, review,
and durable repository decisions.

## Read before editing

Read root `AGENTS.md`, `docs/README.md`, and the nearest owner card. For system
claims read `CHARTER.md`, `DESIGN.md`, and authored capability sources.

## Boundaries

Docs route and explain; they do not override capability sources, `SKILL.md`,
external owners, or generated parity. Keep session traces and task-local plans
out. Historical rationale belongs in decision records or Git history, not in a
second active contract.

## Validation

Review links and claims against current owner surfaces, run `git diff --check`,
and run an owner validator only when the documented contract actually moved.

## Closeout

Report current claims changed, owner sources checked, stale active material
removed, validation, and any decision record added or superseded.
