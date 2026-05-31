# Validator Topology And Owner Modules

- Decision ID: AOA-SK-D-0029
- Status: Accepted
- Date: 2026-05-31
- Owner surface: `docs/validation/VALIDATOR_TOPOLOGY.md`,
  `docs/validation/COMMAND_AUTHORITY.md`,
  `docs/validation/validator_inventory.json`, `config/validation_lanes.json`,
  `scripts/validators/`

## Index Metadata

- Original date: 2026-05-31
- Surface classes: validation guard, agent route, generated/read-model,
  export/runtime
- Skill lanes: none
- Mechanic parents: audit, release-support, boundary-bridge
- Guard families: validator topology, owner module, CI lane, advisory report
- Posture: accepted validator owner-map split

## Context

The validator set had grown through waves of source, generated, export,
runtime, audit, report, and release work. Several root scripts still carried
large execution bodies, contract snippets, or duplicated constants even after
the growth-first CI split.

Future agents need an operational validator map before editing code. The map
must say what each validation-like surface protects, which input it reads, what
success proves, which lane calls it, whether it is blocking or advisory, and
where a failure should route.

## Decision

Create a validator topology surface under `docs/validation/`:

- `VALIDATOR_TOPOLOGY.md` is the human route map.
- `COMMAND_AUTHORITY.md` records the command storage balance between the lane
  manifest, Python callers, workflow YAML, and nearest `AGENTS.md` cards.
- `validator_inventory.json` is the machine-readable inventory used by tests to
  catch orphan validation-like entrypoints and hidden required checks.

Keep deterministic bulky validator execution in owner modules under
`scripts/validators/` while root `scripts/validate_*.py` and `scripts/lint_*.py`
entrypoints stay CLI adapters when the body is non-trivial.

Fold the old Pack 4 semantic AGENTS snippet check into
`scripts/validators/nested_agents_contract.json`; route-law contract data should
not live in a separate one-off Python validator.

Split the remaining root execution bodies into owner modules:

- `scripts/validators/tiny_router_surface.py`
- `scripts/validators/support_resource_surface.py`
- `scripts/validators/trigger_eval_surface.py`
- `scripts/validators/pack_profile_surface.py`

## Rationale

This matches the repository form: source skill meaning, generated/read-model
companions, portable exports, runtime seams, support-resource contracts,
skill-native evidence, and advisory reports are adjacent surfaces, not one
large validator.

The topology map keeps the positive route visible: role, input, output, owner,
lane, check, and next route. Tests guard against validator sprawl without
forcing every advisory report into required CI.

## Consequences

- Positive: root validation scripts are easier for Codex to scan.
- Positive: shared constants and execution phases live with their owner module.
- Positive: new validators must declare owner, lane, mode, and failure route.
- Tradeoff: the inventory must be updated when validation-like entrypoints move.

## Boundaries

This decision does not weaken source, generated, export, runtime, or release
checks.

It does not make advisory live-workspace reports required CI gates.

It does not move broad proof, scoring, or benchmark authority into this
repository.

## Validation

- `docs/validation/validator_inventory.json` records the current validator map.
- `tests/test_validator_topology.py` checks inventory shape, lane wiring, root
  CLI adapter thinness, and absence of orphan validation-like entrypoints.
- `config/validation_lanes.json` is the source of CI command sequencing;
  `scripts/validation_lanes.py` remains the Python loader/API.
