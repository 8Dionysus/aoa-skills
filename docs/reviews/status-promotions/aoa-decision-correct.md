# aoa-decision-correct status promotion review

## Current status

- current maturity status: `evaluated`
- current machine-checkable floor (`candidate_ready` gate only when applicable): `pass`
- current governance lane decision: `stay_evaluated`
- scope: `core`
- current lineage: `published`
- reviewed revision: `4a07913f76e6`

## Target status

- target maturity status: `evaluated`
- why this target now: the correct subskill repairs decision notes, indexes, and
  graph issue posture without creating unnecessary new rationale, and now
  terminates a parent-classified route with unavailable required context as
  `blocked_missing_input` rather than an owner-boundary deferral.
- next status after this step: keep evaluated while correction routes prove the
  missing-input terminal and safe stale-metadata/unknown-surface repair in
  repeated live use.

## Evidence reviewed

- `skills/core/engineering/aoa-decision-correct/SKILL.md`
- `.agents/skills/aoa-decision-correct/SKILL.md`
- `config/portable_skill_overrides.json`
- `tests/test_live_skill_dispatch_harness.py`
- `evals/reports/aoa-skill-live-dispatch-full-collision-authority-routing-returns-20260713-v19-reviewed-procedure-returns-needs-rerun.json`
- `evals/reports/aoa-skill-live-dispatch-full-collision-authority-routing-procedure-returns-20260713-v19-reviewed-clean.json`
- `tests/fixtures/skill_evaluation_cases.yaml`

## Findings

- machine-checkable floor result: `pass`
- recorded governance outcome: `stay_evaluated`
- runtime `SKILL.md` meaning changed: `yes`
- current bundle note: the skill checks graph issues first, repairs existing
  source records or metadata, rebuilds local indexes, and refreshes or checks
  the workspace graph. When its parent route lacks the target note, local index
  contract, or graph/owner packet inside the active evidence boundary, source
  and portable description now require `blocked_missing_input`.

## Gaps and blockers

- blockers for this target status: none; the deterministic bundle and exact-
  merged four-turn return both preserve the evaluated boundary.
- blockers for the next status step: canonical promotion would still need
  repeated real corrections with clean source/index/graph closeout.

## Recommendation

Keep `aoa-decision-correct` at evaluated status. The bounded live return now
supports the missing-input terminal; retain source-first correction plus graph
validation checks for successful repairs before any wider promotion.
