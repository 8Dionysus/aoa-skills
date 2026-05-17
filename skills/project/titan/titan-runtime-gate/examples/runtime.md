# Runtime Example

## Scenario

The session wants to open Forge or Delta runtime lane and must match approval, receipt, target, and evidence before doing so.

## Why this skill fits

The request opens a locked Titan runtime lane only if approval, receipt, actor, and target match.

## Expected inputs

- receipt path
- requested Titan
- gate kind
- intent text
- operator approval ref

## Expected outputs

- updated gate state
- allowed or blocked decision
- receipt event
- lane summary
- next validation step

## Boundary notes

- A Forge gate cannot authorize Delta judgment, and a Delta gate cannot authorize Forge mutation.
- Runtime activation remains narrower than the broader session plan.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
