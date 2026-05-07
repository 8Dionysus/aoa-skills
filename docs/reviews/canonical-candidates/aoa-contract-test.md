# aoa-contract-test candidate review

## Current status

- current maturity status: `canonical`
- canonical promotion decision: promoted in this pass
- candidate set: canonical promotion completed
- scope: `core`
- current lineage: manifest-aligned to published techniques `AOA-T-0003` and `AOA-T-0015`

## Canonical gate check

- traceability heading: pass
- pending technique dependencies: pass
- pending `TBD` path or `source_ref`: pass
- evaluation coverage: pass
- explicit-only policy gate: not applicable
- overall canonical gate result: pass

## Evidence reviewed

- `skills/core/engineering/aoa-contract-test/SKILL.md`
- `skills/core/engineering/aoa-contract-test/techniques.yaml`
- `skills/core/engineering/aoa-contract-test/references/contract-shapes.md`
- `skills/core/engineering/aoa-contract-test/examples/example.md`
- `tests/fixtures/skill_evaluation_cases.yaml`

## Findings

- trigger boundary now covers meaningful module, service, CLI, schema, manifest, report, receipt, generated/export, workflow, and repo handoff boundaries with named consumers
- contracts and verification guidance stay coherent with the skill's boundary-oriented purpose while adding explicit claim limits
- manifest-backed traceability and runtime wording are aligned
- `references/contract-shapes.md` broadens the contract vocabulary across practice objects, execution skills, evaluation artifacts, scenarios, memory or recall surfaces, role contracts, routing, SDK, metrics, and generated/export surfaces without turning the skill into a generic test strategy
- the example now uses a generated catalog, routing, SDK, and source-owner contract posture, and keeps generated surfaces subordinate to owner truth
- trigger fixtures cover generated/export and reusable object-surface use cases, plus incidental-log and internal-detail do-not-use cases
- linked evidence, review evidence, and evaluation evidence are already covered by the repo-local canonical floor
- the skill now reads like a stable default-reference for contract-oriented validation work

## 2026-05-07 contract-shape maintenance audit

- audit trigger: `aoa-contract-test` review found that service-response examples were too narrow for project-wide contract work across practice patterns, evaluation artifacts, role contracts, memory and recall surfaces, scenarios, routing, SDK, metrics, generated/export surfaces, receipts, schemas, and handoffs.
- evidence checked: live `SKILL.md`, `contract-shapes.md`, generated/export example, sibling repo README and route surfaces for `aoa-techniques`, `aoa-evals`, `aoa-agents`, `aoa-memo`, `aoa-playbooks`, `aoa-routing`, `aoa-sdk`, and `aoa-stats`, trigger fixtures, generated export, and quality audit.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep `aoa-contract-test` canonical, keep the core workflow compact, add reference-based contract shapes for diverse producer-consumer seams, and explicitly reject incidental logs or internal implementation details as public contracts.
- blocker status: none; this is a maintenance tightening and depth pass, not a status, scope, invocation posture, or technique-dependency change.

## 2026-05-07 portability maintenance audit

- audit trigger: official OpenAI skill guidance reinforced that the trigger boundary should describe when to use the skill in portable terms and leave domain detail for progressively loaded references.
- evidence checked: official OpenAI skill docs and academy material, live `SKILL.md`, `contract-shapes.md`, example, trigger fixtures, generated export, and quality audit.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep AoA contract shapes as rich application cases, but express the runtime trigger around reusable producer-consumer contracts across modules, schemas, generated/export surfaces, workflows, memory, roles, routing, SDK, metrics, and scenarios.
- blocker status: none; canonical status and default-reference posture stay intact.

## Gaps and blockers

- no current blocker remains at the repository gate level
- future follow-up should preserve named producer-consumer clarity, source-owner versus derived-surface distinction, and review drift rather than reopen the promotion decision
- maintenance should stay comparative and not widen into generic test strategy or whole-system proof

## Recommendation

Keep `aoa-contract-test` as a canonical default reference and use this review record as the maintenance surface for future drift checks.
