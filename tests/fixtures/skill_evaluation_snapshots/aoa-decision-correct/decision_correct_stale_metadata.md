# Evaluation Snapshot

## Prompt
Correct stale index metadata and regenerate the decision indexes for an existing record.

## Expected selection
use

## Why
The task repairs an existing source record or its generated read models.

## Expected object
A source-first correction route that rebuilds local decision indexes and refreshes the graph.

## Boundary notes
This is an aoa-decision-correct case because the source record already exists and its metadata or read models are stale.

## Verification hooks
- inspect the source note first
- rebuild generated decision indexes when metadata changes
- compare the refreshed graph against the corrected source
