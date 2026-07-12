# Example

## Scenario

A repo-local eval suite has already been selected. It exposes a reviewed JSON
sidecar and should run without letting readiness or MCP invent the command.

## Why this skill fits

- the eval surface is selected before the skill starts
- the task is to apply the existing check and report evidence limits
- deterministic local commands are the smallest honest proof path

## Expected inputs

- selected command or eval surface
- owning repository and cwd
- exact source tree/ref and the selected suite sidecar
- expected artifacts or generated outputs
- prior failure or regression context

## Expected outputs

- command result and artifacts
- JIT source validation state plus the exact validated argv/cwd/timeout
- environment capture and private execution receipt
- generated drift status
- scoped proof statement and remaining uncertainty
- next route if coverage is missing

## Boundary notes

- green output is scoped evidence, not central proof acceptance
- sidecar `ready` is source readiness, not pinned-runtime readiness
- inventory and MCP may route the suite but may not execute it
- failed runs are evidence, not permission to guess
- broad release gates should not replace focused validators when one is enough

## Verification notes

- verify JIT source validation immediately before execution
- run the exact validated argv and capture command, cwd, timeout, and result
- verify environment capture and a private execution receipt linked to source
  head and sidecar digest
- verify artifacts and generated drift
- verify the receipt records an execution and is not central proof acceptance
- verify proof limits and follow-up route
