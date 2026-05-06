# Mechanics Antifragility Risk Posture

Date: 2026-05-06

Status: accepted

## Context

Three antifragility-shaped docs remained flat in `docs/`: fallback authoring
guidance, via negativa pruning, and collision stress guidance. Direct reading
showed they are active mechanics guidance, not skill bundle meaning. They
describe how risk, stress, pruning, and collision pressure should move around
skill canon while leaving `SKILL.md`, generated evals, risk rings, runtime
guardrails, and owner-local execution in their own homes.

`Agents-of-Abyss` owns center antifragility doctrine. `aoa-techniques` has a
thinner antifragility package for stress-recovery practice pressure. The
`aoa-skills` slice needed an even narrower local package for skill-layer risk
posture.

## Decision

Create `mechanics/antifragility/` and land only the fallback/pruning/collision
slice:

- `docs/ANTIFRAGILITY_SKILL_ADDENDUM.md` -> `mechanics/antifragility/parts/fallback-authoring-posture/README.md`
- `docs/VIA_NEGATIVA_CHECKLIST.md` -> `mechanics/antifragility/parts/via-negativa-pruning/README.md`
- `docs/SKILL_COLLISION_CHAOS_WAVE1.md` -> `mechanics/antifragility/parts/collision-stress-program/README.md`

Add a package card, direction, parts, provenance, landing log, roadmap, and
active parts.

Keep `docs/ROLLBACK_DRILL_SKILL.md` in place because its own text routes to the
v1.0 installation and first sovereign release wave. A later release-support or
experience pass should decide its honest home.

## Consequences

- Flat `docs/` no longer owns fallback, via negativa, or collision-stress
  movement guidance.
- Antifragility remains below canonical skill meaning and below owner-local
  rollback or cleanup execution.
- Generated collision, description, tiny-router, and risk-ring surfaces remain
  evidence or generated companions, not source truth.
- Rollback drill remains an explicit later pressure, not a forced member of the
  antifragility package.

## Verification

Verify with:

```bash
python -m pytest -q tests/test_mechanics_topology.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py
python scripts/lint_trigger_evals.py --repo-root .
python scripts/lint_description_trigger_evals.py --repo-root .
python scripts/validate_tiny_router_inputs.py --repo-root .
python scripts/validate_nested_agents.py
```
