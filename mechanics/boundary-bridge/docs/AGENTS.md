# AGENTS.md

## Applies to

This card applies to `mechanics/boundary-bridge/docs/`.

## Role

This lane owns bridge documentation for layer position, runtime routes, and skill-technique exchange.

## Read before editing

Read parent `mechanics/boundary-bridge/AGENTS.md`, `mechanics/boundary-bridge/docs/README.md`, and the referenced skill or technique surface.

## Boundaries

Do not collapse skills into techniques or techniques into skills. The bridge explains interaction while each owner keeps its own truth.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

`PYTHONPATH=scripts python scripts/validation/validate_tiny_router_inputs.py --repo-root .` and bridge-specific build checks when docs feed generated routes.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
