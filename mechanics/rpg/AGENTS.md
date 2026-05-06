# AGENTS.md

## Applies to

This card applies to `mechanics/rpg/` and every nested path until a nearer
`AGENTS.md` narrows the lane.

## Read before editing

Read the repository root `AGENTS.md`, `mechanics/AGENTS.md`, this card,
`README.md`, `DIRECTION.md`, `PARTS.md`, and `PROVENANCE.md` before changing
files in this lane.

If the change touches ability schemas, generated ability examples, pack
profiles, overlays, progression artifacts, or skill bundles, read those
affected surfaces too.

## Boundaries

- `mechanics/rpg/` owns the `aoa-skills` side of ability-reader and loadout
  posture around existing skill bundles.
- It does not own hidden ontology, runtime ledger state, role canon, skill
  truth, playbook choreography, proof verdicts, quest closure, memory canon,
  routing authority, owner acceptance, or automatic skill promotion.
- Ability cards and loadout hints remain reader surfaces below canonical skill
  bundles.

## Editing posture

- Change the active part first when behavior changes.
- Keep `README.md` as the package card and route.
- Keep `PARTS.md` focused on functioning part boundaries.
- Keep `PROVENANCE.md` focused on moved-path accounting, generated ability
  companions, pack/profile sources, and owner routes.
- Update `LANDING_LOG.md` when a checked landing changes.
- Update `ROADMAP.md` when future RPG pressure changes.

## Validation

The local narrow path includes generated ability schema validation, mechanics
topology, and nested route validation.

```bash
python -m pytest -q tests/test_generated_surface_schemas.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py
python scripts/validate_nested_agents.py
```

For broader docs, generated, export, or skill-bundle changes, also run the
repository validation path from root `AGENTS.md`.

## Closeout

Closeout must name changed active parts, whether generated ability surfaces or
schemas changed, whether skill meaning changed, checks run, checks skipped,
remaining risk, and the next owner route if this package was only a waypoint.
