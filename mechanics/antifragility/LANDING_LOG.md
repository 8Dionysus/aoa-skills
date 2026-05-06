# Antifragility Landing Log

## 2026-05-06 - Fallback, Pruning, And Collision Stress Slice

Landed the first `aoa-skills` antifragility package around local risk posture
for existing skill canon.

Changed route:

- moved fallback authoring guidance out of flat `docs/`
- moved via negativa pruning guidance out of flat `docs/`
- moved collision stress guidance out of flat `docs/`
- added package card, direction, parts, provenance, landing log, roadmap, and
  three active parts

Preserved stop-lines:

- skill bundles stayed under `skills/`
- generated trigger, description, and tiny-router surfaces stayed in place
- risk-ring and policy config stayed in place
- rollback drill stayed in `docs/` for a later release-support or experience
  pass
- no deletion authority, runtime rollback, proof verdict, routing sovereignty,
  release approval, owner-local cleanup, or automatic skill promotion was
  claimed

Checks:

- `python scripts/lint_trigger_evals.py --repo-root .`
- `python scripts/lint_description_trigger_evals.py --repo-root .`
- `python scripts/validate_tiny_router_inputs.py --repo-root .`
- `python scripts/validate_nested_agents.py`
- `python -m pytest -q tests/test_mechanics_topology.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py`
