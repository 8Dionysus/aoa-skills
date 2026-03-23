# aoa-approval-gate-check

## Current shape

- skill: `aoa-approval-gate-check`
- technique_count: `1`
- technique_ids:
  - `AOA-T-0028`
- composition_class: `single_technique_exception`

## Package rationale

This skill packages bounded approval classification into a reviewable agent
workflow. The skill layer matters because it standardizes how the approval gate
is applied, reported, and acted on.

## Why this is not just the technique

The technique describes the narrow checking practice. The skill adds the
workflow boundary around when to invoke the check, how to present the result,
and how to use it as an execution gate.

## Adjacent skills considered

- `aoa-dry-run-first`
- `aoa-safe-infra-change`
- `aoa-sanitized-share`

## Recommendation

- `keep_exception`
