# aoa-tdd-slice candidate review

## Current status

- current maturity status: `canonical`
- canonical promotion decision: completed in this pass
- candidate set: first canonical-candidate review pass
- scope: `core`
- current lineage: manifest-aligned to published techniques `AOA-T-0014` and `AOA-T-0001`

## Canonical gate check

- traceability heading: pass
- pending technique dependencies: pass
- pending `TBD` path or `source_ref`: pass
- evaluation coverage: pass
- explicit-only policy gate: not applicable
- overall canonical gate result: pass

## Evidence reviewed

- `skills/core/engineering/aoa-tdd-slice/SKILL.md`
- `skills/core/engineering/aoa-tdd-slice/techniques.yaml`
- `skills/core/engineering/aoa-tdd-slice/examples/example.md`
- `skills/core/engineering/aoa-tdd-slice/references/tdd-slice-shapes.md`
- `tests/fixtures/skill_evaluation_cases.yaml`

## Findings

- runtime `SKILL.md` meaning changed: `yes`
- trigger boundary stays sharp around bounded test-first behavior work rather than exploratory, authority-mapping, or architectural tasks
- the trigger now covers observable behavior across module, CLI, builder, parser, validator, schema, generated/export, adapter, router, and workflow surfaces without treating every AoA surface as a special-case hard route
- contracts and verification sections are coherent with the skill's test-first workflow
- the new slice-shape reference gives future agents a broad but bounded way to choose red checks for non-feature-code surfaces
- manifest-backed traceability and runtime wording no longer drift
- the example now exercises source-to-generated builder behavior rather than only a narrow business-validation case
- linked evidence is already covered by manifest-aligned published technique lineage and pinned source refs
- reviewed evidence is already covered by this explicit candidate review pass and the aligned example artifact
- the skill already reads like a stable default recommendation for bounded test-first implementation work

## Gaps and blockers

- no current blocker remains at the repository gate level
- future follow-up should focus on preserving default-use clarity and reviewing drift rather than reopening the initial gate decision
- the historical first cohort should remain documented comparatively rather than rewritten as if canonical status had been automatic
- future generated/export cases should keep the red check on source-owned builder behavior rather than hand-edited derived bytes

## 2026-05-07 portability maintenance audit

- audit trigger: current skill-by-skill review showed that the original wording was correct but could be misread as ordinary feature-code TDD only.
- evidence checked: live `SKILL.md`, runtime example, OpenAI invocation notes, trigger fixtures, adjacent contract/invariant/source-of-truth skill boundaries, and current repository generated/export workflows.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep the skill canonical and broaden the behavior-slice surface set while preserving stop-lines for exploration, authority mapping, invariant work, contract validation, and broad architecture.
- blocker status: none; the update does not change status, scope, or invocation posture.

## Recommendation

Canonical promotion landed in this pass.
Keep this review record as the historical decision surface for why `aoa-tdd-slice` became part of the first canonical pair, and use future reviews only if its default-use rationale or bounded meaning starts to drift.
