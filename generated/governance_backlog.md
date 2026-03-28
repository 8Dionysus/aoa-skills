# Governance backlog

This derived file reconciles repo-local governance readiness and evaluation readiness without changing status.
It is a backlog/maintenance view, not a promotion decision surface.

## Summary

- total skills: 17
- candidate ready without review: 0
- blocked by pending lineage: 0
- canonical maintenance cohort: 12
- comparative pending cohort: 3
- review truth-sync gaps: 0
- docs truth-sync issues: 0

| name | status | lineage | governance ready | eval ready | governance decision | lanes | reconciliation | candidate review | promotion review |
|---|---|---|---|---|---|---|---|---|---|
| aoa-adr-write | canonical | published | true | true | default_reference | decision_docs_authority | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-adr-write.md | docs/reviews/status-promotions/aoa-adr-write.md |
| aoa-approval-gate-check | canonical | published | true | true | default_reference | local_runtime_bringup, risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-approval-gate-check.md | docs/reviews/status-promotions/aoa-approval-gate-check.md |
| aoa-bounded-context-map | canonical | published | true | true | default_reference | context_vs_contract, core_boundary_refactor | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-bounded-context-map.md | docs/reviews/status-promotions/aoa-bounded-context-map.md |
| aoa-change-protocol | canonical | published | true | true | default_reference | change_workflows | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-change-protocol.md | - |
| aoa-contract-test | canonical | published | true | true | default_reference | context_vs_contract | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-contract-test.md | docs/reviews/status-promotions/aoa-contract-test.md |
| aoa-core-logic-boundary | evaluated | published | true | true | stay_evaluated | core_boundary_refactor | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-core-logic-boundary.md | docs/reviews/status-promotions/aoa-core-logic-boundary.md |
| aoa-dry-run-first | canonical | published | true | true | default_reference | risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-dry-run-first.md | docs/reviews/status-promotions/aoa-dry-run-first.md |
| aoa-invariant-coverage-audit | canonical | published | true | true | default_reference | invariant_authoring_vs_audit | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-invariant-coverage-audit.md | docs/reviews/status-promotions/aoa-invariant-coverage-audit.md |
| aoa-local-stack-bringup | evaluated | published | true | true | stay_evaluated | local_runtime_bringup | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-local-stack-bringup.md | docs/reviews/status-promotions/aoa-local-stack-bringup.md |
| aoa-port-adapter-refactor | evaluated | published | true | true | stay_evaluated | core_boundary_refactor | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-port-adapter-refactor.md | docs/reviews/status-promotions/aoa-port-adapter-refactor.md |
| aoa-property-invariants | canonical | published | true | true | default_reference | invariant_authoring_vs_audit | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-property-invariants.md | docs/reviews/status-promotions/aoa-property-invariants.md |
| aoa-safe-infra-change | canonical | published | true | true | default_reference | local_runtime_bringup, risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-safe-infra-change.md | docs/reviews/status-promotions/aoa-safe-infra-change.md |
| aoa-sanitized-share | canonical | published | true | true | default_reference | risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-sanitized-share.md | docs/reviews/status-promotions/aoa-sanitized-share.md |
| aoa-source-of-truth-check | canonical | published | true | true | default_reference | decision_docs_authority | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-source-of-truth-check.md | docs/reviews/status-promotions/aoa-source-of-truth-check.md |
| aoa-tdd-slice | canonical | published | true | true | default_reference | change_workflows | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-tdd-slice.md | - |
| atm10-change-protocol | evaluated | published | false | true | - | - | eval_ready_but_governance_blocked | - | docs/reviews/status-promotions/atm10-change-protocol.md |
| atm10-source-of-truth-check | evaluated | published | false | true | - | - | eval_ready_but_governance_blocked | - | docs/reviews/status-promotions/atm10-source-of-truth-check.md |

## Review truth sync

| name | status | lineage | governance decision | review path | reviewed revision | current revision | meaning changed | issues | synced |
|---|---|---|---|---|---|---|---|---|---|
| aoa-adr-write | canonical | published | default_reference | docs/reviews/status-promotions/aoa-adr-write.md | efea66558a8f | efea66558a8f | True | - | true |
| aoa-approval-gate-check | canonical | published | default_reference | docs/reviews/status-promotions/aoa-approval-gate-check.md | c40906ab85f7 | c40906ab85f7 | True | - | true |
| aoa-bounded-context-map | canonical | published | default_reference | docs/reviews/status-promotions/aoa-bounded-context-map.md | 54dac4ff2176 | 54dac4ff2176 | False | - | true |
| aoa-contract-test | canonical | published | default_reference | docs/reviews/status-promotions/aoa-contract-test.md | afa2aca6eaed | afa2aca6eaed | False | - | true |
| aoa-core-logic-boundary | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-core-logic-boundary.md | ee2eb1cc6aa9 | ee2eb1cc6aa9 | False | - | true |
| aoa-dry-run-first | canonical | published | default_reference | docs/reviews/status-promotions/aoa-dry-run-first.md | 34ca9cb7c545 | 34ca9cb7c545 | True | - | true |
| aoa-invariant-coverage-audit | canonical | published | default_reference | docs/reviews/status-promotions/aoa-invariant-coverage-audit.md | 97ce3d068b91 | 97ce3d068b91 | True | - | true |
| aoa-local-stack-bringup | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-local-stack-bringup.md | 4dc638ecae8b | 4dc638ecae8b | False | - | true |
| aoa-port-adapter-refactor | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-port-adapter-refactor.md | 9f787dcdf31a | 9f787dcdf31a | False | - | true |
| aoa-property-invariants | canonical | published | default_reference | docs/reviews/status-promotions/aoa-property-invariants.md | 3f8c54b28ddd | 3f8c54b28ddd | True | - | true |
| aoa-safe-infra-change | canonical | published | default_reference | docs/reviews/status-promotions/aoa-safe-infra-change.md | 595c4e599075 | 595c4e599075 | False | - | true |
| aoa-sanitized-share | canonical | published | default_reference | docs/reviews/status-promotions/aoa-sanitized-share.md | 5db83815e920 | 5db83815e920 | True | - | true |
| aoa-source-of-truth-check | canonical | published | default_reference | docs/reviews/status-promotions/aoa-source-of-truth-check.md | f4bdf444bbe4 | f4bdf444bbe4 | True | - | true |
| atm10-change-protocol | evaluated | published | - | docs/reviews/status-promotions/atm10-change-protocol.md | bf3b1081c216 | bf3b1081c216 | False | - | true |
| atm10-source-of-truth-check | evaluated | published | - | docs/reviews/status-promotions/atm10-source-of-truth-check.md | ce4b813299a4 | ce4b813299a4 | False | - | true |

## Cohorts

- `candidate_ready_without_review`: -
- `blocked_by_pending_lineage`: -
- `canonical_maintenance`: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice
- `comparative_pending`: aoa-core-logic-boundary, aoa-local-stack-bringup, aoa-port-adapter-refactor
- `review_truth_sync`: -
- `docs_truth_sync`: -

