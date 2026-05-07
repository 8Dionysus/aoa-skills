---
name: aoa-session-self-diagnose
---

# aoa-session-self-diagnose status promotion review

## Current status

- current maturity status: `evaluated`
- current machine-checkable floor (`candidate_ready` gate only when applicable): `pass`
- current governance lane decision: `stay_evaluated`
- scope: `core`
- current lineage: `published`
- reviewed revision: `8699efef95b6`

## Target status

- target maturity status: `evaluated`
- why this target now: the skill has published lineage, autonomy coverage, trigger cases, snapshot coverage, and adjacency evidence that keeps diagnosis before repair.
- next status after this step: keep the skill evaluated until default-reference reasoning can compare diagnosis against repair, runtime overlays, and owner-route checks.

## Evidence reviewed

- `skills/core/session-growth/aoa-session-self-diagnose/SKILL.md`
- `skills/core/session-growth/aoa-session-self-diagnose/techniques.yaml`
- `skills/core/session-growth/aoa-session-self-diagnose/examples/runtime.md`
- `tests/fixtures/skill_evaluation_cases.yaml`
- `tests/fixtures/skill_evaluation_snapshots/aoa-session-self-diagnose/*`

## Findings

- machine-checkable floor result: `pass`
- recorded governance outcome: `stay_evaluated`
- runtime `SKILL.md` meaning changed: `yes`
- current bundle note: the skill is evaluated as a diagnosis packet workflow with explicit evidence posture, so hints, generated summaries, and stale neighboring claims cannot become settled root-cause evidence.

## Gaps and blockers

- blockers for this target status: none at the evaluated floor.
- blockers for the next status step: comparative default-reference rationale remains open against repair and project-runtime diagnostic overlays.

## Recommendation

Promote `aoa-session-self-diagnose` to `evaluated` and keep it at `stay_evaluated`.
