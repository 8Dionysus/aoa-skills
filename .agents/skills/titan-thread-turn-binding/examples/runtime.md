# Runtime Example

## Scenario

A bridge replay needs thread and turn ids bound to event and approval refs so continuity can be inspected.

## Why this skill fits

The request keeps bridge continuity inspectable by tying events and approvals to concrete turns.

## Expected inputs

- thread id
- turn id
- event ids or payloads
- receipt ref
- bridge or console state path

## Expected outputs

- thread-turn binding record
- scoped event list
- approval refs
- replay key
- continuity warning

## Boundary notes

- Turn binding preserves continuity evidence; it does not decide whether the work was correct.
- Missing turns should become repair prompts, not guessed continuity.
- Keep Titan artifacts subordinate to owner-repo validation and human judgment.
- Stop when approval, source refs, validation, or owner route is missing.

## Verification notes

- Confirm explicit Titan invocation or service-cohort request is present.
- Confirm lane and gate status are visible in the output.
- Confirm any receipt, ledger, source, replay, approval, or memory ref is preserved.
- Confirm the next owner-repo action is named when the skill output is not enough.
