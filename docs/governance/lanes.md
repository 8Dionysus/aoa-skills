# Governance lanes

This document is the human companion to `docs/governance/lanes.yaml`.
The YAML manifest is the machine-readable source of truth for lane membership,
governance decision, and adjacency-evidence mapping.
This document explains the same lane decisions in prose without changing status by itself.

## Reading posture

- `candidate_ready` remains a machine gate-pass signal, not a promotion decision
- `default_reference` means the lane now records a default public reference and should align with `canonical` status for that skill
- `stay_evaluated` means the lane records an intentional decision to keep a well-evidenced skill at `evaluated`
- `stable_defaults` lanes may carry more than one default reference when adjacent workflow classes are both part of the public default surface

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
- rationale: `aoa-bounded-context-map` remains the default entry anchor for first-pass context and boundary clarification, while the refactor-oriented pair stays intentionally specialized follow-on work once the main problem is either core-versus-glue separation or a concrete dependency seam
- review sources: `docs/reviews/canonical-candidates/aoa-bounded-context-map.md`, `docs/reviews/canonical-candidates/aoa-core-logic-boundary.md`, `docs/reviews/canonical-candidates/aoa-port-adapter-refactor.md`

## decision_docs_authority

- state: `stable_defaults`
- default references: `aoa-adr-write`, `aoa-source-of-truth-check`
- rationale: both are now stable defaults for adjacent but distinct decision-rationale recording and document-authority clarification work across varied repo conventions
- review sources: `docs/reviews/canonical-candidates/aoa-adr-write.md`, `docs/reviews/canonical-candidates/aoa-source-of-truth-check.md`

## risk_authority_preview_execution

- state: `stable_defaults`
- default references: `aoa-approval-gate-check`, `aoa-dry-run-first`, `aoa-safe-infra-change`, `aoa-sanitized-share`
- rationale: the lane now has stable defaults for four distinct workflow classes: authority classification, preview-first planning, bounded infra/config execution, and sanitized sharing
- review sources: `docs/reviews/canonical-candidates/aoa-approval-gate-check.md`, `docs/reviews/canonical-candidates/aoa-dry-run-first.md`, `docs/reviews/canonical-candidates/aoa-safe-infra-change.md`, `docs/reviews/canonical-candidates/aoa-sanitized-share.md`

## local_runtime_bringup

- state: `comparative_pending`
- default reference anchors: `aoa-approval-gate-check`, `aoa-safe-infra-change`
- stay-evaluated decisions: `aoa-local-stack-bringup`
- rationale: local multi-service bring-up now clears the evaluated floor, but it remains intentionally non-canonical while the repo records its boundary against authority classification and bounded infra-change work
- review sources: `docs/reviews/status-promotions/aoa-local-stack-bringup.md`, `docs/reviews/canonical-candidates/aoa-local-stack-bringup.md`, `docs/reviews/canonical-candidates/aoa-approval-gate-check.md`, `docs/reviews/canonical-candidates/aoa-safe-infra-change.md`

## invariant_authoring_vs_audit

- state: `stable_defaults`
- default references: `aoa-invariant-coverage-audit`, `aoa-property-invariants`
- rationale: both are already stable defaults for adjacent but distinct invariant-authoring and invariant-audit workflows
- review sources: `docs/reviews/canonical-candidates/aoa-invariant-coverage-audit.md`, `docs/reviews/canonical-candidates/aoa-property-invariants.md`
