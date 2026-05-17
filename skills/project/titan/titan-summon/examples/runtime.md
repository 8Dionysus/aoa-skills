# Runtime Example

## Scenario

The operator explicitly summons the first Titan service cohort for a local coding-agent session.

## Why this skill fits

The request starts the service cohort explicitly and keeps Forge and Delta locked until later gates.

## Expected inputs

- workspace root
- summon prompt reference
- operator intent
- receipt output path
- initial route question

## Expected outputs

- summon receipt candidate
- active and locked roster state
- route, risk, and memory posture summary
- gate status
- next move

## Boundary notes

- Summon activates service lanes only; it does not imply mutation or judgment permission.
- Owner docs remain stronger than the local receipt when posture conflicts.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
