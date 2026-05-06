# Checkpoint Direction

This package starts with the smallest honest `aoa-skills` checkpoint slice:
checkpoint notes before reviewed harvest and the bridge boundary into explicit
closeout.

The active route is:

```text
checkpoint signal
  -> append-only provisional checkpoint note
  -> reviewed checkpoint note
  -> Dionysus promoted note or harvest handoff
  -> explicit checkpoint-closeout bridge
  -> explicit core ring skills
```

## Current contour

- Checkpoint notes may preserve `cluster_ref`, owner hints, evidence refs,
  status posture, and promotion conditions.
- Checkpoint notes may prepare a reviewed closeout route.
- Checkpoint notes do not mint `candidate_ref`.
- The bridge skill may use checkpoint hints as shortlist inputs only after a
  reviewed artifact exists.

## Boundaries

- Mid-session collection is not reviewed closeout execution.
- Bridge coordination does not replace donor harvest, progression lift, or
  quest harvest skill meaning.
- Stats refresh stays downstream of explicit closeout receipts.
- Runtime-produced checkpoint notes are evidence, not source truth.

## Current hold

Do not move session-growth maturity, method-growth candidate lineage, questbook,
or SDK checkpoint-control surfaces into this package during this slice.
