# Owner Request Receipts

Date: 2026-05-06

Status: accepted

## Context

`Agents-of-Abyss` owns the center owner-request queue for mechanic slices that
need stronger owner-local landing. Seven current requests name `aoa-skills` as
owner. After the first mechanics reformation, several requested skill-layer
surfaces had actually landed in `aoa-skills`, while others were only accepted
as future package pressure.

Leaving all seven center requests as `requested` would hide owner-local
progress. Marking all seven as `landed` would overclaim surfaces that still
need a package or normal skill review.

## Decision

Add `mechanics/OWNER_REQUEST_RECEIPTS.md` as the owner-local receipt surface for
AoA requests assigned to `aoa-skills`.

The receipt file separates:

- `landed` requests where owner-local surfaces now exist
- `accepted` requests where `aoa-skills` accepts the boundary but future
  package or skill work remains

The first receipt set treats Method-growth, Growth-cycle, Checkpoint, and RPG
as landed skill-layer slices. It treats Distillation, Experience, and Audit as
accepted but not landed.

## Consequences

- `aoa-skills` has one clear owner-local surface the AoA center queue can cite.
- The center can stop pretending all `aoa-skills` requests are still only
  requested.
- Accepted-but-not-landed work stays visible without being hidden in the center
  or promoted into canonical skills too early.
- Proof routes and public quality claims still belong to `aoa-evals`; this
  receipt is not proof.

## Verification

Verify with:

```bash
python -m pytest -q tests/test_mechanics_topology.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py
python scripts/validate_nested_agents.py
python scripts/build_catalog.py --check
python scripts/validate_skills.py --fail-on-review-truth-sync
```
