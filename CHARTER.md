# aoa-skills Charter

## Mission

`aoa-skills` turns demonstrated, reusable agent practice into a navigable
capability ecosystem and a deliberately small set of portable procedures.
Its purpose is better selection and execution, not a larger catalog.

## What this repository owns

- authored capability families, contracts, lifecycle, compatibility, and
  relations under `capabilities/`;
- the source wording and support resources of independently callable bundles
  under `skills/`;
- deterministic projections, portable export, pack handoff, and owner-local
  validation of those sources;
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
| shared routing and SDK contracts | `aoa-routing`, `aoa-sdk` |

An external object may be referenced by an owner-qualified binding. That route
does not transfer its authority here.

## Authority order

1. Authored capability and skill sources.
2. Owner-qualified external contracts for external bindings.
3. Deterministic generated projections.
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
