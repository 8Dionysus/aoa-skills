# AGENTS.md

## Applies to

This card applies to `mechanics/agon/` and every nested path until a nearer
`AGENTS.md` narrows the lane.

## Read before editing

Read the repository root `AGENTS.md`, `mechanics/AGENTS.md`, this card,
`README.md`, `DIRECTION.md`, `PARTS.md`, and `PROVENANCE.md` before changing
files in this lane. Open `legacy/README.md` only when the task needs old source
snapshots or migration accounting.

If the change touches candidate seed data, generated candidates, recurrence
manifests, or tests, read the affected part-local `config/` and `manifests/`,
root `generated/`, `scripts/`, and `tests/` surfaces too.

## Boundaries

- `mechanics/agon/` owns the skill-layer candidate bridge, local stop-lines,
  recurrence observation posture, and validation route for Agon-facing workflow
  candidates.
- It does not own Agon center law, lawful move vocabulary, proof verdicts,
  durable scars, routing sovereignty, role contracts, ToS canon, runtime
  activation, or downstream adoption truth.
- Candidate surfaces stay requested-only until normal skill review accepts a
  concrete bundle.

## Editing posture

- Change the active part first when behavior changes.
- Keep `README.md` as the package card and route, not a long archive.
- Keep `PARTS.md` focused on functioning part boundaries.
- Keep `PROVENANCE.md` focused on source route and moved-path accounting.
- Update `LANDING_LOG.md` when a checked landing changes.
- Update `ROADMAP.md` when future route pressure changes.
- Keep `legacy/` as lineage preservation only; never make it the current route.
- Do not update generated or recurrence surfaces without updating the owning
  source and running the named validators.

## Validation

The local narrow path includes `python mechanics/agon/parts/workflow-candidate-bridge/scripts/build_agon_skill_binding_candidates.py --check`
and `tests/test_mechanics_topology.py`.

```bash
python mechanics/agon/parts/workflow-candidate-bridge/scripts/build_agon_skill_binding_candidates.py --check
python mechanics/agon/parts/workflow-candidate-bridge/scripts/validate_agon_skill_binding_candidates.py
python mechanics/agon/parts/epistemic-candidate-boundary/scripts/build_agon_epistemic_skill_candidates.py --check
python mechanics/agon/parts/epistemic-candidate-boundary/scripts/validate_agon_epistemic_skill_candidates.py
python -m pytest -q mechanics/agon/parts/workflow-candidate-bridge/tests/test_agon_skill_binding_candidates.py mechanics/agon/parts/epistemic-candidate-boundary/tests/test_agon_epistemic_skill_candidates.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py
python scripts/validate_nested_agents.py
```

For broader docs or generated/export changes, also run the repository validation
path from root `AGENTS.md`.

## Closeout

Closeout must name changed active parts, whether candidate seed or generated
surfaces changed, whether recurrence manifests changed, checks run, checks
skipped, remaining risk, and the next owner route if this package was only a
waypoint.
