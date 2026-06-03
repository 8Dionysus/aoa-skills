# Script Source Home Topology

- Decision ID: AOA-SK-D-0031
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `docs/validation/SCRIPT_TOPOLOGY.md`,
  `docs/validation/script_inventory.json`, `scripts/`, `tests/test_script_topology.py`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, source topology, export/runtime, generated/readout
- Skill lanes: none
- Mechanic parents: release-support, audit, boundary-bridge
- Guard families: script topology, validation command authority, generated/read-model, export/runtime, AGENTS/mesh
- Posture: accepted script source-home topology

## Context

The validator and test topology splits made validation ownership visible, but
root `scripts/` still carried implementation as a flat pile of builders,
validators, runtime helpers, bundle tools, audits, reports, refresh flows, and
source-model contracts.

That flatness violated the repository design rule that topology beats flat
accumulation. It also made future script movement ambiguous: a new helper could
land in root because historical files were already there, even when the helper
belonged to export, runtime, bundles, validation, or skill model ownership.

## Decision

Refactor root `scripts/` into a script source-home tree.

Implementation lives under named organ directories:

- `activation/`
- `adapters/`
- `audit/`
- `bridges/`
- `builders/`
- `bundles/`
- `decisions/`
- `export/`
- `lanes/`
- `receipts/`
- `refresh/`
- `reports/`
- `runtime/`
- `skill_model/`
- `validation/`

Root `scripts/*.py` files remain as thin command/front-door compatibility
ingress wrappers through `scripts/_ingress.py`. They keep historical command
paths working while the real implementation moves to organ directories.
Library, contract, source-model, bridge, surface, and helper modules do not get
root wrappers.

Move validator owner modules and manifest-backed contracts under
`scripts/validation/validators/`. Keep `scripts/validators/__init__.py` only as
a compatibility alias package for older `validators.*` imports.

Record the human route in `docs/validation/SCRIPT_TOPOLOGY.md`, the machine
organ map in `docs/validation/script_inventory.json`, and enforce the shape
with `tests/test_script_topology.py`.

## Rationale

The script plane is not one organ. It moves generated projections, release
lanes, portable exports, runtime payloads, bundle handoffs, audits, reports,
refreshes, and skill source contracts. A flat root makes those owner boundaries
invisible.

Keeping root command ingress wrappers is intentional. Current CI, generated
payloads, docs, and downstream invocations still know paths such as
`python scripts/build_catalog.py` and `python scripts/release_check.py`.
Breaking those paths would be churn, not maturity. The durable change is that
new implementation and helper libraries can no longer hide in root.

## Consequences

- Positive: future agents can route scripts by organ before changing code.
- Positive: root command compatibility survives while implementation becomes
  tree-shaped.
- Positive: validator owner modules now sit under the validation organ instead
  of a root-adjacent pseudo-organ.
- Tradeoff: legacy command wrappers remain visible in root until downstream
  command paths can be safely retired or re-pointed.
- Follow-up: new script families should update `SCRIPT_TOPOLOGY.md`,
  `script_inventory.json`, and `tests/test_script_topology.py` before adding
  implementation.

## Current Applicability

As of 2026-06-03, root `scripts/*.py` files except `_ingress.py` are command
ingress wrappers. Implementation modules live under organ directories, helper
imports use organ packages, and `scripts/validators/__init__.py` is alias-only.
