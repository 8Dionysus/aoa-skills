# AGENTS.md

## Applies to

This card applies to `mechanics/rpg/parts/`.

## Role

This lane owns active RPG reader parts and ability-reader support surfaces.

## Read before editing

Read parent `mechanics/rpg/AGENTS.md`, `PARTS.md`, and target part docs.

## Boundaries

Do not make reader metaphors into role authority or agent identity. Keep ability-reader surfaces bounded and generated-aware.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

`python -m pytest -q tests/test_generated_surface_schemas.py tests/test_roadmap_parity.py`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
