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
| abyss-safe-infra-change | evaluated | published | - | docs/reviews/status-promotions/abyss-safe-infra-change.md | 0e1ee104cc89 | 0e1ee104cc89 | False | - | true |
| abyss-sanitized-share | evaluated | published | - | docs/reviews/status-promotions/abyss-sanitized-share.md | 4a6daab9622e | 4a6daab9622e | False | - | true |
| aoa-adr-write | canonical | published | default_reference | docs/reviews/status-promotions/aoa-adr-write.md | d73659d46c84 | d73659d46c84 | True | - | true |
| aoa-approval-gate-check | canonical | published | default_reference | docs/reviews/status-promotions/aoa-approval-gate-check.md | aaf152665bb6 | aaf152665bb6 | True | - | true |
| aoa-automation-opportunity-scan | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-automation-opportunity-scan.md | f23c6710e33b | f23c6710e33b | True | - | true |
| aoa-bounded-context-map | canonical | published | default_reference | docs/reviews/status-promotions/aoa-bounded-context-map.md | e921dd56d297 | e921dd56d297 | True | - | true |
| aoa-checkpoint-closeout-bridge | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-checkpoint-closeout-bridge.md | c835d142ef43 | c835d142ef43 | True | - | true |
| aoa-commit-growth-seam | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-commit-growth-seam.md | e27275438ccf | e27275438ccf | True | - | true |
| aoa-contract-test | canonical | published | default_reference | docs/reviews/status-promotions/aoa-contract-test.md | 897b7fddb02f | 897b7fddb02f | True | - | true |
| aoa-core-logic-boundary | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-core-logic-boundary.md | cc0dc8cd84d8 | cc0dc8cd84d8 | True | - | true |
| aoa-dry-run-first | canonical | published | default_reference | docs/reviews/status-promotions/aoa-dry-run-first.md | fcef34109123 | fcef34109123 | True | - | true |
| aoa-invariant-coverage-audit | canonical | published | default_reference | docs/reviews/status-promotions/aoa-invariant-coverage-audit.md | feeb4ae634fb | feeb4ae634fb | True | - | true |
| aoa-local-stack-bringup | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-local-stack-bringup.md | 962e39b9bcbe | 962e39b9bcbe | False | - | true |
| aoa-port-adapter-refactor | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-port-adapter-refactor.md | 38a599987abb | 38a599987abb | True | - | true |
| aoa-property-invariants | canonical | published | default_reference | docs/reviews/status-promotions/aoa-property-invariants.md | d79309999a7c | d79309999a7c | True | - | true |
| aoa-quest-harvest | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-quest-harvest.md | beb109a2ad4a | beb109a2ad4a | True | - | true |
| aoa-safe-infra-change | canonical | published | default_reference | docs/reviews/status-promotions/aoa-safe-infra-change.md | be0c1056c17a | be0c1056c17a | False | - | true |
| aoa-sanitized-share | canonical | published | default_reference | docs/reviews/status-promotions/aoa-sanitized-share.md | 1ae7817b49fa | 1ae7817b49fa | True | - | true |
| aoa-session-donor-harvest | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-session-donor-harvest.md | a9dbfbe54953 | a9dbfbe54953 | True | - | true |
| aoa-session-progression-lift | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-session-progression-lift.md | 3c0e0a1dd572 | 3c0e0a1dd572 | True | - | true |
| aoa-session-route-forks | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-session-route-forks.md | f293a9bc116e | f293a9bc116e | True | - | true |
| aoa-session-self-diagnose | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-session-self-diagnose.md | 8699efef95b6 | 8699efef95b6 | True | - | true |
| aoa-session-self-repair | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-session-self-repair.md | aeb50edcd1ed | aeb50edcd1ed | True | - | true |
| aoa-source-of-truth-check | canonical | published | default_reference | docs/reviews/status-promotions/aoa-source-of-truth-check.md | 5d049efb957c | 5d049efb957c | True | - | true |
| aoa-summon | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-summon.md | ba7c03bf9d25 | ba7c03bf9d25 | True | - | true |
| atm10-change-protocol | evaluated | published | - | docs/reviews/status-promotions/atm10-change-protocol.md | 91afd96b4d3a | 91afd96b4d3a | False | - | true |
| atm10-source-of-truth-check | evaluated | published | - | docs/reviews/status-promotions/atm10-source-of-truth-check.md | 902b2bdcd7ba | 902b2bdcd7ba | False | - | true |

## Cohorts

- `candidate_ready_without_review`: aoa-automation-opportunity-scan, aoa-checkpoint-closeout-bridge, aoa-commit-growth-seam, aoa-quest-harvest, aoa-session-donor-harvest, aoa-session-progression-lift, aoa-session-route-forks, aoa-session-self-diagnose, aoa-session-self-repair, aoa-summon
- `blocked_by_pending_lineage`: titan-approval-ledger, titan-approval-loom, titan-appserver-bridge, titan-appserver-plan, titan-closeout, titan-console, titan-event-replay, titan-memory-loom, titan-memory-prune, titan-mutation-gate, titan-recall, titan-receipt, titan-runtime-gate, titan-summon, titan-thread-turn-binding
- `canonical_maintenance`: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice
- `comparative_pending`: aoa-automation-opportunity-scan, aoa-checkpoint-closeout-bridge, aoa-commit-growth-seam, aoa-core-logic-boundary, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-quest-harvest, aoa-session-donor-harvest, aoa-session-progression-lift, aoa-session-route-forks, aoa-session-self-diagnose, aoa-session-self-repair, aoa-summon
- `review_truth_sync`: -
- `docs_truth_sync`: -

