# Evaluation Snapshot

## Prompt
Find which existing AoA decision explains a boundary before editing the related source surface.

## Expected selection
use

## Why
The task is to discover existing rationale before making a source change.

## Expected object
A compact decision lookup that verifies graph matches against source notes.

## Boundary notes
This is an aoa-decision-find case because the expected output is evidence and source-backed context, not a new note.

## Verification hooks
- use graph or generated-index lookup first
- inspect matching repo-local source notes
- downgrade confidence when graph issues are present
