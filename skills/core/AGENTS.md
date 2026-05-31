# AGENTS.md

## Applies to

This card applies to `skills/core/`.

## Role

This lane owns core skills that should remain broadly useful inside the AoA skill layer.

## Read before editing

Read `skills/AGENTS.md`, `skills/core/engineering/AGENTS.md` or `skills/core/session-growth/AGENTS.md`, and the target bundle.

## Boundaries

Core skills must stay self-contained and broadly applicable; avoid narrow repository-only examples unless they are clearly examples, not the rule.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run `python scripts/validate_skills.py`, `python scripts/build_catalog.py --check`, `python scripts/validate_agent_skills.py --repo-root .`, and focused bundle checks when present.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
