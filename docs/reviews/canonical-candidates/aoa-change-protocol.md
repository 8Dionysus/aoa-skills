# aoa-change-protocol candidate review

## Current status

- current maturity status: `canonical`
- canonical promotion decision: completed in this pass
- candidate set: first canonical-candidate review pass
- scope: `core`
- current lineage: manifest-aligned to published techniques `AOA-T-0001` and `AOA-T-0002`

## Canonical gate check

- traceability heading: pass
- pending technique dependencies: pass
- pending `TBD` path or `source_ref`: pass
- evaluation coverage: pass
- explicit-only policy gate: not applicable
- overall canonical gate result: pass

## Evidence reviewed

- `skills/core/engineering/aoa-change-protocol/SKILL.md`
- `skills/core/engineering/aoa-change-protocol/techniques.yaml`
- `skills/core/engineering/aoa-change-protocol/checks/review.md`
- `tests/fixtures/skill_evaluation_cases.yaml`

## Findings

- trigger boundary is crisp and distinguishes non-trivial change work from tiny edits
- contracts and verification guidance stay coherent with the bounded change-protocol intent
- manifest-backed traceability and runtime wording are aligned
- the review checklist reinforces the same bounded workflow without widening scope
- linked evidence is already covered by manifest-aligned published technique lineage and pinned source refs
- reviewed evidence is already covered by this explicit candidate review pass and the aligned support artifact
- the skill already reads like a stable default-use workflow rather than a narrow one-project specialization

## Gaps and blockers

- no current blocker remains at the repository gate level
- future follow-up should focus on preserving default-use clarity and reviewing drift rather than reopening the initial gate decision
- the historical first cohort should remain documented comparatively rather than rewritten as if canonical status had been automatic

## 2026-05-03 maintenance audit

- audit trigger: repeated use during `aoa-techniques` mechanics and root source-of-truth work showed the skill still fit, but its runtime wording under-described owner-route reading before planning.
- evidence checked: `Agents-of-Abyss` route law and mechanics package standard; `aoa-techniques` `CHARTER.md`, `docs/ROOT_SURFACE_LAW.md`, `ROADMAP.md`, `mechanics/AGENTS.md`, and active mechanics package surfaces.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep the skill canonical and strengthen it around owner-route inspection, source-grounded planning, generated/export rebuilds, and post-change route review.
- blocker status: none; the update does not change status, scope, or invocation posture.

## 2026-07-12 adaptive boundary audit

- audit trigger: the complete exact-merged v14 `pilot13-returns` run selected
  the generic workflow for an explicit-only production approval classification
  and for an ATM10 manual-overlay prompt.
- evidence checked: the reviewed public receipt, both target skill sources,
  `aoa-change-protocol` source and prompt-visible portable description,
  activation policy, collision-family config, and red-first trigger fixtures.
- runtime `SKILL.md` meaning changed: yes, boundedly. The generic workflow now
  excludes approval-only classification and project-specific manual-overlay
  ownership before planning begins; it does not load either explicit owner.
- decision: keep the skill canonical and keep implicit invocation for genuinely
  generic bounded changes. Narrowing the negative boundary is preferable to
  making the whole workflow manual or weakening the explicit target policies.
- blocker status: the smallest affected exact-source live rerun remains
  required before claiming that the runtime collision is repaired.

## Recommendation

Canonical promotion landed in this pass.
Keep this review record as the historical decision surface for why `aoa-change-protocol` became part of the first canonical pair, and use future reviews only if its default-use rationale or bounded meaning starts to drift.

## 2026-07-12 concrete ATM10 return audit

- audit trigger: the first exact-merged six-turn source-return run closed the
  approval-only collision but still loaded the generic workflow for the
  concrete ATM10 repo-relative overlay prompt.
- evidence checked: the reviewed public six-turn receipt, `collision-14`
  procedure and owner-action contracts, the ATM10 explicit-overlay policy,
  generic source and portable descriptions, and red-first trigger fixtures.
- runtime `SKILL.md` meaning changed: yes, boundedly. ATM10 repo-relative path,
  local-command, or approval-note requests now report the manual owner route
  without loading either the generic skill or the explicit overlay.
- preserved behavior: ordinary generic bounded changes remain implicit; the
  ATM10 target stays explicit-only; neither target procedure nor answer key
  changes.
- decision: keep the skill canonical. The change is a concrete negative-boundary
  clarification of the prior adaptive audit, not a new project overlay inside
  the generic workflow.
- blocker status: the exact affected cohort must rerun after runtime parity;
  deterministic source checks alone do not close the observed collision.
