# Public surface

This derived file summarizes the current public-product surface of `aoa-skills`.
It is built from committed skill bundles, review records, and evaluation fixtures.

## Summary

- total skills: 45
- default references: 12
- default-reference ready skills: 3
- blocked by pending lineage: 16
- risk surfaces: 5

## Default references

| name | maturity | readiness | scope | invocation | lineage | governance decision | lanes | readiness blockers | promotion review | candidate review |
|---|---|---|---|---|---|---|---|---|---|---|
| aoa-adr-write | canonical | ready | core | explicit-preferred | published | default_reference | decision_docs_authority | - | `docs/reviews/status-promotions/aoa-adr-write.md` | `docs/reviews/canonical-candidates/aoa-adr-write.md` |
| aoa-approval-gate-check | canonical | ready | risk | explicit-only | published | default_reference | local_runtime_bringup, risk_authority_preview_execution | - | `docs/reviews/status-promotions/aoa-approval-gate-check.md` | `docs/reviews/canonical-candidates/aoa-approval-gate-check.md` |
| aoa-bounded-context-map | canonical | ready | core | explicit-preferred | published | default_reference | context_vs_contract, core_boundary_refactor | - | `docs/reviews/status-promotions/aoa-bounded-context-map.md` | `docs/reviews/canonical-candidates/aoa-bounded-context-map.md` |
| aoa-change-protocol | canonical | ready | core | explicit-preferred | published | default_reference | change_workflows | - | - | `docs/reviews/canonical-candidates/aoa-change-protocol.md` |
| aoa-contract-test | canonical | ready | core | explicit-preferred | published | default_reference | context_vs_contract | - | `docs/reviews/status-promotions/aoa-contract-test.md` | `docs/reviews/canonical-candidates/aoa-contract-test.md` |
| aoa-dry-run-first | canonical | ready | risk | explicit-only | published | default_reference | risk_authority_preview_execution | - | `docs/reviews/status-promotions/aoa-dry-run-first.md` | `docs/reviews/canonical-candidates/aoa-dry-run-first.md` |
| aoa-invariant-coverage-audit | canonical | ready | core | explicit-preferred | published | default_reference | invariant_authoring_vs_audit | - | `docs/reviews/status-promotions/aoa-invariant-coverage-audit.md` | `docs/reviews/canonical-candidates/aoa-invariant-coverage-audit.md` |
| aoa-property-invariants | canonical | ready | core | explicit-preferred | published | default_reference | invariant_authoring_vs_audit | - | `docs/reviews/status-promotions/aoa-property-invariants.md` | `docs/reviews/canonical-candidates/aoa-property-invariants.md` |
| aoa-safe-infra-change | canonical | ready | risk | explicit-only | published | default_reference | local_runtime_bringup, risk_authority_preview_execution | - | `docs/reviews/status-promotions/aoa-safe-infra-change.md` | `docs/reviews/canonical-candidates/aoa-safe-infra-change.md` |
| aoa-sanitized-share | canonical | ready | risk | explicit-only | published | default_reference | risk_authority_preview_execution | - | `docs/reviews/status-promotions/aoa-sanitized-share.md` | `docs/reviews/canonical-candidates/aoa-sanitized-share.md` |
| aoa-source-of-truth-check | canonical | ready | core | explicit-preferred | published | default_reference | decision_docs_authority | - | `docs/reviews/status-promotions/aoa-source-of-truth-check.md` | `docs/reviews/canonical-candidates/aoa-source-of-truth-check.md` |
| aoa-tdd-slice | canonical | ready | core | explicit-preferred | published | default_reference | change_workflows | - | - | `docs/reviews/canonical-candidates/aoa-tdd-slice.md` |

## Default-reference ready cohort

| name | maturity | readiness | scope | invocation | lineage | governance decision | lanes | readiness blockers | promotion review | candidate review |
|---|---|---|---|---|---|---|---|---|---|---|
| aoa-core-logic-boundary | evaluated | ready | core | explicit-preferred | published | stay_evaluated | core_boundary_refactor | - | `docs/reviews/status-promotions/aoa-core-logic-boundary.md` | `docs/reviews/canonical-candidates/aoa-core-logic-boundary.md` |
| aoa-local-stack-bringup | evaluated | ready | risk | explicit-only | published | stay_evaluated | local_runtime_bringup | - | `docs/reviews/status-promotions/aoa-local-stack-bringup.md` | `docs/reviews/canonical-candidates/aoa-local-stack-bringup.md` |
| aoa-port-adapter-refactor | evaluated | ready | core | explicit-preferred | published | stay_evaluated | core_boundary_refactor | - | `docs/reviews/status-promotions/aoa-port-adapter-refactor.md` | `docs/reviews/canonical-candidates/aoa-port-adapter-refactor.md` |

## Blocked by pending lineage

| name | maturity | readiness | scope | invocation | lineage | governance decision | lanes | readiness blockers | promotion review | candidate review |
|---|---|---|---|---|---|---|---|---|---|---|
| aoa-summon | scaffold | blocked | core | explicit-only | pending | - | - | status_below_evaluated, pending_technique_dependencies, pending_technique_entries, tbd_technique_refs, missing_autonomy_check | - | - |
| titan-approval-ledger | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |
| titan-approval-loom | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |
| titan-appserver-bridge | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |
| titan-appserver-plan | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |
| titan-closeout | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |
| titan-console | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |
| titan-event-replay | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |
| titan-memory-loom | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |
| titan-memory-prune | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |
| titan-mutation-gate | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |
| titan-recall | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |
| titan-receipt | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |
| titan-runtime-gate | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |
| titan-summon | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |
| titan-thread-turn-binding | scaffold | not_applicable | project | explicit-only | pending | - | - | - | - | - |

## Risk surfaces

| name | maturity | readiness | scope | invocation | lineage | governance decision | lanes | readiness blockers | promotion review | candidate review |
|---|---|---|---|---|---|---|---|---|---|---|
| aoa-approval-gate-check | canonical | ready | risk | explicit-only | published | default_reference | local_runtime_bringup, risk_authority_preview_execution | - | `docs/reviews/status-promotions/aoa-approval-gate-check.md` | `docs/reviews/canonical-candidates/aoa-approval-gate-check.md` |
| aoa-dry-run-first | canonical | ready | risk | explicit-only | published | default_reference | risk_authority_preview_execution | - | `docs/reviews/status-promotions/aoa-dry-run-first.md` | `docs/reviews/canonical-candidates/aoa-dry-run-first.md` |
| aoa-local-stack-bringup | evaluated | ready | risk | explicit-only | published | stay_evaluated | local_runtime_bringup | - | `docs/reviews/status-promotions/aoa-local-stack-bringup.md` | `docs/reviews/canonical-candidates/aoa-local-stack-bringup.md` |
| aoa-safe-infra-change | canonical | ready | risk | explicit-only | published | default_reference | local_runtime_bringup, risk_authority_preview_execution | - | `docs/reviews/status-promotions/aoa-safe-infra-change.md` | `docs/reviews/canonical-candidates/aoa-safe-infra-change.md` |
| aoa-sanitized-share | canonical | ready | risk | explicit-only | published | default_reference | risk_authority_preview_execution | - | `docs/reviews/status-promotions/aoa-sanitized-share.md` | `docs/reviews/canonical-candidates/aoa-sanitized-share.md` |

## Legend

- `maturity` is the source-owned skill status ladder (`scaffold` through `canonical`).
- `default_reference_readiness` is the derived machine gate for default-reference consideration and stays separate from maturity.
- `ready` means the current machine-readable default-reference gate passes for a governance-eligible path without implying promotion.
- `blocked` means the default-reference path applies, but machine-checkable blockers remain visible.
- `not_applicable` means the default-reference path does not currently apply, most notably for project overlays without a governance lane.
- `stay_evaluated` means the current governance lane decision is to keep the skill evaluated in this wave even though its canonical gate checks may already pass.
- `pending lineage` means upstream technique publication or refresh still blocks the canonical path.
- `explicit-only` means the skill requires an explicit invocation posture and policy alignment.
- `candidate_ready` remains in the JSON payload as a compatibility alias for the `default_reference_ready` cohort.

