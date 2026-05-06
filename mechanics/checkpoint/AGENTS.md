# AGENTS.md

## Applies to

This card applies to `mechanics/checkpoint/` and every nested path until a
nearer `AGENTS.md` narrows the lane.

## Read before editing

Read the repository root `AGENTS.md`, `mechanics/AGENTS.md`, this card,
`README.md`, `DIRECTION.md`, `PARTS.md`, and `PROVENANCE.md` before changing
files in this lane.

If the change touches checkpoint schemas, checkpoint examples, the
`aoa-checkpoint-closeout-bridge` skill, generated runtime surfaces, project
core kernel surfaces, or tests, read those affected surfaces too.

## Boundaries

- `mechanics/checkpoint/` owns the `aoa-skills` side of checkpoint-note
  protocol and the route boundary into explicit reviewed closeout.
- It does not own checkpoint implementation authority, memory canon, proof
  verdicts, stats truth, runtime activation, owner acceptance, hidden
  scheduling, or autonomous self-repair.
- The bridge skill remains canonical under `skills/aoa-checkpoint-closeout-bridge/`.
  This package may route to it, but must not copy its skill meaning into
  mechanics.

## Editing posture

- Change the active part first when behavior changes.
- Keep `README.md` as the package card and route.
- Keep `PARTS.md` focused on functioning part boundaries.
- Keep `PROVENANCE.md` focused on source route, moved-path accounting, schema
  companions, and neighbor surfaces.
- Update `LANDING_LOG.md` when a checked landing changes.
- Update `ROADMAP.md` when future checkpoint pressure changes.
- Do not move session-growth kernel, questbook, method-growth, or SDK control
  surfaces into this package unless the exact owner split is clear.

## Validation

The local narrow path includes the checkpoint and mechanics topology tests.

```bash
python -m pytest -q tests/test_session_checkpoint_note.py tests/test_session_growth_kernel_maturity.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py
python scripts/validate_nested_agents.py
```

For broader docs, generated, export, or skill-bundle changes, also run the
repository validation path from root `AGENTS.md`.

## Closeout

Closeout must name changed active parts, whether canonical skill meaning
changed, whether schemas/examples/generated surfaces changed, checks run,
checks skipped, remaining risk, and the next owner route if this package was
only a waypoint.
