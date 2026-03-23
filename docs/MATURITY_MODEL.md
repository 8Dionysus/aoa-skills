# Maturity model

This document defines the current public maturity ladder for `aoa-skills`
and the minimum evidence expected before a skill changes status.
The repository currently has a mixed-status public surface with canonical, evaluated, scaffold, and overlay-shaped surfaces already represented.

## Status ladder

### `scaffold`

The skill shape exists and is public-safe, but it is still early.
Typical characteristics:
- bounded `SKILL.md`
- honest `techniques.yaml`
- first support artifact
- no claim yet that the skill is strongly reviewed or evaluation-backed

### `linked`

The skill has honest bridge metadata and pinned upstream source refs.
Typical characteristics:
- manifest shape passes schema-backed validation
- published techniques are pinned to concrete upstream refs
- pending techniques remain explicitly pending
- runtime text and manifest no longer drift silently by omission
- machine-checkable floor: validator-enforced bridge metadata honesty for published and pending technique refs

### `reviewed`

The skill has passed an explicit human review of meaning and boundaries.
Typical characteristics:
- trigger boundary is sharp
- contracts, risks, and verification guidance are coherent
- traceability and runtime wording do not silently conflict
- policy stance matches operational risk
- machine-checkable floor: review evidence exists either in-bundle or as a public review record

### `evaluated`

The skill has behavior-oriented evidence beyond static shape checks.
Typical characteristics:
- autonomy or self-contained runtime checks exist
- trigger-boundary fixtures or similar evaluation evidence exist
- snapshot-backed coverage or equivalent matrix-backed evidence exists
- evidence is strong enough to catch boundary mistakes, not only formatting drift

For reading the evidence itself, use `docs/EVALUATION_PATH.md`.
For the current derived evidence surface, read `../generated/skill_evaluation_matrix.md`.

### `canonical`

The skill is a recommended reusable public reference for its workflow class.
Typical characteristics:
- it is already `linked`, `reviewed`, and `evaluated`
- its meaning is stable enough for broad reuse
- it has explicit promotion rationale
- it is treated as a reference surface, not just a good scaffold

### `deprecated`

The skill remains in the repository for lineage or migration context,
but should not be the default choice for new use.

## Promotion rules

- Status changes must be explicit in the PR description and final report.
- Promotions should normally move one step at a time.
- If a PR proposes skipping a step, it must explain why the missing evidence is already covered elsewhere.
- No skill should become `canonical` without already satisfying the expectations of `linked`, `reviewed`, and `evaluated`.
- `deprecated` should explain what supersedes the skill or why it should no longer be used as the default.

## Canonical gate checks

Before a skill can move to `canonical`, it should pass these repository-level gates:
- `SKILL.md` uses `## Technique traceability`, not `## Future traceability`
- frontmatter `technique_dependencies` contains no `AOA-T-PENDING-*`
- `techniques.yaml` contains no pending IDs and no `path: TBD` or `source_ref: TBD`
- evaluation coverage exists in `tests/fixtures/skill_evaluation_cases.yaml`:
  one autonomy check
  at least one `use` trigger case
  at least one `do_not_use` trigger case
- if the skill is `explicit-only`, existing validator policy checks must still pass

These gates do not promote a skill by themselves.
They define the minimum machine-checkable floor before canonical promotion is even considered.

## Machine-checkable floors vs human decisions

The validator can enforce repository-level maturity floors for statuses such as `linked`, `reviewed`, and `canonical`.
That does not replace human review or promotion judgment.

- machine checks answer: "is the minimum repository evidence floor present?"
- human review still answers: "is this skill actually mature enough to deserve the status change?"

## Promotion evidence checklist

Use this checklist when proposing any status change beyond `scaffold`:
- bridge metadata is current and honest
- runtime selection and inspection stay separate from public-product signaling
- runtime `SKILL.md` remains self-contained
- evaluation evidence is readable in `docs/EVALUATION_PATH.md`
- the derived evaluation matrix in `../generated/skill_evaluation_matrix.md` matches the current fixtures and snapshot cases
- trigger boundary is still crisp
- contracts, risks, and verification guidance are still coherent
- support artifacts and evaluation evidence match the promoted claim
- invocation policy still matches the skill's risk surface
- public-product and governance signals remain readable in `docs/PUBLIC_SURFACE.md`

## First canonical candidates

The first canonical cohort was:
- `aoa-change-protocol` — promoted to `canonical`
- `aoa-tdd-slice` — promoted to `canonical`
- `aoa-approval-gate-check` — promoted to `canonical` after lineage closure and a separate default-reference decision

The next published-lineage promotion wave added:
- `aoa-bounded-context-map` — promoted to `canonical`
- `aoa-contract-test` — promoted to `canonical`
- `aoa-invariant-coverage-audit` — promoted to `canonical`
- `aoa-property-invariants` — promoted to `canonical`

The early canonical-candidate set is therefore no longer uniformly candidate-only.
Seven published-lineage core and risk skills now serve as `canonical` references.
The remaining candidate-ready skills stay `evaluated` until separate default-reference decisions are recorded.

## Review guidance for current candidates

For remaining canonical-candidate work, reviewers should explicitly assess:
- whether the trigger boundary is easy to apply correctly
- whether traceability and runtime wording still align
- whether the current fixtures catch meaningful misuse
- whether the policy stance is appropriate for the operational surface
- whether the skill is reusable beyond one project family without hidden assumptions
- whether the canonical gate checks are already satisfied without exceptions
- whether the review record clearly separates promotion blockers from drift-review follow-up
