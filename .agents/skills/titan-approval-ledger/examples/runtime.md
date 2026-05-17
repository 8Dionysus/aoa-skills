# Runtime Example

## Scenario

An operator explicitly approves one Forge mutation or Delta judgment gate and needs a ledger record that will not become owner truth.

## Why this skill fits

The request is about recording one explicit approval seam, not deciding role truth or executing the approved work.

## Expected inputs

- receipt or ledger reference
- approved Titan lane
- gate kind
- operator intent text
- scope and validation expectation

## Expected outputs

- approval record candidate
- gate kind and target lane
- source refs for the receipt or ledger
- stop note when the approval is missing or ambiguous

## Boundary notes

- Do not let an approval record execute the approved mutation or judgment.
- Do not reuse one approval across another actor, target, or gate kind.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
