# AGENTS.md

## Applies to

This card applies to `tests/`.

## Role

`tests/` owns repository proof for skill contracts, generated-surface parity, trigger collision behavior, public-safe exports, route traces, fault boundaries, and release helpers.

## Read before editing

Read root `AGENTS.md`, `docs/testing/TEST_TOPOLOGY.md`, the target script or source file, and neighboring tests before editing. Prefer adding the smallest test that proves the rule, then broaden only when the behavior crosses surfaces.

## Boundaries

Do not use tests to bless generated drift, adapter-only wording as core meaning, status promotion without review evidence, or broad semantic/model quality claims that belong to an eval organ. Fixtures must stay public-safe and should avoid brittle absolute host paths unless the test is explicitly workspace-scoped.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run the focused test first. For shared or release-facing behavior, use the `release_check` test lane from `config/validation_lanes.json`, currently `python -m pytest -q tests` for this directory. Use pytest markers from `pytest.ini` to keep source, generated, export, router, release, advisory, live, and slow checks visible.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
