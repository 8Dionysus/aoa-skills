# AGENTS.md

## Applies to

This card applies to `mechanics/checkpoint/parts/`.

## Role

This lane owns active checkpoint parts and implementation notes.

## Read before editing

Read parent `mechanics/checkpoint/AGENTS.md`, `PARTS.md`, and the target part README.

## Boundaries

Keep parts tied to checkpoint-note evidence and closeout routes; do not duplicate skill bundle content.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

`python -m pytest -q tests/test_session_checkpoint_note.py tests/test_session_growth_kernel_maturity.py`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
