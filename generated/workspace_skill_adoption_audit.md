# Workspace skill adoption audit: repo-project-foundation

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
| `workspace-root` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |
| `8Dionysus` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |
| `Agents-of-Abyss` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |
| `aoa-agents` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |
| `aoa-evals` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |
| `aoa-kag` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |
| `aoa-memo` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |
| `aoa-playbooks` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |
| `aoa-routing` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |
| `aoa-sdk` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |
| `aoa-skills` | `verified_with_extra_dirs` | true | 23 | 23 | 45 | 0 | 0 | 22 |
| `aoa-stats` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |
| `aoa-techniques` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |
| `ATM10-Agent` | `verified_with_extra_dirs` | true | 23 | 23 | 27 | 0 | 0 | 4 |
| `Dionysus` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |
| `Tree-of-Sophia` | `verified_with_extra_dirs` | true | 23 | 23 | 25 | 0 | 0 | 2 |

## Details

### `workspace-root`

- install root: `/srv/AbyssOS/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon

### `8Dionysus`

- install root: `/srv/AbyssOS/8Dionysus/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon

### `Agents-of-Abyss`

- install root: `/srv/AbyssOS/Agents-of-Abyss/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon

### `aoa-agents`

- install root: `/srv/AbyssOS/aoa-agents/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon

### `aoa-evals`

- install root: `/srv/AbyssOS/aoa-evals/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon

### `aoa-kag`

- install root: `/srv/AbyssOS/aoa-kag/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon

### `aoa-memo`

- install root: `/srv/AbyssOS/aoa-memo/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon

### `aoa-playbooks`

- install root: `/srv/AbyssOS/aoa-playbooks/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon

### `aoa-routing`

- install root: `/srv/AbyssOS/aoa-routing/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon

### `aoa-sdk`

- install root: `/srv/AbyssOS/aoa-sdk/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon

### `aoa-skills`

- install root: `/srv/AbyssOS/aoa-skills/.agents/skills`
- missing: -
- drift: -
- extra: abyss-safe-infra-change, abyss-sanitized-share, abyss-self-diagnostic-spine, aoa-commit-growth-seam, aoa-summon, atm10-change-protocol, atm10-source-of-truth-check, titan-approval-ledger, titan-approval-loom, titan-appserver-bridge, titan-appserver-plan, titan-closeout, titan-console, titan-event-replay, titan-memory-loom, titan-memory-prune, titan-mutation-gate, titan-recall, titan-receipt, titan-runtime-gate, titan-summon, titan-thread-turn-binding

### `aoa-stats`

- install root: `/srv/AbyssOS/aoa-stats/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon

### `aoa-techniques`

- install root: `/srv/AbyssOS/aoa-techniques/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon

### `ATM10-Agent`

- install root: `/srv/AbyssOS/ATM10-Agent/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon, atm10-change-protocol, atm10-source-of-truth-check

### `Dionysus`

- install root: `/srv/AbyssOS/Dionysus/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon

### `Tree-of-Sophia`

- install root: `/srv/AbyssOS/Tree-of-Sophia/.agents/skills`
- missing: -
- drift: -
- extra: aoa-commit-growth-seam, aoa-summon

