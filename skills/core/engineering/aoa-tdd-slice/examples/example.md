# Example

## Scenario

A task-tracking service needs a new rule: creating a task with a title longer than 120 characters should fail with a validation error, while existing valid titles should continue to work unchanged.

## Why this skill fits

- the desired behavior is clear before implementation starts
- the change is small enough to stay inside one bounded slice
- confidence matters because the validation rule affects user-facing behavior

## Expected inputs

- the desired validation rule and the exact failure condition
- the module or service method that creates tasks
- the existing test surface for task creation behavior
- non-goals such as database migrations or UI redesign

## Expected outputs

- a failing test that expresses the new limit before implementation
- the smallest implementation change that makes the test pass
- a short verification summary naming the relevant passing tests

## Boundary notes

- this example is about a bounded behavior slice, not a broader rewrite of the validation framework
- unrelated cleanup such as renaming modules or changing API response shape stays out of scope

## Verification notes

- add or update the task-creation tests first
- run the focused test suite that covers valid and invalid title lengths
- report the covered behavior and note that unrelated task fields were left untouched
