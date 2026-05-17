# Runtime Example

## Scenario

An operator wants a visible Titan lane dashboard that shows active Atlas, Sentinel, Mneme and locked Forge or Delta state.

## Why this skill fits

The request is an explicit Titan console view and needs lane status without changing gate authority.

## Expected inputs

- workspace root
- console state path
- receipt path
- operator intent
- lane updates or approval refs

## Expected outputs

- console state summary
- lane status table
- approval gate status
- digest candidate
- blocked-action notes

## Boundary notes

- A console view is not role authority or approval authority.
- Warnings should stay visible instead of being normalized into green state.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
