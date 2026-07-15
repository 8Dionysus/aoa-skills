# Owner Skill Homes And Projection Boundaries

- Decision ID: AOA-SK-D-0040
- Status: Accepted
- Date: 2026-07-15
- Owner surface: `CHARTER.md`, `DESIGN.md`, `capabilities/`, `skills/`, and host projection contracts

## Index Metadata

- Original date: 2026-07-15
- Surface classes: root/topology, skill source, export/runtime, generated/readout, owner boundary
- Skill lanes: shared, repository-home, portable/export
- Mechanic parents: release-support, cross-mechanic
- Guard families: source topology, owner boundary, export/runtime, generated/read-model, manual admission
- Posture: accepted owner-skill federation

## Context

AOA-SK-D-0039 reduced the central catalog to seven shared bundles and separated
skills from modes, tools, guards, workflows, and adapters. The sibling
workspace still carried copies of the former shared catalog under repository
`.agents/skills/` trees and the workspace root. At the same time, real
repository-specific procedures had no canonical home distinct from plugin or
host packaging.

Live Codex inspection showed that the copies still enter prompt-visible skill
lists, compete with the new shared profile, and can expose two different
bundles with the same name. A workspace-root projection alone is insufficient
inside a child Git repository because repository discovery stops at that
repository root.

## Options Considered

- Keep `aoa-skills` as the source for every shared and project-specific bundle,
  then copy selected bundles into every repository and the workspace root.
- Keep one complete workspace-root projection and remove user and repository
  installs.
- Keep shared procedures in `aoa-skills`, keep repository-specific procedures
  in admitted owner-local homes, and derive one non-overlapping projection per
  actual host scope while federating metadata through KAG.

## Decision

Choose the third option.

1. `aoa-skills/skills/` is the canonical source only for shared portable AoA
   procedures and owns the common compatibility and projection contract.
2. The named repository owner admits a top-level `skills/` home only after at
   least one local procedure demonstrates a stable trigger, distinct ABI,
   independent composition value, held-out benefit, and acceptable
   coexistence. Empty ports and copied shared catalogs are forbidden.
3. A repository home owns its procedure meaning, repository adaptation,
   lifecycle, and evidence posture. `aoa-skills` may keep an owner-qualified
   route but not a second authored copy of the home contract.
4. One host-selected user skill root carries the advertised shared profile.
   Runtime location is verified from the active host rather than inferred from
   a generic path convention.
5. `<owner-repo>/.agents/skills/` is a derived host projection only for that
   repository's advertised home bundles. It must not contain the shared global
   catalog.
6. The workspace-root `.agents/skills/` contains only workspace-owned
   procedures, or remains empty. It is not a substitute for the user profile
   and does not duplicate shared names.
7. Plugin, Claude, Gemini, or other host packages are consumer-driven derived
   projections. A plugin may distribute owner sources but never become their
   only accidental authoring home.
8. `aoa-kag` federates owner metadata, provenance, and typed relations into a
   discoverable graph. It does not copy procedure truth or become execution
   authority. Task-local DAGs and raw trials remain session/runtime artifacts.
9. Manual no-skill, current, candidate, negative, and coexistence trials precede
   durable test or validator additions. Permanent checks protect only stable
   projection, ownership, packaging, and ABI invariants observed through that
   work.

## Rationale

One owner per procedure prevents project facts and commands from drifting in a
central copy. A single shared user profile keeps common discovery available in
every repository without multiplying prompt-visible descriptions. Local host
projections preserve repository-specific affordances while semantic federation
allows tree discovery and DAG composition across owners.

Admission on evidence avoids turning directory symmetry into a new catalog
explosion. Consumer-driven projections preserve cross-host portability without
assuming identical prompt priority, validation, or invocation behavior.

## Consequences

- Positive: shared and home procedure truth have explicit, non-overlapping
  owners.
- Positive: stale shared copies can leave child repositories without hiding
  genuine local capabilities.
- Positive: KAG may federate a cross-repository skill ecosystem while every
  procedure remains returnable to its owner source.
- Tradeoff: bootstrap, SDK detection, KAG provenance, workspace installation,
  and existing plugin packages require a coordinated migration before old
  projections can be removed.
- Tradeoff: repositories without an admitted home procedure have no `skills/`
  directory, so visual symmetry is intentionally incomplete.
- Follow-up: run an owner-by-owner manual admission audit, pilot the smallest
  proven family, then introduce a minimal port/export contract from repeated
  need rather than in advance.

## Current Applicability

As of 2026-07-15, `aoa-skills` and the portable `aoa-session-memory`
repository provide real canonical skill homes. Workspace-local `.aoa/skills`
is an installed materialization of the latter and does not become a second
owner. The sibling repositories still carry legacy shared host copies, and
four launcher bundles remain nested inside an `8Dionysus` plugin pending owner
and admission review. The target shared user profile is not yet declared in
the profile config or proven installed by this decision. No additional
repository home is admitted by this decision.

## Boundaries

This decision does not declare every owner operation a skill, promote any
candidate, require an empty `skills/` port, make KAG authoritative, or prove
that a host projection behaves identically across runtimes. Tools, guards,
playbooks, adapters, facts, and ordinary repository instructions remain in
their stronger owner surfaces unless manual evidence establishes independent
skill value.

## Validation

- Inspect the shared source, existing owner homes, sibling projections, and
  host-visible prompt inventory manually.
- Regenerate decision indexes and validate current source/derived parity.
- Before removing legacy projections, migrate their named SDK, workspace, KAG,
  and plugin consumers and repeat clean user-root, workspace-root, and
  repository-root prompt inspection.
