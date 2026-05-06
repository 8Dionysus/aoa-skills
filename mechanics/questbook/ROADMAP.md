# Questbook Roadmap

## Current Contour

Questbook owns the skill-layer quest source/index boundary, quest dispatch
projection, and `aoa-quest-harvest` posture. The public tracked obligation
index is now root `../../QUESTBOOK.md`; this package explains the mechanism
that keeps that index, lane-first `quests/`, schemas, and generated projections
in authority order.

Active surfaces include `../../QUESTBOOK.md`, `../../quests/`,
`docs/QUESTBOOK_SKILL_INTEGRATION.md`, `parts/source-index-boundary/`,
`parts/session-harvest-posture/`, `parts/dispatch-projection/`,
`generated/quest_catalog.min.json`, and `generated/quest_dispatch.min.json`.

Allowed `aoa-quest-harvest` verdicts remain:

- `keep/open quest`
- `promote to skill`
- `promote to playbook`
- `promote to orchestrator surface`
- `promote to proof surface`
- `promote to memo surface`

## Next Work

- Keep root `QUESTBOOK.md` compact: public bands, update trigger, backing files,
  and the rule for durable skill-layer obligations.
- Decide whether `quests/` needs package-local owner route receipts or should
  stay lane-first with generated dispatch views.
- Decide whether generated quest catalog and dispatch projections need
  package-local validation notes beyond existing validators.
- Keep `aoa-quest-harvest` skill meaning under `skills/`.
- Keep growth-cycle orchestration and checkpoint capture in their own packages.

## When Time Comes

- Promote a repeated quest pattern when it appears twice in one lane or three
  times across lanes.
- Add lane README route notes when a lane gains enough active quests that
  `quests/README.md` is no longer enough.
- Promote a quest family into playbooks, evals, memo, routing, or skill bundles
  only after the owner surface accepts that kind of truth.

## Out Of Scope

- A second roadmap.
- Private scratchpad content or transient generated noise.
- Moving source quest objects merely for symmetry.
- Treating generated quest projections as source truth.
