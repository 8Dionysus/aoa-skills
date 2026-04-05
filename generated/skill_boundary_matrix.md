# Skill boundary matrix

This derived file summarizes adjacency-focused boundary evidence for neighboring `aoa-skills`.
It is built from committed adjacency cases and snapshot-backed evidence only.

## Summary

- total skills: 21
- adjacency cases: 32
- skills with required adjacency coverage: 15
- required adjacency gaps: 0

| name | status | scope | required coverage | use cases | do_not_use cases | adjacent skills | lane ids | ready | blockers |
|---|---|---|---|---:|---:|---|---|---|---|
| abyss-safe-infra-change | evaluated | project | false | 1 | 0 | abyss-sanitized-share | - | true | - |
| abyss-sanitized-share | evaluated | project | false | 1 | 0 | abyss-safe-infra-change | - | true | - |
| aoa-adr-write | canonical | core | true | 1 | 0 | aoa-source-of-truth-check | decision_docs_authority | true | - |
| aoa-approval-gate-check | canonical | risk | true | 3 | 0 | aoa-dry-run-first, aoa-safe-infra-change, aoa-sanitized-share | local_runtime_bringup, risk_authority_preview_execution | true | - |
| aoa-bounded-context-map | canonical | core | true | 3 | 0 | aoa-contract-test, aoa-core-logic-boundary, aoa-port-adapter-refactor | context_vs_contract, core_boundary_refactor | true | - |
| aoa-change-protocol | canonical | core | true | 1 | 0 | aoa-tdd-slice | change_workflows | true | - |
| aoa-contract-test | canonical | core | true | 1 | 0 | aoa-bounded-context-map | context_vs_contract | true | - |
| aoa-core-logic-boundary | evaluated | core | true | 2 | 0 | aoa-bounded-context-map, aoa-port-adapter-refactor | core_boundary_refactor | true | - |
| aoa-dry-run-first | canonical | risk | true | 3 | 0 | aoa-approval-gate-check, aoa-safe-infra-change, aoa-sanitized-share | risk_authority_preview_execution | true | - |
| aoa-invariant-coverage-audit | canonical | core | true | 1 | 0 | aoa-property-invariants | invariant_authoring_vs_audit | true | - |
| aoa-local-stack-bringup | evaluated | risk | true | 2 | 0 | aoa-approval-gate-check, aoa-safe-infra-change | local_runtime_bringup | true | - |
| aoa-port-adapter-refactor | evaluated | core | true | 2 | 0 | aoa-bounded-context-map, aoa-core-logic-boundary | core_boundary_refactor | true | - |
| aoa-property-invariants | canonical | core | true | 1 | 0 | aoa-invariant-coverage-audit | invariant_authoring_vs_audit | true | - |
| aoa-quest-harvest | scaffold | core | false | 0 | 0 | - | - | false | - |
| aoa-safe-infra-change | canonical | risk | true | 3 | 0 | aoa-approval-gate-check, aoa-dry-run-first, aoa-sanitized-share | local_runtime_bringup, risk_authority_preview_execution | true | - |
| aoa-sanitized-share | canonical | risk | true | 3 | 0 | aoa-approval-gate-check, aoa-dry-run-first, aoa-safe-infra-change | risk_authority_preview_execution | true | - |
| aoa-session-donor-harvest | scaffold | core | false | 0 | 0 | - | - | false | - |
| aoa-source-of-truth-check | canonical | core | true | 1 | 0 | aoa-adr-write | decision_docs_authority | true | - |
| aoa-tdd-slice | canonical | core | true | 1 | 0 | aoa-change-protocol | change_workflows | true | - |
| atm10-change-protocol | evaluated | project | false | 1 | 0 | atm10-source-of-truth-check | - | true | - |
| atm10-source-of-truth-check | evaluated | project | false | 1 | 0 | atm10-change-protocol | - | true | - |

## Adjacency cases

| skill | adjacent skill | case id | expected | lane ids | blockers |
|---|---|---|---|---|---|
| aoa-bounded-context-map | aoa-contract-test | bounded_context_map_vs_contract_test_boundary | use | context_vs_contract | - |
| aoa-change-protocol | aoa-tdd-slice | change_protocol_vs_tdd_slice_boundary | use | change_workflows | - |
| aoa-tdd-slice | aoa-change-protocol | tdd_slice_vs_change_protocol_boundary | use | change_workflows | - |
| aoa-bounded-context-map | aoa-core-logic-boundary | bounded_context_map_vs_core_logic_boundary | use | core_boundary_refactor | - |
| aoa-bounded-context-map | aoa-port-adapter-refactor | bounded_context_map_vs_port_adapter_refactor | use | core_boundary_refactor | - |
| aoa-core-logic-boundary | aoa-bounded-context-map | core_logic_boundary_vs_bounded_context_map_boundary | use | core_boundary_refactor | - |
| aoa-core-logic-boundary | aoa-port-adapter-refactor | core_logic_boundary_vs_port_adapter_refactor | use | core_boundary_refactor | - |
| aoa-port-adapter-refactor | aoa-bounded-context-map | port_adapter_refactor_vs_bounded_context_map_boundary | use | core_boundary_refactor | - |
| aoa-port-adapter-refactor | aoa-core-logic-boundary | port_adapter_refactor_vs_core_logic_boundary | use | core_boundary_refactor | - |
| aoa-approval-gate-check | aoa-dry-run-first | approval_gate_vs_preview_and_infra_boundary | use | risk_authority_preview_execution | - |
| aoa-approval-gate-check | aoa-safe-infra-change | approval_gate_vs_safe_infra_boundary | use | risk_authority_preview_execution | - |
| aoa-approval-gate-check | aoa-sanitized-share | approval_gate_vs_sanitized_share_boundary | use | risk_authority_preview_execution | - |
| aoa-contract-test | aoa-bounded-context-map | contract_test_vs_bounded_context_map_boundary | use | context_vs_contract | - |
| aoa-dry-run-first | aoa-approval-gate-check | dry_run_first_vs_approval_gate_boundary | use | risk_authority_preview_execution | - |
| aoa-dry-run-first | aoa-sanitized-share | dry_run_first_vs_sanitized_share_boundary | use | risk_authority_preview_execution | - |
| aoa-dry-run-first | aoa-safe-infra-change | dry_run_first_vs_safe_infra_boundary | use | risk_authority_preview_execution | - |
| aoa-safe-infra-change | aoa-approval-gate-check | safe_infra_change_vs_approval_gate_boundary | use | risk_authority_preview_execution | - |
| aoa-safe-infra-change | aoa-sanitized-share | safe_infra_change_vs_sanitized_share_boundary | use | risk_authority_preview_execution | - |
| aoa-safe-infra-change | aoa-dry-run-first | safe_infra_change_vs_dry_run_first_boundary | use | risk_authority_preview_execution | - |
| aoa-local-stack-bringup | aoa-approval-gate-check | local_stack_bringup_vs_approval_gate_boundary | use | local_runtime_bringup | - |
| aoa-local-stack-bringup | aoa-safe-infra-change | local_stack_bringup_vs_safe_infra_change_boundary | use | local_runtime_bringup | - |
| aoa-sanitized-share | aoa-approval-gate-check | sanitized_share_vs_approval_gate_boundary | use | risk_authority_preview_execution | - |
| aoa-sanitized-share | aoa-dry-run-first | sanitized_share_vs_dry_run_first_boundary | use | risk_authority_preview_execution | - |
| aoa-sanitized-share | aoa-safe-infra-change | sanitized_share_vs_safe_infra_change_boundary | use | risk_authority_preview_execution | - |
| aoa-source-of-truth-check | aoa-adr-write | source_of_truth_check_vs_adr_write_boundary | use | decision_docs_authority | - |
| aoa-adr-write | aoa-source-of-truth-check | adr_write_vs_source_of_truth_check_boundary | use | decision_docs_authority | - |
| aoa-invariant-coverage-audit | aoa-property-invariants | invariant_coverage_audit_vs_property_invariants_boundary | use | invariant_authoring_vs_audit | - |
| aoa-property-invariants | aoa-invariant-coverage-audit | property_invariants_vs_invariant_coverage_audit_boundary | use | invariant_authoring_vs_audit | - |
| atm10-change-protocol | atm10-source-of-truth-check | atm10_change_protocol_vs_source_of_truth_boundary | use | - | - |
| atm10-source-of-truth-check | atm10-change-protocol | atm10_source_of_truth_vs_change_protocol_boundary | use | - | - |
| abyss-safe-infra-change | abyss-sanitized-share | abyss_safe_infra_change_vs_sanitized_share_boundary | use | - | - |
| abyss-sanitized-share | abyss-safe-infra-change | abyss_sanitized_share_vs_safe_infra_change_boundary | use | - | - |

