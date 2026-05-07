# Method-Growth Landing Log

## 2026-05-06 - Candidate Lineage Slice

Landed the first `aoa-skills` method-growth package around reviewed
candidate-lineage movement.

Changed route:

- moved candidate lineage and refinery contracts out of flat `docs/`
- moved owner-status and followthrough contracts out of flat `docs/`
- added package card, direction, parts, provenance, active docs map, and three
  active parts

Preserved stop-lines:

- no skill bundles moved into mechanics
- no generated surface became authority
- no `seed_ref` or `object_ref` minting was added
- no owner acceptance, proof verdict, memory canon, or runtime activation was
  claimed

Checks:

- `python -m pytest -q tests/test_session_checkpoint_note.py tests/test_session_growth_kernel_maturity.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py`
- `python scripts/validate_nested_agents.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_skills.py --fail-on-review-truth-sync`
- `python -m unittest discover -s tests`
- `python scripts/validate_agent_skills.py --repo-root .`
- `python scripts/build_agon_skill_binding_candidates.py --check`
- `python scripts/validate_agon_skill_binding_candidates.py`
- `python scripts/build_agon_epistemic_skill_candidates.py --check`
- `python scripts/validate_agon_epistemic_skill_candidates.py`
- `python scripts/validate_tiny_router_inputs.py --repo-root .`
- `python scripts/validate_support_resources.py --repo-root . --check-portable`

## 2026-05-06 - Adoption Lifecycle Slice

Landed the second `aoa-skills` method-growth slice around explicit adoption
lifecycle posture.

Changed route:

- preserved five repetitive v0.7 downstream adoption source docs as raw
  package-local legacy
- distilled active behavior into adoption boundary, adoption evidence receipts,
  retention/regression/retirement, and pattern adoption handoff parts
- kept governance v0.8 out of the method-growth slice; the relevant
  governance and experience surfaces now route through `mechanics/experience/`

Preserved stop-lines:

- no skill bundles moved into mechanics
- no downstream owner adoption was claimed
- no release approval, runtime activation, proof verdict, direct Tree-of-Sophia
  write, KAG-forced adoption, routing-layer meaning authorship, or automatic
  skill promotion was claimed

Checks:

- `python -m pytest -q tests/test_experience_wave3_seed_contracts.py tests/test_mechanics_topology.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py`
- `python scripts/validate_nested_agents.py`

## 2026-05-07 - Lived-Use Promotion Pressure

Landed a derived promotion-pressure readout so repeatedly used non-canonical
skills no longer depend on manual memory.

Changed route:

- added `docs/PROMOTION_PRESSURE.md`
- added `scripts/report_skill_promotion_pressure.py`
- added generated `skill_promotion_pressure` JSON and Markdown readouts
- linked promotion pressure from public-surface, promotion-path, maturity, and
  docs-map surfaces

Preserved stop-lines:

- no skill status changed
- no automatic canonical promotion was added
- runtime, session, hook, dispatch, and install evidence remain evidence
  companions, not authority
- project overlays route to owner adoption review rather than core canonical
  promotion

Checks:

- `python scripts/report_skill_promotion_pressure.py --repo-root . --workspace-root /srv/AbyssOS --format markdown`
- `python -m pytest -q tests/test_skill_promotion_pressure.py`
