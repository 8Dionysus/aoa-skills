# AGENTS.md

## Applies to

This card applies to `capabilities/` and its descendants.

## Role

`capabilities/` owns the authored semantic capability tree, typed execution
contracts, ABI declarations, lifecycle posture, and cross-object relations for
the AoA skill ecosystem. It distinguishes capabilities from skill bundles,
modes, workflows, tools, guards, adapters, evidence, and projections.

## Read before editing

Inspect the affected family YAML and referenced owner sources. Use
`capabilities/README.md` only for topology; open charter, design, or
architecture only when its contract changes.

## Boundaries

- A family record may route to another repository's object, but it must not
  copy or overrule that owner's procedure, policy, runtime state, or evidence.
- `skills/**/SKILL.md` remains the authored portable procedure for an
  independently callable bundle. A semantic capability or mode does not become
  a bundle merely because it appears in this tree.
- One `primary_parent` supplies navigation. All other structure uses typed
  relations; do not encode a second hidden taxonomy in tags or paths.
- Task-local DAGs are request/session artifacts. Do not commit an individual
  task plan as capability source truth.
- Technique references, when retained, are optional provenance only. They may
  not gate discovery, planning, export, or execution.

## Validation

Run the capability source validator and rebuild/check the derived capability
graph through their owning scripts. Then run the nearest owner checks for any
referenced bundle, workflow, tool, guard, or adapter whose source changed.

## Closeout

Report the families and object kinds changed, owner sources verified, graph and
DAG checks run, manual cases exercised, unresolved bindings, generated/KAG
refresh posture, and any task-local artifacts kept outside the repository.
