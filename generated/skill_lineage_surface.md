# Skill lineage surface

This derived file summarizes manifest-only technique lineage readiness inside `aoa-skills`.
It does not fetch or compare upstream repos; it only reflects committed bundle facts.

## Summary

- total skills: 14
- published lineage: 6
- pending lineage: 8

| name | status | scope | lineage | published techniques | pending techniques | tbd refs | manifest canonical-path ready | blockers |
|---|---|---|---|---:|---:|---:|---|---|
| aoa-adr-write | evaluated | core | pending | 0 | 2 | 1 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| aoa-approval-gate-check | evaluated | risk | pending | 0 | 2 | 1 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| aoa-bounded-context-map | evaluated | core | published | 2 | 0 | 0 | true | - |
| aoa-change-protocol | canonical | core | published | 2 | 0 | 0 | true | - |
| aoa-contract-test | evaluated | core | published | 2 | 0 | 0 | true | - |
| aoa-core-logic-boundary | evaluated | core | pending | 0 | 2 | 1 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| aoa-dry-run-first | evaluated | risk | pending | 1 | 2 | 1 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| aoa-invariant-coverage-audit | evaluated | core | published | 1 | 0 | 0 | true | - |
| aoa-port-adapter-refactor | evaluated | core | pending | 0 | 2 | 1 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| aoa-property-invariants | evaluated | core | published | 2 | 0 | 0 | true | - |
| aoa-safe-infra-change | evaluated | risk | pending | 1 | 2 | 1 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| aoa-sanitized-share | evaluated | risk | pending | 0 | 2 | 1 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| aoa-source-of-truth-check | evaluated | core | pending | 1 | 2 | 1 | false | pending_technique_dependencies, pending_technique_entries, tbd_technique_refs |
| aoa-tdd-slice | canonical | core | published | 2 | 0 | 0 | true | - |

## Reading notes

- `manifest canonical-path ready` only reflects committed manifest facts, not upstream drift or human promotion judgment.
- Skills blocked here still may be `evaluated`; this layer is about lineage readiness only.

