# AGENTS.md

## Applies to

This card applies to `schemas/`.

## Role

`schemas/` owns machine contracts for skill bundles, generated surfaces, support resources, examples, and export records.

## Read before editing

Read root `AGENTS.md`, `schemas/README.md`, the changed schema, and every builder or validator that names it. For bundle schemas, inspect how `SKILL.md` and metadata are validated.

## Boundaries

Schema edits are contract edits. Preserve `$schema` and `$id`, keep backward compatibility explicit, and do not widen fields to hide invalid source data.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run `python scripts/validate_skills.py`, the schema-specific tests, and any builder check for affected generated surfaces.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
