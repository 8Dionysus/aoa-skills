# Mechanics Recurrence Observation

Date: 2026-05-06

Status: accepted

## Context

After Questbook, Growth-cycle, Checkpoint, Method-growth, and Agon gained
package-local routes, two compact recurrence surfaces remained flat in
`docs/`. Direct reading showed they are not skill meaning and not generated
truth. They are active mechanics guidance for how skill activation pressure is
observed and closed as review decisions.

`Agents-of-Abyss` already owns recurrence law. `aoa-techniques` had already
landed a thin local recurrence package with the same two part shapes:
observation producers and review-decision closure. The `aoa-skills` route
needed the same discipline, translated to skill activation pressure rather
than copied as center authority.

## Decision

Create `mechanics/recurrence/` and land only the observation/closure slice:

- `docs/RECURRENCE_LIVE_OBSERVATION_PRODUCERS.md` -> `mechanics/recurrence/parts/live-observation-producers/README.md`
- `docs/RECURRENCE_REVIEW_DECISION_CLOSURE.md` -> `mechanics/recurrence/parts/review-decision-closure/README.md`

Add a package card, direction, parts, provenance, landing log, roadmap, and
active parts.

Keep these surfaces in their current homes:

- recurrence component manifests and hook bindings
- Agon-local recurrence observation under `mechanics/agon/`
- `mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md`
- generated activation and evaluation readouts

## Consequences

- Flat `docs/` no longer owns recurrence observation or closure posture.
- Recurrence can route repeated skill pressure without becoming automatic
  activation or automatic refresh.
- Component refresh law remains available for a later release-support,
  recurrence, or boundary-bridge pass after direct reading.
- Generated recurrence evidence remains advisory.

## Verification

Verify with:

```bash
python -m pytest -q tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py
python -m json.tool manifests/recurrence/component.skills.bundle-and-activation-beacons.json
python -m json.tool manifests/recurrence/hooks/component.skills.bundle-and-activation-beacons.hooks.json
python scripts/validate_nested_agents.py
```
