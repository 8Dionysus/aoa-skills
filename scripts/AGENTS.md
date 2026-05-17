# AGENTS.md

## Applies to

This card applies to `scripts/`.

## Role

`scripts/` owns deterministic builders, validators, audits, release helpers, and repo-relative automation for the skill canon.

## Read before editing

Read root `AGENTS.md`, `DESIGN.md`, `DESIGN.AGENTS.md` when route-law is touched, and the tests for the script being changed. Start from callers before changing shared helpers.

## Boundaries

Scripts must stay deterministic, repo-relative, public-safe, and explicit about source versus generated authority. Keep builder output stable, avoid network assumptions unless already part of the contract, and keep bounded language in reports.

## Validation

Run the script directly. For common builders and validators, use `python scripts/build_catalog.py`, `python scripts/validate_skills.py`, `python scripts/validate_agents_design.py`, related tests, and `python scripts/release_check.py` for release-facing changes.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
