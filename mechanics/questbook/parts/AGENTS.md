# AGENTS.md

## Applies to

This card applies to `mechanics/questbook/parts/`.

## Role

This lane owns active questbook parts and integration helpers.

## Read before editing

Read parent `mechanics/questbook/AGENTS.md`, `PARTS.md`, and target part docs.

## Boundaries

Keep questbook integration connected to owning skill or mechanic surfaces; no orphan obligations.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

`python -m pytest -q tests/test_validate_skills_questbook_contract.py tests/test_session_checkpoint_note.py`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
