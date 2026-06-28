# aoa-decision status promotion review

## Current status

- current maturity status: `evaluated`
- current machine-checkable floor (`candidate_ready` gate only when applicable): `pass`
- current governance lane decision: `stay_evaluated`
- scope: `core`
- current lineage: `published`
- reviewed revision: `32bf356582d5`

## Target status

- target maturity status: `evaluated`
- why this target now: the decision router is part of the decision graph chain and now carries graph status, issue, and impact-packet behavior.
- next status after this step: keep evaluated while graph-first behavior is validated through skill fixtures, generated exports, and MCP wiring.

## Evidence reviewed

- `skills/core/engineering/aoa-decision/SKILL.md`
- `.agents/skills/aoa-decision/SKILL.md`
- `config/portable_skill_overrides.json`
- `config/tiny_router_skill_bands.json`
- `tests/fixtures/skill_evaluation_cases.yaml`

## Findings

- machine-checkable floor result: `pass`
- recorded governance outcome: `stay_evaluated`
- runtime `SKILL.md` meaning changed: `yes`
- current bundle note: the router selects one find, create, or correct subskill, checks `aoa_decisions` status and issue posture first, uses path/repo/surface/decision packets before broad search, keeps repo-local decision notes authoritative, and keeps the `abyss-stack` graph-builder fallback portable by requiring agents to locate the checkout before running it. When prior-session behavior, correction history, tool usage, impact evidence, or "what happened after" matters, it now routes through `.aoa` session evidence after the decision graph route, preferring `usage-chain` for stable decision/tool/path anchors when the question is about usage, outcomes, consequences, recurrence, or nearby errors; `entity-dossier` is reserved for source identity, graph/cooccurrence/timeline context, related entities, or a heavier human packet. Session packets remain evidence refs only.

## Gaps and blockers

- blockers for this target status: none at the current bundle gate.
- blockers for the next status step: canonical promotion would need repeated field evidence that issue-aware graph routing improves agent accuracy without over-routing ordinary docs edits.

## Recommendation

Keep `aoa-decision` at evaluated status and maintain it with decision-graph MCP and skill fixture validation.
