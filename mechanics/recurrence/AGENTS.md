# AGENTS.md

## Applies to

This card applies to `mechanics/recurrence/` and every nested path until a
nearer `AGENTS.md` narrows the lane.

## Read before editing

Read the repository root `AGENTS.md`, `mechanics/AGENTS.md`, this card,
`README.md`, `DIRECTION.md`, `PARTS.md`, and `PROVENANCE.md` before changing
files in this lane.

If the change touches recurrence manifests, hook bindings, Agon recurrence,
component refresh law, generated recurrence outputs, or skill bundles, read
those affected surfaces too.

## Boundaries

- `mechanics/recurrence/` owns the `aoa-skills` side of recurrence observation,
  decision closure, and skill-pressure review routes.
- It does not own ambient continuity, automatic activation, automatic refresh,
  recursor spawn, memory sovereignty, proof verdicts, owner acceptance, or
  generated evidence as source truth.
- Recurrence manifests and hook bindings remain source/config surfaces in this
  slice.

## Editing posture

- Change the active part first when behavior changes.
- Keep `README.md` as the package card and route.
- Keep `PARTS.md` focused on functioning part boundaries.
- Keep `PROVENANCE.md` focused on moved-path accounting, manifests, hooks,
  Agon recurrence, and neighbor mechanics.
- Update `LANDING_LOG.md` when a checked landing changes.
- Update `ROADMAP.md` when future recurrence pressure changes.

## Validation

The local narrow path includes mechanics topology, recurrence JSON formatting,
and nested route validation.

```bash
python -m pytest -q tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py
python -m json.tool mechanics/recurrence/manifests/component.skills.bundle-and-activation-beacons.json
python -m json.tool mechanics/recurrence/manifests/hooks/component.skills.bundle-and-activation-beacons.hooks.json
python scripts/validate_nested_agents.py
```

For broader docs, generated, export, Agon, or skill-bundle changes, also run
the repository validation path from root `AGENTS.md`.

## Closeout

Closeout must name changed active parts, whether recurrence manifests or hooks
changed, whether skill meaning changed, checks run, checks skipped, remaining
risk, and the next owner route if this package was only a waypoint.
