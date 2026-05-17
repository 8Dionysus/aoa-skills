# Governance backlog

This derived file reconciles repo-local governance readiness and evaluation readiness without changing status.
It is a backlog/maintenance view, not a promotion decision surface.
Project-overlay rows may use overlay-specific reconciliation values when no governance lane exists.
Read those rows as per-skill maintenance signals, not as missing canonical-decision debt.

## Summary

- total skills: 45
- candidate ready without review: 10
- pending technique bridge lineage: 15
- canonical maintenance cohort: 12
- comparative pending cohort: 13
- review truth-sync gaps: 0
- docs truth-sync issues: 0

| name | status | lineage | governance ready | eval ready | governance decision | lanes | reconciliation | candidate review | promotion review |
|---|---|---|---|---|---|---|---|---|---|
| abyss-safe-infra-change | evaluated | published | false | true | - | - | project_overlay_federation_ready | - | docs/reviews/status-promotions/abyss-safe-infra-change.md |
| abyss-sanitized-share | evaluated | published | false | true | - | - | project_overlay_federation_ready | - | docs/reviews/status-promotions/abyss-sanitized-share.md |
| abyss-self-diagnostic-spine | scaffold | published | false | true | - | - | project_overlay_federation_ready | - | - |
| aoa-adr-write | canonical | published | true | true | default_reference | decision_docs_authority | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-adr-write.md | docs/reviews/status-promotions/aoa-adr-write.md |
| aoa-approval-gate-check | canonical | published | true | true | default_reference | local_runtime_bringup, risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-approval-gate-check.md | docs/reviews/status-promotions/aoa-approval-gate-check.md |
| aoa-automation-opportunity-scan | evaluated | published | true | true | stay_evaluated | session_growth_closeout | governance_and_eval_ready | - | docs/reviews/status-promotions/aoa-automation-opportunity-scan.md |
| aoa-bounded-context-map | canonical | published | true | true | default_reference | context_vs_contract, core_boundary_refactor | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-bounded-context-map.md | docs/reviews/status-promotions/aoa-bounded-context-map.md |
| aoa-change-protocol | canonical | published | true | true | default_reference | change_workflows | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-change-protocol.md | - |
| aoa-checkpoint-closeout-bridge | evaluated | published | true | true | stay_evaluated | session_growth_closeout | governance_and_eval_ready | - | docs/reviews/status-promotions/aoa-checkpoint-closeout-bridge.md |
| aoa-commit-growth-seam | evaluated | published | true | true | stay_evaluated | session_growth_closeout | governance_and_eval_ready | - | docs/reviews/status-promotions/aoa-commit-growth-seam.md |
| aoa-contract-test | canonical | published | true | true | default_reference | context_vs_contract | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-contract-test.md | docs/reviews/status-promotions/aoa-contract-test.md |
| aoa-core-logic-boundary | evaluated | published | true | true | stay_evaluated | core_boundary_refactor | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-core-logic-boundary.md | docs/reviews/status-promotions/aoa-core-logic-boundary.md |
| aoa-dry-run-first | canonical | published | true | true | default_reference | risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-dry-run-first.md | docs/reviews/status-promotions/aoa-dry-run-first.md |
| aoa-invariant-coverage-audit | canonical | published | true | true | default_reference | invariant_authoring_vs_audit | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-invariant-coverage-audit.md | docs/reviews/status-promotions/aoa-invariant-coverage-audit.md |
| aoa-local-stack-bringup | evaluated | published | true | true | stay_evaluated | local_runtime_bringup | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-local-stack-bringup.md | docs/reviews/status-promotions/aoa-local-stack-bringup.md |
| aoa-port-adapter-refactor | evaluated | published | true | true | stay_evaluated | core_boundary_refactor | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-port-adapter-refactor.md | docs/reviews/status-promotions/aoa-port-adapter-refactor.md |
| aoa-property-invariants | canonical | published | true | true | default_reference | invariant_authoring_vs_audit | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-property-invariants.md | docs/reviews/status-promotions/aoa-property-invariants.md |
| aoa-quest-harvest | evaluated | published | true | true | stay_evaluated | session_growth_closeout | governance_and_eval_ready | - | docs/reviews/status-promotions/aoa-quest-harvest.md |
| aoa-safe-infra-change | canonical | published | true | true | default_reference | local_runtime_bringup, risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-safe-infra-change.md | docs/reviews/status-promotions/aoa-safe-infra-change.md |
| aoa-sanitized-share | canonical | published | true | true | default_reference | risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-sanitized-share.md | docs/reviews/status-promotions/aoa-sanitized-share.md |
| aoa-session-donor-harvest | evaluated | published | true | true | stay_evaluated | session_growth_closeout | governance_and_eval_ready | - | docs/reviews/status-promotions/aoa-session-donor-harvest.md |
| aoa-session-progression-lift | evaluated | published | true | true | stay_evaluated | session_growth_closeout | governance_and_eval_ready | - | docs/reviews/status-promotions/aoa-session-progression-lift.md |
| aoa-session-route-forks | evaluated | published | true | true | stay_evaluated | session_growth_closeout | governance_and_eval_ready | - | docs/reviews/status-promotions/aoa-session-route-forks.md |
| aoa-session-self-diagnose | evaluated | published | true | true | stay_evaluated | session_growth_closeout | governance_and_eval_ready | - | docs/reviews/status-promotions/aoa-session-self-diagnose.md |
| aoa-session-self-repair | evaluated | published | true | true | stay_evaluated | session_growth_closeout | governance_and_eval_ready | - | docs/reviews/status-promotions/aoa-session-self-repair.md |
| aoa-source-of-truth-check | canonical | published | true | true | default_reference | decision_docs_authority | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-source-of-truth-check.md | docs/reviews/status-promotions/aoa-source-of-truth-check.md |
| aoa-summon | evaluated | published | true | true | stay_evaluated | session_growth_closeout | governance_and_eval_ready | - | docs/reviews/status-promotions/aoa-summon.md |
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
| abyss-safe-infra-change | evaluated | published | - | docs/reviews/status-promotions/abyss-safe-infra-change.md | f97c9d760f3e | f97c9d760f3e | True | - | true |
| abyss-sanitized-share | evaluated | published | - | docs/reviews/status-promotions/abyss-sanitized-share.md | 5bd25d9d8c97 | 5bd25d9d8c97 | True | - | true |
| aoa-adr-write | canonical | published | default_reference | docs/reviews/status-promotions/aoa-adr-write.md | a2f205f916c0 | a2f205f916c0 | True | - | true |
| aoa-approval-gate-check | canonical | published | default_reference | docs/reviews/status-promotions/aoa-approval-gate-check.md | a9093bc2b6b3 | a9093bc2b6b3 | True | - | true |
| aoa-automation-opportunity-scan | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-automation-opportunity-scan.md | a6095d450a17 | a6095d450a17 | True | - | true |
| aoa-bounded-context-map | canonical | published | default_reference | docs/reviews/status-promotions/aoa-bounded-context-map.md | 6f7aa701df3c | 6f7aa701df3c | True | - | true |
| aoa-checkpoint-closeout-bridge | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-checkpoint-closeout-bridge.md | d934a5b62bfb | d934a5b62bfb | True | - | true |
| aoa-commit-growth-seam | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-commit-growth-seam.md | 6326b5e4985a | 6326b5e4985a | True | - | true |
| aoa-contract-test | canonical | published | default_reference | docs/reviews/status-promotions/aoa-contract-test.md | 4e13118e6094 | 4e13118e6094 | True | - | true |
| aoa-core-logic-boundary | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-core-logic-boundary.md | 4c1fe5d5fc55 | 4c1fe5d5fc55 | True | - | true |
| aoa-dry-run-first | canonical | published | default_reference | docs/reviews/status-promotions/aoa-dry-run-first.md | fe0e70f084f5 | fe0e70f084f5 | True | - | true |
| aoa-invariant-coverage-audit | canonical | published | default_reference | docs/reviews/status-promotions/aoa-invariant-coverage-audit.md | 9ec574c0f128 | 9ec574c0f128 | True | - | true |
| aoa-local-stack-bringup | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-local-stack-bringup.md | c126c3a41720 | c126c3a41720 | False | - | true |
| aoa-port-adapter-refactor | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-port-adapter-refactor.md | 1b87f9d61c48 | 1b87f9d61c48 | True | - | true |
| aoa-property-invariants | canonical | published | default_reference | docs/reviews/status-promotions/aoa-property-invariants.md | 25d31fa59624 | 25d31fa59624 | True | - | true |
| aoa-quest-harvest | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-quest-harvest.md | b9e9568a5f1c | b9e9568a5f1c | True | - | true |
| aoa-safe-infra-change | canonical | published | default_reference | docs/reviews/status-promotions/aoa-safe-infra-change.md | 882901e7a920 | 882901e7a920 | False | - | true |
| aoa-sanitized-share | canonical | published | default_reference | docs/reviews/status-promotions/aoa-sanitized-share.md | 4a48a4e10b5d | 4a48a4e10b5d | True | - | true |
| aoa-session-donor-harvest | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-session-donor-harvest.md | ba0484678a8d | ba0484678a8d | True | - | true |
| aoa-session-progression-lift | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-session-progression-lift.md | 179c5348cd75 | 179c5348cd75 | True | - | true |
| aoa-session-route-forks | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-session-route-forks.md | 2781c7c38bc3 | 2781c7c38bc3 | True | - | true |
| aoa-session-self-diagnose | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-session-self-diagnose.md | d319db0ea57d | d319db0ea57d | True | - | true |
| aoa-session-self-repair | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-session-self-repair.md | 17edbf208692 | 17edbf208692 | True | - | true |
| aoa-source-of-truth-check | canonical | published | default_reference | docs/reviews/status-promotions/aoa-source-of-truth-check.md | 7f6e64468a52 | 7f6e64468a52 | True | - | true |
| aoa-summon | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-summon.md | 7e8c8fcae843 | 7e8c8fcae843 | True | - | true |
| atm10-change-protocol | evaluated | published | - | docs/reviews/status-promotions/atm10-change-protocol.md | eb340748d355 | eb340748d355 | True | - | true |
| atm10-source-of-truth-check | evaluated | published | - | docs/reviews/status-promotions/atm10-source-of-truth-check.md | fccd8fdf392a | fccd8fdf392a | True | - | true |

## Cohorts

- `candidate_ready_without_review`: aoa-automation-opportunity-scan, aoa-checkpoint-closeout-bridge, aoa-commit-growth-seam, aoa-quest-harvest, aoa-session-donor-harvest, aoa-session-progression-lift, aoa-session-route-forks, aoa-session-self-diagnose, aoa-session-self-repair, aoa-summon
- `blocked_by_pending_lineage`: titan-approval-ledger, titan-approval-loom, titan-appserver-bridge, titan-appserver-plan, titan-closeout, titan-console, titan-event-replay, titan-memory-loom, titan-memory-prune, titan-mutation-gate, titan-recall, titan-receipt, titan-runtime-gate, titan-summon, titan-thread-turn-binding
- `canonical_maintenance`: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice
- `comparative_pending`: aoa-automation-opportunity-scan, aoa-checkpoint-closeout-bridge, aoa-commit-growth-seam, aoa-core-logic-boundary, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-quest-harvest, aoa-session-donor-harvest, aoa-session-progression-lift, aoa-session-route-forks, aoa-session-self-diagnose, aoa-session-self-repair, aoa-summon
- `review_truth_sync`: -
- `docs_truth_sync`: -

