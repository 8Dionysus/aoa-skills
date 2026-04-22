# Skill lineage surface

This derived file summarizes manifest-only technique lineage readiness inside `aoa-skills`.
It does not fetch or compare upstream repos; it only reflects committed bundle facts.

## Summary

- total skills: 45
- published lineage: 29
- pending lineage: 16

| name | status | scope | lineage | published techniques | pending techniques | tbd refs | manifest canonical-path ready | blockers |
|---|---|---|---|---:|---:|---:|---|---|
| abyss-safe-infra-change | evaluated | project | published | 2 | 0 | 0 | true | - |
| abyss-sanitized-share | evaluated | project | published | 2 | 0 | 0 | true | - |
| abyss-self-diagnostic-spine | scaffold | project | published | 2 | 0 | 0 | true | - |
| aoa-adr-write | canonical | core | published | 2 | 0 | 0 | true | - |
| aoa-approval-gate-check | canonical | risk | published | 1 | 0 | 0 | true | - |
| aoa-automation-opportunity-scan | scaffold | core | published | 3 | 0 | 0 | true | - |
| aoa-bounded-context-map | canonical | core | published | 2 | 0 | 0 | true | - |
| aoa-change-protocol | canonical | core | published | 2 | 0 | 0 | true | - |
| aoa-checkpoint-closeout-bridge | scaffold | core | published | 3 | 0 | 0 | true | - |
| aoa-commit-growth-seam | scaffold | core | published | 2 | 0 | 0 | true | - |
| aoa-contract-test | canonical | core | published | 2 | 0 | 0 | true | - |
| aoa-core-logic-boundary | evaluated | core | published | 2 | 0 | 0 | true | - |
| aoa-dry-run-first | canonical | risk | published | 2 | 0 | 0 | true | - |
| aoa-invariant-coverage-audit | canonical | core | published | 1 | 0 | 0 | true | - |
| aoa-local-stack-bringup | evaluated | risk | published | 4 | 0 | 0 | true | - |
| aoa-port-adapter-refactor | evaluated | core | published | 2 | 0 | 0 | true | - |
| aoa-property-invariants | canonical | core | published | 2 | 0 | 0 | true | - |
| aoa-quest-harvest | scaffold | core | published | 2 | 0 | 0 | true | - |
| aoa-safe-infra-change | canonical | risk | published | 2 | 0 | 0 | true | - |
| aoa-sanitized-share | canonical | risk | published | 2 | 0 | 0 | true | - |
| aoa-session-donor-harvest | scaffold | core | published | 3 | 0 | 0 | true | - |
| aoa-session-progression-lift | scaffold | core | published | 2 | 0 | 0 | true | - |
| aoa-session-route-forks | scaffold | core | published | 2 | 0 | 0 | true | - |
| aoa-session-self-diagnose | scaffold | core | published | 2 | 0 | 0 | true | - |
| aoa-session-self-repair | scaffold | core | published | 2 | 0 | 0 | true | - |
| aoa-source-of-truth-check | canonical | core | published | 3 | 0 | 0 | true | - |
| aoa-summon | scaffold | core | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| aoa-tdd-slice | canonical | core | published | 2 | 0 | 0 | true | - |
| atm10-change-protocol | evaluated | project | published | 2 | 0 | 0 | true | - |
| atm10-source-of-truth-check | evaluated | project | published | 2 | 0 | 0 | true | - |
| titan-approval-ledger | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| titan-approval-loom | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| titan-appserver-bridge | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| titan-appserver-plan | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| titan-closeout | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| titan-console | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| titan-event-replay | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| titan-memory-loom | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| titan-memory-prune | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| titan-mutation-gate | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| titan-recall | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| titan-receipt | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| titan-runtime-gate | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| titan-summon | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| titan-thread-turn-binding | scaffold | project | pending | 0 | 2 | 2 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |

## Reading notes

- `manifest canonical-path ready` only reflects committed manifest facts, not upstream drift or human promotion judgment.
- Skills blocked here still may be `evaluated`; this layer is about lineage readiness only.

