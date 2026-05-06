# Questbook Landing Log

## 2026-05-06 - Root Index Alignment

Moved the public tracked obligation index to root `QUESTBOOK.md` so this
package can stay a mechanic route rather than the public quest index itself.

Changed route:

- root `QUESTBOOK.md` is the compact public obligation index
- `mechanics/questbook/` owns integration posture, parts, provenance, roadmap,
  and generated projection boundaries
- `quests/`, schemas, and generated projections keep their existing source and
  read-model roles

Preserved stop-lines:

- no quest source object moved for symmetry
- no generated surface became authority
- no package roadmap became the public quest index

## 2026-05-06 - Integration Posture Slice

Landed the first `aoa-skills` questbook package around skill-layer questbook
integration and session-harvest posture.

Changed route:

- moved questbook integration guidance out of flat `docs/`
- added package card, direction, parts, provenance, active docs map, and three
  active parts
- updated validation source path for the integration note

Preserved stop-lines:

- the public obligation source was still inside the questbook package during
  this slice and is now root `QUESTBOOK.md`
- `quests/`, schemas, and generated projections stayed in place
- no generated surface became authority
- no quest closure, proof verdict, playbook choreography, memory canon, routing
  authority, or owner acceptance was claimed

Checks:

- `python -m pytest -q tests/test_validate_skills.py tests/test_session_checkpoint_note.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py`
- `python scripts/validate_nested_agents.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_skills.py --fail-on-review-truth-sync`
- `python -m pytest -q tests/test_session_growth_kernel_maturity.py tests/test_session_checkpoint_note.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py`
