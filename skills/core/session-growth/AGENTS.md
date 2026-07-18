# AGENTS.md

## Applies to

This card applies to `skills/core/session-growth/`.

## Role

This lane owns session harvest, memo writeback, recovery, and the transitional
checkpoint-closeout callable front door.

## Read before editing

Read `skills/AGENTS.md`, `skills/core/AGENTS.md`, the target bundle, the
session-growth capability family, and the current session owner boundary.

## Boundaries

Session evidence is candidate input, not repository truth or durable memory.
Do not copy raw transcripts, hidden context, task-local DAGs, or session state
into the bundle. Write only reviewed owner-local procedures and contracts.

## Validation

Manually test missing, stale, partial, unsafe, and successful evidence paths;
then run the focused structural and export checks.

## Closeout

Report evidence custody, manual recovery/harvest cases, any candidate handoff,
checks, and session artifacts removed.
