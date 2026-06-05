# Evaluation Snapshot

## Prompt
Compare correcting a stale or misindexed existing decision record with writing a new decision note and choose the clearer fit.

## Expected selection
use

## Why
The task repairs an existing source record or its generated read models.

## Expected object
A source-first correction route that rebuilds local decision indexes and refreshes the graph.

## Boundary notes
This is an aoa-decision-correct case, not an aoa-decision-create case.

## Verification hooks
- inspect the source note first
- rebuild generated decision indexes when metadata changes
- compare the refreshed graph against the corrected source
