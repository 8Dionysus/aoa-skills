# AGENTS.md

## Applies to

This card applies to `manifests/`.

## Role

`manifests/` owns pack and release-oriented manifests that help consumers understand what canonical skill surfaces were exported or staged.

## Read before editing

Read root `AGENTS.md`, `manifests/README.md`, `generated/AGENTS.md`, and the manifest builder or validator before editing.

## Boundaries

Do not use manifests to promote skill status, certify downstream adoption, or replace canonical bundle metadata. Manifest claims must remain derivable or receipt-backed.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run the manifest builder or validator that owns the changed file. For release-visible manifest changes, run `python scripts/release_check.py`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
