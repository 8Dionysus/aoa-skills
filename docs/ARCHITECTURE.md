# Architecture

## Semantic plane

`capabilities/families/*.yaml` forms the shared semantic tree with one primary
parent per node and a typed graph across nodes. Repository owners may provide
home-skill sources that join the federated tree without moving procedure truth
here. The graph distinguishes capabilities, skills, modes, workflows, tools,
guards, adapters, and human gates. Executable nodes carry applicability, ABI,
binding, execution, verification, trust, provenance, lifecycle, and failure
contracts.

## Procedural plane

Seven `aoa-skills/skills/**/SKILL.md` bundles are the current shared callable
procedures. Internal modes stay inside those bundles. An owner repository may
add a home bundle only after manual admission; its canonical source remains in
that repository. External workflows and tools remain owner-qualified graph
bindings. Only shared `aoa-decision` is advertised; the other six shared
bundles are explicit deferred candidates.

## Target derived plane

- `generated/capability_graph.*` supports deep retrieval and composition.
- `user-default` carries one advertised shared bundle at the standard Codex
  user root; installation and fresh-session visibility remain host evidence,
  not consequences of declaring the profile.
- `os-user-default` may select admitted owner-home bundles into the same
  globally discoverable user catalog while truth stays under each owner's
  `skills/` home.
- repository `.agents/skills/*` is reserved for repository-only procedures and
  must not duplicate a bundle selected by the OS user profile. The old
  owner-home repository projection remains v1 migration compatibility only.
- `kag/` exposes source-linked graph and return handles to `aoa-kag`.
- release manifests bind source and portable hashes for pack handoff.

Derived planes never own semantics. They are reproducible from authored source.

## Execution plane

For one request, discovery selects the smallest applicable compatible set and
`scripts/runtime/capability_dag.py` constructs a task-local DAG from ABI and
control relations. The DAG is session/runtime state. Conflicts, missing inputs,
or unavailable external bindings block honestly rather than being guessed.

## Evidence plane

Manual trials compare no skill, current, and candidate behavior, including
negative and coexistence cases. Raw traces remain in the session. Only reviewed
durable contracts, lifecycle decisions, and stable invariants return to the
repository. Shared proof remains with `aoa-evals`.
