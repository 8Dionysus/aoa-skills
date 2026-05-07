# aoa-property-invariants candidate review

## Current status

- current maturity status: `canonical`
- canonical promotion decision: promoted in this pass
- review set: current canonical promotion review pass
- scope: `core`
- current lineage: manifest-aligned to published techniques `AOA-T-0017` and `AOA-T-0007`

## Canonical gate check

- traceability heading: pass
- pending technique dependencies: pass
- pending `TBD` path or `source_ref`: pass
- evaluation coverage: pass
- explicit-only policy gate: not applicable
- overall canonical gate result: pass

## Evidence reviewed

- `skills/core/engineering/aoa-property-invariants/SKILL.md`
- `skills/core/engineering/aoa-property-invariants/techniques.yaml`
- `skills/core/engineering/aoa-property-invariants/examples/example.md`
- `skills/core/engineering/aoa-property-invariants/references/invariant-shapes.md`
- `tests/fixtures/skill_evaluation_cases.yaml`

## Findings

- trigger boundary stays focused on stable truths, invariants, and broad coverage rather than presentation-only examples
- contracts and verification guidance stay coherent with the invariant-oriented testing intent
- manifest-backed traceability and runtime wording are aligned
- the example reinforces property-oriented thinking without collapsing into generic test design
- the trigger now covers stable artifact, transformation, generated/export, workflow, route, provenance, lifecycle, uniqueness, repeatability, and source-ref preservation invariants without tying activation to project-local object names
- `references/invariant-shapes.md` carries wider invariant vocabulary without turning the core skill into a proof encyclopedia
- the example now uses a source-to-generated catalog invariant shape where generated surfaces stay derived from source truth
- linked evidence is already covered by manifest-aligned published technique lineage and pinned source refs
- reviewed evidence is already covered by this explicit candidate review pass and the aligned example artifact
- the skill now reads as a stable default reference for invariant-oriented testing work
- runtime `SKILL.md` meaning changed: yes, boundedly, to cover artifact and workflow invariants beyond ordinary data behavior while preserving the invariant-authoring lane

## Gaps and blockers

- no current blocker remains at the repository gate level
- future follow-up should preserve invariant clarity and maintenance drift rather than reopen the initial gate decision
- the record now serves as the canonical maintenance reference instead of a candidate comparison
- future maintenance should keep existing-coverage review routed to `aoa-invariant-coverage-audit` and consumer-visible seam validation routed to `aoa-contract-test`

## 2026-05-07 portability maintenance audit

- audit trigger: official OpenAI skill guidance reinforced that trigger wording should remain broad and concise while richer domain variants load through references only when useful.
- evidence checked: official OpenAI skill docs and academy material, live `SKILL.md`, invariant-shapes reference, example, trigger fixtures, generated export, and quality audit.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep `aoa-property-invariants` canonical, expand the invariant vocabulary through portable shape language, and keep project-specific generated/export and provenance cases as applications rather than activation law.
- blocker status: none; canonical status and default-reference posture stay intact.

## Recommendation

Keep `aoa-property-invariants` as the canonical reference for invariant-oriented testing work.
Use this review record as the maintenance decision surface after promotion.
