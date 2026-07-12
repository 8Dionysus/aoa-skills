## Prompt

The repo-local suite is already selected and exposes a reviewed evals/suites/example.suite.json sidecar; JIT-validate and run its exact typed invocation with environment and receipt capture.

## Expected selection

use

## Why

Decision: use `aoa-eval-apply`. JIT-validate the selected sidecar, execute only its exact typed runner, and preserve environment plus private receipt evidence.

## Expected object

An owner-validated application using the exact argv, cwd, timeout, and accepted exit codes, with source identity, environment capture, and an execution receipt.

## Boundary notes

Sidecar `ready` means source-contract readiness, not runtime reproducibility or proof acceptance. Inventory, readiness, dashboards, and MCP may route the contract but may not execute it.

## Verification hooks

Check JIT state, source head, sidecar digest, exact invocation, environment metadata, result, artifacts, generated drift, receipt privacy, and proof limits.
