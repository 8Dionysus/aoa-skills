# AGENTS.md

## Applies to

This card applies to `mechanics/recurrence/parts/`.

## Role

This lane owns active recurrence parts and repeated-use observation helpers.

## Read before editing

Read parent `mechanics/recurrence/AGENTS.md`, `PARTS.md`, and target part docs.

## Boundaries

Do not turn recurrence signals into automatic canonical promotion. Repetition is evidence pressure, not final status.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

`python -m pytest -q tests/test_roadmap_parity.py tests/test_current_direction_routes.py`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
