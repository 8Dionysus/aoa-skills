# Example

## Scenario

A repo change may need an eval, but the owner route is unclear.

## Why this skill fits

- the task has eval-lane pressure, not only ordinary test work
- the next step is route selection before implementation
- central proof, local intake, MCP access, and session evidence must stay separate

## Expected inputs

- target repository and touched paths
- local `evals/PORT.yaml` and nearby validators
- central `aoa-evals` owner boundary
- any `.aoa` evidence refs only if session mining is being considered

## Expected outputs

- exactly one selected subskill route
- owner-boundary statement
- stop line when the safe owner surface is missing

## Boundary notes

- `aoa-eval` is a router, not a proof owner
- local intake pressure is weaker than central `aoa-evals` proof
- `.aoa` refs are candidate evidence only

## Verification notes

- verify that one route is chosen
- verify local and central owner surfaces are named
- verify no central proof file is written through an access plane
