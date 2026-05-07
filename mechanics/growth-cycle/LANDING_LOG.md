# Growth-Cycle Landing Log

## 2026-05-07 - Semantic Example Family Names

Reanchored active growth-cycle example names away from pass labels.

Changed route:

- renamed the pre-semantic example artifact directory to
  `session-growth-artifacts/`
- replaced pass-label example-family suffixes with
  `reviewed-donor-harvest`, `derived-visibility-handoff`, and
  `kernel-maturity`
- kept examples as evidence companions rather than skill truth, proof,
  scheduler state, or owner acceptance

Preserved stop-lines:

- no skill bundle moved into mechanics
- no example became promotion authority
- no generated surface became authority
- no proof, memory, runtime, owner acceptance, scheduler authority, or quest
  promotion was claimed

Checks:

- semantic legacy-pattern audit across growth-cycle, session-growth skills,
  generated surfaces, tests, and status-promotion reviews returned no matches
- `python -m json.tool mechanics/growth-cycle/examples/session_harvest_family.receipts.example.json >/dev/null && for f in mechanics/growth-cycle/examples/session-growth-artifacts/*.json; do python -m json.tool "$f" >/dev/null || exit 1; done`
- `python scripts/validate_skills.py --fail-on-review-truth-sync`
- `python scripts/build_catalog.py --check`
- `python scripts/build_runtime_seam.py --repo-root . --check`
- `python scripts/build_runtime_guardrails.py --repo-root . --check`
- `python scripts/build_tiny_router_inputs.py --repo-root . --check`
- `python scripts/validate_agent_skills.py --repo-root .`
- `python scripts/validate_support_resources.py --repo-root . --check-portable`
- `python scripts/validate_tiny_router_inputs.py --repo-root .`
- `python scripts/lint_trigger_evals.py --repo-root .`
- `python scripts/validate_nested_agents.py`
- `python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques --skill aoa-session-self-diagnose --skill aoa-session-self-repair --fail-on-drift`
- `python -m py_compile $(find scripts tests -name '*.py' | tr '\n' ' ')`
- `python -m pytest -q tests/test_session_growth_kernel_maturity.py tests/test_session_checkpoint_note.py tests/test_skill_evaluation.py tests/test_validate_skills.py tests/test_skill_quality_audit.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py`
- `python -m pytest -q tests`
- `python -m unittest discover -s tests`

## 2026-05-06 - Orchestration And Kernel Maturity Slice

Landed the first `aoa-skills` growth-cycle package around adaptive
orchestration and session-growth kernel maturity.

Changed route:

- moved adaptive orchestration guidance out of flat `docs/`
- moved session-growth kernel maturity guidance out of flat `docs/`
- added package card, direction, parts, provenance, active docs map, and three
  active parts
- updated recurrence component decision-surface refs to the package-local path

Preserved stop-lines:

- no skill bundles moved into mechanics
- no session-harvest notes moved in this slice
- no generated surface became authority
- no proof, memory, runtime, owner acceptance, scheduler authority, or quest
  promotion was claimed

Checks:

- `python -m pytest -q tests/test_session_growth_kernel_maturity.py tests/test_session_checkpoint_note.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py`
- `python scripts/validate_nested_agents.py`
- `python -m json.tool mechanics/recurrence/manifests/component.skills.bundle-and-activation-beacons.json`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_skills.py --fail-on-review-truth-sync`
- `python -m unittest discover -s tests`
- `python scripts/validate_agent_skills.py --repo-root .`
- `python scripts/validate_tiny_router_inputs.py --repo-root .`
- `python scripts/validate_support_resources.py --repo-root . --check-portable`
- `python scripts/build_agon_skill_binding_candidates.py --check`
- `python scripts/validate_agon_skill_binding_candidates.py`
- `python scripts/build_agon_epistemic_skill_candidates.py --check`
- `python scripts/validate_agon_epistemic_skill_candidates.py`
