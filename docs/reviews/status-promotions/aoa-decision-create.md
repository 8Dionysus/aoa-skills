# aoa-decision-create status promotion review

## Current status

- current maturity status: `evaluated`
- current machine-checkable floor (`candidate_ready` gate only when applicable): `pass`
- current governance lane decision: `stay_evaluated`
- scope: `core`
- current lineage: `published`
- reviewed revision: `97d779ad97b8`

## Target status

- target maturity status: `evaluated`
- why this target now: the create subskill writes source-owned decision records,
  includes graph issue stop-lines before writes, and now terminates a
  parent-classified route with unavailable required context as
  `blocked_missing_input` rather than an owner-boundary deferral.
- next status after this step: keep evaluated while create routes prove both the
  missing-input terminal and successful local-index/workspace-graph refresh in
  repeated live use.

## Evidence reviewed

- `skills/core/engineering/aoa-decision-create/SKILL.md`
- `.agents/skills/aoa-decision-create/SKILL.md`
- `config/portable_skill_overrides.json`
- `tests/test_live_skill_dispatch_harness.py`
- `evals/reports/aoa-skill-live-dispatch-full-collision-authority-routing-returns-20260713-v19-reviewed-procedure-returns-needs-rerun.json`
- `tests/fixtures/skill_evaluation_cases.yaml`

## Findings

- machine-checkable floor result: `pass`
- recorded governance outcome: `stay_evaluated`
- runtime `SKILL.md` meaning changed: `yes`
- current bundle note: the skill checks graph status and issues before writing,
  uses narrower placement packets before broad search, reads repo-local route
  law, and requires local index plus graph validation after writes. When its
  parent route lacks the chosen decision, repo, source, graph, or local-law
  inputs inside the active evidence boundary, source and portable description
  now require `blocked_missing_input`.

## Gaps and blockers

- blockers for this target status: none at the deterministic bundle gate; the
  bounded live correction remains intentionally unclaimed.
- blockers for the next status step: the four-turn 40-41 return must verify the
  new terminal after exact merge, and canonical promotion would still need
  broader evidence that create routes avoid unnecessary decision records.

## Recommendation

Keep `aoa-decision-create` at evaluated status. Require the bounded live return
before claiming the terminal repair, and retain source-note, index, and
decision-graph landing validation for successful writes.
