# AGENTS.md

## Applies to

This card applies to `mechanics/recurrence/` except where a nearer card applies.

## Role

`mechanics/recurrence/` owns recurrence observation, repeated-use signals, and manifest-backed skill movement for the skill layer. Recurrence package guidance keeps this movement bounded and reviewable.

## Read before editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/recurrence/README.md`, `mechanics/recurrence/DIRECTION.md`, `mechanics/recurrence/PARTS.md`, `mechanics/recurrence/PROVENANCE.md`, `mechanics/recurrence/ROADMAP.md`, and any nearer card, `parts/AGENTS.md`, `legacy/AGENTS.md`, `manifests/AGENTS.md`.

## Boundaries

Keep `mechanics/recurrence/` focused on mechanic movement. Do not make it canonical skill content, sibling-repo technique truth, proof doctrine, or generated authority. Preserve recurrence observation as a bounded local signal, not a global command.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run `python -m pytest -q tests/test_roadmap_parity.py tests/test_current_direction_routes.py`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
