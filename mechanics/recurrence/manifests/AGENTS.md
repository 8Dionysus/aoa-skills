# AGENTS.md

## Applies to

This card applies to `mechanics/recurrence/manifests/`.

## Role

This lane owns recurrence manifests that summarize repeated-use observations.

## Read before editing

Read parent `mechanics/recurrence/AGENTS.md`, `manifests/README.md`, and the manifest builder or report that consumes these files.

## Boundaries

Manifests show recurrence evidence; they do not promote status or replace review records.

## Validation

`python -m pytest -q tests/test_roadmap_parity.py tests/test_current_direction_routes.py` plus any manifest validator.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
