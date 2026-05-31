# AGENTS.md

## Applies to

This card applies to `skills/project/abyss/`.

## Role

This lane owns AbyssOS/AoA project skills for safe infra, sanitized sharing, and diagnostic spine work.

## Read before editing

Read `skills/project/AGENTS.md`, the target `SKILL.md`, and the owning AbyssOS or AoA repo card before changing behavior.

## Boundaries

Keep Abyss project language clear without making these skills universal defaults for non-Abyss repos.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run `python scripts/validate_skills.py`, `python scripts/build_catalog.py --check`, `python scripts/validate_agent_skills.py --repo-root .`, and focused bundle checks when present.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
