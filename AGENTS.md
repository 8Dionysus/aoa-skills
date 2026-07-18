# AGENTS.md

## Applies to

This card applies to the whole repository unless a nearer `AGENTS.md` narrows
the lane.

## Role

`aoa-skills` owns the shared AoA capability contract, the shared navigation
root, and the small set of portable shared bundles that are independently
callable by an agent host. Repository-specific callable procedures remain
authored by their repository owner and are federated without being copied here.

## Read before editing

Read this card, then the nearest nested card. For semantic or structural work
read `CHARTER.md`, `DESIGN.md`, `capabilities/README.md`, and the affected
family source. For bundle work also read `skills/README.md` and the target
`SKILL.md`. For generated, release, KAG, quest, or decision work, read that
surface's own card and README.

## Boundaries

- `capabilities/` owns shared semantic nodes, one-parent navigation, typed
  relations, ABI, binding, lifecycle, compatibility, and evidence posture;
  external owner nodes remain owner-qualified references.
- `skills/` owns the admitted shared portable callable bundles; a capability, mode,
  external adapter, or repository-local procedure is not automatically a
  bundle here.
- A sibling `skills/` home owns only that repository's admitted callable
  procedures. Its host projections remain derived from that owner source.
- `generated/`, explicit external portable assemblies, and `kag/` are derived
  projections and never outrank authored sources. This repository's own
  `.agents/skills/` remains absent.
- Techniques may be optional provenance, never an execution dependency.
- Workflow, tool, guard, role, runtime, proof, memory, routing, KAG, and
  project truth remain with their named owners.
- Task-local DAGs and raw trial traces belong to the current session or runtime,
  not to repository source.

## Validation

Manual trials are primary evidence for usefulness and behavior. Repository
checks protect only durable structural, ABI, export, and packaging invariants.
Use the command sequences in `config/validation_lanes.json`; the normal bounded
check is `PYTHONPATH=scripts python scripts/lanes/ci_gate.py --mode source-fast`.

## Closeout

Report authored sources changed, manual cases exercised, derived surfaces
rebuilt, checks run, checks skipped, unresolved owner or runtime evidence, and
any session-only artifacts removed. Do not call a green validator proof that a
skill improves outcomes.

## Route map

| Need | Owner surface |
| --- | --- |
| repository authority | `CHARTER.md` |
| capability architecture | `DESIGN.md`, `capabilities/README.md` |
| callable procedure | `skills/README.md`, target `SKILL.md` |
| generated projection | `generated/AGENTS.md` |
| portable handoff | `mechanics/release-support/AGENTS.md` |
| local KAG packet | `kag/AGENTS.md` |
| durable obligation | `mechanics/questbook/AGENTS.md`, `QUESTBOOK.md` |
| repository decision | `docs/decisions/AGENTS.md` |
| validation command | `config/validation_lanes.json` |

## Source law

Edit the owner source first, then rebuild its projections. Never hand-edit a
generated repository index, portable export, or derived catalog to conceal
source drift. External bindings must identify the owner and remain unbound when
the owner route or required tool cannot be verified.

## Decision and landing

Record a decision when future maintainers need the rationale for a durable
ownership, topology, lifecycle, or compatibility choice. When landing is
requested, use an isolated branch, commit the intended diff, open a PR, wait
for required checks, merge through GitHub, and verify the resulting main branch.
