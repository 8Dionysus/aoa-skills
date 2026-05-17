# AGENTS.md

## Applies to

This card applies to `mechanics/rpg/` except where a nearer card applies.

## Role

`mechanics/rpg/` owns ability-reader surfaces and role-like reader projections without turning skills into characters for the skill layer. RPG package guidance keeps this movement bounded and reviewable.

## Read before editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/rpg/README.md`, `mechanics/rpg/DIRECTION.md`, `mechanics/rpg/PARTS.md`, `mechanics/rpg/PROVENANCE.md`, `mechanics/rpg/ROADMAP.md`, and any nearer card, `parts/AGENTS.md`.

## Boundaries

Keep `mechanics/rpg/` focused on mechanic movement. Do not make it canonical skill content, sibling-repo technique truth, proof doctrine, or generated authority. Preserve ability-reader as a bounded local signal, not a global command.

## Validation

Run `python -m pytest -q tests/test_generated_surface_schemas.py tests/test_roadmap_parity.py`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
