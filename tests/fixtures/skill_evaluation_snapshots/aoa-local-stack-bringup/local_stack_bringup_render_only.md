# Evaluation Snapshot

## Prompt
Only render the composed local runtime for review; do not plan or start the stack yet.

## Expected selection
do_not_use

## Why
The request stays inspect-only and does not ask for a bounded local bring-up decision or launch path.

## Expected object
A deflection that keeps the work at render-only inspection or another narrower pre-start surface instead of a full bring-up workflow.

## Boundary notes
Do not widen an inspect-only render request into startup, readiness, or lifecycle control when no launch decision is being made.

## Verification hooks
- keeps the response inspect-only
- does not introduce a launch recommendation without a bring-up request
- names that the full bring-up skill would be too broad here
