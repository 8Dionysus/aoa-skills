# Runtime Example

## Scenario

A Titan service-cohort session is ending and needs a receipt-linked summary of roles, gates, provenance, validation, and next owner steps.

## Why this skill fits

The request is a session closeout surface and must preserve evidence boundaries before later owner review.

## Expected inputs

- receipt path
- operator summary
- gates used
- validation evidence
- memory candidates and owner-route hints

## Expected outputs

- closed receipt or closeout packet
- role and boundary summary
- gate summary
- verification status
- next owner-repo action

## Boundary notes

- Closeout can recommend owner moves; it cannot promote memory, proof, or role truth.
- Missing validation should remain visible as unfinished owner follow-up.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
