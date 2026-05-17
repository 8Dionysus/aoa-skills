# Runtime Example

## Scenario

A later session asks what a Titan lane previously observed and needs candidate recall with source refs and authority warnings.

## Why this skill fits

The request retrieves candidate memory and must route any important claim back to source evidence.

## Expected inputs

- query text
- bearer id or Titan name
- memory index path
- time or session filter
- verification target

## Expected outputs

- matching remembrance records
- record ids and source refs
- authority warning
- confidence notes
- verification path

## Boundary notes

- Recall output is advisory until checked against source refs.
- Redacted or tombstoned entries should not be reconstructed from memory context.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
