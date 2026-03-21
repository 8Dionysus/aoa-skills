# Evaluation Snapshot

## Prompt
Compare a test-first feature slice with a general change workflow and choose the clearer fit for a small behavior change.

## Expected selection
use

## Why
The task can be specified as a bounded behavior slice before implementation rather than a broad change workflow.

## Expected object
A small test-first slice with a limited implementation surface.

## Boundary notes
This is a tdd-slice case, not a change-protocol case.

## Verification hooks
- mention tests first
- keep the implementation surface limited
- avoid turning the slice into a general change program
