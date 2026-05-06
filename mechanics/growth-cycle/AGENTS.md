# AGENTS.md

## Applies to

This card applies to `mechanics/growth-cycle/` and every nested path until a
nearer `AGENTS.md` narrows the lane.

## Read before editing

Read the repository root `AGENTS.md`, `mechanics/AGENTS.md`, this card,
`README.md`, `DIRECTION.md`, `PARTS.md`, and `PROVENANCE.md` before changing
files in this lane.

If the change touches session-growth kernel config, receipt publisher scripts,
session-growth examples, checkpoint, method-growth, questbook, recurrence
manifests, generated surfaces, or tests, read those affected surfaces too.

## Boundaries

- `mechanics/growth-cycle/` owns the `aoa-skills` side of adaptive skill
  orchestration, closeout-versus-harvest separation, and session-growth kernel
  maturity guidance.
- It does not own canonical skill bundle meaning, checkpoint implementation,
  candidate identity, quest promotion authority, memory canon, proof verdicts,
  stats truth, runtime activation, or owner acceptance.
- Session-harvest notes under `docs/session-harvests/` remain evidence notes in
  this slice; do not move them unless the owner route for every note is clear.

## Editing posture

- Change the active part first when behavior changes.
- Keep `README.md` as the package card and route.
- Keep `PARTS.md` focused on functioning part boundaries.
- Keep `PROVENANCE.md` focused on source route, moved-path accounting, examples,
  manifests, and neighbor mechanics.
- Update `LANDING_LOG.md` when a checked landing changes.
- Update `ROADMAP.md` when future growth-cycle pressure changes.

## Validation

The local narrow path includes session-growth maturity, checkpoint, recurrence,
and mechanics topology tests.

```bash
python -m pytest -q tests/test_session_growth_kernel_maturity.py tests/test_session_checkpoint_note.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py
python scripts/validate_nested_agents.py
```

For broader docs, generated, export, recurrence manifest, or skill-bundle
changes, also run the repository validation path from root `AGENTS.md`.

## Closeout

Closeout must name changed active parts, whether canonical skill meaning
changed, whether examples/generated/recurrence surfaces changed, checks run,
checks skipped, remaining risk, and the next owner route if this package was
only a waypoint.
