# Semantic Capability Ecosystem

- Decision ID: AOA-SK-D-0039
- Status: Accepted
- Date: 2026-07-15
- Owner surface: `capabilities/`, `skills/`, `config/`, `mechanics/`, `evals/`,
  `kag/`, and their deterministic projections

## Index Metadata

- Original date: 2026-07-15
- Surface classes: root/topology, skill source, generated/readout, export/runtime, review/governance, validation guard, memory/writeback, mechanic package
- Skill lanes: core/engineering, core/session-growth, core/stewardship, portable/export
- Mechanic parents: agon, questbook, release-support, cross-mechanic
- Guard families: source topology, generated/read-model, export/runtime, release/tooling, questbook, memo writeback, evaluation/public surface
- Posture: accepted semantic capability ecosystem v2

## Context

The repository had grown to 57 separately routed skills plus technique
manifests, activation machinery, evaluation proxies, review readouts, mechanics,
and generated registries. Many leaf skills were actually modes of the same
procedure. Their descriptions competed for limited discovery context, several
validators protected retired topology rather than behavior, and mandatory
technique lineage made a portable procedure depend on a sibling representation.

The required future shape is an agent-OS capability ecosystem: discovery must
stay small, composition must preserve real input/output and compatibility
relations, effects must remain owner-scoped, and a skill must earn its place by
improving held-out work rather than by passing structural checks. Session-memory
systems may provide candidate evidence, but their availability and quality
cannot be a runtime prerequisite for the skill layer.

## Options Considered

- Repair all 57 bundles in place, retain technique manifests, and strengthen
  their routers and validators.
- Replace the catalog with a few broad monolithic skills and encode all routing
  in prose.
- Model a semantic capability tree plus typed cross-relations, expose only
  independently callable bundles, and assemble a task-local DAG for execution.

## Decision

Choose the third option.

1. `capabilities/families/*.yaml` owns the semantic capability tree. Every node
   has one primary parent for navigation; typed relations carry requirements,
   products, composition, handoff, alternatives, conflicts, adaptation, and
   supersession.
2. A task selects the smallest compatible capability set and assembles a
   task-local DAG from declared inputs, outputs, effects, tools, and relations.
   The DAG is runtime/session state and is never committed as repository truth.
3. `skills/**/SKILL.md` exists only for independently callable procedural
   bundles. The initial source surface is seven bundles: `aoa-decision` is
   advertised; engineering-shape, eval, verification, knowledge-stewardship,
   session-harvest, and session-recovery remain deferred until held-out manual
   evidence justifies wider discovery.
4. The former 57 skills are accounted for in
   `capabilities/legacy-skill-migration.yaml` as absorbed modes, aliases,
   external owner routes, or retired behavior. Compatibility names aid search;
   they do not recreate callable child bundles.
5. Technique references are optional provenance only. No source build, export,
   discovery, planning, or execution contract may require `aoa-techniques` or
   a `techniques.yaml` file.
6. Skills own procedures; MCP and runtime owners provide live actions/data;
   playbooks own stabilized multi-step workflows. Portable `.agents/skills/*`
   stays a flat generated host projection, while KAG stays a derived discovery
   and return map.
7. Manual comparison is the behavioral authority: no skill, current skill,
   candidate/composition, direct versus retrieval, positive versus negative,
   isolated versus coexistence, and flat selection versus task-local DAG where
   relevant. Validators are admitted only for durable deterministic invariants
   observed through that work; a green result never promotes a capability.
8. Raw traces, one-session reports, task-local plans, and session identifiers
   remain session-owned. This repository keeps only reusable owner sources and
   owner-safe projections; it does not pre-create an empty local memo port.
9. Active mechanics are limited to Agon candidate intake, Questbook durable
   obligations, and release support. Agon requests enter as capability
   candidates, not presumptive skills. Other former mechanics remain in Git
   history unless a current independent owner contract re-establishes them.

## Rationale

The tree makes discovery explainable without exposing every atomic operation.
Typed relations preserve composition that a pure directory hierarchy cannot,
and a task-local DAG avoids turning one reusable sequence into a universal
workflow. Seven focused bundles keep portable discovery bounded while the
capability graph can still represent external tools, guards, workflows, human
gates, and internal modes without multiplying `SKILL.md` files.

Optional technique provenance preserves useful lineage without coupling skill
availability to a sibling repo. Manual-first lifecycle decisions prevent
structural tests, generated reports, or session-memory retrieval from becoming
surrogate outcome truth. Explicit owner and session boundaries keep the
repository durable and public-safe.

## Consequences

- Positive: discovery pressure falls from 57 competing bundles to one
  advertised front door plus six deliberate challengers.
- Positive: every former skill has an explicit destination; removed source is
  recoverable from Git history without active compatibility scaffolding.
- Positive: composition, conflicts, effects, provenance, lifecycle, and owner
  return routes are machine-readable without making the graph execution truth.
- Tradeoff: six bundles remain intentionally harder to discover until manual
  trials establish benefit and coexistence safety.
- Tradeoff: tree/graph/DAG parity and portable projection add deterministic
  maintenance work, but that work protects an actual cross-surface contract.
- Tradeoff: platform and model behavior must be rechecked; common Markdown
  format does not imply runtime parity.
- Follow-up: repeat clean-host and held-out manual trials after material model,
  host, owner-contract, or workflow drift; revise, promote, split, merge,
  demote, or remove candidates only when new evidence changes the disposition.

## Supersession Map

- This decision supersedes the active topology portions of AOA-SK-D-0015,
  AOA-SK-D-0019, AOA-SK-D-0021, AOA-SK-D-0022, AOA-SK-D-0023,
  AOA-SK-D-0026, AOA-SK-D-0036, AOA-SK-D-0037, and AOA-SK-D-0038.
- It revises the concrete lane, validator, test, and script inventories of
  AOA-SK-D-0028 through AOA-SK-D-0031 while preserving their source/derived and
  single-command-authority principles.
- It absorbs the callable child-chain implementation of AOA-SK-D-0034 and
  AOA-SK-D-0035 into the `aoa-decision` family while preserving authored
  decision records as authority and graph lookup as a bounded aid.
- AOA-SK-D-0017's requirement for lived-use evidence remains valid, now under
  the stricter manual baseline/challenger and held-out lifecycle rule.

## Current Applicability

As of 2026-07-15, the authored tree contains ten families and 87 nodes. Seven
source bundles exist. Held-out manual comparison retained `aoa-decision` as the
single advertised challenger because its record/correct modes prevented errors
seen without the skill; the other six produced no necessary outcome lift and
remain evaluated, degraded, and deferred. The old source bundles, mandatory
technique bridge, old eval/stat proxies, Spark lane, obsolete mechanics,
inherited review records, and repo-local memo candidate port have left the
active tree.

## Boundaries

This decision does not prove that any deferred bundle improves outcomes, make
KAG or a generated graph authoritative, turn an alias into a callable skill,
grant MCP/tool permissions, move workflow ownership into a skill, or allow
session evidence to be committed as owner truth. It does not require every
capability node to become a skill.

## Validation

- Manually inspect the exact 57-entry migration and the seven source procedures.
- Build and validate the capability graph, portable export, Questbook, Agon
  candidate projections, decision indexes, and both install profiles.
- Exercise positive, negative, coexistence, direct/retrieved, and composed cases
  in clean prompt-visible sessions before any lifecycle promotion.
- Validate the repo-local KAG family through the `aoa-kag` owner generator and
  validator after all authored sources are staged.
- Inspect the final tree and diff for stale paths, session identifiers,
  mandatory technique dependencies, temporary artifacts, and deleted-owner
  scaffolding.
