# Governance backlog

This derived file reconciles repo-local governance readiness and evaluation readiness without changing status.
It is a backlog/maintenance view, not a promotion decision surface.

## Summary

- total skills: 14
- candidate ready without review: 0
- blocked by pending lineage: 8
- canonical maintenance cohort: 6
- docs truth-sync issues: 0

| name | status | lineage | governance ready | eval ready | reconciliation | candidate review | promotion review |
|---|---|---|---|---|---|---|---|
| aoa-adr-write | evaluated | pending | false | true | eval_ready_but_governance_blocked | - | docs/reviews/status-promotions/aoa-adr-write.md |
| aoa-approval-gate-check | evaluated | pending | false | true | eval_ready_but_governance_blocked | docs/reviews/canonical-candidates/aoa-approval-gate-check.md | docs/reviews/status-promotions/aoa-approval-gate-check.md |
| aoa-bounded-context-map | canonical | published | true | true | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-bounded-context-map.md | docs/reviews/status-promotions/aoa-bounded-context-map.md |
| aoa-change-protocol | canonical | published | true | true | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-change-protocol.md | - |
| aoa-contract-test | canonical | published | true | true | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-contract-test.md | docs/reviews/status-promotions/aoa-contract-test.md |
| aoa-core-logic-boundary | evaluated | pending | false | true | eval_ready_but_governance_blocked | - | docs/reviews/status-promotions/aoa-core-logic-boundary.md |
| aoa-dry-run-first | evaluated | pending | false | true | eval_ready_but_governance_blocked | - | docs/reviews/status-promotions/aoa-dry-run-first.md |
| aoa-invariant-coverage-audit | canonical | published | true | true | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-invariant-coverage-audit.md | docs/reviews/status-promotions/aoa-invariant-coverage-audit.md |
| aoa-port-adapter-refactor | evaluated | pending | false | true | eval_ready_but_governance_blocked | - | docs/reviews/status-promotions/aoa-port-adapter-refactor.md |
| aoa-property-invariants | canonical | published | true | true | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-property-invariants.md | docs/reviews/status-promotions/aoa-property-invariants.md |
| aoa-safe-infra-change | evaluated | pending | false | true | eval_ready_but_governance_blocked | - | docs/reviews/status-promotions/aoa-safe-infra-change.md |
| aoa-sanitized-share | evaluated | pending | false | true | eval_ready_but_governance_blocked | - | docs/reviews/status-promotions/aoa-sanitized-share.md |
| aoa-source-of-truth-check | evaluated | pending | false | true | eval_ready_but_governance_blocked | - | docs/reviews/status-promotions/aoa-source-of-truth-check.md |
| aoa-tdd-slice | canonical | published | true | true | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-tdd-slice.md | - |

## Cohorts

- `candidate_ready_without_review`: -
- `blocked_by_pending_lineage`: aoa-adr-write, aoa-approval-gate-check, aoa-core-logic-boundary, aoa-dry-run-first, aoa-port-adapter-refactor, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check
- `canonical_maintenance`: aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-invariant-coverage-audit, aoa-property-invariants, aoa-tdd-slice
- `docs_truth_sync`: -

