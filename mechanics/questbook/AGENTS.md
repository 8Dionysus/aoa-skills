# AGENTS.md

## Applies to

This card applies to `mechanics/questbook/` and every nested path until a
nearer `AGENTS.md` narrows the lane.

## Read before editing

Read the repository root `AGENTS.md`, `mechanics/AGENTS.md`, this card,
`README.md`, `DIRECTION.md`, `PARTS.md`, and `PROVENANCE.md` before changing
files in this lane.

If the change touches `mechanics/questbook/QUESTBOOK.md`, `quests/`, quest schemas, generated quest
catalogs, the quest-harvest skill, validators, or tests, read those affected
surfaces too.

## Boundaries

- `mechanics/questbook/` owns the `aoa-skills` side of questbook integration,
  session-harvest posture, source/index boundaries, and generated dispatch
  projection routes.
- It does not own a second roadmap, private scratchpad, playbook choreography,
  proof verdicts, memory canon, routing authority, closure proof, or owner
  acceptance.
- `mechanics/questbook/QUESTBOOK.md` and `quests/` remain source surfaces in this slice.

## Editing posture

- Change the active part first when behavior changes.
- Keep `README.md` as the package card and route.
- Keep `PARTS.md` focused on functioning part boundaries.
- Keep `PROVENANCE.md` focused on source route, moved-path accounting, schemas,
  generated companions, and neighbor mechanics.
- Update `LANDING_LOG.md` when a checked landing changes.
- Update `ROADMAP.md` when future questbook pressure changes.

## Validation

The local narrow path includes quest validation, checkpoint, and mechanics
topology tests.

```bash
python -m pytest -q tests/test_validate_skills.py tests/test_session_checkpoint_note.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py
python scripts/validate_nested_agents.py
python scripts/validate_skills.py --fail-on-review-truth-sync
```

For broader docs, generated, export, or skill-bundle changes, also run the
repository validation path from root `AGENTS.md`.

## Closeout

Closeout must name changed active parts, whether quest source surfaces changed,
whether generated quest projections changed, checks run, checks skipped,
remaining risk, and the next owner route if this package was only a waypoint.
