# Evaluation Snapshot

## Prompt
Use the decisions graph to decide whether this docs/decisions task is a lookup, a new record, or a correction.

## Expected selection
use

## Why
The task is decision-lane work and the router should choose the smallest find, create, or correct path.

## Expected object
A route decision that selects one find, create, or correct path and uses the decision graph before broad repo reads.

## Boundary notes
This is an aoa-decision case because graph status and impact packets can narrow the route before source-note reads.

## Verification hooks
- check graph status and issue posture first
- choose exactly one subskill
- keep repo-local decision notes authoritative
