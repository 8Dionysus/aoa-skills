# Example

## Scenario

An eval validator has already been selected and should be run.

## Why this skill fits

- the eval surface is selected before the skill starts
- the task is to apply the existing check and report evidence limits
- deterministic local commands are the smallest honest proof path

## Expected inputs

- selected command or eval surface
- owning repository and cwd
- expected artifacts or generated outputs
- prior failure or regression context

## Expected outputs

- command result and artifacts
- generated drift status
- scoped proof statement and remaining uncertainty
- next route if coverage is missing

## Boundary notes

- green output is scoped evidence, not central proof acceptance
- failed runs are evidence, not permission to guess
- broad release gates should not replace focused validators when one is enough

## Verification notes

- verify command, cwd, and result
- verify artifacts and generated drift
- verify proof limits and follow-up route
