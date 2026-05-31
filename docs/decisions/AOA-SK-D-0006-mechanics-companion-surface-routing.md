# Mechanics Companion Surface Routing

- Decision ID: AOA-SK-D-0006

## Index Metadata

- Original date: 2026-05-06
- Surface classes: root/topology, mechanic package, generated/readout
- Skill lanes: none
- Mechanic parents: cross-mechanic
- Guard families: source topology, generated/read-model
- Posture: accepted companion surface routing

Date: 2026-05-06

## Context

After the first mechanics rehome, root companion districts still carried
mechanic-owned files: schema-backed examples, Agon seed configs, recurrence
manifests, hook bindings, and flat quest source files.

AoA already separates these concerns:

- root `generated/` may publish repo-wide or root-readable derived surfaces
- root `examples/` is only for root-owned examples
- manifest records live with the owning mechanic or part
- quest sources use lane-first lifecycle paths
- mechanic-local seed configs live with the owning mechanic or part

## Decision

Route mechanic-owned companion surfaces to their owning homes:

- Agon candidate seed configs to the owning Agon parts
- Agon examples to `mechanics/agon/examples/`
- MCP/OpenAI scaffold examples to `mechanics/boundary-bridge/examples/`
- checkpoint examples to `mechanics/checkpoint/examples/`
- Experience contract examples to `mechanics/experience/examples/`
- session-growth artifact examples to `mechanics/growth-cycle/examples/`
- method-growth adoption and owner-landing examples to `mechanics/method-growth/examples/`
- recurrence records to `mechanics/recurrence/manifests/`
- Agon recurrence records to `mechanics/agon/parts/recurrence-observation/manifests/`
- release-support examples to `mechanics/release-support/examples/`
- quest source files to `quests/<lane>/<state>/`

Keep root `generated/` as the repo-wide derived publication district, and keep
root `config/` and `schemas/` only for shared repo-wide contracts.

## Rationale

The move keeps authored companion data close to the mechanic that owns its
meaning while preserving root districts for repo-wide routing and publication.
It prevents examples, configs, manifests, and quests from becoming a flat
miscellaneous layer that future agents must rediscover by filename.

## Consequences

- Builders, validators, release checks, tests, and generated quest read models
  must use the new owner paths.
- Root `examples/` and `manifests/` now act as route districts rather than
  storage for mechanic records.
- Future examples and manifests should start at the owner package and move to
  root only when they are genuinely root-owned or root-published derived output.
