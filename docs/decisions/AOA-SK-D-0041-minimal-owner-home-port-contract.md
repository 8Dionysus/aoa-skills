# Minimal Owner Home Port Contract

- Decision ID: AOA-SK-D-0041
- Status: Partially superseded by AOA-SK-D-0042
- Date: 2026-07-15
- Owner surface: `schemas/skill-home-port.schema.json`,
  `docs/HOME_SKILL_PORT.md`, and owner projection scripts

## Index Metadata

- Original date: 2026-07-15
- Surface classes: skill source, export/runtime, owner boundary, validation
- Skill lanes: repository-home, portable/export
- Mechanic parents: cross-mechanic
- Guard families: source topology, owner boundary, export/runtime, manual admission
- Posture: accepted minimal owner-home port

## Context

AOA-SK-D-0040 established that repository-specific callable procedures stay
with their named owner and that `.agents/skills` is a derived repository
projection. It intentionally did not create a port before a real owner family
proved the need.

The first owner-by-owner manual pilot used `aoa-stats`. Bounded answer,
diagnosis, evolution, held-out lifecycle, committed-versus-live, negative, and
coexistence cases supported one three-mode owner bundle. The same work exposed
25 copied legacy shared bundles in that repository. The repeated source,
projection, cleanup, and CI need is durable, while the trial traces themselves
remain session evidence.

## Options Considered

- Let every owner invent its own home manifest and copy procedure files into
  host directories manually.
- Place all repository procedures back in `aoa-skills` so the existing shared
  exporter can distribute them.
- Define one narrow common port and deterministic repo projection contract,
  while leaving admission and procedure truth with each owner.

## Decision

Choose the third option.

1. An admitted owner home uses canonical `skills/<bundle-name>/` sources and a
   non-empty `skills/port.manifest.json` containing only prompt-advertised
   bundles. Deferred or explicit-only candidates remain outside the port.
2. The owner manifest names the repository authority and an owner-held
   admission decision for every bundle.
3. The only standard owner projection is an exact generated copy at
   `.agents/skills`; it contains the full declared home and no undeclared
   shared or legacy bundle.
4. Projection preview and drift checks are read-only. Writing requires
   explicit execution; deleting undeclared entries requires separate explicit
   prune intent. Declared payloads are staged and compared before pruning
   begins.
5. The permanent validator and focused test protect path containment without
   symlink indirection, regular owned payload, manifest/source identity, and
   byte plus executable-bit parity. They never decide usefulness or lifecycle.
6. Empty ports, candidate scaffolds, raw trials, task-local DAGs, and
   repository-independent shared copies are outside this contract.

## Rationale

The port is small enough to preserve one owner and one reproducible host copy
without becoming a second semantic platform. Explicit pruning makes the
destructive migration boundary reviewable. Requiring owner admission before
the manifest prevents structural tooling from manufacturing a skill ecosystem
whose only evidence is a green schema check.

The manual pilot justifies preserving the repeated structural invariant, not
encoding the pilot's model judgments as fixtures or scores.

## Consequences

- Positive: owner procedure truth and Codex discovery no longer require the
  same directory to be authoritative.
- Positive: copied shared catalogs can be removed with an inspectable,
  deterministic replacement.
- Positive: sibling CI can pin one common structural contract.
- Tradeoff: source and projection are intentionally duplicated bytes because
  repository discovery cannot rely on a parent workspace path.
- Tradeoff: each owner must maintain its own admission rationale and rerun
  semantic trials; the common validator cannot do that work.
- Follow-up: land the `aoa-stats` owner bundle as the first consumer, then use
  later owner audits rather than directory symmetry to admit further homes.

## Current Applicability

As of 2026-07-15, the common contract is ready for its first owner consumer.
It does not itself admit `aoa-stats` or any other sibling bundle. The existing
legacy sibling projections remain migration debt until their owners are
handled through clean branches and reviewed landings.

The admission, source-shape, containment, and package-residue rules remain
active. AOA-SK-D-0042 supersedes the v1 repository projection as the target:
v1 is now migration compatibility, and new admitted owner homes declare v2
OS-user exposure without a same-name repository copy.

## Boundaries

Do not infer cross-host behavioral parity, agent improvement, routing quality,
security, freshness, or KAG federation from structural parity. Do not add an
owner manifest merely to satisfy topology symmetry. The owner repository, not
this decision, controls bundle meaning and admission.

## Validation

- Reproduce missing projection, source drift, undeclared legacy entry,
  explicit prune, transient residue, and symlink rejection manually.
- Run the focused durable test only after that reproduction.
- Validate the schema, script and validator inventories, decision indexes,
  source-fast lane, and full repository tests.
