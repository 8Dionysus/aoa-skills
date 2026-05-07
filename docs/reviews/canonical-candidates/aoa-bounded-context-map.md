# aoa-bounded-context-map candidate review

## Current status

- current maturity status: `canonical`
- canonical promotion decision: promoted in this pass
- candidate set: canonical promotion completed
- scope: `core`
- current lineage: manifest-aligned to published techniques `AOA-T-0016` and `AOA-T-0002`

## Canonical gate check

- traceability heading: pass
- pending technique dependencies: pass
- pending `TBD` path or `source_ref`: pass
- evaluation coverage: pass
- explicit-only policy gate: not applicable
- overall canonical gate result: pass

## Evidence reviewed

- `skills/core/engineering/aoa-bounded-context-map/SKILL.md`
- `skills/core/engineering/aoa-bounded-context-map/references/boundary-lenses.md`
- `skills/core/engineering/aoa-bounded-context-map/references/context-map.template.md`
- `skills/core/engineering/aoa-bounded-context-map/techniques.yaml`
- `skills/core/engineering/aoa-bounded-context-map/examples/example.md`
- `tests/fixtures/skill_evaluation_cases.yaml`

## Findings

- trigger boundary stays crisp around boundary mapping rather than generic architecture rewrites
- contracts and verification guidance stay aligned with the boundary-scoping intent
- manifest-backed traceability and runtime wording are aligned
- the example reinforces the same bounded-context vocabulary without widening the skill into a full architecture review
- linked evidence, review evidence, and evaluation evidence are already covered by the repo-local canonical floor
- the skill now reads like a stable default-reference for boundary clarification work
- the trigger boundary now blocks broad architecture taxonomy or governance-program requests unless one concrete ambiguity-reduction pass is isolated
- the new compact context-map template gives agents a usable fallback shape without making local repositories inherit a global governance format
- the new boundary-lenses reference deepens the skill across owner, layer, surface-state, lifecycle, workflow/process, authority, portability, proof, runtime-facing, role, time, risk, and scale distinctions without making the core `SKILL.md` a long taxonomy
- the trigger fixtures now include both a multi-layer session/repository ambiguity and an exhaustive-lens misuse case

## Gaps and blockers

- no current blocker remains at the repository gate level
- future follow-up should preserve the default-reference rationale and review drift rather than reopen the promotion decision
- maintenance should stay comparative and not blur into a broader architecture review

## 2026-05-03 maintenance audit

- audit trigger: `aoa-techniques` now explicitly carries dual posture as standalone public library and ecosystem component, while mechanics work repeatedly needs owner splits across practice patterns, execution skills, evaluation artifacts, routing, scenarios, generated companions, and center law.
- evidence checked: `Agents-of-Abyss` federation rules and repo roles; `aoa-techniques` charter, technique atom/topology contracts, mechanics atlas, and active package cards.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep the skill canonical and strengthen it around layer/owner boundaries, portable-versus-integration wording, stop-lines, and handoffs to stronger owners.
- blocker status: none; the update does not change status, scope, or invocation posture.

## 2026-05-07 maintenance audit

- audit trigger: skill-level audit found that bounded-context mapping could still be over-invoked for broad architecture programs, despite being meant for one concrete ambiguity or scoping problem.
- evidence checked: live `SKILL.md`, new compact context-map template, trigger-evaluation fixture coverage, generated runtime router hints, and status-promotion review sync.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep the skill canonical, add the broad-architecture stop-line, make the first procedure step narrow the task before mapping, and provide a small fallback template only when no repo-local map shape exists.
- blocker status: none; this is a maintenance tightening, not a status or scope promotion.

## 2026-05-07 lens-depth maintenance audit

- audit trigger: follow-up review found that project-wide use needs more diverse, reusable boundary lenses without turning the skill into a narrow AoA-specific case catalog.
- evidence checked: `Agents-of-Abyss` federation and layer surfaces, sibling repo route cards, `aoa-skills` architecture and boundary-bridge docs, upstream technique `AOA-T-0016`, live `SKILL.md`, boundary-lenses reference, context-map template, trigger fixtures, generated export, and quality audit.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: keep the core skill compact, add a reference-based lens grammar for diverse contexts, require only the smallest useful lens set, and explicitly reject exhaustive lens application without a concrete ambiguity.
- blocker status: none; the update keeps canonical status and invocation posture intact.

## 2026-05-07 portability maintenance audit

- audit trigger: official OpenAI skill guidance reinforced that broad skill triggers should stay concise and portable, with domain-specific detail loaded through references only when the task needs it.
- evidence checked: official OpenAI skill docs and academy material, live `SKILL.md`, `boundary-lenses.md`, example, trigger fixtures, generated export, and quality audit.
- runtime `SKILL.md` meaning changed: yes, boundedly.
- decision: replace project-specific trigger language with reusable component/layer/surface language, keep the diverse AoA topology as stress-test context, and keep exact local routes in overlays or references.
- blocker status: none; canonical status and invocation posture stay intact.

## Recommendation

Keep `aoa-bounded-context-map` as a canonical default reference and use this review record as the maintenance surface for future drift checks.
