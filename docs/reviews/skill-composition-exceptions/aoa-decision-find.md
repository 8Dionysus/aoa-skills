# aoa-decision-find

## Current shape

- skill: `aoa-decision-find`
- technique_count: `1`
- technique_ids:
  - `AOA-T-0002`
- composition_class: `single_technique_exception`

## Package rationale

This skill packages a graph-first lookup workflow for decision records. It is
not a new authority layer; it turns the source-of-truth technique into a bounded
decision-search route with source-note verification and explicit handoff when a
record is missing or stale.

## Why this is not just the technique

The technique explains source-of-truth layout. The skill adds the operational
steps for using the workspace decision graph, ranking decision matches, checking
source notes, and routing to create or correct only when lookup is insufficient.

## Adjacent skills considered

- `aoa-decision`
- `aoa-decision-create`
- `aoa-decision-correct`
- `aoa-source-of-truth-check`

## Recommendation

- `keep_exception`
