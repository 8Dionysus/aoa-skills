# Example

## Scenario

A local eval suite must be designed after no existing surface fits.

## Why this skill fits

- the behavior or invariant is explicit enough to evaluate
- deterministic checks should be planned before subjective graders
- the output is a local draft, not central proof acceptance

## Expected inputs

- target behavior or invariant
- existing local tests, scripts, validators, and fixtures
- evidence refs and rejected existing surfaces
- local eval-port path

## Expected outputs

- local suite or report design
- positive, negative, and regression cases
- deterministic check plan
- proof limit and owner handoff

## Boundary notes

- do not design around vague success criteria
- trace or rubric review is supporting, not the default
- central proof acceptance remains with `aoa-evals`

## Verification notes

- verify target invariant
- verify deterministic checks were considered first
- verify local owner path and proof limit
