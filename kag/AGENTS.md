# AGENTS.md

## Applies to

This card applies to `aoa-skills/kag/` and every nested path until a nearer card
narrows the lane.

## Role

`kag/` is the derived, source-linked provider packet for the `aoa-skills`
semantic capability system. It exposes capability and callable-bundle handles
to `aoa-kag`; it does not own skill meaning, retrieval policy, or runtime state.

## Read before editing

Read the root `AGENTS.md`, this card, `kag/README.md`, `kag/manifest.json`,
`capabilities/README.md`, `generated/capability_graph.json`, and
`skills/README.md`.

## Boundaries

- `capabilities/` owns capability semantics, relations, compatibility, and bundle bindings.
- `skills/` owns the seven callable procedural bundles.
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
