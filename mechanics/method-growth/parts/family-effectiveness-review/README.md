# Family Effectiveness Review

## Use When

Use this part when the whole current skill family needs one reviewed lifecycle
disposition per skill after quality, promotion, and episode evidence has been
inspected.

## Do Not Use When

Do not use it for a single ordinary skill edit, as an automatic status
promoter, or as a substitute for proof, runtime admission, downstream owner
adoption, or per-skill status review.

## Route Check

Confirm current source membership first. Keep prompt visibility, selection,
load/read, procedure, verification, outcome, mentions, and co-occurrence
separate. Keep raw sessions private and route only public reviewed candidate
episode refs into the family record.

## Active Outputs

- `skill_effectiveness_family_review`

The output chooses exactly one `improve`, `split`, `merge`, `promote`,
`retain`, or `retire` disposition for every current skill and names the next
review condition.

## Next Route

Route bounded skill repair to its owner bundle, status movement to
`docs/reviews/status-promotions/`, canonical selection to
`docs/reviews/canonical-candidates/`, proof to `aoa-evals`, and downstream
adoption or runtime behavior to the corresponding owner repository.
