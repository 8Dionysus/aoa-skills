# AGENTS.md

## Applies to

This card applies to `docs/` except where a nearer nested card applies.

## Role

`docs/` preserves architecture, repository structure, governance, reviews, decisions, and historical context for the skill layer.

## Read before editing

Read root `AGENTS.md`, `docs/README.md`, `docs/ARCHITECTURE.md`, and the nearest nested docs card. For route-law or agent-facing shape, also read `DESIGN.AGENTS.md`.

## Boundaries

Docs may explain, decide, and route, but they must not override `skills/**`, mechanic package source surfaces, generated-source boundaries, or review evidence. Move agent operational law into the nearest `AGENTS.md`; keep long rationale in docs.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

For docs-only changes, run `git diff --check`. For architecture, review, route-law, or generated/export claims, run the validator named by the owning surface and `PYTHONPATH=scripts python scripts/validation/validate_agents_design.py` when AGENTS cards moved.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
