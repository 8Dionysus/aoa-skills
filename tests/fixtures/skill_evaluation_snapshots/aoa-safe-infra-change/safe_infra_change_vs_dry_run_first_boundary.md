# Evaluation Snapshot

## Prompt
Compare a bounded infrastructure change with preview-first planning and choose the clearer fit when the operational change itself is ready to be planned and verified.

## Expected selection
use

## Why
The task is to plan and verify the operational change itself, not to stop at a preview-first decision seam.

## Expected object
A bounded change plan or recommendation that names the operational surface, the validation path, and rollback or recovery notes.

## Boundary notes
This is a safe-infra-change case, not a dry-run-first case.

## Verification hooks
- name the operational surface
- include validation and rollback thinking
- avoid collapsing the task into preview-path selection alone
