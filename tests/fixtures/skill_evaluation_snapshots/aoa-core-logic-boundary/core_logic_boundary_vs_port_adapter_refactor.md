# Evaluation Snapshot

## Prompt
Compare a boundary-clarity task with a port/adapter refactor and choose the clearer fit for a mixed core and wiring module.

## Expected selection
use

## Why
The task is to separate reusable core logic from surrounding wiring or orchestration detail.

## Expected object
A boundary judgment that separates reusable core logic from adapter or wiring responsibilities.

## Boundary notes
This is a core-logic-boundary case, not a port-adapter-refactor case.

## Verification hooks
- name the stable core logic
- name the edge or wiring detail
- avoid pretending the refactor is only about ports
