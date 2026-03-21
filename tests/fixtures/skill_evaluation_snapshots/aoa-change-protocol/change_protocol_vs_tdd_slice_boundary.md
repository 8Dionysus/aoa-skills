# Evaluation Snapshot

## Prompt
Compare a bounded change workflow with a test-first slice and choose the clearer fit for a non-trivial repo change.

## Expected selection
use

## Why
The task is about a bounded change plan with explicit verification rather than a small test-first behavior slice.

## Expected object
An explicit plan and verification summary for the named change.

## Boundary notes
This is a change-protocol case, not a tdd-slice case.

## Verification hooks
- mention the change scope
- name a verification step
- avoid widening into test-first slice territory
