# Public surface

This derived file summarizes the current public-product surface of `aoa-skills`.
It is built from committed skill bundles, review records, and evaluation fixtures.

## Summary

- total skills: 56
- default references: 12
- default-reference ready skills: 17
- pending technique bridge lineage: 0
- risk surfaces: 5

## Default references

| name | maturity | readiness | scope | invocation | lineage | governance decision | lanes | readiness blockers | technique bridge | promotion review | candidate review |
|---|---|---|---|---|---|---|---|---|---|---|---|
| aoa-adr-write | canonical | ready | core | explicit-preferred | published | default_reference | decision_docs_authority, decision_graph_chain | - | - | `docs/reviews/status-promotions/aoa-adr-write.md` | `docs/reviews/canonical-candidates/aoa-adr-write.md` |
| aoa-approval-gate-check | canonical | ready | risk | explicit-only | published | default_reference | local_runtime_bringup, risk_authority_preview_execution | - | - | `docs/reviews/status-promotions/aoa-approval-gate-check.md` | `docs/reviews/canonical-candidates/aoa-approval-gate-check.md` |
| aoa-bounded-context-map | canonical | ready | core | explicit-preferred | published | default_reference | context_vs_contract, core_boundary_refactor | - | - | `docs/reviews/status-promotions/aoa-bounded-context-map.md` | `docs/reviews/canonical-candidates/aoa-bounded-context-map.md` |
| aoa-change-protocol | canonical | ready | core | explicit-preferred | published | default_reference | change_workflows | - | - | - | `docs/reviews/canonical-candidates/aoa-change-protocol.md` |
| aoa-contract-test | canonical | ready | core | explicit-preferred | published | default_reference | context_vs_contract | - | - | `docs/reviews/status-promotions/aoa-contract-test.md` | `docs/reviews/canonical-candidates/aoa-contract-test.md` |
| aoa-dry-run-first | canonical | ready | risk | explicit-only | published | default_reference | risk_authority_preview_execution | - | - | `docs/reviews/status-promotions/aoa-dry-run-first.md` | `docs/reviews/canonical-candidates/aoa-dry-run-first.md` |
| aoa-invariant-coverage-audit | canonical | ready | core | explicit-preferred | published | default_reference | invariant_authoring_vs_audit | - | - | `docs/reviews/status-promotions/aoa-invariant-coverage-audit.md` | `docs/reviews/canonical-candidates/aoa-invariant-coverage-audit.md` |
| aoa-property-invariants | canonical | ready | core | explicit-preferred | published | default_reference | invariant_authoring_vs_audit | - | - | `docs/reviews/status-promotions/aoa-property-invariants.md` | `docs/reviews/canonical-candidates/aoa-property-invariants.md` |
| aoa-safe-infra-change | canonical | ready | risk | explicit-only | published | default_reference | local_runtime_bringup, risk_authority_preview_execution | - | - | `docs/reviews/status-promotions/aoa-safe-infra-change.md` | `docs/reviews/canonical-candidates/aoa-safe-infra-change.md` |
| aoa-sanitized-share | canonical | ready | risk | explicit-only | published | default_reference | risk_authority_preview_execution | - | - | `docs/reviews/status-promotions/aoa-sanitized-share.md` | `docs/reviews/canonical-candidates/aoa-sanitized-share.md` |
| aoa-source-of-truth-check | canonical | ready | core | explicit-preferred | published | default_reference | decision_docs_authority | - | - | `docs/reviews/status-promotions/aoa-source-of-truth-check.md` | `docs/reviews/canonical-candidates/aoa-source-of-truth-check.md` |
| aoa-tdd-slice | canonical | ready | core | explicit-preferred | published | default_reference | change_workflows | - | - | - | `docs/reviews/canonical-candidates/aoa-tdd-slice.md` |

## Default-reference ready cohort

| name | maturity | readiness | scope | invocation | lineage | governance decision | lanes | readiness blockers | technique bridge | promotion review | candidate review |
|---|---|---|---|---|---|---|---|---|---|---|---|
| aoa-automation-opportunity-scan | evaluated | ready | core | explicit-only | published | stay_evaluated | session_growth_closeout | - | - | `docs/reviews/status-promotions/aoa-automation-opportunity-scan.md` | - |
| aoa-checkpoint-closeout-bridge | evaluated | ready | core | explicit-preferred | published | stay_evaluated | session_growth_closeout | - | - | `docs/reviews/status-promotions/aoa-checkpoint-closeout-bridge.md` | - |
| aoa-commit-growth-seam | evaluated | ready | core | explicit-only | published | stay_evaluated | session_growth_closeout | - | - | `docs/reviews/status-promotions/aoa-commit-growth-seam.md` | - |
| aoa-core-logic-boundary | evaluated | ready | core | explicit-preferred | published | stay_evaluated | core_boundary_refactor | - | - | `docs/reviews/status-promotions/aoa-core-logic-boundary.md` | `docs/reviews/canonical-candidates/aoa-core-logic-boundary.md` |
| aoa-decision | evaluated | ready | core | explicit-preferred | published | stay_evaluated | decision_graph_chain | - | - | `docs/reviews/status-promotions/aoa-decision.md` | - |
| aoa-decision-correct | evaluated | ready | core | explicit-preferred | published | stay_evaluated | decision_graph_chain | - | - | `docs/reviews/status-promotions/aoa-decision-correct.md` | - |
| aoa-decision-create | evaluated | ready | core | explicit-preferred | published | stay_evaluated | decision_graph_chain | - | - | `docs/reviews/status-promotions/aoa-decision-create.md` | - |
| aoa-decision-find | evaluated | ready | core | explicit-preferred | published | stay_evaluated | decision_graph_chain | - | - | `docs/reviews/status-promotions/aoa-decision-find.md` | - |
| aoa-local-stack-bringup | evaluated | ready | risk | explicit-only | published | stay_evaluated | local_runtime_bringup | - | - | `docs/reviews/status-promotions/aoa-local-stack-bringup.md` | `docs/reviews/canonical-candidates/aoa-local-stack-bringup.md` |
| aoa-port-adapter-refactor | evaluated | ready | core | explicit-preferred | published | stay_evaluated | core_boundary_refactor | - | - | `docs/reviews/status-promotions/aoa-port-adapter-refactor.md` | `docs/reviews/canonical-candidates/aoa-port-adapter-refactor.md` |
| aoa-quest-harvest | evaluated | ready | core | explicit-only | published | stay_evaluated | session_growth_closeout | - | - | `docs/reviews/status-promotions/aoa-quest-harvest.md` | - |
| aoa-session-donor-harvest | evaluated | ready | core | explicit-only | published | stay_evaluated | session_growth_closeout | - | - | `docs/reviews/status-promotions/aoa-session-donor-harvest.md` | - |
| aoa-session-progression-lift | evaluated | ready | core | explicit-only | published | stay_evaluated | session_growth_closeout | - | - | `docs/reviews/status-promotions/aoa-session-progression-lift.md` | - |
| aoa-session-route-forks | evaluated | ready | core | explicit-only | published | stay_evaluated | session_growth_closeout | - | - | `docs/reviews/status-promotions/aoa-session-route-forks.md` | - |
| aoa-session-self-diagnose | evaluated | ready | core | explicit-only | published | stay_evaluated | session_growth_closeout | - | - | `docs/reviews/status-promotions/aoa-session-self-diagnose.md` | - |
| aoa-session-self-repair | evaluated | ready | core | explicit-only | published | stay_evaluated | session_growth_closeout | - | - | `docs/reviews/status-promotions/aoa-session-self-repair.md` | - |
| aoa-summon | evaluated | ready | core | explicit-only | published | stay_evaluated | session_growth_closeout | - | - | `docs/reviews/status-promotions/aoa-summon.md` | - |

## Pending technique bridge lineage

| name | maturity | readiness | scope | invocation | lineage | governance decision | lanes | readiness blockers | technique bridge | promotion review | candidate review |
|---|---|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | - | - | - | - | - | - | - | - |

## Risk surfaces

| name | maturity | readiness | scope | invocation | lineage | governance decision | lanes | readiness blockers | technique bridge | promotion review | candidate review |
|---|---|---|---|---|---|---|---|---|---|---|---|
| aoa-approval-gate-check | canonical | ready | risk | explicit-only | published | default_reference | local_runtime_bringup, risk_authority_preview_execution | - | - | `docs/reviews/status-promotions/aoa-approval-gate-check.md` | `docs/reviews/canonical-candidates/aoa-approval-gate-check.md` |
| aoa-dry-run-first | canonical | ready | risk | explicit-only | published | default_reference | risk_authority_preview_execution | - | - | `docs/reviews/status-promotions/aoa-dry-run-first.md` | `docs/reviews/canonical-candidates/aoa-dry-run-first.md` |
| aoa-local-stack-bringup | evaluated | ready | risk | explicit-only | published | stay_evaluated | local_runtime_bringup | - | - | `docs/reviews/status-promotions/aoa-local-stack-bringup.md` | `docs/reviews/canonical-candidates/aoa-local-stack-bringup.md` |
| aoa-safe-infra-change | canonical | ready | risk | explicit-only | published | default_reference | local_runtime_bringup, risk_authority_preview_execution | - | - | `docs/reviews/status-promotions/aoa-safe-infra-change.md` | `docs/reviews/canonical-candidates/aoa-safe-infra-change.md` |
| aoa-sanitized-share | canonical | ready | risk | explicit-only | published | default_reference | risk_authority_preview_execution | - | - | `docs/reviews/status-promotions/aoa-sanitized-share.md` | `docs/reviews/canonical-candidates/aoa-sanitized-share.md` |

## Legend

- `maturity` is the source-owned skill status ladder (`scaffold` through `canonical`).
- `default_reference_readiness` is the derived machine gate for default-reference consideration and stays separate from maturity.
- `ready` means the current machine-readable default-reference gate passes for a governance-eligible path without implying promotion.
- `blocked` means the default-reference path applies, but machine-checkable blockers remain visible.
- `not_applicable` means the default-reference path does not currently apply, most notably for project overlays without a governance lane.
- `stay_evaluated` means the current governance lane decision is to keep the skill evaluated in this wave even though its canonical gate checks may already pass.
- `pending lineage` means upstream technique publication or refresh still needs bridge review; it does not by itself define whether the skill execution object is mature.
- `explicit-only` means the skill requires an explicit invocation posture and policy alignment.
- `candidate_ready` remains in the JSON payload as a compatibility alias for the `default_reference_ready` cohort.

