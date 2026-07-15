# Committed Evidence Readout Completeness Gate

- Decision ID: AOA-SK-D-0038
- Status: Superseded by AOA-SK-D-0039
- Date: 2026-07-13
- Owner surface: `config/validation_lanes.json`,
  `scripts/validation/validators/skill_evidence_readout_surface.py`, and the
  committed skill quality and promotion readouts under `generated/`

## Index Metadata

- Original date: 2026-07-13
- Surface classes: validation guard, generated/readout, review/governance
- Skill lanes: none
- Mechanic parents: audit, method-growth, release-support
- Guard families: generated/read-model, validator topology, promotion evidence, release/CI
- Posture: superseded evidence-readout gate; see AOA-SK-D-0039

## Context

The generated skill evaluation matrix described all 57 current skills, while
the committed quality-audit and promotion-pressure readouts still described
only 45. The ordinary source, generated, export, and release routes could stay
green because they validated the evaluation matrix and export families but did
not constrain completeness of these two review-facing reports.

The reports mix two different evidence classes. Current skill membership,
`status`, and `scope` are deterministic repo-derived fields. Session mentions,
hook observations, dispatch events, reality trials, and sibling technique drift
are advisory observations whose freshness depends on live or external owner
surfaces. Treating the whole report as deterministic would pull private or
moving workspace evidence into required CI. Treating the whole report as
unconstrained advisory output lets newly added skills disappear from the
quality and promotion queues without a failing gate.

## Options Considered

- Keep both reports entirely advisory and rely on manual regeneration before a
  family-wide review.
- Rebuild and compare complete reports in ordinary CI, including live session,
  hook, dispatch, reality-trial, and technique-drift inputs.
- Block only on the deterministic projection that a committed report must
  preserve, while keeping live evidence freshness explicitly advisory.

## Decision

Choose the third option.

Use `generated/skill_evaluation_matrix.json` as the generated reference for the
current skill set and its `status`/`scope` classification. Require both
committed JSON reports to have:

- `skill_count` equal to the current evaluation-matrix count;
- unique skill names with no missing or unexpected entries;
- exact `status` and `scope` parity for every current skill.

Require each committed Markdown companion to have the same skill count and the
same skill/status matrix as its JSON report. Route this deterministic validator
through generated-export check, full export, and release command sequences.

The quality-audit and promotion-pressure scripts remain the builders and
semantic owners of their reports. A completeness failure routes to those owner
commands for regeneration; the validator does not rewrite reports and does not
interpret promotion pressure.

## Rationale

This is the smallest stable invariant that prevents silent family omission.
It constrains fields already owned by current repository source and a generated
matrix without pretending that local usage observations or sibling-repository
state are reproducible in ordinary CI.

Keeping the validator as a thin CLI over a bounded owner module follows the
existing validator topology. Wiring the command through the lane manifest
keeps command authority in one source. Checking the Markdown projection closes
the human-reader path as well as the machine-reader path.

## Consequences

- Positive: adding, removing, or reclassifying a skill cannot leave committed
  quality and promotion readouts silently incomplete.
- Positive: machine and human readouts fail together when their deterministic
  skill projection diverges.
- Positive: review queues see every current skill before promotion, retention,
  split, merge, or retirement decisions are made.
- Tradeoff: source changes that alter the skill set or status/scope now require
  both owner reports to be regenerated before export or release lanes pass.
- Tradeoff: a green completeness gate does not prove that live counts or
  technique-drift observations were refreshed recently.
- Follow-up: route live evidence freshness through explicit owner campaigns and
  keep newly exposed maintenance findings visible instead of weakening this
  deterministic gate.

## Current Applicability

As of 2026-07-13:

- Still valid: the evaluation matrix is generated evidence, not authored skill
  meaning; source skill bundles and review records remain stronger.
- Current family count: 57 skills.
- Current readout posture: both JSON and Markdown report families have been
  regenerated and satisfy the deterministic completeness contract.
- Remaining advisory findings: technique drift and autonomy coverage remain
  separate maintenance inputs and are not converted into gate success or
  automatic promotion.
- Superseded by: none.

## Review Log

### 2026-07-13 - Initial completeness boundary

- Previous assumption: because quality and promotion reports are advisory,
  ordinary blocking lanes did not need to constrain their committed shape.
- New reality: a 45-of-57 report stayed green and hid 12 current skills from
  both family-wide reader surfaces.
- Reason: advisory interpretation does not justify deterministic membership
  drift in a committed artifact.
- Source surfaces updated: lane command authority, validator topology and
  inventory, focused tests, and the two owner-generated report families.
- Validation: focused validator and topology tests, direct 57-skill
  completeness validation, decision-index generation/check, and affected
  generated/export/release lanes.

## Boundaries

This decision does not make session memory, hook logs, dispatch receipts,
reality trials, or sibling technique state proof authority. It does not require
raw or private evidence in CI. It does not auto-promote a skill, accept a
quality verdict, or claim that an advisory count is current merely because the
skill row exists.

The evaluation matrix remains a generated reference for this parity check; it
does not override `skills/**/SKILL.md`, review records, governance decisions, or
the owner builders that produce the reports.

## Source Surfaces

- `config/validation_lanes.json`
- `scripts/validation/validate_skill_evidence_readouts.py`
- `scripts/validation/validators/skill_evidence_readout_surface.py`
- `docs/validation/VALIDATOR_TOPOLOGY.md`
- `docs/validation/validator_inventory.json`
- `generated/skill_evaluation_matrix.json`
- `generated/skill_quality_audit.json`
- `generated/skill_quality_audit.md`
- `generated/skill_promotion_pressure.json`
- `generated/skill_promotion_pressure.md`

## Validation

- `tests/test_skill_evidence_readout_freshness.py` exercises missing, extra,
  duplicate, status/scope drift, Markdown projection drift, and the bounded
  claim surface.
- `tests/test_validator_topology.py` keeps the new CLI inventoried, thin, and
  wired through command authority.
- The direct validator must report all 57 current skills with zero issues.
- Decision indexes and the generated/export/release lanes must remain fresh.
