# Evaluation Snapshot

## Prompt

Compare a full checkpoint-aware reviewed closeout chain with donor harvest alone when checkpoint hints already point to donor, progression, and quest follow-through.

## Expected selection

use

## Why

The route needs one reviewed closeout chain that treats checkpoint hints as
focus, rereads the reviewed artifact, and then runs the downstream skills in a
fixed order.

## Expected object

A closeout-context bundle that runs donor harvest, progression lift, and quest harvest in order from reviewed evidence.

## Boundary notes

This is a checkpoint-closeout-bridge case, not a donor-harvest-only case.

## Verification hooks

- confirm checkpoint notes remain provisional
- confirm the reviewed artifact is reread before harvest
- preserve the donor -> progression -> quest order
