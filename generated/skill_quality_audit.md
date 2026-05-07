# Skill Quality Audit

This report audits authored skill bodies against evaluation fixtures,
runtime discovery, support artifacts, governance status, and technique
lineage. Generated surfaces are evidence; `skills/**/SKILL.md` and
`techniques.yaml` remain the meaning source.

- skill count: 45

## Verdicts

- `healthy`: 28
- `working_scaffold_needs_promotion_review`: 16
- `working_with_maintenance_findings`: 1

## Technique Drift

- repo: `/srv/AbyssOS/aoa-techniques`
- target ref: `ab981e7c9b4e929b6165b942bcf7a344d406030f`
- states: clean=62, pending=32

## Findings

- `pending_technique_lineage`: 16

## Upgrade Targets

| skill | status | scope | verdict | findings |
|---|---|---|---|---|
| `abyss-self-diagnostic-spine` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | - |
| `aoa-summon` | `evaluated` | `core` | `working_with_maintenance_findings` | `pending_technique_lineage` |
| `titan-approval-ledger` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |
| `titan-approval-loom` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |
| `titan-appserver-bridge` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |
| `titan-appserver-plan` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |
| `titan-closeout` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |
| `titan-console` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |
| `titan-event-replay` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |
| `titan-memory-loom` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |
| `titan-memory-prune` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |
| `titan-mutation-gate` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |
| `titan-recall` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |
| `titan-receipt` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |
| `titan-runtime-gate` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |
| `titan-summon` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |
| `titan-thread-turn-binding` | `scaffold` | `project` | `working_scaffold_needs_promotion_review` | `pending_technique_lineage` |

## Skill Matrix

| skill | status | lineage | technique drift | eval | body | runtime | verdict |
|---|---|---|---|---|---|---|---|
| `abyss-safe-infra-change` | `evaluated` | `published` | `clean2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v5/p5` | `project-overlay, runtime, implicit=false` | `healthy` |
| `abyss-sanitized-share` | `evaluated` | `published` | `clean2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v5/p5` | `project-overlay, sharing, implicit=false` | `healthy` |
| `abyss-self-diagnostic-spine` | `scaffold` | `published` | `clean2` | `a1/u1/d1/su1/sd1` | `out9/c7/r6/v7/p8` | `project-overlay, none, implicit=true` | `working_scaffold_needs_promotion_review` |
| `aoa-adr-write` | `canonical` | `published` | `clean2` | `a1/u2/d6/su1/sd1` | `out7/c9/r11/v10/p10` | `portable-core, repo, implicit=true` | `healthy` |
| `aoa-approval-gate-check` | `canonical` | `published` | `clean1` | `a1/u1/d1/su1/sd1` | `out5/c6/r6/v6/p6` | `explicit-risk, none, implicit=false` | `healthy` |
| `aoa-automation-opportunity-scan` | `evaluated` | `published` | `clean3` | `a1/u2/d1/su1/sd1` | `out7/c9/r7/v9/p10` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-bounded-context-map` | `canonical` | `published` | `clean2` | `a1/u2/d4/su1/sd1` | `out6/c6/r9/v7/p9` | `portable-core, none, implicit=true` | `healthy` |
| `aoa-change-protocol` | `canonical` | `published` | `clean2` | `a1/u1/d1/su1/sd1` | `out5/c7/r7/v6/p9` | `portable-core, repo, implicit=true` | `healthy` |
| `aoa-checkpoint-closeout-bridge` | `evaluated` | `published` | `clean3` | `a1/u1/d1/su1/sd1` | `out12/c11/r7/v8/p11` | `portable-core, none, implicit=true` | `healthy` |
| `aoa-commit-growth-seam` | `evaluated` | `published` | `clean2` | `a1/u1/d1/su1/sd1` | `out5/c5/r5/v5/p8` | `portable-core, repo, implicit=false` | `healthy` |
| `aoa-contract-test` | `canonical` | `published` | `clean2` | `a1/u3/d3/su1/sd1` | `out5/c7/r7/v6/p7` | `portable-core, repo, implicit=true` | `healthy` |
| `aoa-core-logic-boundary` | `evaluated` | `published` | `clean2` | `a1/u3/d3/su1/sd1` | `out5/c6/r7/v6/p7` | `portable-core, repo, implicit=true` | `healthy` |
| `aoa-dry-run-first` | `canonical` | `published` | `clean2` | `a1/u1/d2/su1/sd1` | `out5/c6/r6/v7/p7` | `explicit-risk, runtime, implicit=false` | `healthy` |
| `aoa-invariant-coverage-audit` | `canonical` | `published` | `clean1` | `a1/u1/d1/su1/sd1` | `out6/c7/r7/v6/p7` | `portable-core, none, implicit=true` | `healthy` |
| `aoa-local-stack-bringup` | `evaluated` | `published` | `clean4` | `a1/u1/d1/su1/sd1` | `out5/c6/r6/v6/p7` | `explicit-risk, runtime, implicit=false` | `healthy` |
| `aoa-port-adapter-refactor` | `evaluated` | `published` | `clean2` | `a1/u2/d2/su1/sd1` | `out5/c7/r7/v6/p8` | `portable-core, repo, implicit=true` | `healthy` |
| `aoa-property-invariants` | `canonical` | `published` | `clean2` | `a1/u2/d3/su1/sd1` | `out5/c6/r9/v6/p8` | `portable-core, repo, implicit=true` | `healthy` |
| `aoa-quest-harvest` | `evaluated` | `published` | `clean2` | `a1/u2/d1/su1/sd1` | `out7/c10/r6/v8/p12` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-safe-infra-change` | `canonical` | `published` | `clean2` | `a1/u1/d2/su1/sd1` | `out4/c4/r4/v5/p6` | `explicit-risk, runtime, implicit=false` | `healthy` |
| `aoa-sanitized-share` | `canonical` | `published` | `clean2` | `a1/u1/d3/su1/sd1` | `out4/c6/r17/v7/p7` | `explicit-risk, sharing, implicit=false` | `healthy` |
| `aoa-session-donor-harvest` | `evaluated` | `published` | `clean3` | `a1/u3/d2/su1/sd1` | `out17/c13/r10/v13/p25` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-session-progression-lift` | `evaluated` | `published` | `clean2` | `a1/u2/d1/su1/sd1` | `out7/c9/r7/v7/p9` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-session-route-forks` | `evaluated` | `published` | `clean2` | `a1/u2/d1/su1/sd1` | `out7/c9/r7/v7/p10` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-session-self-diagnose` | `evaluated` | `published` | `clean2` | `a1/u2/d1/su1/sd1` | `out7/c9/r7/v7/p9` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-session-self-repair` | `evaluated` | `published` | `clean2` | `a1/u2/d1/su1/sd1` | `out6/c10/r6/v7/p9` | `portable-core, none, implicit=false` | `healthy` |
| `aoa-source-of-truth-check` | `canonical` | `published` | `clean3` | `a1/u2/d2/su1/sd1` | `out7/c8/r10/v8/p10` | `portable-core, none, implicit=true` | `healthy` |
| `aoa-summon` | `evaluated` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out6/c10/r6/v10/p14` | `portable-core, none, implicit=false` | `working_with_maintenance_findings` |
| `aoa-tdd-slice` | `canonical` | `published` | `clean2` | `a1/u2/d2/su1/sd1` | `out5/c7/r6/v5/p7` | `portable-core, repo, implicit=true` | `healthy` |
| `atm10-change-protocol` | `evaluated` | `published` | `clean2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v5/p5` | `project-overlay, repo, implicit=true` | `healthy` |
| `atm10-source-of-truth-check` | `evaluated` | `published` | `clean2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v5/p5` | `project-overlay, none, implicit=true` | `healthy` |
| `titan-approval-ledger` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out4/c4/r4/v4/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-approval-loom` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out4/c4/r4/v4/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-appserver-bridge` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v4/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-appserver-plan` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v4/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-closeout` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v4/p5` | `project-overlay, none, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-console` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v4/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-event-replay` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v4/p5` | `project-overlay, none, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-memory-loom` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v4/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-memory-prune` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v4/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-mutation-gate` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v4/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-recall` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v4/p5` | `project-overlay, none, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-receipt` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v4/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-runtime-gate` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v4/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-summon` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v4/p5` | `project-overlay, none, implicit=false` | `working_scaffold_needs_promotion_review` |
| `titan-thread-turn-binding` | `scaffold` | `pending` | `pending2` | `a1/u1/d1/su1/sd1` | `out5/c4/r4/v4/p5` | `project-overlay, repo, implicit=false` | `working_scaffold_needs_promotion_review` |
