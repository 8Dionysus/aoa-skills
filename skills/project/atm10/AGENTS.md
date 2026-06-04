# AGENTS.md

## Applies to

This card applies to `skills/project/atm10/`.

## Role

This lane owns ATM10 project skills for local companion and source-of-truth work.

## Read before editing

Read `skills/project/AGENTS.md`, the target bundle, and the owning ATM10 repository guidance before editing.

## Boundaries

Do not generalize ATM10-only assumptions into core skills or sibling projects.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run `PYTHONPATH=scripts python scripts/validation/validate_skills.py`, `PYTHONPATH=scripts python scripts/builders/build_catalog.py --check`, `PYTHONPATH=scripts python scripts/validation/validate_agent_skills.py --repo-root .`, and focused bundle checks when present.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
