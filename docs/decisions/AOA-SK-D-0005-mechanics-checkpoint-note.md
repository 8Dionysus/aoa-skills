# Mechanics Checkpoint Note

- Decision ID: AOA-SK-D-0005

## Index Metadata

- Original date: 2026-05-06
- Surface classes: mechanic package
- Skill lanes: none
- Mechanic parents: checkpoint
- Guard families: source topology
- Posture: accepted checkpoint note posture

Date: 2026-05-06

Status: accepted

## Context

After Agon and Method-growth landed as local mechanics packages, the next
bounded flat-doc surface was the checkpoint-note path. Direct reading showed it
is not session-growth kernel meaning and not method-growth candidate identity.
It is the pre-harvest checkpoint protocol and the bridge boundary into explicit
reviewed closeout.

The canonical bridge workflow remains the `aoa-checkpoint-closeout-bridge`
skill. The schema and example remain under `schemas/` and `examples/`.

## Decision

Create `mechanics/checkpoint/` and land only the checkpoint-note slice:

- `docs/CHECKPOINT_NOTE_PATH.md` -> `mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md`

Add a package card, direction, parts, provenance, landing log, roadmap, active
docs map, and active parts for checkpoint-note lane and closeout bridge
boundary.

Do not move the bridge skill, session-growth kernel maturity, method-growth
candidate lineage, questbook, SDK controls, or runtime checkpoint exports in
this slice.

## Consequences

- The docs root no longer owns checkpoint-note protocol.
- `mechanics/checkpoint/` becomes the local route for provisional checkpoint
  carry and reviewed closeout bridge boundaries.
- Checkpoint notes remain weaker than donor harvest, progression lift, quest
  harvest, memory, proof, runtime, stats, and owner acceptance.
- Runtime-produced checkpoint notes remain evidence, not source truth.

## Verification

Verification covered checkpoint-note and session-growth maturity behavior,
mechanics routes and topology, nested agent cards, and the repository test
suite.
