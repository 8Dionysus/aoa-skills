# AGENTS.md

## Applies to

This card applies to `aoa-skills/kag/` and every nested path until a nearer card
narrows the lane.

## Role

`kag/` is the derived, source-linked provider packet for the `aoa-skills`
semantic capability system. It exposes capability and callable-bundle handles
to `aoa-kag`; it does not own skill meaning, retrieval policy, or runtime state.

## Read before editing

Inspect `kag/manifest.json`, affected records, and owner sources. Use the KAG
README only for provider topology; capability or skill READMEs only when their
source claims change.

## Boundaries

- `capabilities/` owns capability semantics, relations, compatibility, and bundle bindings.
- `skills/` owns nine shared callable source bundles; seven are advertised and
  two remain deferred for explicit research or compatibility use.
- `aoa-kag` owns the shared local-KAG schemas, index generator, registry, retrieval, and composition.
- Runtime graph, vector, cache, and MCP serving state stay with their runtime owners.
- Never reconstruct a retired skill or technique ontology inside this derived packet.

## Validation

Validate capability sources and generated parity first. Generate and validate
the repository index family with the pinned `aoa-kag` owner tools. Do not
hand-edit generated repository indexes.

## Closeout

Report the provider records, source-return routes, capability parity, KAG index
family validation, and the consumer route exercised.
