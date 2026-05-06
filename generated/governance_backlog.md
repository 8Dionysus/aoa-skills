# Governance backlog

This derived file reconciles repo-local governance readiness and evaluation readiness without changing status.
It is a backlog/maintenance view, not a promotion decision surface.
Project-overlay rows may use overlay-specific reconciliation values when no governance lane exists.
Read those rows as per-skill maintenance signals, not as missing canonical-decision debt.

## Summary

- total skills: 45
- candidate ready without review: 0
- blocked by pending lineage: 16
- canonical maintenance cohort: 12
- comparative pending cohort: 3
- review truth-sync gaps: 0
- docs truth-sync issues: 0

| name | status | lineage | governance ready | eval ready | governance decision | lanes | reconciliation | candidate review | promotion review |
|---|---|---|---|---|---|---|---|---|---|
| abyss-safe-infra-change | evaluated | published | false | true | - | - | project_overlay_federation_ready | - | docs/reviews/status-promotions/abyss-safe-infra-change.md |
| abyss-sanitized-share | evaluated | published | false | true | - | - | project_overlay_federation_ready | - | docs/reviews/status-promotions/abyss-sanitized-share.md |
| abyss-self-diagnostic-spine | scaffold | published | false | true | - | - | project_overlay_federation_ready | - | - |
| aoa-adr-write | canonical | published | true | true | default_reference | decision_docs_authority | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-adr-write.md | docs/reviews/status-promotions/aoa-adr-write.md |
| aoa-approval-gate-check | canonical | published | true | true | default_reference | local_runtime_bringup, risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-approval-gate-check.md | docs/reviews/status-promotions/aoa-approval-gate-check.md |
| aoa-automation-opportunity-scan | scaffold | published | false | true | - | - | eval_ready_but_governance_blocked | - | - |
| aoa-bounded-context-map | canonical | published | true | true | default_reference | context_vs_contract, core_boundary_refactor | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-bounded-context-map.md | docs/reviews/status-promotions/aoa-bounded-context-map.md |
| aoa-change-protocol | canonical | published | true | true | default_reference | change_workflows | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-change-protocol.md | - |
| aoa-checkpoint-closeout-bridge | scaffold | published | false | true | - | - | eval_ready_but_governance_blocked | - | - |
| aoa-commit-growth-seam | scaffold | published | false | true | - | - | eval_ready_but_governance_blocked | - | - |
| aoa-contract-test | canonical | published | true | true | default_reference | context_vs_contract | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-contract-test.md | docs/reviews/status-promotions/aoa-contract-test.md |
| aoa-core-logic-boundary | evaluated | published | true | true | stay_evaluated | core_boundary_refactor | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-core-logic-boundary.md | docs/reviews/status-promotions/aoa-core-logic-boundary.md |
| aoa-dry-run-first | canonical | published | true | true | default_reference | risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-dry-run-first.md | docs/reviews/status-promotions/aoa-dry-run-first.md |
| aoa-invariant-coverage-audit | canonical | published | true | true | default_reference | invariant_authoring_vs_audit | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-invariant-coverage-audit.md | docs/reviews/status-promotions/aoa-invariant-coverage-audit.md |
| aoa-local-stack-bringup | evaluated | published | true | true | stay_evaluated | local_runtime_bringup | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-local-stack-bringup.md | docs/reviews/status-promotions/aoa-local-stack-bringup.md |
| aoa-port-adapter-refactor | evaluated | published | true | true | stay_evaluated | core_boundary_refactor | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-port-adapter-refactor.md | docs/reviews/status-promotions/aoa-port-adapter-refactor.md |
| aoa-property-invariants | canonical | published | true | true | default_reference | invariant_authoring_vs_audit | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-property-invariants.md | docs/reviews/status-promotions/aoa-property-invariants.md |
| aoa-quest-harvest | scaffold | published | false | true | - | - | eval_ready_but_governance_blocked | - | - |
| aoa-safe-infra-change | canonical | published | true | true | default_reference | local_runtime_bringup, risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-safe-infra-change.md | docs/reviews/status-promotions/aoa-safe-infra-change.md |
| aoa-sanitized-share | canonical | published | true | true | default_reference | risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-sanitized-share.md | docs/reviews/status-promotions/aoa-sanitized-share.md |
| aoa-session-donor-harvest | scaffold | published | false | true | - | - | eval_ready_but_governance_blocked | - | - |
| aoa-session-progression-lift | scaffold | published | false | true | - | - | eval_ready_but_governance_blocked | - | - |
| aoa-session-route-forks | scaffold | published | false | true | - | - | eval_ready_but_governance_blocked | - | - |
| aoa-session-self-diagnose | scaffold | published | false | true | - | - | eval_ready_but_governance_blocked | - | - |
| aoa-session-self-repair | scaffold | published | false | true | - | - | eval_ready_but_governance_blocked | - | - |
| aoa-source-of-truth-check | canonical | published | true | true | default_reference | decision_docs_authority | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-source-of-truth-check.md | docs/reviews/status-promotions/aoa-source-of-truth-check.md |
| aoa-summon | scaffold | pending | false | true | - | - | eval_ready_but_governance_blocked | - | - |
| aoa-tdd-slice | canonical | published | true | true | default_reference | change_workflows | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-tdd-slice.md | - |
| atm10-change-protocol | evaluated | published | false | true | - | - | project_overlay_federation_ready | - | docs/reviews/status-promotions/atm10-change-protocol.md |
| atm10-source-of-truth-check | evaluated | published | false | true | - | - | project_overlay_federation_ready | - | docs/reviews/status-promotions/atm10-source-of-truth-check.md |
| titan-approval-ledger | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |
| titan-approval-loom | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |
| titan-appserver-bridge | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |
| titan-appserver-plan | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |
| titan-closeout | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |
| titan-console | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |
| titan-event-replay | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |
| titan-memory-loom | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |
| titan-memory-prune | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |
| titan-mutation-gate | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |
| titan-recall | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |
| titan-receipt | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |
| titan-runtime-gate | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |
| titan-summon | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |
| titan-thread-turn-binding | scaffold | pending | false | true | - | - | project_overlay_eval_ready | - | - |

## Review truth sync

| name | status | lineage | governance decision | review path | reviewed revision | current revision | meaning changed | issues | synced |
|---|---|---|---|---|---|---|---|---|---|
| abyss-safe-infra-change | evaluated | published | - | docs/reviews/status-promotions/abyss-safe-infra-change.md | 9241b2de96a9 | 9241b2de96a9 | False | - | true |
| abyss-sanitized-share | evaluated | published | - | docs/reviews/status-promotions/abyss-sanitized-share.md | ece4e85825d5 | ece4e85825d5 | False | - | true |
| aoa-adr-write | canonical | published | default_reference | docs/reviews/status-promotions/aoa-adr-write.md | 09b00a875a30 | 09b00a875a30 | True | - | true |
| aoa-approval-gate-check | canonical | published | default_reference | docs/reviews/status-promotions/aoa-approval-gate-check.md | 9779fde8cb33 | 9779fde8cb33 | True | - | true |
| aoa-bounded-context-map | canonical | published | default_reference | docs/reviews/status-promotions/aoa-bounded-context-map.md | 053ae549a248 | 053ae549a248 | True | - | true |
| aoa-contract-test | canonical | published | default_reference | docs/reviews/status-promotions/aoa-contract-test.md | 516b6371908c | 516b6371908c | False | - | true |
| aoa-core-logic-boundary | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-core-logic-boundary.md | 03dde8604ec3 | 03dde8604ec3 | False | - | true |
| aoa-dry-run-first | canonical | published | default_reference | docs/reviews/status-promotions/aoa-dry-run-first.md | 1871a24198fe | 1871a24198fe | True | - | true |
| aoa-invariant-coverage-audit | canonical | published | default_reference | docs/reviews/status-promotions/aoa-invariant-coverage-audit.md | c3bfe77e540d | c3bfe77e540d | True | - | true |
| aoa-local-stack-bringup | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-local-stack-bringup.md | 2b902decb446 | 2b902decb446 | False | - | true |
| aoa-port-adapter-refactor | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-port-adapter-refactor.md | e2f144d405aa | e2f144d405aa | False | - | true |
| aoa-property-invariants | canonical | published | default_reference | docs/reviews/status-promotions/aoa-property-invariants.md | 791ea1c445d4 | 791ea1c445d4 | True | - | true |
| aoa-safe-infra-change | canonical | published | default_reference | docs/reviews/status-promotions/aoa-safe-infra-change.md | 7fd2fb96e1cb | 7fd2fb96e1cb | False | - | true |
| aoa-sanitized-share | canonical | published | default_reference | docs/reviews/status-promotions/aoa-sanitized-share.md | df0cebb8654a | df0cebb8654a | True | - | true |
| aoa-source-of-truth-check | canonical | published | default_reference | docs/reviews/status-promotions/aoa-source-of-truth-check.md | eccfc4de7849 | eccfc4de7849 | True | - | true |
| atm10-change-protocol | evaluated | published | - | docs/reviews/status-promotions/atm10-change-protocol.md | 7da6f549a807 | 7da6f549a807 | False | - | true |
| atm10-source-of-truth-check | evaluated | published | - | docs/reviews/status-promotions/atm10-source-of-truth-check.md | b5bf512142eb | b5bf512142eb | False | - | true |

## Cohorts

- `candidate_ready_without_review`: -
- `blocked_by_pending_lineage`: aoa-summon, titan-approval-ledger, titan-approval-loom, titan-appserver-bridge, titan-appserver-plan, titan-closeout, titan-console, titan-event-replay, titan-memory-loom, titan-memory-prune, titan-mutation-gate, titan-recall, titan-receipt, titan-runtime-gate, titan-summon, titan-thread-turn-binding
- `canonical_maintenance`: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice
- `comparative_pending`: aoa-core-logic-boundary, aoa-local-stack-bringup, aoa-port-adapter-refactor
- `review_truth_sync`: -
- `docs_truth_sync`: -

