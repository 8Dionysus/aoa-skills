# AGENTS.md

## Applies to

This card applies to `tests/`.

## Role

`tests/` owns repository proof for skill contracts, generated-surface parity, trigger collision behavior, public-safe exports, and release helpers.

## Read before editing

Read root `AGENTS.md`, the target script or source file, and neighboring tests before editing. Prefer adding the smallest test that proves the rule, then broaden only when the behavior crosses surfaces.

## Boundaries

Do not use tests to bless generated drift, adapter-only wording as core meaning, or status promotion without review evidence. Fixtures must stay public-safe and should avoid brittle absolute host paths unless the test is explicitly workspace-scoped.

## Validation

Run the focused test first, then `python -m pytest -q tests` when the behavior is shared or release-facing.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
