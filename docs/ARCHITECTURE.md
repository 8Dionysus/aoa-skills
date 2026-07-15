# Architecture

## Semantic plane

`capabilities/families/*.yaml` forms a semantic tree with one primary parent
per node and a typed graph across nodes. It distinguishes capabilities, skills,
modes, workflows, tools, guards, adapters, and human gates. Executable nodes
carry applicability, ABI, binding, execution, verification, trust, provenance,
lifecycle, and failure contracts.

## Procedural plane

Seven `skills/**/SKILL.md` bundles are the only current host-callable
procedures. Internal modes stay inside those bundles. External workflows and
tools remain owner-qualified graph bindings. Only `aoa-decision` is advertised;
the other six are explicit deferred candidates.

## Derived plane

- `generated/capability_graph.*` supports deep retrieval and composition.
- `.agents/skills/*` and agent catalogs are the flat portable host export.
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
