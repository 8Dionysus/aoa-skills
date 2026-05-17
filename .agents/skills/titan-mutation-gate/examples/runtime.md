# Runtime Example

## Scenario

Forge is asked to edit repository files and the session needs a fail-closed mutation gate before work begins.

## Why this skill fits

The request crosses toward Forge mutation and needs one explicit, receipt-linked gate before writes.

## Expected inputs

- intent text
- target repos and paths
- allowed actor
- precheck evidence
- validation command
- rollback or stop condition

## Expected outputs

- mutation gate packet
- allowed or blocked decision
- precheck summary
- validation expectation
- rollback or stop note

## Boundary notes

- The gate fails closed when target, approval, validation, or rollback posture is missing.
- The gate packet is not permission for extra mutations beyond the named target.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
