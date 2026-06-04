# AGENTS.md

## Applies to

This card applies to `skills/core/engineering/`.

## Role

This lane owns engineering workflow skills such as contract tests, invariants, ports, ADRs, and source-of-truth checks.

## Read before editing

Read `skills/AGENTS.md`, `skills/core/AGENTS.md`, the target `SKILL.md`, `techniques.yaml`, and any checks/examples/references.

## Boundaries

Keep engineering skills neutral, execution-oriented, and not overfit to one repo. AoA examples may guide but must not collapse general utility.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run `PYTHONPATH=scripts python scripts/validation/validate_skills.py`, `PYTHONPATH=scripts python scripts/builders/build_catalog.py --check`, `PYTHONPATH=scripts python scripts/validation/validate_agent_skills.py --repo-root .`, and focused bundle checks when present.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
