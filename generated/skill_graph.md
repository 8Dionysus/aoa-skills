# Skill graph

This derived file summarizes maturity, lineage, scope, invocation, and technique edges for the current skill surface.

```mermaid
graph TD
  skill_aoa_adr_write["aoa-adr-write"]
  status_canonical["status: canonical"]
  scope_core["scope: core"]
  lineage_published["lineage: published"]
  policy_explicit_preferred["invocation: explicit-preferred"]
  technique_AOA_T_0033["AOA-T-0033"]
  technique_AOA_T_0002["AOA-T-0002"]
  skill_aoa_approval_gate_check["aoa-approval-gate-check"]
  scope_risk["scope: risk"]
  policy_explicit_only["invocation: explicit-only"]
  technique_AOA_T_0028["AOA-T-0028"]
  skill_aoa_bounded_context_map["aoa-bounded-context-map"]
  technique_AOA_T_0016["AOA-T-0016"]
  skill_aoa_change_protocol["aoa-change-protocol"]
  technique_AOA_T_0001["AOA-T-0001"]
  skill_aoa_contract_test["aoa-contract-test"]
  technique_AOA_T_0003["AOA-T-0003"]
  technique_AOA_T_0015["AOA-T-0015"]
  skill_aoa_core_logic_boundary["aoa-core-logic-boundary"]
  status_evaluated["status: evaluated"]
  skill_aoa_dry_run_first["aoa-dry-run-first"]
  technique_AOA_T_0004["AOA-T-0004"]
  skill_aoa_invariant_coverage_audit["aoa-invariant-coverage-audit"]
  technique_AOA_T_0017["AOA-T-0017"]
  skill_aoa_local_stack_bringup["aoa-local-stack-bringup"]
  technique_AOA_T_0036["AOA-T-0036"]
  technique_AOA_T_0037["AOA-T-0037"]
  technique_AOA_T_0038["AOA-T-0038"]
  skill_aoa_port_adapter_refactor["aoa-port-adapter-refactor"]
  skill_aoa_property_invariants["aoa-property-invariants"]
  technique_AOA_T_0007["AOA-T-0007"]
  skill_aoa_safe_infra_change["aoa-safe-infra-change"]
  skill_aoa_sanitized_share["aoa-sanitized-share"]
  technique_AOA_T_0034["AOA-T-0034"]
  skill_aoa_source_of_truth_check["aoa-source-of-truth-check"]
  technique_AOA_T_0013["AOA-T-0013"]
  technique_AOA_T_0009["AOA-T-0009"]
  skill_aoa_tdd_slice["aoa-tdd-slice"]
  technique_AOA_T_0014["AOA-T-0014"]
  skill_atm10_change_protocol["atm10-change-protocol"]
  status_reviewed["status: reviewed"]
  scope_project["scope: project"]
  skill_atm10_source_of_truth_check["atm10-source-of-truth-check"]
  skill_aoa_adr_write -->|maturity| status_canonical
  skill_aoa_adr_write -->|scope| scope_core
  skill_aoa_adr_write -->|lineage| lineage_published
  skill_aoa_adr_write -->|invocation_policy| policy_explicit_preferred
  skill_aoa_adr_write -->|depends_on| technique_AOA_T_0033
  skill_aoa_adr_write -->|depends_on| technique_AOA_T_0002
  skill_aoa_approval_gate_check -->|maturity| status_canonical
  skill_aoa_approval_gate_check -->|scope| scope_risk
  skill_aoa_approval_gate_check -->|lineage| lineage_published
  skill_aoa_approval_gate_check -->|invocation_policy| policy_explicit_only
  skill_aoa_approval_gate_check -->|depends_on| technique_AOA_T_0028
  skill_aoa_bounded_context_map -->|maturity| status_canonical
  skill_aoa_bounded_context_map -->|scope| scope_core
  skill_aoa_bounded_context_map -->|lineage| lineage_published
  skill_aoa_bounded_context_map -->|invocation_policy| policy_explicit_preferred
  skill_aoa_bounded_context_map -->|depends_on| technique_AOA_T_0016
  skill_aoa_bounded_context_map -->|depends_on| technique_AOA_T_0002
  skill_aoa_change_protocol -->|maturity| status_canonical
  skill_aoa_change_protocol -->|scope| scope_core
  skill_aoa_change_protocol -->|lineage| lineage_published
  skill_aoa_change_protocol -->|invocation_policy| policy_explicit_preferred
  skill_aoa_change_protocol -->|depends_on| technique_AOA_T_0001
  skill_aoa_change_protocol -->|depends_on| technique_AOA_T_0002
  skill_aoa_contract_test -->|maturity| status_canonical
  skill_aoa_contract_test -->|scope| scope_core
  skill_aoa_contract_test -->|lineage| lineage_published
  skill_aoa_contract_test -->|invocation_policy| policy_explicit_preferred
  skill_aoa_contract_test -->|depends_on| technique_AOA_T_0003
  skill_aoa_contract_test -->|depends_on| technique_AOA_T_0015
  skill_aoa_core_logic_boundary -->|maturity| status_evaluated
  skill_aoa_core_logic_boundary -->|scope| scope_core
  skill_aoa_core_logic_boundary -->|lineage| lineage_published
  skill_aoa_core_logic_boundary -->|invocation_policy| policy_explicit_preferred
  skill_aoa_core_logic_boundary -->|depends_on| technique_AOA_T_0016
  skill_aoa_core_logic_boundary -->|depends_on| technique_AOA_T_0015
  skill_aoa_dry_run_first -->|maturity| status_canonical
  skill_aoa_dry_run_first -->|scope| scope_risk
  skill_aoa_dry_run_first -->|lineage| lineage_published
  skill_aoa_dry_run_first -->|invocation_policy| policy_explicit_only
  skill_aoa_dry_run_first -->|depends_on| technique_AOA_T_0004
  skill_aoa_dry_run_first -->|depends_on| technique_AOA_T_0028
  skill_aoa_invariant_coverage_audit -->|maturity| status_canonical
  skill_aoa_invariant_coverage_audit -->|scope| scope_core
  skill_aoa_invariant_coverage_audit -->|lineage| lineage_published
  skill_aoa_invariant_coverage_audit -->|invocation_policy| policy_explicit_preferred
  skill_aoa_invariant_coverage_audit -->|depends_on| technique_AOA_T_0017
  skill_aoa_local_stack_bringup -->|maturity| status_evaluated
  skill_aoa_local_stack_bringup -->|scope| scope_risk
  skill_aoa_local_stack_bringup -->|lineage| lineage_published
  skill_aoa_local_stack_bringup -->|invocation_policy| policy_explicit_only
  skill_aoa_local_stack_bringup -->|depends_on| technique_AOA_T_0036
  skill_aoa_local_stack_bringup -->|depends_on| technique_AOA_T_0037
  skill_aoa_local_stack_bringup -->|depends_on| technique_AOA_T_0028
  skill_aoa_local_stack_bringup -->|depends_on| technique_AOA_T_0038
  skill_aoa_port_adapter_refactor -->|maturity| status_evaluated
  skill_aoa_port_adapter_refactor -->|scope| scope_core
  skill_aoa_port_adapter_refactor -->|lineage| lineage_published
  skill_aoa_port_adapter_refactor -->|invocation_policy| policy_explicit_preferred
  skill_aoa_port_adapter_refactor -->|depends_on| technique_AOA_T_0016
  skill_aoa_port_adapter_refactor -->|depends_on| technique_AOA_T_0015
  skill_aoa_property_invariants -->|maturity| status_canonical
  skill_aoa_property_invariants -->|scope| scope_core
  skill_aoa_property_invariants -->|lineage| lineage_published
  skill_aoa_property_invariants -->|invocation_policy| policy_explicit_preferred
  skill_aoa_property_invariants -->|depends_on| technique_AOA_T_0017
  skill_aoa_property_invariants -->|depends_on| technique_AOA_T_0007
  skill_aoa_safe_infra_change -->|maturity| status_canonical
  skill_aoa_safe_infra_change -->|scope| scope_risk
  skill_aoa_safe_infra_change -->|lineage| lineage_published
  skill_aoa_safe_infra_change -->|invocation_policy| policy_explicit_only
  skill_aoa_safe_infra_change -->|depends_on| technique_AOA_T_0028
  skill_aoa_safe_infra_change -->|depends_on| technique_AOA_T_0001
  skill_aoa_sanitized_share -->|maturity| status_canonical
  skill_aoa_sanitized_share -->|scope| scope_risk
  skill_aoa_sanitized_share -->|lineage| lineage_published
  skill_aoa_sanitized_share -->|invocation_policy| policy_explicit_only
  skill_aoa_sanitized_share -->|depends_on| technique_AOA_T_0034
  skill_aoa_sanitized_share -->|depends_on| technique_AOA_T_0002
  skill_aoa_source_of_truth_check -->|maturity| status_canonical
  skill_aoa_source_of_truth_check -->|scope| scope_core
  skill_aoa_source_of_truth_check -->|lineage| lineage_published
  skill_aoa_source_of_truth_check -->|invocation_policy| policy_explicit_preferred
  skill_aoa_source_of_truth_check -->|depends_on| technique_AOA_T_0013
  skill_aoa_source_of_truth_check -->|depends_on| technique_AOA_T_0002
  skill_aoa_source_of_truth_check -->|depends_on| technique_AOA_T_0009
  skill_aoa_tdd_slice -->|maturity| status_canonical
  skill_aoa_tdd_slice -->|scope| scope_core
  skill_aoa_tdd_slice -->|lineage| lineage_published
  skill_aoa_tdd_slice -->|invocation_policy| policy_explicit_preferred
  skill_aoa_tdd_slice -->|depends_on| technique_AOA_T_0014
  skill_aoa_tdd_slice -->|depends_on| technique_AOA_T_0001
  skill_atm10_change_protocol -->|maturity| status_reviewed
  skill_atm10_change_protocol -->|scope| scope_project
  skill_atm10_change_protocol -->|lineage| lineage_published
  skill_atm10_change_protocol -->|invocation_policy| policy_explicit_preferred
  skill_atm10_change_protocol -->|depends_on| technique_AOA_T_0001
  skill_atm10_change_protocol -->|depends_on| technique_AOA_T_0002
  skill_atm10_source_of_truth_check -->|maturity| status_reviewed
  skill_atm10_source_of_truth_check -->|scope| scope_project
  skill_atm10_source_of_truth_check -->|lineage| lineage_published
  skill_atm10_source_of_truth_check -->|invocation_policy| policy_explicit_preferred
  skill_atm10_source_of_truth_check -->|depends_on| technique_AOA_T_0013
  skill_atm10_source_of_truth_check -->|depends_on| technique_AOA_T_0002
```

| name | status | scope | invocation | lineage | techniques |
|---|---|---|---|---|---|
| aoa-adr-write | canonical | core | explicit-preferred | published | AOA-T-0033, AOA-T-0002 |
| aoa-approval-gate-check | canonical | risk | explicit-only | published | AOA-T-0028 |
| aoa-bounded-context-map | canonical | core | explicit-preferred | published | AOA-T-0016, AOA-T-0002 |
| aoa-change-protocol | canonical | core | explicit-preferred | published | AOA-T-0001, AOA-T-0002 |
| aoa-contract-test | canonical | core | explicit-preferred | published | AOA-T-0003, AOA-T-0015 |
| aoa-core-logic-boundary | evaluated | core | explicit-preferred | published | AOA-T-0016, AOA-T-0015 |
| aoa-dry-run-first | canonical | risk | explicit-only | published | AOA-T-0004, AOA-T-0028 |
| aoa-invariant-coverage-audit | canonical | core | explicit-preferred | published | AOA-T-0017 |
| aoa-local-stack-bringup | evaluated | risk | explicit-only | published | AOA-T-0036, AOA-T-0037, AOA-T-0028, AOA-T-0038 |
| aoa-port-adapter-refactor | evaluated | core | explicit-preferred | published | AOA-T-0016, AOA-T-0015 |
| aoa-property-invariants | canonical | core | explicit-preferred | published | AOA-T-0017, AOA-T-0007 |
| aoa-safe-infra-change | canonical | risk | explicit-only | published | AOA-T-0028, AOA-T-0001 |
| aoa-sanitized-share | canonical | risk | explicit-only | published | AOA-T-0034, AOA-T-0002 |
| aoa-source-of-truth-check | canonical | core | explicit-preferred | published | AOA-T-0013, AOA-T-0002, AOA-T-0009 |
| aoa-tdd-slice | canonical | core | explicit-preferred | published | AOA-T-0014, AOA-T-0001 |
| atm10-change-protocol | reviewed | project | explicit-preferred | published | AOA-T-0001, AOA-T-0002 |
| atm10-source-of-truth-check | reviewed | project | explicit-preferred | published | AOA-T-0013, AOA-T-0002 |

