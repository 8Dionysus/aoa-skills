# AGENTS.md

## Applies to

This card applies to `skills/project/titan/`.

## Role

This lane owns Titan project skills for approval, runtime, memory, receipt, and console workflows.

## Read before editing

Read `skills/project/AGENTS.md`, the target bundle, and Titan owner guidance before editing.

## Boundaries

Keep Titan runtime and memory claims in Titan-owned context. This repo owns the skill wrapper, not live Titan state.

## Validation

Run `python scripts/validate_skills.py`, `python scripts/build_catalog.py --check`, `python scripts/validate_agent_skills.py --repo-root .`, and focused bundle checks when present.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
