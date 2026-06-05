# Evaluation Snapshot

## Prompt
Compare routing decision-lane work through the workspace graph with writing a standalone ADR and choose the clearer fit when the task may be find, create, or correct.

## Expected selection
use

## Why
The task is to classify the decision-lane route before choosing the smaller operational skill.

## Expected object
A route decision that selects one find, create, or correct path and uses the decision graph before broad repo reads.

## Boundary notes
This is an aoa-decision case, not an aoa-adr-write case.

## Verification hooks
- choose one route
- use graph context before broad reads
- keep repo-local decision notes authoritative
