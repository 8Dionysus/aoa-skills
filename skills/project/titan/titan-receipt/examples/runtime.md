# Runtime Example

## Scenario

A Titan lane event, gate, or closeout step needs a receipt packet that acts as witness evidence.

## Why this skill fits

The request needs a witness packet that records state and evidence without becoming final truth.

## Expected inputs

- workspace root
- operator id
- receipt path
- note or closeout summary
- gate refs or validation command

## Expected outputs

- created or updated receipt
- validation result
- receipt note
- closeout state
- authority warning

## Boundary notes

- A receipt witnesses a state transition; it does not prove the transition was correct.
- Receipts should preserve unknowns instead of smoothing them away.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
