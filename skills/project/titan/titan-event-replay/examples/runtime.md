# Runtime Example

## Scenario

A bridge event stream must be replayed after interruption so reviewers can inspect derived state and source gaps.

## Why this skill fits

The request reconstructs reviewable state from saved events while keeping replay derived and non-authoritative.

## Expected inputs

- event log path
- optional current state path
- thread or turn filter
- receipt ref
- expected replay target

## Expected outputs

- replayed state summary
- event order report
- differences from current state
- authority warning
- next verification step

## Boundary notes

- Replay is derived evidence and cannot open a gate by itself.
- Ordering gaps should remain explicit even when the replay is useful.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
