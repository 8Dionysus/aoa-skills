# Root Ingress Closure

- Decision ID: AOA-SK-D-0033
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `docs/validation/script_inventory.json`,
  `docs/validation/SCRIPT_TOPOLOGY.md`, `scripts/`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: source topology, validation guard, export/runtime
- Skill lanes: portable/export
- Mechanic parents: release-support, audit, boundary-bridge
- Guard families: script topology, validation command authority, release/CI
- Posture: accepted root-ingress closure

## Context

AOA-SK-D-0031 made `scripts/` tree-shaped by moving implementation into organ
directories while keeping root wrappers as compatibility ingress. AOA-SK-D-0032
then moved active lane command authority to organ paths.

That still left a broad flat root layer: many wrappers had no active in-repo
consumer after docs, tests, generated hints, and validators learned the organ
route. Keeping those wrappers would teach future agents that flat root script
paths are normal command owners.

## Options Considered

- Keep all root wrappers as long-lived compatibility paths.
- Delete every root wrapper and force all public consumers onto organ paths.
- Keep only evidenced public front doors, and retire the internal wrappers
  whose active references moved to organ paths.

## Decision

Root `scripts/*.py` compatibility ingress is limited to three public classes:

- lane front doors: `scripts/ci_gate.py`, `scripts/release_check.py`,
  `scripts/validation_lanes.py`
- runtime and activation front doors emitted by generated runtime or adapter
  surfaces
- bundle handoff front doors for stage, inspect, import, install, smoke, and
  verify workflows

All internal builder, validator, audit, report, refresh, receipt, adapter, and
skill-model tools run from organ paths. Direct organ commands use the explicit
contract `PYTHONPATH=scripts python scripts/<organ>/<tool>.py ...`; lane runners
inject that path automatically.

`docs/validation/script_inventory.json` now stores the allowlist with owner,
reason, downstream evidence, and retirement condition, plus a retired ingress
list for the removed wrappers and their organ targets.

## Rationale

The repo should expose a convex tree, not a flat script junk drawer with
implementation hidden behind wrappers. The public runtime, bundle, and lane
front doors still have generated or documented downstream evidence, so deleting
them would create avoidable consumer churn. The internal wrappers no longer had
that evidence after active surfaces migrated to organ paths.

This keeps compatibility where it protects a real route and removes it where it
only preserves habit.

## Consequences

- Positive: root `scripts/` now contains only `_ingress.py` plus 13 evidenced
  public compatibility wrappers.
- Positive: validators prevent new root wrapper sprawl without explicit owner,
  evidence, and retirement route.
- Positive: active docs, tests, generated hints, and lane command authority
  teach organ paths instead of root internal paths.
- Tradeoff: ad-hoc direct execution of retired root paths now fails; users must
  run the organ path with `PYTHONPATH=scripts` or use a lane front door.
- Follow-up: retire runtime, bundle, or lane root fronts only when their
  generated and downstream public contracts move.

## Current Applicability

As of 2026-06-04:

- Still valid: root ingress is compatibility, not implementation.
- Still valid: active command authority lives in `config/validation_lanes.json`
  and names organ paths.
- Still valid: historical decisions, changelogs, legacy captures, and landing
  logs may preserve old command evidence.
- Not superseded.

## Review Log

### 2026-06-04 - Root wrapper closure

- Previous assumption: internal root wrappers could stay as harmless
  compatibility while command authority used organ paths.
- New reality: after active docs, tests, generated hints, and validator
  contracts moved to organ paths, those wrappers became root topology noise.
- Reason: future agents should see the organ tree as the operating map.
- Source surfaces updated: `docs/validation/script_inventory.json`,
  `docs/validation/SCRIPT_TOPOLOGY.md`, `docs/validation/VALIDATOR_TOPOLOGY.md`,
  active route cards, tests, generated manifests, and root `scripts/`.
- Validation: focused script, validator, test-topology, runtime, tiny-router,
  and MCP-wiring tests passed before release-gate closeout.

## Boundaries

This decision does not rewrite historical records. It also does not claim that
runtime, bundle, or lane public root fronts should disappear before their
downstream contracts move.

## Validation

- `python -m pytest -q tests/test_script_topology.py`
- `python -m pytest -q tests/test_validator_topology.py tests/test_test_topology.py tests/test_script_topology.py tests/test_tiny_router_inputs.py tests/test_skills_ref_validation.py tests/test_validate_skills_generated_drift.py tests/test_component_refresh_law.py tests/test_runtime_seam_toolchain.py tests/test_runtime_guardrails_builder.py`
- `python -m pytest -q tests/test_validate_skill_mcp_wiring.py`
