# Workspace skill adoption audit: repo-session-growth

This read-only report verifies real workspace install roots against the
current `aoa-skills` portable export. It does not install, approve, or
accept skills for any downstream owner.

- workspace root: `/srv/AbyssOS`
- source repo root: `/srv/AbyssOS/aoa-skills`
- strict root: `false`
- target count: 16

## Summary

- `verified_with_extra_dirs`: 16

## Targets

| target | state | verified | expected | ok | installed | missing | drift | extra |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `workspace-root` | `verified_with_extra_dirs` | true | 10 | 10 | 25 | 0 | 0 | 15 |
| `8Dionysus` | `verified_with_extra_dirs` | true | 10 | 10 | 25 | 0 | 0 | 15 |
| `Agents-of-Abyss` | `verified_with_extra_dirs` | true | 10 | 10 | 25 | 0 | 0 | 15 |
| `aoa-agents` | `verified_with_extra_dirs` | true | 10 | 10 | 25 | 0 | 0 | 15 |
| `aoa-evals` | `verified_with_extra_dirs` | true | 10 | 10 | 25 | 0 | 0 | 15 |
| `aoa-kag` | `verified_with_extra_dirs` | true | 10 | 10 | 25 | 0 | 0 | 15 |
| `aoa-memo` | `verified_with_extra_dirs` | true | 10 | 10 | 25 | 0 | 0 | 15 |
| `aoa-playbooks` | `verified_with_extra_dirs` | true | 10 | 10 | 25 | 0 | 0 | 15 |
| `aoa-routing` | `verified_with_extra_dirs` | true | 10 | 10 | 25 | 0 | 0 | 15 |
| `aoa-sdk` | `verified_with_extra_dirs` | true | 10 | 10 | 25 | 0 | 0 | 15 |
| `aoa-skills` | `verified_with_extra_dirs` | true | 10 | 10 | 45 | 0 | 0 | 35 |
| `aoa-stats` | `verified_with_extra_dirs` | true | 10 | 10 | 25 | 0 | 0 | 15 |
| `aoa-techniques` | `verified_with_extra_dirs` | true | 10 | 10 | 25 | 0 | 0 | 15 |
| `ATM10-Agent` | `verified_with_extra_dirs` | true | 10 | 10 | 27 | 0 | 0 | 17 |
| `Dionysus` | `verified_with_extra_dirs` | true | 10 | 10 | 25 | 0 | 0 | 15 |
| `Tree-of-Sophia` | `verified_with_extra_dirs` | true | 10 | 10 | 25 | 0 | 0 | 15 |

## Details

### `workspace-root`

- install root: `/srv/AbyssOS/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice

### `8Dionysus`

- install root: `/srv/AbyssOS/8Dionysus/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice

### `Agents-of-Abyss`

- install root: `/srv/AbyssOS/Agents-of-Abyss/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice

### `aoa-agents`

- install root: `/srv/AbyssOS/aoa-agents/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice

### `aoa-evals`

- install root: `/srv/AbyssOS/aoa-evals/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice

### `aoa-kag`

- install root: `/srv/AbyssOS/aoa-kag/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice

### `aoa-memo`

- install root: `/srv/AbyssOS/aoa-memo/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice

### `aoa-playbooks`

- install root: `/srv/AbyssOS/aoa-playbooks/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice

### `aoa-routing`

- install root: `/srv/AbyssOS/aoa-routing/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice

### `aoa-sdk`

- install root: `/srv/AbyssOS/aoa-sdk/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice

### `aoa-skills`

- install root: `/srv/AbyssOS/aoa-skills/.agents/skills`
- missing: -
- drift: -
- extra: abyss-safe-infra-change, abyss-sanitized-share, abyss-self-diagnostic-spine, aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice, atm10-change-protocol, atm10-source-of-truth-check, titan-approval-ledger, titan-approval-loom, titan-appserver-bridge, titan-appserver-plan, titan-closeout, titan-console, titan-event-replay, titan-memory-loom, titan-memory-prune, titan-mutation-gate, titan-recall, titan-receipt, titan-runtime-gate, titan-summon, titan-thread-turn-binding

### `aoa-stats`

- install root: `/srv/AbyssOS/aoa-stats/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice

### `aoa-techniques`

- install root: `/srv/AbyssOS/aoa-techniques/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice

### `ATM10-Agent`

- install root: `/srv/AbyssOS/ATM10-Agent/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice, atm10-change-protocol, atm10-source-of-truth-check

### `Dionysus`

- install root: `/srv/AbyssOS/Dionysus/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice

### `Tree-of-Sophia`

- install root: `/srv/AbyssOS/Tree-of-Sophia/.agents/skills`
- missing: -
- drift: -
- extra: aoa-adr-write, aoa-approval-gate-check, aoa-bounded-context-map, aoa-change-protocol, aoa-contract-test, aoa-core-logic-boundary, aoa-dry-run-first, aoa-invariant-coverage-audit, aoa-local-stack-bringup, aoa-port-adapter-refactor, aoa-property-invariants, aoa-safe-infra-change, aoa-sanitized-share, aoa-source-of-truth-check, aoa-tdd-slice

