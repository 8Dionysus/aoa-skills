# AGENTS.md

## Applies to

This card applies to `mechanics/antifragility/` and every nested path until a
nearer `AGENTS.md` narrows the lane.

## Read before editing

Read the repository root `AGENTS.md`, `mechanics/AGENTS.md`, this card,
`README.md`, `DIRECTION.md`, `PARTS.md`, and `PROVENANCE.md` before changing
files in this lane.

If the change touches trigger evals, description evals, tiny-router inputs,
risk-guard rings, runtime guardrails, support resources, release posture, or
skill bundles, read those affected surfaces too.

## Boundaries

- `mechanics/antifragility/` owns the `aoa-skills` side of fallback authoring,
  via negativa pruning, trigger-collision stress, and explicit risk posture
  around existing skill canon.
- It does not own skill bundle meaning, deletion authority, runtime rollback,
  proof verdicts, routing sovereignty, release approval, owner-local cleanup,
  or hidden mutation.
- Rollback drill and installation/release surfaces route through
  release-support or experience boundaries unless a later direct-read pass
  proves a narrower antifragility part.

## Editing posture

- Change the active part first when behavior changes.
- Keep `README.md` as the package card and route.
- Keep `PARTS.md` focused on functioning part boundaries.
- Keep `PROVENANCE.md` focused on moved-path accounting, trigger/eval
  companions, risk-ring surfaces, and owner routes.
- Update `LANDING_LOG.md` when a checked landing changes.
- Update `ROADMAP.md` when future antifragility pressure changes.

## Validation

The local narrow path includes mechanics topology, nested route validation, and
trigger-collision validation when the collision-stress part changes.

```bash
python -m pytest -q tests/test_mechanics_topology.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py
python scripts/lint_trigger_evals.py --repo-root .
python scripts/lint_description_trigger_evals.py --repo-root .
python scripts/validate_tiny_router_inputs.py --repo-root .
python scripts/validate_nested_agents.py
```

For broader docs, generated, export, support-resource, runtime, or skill-bundle
changes, also run the repository validation path from root `AGENTS.md`.

## Closeout

Closeout must name changed active parts, whether skill meaning changed, whether
trigger/generated/export surfaces changed, checks run, checks skipped, remaining
risk, and the next owner route if this package was only a waypoint.
