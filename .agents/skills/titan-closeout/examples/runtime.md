# Runtime Example

## Scenario

A Titan service-cohort session needs `titan-closeout` to handle one bounded operator-visible step while preserving receipt, gate, and owner-route evidence.

## Why this skill fits

The request matches the skill boundary for Titan Closeout and can be handled without hidden agents, silent mutation, or source-of-truth transfer.

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

- Keep Forge mutation and Delta judgment gates explicit.
- Keep receipt, bridge, console, replay, and memory outputs subordinate to owner-repo validation.
- Stop when operator approval, source refs, or validation paths are missing.

## Verification notes

- Confirm the lane and gate status are visible in the output.
- Confirm any receipt or ledger ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
