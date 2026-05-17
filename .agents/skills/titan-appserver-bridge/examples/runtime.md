# Runtime Example

## Scenario

A Titan operator console needs a JSON-RPC shaped bridge over thread, turn, event, approval, replay, and metrics state.

## Why this skill fits

The request is about inspectable bridge state over existing events and approvals, not launching agents.

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

- A bridge relay can expose state; it cannot grant authority by itself.
- Keep generated metrics below receipts and event sources.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
