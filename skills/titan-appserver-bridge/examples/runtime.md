# Runtime Example

## Scenario

A Titan service-cohort session needs `titan-appserver-bridge` to handle one bounded operator-visible step while preserving receipt, gate, and owner-route evidence.

## Why this skill fits

The request matches the skill boundary for Titan App-Server Bridge and can be handled without hidden agents, silent mutation, or source-of-truth transfer.

## Expected inputs

- workspace root
- bridge state path
- thread and turn identifiers
- event payloads or launch plan request
- approval and receipt refs

## Expected outputs

- bridge plan or state summary
- normalized event candidates
- approval queue status
- replay or metrics summary
- explicit non-execution note

## Boundary notes

- Keep Forge mutation and Delta judgment gates explicit.
- Keep receipt, bridge, console, replay, and memory outputs subordinate to owner-repo validation.
- Stop when operator approval, source refs, or validation paths are missing.

## Verification notes

- Confirm the lane and gate status are visible in the output.
- Confirm any receipt or ledger ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
