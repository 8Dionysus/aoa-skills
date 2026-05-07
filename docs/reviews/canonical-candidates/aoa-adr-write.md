# aoa-adr-write candidate review

## Current status

- current maturity status: `canonical`
- canonical promotion decision: promoted in this pass
- candidate set: canonical promotion completed
- scope: `core`
- current lineage: manifest-aligned with published technique `AOA-T-0033`

## Canonical gate check

- traceability heading: pass
- pending technique dependencies: pass
- pending `TBD` path or `source_ref`: pass
- evaluation coverage: pass
- explicit-only policy gate: not applicable
- overall canonical gate result: pass

## Evidence reviewed

- `skills/core/engineering/aoa-adr-write/SKILL.md`
- `skills/core/engineering/aoa-adr-write/techniques.yaml`
- `skills/core/engineering/aoa-adr-write/examples/example.md`
- `skills/core/engineering/aoa-adr-write/references/decision-boundary-lenses.md`
- `skills/core/engineering/aoa-adr-write/references/decision-note.template.md`
- `skills/core/engineering/aoa-adr-write/agents/openai.yaml`
- `tests/fixtures/skill_evaluation_cases.yaml`

## Findings

- the trigger boundary stays crisp around recording meaningful architecture or workflow decisions rather than generic docs cleanup
- the no-decision stop-line rejects premature ADR writing before a real choice exists
- the example and evaluation coverage reinforce rationale, tradeoffs, and consequence capture without widening the skill into broad governance prose
- the bundle now reads like a stable default reference for recording why a path was chosen even when local ADR templates or note homes vary
- published lineage and runtime wording are aligned
- the bundle is candidate-ready at the repository gate level
- the new decision-boundary lenses deepen the skill across owner/source, placement, evidence state, workflow/process, lifecycle, portability, runtime-facing surfaces, handoff, risk, and scale without turning ADR writing into generic boundary mapping
- trigger coverage now includes a reviewed cross-boundary decision, an unresolved-boundary stop-line, and an unreviewed evidence/generated-observation misuse case
- the trigger boundary now rejects ordinary implementation choices when the diff, tests, commit message, or review summary preserve enough rationale
- runtime or incident follow-up cases now route toward runbook, risk approval, or operational follow-up rather than ADR clutter

## Gaps and blockers

- no current blocker remains at the repository gate level
- future maintenance should preserve the boundary between decision-rationale recording and neighboring source-of-truth or boundary-mapping workflows
- future drift review should keep template variability and placement rules from turning the skill into document-authority work
- future maintenance should keep the decision-lens reference subordinate to one reviewed decision per note
- future no-harm checks should prefer no ADR whenever a lighter artifact preserves enough rationale for future work

## 2026-05-07 decision-lens maintenance audit

- audit trigger: follow-up review after `aoa-bounded-context-map` lens work found that ADR writing also needs deeper discrimination between durable decisions, evidence surfaces, provisional workflow hints, generated observations, source-of-truth routes, and unresolved owner boundaries.
- evidence checked: live `SKILL.md`, `decision-boundary-lenses.md`, decision-note template, adjacent `aoa-source-of-truth-check` and `aoa-bounded-context-map` boundaries, upstream `AOA-T-0033`, trigger fixtures, generated export, and quality audit.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep `aoa-adr-write` canonical, keep the core workflow compact, add ADR-specific boundary lenses as a reference, and explicitly route unresolved-boundary or unreviewed-hint cases away before writing a decision record.
- blocker status: none; this is a maintenance tightening and depth pass, not a status or invocation posture change.

## 2026-05-07 no-harm maintenance audit

- audit trigger: user concern that an AoA-first ADR skill must not make unrelated or ordinary work worse by over-documenting routine implementation choices.
- evidence checked: live `SKILL.md`, `decision-boundary-lenses.md`, trigger fixtures, generated export, and quality audit after regeneration.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep AoA-first ADR writing, but add no-harm stop-lines and trigger coverage so ordinary implementation choices, review-summary cases, runbook updates, incident notes, risk approvals, and operational follow-ups do not become durable ADR clutter.
- blocker status: none; this is a maintenance tightening and does not change status, invocation posture, or technique dependencies.

## 2026-05-07 portability maintenance audit

- audit trigger: official OpenAI skill guidance emphasizes concise trigger metadata, progressive disclosure, and reusable self-contained skills; the core ADR skill should not activate only because project-local session or campaign language appears.
- evidence checked: official OpenAI skill docs and academy material, live `SKILL.md`, decision-boundary reference, trigger fixtures, and existing review records.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep the core trigger portable and evidence-oriented; keep project-specific session, checkpoint, campaign, and roadmap language as application examples or local overlays rather than primary activation law.
- blocker status: none; this is a portability tightening that preserves canonical status and default-reference posture.

## Recommendation

Keep `aoa-adr-write` as a canonical default reference and use this review record as the maintenance surface for future drift checks.
