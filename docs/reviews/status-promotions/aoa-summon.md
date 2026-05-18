---
name: aoa-summon
---

# aoa-summon status promotion review

## Current status

- current maturity status: `evaluated`
- current machine-checkable floor (`candidate_ready` gate only when applicable): `pass`
- current governance lane decision: `stay_evaluated`
- scope: `core`
- current lineage: `published`
- reviewed revision: `64a3947c88b3`

## Target status

- target maturity status: `evaluated`
- why this target now: the bundle has self-contained runtime wording, trigger cases, snapshot coverage, autonomy coverage, and adjacency evidence for bounded child-route delegation, while live use shows it should no longer depend on scaffold memory.
- next status after this step: keep the skill evaluated until comparative default-reference review is ready.

## Evidence reviewed

- `skills/core/session-growth/aoa-summon/SKILL.md`
- `skills/core/session-growth/aoa-summon/techniques.yaml`
- `tests/fixtures/skill_evaluation_cases.yaml`
- `tests/fixtures/skill_evaluation_snapshots/aoa-summon/*`

## Findings

- machine-checkable floor result: `pass`
- recorded governance outcome: `stay_evaluated`
- runtime `SKILL.md` meaning changed: `yes`
- current bundle note: technique lineage is grounded in published decision, risk-passport, bounded-episode, and receipt-confirmed handoff techniques; the bundle now also blocks unresolved route choice to `aoa-session-route-forks` and requires an explicit receipt or acceptance expectation for cross-boundary child work. Latest lineage maintenance only refreshed the published `AOA-T-0062` source ref and did not change the evaluated status decision.

## Gaps and blockers

- blockers for this target status: none at the evaluated floor.
- blockers for the next status step: comparative default-reference rationale remains open.

## Recommendation

Keep `aoa-summon` at `evaluated` with governance at `stay_evaluated`; technique lineage is no longer pending, while default-reference promotion still needs comparative review.
