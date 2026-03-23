# Evaluation Snapshot

## Prompt
Bring up a local multi-service stack after choosing a profile that changes what starts and requires host readiness checks before launch.

## Expected selection
use

## Why
The task needs a bounded local bring-up workflow with pre-start render review, readiness checks, and one explicit launch path.

## Expected object
Rendered runtime truth, a readiness verdict, and one explicit launch recommendation for the selected local stack.

## Boundary notes
This stays inside local stack bring-up rather than widening into remote deployment, generic bootstrap, or continuous monitoring.

## Verification hooks
- renders what would actually start before launch
- reports selector-aware readiness findings
- keeps launch explicit and names the stop path
- reports blockers, warnings, or deferred follow-up
