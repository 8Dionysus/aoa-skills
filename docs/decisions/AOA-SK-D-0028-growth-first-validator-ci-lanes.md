# Growth-First Validator CI Lanes

- Decision ID: AOA-SK-D-0028
- Status: Accepted
- Date: 2026-05-31
- Owner surface: `scripts/validation_lanes.py`, `scripts/ci_gate.py`,
  `.github/workflows/`

## Index Metadata

- Original date: 2026-05-31
- Surface classes: validation guard, export/runtime, generated/readout, agent route
- Skill lanes: none
- Mechanic parents: release-support, audit
- Guard families: CI lane, release/tooling, generated/read-model, export/runtime
- Posture: accepted growth-first split

## Context

`aoa-skills` releases a bounded skill-canon baseline and then keeps growing
`main` immediately. That means `main` is a moving growth surface, not a frozen
release branch.

The prior CI shape treated ordinary growth, generated read-model freshness,
portable export, sibling technique drift, and release packaging smoke as one
large landing posture. That made local skill edits expensive and made scheduled
or post-release checks vulnerable to a false assumption: `main` should still
look like the latest release after the tag is cut.

The repository's own design already separates authored skill meaning from
generated and exported companions. CI should preserve that separation instead of
making every growth edit pass through release-freeze machinery.

## Options Considered

- Keep `release_check.py` as the required PR and `main` gate.
- Keep export checks on every PR but tolerate failures after release.
- Split CI into explicit growth, generated, export, release, and nightly lanes
  with a repo-local entrypoint that owns lane meaning.

## Decision

Use `scripts/ci_gate.py` as the repo-local entrypoint for CI lane semantics:

- `source-fast`: validates source-facing route, AGENTS mesh, and skill contracts
  without generated/export freshness checks.
- `generated`: validates grouped generated/readout companions: `reader`,
  `public`, `evaluation`, `governance`, `export`, `runtime`, or `all`.
- `export`: validates portable export, runtime, support, and tiny-router
  surfaces when that lane is explicitly relevant.
- `release`: runs the full release-prep gate with packaging smoke.
- `nightly`: checks moving `main` as a growth surface and reports release
  identity without treating `has_unreleased_changes: true` as failure.

`Repo Validation` remains the required growth gate for PRs and `main`. The
existing `build-validate` required check remains present, but becomes a
growth-safe export sentinel that skips heavy export work when the diff does not
touch export/runtime generated inputs. A separate `Release Audit` workflow runs
on `v*` tags and manual dispatch. `Nightly Sentinel` checks the latest release
tag separately from moving `main`.

## Rationale

This preserves the repository's owner boundaries:

- authored skill bundles stay the source of workflow meaning;
- generated readers and portable exports stay companions;
- release checks stay available for frozen release surfaces;
- nightly checks observe growth rather than enforcing release stasis.

Keeping lane definitions in `scripts/validation_lanes.py` and execution routing
in `scripts/ci_gate.py` also prevents GitHub YAML and release helper scripts
from becoming hidden sources of validation authority.

## Consequences

- Positive: ordinary PRs can validate source contracts without paying the full
  release/export cost.
- Positive: scheduled checks no longer fail merely because `main` has unreleased
  growth after a release.
- Positive: release tags still get the full release gate and packaging smoke.
- Tradeoff: export drift can be intentionally deferred during growth and must
  be closed before release.
- Follow-up: future branch-protection changes should keep required checks
  aligned with `Repo Validation` and `build-validate` meanings.

## Current Applicability

As of 2026-05-31:

- Still valid: `release_check.py` remains the full release-prep gate.
- Changed: PR and moving-main CI route through growth-first lanes instead of
  release-freeze posture.
- Superseded by: none.

## Review Log

### 2026-05-31 - Initial growth-first CI split

- Previous assumption: broad release validation was a reasonable default for
  PRs, `main`, and scheduled checks.
- New reality: `main` moves immediately after releases, and validator/export
  aggregation was becoming heavier than the skill-canon organ it protects.
- Reason: `aoa-skills` needs fast source checks during growth and full release
  checks only when freezing a release artifact.
- Source surfaces updated: `scripts/validation_lanes.py`, `scripts/ci_gate.py`,
  `scripts/validate_skills.py`, `scripts/build_catalog.py`,
  `.github/workflows/`, root and release-support route docs. The generated lane
  now includes explicit export and runtime groups instead of hiding those checks
  behind release-only posture.
- Follow-up hardening: nested AGENTS route-law snippets moved from Python into
  `scripts/validators/nested_agents_contract.json`, and
  `scripts/validate_agent_skills.py` now delegates to
  `scripts/validators/agent_skills_export_surface.py` as a thin CLI adapter.
- Follow-up hardening: Agent Skills export contract data moved to
  `scripts/validators/agent_skills_export_contract.json`, and questbook surface
  contract data moved to `scripts/validators/questbook_contract.json`.
- Follow-up hardening: generated/read-model validation execution moved to
  `scripts/validators/generated_surface.py`, and questbook surface validation
  execution moved to `scripts/validators/questbook_surface.py`; `validate_skills.py`
  remains the CLI/orchestration shell. Questbook validation is phase-split into
  schema, quest YAML, generated catalog, and dispatch checks.
- Follow-up hardening: Agent Skills export/runtime validation is phase-split
  into document loading, index building, skill-set parity, per-skill
  resource/runtime/router checks, project ring checks, release relationship
  checks, and runtime guardrail checks. Tests now guard the thin CLI adapter and
  the phase-split validator shape.
- Follow-up hardening: the Spark lane validator now reads the shared release
  command sequence from `scripts/validation_lanes.py` instead of scanning
  `scripts/release_check.py` text.
- Follow-up hardening: full export validation now includes trigger-eval seed
  rebuilds and drift paths because description-trigger, runtime seam, and
  tiny-router surfaces consume those seed cases.
- Validation: source-fast, generated, workflow syntax parsing, focused unit
  tests, and release gate checks.

## Boundaries

This decision does not weaken skill source contracts.

It does not delete or demote `release_check.py`.

It does not make generated or exported surfaces source authority.

It does not move technique, proof, routing, memory, runtime, or downstream
truth into `aoa-skills`.

It does not require `main` to match the latest release tag.

## Validation

- `scripts/validation_lanes.py` owns shared command sequences and drift paths.
- `scripts/ci_gate.py` executes active CI lanes.
- `.github/workflows/repo-validation.yml` keeps the required growth check.
- `.github/workflows/codex-portable-export.yml` keeps required `build-validate`
  reporting without path-filter pending risk.
- `.github/workflows/release-audit.yml` owns tag/manual release auditing.
- `.github/workflows/nightly-sentinel.yml` separates moving `main` from latest
  release reproduction.
