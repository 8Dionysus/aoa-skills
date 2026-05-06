# AGENTS.md

## Applies to

This card applies to `mechanics/method-growth/` and every nested path until a
nearer `AGENTS.md` narrows the lane.

## Read before editing

Read the repository root `AGENTS.md`, `mechanics/AGENTS.md`, this card,
`README.md`, `DIRECTION.md`, `PARTS.md`, and `PROVENANCE.md` before changing
files in this lane.

If the change touches reviewed owner-landing schemas, route-followthrough
examples, adoption schemas/examples, session-growth examples, project-core
kernel surfaces, generated outputs, or tests, read those affected surfaces too.

## Boundaries

- `mechanics/method-growth/` owns the `aoa-skills` side of candidate lineage,
  first reviewed owner-status landing, governed followthrough after
  `candidate_ref` exists, and explicit adoption lifecycle posture.
- It does not own center method-growth law, seed truth, final object truth,
  proof verdicts, memory canon, playbook choreography, runtime activation, or
  owner acceptance for another repository.
- Skill bundles stay under `skills/`. This package may route skill-shaped
  candidate movement, but it must not become a second skill tree.

## Editing posture

- Change the active part first when behavior changes.
- Keep `README.md` as the package card and route.
- Keep `PARTS.md` focused on functioning part boundaries.
- Keep `PROVENANCE.md` focused on source route, moved-path accounting, raw
  legacy accounting, schema companions, and neighbor surfaces.
- Update `LANDING_LOG.md` when a checked landing changes.
- Update `ROADMAP.md` when future method-growth pressure changes.
- Do not move session-growth, checkpoint, governance, proof, or quest surfaces
  into this package unless the package route can name the stop-line and
  validation for that exact slice.

## Validation

The local narrow path includes the owner-landing and growth-kernel tests plus
mechanics topology.

```bash
python -m pytest -q tests/test_session_checkpoint_note.py tests/test_session_growth_kernel_maturity.py tests/test_experience_wave3_seed_contracts.py tests/test_roadmap_parity.py tests/test_mechanics_topology.py
python scripts/validate_nested_agents.py
```

For broader docs, generated, export, or skill-bundle changes, also run the
repository validation path from root `AGENTS.md`.

## Closeout

Closeout must name changed active parts, whether canonical skill meaning
changed, whether schemas/examples/generated surfaces changed, checks run,
checks skipped, remaining risk, and the next owner route if this package was
only a waypoint.
