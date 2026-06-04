# AGENTS.md

## Applies to

This card applies to `docs/governance/`.

## Role

Governance docs name lanes, status rules, and review expectations that help the repository decide what a skill may claim.

## Read before editing

Read root `AGENTS.md`, `docs/AGENTS.md`, `docs/governance/lanes.md`, and `docs/governance/lanes.yaml` before editing.

## Boundaries

Do not change governance wording without checking validators and review surfaces that depend on it. Governance can constrain status; it cannot replace evidence.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run `PYTHONPATH=scripts python scripts/validation/validate_skills.py`, `PYTHONPATH=scripts python scripts/reports/report_skill_evaluation.py --fail-on-canonical-gaps`, and `git diff --check` when governance fields or lane semantics move.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
