# aoa-port-adapter-refactor candidate review

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

- `skills/core/engineering/aoa-port-adapter-refactor/SKILL.md`
- `skills/core/engineering/aoa-port-adapter-refactor/techniques.yaml`
- `skills/core/engineering/aoa-port-adapter-refactor/examples/example.md`
- `skills/core/engineering/aoa-port-adapter-refactor/references/adapter-seam-shapes.md`
- `skills/core/engineering/aoa-port-adapter-refactor/agents/openai.yaml`
- `tests/fixtures/skill_evaluation_cases.yaml`
- `docs/governance/lanes.md`

## Findings

- the trigger boundary stays focused on ports and adapters around concrete dependency pressure after the broader context boundary is already understood
- the skill now reads clearly as a follow-on to `aoa-bounded-context-map` rather than as a competing first-pass boundary-clarification skill
- the skill remains distinct from `aoa-core-logic-boundary` by staying on a narrower dependency seam rather than a general reusable-rules versus orchestration decision
- the trigger now covers concrete dependencies beyond provider clients, including builders, CLIs, SDK facades, generated/export writers, filesystem paths, environment lookups, clocks, network clients, subprocesses, storage layers, and runtime discovery
- `references/adapter-seam-shapes.md` carries wider seam vocabulary without making the runtime `SKILL.md` a long dependency catalog
- the example now uses a generated/export builder seam where reusable source-to-output mapping stays separate from path discovery and artifact writing
- published lineage, runtime wording, and evaluation coverage are aligned
- the bundle is candidate-ready at the repository gate level

## Gaps and blockers

- no lineage or evaluation blocker remains at the repository gate level
- the lane keeps `aoa-bounded-context-map` as the default entry anchor, while `aoa-port-adapter-refactor` stays a specialized follow-on skill for concrete dependency seams once context carving is already done
- future canonical review should preserve the narrow port/adapter seam and avoid widening the skill into open-ended restructuring
- future maintenance should keep consumer-visible schema validation routed to `aoa-contract-test` after the seam exists

## 2026-05-07 portability maintenance audit

- audit trigger: official OpenAI skill guidance reinforces concise trigger metadata, progressive disclosure, and self-contained skills; `aoa-port-adapter-refactor` needed broader dependency-seam coverage without becoming generic architecture cleanup.
- evidence checked: official OpenAI skill docs and academy material, live `SKILL.md`, adapter seam reference, example, trigger fixtures, generated export, and quality audit.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep the skill evaluated and specialized around concrete dependency seams, while moving diverse dependency shapes into a reference and preserving stop-lines to bounded-context mapping, core-logic boundary work, and contract testing.
- blocker status: none; evaluated status and stay-evaluated lane decision remain unchanged.

## Recommendation

Keep `aoa-port-adapter-refactor` at `evaluated` in this pass.
Use this record as the explicit stay-evaluated decision while `aoa-bounded-context-map` remains the entry anchor for this lane.
