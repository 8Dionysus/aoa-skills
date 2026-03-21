# Evaluation Snapshot
## Prompt
Update code and config for a non-trivial change with an explicit validation path.
## Expected selection
use
## Why
The change affects code, config, docs, or operational surfaces in a meaningful way, and the task benefits from an explicit plan and verification path.
## Expected object
A scoped change plan with a stated risk, bounded edit, and named verification step.
## Boundary notes
Use this skill for reviewable changes that need planning and verification. Do not use it for a tiny, consequence-free edit.
## Verification hooks
The response should mention the target surfaces, the main risk, and at least one concrete validation step.

