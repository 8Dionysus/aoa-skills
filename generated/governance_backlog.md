# Governance backlog

This derived file reconciles repo-local governance readiness and evaluation readiness without changing status.
It is a backlog/maintenance view, not a promotion decision surface.

## Summary

- total skills: 16
- candidate ready without review: 0
- blocked by pending lineage: 0
- canonical maintenance cohort: 7
- comparative pending cohort: 7
- docs truth-sync issues: 0

| name | status | lineage | governance ready | eval ready | governance decision | lanes | reconciliation | candidate review | promotion review |
|---|---|---|---|---|---|---|---|---|---|
| aoa-adr-write | evaluated | published | true | true | stay_evaluated | decision_docs_authority | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-adr-write.md | docs/reviews/status-promotions/aoa-adr-write.md |
| aoa-approval-gate-check | canonical | published | true | true | default_reference | risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-approval-gate-check.md | docs/reviews/status-promotions/aoa-approval-gate-check.md |
| aoa-bounded-context-map | canonical | published | true | true | default_reference | context_vs_contract, core_boundary_refactor | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-bounded-context-map.md | docs/reviews/status-promotions/aoa-bounded-context-map.md |
| aoa-change-protocol | canonical | published | true | true | default_reference | change_workflows | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-change-protocol.md | - |
| aoa-contract-test | canonical | published | true | true | default_reference | context_vs_contract | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-contract-test.md | docs/reviews/status-promotions/aoa-contract-test.md |
| aoa-core-logic-boundary | evaluated | published | true | true | stay_evaluated | core_boundary_refactor | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-core-logic-boundary.md | docs/reviews/status-promotions/aoa-core-logic-boundary.md |
| aoa-dry-run-first | evaluated | published | true | true | stay_evaluated | risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-dry-run-first.md | docs/reviews/status-promotions/aoa-dry-run-first.md |
| aoa-invariant-coverage-audit | canonical | published | true | true | default_reference | invariant_authoring_vs_audit | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-invariant-coverage-audit.md | docs/reviews/status-promotions/aoa-invariant-coverage-audit.md |
| aoa-port-adapter-refactor | evaluated | published | true | true | stay_evaluated | core_boundary_refactor | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-port-adapter-refactor.md | docs/reviews/status-promotions/aoa-port-adapter-refactor.md |
| aoa-property-invariants | canonical | published | true | true | default_reference | invariant_authoring_vs_audit | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-property-invariants.md | docs/reviews/status-promotions/aoa-property-invariants.md |
| aoa-safe-infra-change | evaluated | published | true | true | stay_evaluated | risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-safe-infra-change.md | docs/reviews/status-promotions/aoa-safe-infra-change.md |
| aoa-sanitized-share | evaluated | published | true | true | stay_evaluated | risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-sanitized-share.md | docs/reviews/status-promotions/aoa-sanitized-share.md |
| aoa-source-of-truth-check | evaluated | published | true | true | stay_evaluated | decision_docs_authority | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-source-of-truth-check.md | docs/reviews/status-promotions/aoa-source-of-truth-check.md |
| aoa-tdd-slice | canonical | published | true | true | default_reference | change_workflows | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-tdd-slice.md | - |
| atm10-change-protocol | scaffold | published | false | true | - | - | eval_ready_but_governance_blocked | - | - |
| atm10-source-of-truth-check | scaffold | published | false | true | - | - | eval_ready_but_governance_blocked | - | - |

## Cohorts

- `candidate_ready_without_review`: -
- `blocked_by_pending_lineage`: -
- `canonical_maintenance`: aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-invariant-coverage-audit, aoa-property-invariants, aoa-tdd-slice
- `comparative_pending`: aoa-adr-write, aoa-core-logic-boundary, aoa-dry-run-first, aoa-port-adapter-refactor, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check
- `docs_truth_sync`: -

