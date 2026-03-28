# Evaluation Snapshot
## Prompt
In an abyss repository, choose between sanitizing a shareable artifact and changing runtime configuration because the main need is to publish a safe summary from raw local material.
## Expected selection
use
## Why
This is a sharing-first task with explicit local thresholds and a repo-relative destination, not an operational mutation.
## Expected object
This is an abyss-sanitized-share case, not an abyss-safe-infra-change case.

A sanitized local share artifact that names the repo-relative destination and explicit local sharing thresholds.
## Boundary notes
Use `abyss-safe-infra-change` only when the real task is the operational mutation itself rather than preparing the shareable result.
## Verification hooks
The response should prefer the sanitization path and avoid turning the answer into an execution plan for runtime mutation.
