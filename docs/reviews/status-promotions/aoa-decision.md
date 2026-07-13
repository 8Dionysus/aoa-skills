# aoa-decision status promotion review

## Current status

- current maturity status: `evaluated`
- current machine-checkable floor (`candidate_ready` gate only when applicable): `pass`
- current governance lane decision: `stay_evaluated`
- scope: `core`
- current lineage: `published`
- reviewed revision: `c30d86bc4859`

## Target status

- target maturity status: `evaluated`
- why this target now: the decision router is part of the decision graph chain and now carries graph status, issue, and impact-packet behavior.
- next status after this step: keep evaluated while graph-first behavior is validated through skill fixtures, generated exports, and MCP wiring.

## Evidence reviewed

- `skills/core/engineering/aoa-decision/SKILL.md`
- `.agents/skills/aoa-decision/SKILL.md`
- `config/portable_skill_overrides.json`
- `skills/core/engineering/aoa-decision/agents/openai.yaml`
- `config/tiny_router_skill_bands.json`
- `tests/fixtures/skill_evaluation_cases.yaml`
- `evals/reports/aoa-skill-live-dispatch-pilot13-returns-20260712-v14-reviewed-complete-skill-returns-needs-rerun.json`

## Findings

- machine-checkable floor result: `pass`
- recorded governance outcome: `stay_evaluated`
- runtime `SKILL.md` meaning changed: `yes`
- current bundle note: the router classifies the task, then selects and fully
  reads exactly one find, create, or correct child before that child performs
  graph lookup or a write. Root-only graph execution after merely naming a
  child is explicitly incomplete. The selected child still checks
  `aoa_decisions` status and issue posture first, uses
  path/repo/surface/decision packets before broad search, keeps repo-local
  decision notes authoritative, and retains the portable `abyss-stack`
  graph-builder fallback. Session packets remain evidence refs only and stay
  downstream of the decision route.

## Gaps and blockers

- blockers for this target status: none at the current bundle gate.
- blockers for the next status step: canonical promotion still needs repeated
  field evidence that issue-aware graph routing improves agent accuracy without
  over-routing ordinary docs edits. The exact affected live case must also be
  rerun after this child-handoff repair; the source change alone is not evidence
  of runtime improvement.

## Recommendation

Keep `aoa-decision` at evaluated status and maintain it with decision-graph
MCP, skill fixture validation, prompt-visible export checks, and the smallest
source-locked live return before any wider promotion claim.
