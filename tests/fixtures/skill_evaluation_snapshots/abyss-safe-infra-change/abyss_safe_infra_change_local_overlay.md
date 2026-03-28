# Evaluation Snapshot
## Prompt
Apply a bounded runtime or configuration change inside an abyss repository where repo-relative commands, local authority notes, and rollback checks still need to be named explicitly.
## Expected selection
use
## Why
The base `aoa-safe-infra-change` workflow is already correct, but the local repo still needs repo-relative operational surfaces, commands, and rollback posture named explicitly.
## Expected object
A bounded local infra-change note that keeps repo-relative operational surfaces, commands, and rollback posture explicit.
## Boundary notes
Use this overlay when the base infra-change workflow is right and the remaining work is a thin `abyss-*` local adaptation.
## Verification hooks
The response should name the repo-relative operational surface, keep local authority explicit, and preserve rollback thinking.
