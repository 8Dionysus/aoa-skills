# AGENTS.md

## Applies to

This card applies to `mechanics/questbook/`.

## Role

This package owns the repo-local quest schema, admission boundary, deterministic
catalog/dispatch projection, and active root index.

## Read before editing

Read root and mechanics cards, `mechanics/questbook/README.md`, `QUESTBOOK.md`,
the schemas, builder, validator, and current quest sources.

## Boundaries

Questbook is not a second roadmap, hidden queue, session ledger, skill
promotion engine, or proof system. Empty is a valid and preferred state when no
durable obligation survives.

## Validation

Build with `scripts/builders/build_questbook.py`, run its parity check, then the
Questbook surface validator and focused test.

## Closeout

Report admitted/closed/removed IDs, owner anchors, generated parity, validation,
and session material kept out.
