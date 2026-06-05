# Evaluation Snapshot

## Prompt
Write a new decision record for a chosen MCP access-plane change.

## Expected selection
do_not_use

## Why
The task is to create source rationale, not merely find existing rationale.

## Expected object
A deflection toward aoa-decision-create because a source decision note must be written.

## Boundary notes
This is not an aoa-decision-find case once the requested output is a new repo-local decision note.

## Verification hooks
- route creation through aoa-decision-create
- read the target repo decision route card first
- rebuild local decision indexes after writing the source note
