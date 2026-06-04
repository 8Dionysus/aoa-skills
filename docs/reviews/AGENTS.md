# AGENTS.md

## Applies to

This card applies to `docs/reviews/` and review subdirectories unless a nearer card is added.

## Role

Review docs preserve evaluated evidence for canonical candidacy, status promotions, and composition exceptions.

## Read before editing

Read root `AGENTS.md`, `docs/AGENTS.md`, `docs/reviews/README.md`, and the target skill bundle before changing a review file.

## Boundaries

A review file may record evidence; it must not auto-promote a skill. Status changes still need the configured evaluation and promotion gates.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run `PYTHONPATH=scripts python scripts/reports/report_skill_evaluation.py --fail-on-canonical-gaps`, `PYTHONPATH=scripts python scripts/reports/report_skill_promotion_pressure.py --repo-root . --workspace-root /srv/AbyssOS`, and the focused validator for the reviewed bundle when relevant.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
