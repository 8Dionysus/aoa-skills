# Test Topology And Agentic Contracts

- Decision ID: AOA-SK-D-0030
- Status: Accepted
- Date: 2026-05-31
- Owner surface: `docs/testing/TEST_TOPOLOGY.md`,
  `docs/testing/test_inventory.json`, `tests/AGENTS.md`, `pytest.ini`,
  `config/validation_lanes.json`, `tests/support/`

## Index Metadata

- Original date: 2026-05-31
- Surface classes: validation guard, agent route, generated/readout, export/runtime
- Skill lanes: none
- Mechanic parents: agon, release-support
- Guard families: source topology, generated/read-model, export/runtime, AGENTS/mesh, release/tooling, evaluation/public surface
- Posture: accepted test topology split

## Context

The test tree had inherited the same pressure as the validators: large files,
historical wave names, duplicated fixture builders, release-validator replay
inside ordinary tests, and several exact-count assertions that treated today's
skill total as a durable truth.

`aoa-skills` needs tests that protect an agentic skill organ: source skill
contracts, generated/read-model drift, export/runtime seams, route-law, trigger
and router posture, release lane composition, and compact high-risk handoff
cases. It should not become a broad model-evaluation repository.

## Options Considered

- Keep the test suite mostly flat and document only the existing commands.
- Move broad evaluation and semantic checks into this repository.
- Split tests by owner surface, keep deterministic local contracts here, and
  make route/failure meaning explicit.

## Decision

Create an explicit test topology under `docs/testing/`.

`TEST_TOPOLOGY.md` records family, protected surface, owner truth, lane,
focused target, and failure route. `test_inventory.json` is the
machine-readable index that keeps discovered tests aligned with that map while
leaving commands to lane authority and `tests/AGENTS.md`. `pytest.ini` carries the
small marker vocabulary for source, generated, export, router, release,
advisory, live, and slow checks.

Use pytest as the default test lane in `config/validation_lanes.json` and keep
`tests/AGENTS.md` aligned with that lane authority.

Split oversized tests by owner surface and put shared temp-repo, fixture,
generated-copy, catalog-count, and subprocess helpers in `tests/support/`.

Keep deterministic agentic-OS contracts in this repository:

- positive and negative source-snapshot coverage per skill;
- compact golden route cases for approval, dry-run, safe infrastructure,
  sanitized sharing, summon handoff, session repair, and explicit mutation;
- fault-boundary tests for malformed JSON, missing generated files, stale
  manifests, unavailable external executables, and refusal/permission seams;
- lane-composition checks that prove release/export validators are wired without
  replaying the whole batch inside ordinary unit tests.

## Rationale

The source of truth for a skill organ is not a giant test file or a frozen skill
count. It is the route from authored source, through generated companions and
runtime/export surfaces, into the lane that knows how to fail and where to send
the next edit.

Keeping broad semantic/model evaluation out of the default test tree preserves
the local purpose of `aoa-skills`: deterministic skill topology, route law,
export/runtime readiness, and compact risk contracts.

## Consequences

- Positive: large test files can be scanned and changed by owner surface.
- Positive: source counts derive from generated catalog truth instead of exact
  literals in unrelated tests.
- Positive: release and export validation remain wired, but ordinary tests no
  longer duplicate broad validator execution.
- Tradeoff: the test inventory must be regenerated when test files are added,
  renamed, or moved.
- Follow-up: any future live or model-backed checks must declare an advisory or
  external lane before joining CI.

## Current Applicability

As of 2026-05-31:

- Still valid: deterministic local tests protect source, generated, export,
  router, route-law, release-lane, and compact agentic fault surfaces.
- Changed: the default test lane is pytest rather than unittest discovery.
- Superseded by: none.

## Review Log

### 2026-05-31 - Initial test topology split

- Previous assumption: the test suite could keep expanding through large
  historical files and direct validator replay.
- New reality: test shape now affected agent context cost and obscured owner
  routes.
- Reason: `aoa-skills` needs tests that are smaller, deterministic, routed, and
  explicit about what they prove.
- Source surfaces updated: `docs/testing/`, `tests/AGENTS.md`, `pytest.ini`,
  `config/validation_lanes.json`, split `tests/test_validate_skills_*.py`,
  split `tests/test_build_catalog_*.py`, route/fault tests, renamed active
  owner-surface tests, and `tests/support/`.
- Validation: focused tests for topology, release lane, route/fault contracts,
  split validation/catalog suites, full default pytest lane, mechanics Agon
  pytest lane, Spark unittest lane, source-fast CI gate, and release gate.

## Boundaries

This decision does not delete release validation, export validation, generated
drift checks, or route-law tests.

It does not make exact source-skill totals durable test truth.

It does not move broad semantic scoring, model benchmarking, or open-ended eval
authority into `aoa-skills`.

## Validation

- `docs/testing/TEST_TOPOLOGY.md` is the human test route map.
- `docs/testing/test_inventory.json` records the discovered test inventory.
- `tests/test_test_topology.py` guards map shape, inventory coverage, marker
  declarations, release-lane pytest wiring, and absence of hidden broad
  validator replay in ordinary tests.
- `tests/test_agentic_trace_contract.py` guards compact positive/negative and
  high-risk route traces.
- `tests/test_agentic_fault_boundaries.py` guards fault and tool-boundary
  behavior.
