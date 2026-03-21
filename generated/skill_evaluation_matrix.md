# Skill evaluation matrix

This derived file summarizes deterministic evaluation evidence for `aoa-skills`.
It is built from committed skill bundles, runtime artifacts, review records,
evaluation fixtures, and authored snapshot-backed evidence files.

## Summary

- total skills: 14
- canonical skills: 6
- canonical skills with eval gaps: 0

| name | status | scope | invocation | autonomy | use cases | do_not_use cases | use snapshots | do_not_use snapshots | runtime artifact | promotion review | candidate review | canonical eval ready | blockers |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| aoa-adr-write | evaluated | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-adr-write/examples/example.md` | `docs/reviews/status-promotions/aoa-adr-write.md` | - | true | - |
| aoa-approval-gate-check | evaluated | risk | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/aoa-approval-gate-check/examples/runtime.md` | `docs/reviews/status-promotions/aoa-approval-gate-check.md` | `docs/reviews/canonical-candidates/aoa-approval-gate-check.md` | true | - |
| aoa-bounded-context-map | canonical | core | explicit-preferred | 1 | 1 | 2 | 1 | 1 | `skills/aoa-bounded-context-map/examples/example.md` | `docs/reviews/status-promotions/aoa-bounded-context-map.md` | `docs/reviews/canonical-candidates/aoa-bounded-context-map.md` | true | - |
| aoa-change-protocol | canonical | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-change-protocol/examples/runtime.md` | - | `docs/reviews/canonical-candidates/aoa-change-protocol.md` | true | - |
| aoa-contract-test | canonical | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-contract-test/examples/example.md` | `docs/reviews/status-promotions/aoa-contract-test.md` | `docs/reviews/canonical-candidates/aoa-contract-test.md` | true | - |
| aoa-core-logic-boundary | evaluated | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-core-logic-boundary/examples/example.md` | `docs/reviews/status-promotions/aoa-core-logic-boundary.md` | - | true | - |
| aoa-dry-run-first | evaluated | risk | explicit-only | 1 | 1 | 2 | 1 | 1 | `skills/aoa-dry-run-first/examples/runtime.md` | `docs/reviews/status-promotions/aoa-dry-run-first.md` | - | true | - |
| aoa-invariant-coverage-audit | canonical | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-invariant-coverage-audit/examples/example.md` | `docs/reviews/status-promotions/aoa-invariant-coverage-audit.md` | `docs/reviews/canonical-candidates/aoa-invariant-coverage-audit.md` | true | - |
| aoa-port-adapter-refactor | evaluated | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-port-adapter-refactor/examples/example.md` | `docs/reviews/status-promotions/aoa-port-adapter-refactor.md` | - | true | - |
| aoa-property-invariants | canonical | core | explicit-preferred | 1 | 1 | 2 | 1 | 1 | `skills/aoa-property-invariants/examples/example.md` | `docs/reviews/status-promotions/aoa-property-invariants.md` | `docs/reviews/canonical-candidates/aoa-property-invariants.md` | true | - |
| aoa-safe-infra-change | evaluated | risk | explicit-only | 1 | 1 | 2 | 1 | 1 | `skills/aoa-safe-infra-change/examples/runtime.md` | `docs/reviews/status-promotions/aoa-safe-infra-change.md` | - | true | - |
| aoa-sanitized-share | evaluated | risk | explicit-only | 1 | 1 | 3 | 1 | 1 | `skills/aoa-sanitized-share/examples/runtime.md` | `docs/reviews/status-promotions/aoa-sanitized-share.md` | - | true | - |
| aoa-source-of-truth-check | evaluated | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-source-of-truth-check/examples/example.md` | `docs/reviews/status-promotions/aoa-source-of-truth-check.md` | - | true | - |
| aoa-tdd-slice | canonical | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/aoa-tdd-slice/examples/example.md` | - | `docs/reviews/canonical-candidates/aoa-tdd-slice.md` | true | - |

## Reading notes

- Runtime artifacts support inspection and object use, but do not replace `SKILL.md` as the meaning-authoritative source.
- The evaluation matrix is a separate derived evidence layer from the runtime walkthroughs and the public/governance surface.
- In this wave, `canonical` skills must pass the snapshot-backed eval floor; other `evaluated` skills may still show reportable snapshot gaps without failing status.

