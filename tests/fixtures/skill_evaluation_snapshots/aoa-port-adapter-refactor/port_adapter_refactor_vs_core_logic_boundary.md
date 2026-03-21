# Evaluation Snapshot

## Prompt
Compare a seam-making refactor with a core-versus-edge analysis and choose the clearer fit for a coupled dependency.

## Expected selection
use

## Why
The task is to reduce coupling by introducing or clarifying a port and adapter seam.

## Expected object
A seam, port, or adapter boundary that reduces coupling to the concrete dependency.

## Boundary notes
This is a port-adapter-refactor case, not a core-logic-boundary case.

## Verification hooks
- name the concrete dependency
- show the narrower seam
- avoid widening into a general boundary rewrite
