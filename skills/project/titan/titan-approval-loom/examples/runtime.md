# Runtime Example

## Scenario

A bridge session has several pending approvals and needs a visible queue update before any Forge or Delta lane can open.

## Why this skill fits

The request is about queue posture and visible operator intent across approvals, not hidden execution.

## Expected inputs

- bridge state path
- thread id and turn id
- approval request id
- operator decision
- receipt or event refs

## Expected outputs

- updated approval queue entry
- decision event candidate
- gate status summary
- blocked-action note when approval is insufficient

## Boundary notes

- Treat the queue as runtime posture, not a policy source.
- Do not collapse expired, blocked, and allowed approvals into one status.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
