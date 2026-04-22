# Runtime Example

## Scenario

A Titan service-cohort session needs `titan-approval-loom` to handle one bounded operator-visible step while preserving receipt, gate, and owner-route evidence.

## Why this skill fits

The request matches the skill boundary for Titan Approval Loom and can be handled without hidden agents, silent mutation, or source-of-truth transfer.

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

- Keep Forge mutation and Delta judgment gates explicit.
- Keep receipt, bridge, console, replay, and memory outputs subordinate to owner-repo validation.
- Stop when operator approval, source refs, or validation paths are missing.

## Verification notes

- Confirm the lane and gate status are visible in the output.
- Confirm any receipt or ledger ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
