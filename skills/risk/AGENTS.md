# AGENTS.md

## Applies to

This card applies to `skills/risk/`.

## Role

This lane owns risk-control skills such as approval gates, dry-run-first, sanitized share, local stack bringup, and safe infra change.

## Read before editing

Read `skills/AGENTS.md`, the target risk bundle, and any guard or approval surface referenced by the task.

## Boundaries

Risk skills must make actions safer without becoming blanket permission. Keep gates explicit and do not hide risky mutation behind workflow language.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run `PYTHONPATH=scripts python scripts/validation/validate_skills.py`, `PYTHONPATH=scripts python scripts/builders/build_catalog.py --check`, `PYTHONPATH=scripts python scripts/validation/validate_agent_skills.py --repo-root .`, and focused bundle checks when present.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
