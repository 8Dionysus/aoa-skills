# AGENTS.md

## Applies to

This card applies to `scripts/`.

## Role

`scripts/` owns deterministic source models, builders, validators, task-DAG
planning, portable handoff, decision indexes, Questbook read models, and lane
orchestration.

## Read before editing

Read root `AGENTS.md`, the owning source/config/schema, all direct callers, and
focused tests. For command ordering read `config/validation_lanes.json`.

## Boundaries

Scripts remain repository-relative, deterministic where declared, explicit
about effects, and honest about source versus derived authority. Do not encode
outcome quality as a structural proxy, preserve retired ontology through
compatibility code, or read session evidence as repository truth.

## Validation

Run the script directly on a manual positive and negative case, then focused
tests and the narrowest lane that uses it. Builders must support deterministic
parity where their output is committed.

## Closeout

Report callers and outputs changed, manual cases, deterministic parity, tests,
effects, and obsolete helpers removed.
