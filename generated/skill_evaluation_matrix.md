# Skill evaluation matrix

This derived file summarizes deterministic evaluation evidence for `aoa-skills`.
It is built from committed skill bundles, runtime artifacts, review records,
evaluation fixtures, and authored snapshot-backed evidence files.

## Summary

- total skills: 19
- canonical skills: 12
- canonical skills with eval gaps: 0

| name | status | scope | invocation | autonomy | use cases | do_not_use cases | use snapshots | do_not_use snapshots | runtime artifact | promotion review | candidate review | canonical eval ready | blockers |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| abyss-safe-infra-change | evaluated | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/abyss-safe-infra-change/examples/example.md` | `docs/reviews/status-promotions/abyss-safe-infra-change.md` | - | true | - |
| abyss-sanitized-share | evaluated | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/abyss-sanitized-share/examples/example.md` | `docs/reviews/status-promotions/abyss-sanitized-share.md` | - | true | - |
| aoa-adr-write | canonical | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-adr-write/examples/example.md` | `docs/reviews/status-promotions/aoa-adr-write.md` | `docs/reviews/canonical-candidates/aoa-adr-write.md` | true | - |
| aoa-approval-gate-check | canonical | risk | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/aoa-approval-gate-check/examples/runtime.md` | `docs/reviews/status-promotions/aoa-approval-gate-check.md` | `docs/reviews/canonical-candidates/aoa-approval-gate-check.md` | true | - |
| aoa-bounded-context-map | canonical | core | explicit-preferred | 1 | 1 | 2 | 1 | 1 | `skills/aoa-bounded-context-map/examples/example.md` | `docs/reviews/status-promotions/aoa-bounded-context-map.md` | `docs/reviews/canonical-candidates/aoa-bounded-context-map.md` | true | - |
| aoa-change-protocol | canonical | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-change-protocol/examples/runtime.md` | - | `docs/reviews/canonical-candidates/aoa-change-protocol.md` | true | - |
| aoa-contract-test | canonical | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-contract-test/examples/example.md` | `docs/reviews/status-promotions/aoa-contract-test.md` | `docs/reviews/canonical-candidates/aoa-contract-test.md` | true | - |
| aoa-core-logic-boundary | evaluated | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-core-logic-boundary/examples/example.md` | `docs/reviews/status-promotions/aoa-core-logic-boundary.md` | `docs/reviews/canonical-candidates/aoa-core-logic-boundary.md` | true | - |
| aoa-dry-run-first | canonical | risk | explicit-only | 1 | 1 | 2 | 1 | 1 | `skills/aoa-dry-run-first/examples/runtime.md` | `docs/reviews/status-promotions/aoa-dry-run-first.md` | `docs/reviews/canonical-candidates/aoa-dry-run-first.md` | true | - |
| aoa-invariant-coverage-audit | canonical | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-invariant-coverage-audit/examples/example.md` | `docs/reviews/status-promotions/aoa-invariant-coverage-audit.md` | `docs/reviews/canonical-candidates/aoa-invariant-coverage-audit.md` | true | - |
| aoa-local-stack-bringup | evaluated | risk | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/aoa-local-stack-bringup/examples/runtime.md` | `docs/reviews/status-promotions/aoa-local-stack-bringup.md` | `docs/reviews/canonical-candidates/aoa-local-stack-bringup.md` | true | - |
| aoa-port-adapter-refactor | evaluated | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-port-adapter-refactor/examples/example.md` | `docs/reviews/status-promotions/aoa-port-adapter-refactor.md` | `docs/reviews/canonical-candidates/aoa-port-adapter-refactor.md` | true | - |
| aoa-property-invariants | canonical | core | explicit-preferred | 1 | 1 | 2 | 1 | 1 | `skills/aoa-property-invariants/examples/example.md` | `docs/reviews/status-promotions/aoa-property-invariants.md` | `docs/reviews/canonical-candidates/aoa-property-invariants.md` | true | - |
| aoa-safe-infra-change | canonical | risk | explicit-only | 1 | 1 | 2 | 1 | 1 | `skills/aoa-safe-infra-change/examples/runtime.md` | `docs/reviews/status-promotions/aoa-safe-infra-change.md` | `docs/reviews/canonical-candidates/aoa-safe-infra-change.md` | true | - |
| aoa-sanitized-share | canonical | risk | explicit-only | 1 | 1 | 3 | 1 | 1 | `skills/aoa-sanitized-share/examples/runtime.md` | `docs/reviews/status-promotions/aoa-sanitized-share.md` | `docs/reviews/canonical-candidates/aoa-sanitized-share.md` | true | - |
| aoa-source-of-truth-check | canonical | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-source-of-truth-check/examples/example.md` | `docs/reviews/status-promotions/aoa-source-of-truth-check.md` | `docs/reviews/canonical-candidates/aoa-source-of-truth-check.md` | true | - |
| aoa-tdd-slice | canonical | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-tdd-slice/examples/example.md` | - | `docs/reviews/canonical-candidates/aoa-tdd-slice.md` | true | - |
| atm10-change-protocol | evaluated | project | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/atm10-change-protocol/examples/example.md` | `docs/reviews/status-promotions/atm10-change-protocol.md` | - | true | - |
| atm10-source-of-truth-check | evaluated | project | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/atm10-source-of-truth-check/examples/example.md` | `docs/reviews/status-promotions/atm10-source-of-truth-check.md` | - | true | - |

## Reading notes

- Runtime artifacts support inspection and object use, but do not replace `SKILL.md` as the meaning-authoritative source.
- The evaluation matrix is a separate derived evidence layer from the runtime walkthroughs and the public/governance surface.
- In this wave, `canonical` skills must pass the snapshot-backed eval floor; other `evaluated` skills may still show reportable snapshot gaps without failing status.

