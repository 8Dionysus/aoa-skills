# AGENTS.md

## Applies to

This card applies to `mechanics/agon/parts/`.

## Role

This lane owns active Agon bridge parts, scripts, tests, and candidate outputs.

## Read before editing

Read parent `mechanics/agon/AGENTS.md`, `mechanics/agon/PARTS.md`, and the target part README before editing.

## Boundaries

Do not orphan parts from `PARTS.md`, do not bypass requested-only candidate boundaries, and do not treat candidate output as accepted skill truth.

## Validation

Run the changed part's builder, validator, and part-local test. For package
shape, also run `tests/test_mechanics_topology.py`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
