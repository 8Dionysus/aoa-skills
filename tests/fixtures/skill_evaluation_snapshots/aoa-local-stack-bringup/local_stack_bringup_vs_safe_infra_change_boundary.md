# Evaluation Snapshot

## Prompt
Compare local multi-service stack bring-up with bounded infrastructure change planning and choose the clearer fit when the task is to render, check, and launch one selected local runtime.

## Expected selection
use

## Why
The task centers on local runtime composition, readiness review, and one explicit lifecycle path rather than on planning an infrastructure change in the abstract.

## Expected object
A reviewable local bring-up path with render review, readiness checks, and one explicit launch step.

## Boundary notes
This is a local-stack-bringup case, not a safe-infra-change case.

## Verification hooks
- render the selected runtime before launch
- report readiness before execution
- keep the result inside one bounded local lifecycle path
