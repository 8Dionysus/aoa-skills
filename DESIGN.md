# Capability Ecosystem Design

## Core model

AoA uses three distinct structures across shared and repository-owned sources:

1. A semantic tree makes capabilities discoverable. Each node has one
   `primary_parent`.
2. Typed relations form a graph for requirements, inputs, outputs,
   compatibility, alternatives, handoffs, conflicts, adaptation, and
   supersession.
3. A task-local DAG selects and orders the smallest compatible executable set
   for one request.

Each authored node has exactly one owner. The tree and graph may be federated
deterministic projections of those owner sources. The task-local DAG is
session/runtime state and is not committed as skill truth.

## Object kinds

The graph distinguishes `capability`, `skill`, `mode`, `workflow`, `tool`,
`guard`, `adapter`, and `human-gate`. Only an independently callable portable
procedure is a `skill`. Other objects keep owner-qualified bindings and may be
composed without becoming host-visible bundles.

## Executable contract

An executable node states:

- identity, owner, applicability, and negative applicability;
- input and output ABI;
- binding kind, operation, and availability;
- execution freedom, tool requirements, verification, termination, effects,
  reversibility, and failure modes;
- trust, provenance, lifecycle, visibility, evidence, and health;
- typed relations to other nodes.

Missing owner truth or unavailable requirements produce an explicit unbound or
blocked result. The planner never invents a substitute binding.

## Callable bundle threshold

A mode or capability becomes a separate bundle only after evidence shows all
of the following:

- a stable independent trigger;
- a distinct input/output ABI;
- useful independent composition;
- measurable benefit over no-skill and the containing bundle;
- acceptable coexistence with the visible library.

Otherwise it remains an internal mode or graph node. Consolidation follows the
same rule in reverse and requires held-out equivalence, not aesthetic symmetry.

## Shared and home skill sources

`aoa-skills/skills/` owns reusable shared procedures. A repository may create a
top-level `skills/` home only when at least one repository-specific procedure
passes the callable bundle threshold. Empty ports and copied shared catalogs
are not part of the topology.

The repository owner keeps admission, procedure meaning, local ABI adaptation,
lifecycle, and evidence posture. `aoa-skills` owns the shared compatibility and
projection grammar; `aoa-kag` may federate owner metadata and relations without
copying or overriding the procedure. Tools, guards, playbooks, adapters, and
repository facts stay in their stronger owner surfaces unless independent
skill value is demonstrated.

## Discovery and execution

Host-visible descriptions are a small first-pass index. Deep retrieval may use
the full capability contract and graph. Retrieval ranks applicability before
topical similarity and checks set compatibility before DAG construction.
Execution follows data and control edges, preserves owner boundaries, and stops
on conflicts or missing required inputs.

## Evidence and lifecycle loop

The loop is:

`observe real work -> form candidate -> run manual comparison -> attribute the
effect -> revise or reject -> preserve durable invariants -> monitor drift`.

Trials compare no skill, current bundle, and candidate; direct provision and
retrieval; isolated and coexistence use; flat selection and task-local DAG.
Model, host, tools, source revision, context, effects, artifacts, time, and
token cost are recorded when available. Promotion requires useful transfer to
held-out cases. Safety and refusal behavior are tested separately.

## Source and projections

| Layer | Surface |
| --- | --- |
| authored semantics | `capabilities/families/*.yaml` |
| shared callable procedures | `aoa-skills/skills/**/SKILL.md` |
| repository-owned callable procedures | `<owner-repo>/skills/**/SKILL.md` when admitted |
| migration disposition | `capabilities/legacy-skill-migration.yaml` |
| deterministic graph | `generated/capability_graph.*` |
| target user shared host profile | one host-selected user skill root after declared, built, installed, and fresh-session inspected |
| repository host bundles | `<owner-repo>/.agents/skills/*`, derived only from that owner home |
| workspace-root host bundles | workspace-owned procedures only, otherwise empty |
| KAG return map | `kag/` |
| per-task plan and raw trials | session/runtime only |

Technique references are optional lineage. No build, export, discovery,
planning, or execution path may require `aoa-techniques`.
