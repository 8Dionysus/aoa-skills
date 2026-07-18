# Repository Capability Home Port

The capability home port lets a repository keep its own procedure and
capability truth while reusing the shared AoA grammar for semantic navigation,
typed relations, progressive disclosure, and task-local composition.

It complements the skill home port:

- `skills/port.manifest.json` names the small set of admitted callable
  packages that a runtime may advertise;
- `capabilities/port.manifest.json` names the complete owner-local capability
  source, federation parent, generated projections, and eval-port route;
- `capabilities/families/*.yaml` owns the repository's nodes and relations;
- `generated/capability_graph.json` and the generated router card are
  reproducible read models.

The graph is never procedure truth, runtime policy, execution evidence, or an
eval verdict.

## Owner contract

An owner port uses this shape:

```text
capabilities/
├── AGENTS.md
├── port.manifest.json
└── families/
    └── <owner-family>.yaml
skills/
├── port.manifest.json
└── <advertised-or-deferred-packages>/
generated/
├── capability_graph.json
└── capability_graph.md
```

Every executable skill node carries positive and negative applicability,
typed input and output ABI, procedure binding, freedom level, tools, runtime
requirements, verification, termination, effects, reversibility, failure
modes, trust, provenance, lifecycle, classification, and security posture.
Mutating nodes also carry preview, explicit-apply, recovery, and postcondition
contracts.

Every node has one primary navigation parent. Cross-tree reality belongs in
typed relations such as `requires`, `produces`, `consumes`, `hands-off-to`,
`conflicts-with`, `verifies`, `specializes`, `adapts`, `supersedes`, and
`incompatible-with-version`. The validator checks endpoints, inverses,
dependency cycles, ABI compatibility, package closure, and declared effects.

## Progressive discovery

Discovery is deliberately two-stage:

1. inspect only the compact descriptions of prompt-visible advertised
   routers;
2. after one owner is admitted, rerank that owner's full contracts and
   package text.

The result separates callable candidates from navigation branches. A generic
token occurring in a package id is not enough to bypass the first stage.
Increasing the deep candidate limit must not displace a valid callable leaf
with navigation-only nodes.

Use:

```bash
PYTHONPATH=scripts python scripts/capability_home.py \
  --owner-root /path/to/owner discover "bounded task"
```

## Task-local DAG

For a compound task, the planner selects the smallest named capability set,
checks hard dependencies, ABI flow, handoffs, verification relations,
conflicts, versions, permissions, and required inputs, then returns a
`aoa-task-local-dag-v2` packet.

The packet records ordered execution stages, typed edges, checkpoints,
blockers, the terminal contract, and the exact source-graph hash. It is
ephemeral runtime state. Repetition does not automatically turn it into a
skill or playbook; the playbook owner requires separate recurrence and
regression evidence.

Use:

```bash
PYTHONPATH=scripts python scripts/capability_home.py \
  --owner-root /path/to/owner plan \
  --capability skill.first --capability skill.second \
  --input artifact-type --permission read-owner-state
```

## Build and validation

From the matching `aoa-skills` checkout:

```bash
PYTHONPATH=scripts python scripts/validate_capability_home_port.py \
  --owner-root /path/to/owner
PYTHONPATH=scripts python scripts/build_capability_home_projection.py \
  --owner-root /path/to/owner
PYTHONPATH=scripts python scripts/build_capability_home_projection.py \
  --owner-root /path/to/owner --check
PYTHONPATH=scripts python scripts/validate_capability_home_port.py \
  --owner-root /path/to/owner --check-generated
```

The builder records source paths and hashes, shared schema and validator
fingerprints, package fingerprints, and one graph content hash. It excludes
its own generated router from the authored package fingerprint to avoid a
self-referential digest. Installed runtime package digests therefore remain a
separate identity dimension.

A green result proves contract and projection invariants only. It does not
prove discovery lift, procedure use, cross-runtime parity, safe behavior, or
benefit over no skill.
