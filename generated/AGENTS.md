# AGENTS.md

## Applies to

This card applies to `generated/`.

## Role

`generated/` carries deterministic read models for capability discovery,
portable export, release handoff, Questbook, and requested Agon candidates.

## Read before editing

Inspect the affected output, owner source, and builder. Use the README only to
select a projection or change the human map.

## Boundaries

Do not hand-author files in `generated/`. Fix authored sources, config, or the
builder and regenerate. A generated graph, catalog, receipt, or candidate never
outranks its source or proves outcome quality.

## Validation

Run the owning builder in build and parity-check posture, then the focused
validator. Use `config/validation_lanes.json` for grouped checks.

## Closeout

Report source moved, builder used, generated files changed, drift check, and
any consumer not refreshed.
