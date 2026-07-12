# Skill evaluation matrix

This derived file summarizes deterministic evaluation evidence for `aoa-skills`.
It is built from committed skill bundles, runtime artifacts, review records,
evaluation fixtures, and authored snapshot-backed evidence files.

## Summary

- total skills: 57
- canonical skills: 12
- canonical skills with eval gaps: 0

| name | status | scope | invocation | autonomy | use cases | do_not_use cases | use snapshots | do_not_use snapshots | runtime artifact | promotion review | candidate review | canonical eval ready | blockers |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| abyss-safe-infra-change | evaluated | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/abyss/abyss-safe-infra-change/examples/example.md` | `docs/reviews/status-promotions/abyss-safe-infra-change.md` | - | true | - |
| abyss-sanitized-share | evaluated | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/abyss/abyss-sanitized-share/examples/example.md` | `docs/reviews/status-promotions/abyss-sanitized-share.md` | - | true | - |
| abyss-self-diagnostic-spine | scaffold | project | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/project/abyss/abyss-self-diagnostic-spine/examples/example.md` | - | - | true | - |
| aoa-adr-write | canonical | core | explicit-preferred | 1 | 2 | 6 | 1 | 1 | `skills/core/engineering/aoa-adr-write/examples/example.md` | `docs/reviews/status-promotions/aoa-adr-write.md` | `docs/reviews/canonical-candidates/aoa-adr-write.md` | true | - |
| aoa-approval-gate-check | canonical | risk | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/risk/aoa-approval-gate-check/examples/runtime.md` | `docs/reviews/status-promotions/aoa-approval-gate-check.md` | `docs/reviews/canonical-candidates/aoa-approval-gate-check.md` | true | - |
| aoa-automation-opportunity-scan | evaluated | core | explicit-only | 1 | 2 | 1 | 1 | 1 | `skills/core/session-growth/aoa-automation-opportunity-scan/examples/runtime.md` | `docs/reviews/status-promotions/aoa-automation-opportunity-scan.md` | - | true | - |
| aoa-bounded-context-map | canonical | core | explicit-preferred | 1 | 2 | 4 | 1 | 1 | `skills/core/engineering/aoa-bounded-context-map/examples/example.md` | `docs/reviews/status-promotions/aoa-bounded-context-map.md` | `docs/reviews/canonical-candidates/aoa-bounded-context-map.md` | true | - |
| aoa-change-protocol | canonical | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/core/engineering/aoa-change-protocol/examples/runtime.md` | - | `docs/reviews/canonical-candidates/aoa-change-protocol.md` | true | - |
| aoa-checkpoint-closeout-bridge | evaluated | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/core/session-growth/aoa-checkpoint-closeout-bridge/examples/runtime.md` | `docs/reviews/status-promotions/aoa-checkpoint-closeout-bridge.md` | - | true | - |
| aoa-commit-growth-seam | evaluated | core | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/core/session-growth/aoa-commit-growth-seam/examples/runtime.md` | `docs/reviews/status-promotions/aoa-commit-growth-seam.md` | - | true | - |
| aoa-contract-test | canonical | core | explicit-preferred | 1 | 3 | 3 | 1 | 1 | `skills/core/engineering/aoa-contract-test/examples/example.md` | `docs/reviews/status-promotions/aoa-contract-test.md` | `docs/reviews/canonical-candidates/aoa-contract-test.md` | true | - |
| aoa-core-logic-boundary | evaluated | core | explicit-preferred | 1 | 3 | 3 | 1 | 1 | `skills/core/engineering/aoa-core-logic-boundary/examples/example.md` | `docs/reviews/status-promotions/aoa-core-logic-boundary.md` | `docs/reviews/canonical-candidates/aoa-core-logic-boundary.md` | true | - |
| aoa-decision | evaluated | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/core/engineering/aoa-decision/checks/review.md` | `docs/reviews/status-promotions/aoa-decision.md` | - | true | - |
| aoa-decision-correct | evaluated | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/core/engineering/aoa-decision-correct/checks/review.md` | `docs/reviews/status-promotions/aoa-decision-correct.md` | - | true | - |
| aoa-decision-create | evaluated | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/core/engineering/aoa-decision-create/checks/review.md` | `docs/reviews/status-promotions/aoa-decision-create.md` | - | true | - |
| aoa-decision-find | evaluated | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/core/engineering/aoa-decision-find/checks/review.md` | `docs/reviews/status-promotions/aoa-decision-find.md` | - | true | - |
| aoa-dry-run-first | canonical | risk | explicit-only | 1 | 1 | 2 | 1 | 1 | `skills/risk/aoa-dry-run-first/examples/runtime.md` | `docs/reviews/status-promotions/aoa-dry-run-first.md` | `docs/reviews/canonical-candidates/aoa-dry-run-first.md` | true | - |
| aoa-eval | scaffold | core | explicit-preferred | 1 | 6 | 3 | 2 | 2 | `skills/core/engineering/aoa-eval/examples/runtime.md` | - | - | true | - |
| aoa-eval-apply | scaffold | core | explicit-preferred | 1 | 2 | 1 | 2 | 1 | `skills/core/engineering/aoa-eval-apply/examples/runtime.md` | - | - | true | - |
| aoa-eval-design | scaffold | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/core/engineering/aoa-eval-design/examples/runtime.md` | - | - | true | - |
| aoa-eval-local-need | scaffold | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/core/engineering/aoa-eval-local-need/examples/runtime.md` | - | - | true | - |
| aoa-eval-select | scaffold | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/core/engineering/aoa-eval-select/examples/runtime.md` | - | - | true | - |
| aoa-eval-session-mining | scaffold | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/core/engineering/aoa-eval-session-mining/examples/runtime.md` | - | - | true | - |
| aoa-invariant-coverage-audit | canonical | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/core/engineering/aoa-invariant-coverage-audit/examples/example.md` | `docs/reviews/status-promotions/aoa-invariant-coverage-audit.md` | `docs/reviews/canonical-candidates/aoa-invariant-coverage-audit.md` | true | - |
| aoa-local-stack-bringup | evaluated | risk | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/risk/aoa-local-stack-bringup/examples/runtime.md` | `docs/reviews/status-promotions/aoa-local-stack-bringup.md` | `docs/reviews/canonical-candidates/aoa-local-stack-bringup.md` | true | - |
| aoa-memo-writeback | scaffold | core | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/core/session-growth/aoa-memo-writeback/examples/runtime.md` | - | - | true | - |
| aoa-port-adapter-refactor | evaluated | core | explicit-preferred | 1 | 2 | 2 | 1 | 1 | `skills/core/engineering/aoa-port-adapter-refactor/examples/example.md` | `docs/reviews/status-promotions/aoa-port-adapter-refactor.md` | `docs/reviews/canonical-candidates/aoa-port-adapter-refactor.md` | true | - |
| aoa-property-invariants | canonical | core | explicit-preferred | 1 | 2 | 3 | 1 | 1 | `skills/core/engineering/aoa-property-invariants/examples/example.md` | `docs/reviews/status-promotions/aoa-property-invariants.md` | `docs/reviews/canonical-candidates/aoa-property-invariants.md` | true | - |
| aoa-quest-harvest | evaluated | core | explicit-only | 1 | 2 | 1 | 1 | 1 | `skills/core/session-growth/aoa-quest-harvest/examples/runtime.md` | `docs/reviews/status-promotions/aoa-quest-harvest.md` | - | true | - |
| aoa-safe-infra-change | canonical | risk | explicit-only | 1 | 1 | 2 | 1 | 1 | `skills/risk/aoa-safe-infra-change/examples/runtime.md` | `docs/reviews/status-promotions/aoa-safe-infra-change.md` | `docs/reviews/canonical-candidates/aoa-safe-infra-change.md` | true | - |
| aoa-sanitized-share | canonical | risk | explicit-only | 1 | 1 | 3 | 1 | 1 | `skills/risk/aoa-sanitized-share/examples/runtime.md` | `docs/reviews/status-promotions/aoa-sanitized-share.md` | `docs/reviews/canonical-candidates/aoa-sanitized-share.md` | true | - |
| aoa-session-donor-harvest | evaluated | core | explicit-only | 1 | 3 | 2 | 1 | 1 | `skills/core/session-growth/aoa-session-donor-harvest/examples/runtime.md` | `docs/reviews/status-promotions/aoa-session-donor-harvest.md` | - | true | - |
| aoa-session-progression-lift | evaluated | core | explicit-only | 1 | 2 | 1 | 1 | 1 | `skills/core/session-growth/aoa-session-progression-lift/examples/runtime.md` | `docs/reviews/status-promotions/aoa-session-progression-lift.md` | - | true | - |
| aoa-session-route-forks | evaluated | core | explicit-only | 1 | 2 | 1 | 1 | 1 | `skills/core/session-growth/aoa-session-route-forks/examples/runtime.md` | `docs/reviews/status-promotions/aoa-session-route-forks.md` | - | true | - |
| aoa-session-self-diagnose | evaluated | core | explicit-only | 1 | 2 | 1 | 1 | 1 | `skills/core/session-growth/aoa-session-self-diagnose/examples/runtime.md` | `docs/reviews/status-promotions/aoa-session-self-diagnose.md` | - | true | - |
| aoa-session-self-repair | evaluated | core | explicit-only | 1 | 2 | 1 | 1 | 1 | `skills/core/session-growth/aoa-session-self-repair/examples/runtime.md` | `docs/reviews/status-promotions/aoa-session-self-repair.md` | - | true | - |
| aoa-source-of-truth-check | canonical | core | explicit-preferred | 1 | 2 | 2 | 1 | 1 | `skills/core/engineering/aoa-source-of-truth-check/examples/example.md` | `docs/reviews/status-promotions/aoa-source-of-truth-check.md` | `docs/reviews/canonical-candidates/aoa-source-of-truth-check.md` | true | - |
| aoa-summon | evaluated | core | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/core/session-growth/aoa-summon/examples/runtime.md` | `docs/reviews/status-promotions/aoa-summon.md` | - | true | - |
| aoa-tdd-slice | canonical | core | explicit-preferred | 1 | 2 | 2 | 1 | 1 | `skills/core/engineering/aoa-tdd-slice/examples/example.md` | - | `docs/reviews/canonical-candidates/aoa-tdd-slice.md` | true | - |
| atm10-change-protocol | evaluated | project | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/project/atm10/atm10-change-protocol/examples/example.md` | `docs/reviews/status-promotions/atm10-change-protocol.md` | - | true | - |
| atm10-source-of-truth-check | evaluated | project | explicit-preferred | 1 | 1 | 1 | 1 | 1 | `skills/project/atm10/atm10-source-of-truth-check/examples/example.md` | `docs/reviews/status-promotions/atm10-source-of-truth-check.md` | - | true | - |
| os-abyss-artifact-trust-loop | scaffold | project | explicit-preferred | 0 | 1 | 1 | 1 | 1 | `skills/project/abyss/os-abyss-artifact-trust-loop/examples/example.md` | - | - | true | - |
| titan-approval-ledger | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-approval-ledger/examples/runtime.md` | - | - | true | - |
| titan-approval-loom | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-approval-loom/examples/runtime.md` | - | - | true | - |
| titan-appserver-bridge | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-appserver-bridge/examples/runtime.md` | - | - | true | - |
| titan-appserver-plan | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-appserver-plan/examples/runtime.md` | - | - | true | - |
| titan-closeout | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-closeout/examples/runtime.md` | - | - | true | - |
| titan-console | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-console/examples/runtime.md` | - | - | true | - |
| titan-event-replay | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-event-replay/examples/runtime.md` | - | - | true | - |
| titan-memory-loom | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-memory-loom/examples/runtime.md` | - | - | true | - |
| titan-memory-prune | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-memory-prune/examples/runtime.md` | - | - | true | - |
| titan-mutation-gate | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-mutation-gate/examples/runtime.md` | - | - | true | - |
| titan-recall | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-recall/examples/runtime.md` | - | - | true | - |
| titan-receipt | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-receipt/examples/runtime.md` | - | - | true | - |
| titan-runtime-gate | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-runtime-gate/examples/runtime.md` | - | - | true | - |
| titan-summon | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-summon/examples/runtime.md` | - | - | true | - |
| titan-thread-turn-binding | scaffold | project | explicit-only | 1 | 1 | 1 | 1 | 1 | `skills/project/titan/titan-thread-turn-binding/examples/runtime.md` | - | - | true | - |

## Reading notes

- Runtime artifacts support inspection and object use, but do not replace `SKILL.md` as the meaning-authoritative source.
- The evaluation matrix is a separate derived evidence layer from the runtime walkthroughs and the public/governance surface.
- In this wave, `canonical` skills must pass the snapshot-backed eval floor; other `evaluated` skills may still show reportable snapshot gaps without failing status.

