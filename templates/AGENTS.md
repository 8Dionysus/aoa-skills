# AGENTS.md

## Applies to

This card applies to `templates/`.

## Role

`templates/` owns reusable source templates such as `SKILL.template.md` and `PROJECT_OVERLAY.template.md`.

## Read before editing

Read root `AGENTS.md`, `templates/README.md` if present, the consuming builder or validator, and at least one current canonical bundle using the template pattern.

## Boundaries

Preserve placeholder intent. Do not make templates silently AoA-only when they need to remain portable, and do not add fields that validators or generated surfaces cannot consume.

## Validation

Run `python scripts/validate_skills.py`, template-related tests, and any builder affected by the template.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.

## Template Contract

Templates teach expected source shape; they do not override live repository
doctrine, schemas, validators, or canonical bundles.

When changing a template, inspect a current canonical example and the validator
that accepts it. Keep optional sections visibly optional, required fields
matched to schema expectations, and generated/export consumers in sync.

Do not hide workflow law in a template that active bundles, schemas, and
validators do not understand.
