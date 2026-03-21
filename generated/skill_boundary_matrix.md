# Skill boundary matrix

This derived file summarizes adjacency-focused boundary evidence for neighboring `aoa-skills`.
It is built from committed adjacency cases and snapshot-backed evidence only.

## Summary

- total skills: 14
- adjacency cases: 20
- skills with required adjacency coverage: 6
- required adjacency gaps: 0

| name | status | scope | required coverage | use cases | do_not_use cases | adjacent skills | ready | blockers |
|---|---|---|---|---:|---:|---|---|---|
| aoa-adr-write | evaluated | core | false | 1 | 0 | aoa-source-of-truth-check | true | - |
| aoa-approval-gate-check | evaluated | risk | false | 3 | 0 | aoa-dry-run-first, aoa-safe-infra-change, aoa-sanitized-share | true | - |
| aoa-bounded-context-map | canonical | core | true | 1 | 0 | aoa-contract-test | true | - |
| aoa-change-protocol | canonical | core | true | 1 | 0 | aoa-tdd-slice | true | - |
| aoa-contract-test | canonical | core | true | 1 | 0 | aoa-bounded-context-map | true | - |
| aoa-core-logic-boundary | evaluated | core | false | 1 | 0 | aoa-port-adapter-refactor | true | - |
| aoa-dry-run-first | evaluated | risk | false | 2 | 0 | aoa-approval-gate-check, aoa-sanitized-share | true | - |
| aoa-invariant-coverage-audit | canonical | core | true | 1 | 0 | aoa-property-invariants | true | - |
| aoa-port-adapter-refactor | evaluated | core | false | 1 | 0 | aoa-core-logic-boundary | true | - |
| aoa-property-invariants | canonical | core | true | 1 | 0 | aoa-invariant-coverage-audit | true | - |
| aoa-safe-infra-change | evaluated | risk | false | 2 | 0 | aoa-approval-gate-check, aoa-sanitized-share | true | - |
| aoa-sanitized-share | evaluated | risk | false | 3 | 0 | aoa-approval-gate-check, aoa-dry-run-first, aoa-safe-infra-change | true | - |
| aoa-source-of-truth-check | evaluated | core | false | 1 | 0 | aoa-adr-write | true | - |
| aoa-tdd-slice | canonical | core | true | 1 | 0 | aoa-change-protocol | true | - |

## Adjacency cases

| skill | adjacent skill | case id | expected | blockers |
|---|---|---|---|---|
| aoa-bounded-context-map | aoa-contract-test | bounded_context_map_vs_contract_test_boundary | use | - |
| aoa-change-protocol | aoa-tdd-slice | change_protocol_vs_tdd_slice_boundary | use | - |
| aoa-tdd-slice | aoa-change-protocol | tdd_slice_vs_change_protocol_boundary | use | - |
| aoa-core-logic-boundary | aoa-port-adapter-refactor | core_logic_boundary_vs_port_adapter_refactor | use | - |
| aoa-port-adapter-refactor | aoa-core-logic-boundary | port_adapter_refactor_vs_core_logic_boundary | use | - |
| aoa-approval-gate-check | aoa-dry-run-first | approval_gate_vs_preview_and_infra_boundary | use | - |
| aoa-approval-gate-check | aoa-safe-infra-change | approval_gate_vs_safe_infra_boundary | use | - |
| aoa-approval-gate-check | aoa-sanitized-share | approval_gate_vs_sanitized_share_boundary | use | - |
| aoa-contract-test | aoa-bounded-context-map | contract_test_vs_bounded_context_map_boundary | use | - |
| aoa-dry-run-first | aoa-approval-gate-check | dry_run_first_vs_approval_gate_boundary | use | - |
| aoa-dry-run-first | aoa-sanitized-share | dry_run_first_vs_sanitized_share_boundary | use | - |
| aoa-safe-infra-change | aoa-approval-gate-check | safe_infra_change_vs_approval_gate_boundary | use | - |
| aoa-safe-infra-change | aoa-sanitized-share | safe_infra_change_vs_sanitized_share_boundary | use | - |
| aoa-sanitized-share | aoa-approval-gate-check | sanitized_share_vs_approval_gate_boundary | use | - |
| aoa-sanitized-share | aoa-dry-run-first | sanitized_share_vs_dry_run_first_boundary | use | - |
| aoa-sanitized-share | aoa-safe-infra-change | sanitized_share_vs_safe_infra_change_boundary | use | - |
| aoa-source-of-truth-check | aoa-adr-write | source_of_truth_check_vs_adr_write_boundary | use | - |
| aoa-adr-write | aoa-source-of-truth-check | adr_write_vs_source_of_truth_check_boundary | use | - |
| aoa-invariant-coverage-audit | aoa-property-invariants | invariant_coverage_audit_vs_property_invariants_boundary | use | - |
| aoa-property-invariants | aoa-invariant-coverage-audit | property_invariants_vs_invariant_coverage_audit_boundary | use | - |

