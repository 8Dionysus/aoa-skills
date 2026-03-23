# Public surface

This derived file summarizes the current public-product surface of `aoa-skills`.
It is built from committed skill bundles, review records, and evaluation fixtures.

## Summary

- total skills: 16
- default references: 7
- candidate-ready skills: 7
- blocked by pending lineage: 0
- risk surfaces: 4

## Default references

| name | status | scope | invocation | lineage | blockers | promotion review | candidate review |
|---|---|---|---|---|---|---|---|
| aoa-approval-gate-check | canonical | risk | explicit-only | published | - | `docs/reviews/status-promotions/aoa-approval-gate-check.md` | `docs/reviews/canonical-candidates/aoa-approval-gate-check.md` |
| aoa-bounded-context-map | canonical | core | explicit-preferred | published | - | `docs/reviews/status-promotions/aoa-bounded-context-map.md` | `docs/reviews/canonical-candidates/aoa-bounded-context-map.md` |
| aoa-change-protocol | canonical | core | explicit-preferred | published | - | - | `docs/reviews/canonical-candidates/aoa-change-protocol.md` |
| aoa-contract-test | canonical | core | explicit-preferred | published | - | `docs/reviews/status-promotions/aoa-contract-test.md` | `docs/reviews/canonical-candidates/aoa-contract-test.md` |
| aoa-invariant-coverage-audit | canonical | core | explicit-preferred | published | - | `docs/reviews/status-promotions/aoa-invariant-coverage-audit.md` | `docs/reviews/canonical-candidates/aoa-invariant-coverage-audit.md` |
| aoa-property-invariants | canonical | core | explicit-preferred | published | - | `docs/reviews/status-promotions/aoa-property-invariants.md` | `docs/reviews/canonical-candidates/aoa-property-invariants.md` |
| aoa-tdd-slice | canonical | core | explicit-preferred | published | - | - | `docs/reviews/canonical-candidates/aoa-tdd-slice.md` |

## Candidate-ready cohort

| name | status | scope | invocation | lineage | blockers | promotion review | candidate review |
|---|---|---|---|---|---|---|---|
| aoa-adr-write | evaluated | core | explicit-preferred | published | - | `docs/reviews/status-promotions/aoa-adr-write.md` | `docs/reviews/canonical-candidates/aoa-adr-write.md` |
| aoa-core-logic-boundary | evaluated | core | explicit-preferred | published | - | `docs/reviews/status-promotions/aoa-core-logic-boundary.md` | `docs/reviews/canonical-candidates/aoa-core-logic-boundary.md` |
| aoa-dry-run-first | evaluated | risk | explicit-only | published | - | `docs/reviews/status-promotions/aoa-dry-run-first.md` | `docs/reviews/canonical-candidates/aoa-dry-run-first.md` |
| aoa-port-adapter-refactor | evaluated | core | explicit-preferred | published | - | `docs/reviews/status-promotions/aoa-port-adapter-refactor.md` | `docs/reviews/canonical-candidates/aoa-port-adapter-refactor.md` |
| aoa-safe-infra-change | evaluated | risk | explicit-only | published | - | `docs/reviews/status-promotions/aoa-safe-infra-change.md` | `docs/reviews/canonical-candidates/aoa-safe-infra-change.md` |
| aoa-sanitized-share | evaluated | risk | explicit-only | published | - | `docs/reviews/status-promotions/aoa-sanitized-share.md` | `docs/reviews/canonical-candidates/aoa-sanitized-share.md` |
| aoa-source-of-truth-check | evaluated | core | explicit-preferred | published | - | `docs/reviews/status-promotions/aoa-source-of-truth-check.md` | `docs/reviews/canonical-candidates/aoa-source-of-truth-check.md` |

## Blocked by pending lineage

| name | status | scope | invocation | lineage | blockers | promotion review | candidate review |
|---|---|---|---|---|---|---|---|
| - | - | - | - | - | - | - | - |

## Risk surfaces

| name | status | scope | invocation | lineage | blockers | promotion review | candidate review |
|---|---|---|---|---|---|---|---|
| aoa-approval-gate-check | canonical | risk | explicit-only | published | - | `docs/reviews/status-promotions/aoa-approval-gate-check.md` | `docs/reviews/canonical-candidates/aoa-approval-gate-check.md` |
| aoa-dry-run-first | evaluated | risk | explicit-only | published | - | `docs/reviews/status-promotions/aoa-dry-run-first.md` | `docs/reviews/canonical-candidates/aoa-dry-run-first.md` |
| aoa-safe-infra-change | evaluated | risk | explicit-only | published | - | `docs/reviews/status-promotions/aoa-safe-infra-change.md` | `docs/reviews/canonical-candidates/aoa-safe-infra-change.md` |
| aoa-sanitized-share | evaluated | risk | explicit-only | published | - | `docs/reviews/status-promotions/aoa-sanitized-share.md` | `docs/reviews/canonical-candidates/aoa-sanitized-share.md` |

## Legend

- `canonical` means the skill is the current default public reference for its workflow class.
- `evaluated` means behavior-oriented evidence exists, but it is not automatically a default reference.
- `candidate_ready` means the current machine-readable canonical gate checks pass without implying promotion.
- `pending lineage` means upstream technique publication or refresh still blocks the canonical path.
- `explicit-only` means the skill requires an explicit invocation posture and policy alignment.

