# Runtime Example

## Scenario

A Titan service-cohort session needs `titan-memory-prune` to handle one bounded operator-visible step while preserving receipt, gate, and owner-route evidence.

## Why this skill fits

The request matches the skill boundary for Titan Memory Prune and can be handled without hidden agents, silent mutation, or source-of-truth transfer.

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

- Keep Forge mutation and Delta judgment gates explicit.
- Keep receipt, bridge, console, replay, and memory outputs subordinate to owner-repo validation.
- Stop when operator approval, source refs, or validation paths are missing.

## Verification notes

- Confirm the lane and gate status are visible in the output.
- Confirm any receipt or ledger ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
