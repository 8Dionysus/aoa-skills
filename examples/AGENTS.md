# AGENTS.md

## Applies to

This card applies to `examples/`.

## Role

`examples/` is the root example district for portable, public-safe demonstrations that do not belong to one mechanic package or one skill bundle.

## Read before editing

Read root `AGENTS.md`, `examples/README.md`, and the schema or builder referenced by the example. Use `mechanics/<slug>/examples/` for mechanic-local examples and bundle-local `examples/` for skill-specific runtime cards.

## Boundaries

Examples must be public-safe, preserve schema-backed shape when a schema exists, and be written with neutral placeholders. Do not use examples to introduce active doctrine, hidden adoption claims, secrets, or unbounded posture.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run the nearest schema or builder check. For broad example drift, run `python scripts/validate_skills.py` and any package-local tests named by the owning mechanic.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
