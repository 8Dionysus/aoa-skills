# Maturity model

This document defines the current public maturity ladder for `aoa-skills`
and the minimum evidence expected before a skill changes status.

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

### `reviewed`

The skill has passed an explicit human review of meaning and boundaries.
Typical characteristics:
- trigger boundary is sharp
- contracts, risks, and verification guidance are coherent
- traceability and runtime wording do not silently conflict
- policy stance matches operational risk

### `evaluated`

The skill has behavior-oriented evidence beyond static shape checks.
Typical characteristics:
- autonomy or self-contained runtime checks exist
- trigger-boundary fixtures or similar evaluation evidence exist
- evidence is strong enough to catch boundary mistakes, not only formatting drift

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

## Promotion evidence checklist

Use this checklist when proposing any status change beyond `scaffold`:
- bridge metadata is current and honest
- runtime `SKILL.md` remains self-contained
- trigger boundary is still crisp
- contracts, risks, and verification guidance are still coherent
- support artifacts and evaluation evidence match the promoted claim
- invocation policy still matches the skill's risk surface

## First canonical candidates

The first review set for future canonical promotion is:
- `aoa-change-protocol`
- `aoa-tdd-slice`
- `aoa-approval-gate-check`

These skills are candidates only.
They should not be promoted until review and evaluation evidence is captured explicitly.

## Review guidance for current candidates

For the first canonical-candidate pass, reviewers should explicitly assess:
- whether the trigger boundary is easy to apply correctly
- whether traceability and runtime wording still align
- whether the current fixtures catch meaningful misuse
- whether the policy stance is appropriate for the operational surface
- whether the skill is reusable beyond one project family without hidden assumptions
