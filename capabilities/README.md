# Capability Ecosystem Source

This directory is the authored semantic map of AoA abilities. It answers two
questions that a directory of `SKILL.md` files cannot answer safely:

1. Which capability is relevant, and where does it sit in the navigation tree?
2. Which skill, mode, workflow, tool, guard, adapter, or human gate can realize
   it for this request?

The tree is for discovery. Typed relations describe compatibility and
composition. A task-local DAG is assembled only for the current request and is
not committed here.

## Source split

| Surface | Owns |
|---|---|
| `capabilities/families/*.yaml` | semantic nodes, one primary parent, ABI, typed relations, binding and lifecycle posture |
| `skills/**/SKILL.md` | portable instructions for independently callable bundles |
| sibling owner source | workflow, tool, guard, adapter, runtime, role, proof, memory, routing, or KAG truth |
| `generated/capability_graph.json` | deterministic derived graph and deep-retrieval document set |
| task-local DAG | current request plan; session/runtime artifact only |

An executable node must name exact applicability, ABI, binding, verification,
termination, effects, failure modes, trust, provenance, visibility, evidence,
and health. An external binding is only a source-linked route; it does not make
`aoa-skills` authoritative for the target object.

Technique lineage is optional provenance (`derived-from`, `informed-by`, or
`extracts-to`). No active capability may require a technique repository at
discovery, build, export, planning, or execution time.
