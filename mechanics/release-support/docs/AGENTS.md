# AGENTS.md

## Applies to

This card applies to `mechanics/release-support/docs/`.

## Role

This lane owns release-support documentation for portable export, runtime path, and component refresh law.

## Read before editing

Read parent `mechanics/release-support/AGENTS.md`, docs README, and the referenced builder or validator.

## Boundaries

Do not describe manual pack edits as source work. Portable export must remain builder-backed and receipt-aware.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Use `python scripts/ci_gate.py --mode export` for export/support surfaces and
`python scripts/ci_gate.py --mode release` for release-facing surfaces, or the
specific export/support validator named by the changed document.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
