# VIA_NEGATIVA_CHECKLIST

This checklist is for `aoa-skills` as the bounded execution workflows.

## Keep intact

- skills with explicit trigger boundaries and bounded outputs
- workflow steps that add execution value beyond the underlying technique
- clear risk and verification posture

## Merge, move, suppress, quarantine, deprecate, or remove when found

- skills that mostly paraphrase a technique
- skills that duplicate owner runbooks or source-of-truth docs
- skills with fuzzy trigger boundaries or overlapping purpose

## Questions before adding anything new

1. Does this skill own a bounded job, or is it just a renamed technique?
2. Could this be an addendum to an existing skill instead of a new skill?
3. Is the workflow actually crossing owner boundaries without an explicit
   handoff?

## Safe exceptions

- a new skill when the execution contract is materially new
- temporary migration wrappers with expiry

## Exit condition

- Every surviving skill should feel necessary, bounded, and non-redundant.
