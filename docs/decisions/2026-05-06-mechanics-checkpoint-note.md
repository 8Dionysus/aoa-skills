# Mechanics Checkpoint Note

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

Verify with:

```bash
python -m pytest -q tests/test_session_checkpoint_note.py tests/test_session_growth_kernel_maturity.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py
python scripts/validate_nested_agents.py
python -m unittest discover -s tests
```
