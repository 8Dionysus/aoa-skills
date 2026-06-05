# aoa-decision-correct status promotion review

## Current status

- current maturity status: `evaluated`
- current machine-checkable floor (`candidate_ready` gate only when applicable): `pass`
- current governance lane decision: `stay_evaluated`
- scope: `core`
- current lineage: `published`
- reviewed revision: `18f68b1173b4`

## Target status

- target maturity status: `evaluated`
- why this target now: the correct subskill repairs decision notes, indexes, and graph issue posture without creating unnecessary new rationale.
- next status after this step: keep evaluated while correction routes prove they handle stale metadata and unknown-surface issues safely.

## Evidence reviewed

- `skills/core/engineering/aoa-decision-correct/SKILL.md`
- `.agents/skills/aoa-decision-correct/SKILL.md`
- `tests/fixtures/skill_evaluation_cases.yaml`

## Findings

- machine-checkable floor result: `pass`
- recorded governance outcome: `stay_evaluated`
- runtime `SKILL.md` meaning changed: `yes`
- current bundle note: the skill checks graph issues first, repairs existing source records or metadata, rebuilds local indexes, and refreshes or checks the workspace graph.

## Gaps and blockers

- blockers for this target status: none at the current bundle gate.
- blockers for the next status step: canonical promotion would need repeated real corrections with clean post-graph evidence.

## Recommendation

Keep `aoa-decision-correct` at evaluated status and maintain it with source-first correction and graph validation checks.
