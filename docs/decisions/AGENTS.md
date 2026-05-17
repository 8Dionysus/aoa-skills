# AGENTS.md

## Applies to

This card applies to `docs/decisions/`.

## Role

Decision records preserve why structural, ownership, workflow, validator, route-law, topology, public-contract, or export-posture choices were made.

## Read before editing

Read root `AGENTS.md`, `docs/AGENTS.md`, and the nearest existing decision for the same surface before adding a new record.

## Boundaries

Do not use a decision record to make active changes by itself. If current behavior changes, update the active source surface and let the decision explain why.

## Validation

Run `git diff --check`. If the decision changes a validated surface, run that surface's validator too.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
