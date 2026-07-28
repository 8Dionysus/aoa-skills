# aoa-skills Charter

## Mission

`aoa-skills` turns demonstrated, reusable agent practice into a navigable
shared capability ecosystem and a deliberately small set of portable shared
procedures. It also defines how repository-owned skill homes join that
ecosystem without transferring their procedure truth here. Its purpose is
better selection and execution, not a larger central catalog.

## What this repository owns

- shared capability families, contracts, lifecycle, compatibility, relations,
  and owner-qualified external routes under `capabilities/`;
- the source wording and support resources of independently callable shared
  bundles under `skills/`;
- the shared compatibility and projection contract for repository-owned skill
  homes, while each repository owns admission of its procedures;
- deterministic projections, portable export, pack handoff, and owner-local
  validation of this repository's sources;
- the local KAG provider packet as a derived return map;
- repository decisions and durable obligations about this owner surface.

## What it does not own

| Truth | Owner |
| --- | --- |
| reusable methods or techniques | `aoa-techniques` when such provenance is useful |
| outcome proof and shared eval doctrine | `aoa-evals` |
| retrieval, federation, and KAG protocol | `aoa-kag` |
| session history or durable memory | `.aoa`, `aoa-session-memory`, `aoa-memo` |
| workflows and playbooks | `aoa-playbooks` |
| agent roles and progression | `aoa-agents` |
| runtime tools, services, state, and permissions | the named runtime or project owner |
| canonical routing and shared SDK contracts | `aoa-sdk` |
| repository-specific callable procedure truth | the named repository's admitted `skills/` home |
| cross-repository skill federation and retrieval | `aoa-kag` |

An external object may be referenced by an owner-qualified binding. That route
does not transfer its authority here.

## Authority order

1. The named owner's authored capability and skill sources.
2. Shared AoA capability contracts and owner-qualified external routes.
3. Deterministic generated or host projections.
4. Runtime/session evidence for the specific run.

Later layers may reveal drift or failure but do not silently rewrite earlier
owner truth. A proposed change returns to its owner and is admitted only after
review.

## Evidence posture

Manual held-out trials establish whether a bundle helps, harms, collides, or
adds no value. Tests and validators may preserve stable invariants discovered
there, but cannot substitute for outcome evidence. A successful final answer,
single trace, routing score, or green test is insufficient for promotion.

## Lifecycle posture

Every callable bundle and executable capability states its evidence and
visibility. Improvement, split, merge, demotion, supersession, or removal is a
normal lifecycle action. Only demonstrated independent trigger, ABI,
composition value, and outcome lift justify a new host-visible bundle.
