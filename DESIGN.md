# Capability Ecosystem Design

## Core model

AoA uses three distinct structures:

1. A semantic tree makes capabilities discoverable. Each node has one
   `primary_parent`.
2. Typed relations form a graph for requirements, inputs, outputs,
   compatibility, alternatives, handoffs, conflicts, adaptation, and
   supersession.
3. A task-local DAG selects and orders the smallest compatible executable set
   for one request.

The tree and graph are repository source or deterministic projections. The
task-local DAG is session/runtime state and is not committed as skill truth.

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
| callable procedures | `skills/**/SKILL.md` |
| migration disposition | `capabilities/legacy-skill-migration.yaml` |
| deterministic graph | `generated/capability_graph.*` |
| portable host bundles | `.agents/skills/*` |
| KAG return map | `kag/` |
| per-task plan and raw trials | session/runtime only |

Technique references are optional lineage. No build, export, discovery,
planning, or execution path may require `aoa-techniques`.
