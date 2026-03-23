# aoa-invariant-coverage-audit

## Current shape

- skill: `aoa-invariant-coverage-audit`
- technique_count: `1`
- technique_ids:
  - `AOA-T-0017`
- composition_class: `single_technique_exception`

## Package rationale

This skill packages an audit workflow around invariant coverage. It is a
bounded reviewable package for checking whether invariants are covered in the
right places and with the right evidence posture.

## Why this is not just the technique

The technique captures the narrow audit idea. The skill adds the operational
steps for deciding scope, checking coverage, and reporting the audit result as a
workflow output.

## Adjacent skills considered

- `aoa-property-invariants`
- `aoa-contract-test`
- `aoa-core-logic-boundary`

## Recommendation

- `keep_exception`
