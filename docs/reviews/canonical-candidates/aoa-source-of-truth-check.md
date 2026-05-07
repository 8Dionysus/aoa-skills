# aoa-source-of-truth-check candidate review

## Current status

- current maturity status: `canonical`
- canonical promotion decision: promoted in this pass
- candidate set: canonical promotion completed
- scope: `core`
- current lineage: manifest-aligned with published techniques `AOA-T-0013`, `AOA-T-0002`, and `AOA-T-0009`

## Canonical gate check

- traceability heading: pass
- pending technique dependencies: pass
- pending `TBD` path or `source_ref`: pass
- evaluation coverage: pass
- explicit-only policy gate: not applicable
- overall canonical gate result: pass

## Evidence reviewed

- `skills/core/engineering/aoa-source-of-truth-check/SKILL.md`
- `skills/core/engineering/aoa-source-of-truth-check/techniques.yaml`
- `skills/core/engineering/aoa-source-of-truth-check/examples/example.md`
- `skills/core/engineering/aoa-source-of-truth-check/references/authority-surface-shapes.md`
- `skills/core/engineering/aoa-source-of-truth-check/agents/openai.yaml`
- `tests/fixtures/skill_evaluation_cases.yaml`
- `tests/fixtures/skill_evaluation_snapshots/aoa-source-of-truth-check/*`

## Findings

- runtime `SKILL.md` meaning changed: `yes`
- the trigger boundary now treats document authority as one authority-surface shape among docs, source/config/schema, generated/export, runtime receipt, legacy/provenance, decision, and downstream owner surfaces
- the example keeps the workflow centered on authoritative source mapping, conflict reduction, and lightweight snapshot discipline for top-level status docs when canonical homes already exist
- the new authority-shape reference lets the skill stay portable without flattening every project into AoA-specific docs law
- the bundle now reads like a stable default reference for source-of-truth clarification across varied repository topologies and governance styles
- published lineage, runtime wording, and evaluation coverage are aligned
- the bundle is candidate-ready at the repository gate level

## Gaps and blockers

- no current blocker remains at the repository gate level
- future maintenance should preserve the document-authority boundary and avoid widening the skill into general roadmap or policy maintenance
- future drift review should keep entrypoint-doc cleanup tied to canonical homes rather than turning the skill into generic docs cleanup
- future generated/export cases should use this skill only when authority is unclear, not when a known source owner simply needs rebuild verification

## 2026-05-03 maintenance audit

- audit trigger: `aoa-techniques` root cleanup and mechanics restructuring showed that document authority now routinely includes active surfaces, legacy/provenance bridges, generated companions, decisions, and owner-local handoff surfaces.
- evidence checked: `Agents-of-Abyss` root surface law and mechanic package law; `aoa-techniques` root source-of-truth stack, Audit provenance for the former root roadmap, and Distillation/Agon active-first legacy bridges.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep the skill canonical and strengthen it around active/current versus historical/provenance/generated placement, portable public readability, and avoiding broad law blocks in unrelated surfaces.
- blocker status: none; the update does not change status, scope, or invocation posture.

## 2026-05-07 portability maintenance audit

- audit trigger: OpenAI-style skill portability review showed that the previous wording could still read as a docs-only cleanup skill even though AoA repositories routinely carry authority across source manifests, builders, generated exports, runtime receipts, public entrypoints, and downstream owner routes.
- evidence checked: live `SKILL.md`, runtime example, OpenAI invocation notes, trigger fixtures, source/generated authority patterns already present in adjacent engineering skills, and current review truth-sync expectations.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep the skill canonical and broaden its language from document-only authority to authority-surface mapping while preserving stop-lines for broad policy design, source-clear rebuilds, and generic derived-surface maintenance.
- blocker status: none; the update does not change status, scope, or invocation posture.

## Recommendation

Keep `aoa-source-of-truth-check` as a canonical default reference and use this review record as the maintenance surface for future drift checks.
