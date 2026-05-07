# aoa-core-logic-boundary candidate review

## Current status

- current maturity status: `evaluated`
- current machine-checkable floor: published lineage plus example-backed evaluation coverage
- candidate set: post-lineage conservative review wave
- scope: `core`
- current lineage: manifest-aligned with published techniques `AOA-T-0016` and `AOA-T-0015`

## Canonical gate check

- traceability heading: pass
- pending technique dependencies: pass
- pending `TBD` path or `source_ref`: pass
- evaluation coverage: pass
- explicit-only policy gate: not applicable
- overall canonical gate result: pass

## Evidence reviewed

- `skills/core/engineering/aoa-core-logic-boundary/SKILL.md`
- `skills/core/engineering/aoa-core-logic-boundary/techniques.yaml`
- `skills/core/engineering/aoa-core-logic-boundary/references/core-boundary-shapes.md`
- `skills/core/engineering/aoa-core-logic-boundary/examples/example.md`
- `skills/core/engineering/aoa-core-logic-boundary/agents/openai.yaml`
- `tests/fixtures/skill_evaluation_cases.yaml`
- `docs/governance/lanes.md`

## Findings

- the trigger boundary remains focused on deciding what belongs in a reusable center versus glue, projection, rendering, runtime, infrastructure, or orchestration detail after the broader context boundary is already understood
- the wording now reads clearly as a follow-on to `aoa-bounded-context-map` rather than as a competing first-pass boundary-clarification skill
- the wording stays distinct from `aoa-port-adapter-refactor` by keeping the object on reusable rules versus surrounding orchestration instead of on a narrower concrete dependency seam
- the wording now stays distinct from `aoa-contract-test` by routing consumer-visible contract validation away once the core-versus-edge split is already clear
- `references/core-boundary-shapes.md` broadens the usable vocabulary across code, execution skills, practice patterns, evaluation artifacts, role contracts, memory or recall surfaces, scenarios, routing, SDK, metrics, generated/export, process, and workflow surfaces without asking the runtime skill body to carry a long checklist
- the example now uses a workflow catalog-builder seam where source-owned classification rules stay separate from installed export formatting, report rendering, router hints, and local path discovery
- trigger fixtures now cover skill export projection, eval report rendering, unclear source-owner deflection, and contract-validation deflection
- published lineage, runtime wording, and evaluation evidence are aligned
- the bundle is candidate-ready at the repository gate level

## 2026-05-07 core-boundary maintenance audit

- audit trigger: `aoa-core-logic-boundary` review found that the previous fulfillment-module example and code-centric wording were too narrow for project-wide work where reusable centers can be workflow rules, practice moves, eval scoring semantics, role contracts, recall rules, scenario phases, routing decisions, SDK loaders, metric envelopes, generated mappings, process contracts, or workflow phase gates.
- evidence checked: live `SKILL.md`, `core-boundary-shapes.md`, workflow catalog example, sibling repo route surfaces for `aoa-techniques`, `aoa-evals`, `aoa-agents`, `aoa-memo`, `aoa-playbooks`, `aoa-routing`, `aoa-sdk`, and `aoa-stats`, trigger fixtures, generated export, and quality audit.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep `aoa-core-logic-boundary` at `evaluated`; deepen the reusable-center vocabulary while preserving its lane role as a specialized follow-on after `aoa-bounded-context-map`, not the default boundary anchor.
- blocker status: none at the repository gate level; canonical/default-reference promotion remains a comparative lane question, not a quality blocker.

## 2026-05-07 portability maintenance audit

- audit trigger: official OpenAI skill guidance reinforced that the core trigger should stay self-contained and broadly reusable while examples and references carry richer domain detail.
- evidence checked: official OpenAI skill docs and academy material, live `SKILL.md`, `core-boundary-shapes.md`, example, trigger fixtures, generated export, and quality audit.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: replace project-specific trigger language with portable repository/layer/surface language while preserving rich project seams as examples and reference stress cases.
- blocker status: none; evaluated status and stay-evaluated lane decision remain unchanged.

## Gaps and blockers

- no lineage or evaluation blocker remains at the repository gate level
- the lane keeps `aoa-bounded-context-map` as the default starting point, while `aoa-core-logic-boundary` stays a specialized follow-on skill for the narrower "reusable center versus glue" decision once context carving is already done
- future canonical review should preserve the "reusable center versus glue" decision boundary, the source-owner stop-lines, and the explicit deflections to `aoa-contract-test` and `aoa-port-adapter-refactor`

## Recommendation

Keep `aoa-core-logic-boundary` at `evaluated` in this pass.
Use this record as the explicit stay-evaluated decision while `aoa-bounded-context-map` remains the entry anchor for this lane.
