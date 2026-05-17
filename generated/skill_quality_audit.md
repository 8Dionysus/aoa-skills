# Skill Quality Audit

This report audits authored skill bodies against evaluation fixtures,
runtime discovery, support artifacts, governance status, and technique
lineage. Generated surfaces are evidence; `skills/**/SKILL.md` and
`techniques.yaml` remain the meaning source.

- skill count: 45

## Verdicts

- `healthy`: 29
- `working_scaffold_needs_promotion_review`: 16

## Technique Drift

- repo: `/srv/AbyssOS/aoa-techniques`
- target ref: `3b1d5d623569aa4920b87280d0db0e911d2e29d5`
- states: clean=112

## Findings

- no findings

## Upgrade Targets

| skill | status | scope | verdict | findings |
|---|---|---|---|---|
| `abyss-self-diagnostic-spine` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-approval-ledger` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-approval-loom` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-appserver-bridge` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-appserver-plan` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-closeout` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-console` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-event-replay` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-memory-loom` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-memory-prune` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-mutation-gate` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-recall` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-receipt` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-runtime-gate` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-summon` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `titan-thread-turn-binding` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |

## Skill Matrix

| skill | status | lineage | technique drift | eval | body | runtime | verdict |
|---|---|---|---|---|---|---|---|
| `abyss-safe-infra-change` | `evaluated` | `published` | `clean2` | `a1/u1/d1/su1/sd1` | `out7/c6/r7/v7/p8` | `project-overlay, runtime, implicit=false` | `healthy` |
| `abyss-sanitized-share` | `evaluated` | `published` | `clean2` | `a1/u1/d1/su1/sd1` | `out7/c7/r7/v8/p7` | `project-overlay, sharing, implicit=false` | `healthy` |
| `abyss-self-diagnostic-spine` | `scaffold` | `published` | `clean2` | `a1/u1/d1/su1/sd1` | `out11/c10/r9/v9/p10` | `project-overlay, none, implicit=false` | `working_scaffold_needs_promotion_review` |
| `aoa-adr-write` | `canonical` | `published` | `clean2` | `a1/u2/d6/su1/sd1` | `out7/c9/r11/v10/p10` | `portable-core, repo, implicit=true` | `healthy` |
| `aoa-approval-gate-check` | `canonical` | `published` | `clean1` | `a1/u1/d1/su1/sd1` | `out5/c6/r6/v6/p6` | `explicit-risk, none, implicit=false` | `healthy` |
| `aoa-automation-opportunity-scan` | `evaluated` | `published` | `clean3` | `a1/u2/d1/su1/sd1` | `out8/c10/r8/v10/p11` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-bounded-context-map` | `canonical` | `published` | `clean2` | `a1/u2/d4/su1/sd1` | `out6/c6/r9/v7/p9` | `portable-core, none, implicit=true` | `healthy` |
| `aoa-change-protocol` | `canonical` | `published` | `clean2` | `a1/u1/d1/su1/sd1` | `out5/c7/r7/v6/p9` | `portable-core, repo, implicit=true` | `healthy` |
| `aoa-checkpoint-closeout-bridge` | `evaluated` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out14/c12/r8/v9/p13` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-commit-growth-seam` | `evaluated` | `published` | `clean2` | `a1/u1/d1/su1/sd1` | `out6/c6/r6/v6/p9` | `portable-core, repo, implicit=false` | `healthy` |
| `aoa-contract-test` | `canonical` | `published` | `clean2` | `a1/u3/d3/su1/sd1` | `out5/c7/r7/v6/p7` | `portable-core, repo, implicit=true` | `healthy` |
| `aoa-core-logic-boundary` | `evaluated` | `published` | `clean2` | `a1/u3/d3/su1/sd1` | `out5/c6/r7/v6/p7` | `portable-core, repo, implicit=true` | `healthy` |
| `aoa-dry-run-first` | `canonical` | `published` | `clean2` | `a1/u1/d2/su1/sd1` | `out5/c6/r6/v7/p7` | `explicit-risk, runtime, implicit=false` | `healthy` |
| `aoa-invariant-coverage-audit` | `canonical` | `published` | `clean1` | `a1/u1/d1/su1/sd1` | `out6/c7/r7/v6/p7` | `portable-core, none, implicit=true` | `healthy` |
| `aoa-local-stack-bringup` | `evaluated` | `published` | `clean4` | `a1/u1/d1/su1/sd1` | `out5/c6/r6/v6/p7` | `explicit-risk, runtime, implicit=false` | `healthy` |
| `aoa-port-adapter-refactor` | `evaluated` | `published` | `clean2` | `a1/u2/d2/su1/sd1` | `out5/c7/r7/v6/p8` | `portable-core, repo, implicit=true` | `healthy` |
| `aoa-property-invariants` | `canonical` | `published` | `clean2` | `a1/u2/d3/su1/sd1` | `out5/c6/r9/v6/p8` | `portable-core, repo, implicit=true` | `healthy` |
| `aoa-quest-harvest` | `evaluated` | `published` | `clean2` | `a1/u2/d1/su1/sd1` | `out9/c13/r9/v11/p15` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-safe-infra-change` | `canonical` | `published` | `clean2` | `a1/u1/d2/su1/sd1` | `out4/c4/r4/v5/p6` | `explicit-risk, runtime, implicit=false` | `healthy` |
| `aoa-sanitized-share` | `canonical` | `published` | `clean2` | `a1/u1/d3/su1/sd1` | `out4/c6/r17/v7/p7` | `explicit-risk, sharing, implicit=false` | `healthy` |
| `aoa-session-donor-harvest` | `evaluated` | `published` | `clean3` | `a1/u3/d2/su1/sd1` | `out18/c14/r12/v15/p27` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-session-progression-lift` | `evaluated` | `published` | `clean2` | `a1/u2/d1/su1/sd1` | `out9/c11/r10/v9/p15` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-session-route-forks` | `evaluated` | `published` | `clean2` | `a1/u2/d1/su1/sd1` | `out7/c10/r7/v8/p11` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-session-self-diagnose` | `evaluated` | `published` | `clean2` | `a1/u2/d1/su1/sd1` | `out8/c10/r9/v8/p10` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-session-self-repair` | `evaluated` | `published` | `clean2` | `a1/u2/d1/su1/sd1` | `out7/c11/r7/v8/p11` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-source-of-truth-check` | `canonical` | `published` | `clean3` | `a1/u2/d2/su1/sd1` | `out7/c8/r10/v8/p10` | `portable-core, none, implicit=true` | `healthy` |
| `aoa-summon` | `evaluated` | `published` | `clean4` | `a1/u1/d1/su1/sd1` | `out7/c12/r7/v12/p15` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-tdd-slice` | `canonical` | `published` | `clean2` | `a1/u2/d2/su1/sd1` | `out5/c7/r6/v5/p7` | `portable-core, repo, implicit=true` | `healthy` |
| `atm10-change-protocol` | `evaluated` | `published` | `clean2` | `a1/u1/d1/su1/sd1` | `out8/c8/r8/v9/p10` | `project-overlay, repo, implicit=false` | `healthy` |
| `atm10-source-of-truth-check` | `evaluated` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out7/c9/r9/v9/p9` | `project-overlay, none, implicit=false` | `healthy` |
| `titan-approval-ledger` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out4/c5/r5/v5/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-approval-loom` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out4/c5/r5/v5/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-appserver-bridge` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out5/c5/r5/v5/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-appserver-plan` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out5/c5/r5/v5/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-closeout` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out5/c5/r5/v5/p5` | `project-overlay, none, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-console` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out5/c5/r5/v5/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-event-replay` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out5/c5/r5/v5/p5` | `project-overlay, none, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-memory-loom` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out5/c5/r5/v5/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-memory-prune` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out5/c5/r5/v5/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-mutation-gate` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out5/c5/r5/v5/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-recall` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out5/c5/r5/v5/p5` | `project-overlay, none, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-receipt` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out5/c5/r5/v5/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-runtime-gate` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out5/c5/r5/v5/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-summon` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out5/c5/r5/v5/p6` | `project-overlay, none, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-thread-turn-binding` | `scaffold` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out5/c5/r5/v5/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
