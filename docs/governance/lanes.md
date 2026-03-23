# Governance lanes

This document is the human companion to `docs/governance/lanes.yaml`.
The YAML manifest is the machine-readable source of truth for lane membership,
governance decision, and adjacency-evidence mapping.
This document explains the same lane decisions in prose without changing status by itself.

## Reading posture

- `candidate_ready` remains a machine gate-pass signal, not a promotion decision
- `default_reference` means the current lane decision is to keep the skill as a default public reference
- `stay_evaluated` means the current lane decision is to keep the skill evaluated and explicitly not promote it in this wave
- lane decisions are status-neutral in `v0.5`

## change_workflows

- state: `stable_defaults`
- default references: `aoa-change-protocol`, `aoa-tdd-slice`
- rationale: both are already stable default references for adjacent but distinct change-execution workflows
- review sources: `docs/reviews/canonical-candidates/aoa-change-protocol.md`, `docs/reviews/canonical-candidates/aoa-tdd-slice.md`

## context_vs_contract

- state: `stable_defaults`
- default references: `aoa-bounded-context-map`, `aoa-contract-test`
- rationale: both are already stable defaults for adjacent but distinct context-carving and contract-validation work
- review sources: `docs/reviews/canonical-candidates/aoa-bounded-context-map.md`, `docs/reviews/canonical-candidates/aoa-contract-test.md`

## core_boundary_refactor

- state: `comparative_pending`
- default reference anchor: `aoa-bounded-context-map`
- stay-evaluated decisions: `aoa-core-logic-boundary`, `aoa-port-adapter-refactor`
- rationale: current reviews keep the refactor-oriented pair at `evaluated` until a stronger comparative default-reference case is recorded
- review sources: `docs/reviews/canonical-candidates/aoa-bounded-context-map.md`, `docs/reviews/canonical-candidates/aoa-core-logic-boundary.md`, `docs/reviews/canonical-candidates/aoa-port-adapter-refactor.md`

## decision_docs_authority

- state: `comparative_pending`
- stay-evaluated decisions: `aoa-adr-write`, `aoa-source-of-truth-check`
- rationale: both are gate-clean, but neither is promoted to default-reference status in this wave
- review sources: `docs/reviews/canonical-candidates/aoa-adr-write.md`, `docs/reviews/canonical-candidates/aoa-source-of-truth-check.md`

## risk_authority_preview_execution

- state: `comparative_pending`
- default reference anchor: `aoa-approval-gate-check`
- stay-evaluated decisions: `aoa-dry-run-first`, `aoa-safe-infra-change`, `aoa-sanitized-share`
- rationale: authority classification stays the default reference in this lane while the adjacent preview/execution/share workflows remain explicitly evaluated
- review sources: `docs/reviews/canonical-candidates/aoa-approval-gate-check.md`, `docs/reviews/canonical-candidates/aoa-dry-run-first.md`, `docs/reviews/canonical-candidates/aoa-safe-infra-change.md`, `docs/reviews/canonical-candidates/aoa-sanitized-share.md`

## invariant_authoring_vs_audit

- state: `stable_defaults`
- default references: `aoa-invariant-coverage-audit`, `aoa-property-invariants`
- rationale: both are already stable defaults for adjacent but distinct invariant-authoring and invariant-audit workflows
- review sources: `docs/reviews/canonical-candidates/aoa-invariant-coverage-audit.md`, `docs/reviews/canonical-candidates/aoa-property-invariants.md`
