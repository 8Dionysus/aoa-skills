# Example

## Scenario

The user asks whether a repository already has an eval for a regression.

## Why this skill fits

- existing eval, validator, test, or script coverage may already answer the question
- local `evals/` and central `aoa-evals` need to be inspected before new work
- selection should produce fit, no-fit, or nearest-wrong-target evidence

## Expected inputs

- target repo and touched paths
- local `evals/PORT.yaml`
- nearby tests, validators, scripts, reports, and intake files
- central `aoa-evals` standards when relevant

## Expected outputs

- selected existing surface or no-fit classification
- rejected alternatives
- next route to apply, local need, design, or stop

## Boundary notes

- selection is read-first and may stop without mutation
- generated indexes and MCP packets remain weaker than source files
- central proof doctrine does not absorb local intake pressure

## Verification notes

- verify local port status
- verify the selected surface and owner route
- verify why nearest alternatives were rejected
