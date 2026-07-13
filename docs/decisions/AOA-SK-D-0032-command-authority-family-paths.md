# Command Authority Family Paths

- Decision ID: AOA-SK-D-0032
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `config/validation_lanes.json`,
  `docs/validation/COMMAND_AUTHORITY.md`,
  `docs/validation/VALIDATOR_TOPOLOGY.md`, `scripts/lanes/`,
  `docs/validation/validator_inventory.json`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, source topology, workflow, generated/readout
- Skill lanes: none
- Mechanic parents: release-support, audit
- Guard families: validation command authority, script topology, release/CI
- Posture: accepted command-authority migration

## Context

AOA-SK-D-0031 moved script implementation into organ directories while keeping
root `scripts/*.py` files as thin compatibility ingress wrappers. That protected
historical commands, but the active lane manifest still named root wrapper paths.

The result was a half-migrated topology: source implementation was tree-shaped,
but command authority still taught future agents and CI to think of root
wrappers as the operational owners.

## Options Considered

- Keep root wrapper paths in `config/validation_lanes.json` until every external
  caller is retired.
- Delete root wrappers immediately and update all historical command evidence.
- Move active command authority to organ implementation paths while keeping root
  wrappers as explicit compatibility front doors.

## Decision

Blocking validation lane sequences name organ implementation paths, such as
`scripts/validation/validate_skills.py`,
`scripts/builders/build_catalog.py`,
`scripts/runtime/build_runtime_seam.py`, and
`scripts/lanes/release_check.py`.

`scripts/lanes/ci_gate.py` and `scripts/lanes/release_check.py` inject
`scripts/` into `PYTHONPATH` before executing organ commands, so lane execution
can call implementation modules directly without depending on root wrappers.

Root `scripts/*.py` wrappers remain compatibility ingress only. They do not own
lane command authority and should not be used as the source of active lane
semantics.

## Rationale

The tree-shaped script source home only becomes durable when the active command
surface also names the tree. Otherwise future agents see two competing truths:
implementation in organ directories and execution authority in root wrappers.

Keeping root wrappers avoids unnecessary downstream churn, but moving the lane
manifest and validator inventory to organ paths makes owner, route, and failure
analysis match the actual implementation surface.

## Consequences

- Positive: active CI/release lanes now execute family-scoped script paths.
- Positive: validator inventory describes implementation owners instead of
  compatibility wrappers.
- Positive: root wrappers can be retired later from evidence, not guesswork.
- Tradeoff: direct organ script commands need `PYTHONPATH=scripts` unless they
  are run through the lane runners.
- Follow-up: after downstream command evidence is migrated, shrink the root
  ingress allowlist in `docs/validation/script_inventory.json`.

## Current Applicability

As of 2026-06-03:

- Still valid: root wrappers exist for compatibility, not authority.
- Still valid: lane command sequences live in `config/validation_lanes.json`.
- Changed: the manifest and validator inventory name organ implementation
  paths.
- Not superseded.

## Boundaries

This decision does not require rewriting historical decision records, changelog
entries, landing logs, or legacy captures that preserve old command evidence.
It does not claim that every external consumer has stopped using root wrapper
paths.

## Validation

Validation covered validator, release, and script topology tests; both lane
entrypoint help surfaces; and the `source-fast` lane.
