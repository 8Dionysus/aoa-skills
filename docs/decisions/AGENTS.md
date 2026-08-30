# AGENTS.md

## Applies to

This card applies to `docs/decisions/` and durable decision notes inside it.

## Role

Decision records preserve why structural, ownership, workflow, validator,
route-law, topology, public-contract, source/export, skill-lane, generated
lookup, or mechanic choices were made.

Decision notes explain why a route was chosen. Current skill, design,
architecture, generated-reader, portable-export, mechanic, review, and
sibling-owner authority stays with the owning source surface.

## Read before editing

Inspect the template, nearest decision for the same surface, and affected owner
source. Use the decision README or generated indexes only to choose the lane or
locate precedent.

## Boundaries

Do not use a decision record to make active changes by itself. If current behavior changes, update the active source surface and let the decision explain why.

Keep evidence, working notes, generated output, and runtime facts as context;
do not promote them into decision authority.

Give every decision a canonical `Decision ID: AOA-SK-D-####` whose filename
prefix matches the ID exactly. Give every decision an `## Index Metadata` block
so lookup indexes can be regenerated from source notes instead of hand-maintained
crosswalks.
Keep `modeled_surfaces` in `indexes/index_contract.yaml` as a top-level list
of normalized repo-relative paths under `docs/decisions/`; do not use it for
root non-record Markdown.

Old date-prefixed decision paths stay in git history only. Do not recreate
date-named stubs or compatibility maps for retired paths.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run:

```bash
PYTHONPATH=scripts python scripts/decisions/generate_decision_indexes.py --check
git diff --check
```

When decision metadata changes, run `PYTHONPATH=scripts python scripts/decisions/generate_decision_indexes.py`
before the `--check` form.

If the decision changes a validated surface, run that surface's validator too.

## Closeout

Report which decision was added or changed, whether generated lookup indexes
were refreshed, which source surface it constrains, what validation ran, what
existing drift remains, and which follow-up route the decision enables. If a
nearby source document carried agent-facing working law into this card, name
that transfer.
