# Runtime Example

## Scenario

Titan memory contains stale or sensitive candidate records and needs a reviewed retain, redact, tombstone, merge, or defer proposal.

## Why this skill fits

The request reviews memory retention or obsolescence without silently deleting or rewriting records.

## Expected inputs

- memory record id
- source refs
- reason for prune request
- retention rule
- operator or owner confirmation state

## Expected outputs

- redaction proposal
- tombstone proposal
- records to keep unchanged
- reason and source refs
- stop line for missing confirmation

## Boundary notes

- Prune recommendations are not deletions unless an owner-approved mutation follows.
- Tombstone and redaction decisions should preserve enough provenance for audit.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
