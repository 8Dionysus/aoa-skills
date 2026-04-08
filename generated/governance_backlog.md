# Governance backlog

This derived file reconciles repo-local governance readiness and evaluation readiness without changing status.
It is a backlog/maintenance view, not a promotion decision surface.
Project-overlay rows may use overlay-specific reconciliation values when no governance lane exists.
Read those rows as per-skill maintenance signals, not as missing canonical-decision debt.

## Summary

- total skills: 26
- candidate ready without review: 0
- blocked by pending lineage: 0
- canonical maintenance cohort: 12
- comparative pending cohort: 3
- review truth-sync gaps: 17
- docs truth-sync issues: 0

| name | status | lineage | governance ready | eval ready | governance decision | lanes | reconciliation | candidate review | promotion review |
|---|---|---|---|---|---|---|---|---|---|
| abyss-safe-infra-change | evaluated | published | false | true | - | - | project_overlay_federation_ready | - | docs/reviews/status-promotions/abyss-safe-infra-change.md |
| abyss-sanitized-share | evaluated | published | false | true | - | - | project_overlay_federation_ready | - | docs/reviews/status-promotions/abyss-sanitized-share.md |
| aoa-adr-write | canonical | published | true | true | default_reference | decision_docs_authority | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-adr-write.md | docs/reviews/status-promotions/aoa-adr-write.md |
| aoa-approval-gate-check | canonical | published | true | true | default_reference | local_runtime_bringup, risk_authority_preview_execution | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-approval-gate-check.md | docs/reviews/status-promotions/aoa-approval-gate-check.md |
| aoa-automation-opportunity-scan | scaffold | published | false | true | - | - | eval_ready_but_governance_blocked | - | - |
| aoa-bounded-context-map | canonical | published | true | true | default_reference | context_vs_contract, core_boundary_refactor | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-bounded-context-map.md | docs/reviews/status-promotions/aoa-bounded-context-map.md |
| aoa-change-protocol | canonical | published | true | true | default_reference | change_workflows | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-change-protocol.md | - |
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
| aoa-tdd-slice | canonical | published | true | true | default_reference | change_workflows | governance_and_eval_ready | docs/reviews/canonical-candidates/aoa-tdd-slice.md | - |
| atm10-change-protocol | evaluated | published | false | true | - | - | project_overlay_federation_ready | - | docs/reviews/status-promotions/atm10-change-protocol.md |
| atm10-source-of-truth-check | evaluated | published | false | true | - | - | project_overlay_federation_ready | - | docs/reviews/status-promotions/atm10-source-of-truth-check.md |

## Review truth sync

| name | status | lineage | governance decision | review path | reviewed revision | current revision | meaning changed | issues | synced |
|---|---|---|---|---|---|---|---|---|---|
| abyss-safe-infra-change | evaluated | published | - | docs/reviews/status-promotions/abyss-safe-infra-change.md | ade3139d7db3 | cd5c169a6c4c | False | reviewed_revision_mismatch(expected=cd5c169a6c4c, recorded=ade3139d7db3) | false |
| abyss-sanitized-share | evaluated | published | - | docs/reviews/status-promotions/abyss-sanitized-share.md | 80b1a85ce739 | b748332deeb3 | False | reviewed_revision_mismatch(expected=b748332deeb3, recorded=80b1a85ce739) | false |
| aoa-adr-write | canonical | published | default_reference | docs/reviews/status-promotions/aoa-adr-write.md | 79434b7b4046 | 85363f128a32 | True | reviewed_revision_mismatch(expected=85363f128a32, recorded=79434b7b4046) | false |
| aoa-approval-gate-check | canonical | published | default_reference | docs/reviews/status-promotions/aoa-approval-gate-check.md | 60144f9b6720 | 5f5fddc53dbf | True | reviewed_revision_mismatch(expected=5f5fddc53dbf, recorded=60144f9b6720) | false |
| aoa-bounded-context-map | canonical | published | default_reference | docs/reviews/status-promotions/aoa-bounded-context-map.md | 179cc653ed94 | 81d64fe3b35a | False | reviewed_revision_mismatch(expected=81d64fe3b35a, recorded=179cc653ed94) | false |
| aoa-contract-test | canonical | published | default_reference | docs/reviews/status-promotions/aoa-contract-test.md | d55dacb4365e | 630cd7200d6f | False | reviewed_revision_mismatch(expected=630cd7200d6f, recorded=d55dacb4365e) | false |
| aoa-core-logic-boundary | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-core-logic-boundary.md | 2bef71351866 | edc922f89c31 | False | reviewed_revision_mismatch(expected=edc922f89c31, recorded=2bef71351866) | false |
| aoa-dry-run-first | canonical | published | default_reference | docs/reviews/status-promotions/aoa-dry-run-first.md | 968dec89b040 | a36559876459 | True | reviewed_revision_mismatch(expected=a36559876459, recorded=968dec89b040) | false |
| aoa-invariant-coverage-audit | canonical | published | default_reference | docs/reviews/status-promotions/aoa-invariant-coverage-audit.md | 150029c46b64 | bae3ee49239c | True | reviewed_revision_mismatch(expected=bae3ee49239c, recorded=150029c46b64) | false |
| aoa-local-stack-bringup | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-local-stack-bringup.md | a29b29ed6402 | 25ce8d3dfd74 | False | reviewed_revision_mismatch(expected=25ce8d3dfd74, recorded=a29b29ed6402) | false |
| aoa-port-adapter-refactor | evaluated | published | stay_evaluated | docs/reviews/status-promotions/aoa-port-adapter-refactor.md | dcd7ba77858f | ae55c27f1def | False | reviewed_revision_mismatch(expected=ae55c27f1def, recorded=dcd7ba77858f) | false |
| aoa-property-invariants | canonical | published | default_reference | docs/reviews/status-promotions/aoa-property-invariants.md | 3c46d42a16e4 | 583b00c7022b | True | reviewed_revision_mismatch(expected=583b00c7022b, recorded=3c46d42a16e4) | false |
| aoa-safe-infra-change | canonical | published | default_reference | docs/reviews/status-promotions/aoa-safe-infra-change.md | c19470b0d9b8 | be3c837ac0ef | False | reviewed_revision_mismatch(expected=be3c837ac0ef, recorded=c19470b0d9b8) | false |
| aoa-sanitized-share | canonical | published | default_reference | docs/reviews/status-promotions/aoa-sanitized-share.md | 609be0fb9853 | 66e22f9be20a | True | reviewed_revision_mismatch(expected=66e22f9be20a, recorded=609be0fb9853) | false |
| aoa-source-of-truth-check | canonical | published | default_reference | docs/reviews/status-promotions/aoa-source-of-truth-check.md | 6a765363cb55 | d05107b7628c | True | reviewed_revision_mismatch(expected=d05107b7628c, recorded=6a765363cb55) | false |
| atm10-change-protocol | evaluated | published | - | docs/reviews/status-promotions/atm10-change-protocol.md | 167344a9bfa8 | d619f3e2e5c3 | False | reviewed_revision_mismatch(expected=d619f3e2e5c3, recorded=167344a9bfa8) | false |
| atm10-source-of-truth-check | evaluated | published | - | docs/reviews/status-promotions/atm10-source-of-truth-check.md | 276bb620c2df | 2e1ac0095772 | False | reviewed_revision_mismatch(expected=2e1ac0095772, recorded=276bb620c2df) | false |

## Cohorts

- `candidate_ready_without_review`: -
- `blocked_by_pending_lineage`: -
- `canonical_maintenance`: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice
- `comparative_pending`: aoa-core-logic-boundary, aoa-local-stack-bringup, aoa-port-adapter-refactor
- `review_truth_sync`: abyss-safe-infra-change, abyss-sanitized-share, aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, atm10-change-protocol, atm10-source-of-truth-check
- `docs_truth_sync`: -

