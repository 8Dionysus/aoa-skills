# Evaluation Snapshot

## Prompt
Compare auditing existing checks with authoring property invariants and choose the clearer fit for a coverage review.

## Expected selection
use

## Why
The task is to review coverage strength for an already named stable truth.

## Expected object
An invariant coverage audit that names the stable truth, maps current checks to it, and isolates the smallest bounded gaps.

## Boundary notes
This is an invariant-coverage-audit case, not a property-invariants case.

## Verification hooks
- name the stable truth under review
- map current checks to it
- avoid writing new properties instead of auditing coverage
