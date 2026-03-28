# Evaluation Snapshot
## Prompt
In an abyss repository, choose between a bounded operational mutation and a sanitized sharing pass because the real work is changing runtime configuration rather than preparing a shareable artifact.
## Expected selection
use
## Why
This is an operational mutation with repo-relative commands and rollback posture, not a sharing-first task.
## Expected object
This is an abyss-safe-infra-change case, not an abyss-sanitized-share case.

A bounded local infra-change note that keeps repo-relative operational surfaces, commands, and rollback posture explicit.
## Boundary notes
Use `abyss-sanitized-share` only when the real task is preparing a safe shareable artifact from raw material.
## Verification hooks
The response should prefer the bounded infra-change path and keep sharing logic out of the main recommendation.
