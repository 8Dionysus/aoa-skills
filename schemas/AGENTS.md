# AGENTS.md

## Applies to

This card applies to `schemas/`.

## Role

`schemas/` owns shared machine shape for capability sources, graph and DAG
projections, skill frontmatter, migration, and release manifests.

## Read before editing

Inspect the schema, semantic owner, producers, and consumers. Use the README
only to select a contract or change the human catalog.

## Boundaries

Schema edits are contract edits. Preserve `$schema` and stable `$id` where
present, keep compatibility deliberate, and never loosen a contract merely to
make invalid source green. Schemas constrain shape; owner docs own meaning.

## Validation

Run producers, consumers, negative manual cases, and focused tests for the
changed boundary before the wider lane.

## Closeout

Report compatibility, producers/consumers checked, negative case, generated
refresh, and any migration requirement.
