# Evaluation Snapshot

## Prompt
Compare local multi-service stack bring-up with authority classification and choose the clearer fit when the operator already intends to start a selected local runtime.

## Expected selection
use

## Why
The task is to render, check, and launch one selected local runtime rather than decide whether authority exists at all.

## Expected object
A reviewable local bring-up path with render review, readiness checks, and one explicit launch step.

## Boundary notes
This is a local-stack-bringup case, not an approval-gate-check case.

## Verification hooks
- render what would start before launch
- report selector-aware readiness findings
- keep the launch path explicit instead of reducing the task to authority classification
