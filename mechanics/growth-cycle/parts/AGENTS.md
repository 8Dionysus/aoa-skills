# AGENTS.md

## Applies to

This card applies to `mechanics/growth-cycle/parts/`.

## Role

This lane owns active growth-cycle parts and candidate implementations.

## Read before editing

Read parent `mechanics/growth-cycle/AGENTS.md`, `PARTS.md`, and target part docs.

## Boundaries

Do not make part-local adaptive skill experiments into canonical skill status without review gates.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

`python -m pytest -q tests/test_session_growth_kernel_maturity.py tests/test_session_checkpoint_note.py`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
