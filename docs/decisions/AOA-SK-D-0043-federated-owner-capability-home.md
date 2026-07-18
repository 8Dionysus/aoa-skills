# Federated Owner Capability Home

- Decision ID: AOA-SK-D-0043
- Status: Accepted
- Date: 2026-07-18
- Owner surface: `schemas/capability-home-port.schema.json`,
  `schemas/capability_family.schema.json`, `scripts/skill_model/`, and
  `docs/CAPABILITY_HOME_PORT.md`

## Index Metadata

- Original date: 2026-07-18
- Surface classes: root/topology, skill source, generated/readout, export/runtime, owner boundary, validation guard
- Skill lanes: repository-home, portable/export
- Mechanic parents: release-support, cross-mechanic
- Guard families: source topology, generated/read-model, owner boundary, export/runtime, evaluation/public surface
- Posture: accepted federated owner capability home

## Context

The shared semantic capability system could describe `aoa-skills` itself, and
the skill home port could expose callable bundles from another repository.
An owner repository still lacked a common way to publish its complete
capability contracts without copying procedure truth into `aoa-skills` or
inventing a local tree, relation, retrieval, and task-DAG standard.

Large owner libraries also need a stronger separation between the tiny
prompt-visible router set and deep contract retrieval. Treating every node as
one flat document would reintroduce the routing interference that the
capability system is intended to control.

## Options Considered

- Copy each owner's capability definitions into the global `aoa-skills` tree.
- Let every owner invent its own graph, generated router, and composition
  packet.
- Define one shared owner-port grammar and validator while leaving each
  repository's nodes, procedures, lifecycle, and evidence with that owner.

## Decision

Choose the third option.

1. `capabilities/port.manifest.json` federates one owner-local root beneath one
   shared parent without copying either side.
2. The owner repository keeps authored node, relation, package, lifecycle, and
   procedure truth in `capabilities/families/*.yaml` and `skills/`.
3. `aoa-skills` owns the common schema, validator, deterministic graph/router
   builder, two-stage discovery, and `aoa-task-local-dag-v2` representation.
4. Initial discovery reads only advertised router descriptions. Full contract
   and package reranking begins only after the owner is admitted.
5. Generated graphs record source and shared-contract fingerprints but remain
   non-authoritative read models.
6. Task-local DAGs are ephemeral execution packets. A stable repeated sequence
   requires separate owner admission before it becomes a playbook.
7. Package scans cover the full regular-file closure, host-path leakage,
   transient or symlink residue, explicit mutations, network/install commands,
   declared permissions, and recovery contracts. Runtime and tool policy
   remain stronger than skill text.
8. Structural validation cannot promote a skill. Owner-local eval ports carry
   cases and execution metadata; `aoa-evals` retains benefit and promotion
   verdict authority.

## Rationale

One shared grammar makes cross-owner routing and composition inspectable
without moving semantic ownership. Two-stage retrieval preserves rare
capabilities without placing every contract in initial context. Typed ABI,
effects, conflicts, versions, verification relations, and blockers make a
planned composition explainable, while the transient DAG/playbook boundary
prevents one successful trace from becoming doctrine.

## Consequences

- Positive: owner repositories can expose complete capability truth through
  one validated, reproducible contract.
- Positive: prompt-visible routing remains bounded while deep retrieval can
  use full package and relation evidence.
- Tradeoff: an owner CI lane needs a compatible `aoa-skills` checkout and must
  rebuild projections after either owner source or shared-contract changes.
- Tradeoff: graph and package fingerprints prove identity and drift, not
  behavioral equivalence across runtimes.
- Follow-up: exercise the first owner port through source, portable,
  installed-runtime, collision, composition, and controlled comparison lanes
  before any experimental lifecycle promotion.

## Current Applicability

As of 2026-07-18, the contract supports one owner manifest, deterministic
graph and router outputs, full skill contracts, package provenance,
two-stage discovery, legacy DAG v1 reads, and DAG v2 planning with stages,
checkpoints, blockers, and terminal conditions.

## Boundaries

Do not infer that an owner manifest admits every leaf as a callable skill, that
a graph relation authorizes execution, that a matching package digest proves
cross-runtime behavior, that a generated DAG is a playbook, or that a green
validator establishes outcome lift or safety.

## Validation

- Validate both schemas with Draft 2020-12.
- Run capability-system and owner-port focused tests.
- Build and check one real owner graph and router from its canonical sources.
- Exercise positive, negative, collision, ABI, conflict, version, verification,
  and prompt-budget cases.
- Run source-fast, generated, export, release, and decision-index parity before
  landing.
