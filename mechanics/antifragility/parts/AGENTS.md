# AGENTS.md

## Applies to

This card applies to `mechanics/antifragility/parts/`.

## Role

This lane owns active antifragility parts and collision-stress implementation surfaces.

## Read before editing

Read parent `mechanics/antifragility/AGENTS.md`, `PARTS.md`, and the target part README.

## Boundaries

Do not make risk probes into release claims, status promotions, or project-wide mandates without owner review.

## Validation

`python -m pytest -q tests/test_mechanics_topology.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
