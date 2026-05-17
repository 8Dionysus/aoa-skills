# Runtime Example

## Scenario

An operator wants an app-server launch plan for Titan runtime surfaces, but no runtime process should start yet.

## Why this skill fits

The request needs a plan artifact before runtime starts, so dry-run and mutation-gate posture stay visible.

## Expected inputs

- workspace root
- console or bridge state ref
- desired endpoint or transport shape
- receipt path
- operator intent

## Expected outputs

- JSONL launch-plan entries
- required prechecks
- approval gates
- non-execution reminder
- validation command suggestion

## Boundary notes

- Plan output is allowed; runtime start requires a separate explicit gate.
- Avoid hard-coding host-only paths when owner docs provide the current command.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
