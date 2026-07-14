# Skill-effectiveness family review

This contract defines the current whole-family disposition layer for
`aoa-skills`.

## Use

Use the family review after quality, promotion-pressure, fixture, snapshot,
and reviewed live-episode surfaces have been inspected and every current skill
needs one explicit lifecycle decision.

The allowed dispositions are `improve`, `split`, `merge`, `promote`, `retain`,
and `retire`. Exactly one applies to each current skill in a review cycle.

## Evidence stages

Each row preserves separate posture for prompt visibility, selection,
load/read, procedure, verification, and bounded outcome. A clean later stage
does not manufacture an earlier one. Mentions and co-occurrence are recorded
only as non-authoritative signals.

Public live-dispatch receipts are reviewed candidate evidence. A clean
per-skill measure inside a cohort-level `needs-rerun` receipt may support that
bounded row, but it cannot become a clean cohort claim. Raw session content and
private traces stay outside the public record.

## Disposition semantics

- `improve` keeps the workflow boundary and records a bounded repair route.
- `split` proposes two or more bounded successor workflows and requires later
  owner review.
- `merge` names another current skill and requires a migration route.
- `promote` names a target maturity status and still requires the normal
  per-skill promotion surface.
- `retain` keeps the current boundary and status with an explicit revisit
  condition.
- `retire` names a replacement route and still requires regression and
  migration evidence.

Name similarity, low usage, high mention counts, and generated pressure are
not sufficient by themselves for split, merge, promotion, or retirement.

## Current versus history

`docs/reviews/skill-effectiveness/aoa-family-current.json` is the current
source-exact register. Git history preserves prior cycles. The current record
must update when source membership, path, scope, status, or landed action state
changes.

## Authority

The record carries `proof_authority=false`, `promotion_authority=false`, and
`runtime_authority=false`. It does not replace source bundle meaning,
per-skill status review, `aoa-evals`, downstream owner adoption, or live runtime
admission.

## Contract surfaces

- schema: `mechanics/method-growth/schemas/skill_effectiveness_family_review_v1.json`
- current review: `docs/reviews/skill-effectiveness/aoa-family-current.json`
- decision: `docs/decisions/AOA-SK-D-0039-reviewed-skill-effectiveness-family-dispositions.md`
- validator owner: `scripts/validation/validators/skill_effectiveness_family_review_surface.py`
