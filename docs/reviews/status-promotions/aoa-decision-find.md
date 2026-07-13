# aoa-decision-find status promotion review

## Current status

- current maturity status: `evaluated`
- current machine-checkable floor (`candidate_ready` gate only when applicable): `pass`
- current governance lane decision: `stay_evaluated`
- scope: `core`
- current lineage: `published`
- reviewed revision: `21e7560eb13c`

## Target status

- target maturity status: `evaluated`
- why this target now: the find subskill is part of the decision graph chain and must stay portable, bounded, and source-verifying.
- next status after this step: keep evaluated while lookup accuracy is covered by graph packet and source-note verification fixtures.

## Evidence reviewed

- `skills/core/engineering/aoa-decision-find/SKILL.md`
- `.agents/skills/aoa-decision-find/SKILL.md`
- `config/portable_skill_overrides.json`
- `skills/core/engineering/aoa-decision-find/agents/openai.yaml`
- `tests/fixtures/skill_evaluation_cases.yaml`
- `evals/reports/aoa-skill-live-dispatch-pilot13-skill-returns-20260712-v14-reviewed-mixed-source-and-observation-returns-needs-rerun.json`

## Findings

- machine-checkable floor result: `pass`
- recorded governance outcome: `stay_evaluated`
- runtime `SKILL.md` meaning changed: `yes`
- current bundle note: the skill uses the narrowest available decision graph
  packet, treats broad graph search as fallback after
  path/repo/surface/decision anchors, then verifies claims against repo-local
  source notes before reporting rationale. If the permitted boundary contains
  neither graph/fallback access nor graph and owner inputs, it now stops with
  `blocked_missing_input` rather than reporting an owner-boundary deferral.

## Gaps and blockers

- blockers for this target status: none at the current bundle gate.
- blockers for the next status step: canonical promotion would need stronger
  evidence across repeated real decision lookups. The exact affected live pair
  must rerun after this disposition repair; source checks alone do not prove the
  model follows the terminal contract.

## Recommendation

Keep `aoa-decision-find` at evaluated status and maintain it through graph
packet, source-note, prompt-visible export, and smallest-return live checks.
