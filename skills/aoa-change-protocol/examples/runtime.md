# Runtime Example

## Scenario

Update a public README line and a validator message after a wording contract changes in the repository.

## Why this skill fits

This is a non-trivial change because it touches documentation and validation-facing text, so it benefits from an explicit plan, scoped edits, and a clear verification step.

## Expected inputs

- target goal
- touched files or surfaces
- the main risk of the change
- the validation path to run after editing

## Expected outputs

- a small, reviewable diff
- a short verification note
- a concise final report that names what changed and what was checked

## Boundary notes

- Do not use this skill for a tiny typo fix with no meaningful review consequence.
- If the main question is whether the task is allowed at all, use the approval-gate skill first.
- If the main risk is operational rollback or preview behavior, use the dry-run-first skill instead.

## Verification notes

- Confirm the change was planned before editing.
- Confirm the diff stayed inside the declared scope.
- Confirm at least one explicit check was run or intentionally skipped with a reason.
- Confirm the final report names the outcome and any remaining risk.
