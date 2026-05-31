# Canonical Decision IDs And Indexes

- Decision ID: AOA-SK-D-0027
- Status: Accepted
- Date: 2026-05-30
- Owner surface: `docs/decisions/`

## Index Metadata

- Original date: 2026-05-30
- Surface classes: docs route, generated/readout, validation guard
- Skill lanes: none
- Mechanic parents: none
- Guard families: decision index/read-model, docs route, release/tooling
- Posture: accepted canonical cleanup

## Context

`aoa-skills` decision records still used date-prefixed filenames and had no
source-owned metadata for generated lookup indexes. That was readable for a
small lane, but it made route recovery expensive: an agent had to scan a flat
directory and infer decision order, surface class, mechanic parent, or skill
lane from titles and prose.

`aoa-memo` and `aoa-evals` already landed the stronger principle: decision
records keep stable canonical handles, source notes carry the metadata that
makes them findable, and generated indexes are lookup read models rather than
rationale authority.

For `aoa-skills`, the same principle needs a local shape. This repository owns
bounded workflow meaning, skill lanes, mechanics around skill movement, portable
exports, generated companions, and review pressure. It should not import
memory-object classes from `aoa-memo` or proof-specific fields from
`aoa-evals`.

## Options Considered

- Keep date-prefixed filenames and add only a manual README index.
- Add in-file decision IDs but leave active paths date-prefixed.
- Use full canonical decision IDs as both in-file handles and filename prefixes,
  then generate lookup indexes from local metadata.

## Decision

Use full canonical IDs for `aoa-skills` decision records:

`AOA-SK-D-####`

Each decision note must include `- Decision ID: AOA-SK-D-####`, and the
filename prefix must match the decision ID exactly:

`docs/decisions/AOA-SK-D-####-short-slug.md`

Each decision note also owns an `## Index Metadata` block with `Original date`,
surface classes, skill lanes, mechanic parents, guard families, and posture.
Generated lookup indexes derive from that metadata:

- `by-number.md`
- `by-date.md`
- `by-surface.md`
- `by-skill-lane.md`
- `by-mechanic.md`
- `by-guard.md`

Previous date-prefixed paths are retired. They remain recoverable through git
history, PRs, and release notes, not through compatibility stubs or generated
path maps.

## Rationale

Canonical IDs make decision references stable across file listings, search
results, generated read models, review notes, and cross-repo context packets.

Matching filenames make the owner and object class visible from the path itself:
`AOA-SK-D` means an `aoa-skills` decision, the number gives stable order, and
the slug keeps the record human-readable.

Generated indexes keep lookup cheap while preserving decision notes as the
rationale authority. The `Skill lanes` metadata is the local adaptation of the
shared principle: it lets future agents find decisions that affect
`core/session-growth`, `risk`, `project`, or portable export routes without
pretending this repository owns memory or proof object classes.

Avoiding compatibility maps keeps the active lane small. Old date paths were
local addresses, not durable external contracts.

## Consequences

- Positive: decision records are now self-identifying outside local directory
  context.
- Positive: agents can search `AOA-SK-D-####` as a stable decision handle.
- Positive: date, surface, skill-lane, mechanic, and guard lookup are generated
  from source metadata.
- Tradeoff: existing date-path references outside git history must be updated to
  canonical paths.
- Follow-up: future decision notes must use the canonical ID template before
  generated index parity can pass.

## Current Applicability

As of 2026-05-30:

- Still valid: decision notes explain why; source surfaces keep current skill,
  mechanic, generated, export, and agent-route authority.
- Changed: active decision source paths use full canonical ID filename prefixes.
- Superseded by: none.

## Review Log

### 2026-05-30 - Initial canonical-address landing

- Previous assumption: date-prefixed filenames were sufficient because the lane
  was small.
- New reality: sibling decision lanes now use canonical IDs and generated lookup
  indexes, and `aoa-skills` has enough mechanics, lanes, exports, and review
  surfaces to need the same operability.
- Reason: this makes decision refs easier to route from search, generated
  indexes, reviews, memory packets, and cross-repo notes.
- Source surfaces updated: `docs/decisions/`, generated decision indexes,
  `docs/decisions/indexes/index_contract.yaml`, and
  `scripts/decision_indexes.py`.
- Validation: `python scripts/generate_decision_indexes.py --check`, focused
  decision-index tests, `python scripts/validate_agents_design.py`, and
  `git diff --check`.

## Boundaries

This decision does not make generated indexes decision authority.

It does not import memory-object metadata from `aoa-memo` or proof-object fields
from `aoa-evals`.

It does not preserve old date-prefixed paths as active compatibility routes.

It does not change the bounded workflow meaning of any skill bundle, technique
bridge, mechanic package, generated companion, portable export, or Spark lane
surface.

## Validation

- `scripts/decision_indexes.py` enforces canonical ID filename prefixes,
  in-file decision IDs, original dates, metadata fields, and generated index
  parity.
- `docs/decisions/indexes/index_contract.yaml` names the active path policy.
- Generated decision indexes route back to `AOA-SK-D-####-*.md` source notes.
