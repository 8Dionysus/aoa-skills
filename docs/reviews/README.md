# Review records

This folder stores public review records for repository-level skill review work.

## Current use

- `canonical-candidates/` stores the current review records for skills being considered as future canonical references
- `status-promotions/` stores public review records for non-canonical status promotions such as `scaffold -> evaluated`
- the review records here are the human decision companion to `docs/PUBLIC_SURFACE.md`, `docs/governance/lanes.yaml`, and the derived governance surfaces in `generated/public_surface.md` and `generated/governance_backlog.md`

## Conventions

- review records are tracked, public repository artifacts
- a review record documents findings, evidence, blockers, and recommendation
- a review record does not change skill status by itself
- a review record should say whether the current machine-checkable floors pass
- a review record should say whether the explicit governance outcome is `default_reference` or `stay_evaluated`
- `candidate_ready` is a gate-pass signal only; the lane decision is the explicit governance outcome
- `stay_evaluated` is a valid recorded outcome, not a placeholder for missing work
- a review record should say whether the runtime `SKILL.md` meaning changed or only metadata/evidence changed
- a review record should name what still blocks the next status step
- candidate reviews should use `templates/CANDIDATE_REVIEW.template.md`
- status-promotion reviews should use `templates/STATUS_PROMOTION_REVIEW.template.md`

## Expected location

For canonical-candidate work, use:

`docs/reviews/canonical-candidates/<skill-name>.md`

For non-canonical promotion work, use:

`docs/reviews/status-promotions/<skill-name>.md`
