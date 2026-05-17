# Runtime Example

## Scenario

A receipt or bridge event should become recallable later as candidate memory with source refs and confidence.

## Why this skill fits

The request creates candidate memory for later recall while keeping source refs and authority limits visible.

## Expected inputs

- receipt or event source
- bearer id or Titan name
- source refs
- confidence note
- redaction or retention hints

## Expected outputs

- candidate remembrance record
- recall authority warning
- source and confidence fields
- redaction or tombstone candidates
- digest note

## Boundary notes

- Candidate memory must not become canon by being recallable.
- Sensitive entries need retention or redaction review before reuse.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
