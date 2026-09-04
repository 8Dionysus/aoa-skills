# AGENTS.md

## Applies to

This card applies to `tests/`.

## Role

`tests/` preserves the small set of durable invariants first established by
manual trials: capability integrity, source/export boundaries, pack handoff,
Questbook independence, and live validation-lane references.

## Read before editing

Inspect the manual observation and producer/consumer under test. Use
`TEST_TOPOLOGY.md` only to add, remove, or reclassify a durable test surface.

## Boundaries

Do not create tests as temporary scaffolding, encode a model judgment as a
golden truth, or use green output as evidence of agent benefit. Avoid tests for
retired compatibility surfaces. Fixtures remain minimal and public-safe.

## Validation

Reproduce behavior manually, run the focused test, then use the repository
[`Tests`](../VALIDATION.md#tests) route. Delete a test when its durable contract
disappears.

## Closeout

Report the manual invariant, test added/changed/removed, focused and full
results, and what the test intentionally does not prove.
