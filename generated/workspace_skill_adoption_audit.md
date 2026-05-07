# Workspace skill adoption audit: repo-project-foundation

This read-only report verifies real workspace install roots against the
current `aoa-skills` portable export. It does not install, approve, or
accept skills for any downstream owner.

- workspace root: `/srv/AbyssOS`
- source repo root: `/srv/AbyssOS/aoa-skills`
- strict root: `false`
- target count: 16

## Summary

- `verified`: 14
- `verified_with_extra_dirs`: 2

## Targets

| target | state | verified | expected | ok | installed | missing | drift | extra |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `workspace-root` | `verified` | true | 23 | 23 | 23 | 0 | 0 | 0 |
| `8Dionysus` | `verified` | true | 23 | 23 | 23 | 0 | 0 | 0 |
| `Agents-of-Abyss` | `verified` | true | 23 | 23 | 23 | 0 | 0 | 0 |
| `aoa-agents` | `verified` | true | 23 | 23 | 23 | 0 | 0 | 0 |
| `aoa-evals` | `verified` | true | 23 | 23 | 23 | 0 | 0 | 0 |
| `aoa-kag` | `verified` | true | 23 | 23 | 23 | 0 | 0 | 0 |
| `aoa-memo` | `verified` | true | 23 | 23 | 23 | 0 | 0 | 0 |
| `aoa-playbooks` | `verified` | true | 23 | 23 | 23 | 0 | 0 | 0 |
| `aoa-routing` | `verified` | true | 23 | 23 | 23 | 0 | 0 | 0 |
| `aoa-sdk` | `verified` | true | 23 | 23 | 23 | 0 | 0 | 0 |
| `aoa-skills` | `verified_with_extra_dirs` | true | 23 | 23 | 45 | 0 | 0 | 22 |
| `aoa-stats` | `verified` | true | 23 | 23 | 23 | 0 | 0 | 0 |
| `aoa-techniques` | `verified` | true | 23 | 23 | 23 | 0 | 0 | 0 |
| `ATM10-Agent` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |
| `Dionysus` | `verified` | true | 23 | 23 | 23 | 0 | 0 | 0 |
| `Tree-of-Sophia` | `verified` | true | 23 | 23 | 23 | 0 | 0 | 0 |

## Details

### `aoa-skills`

- install root: `/srv/AbyssOS/aoa-skills/.agents/skills`
- missing: -
- drift: -
- extra: abyss-safe-infra-change, abyss-sanitized-share, abyss-self-diagnostic-spine, aoa-commit-growth-seam, aoa-summon, atm10-change-protocol, atm10-source-of-truth-check, titan-approval-ledger, titan-approval-loom, titan-appserver-bridge, titan-appserver-plan, titan-closeout, titan-console, titan-event-replay, titan-memory-loom, titan-memory-prune, titan-mutation-gate, titan-recall, titan-receipt, titan-runtime-gate, titan-summon, titan-thread-turn-binding

### `ATM10-Agent`

- install root: `/srv/AbyssOS/ATM10-Agent/.agents/skills`
- missing: -
- drift: -
- extra: atm10-change-protocol, atm10-source-of-truth-check

