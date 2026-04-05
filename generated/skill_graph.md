# Skill graph

This derived file summarizes maturity, lineage, scope, invocation, technique, profile, and artifact-group edges for the current skill surface.

```mermaid
graph TD
  skill_abyss_safe_infra_change["abyss-safe-infra-change"]
  status_evaluated["status: evaluated"]
  scope_project["scope: project"]
  lineage_published["lineage: published"]
  policy_explicit_only["invocation: explicit-only"]
  technique_AOA_T_0028["AOA-T-0028"]
  technique_AOA_T_0001["AOA-T-0001"]
  profile_repo_abyss_overlay["profile: repo-abyss-overlay"]
  profile_repo_default["profile: repo-default"]
  artifact_group_portable_export["artifact group: portable_export"]
  artifact_group_runtime_seam["artifact group: runtime_seam"]
  artifact_group_runtime_guardrails["artifact group: runtime_guardrails"]
  artifact_group_description_trigger["artifact group: description_trigger"]
  artifact_group_tiny_router["artifact group: tiny_router"]
  skill_abyss_sanitized_share["abyss-sanitized-share"]
  technique_AOA_T_0034["AOA-T-0034"]
  technique_AOA_T_0002["AOA-T-0002"]
  skill_aoa_adr_write["aoa-adr-write"]
  status_canonical["status: canonical"]
  scope_core["scope: core"]
  policy_explicit_preferred["invocation: explicit-preferred"]
  technique_AOA_T_0033["AOA-T-0033"]
  profile_repo_core_only["profile: repo-core-only"]
  profile_user_curated_core["profile: user-curated-core"]
  skill_aoa_approval_gate_check["aoa-approval-gate-check"]
  scope_risk["scope: risk"]
  profile_repo_risk_explicit["profile: repo-risk-explicit"]
  skill_aoa_bounded_context_map["aoa-bounded-context-map"]
  technique_AOA_T_0016["AOA-T-0016"]
  skill_aoa_change_protocol["aoa-change-protocol"]
  skill_aoa_contract_test["aoa-contract-test"]
  technique_AOA_T_0003["AOA-T-0003"]
  technique_AOA_T_0015["AOA-T-0015"]
  skill_aoa_core_logic_boundary["aoa-core-logic-boundary"]
  skill_aoa_dry_run_first["aoa-dry-run-first"]
  technique_AOA_T_0004["AOA-T-0004"]
  artifact_group_support_resources["artifact group: support_resources"]
  skill_aoa_invariant_coverage_audit["aoa-invariant-coverage-audit"]
  technique_AOA_T_0017["AOA-T-0017"]
  skill_aoa_local_stack_bringup["aoa-local-stack-bringup"]
  technique_AOA_T_0036["AOA-T-0036"]
  technique_AOA_T_0037["AOA-T-0037"]
  technique_AOA_T_0038["AOA-T-0038"]
  skill_aoa_port_adapter_refactor["aoa-port-adapter-refactor"]
  skill_aoa_property_invariants["aoa-property-invariants"]
  technique_AOA_T_0007["AOA-T-0007"]
  skill_aoa_quest_harvest["aoa-quest-harvest"]
  status_scaffold["status: scaffold"]
  lineage_pending["lineage: pending"]
  technique_AOA_T_PENDING_QUEST_HARVEST["AOA-T-PENDING-QUEST-HARVEST"]
  technique_AOA_T_PENDING_PROMOTION_TRIAGE["AOA-T-PENDING-PROMOTION-TRIAGE"]
  profile_repo_quest_harvest_only["profile: repo-quest-harvest-only"]
  skill_aoa_safe_infra_change["aoa-safe-infra-change"]
  skill_aoa_sanitized_share["aoa-sanitized-share"]
  skill_aoa_session_donor_harvest["aoa-session-donor-harvest"]
  technique_AOA_T_PENDING_SESSION_DONOR_HARVEST["AOA-T-PENDING-SESSION-DONOR-HARVEST"]
  technique_AOA_T_PENDING_OWNER_LAYER_TRIAGE["AOA-T-PENDING-OWNER-LAYER-TRIAGE"]
  profile_repo_session_donor_harvest_only["profile: repo-session-donor-harvest-only"]
  skill_aoa_source_of_truth_check["aoa-source-of-truth-check"]
  technique_AOA_T_0013["AOA-T-0013"]
  technique_AOA_T_0009["AOA-T-0009"]
  skill_aoa_tdd_slice["aoa-tdd-slice"]
  technique_AOA_T_0014["AOA-T-0014"]
  skill_atm10_change_protocol["atm10-change-protocol"]
  profile_repo_atm10_overlay["profile: repo-atm10-overlay"]
  skill_atm10_source_of_truth_check["atm10-source-of-truth-check"]
  skill_abyss_safe_infra_change -->|maturity| status_evaluated
  skill_abyss_safe_infra_change -->|scope| scope_project
  skill_abyss_safe_infra_change -->|lineage| lineage_published
  skill_abyss_safe_infra_change -->|invocation_policy| policy_explicit_only
  skill_abyss_safe_infra_change -->|depends_on| technique_AOA_T_0028
  skill_abyss_safe_infra_change -->|depends_on| technique_AOA_T_0001
  skill_abyss_safe_infra_change -->|included_in_profile| profile_repo_abyss_overlay
  skill_abyss_safe_infra_change -->|included_in_profile| profile_repo_default
  skill_abyss_safe_infra_change -->|available_in_artifact_group| artifact_group_portable_export
  skill_abyss_safe_infra_change -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_abyss_safe_infra_change -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_abyss_safe_infra_change -->|available_in_artifact_group| artifact_group_description_trigger
  skill_abyss_safe_infra_change -->|available_in_artifact_group| artifact_group_tiny_router
  skill_abyss_sanitized_share -->|maturity| status_evaluated
  skill_abyss_sanitized_share -->|scope| scope_project
  skill_abyss_sanitized_share -->|lineage| lineage_published
  skill_abyss_sanitized_share -->|invocation_policy| policy_explicit_only
  skill_abyss_sanitized_share -->|depends_on| technique_AOA_T_0034
  skill_abyss_sanitized_share -->|depends_on| technique_AOA_T_0002
  skill_abyss_sanitized_share -->|included_in_profile| profile_repo_abyss_overlay
  skill_abyss_sanitized_share -->|included_in_profile| profile_repo_default
  skill_abyss_sanitized_share -->|available_in_artifact_group| artifact_group_portable_export
  skill_abyss_sanitized_share -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_abyss_sanitized_share -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_abyss_sanitized_share -->|available_in_artifact_group| artifact_group_description_trigger
  skill_abyss_sanitized_share -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_adr_write -->|maturity| status_canonical
  skill_aoa_adr_write -->|scope| scope_core
  skill_aoa_adr_write -->|lineage| lineage_published
  skill_aoa_adr_write -->|invocation_policy| policy_explicit_preferred
  skill_aoa_adr_write -->|depends_on| technique_AOA_T_0033
  skill_aoa_adr_write -->|depends_on| technique_AOA_T_0002
  skill_aoa_adr_write -->|included_in_profile| profile_repo_core_only
  skill_aoa_adr_write -->|included_in_profile| profile_repo_default
  skill_aoa_adr_write -->|included_in_profile| profile_user_curated_core
  skill_aoa_adr_write -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_adr_write -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_adr_write -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_adr_write -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_adr_write -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_approval_gate_check -->|maturity| status_canonical
  skill_aoa_approval_gate_check -->|scope| scope_risk
  skill_aoa_approval_gate_check -->|lineage| lineage_published
  skill_aoa_approval_gate_check -->|invocation_policy| policy_explicit_only
  skill_aoa_approval_gate_check -->|depends_on| technique_AOA_T_0028
  skill_aoa_approval_gate_check -->|included_in_profile| profile_repo_default
  skill_aoa_approval_gate_check -->|included_in_profile| profile_repo_risk_explicit
  skill_aoa_approval_gate_check -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_approval_gate_check -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_approval_gate_check -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_approval_gate_check -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_approval_gate_check -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_bounded_context_map -->|maturity| status_canonical
  skill_aoa_bounded_context_map -->|scope| scope_core
  skill_aoa_bounded_context_map -->|lineage| lineage_published
  skill_aoa_bounded_context_map -->|invocation_policy| policy_explicit_preferred
  skill_aoa_bounded_context_map -->|depends_on| technique_AOA_T_0016
  skill_aoa_bounded_context_map -->|depends_on| technique_AOA_T_0002
  skill_aoa_bounded_context_map -->|included_in_profile| profile_repo_core_only
  skill_aoa_bounded_context_map -->|included_in_profile| profile_repo_default
  skill_aoa_bounded_context_map -->|included_in_profile| profile_user_curated_core
  skill_aoa_bounded_context_map -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_bounded_context_map -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_bounded_context_map -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_bounded_context_map -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_bounded_context_map -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_change_protocol -->|maturity| status_canonical
  skill_aoa_change_protocol -->|scope| scope_core
  skill_aoa_change_protocol -->|lineage| lineage_published
  skill_aoa_change_protocol -->|invocation_policy| policy_explicit_preferred
  skill_aoa_change_protocol -->|depends_on| technique_AOA_T_0001
  skill_aoa_change_protocol -->|depends_on| technique_AOA_T_0002
  skill_aoa_change_protocol -->|included_in_profile| profile_repo_core_only
  skill_aoa_change_protocol -->|included_in_profile| profile_repo_default
  skill_aoa_change_protocol -->|included_in_profile| profile_user_curated_core
  skill_aoa_change_protocol -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_change_protocol -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_change_protocol -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_change_protocol -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_change_protocol -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_contract_test -->|maturity| status_canonical
  skill_aoa_contract_test -->|scope| scope_core
  skill_aoa_contract_test -->|lineage| lineage_published
  skill_aoa_contract_test -->|invocation_policy| policy_explicit_preferred
  skill_aoa_contract_test -->|depends_on| technique_AOA_T_0003
  skill_aoa_contract_test -->|depends_on| technique_AOA_T_0015
  skill_aoa_contract_test -->|included_in_profile| profile_repo_core_only
  skill_aoa_contract_test -->|included_in_profile| profile_repo_default
  skill_aoa_contract_test -->|included_in_profile| profile_user_curated_core
  skill_aoa_contract_test -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_contract_test -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_contract_test -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_contract_test -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_contract_test -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_core_logic_boundary -->|maturity| status_evaluated
  skill_aoa_core_logic_boundary -->|scope| scope_core
  skill_aoa_core_logic_boundary -->|lineage| lineage_published
  skill_aoa_core_logic_boundary -->|invocation_policy| policy_explicit_preferred
  skill_aoa_core_logic_boundary -->|depends_on| technique_AOA_T_0016
  skill_aoa_core_logic_boundary -->|depends_on| technique_AOA_T_0015
  skill_aoa_core_logic_boundary -->|included_in_profile| profile_repo_core_only
  skill_aoa_core_logic_boundary -->|included_in_profile| profile_repo_default
  skill_aoa_core_logic_boundary -->|included_in_profile| profile_user_curated_core
  skill_aoa_core_logic_boundary -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_core_logic_boundary -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_core_logic_boundary -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_core_logic_boundary -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_core_logic_boundary -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_dry_run_first -->|maturity| status_canonical
  skill_aoa_dry_run_first -->|scope| scope_risk
  skill_aoa_dry_run_first -->|lineage| lineage_published
  skill_aoa_dry_run_first -->|invocation_policy| policy_explicit_only
  skill_aoa_dry_run_first -->|depends_on| technique_AOA_T_0004
  skill_aoa_dry_run_first -->|depends_on| technique_AOA_T_0028
  skill_aoa_dry_run_first -->|included_in_profile| profile_repo_default
  skill_aoa_dry_run_first -->|included_in_profile| profile_repo_risk_explicit
  skill_aoa_dry_run_first -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_dry_run_first -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_dry_run_first -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_dry_run_first -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_dry_run_first -->|available_in_artifact_group| artifact_group_support_resources
  skill_aoa_dry_run_first -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_invariant_coverage_audit -->|maturity| status_canonical
  skill_aoa_invariant_coverage_audit -->|scope| scope_core
  skill_aoa_invariant_coverage_audit -->|lineage| lineage_published
  skill_aoa_invariant_coverage_audit -->|invocation_policy| policy_explicit_preferred
  skill_aoa_invariant_coverage_audit -->|depends_on| technique_AOA_T_0017
  skill_aoa_invariant_coverage_audit -->|included_in_profile| profile_repo_core_only
  skill_aoa_invariant_coverage_audit -->|included_in_profile| profile_repo_default
  skill_aoa_invariant_coverage_audit -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_invariant_coverage_audit -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_invariant_coverage_audit -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_invariant_coverage_audit -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_invariant_coverage_audit -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_local_stack_bringup -->|maturity| status_evaluated
  skill_aoa_local_stack_bringup -->|scope| scope_risk
  skill_aoa_local_stack_bringup -->|lineage| lineage_published
  skill_aoa_local_stack_bringup -->|invocation_policy| policy_explicit_only
  skill_aoa_local_stack_bringup -->|depends_on| technique_AOA_T_0036
  skill_aoa_local_stack_bringup -->|depends_on| technique_AOA_T_0037
  skill_aoa_local_stack_bringup -->|depends_on| technique_AOA_T_0028
  skill_aoa_local_stack_bringup -->|depends_on| technique_AOA_T_0038
  skill_aoa_local_stack_bringup -->|included_in_profile| profile_repo_default
  skill_aoa_local_stack_bringup -->|included_in_profile| profile_repo_risk_explicit
  skill_aoa_local_stack_bringup -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_local_stack_bringup -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_local_stack_bringup -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_local_stack_bringup -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_local_stack_bringup -->|available_in_artifact_group| artifact_group_support_resources
  skill_aoa_local_stack_bringup -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_port_adapter_refactor -->|maturity| status_evaluated
  skill_aoa_port_adapter_refactor -->|scope| scope_core
  skill_aoa_port_adapter_refactor -->|lineage| lineage_published
  skill_aoa_port_adapter_refactor -->|invocation_policy| policy_explicit_preferred
  skill_aoa_port_adapter_refactor -->|depends_on| technique_AOA_T_0016
  skill_aoa_port_adapter_refactor -->|depends_on| technique_AOA_T_0015
  skill_aoa_port_adapter_refactor -->|included_in_profile| profile_repo_core_only
  skill_aoa_port_adapter_refactor -->|included_in_profile| profile_repo_default
  skill_aoa_port_adapter_refactor -->|included_in_profile| profile_user_curated_core
  skill_aoa_port_adapter_refactor -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_port_adapter_refactor -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_port_adapter_refactor -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_port_adapter_refactor -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_port_adapter_refactor -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_property_invariants -->|maturity| status_canonical
  skill_aoa_property_invariants -->|scope| scope_core
  skill_aoa_property_invariants -->|lineage| lineage_published
  skill_aoa_property_invariants -->|invocation_policy| policy_explicit_preferred
  skill_aoa_property_invariants -->|depends_on| technique_AOA_T_0017
  skill_aoa_property_invariants -->|depends_on| technique_AOA_T_0007
  skill_aoa_property_invariants -->|included_in_profile| profile_repo_core_only
  skill_aoa_property_invariants -->|included_in_profile| profile_repo_default
  skill_aoa_property_invariants -->|included_in_profile| profile_user_curated_core
  skill_aoa_property_invariants -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_property_invariants -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_property_invariants -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_property_invariants -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_property_invariants -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_quest_harvest -->|maturity| status_scaffold
  skill_aoa_quest_harvest -->|scope| scope_core
  skill_aoa_quest_harvest -->|lineage| lineage_pending
  skill_aoa_quest_harvest -->|invocation_policy| policy_explicit_only
  skill_aoa_quest_harvest -->|depends_on| technique_AOA_T_PENDING_QUEST_HARVEST
  skill_aoa_quest_harvest -->|depends_on| technique_AOA_T_PENDING_PROMOTION_TRIAGE
  skill_aoa_quest_harvest -->|included_in_profile| profile_repo_core_only
  skill_aoa_quest_harvest -->|included_in_profile| profile_repo_default
  skill_aoa_quest_harvest -->|included_in_profile| profile_repo_quest_harvest_only
  skill_aoa_quest_harvest -->|included_in_profile| profile_user_curated_core
  skill_aoa_quest_harvest -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_quest_harvest -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_quest_harvest -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_quest_harvest -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_quest_harvest -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_safe_infra_change -->|maturity| status_canonical
  skill_aoa_safe_infra_change -->|scope| scope_risk
  skill_aoa_safe_infra_change -->|lineage| lineage_published
  skill_aoa_safe_infra_change -->|invocation_policy| policy_explicit_only
  skill_aoa_safe_infra_change -->|depends_on| technique_AOA_T_0028
  skill_aoa_safe_infra_change -->|depends_on| technique_AOA_T_0001
  skill_aoa_safe_infra_change -->|included_in_profile| profile_repo_default
  skill_aoa_safe_infra_change -->|included_in_profile| profile_repo_risk_explicit
  skill_aoa_safe_infra_change -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_safe_infra_change -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_safe_infra_change -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_safe_infra_change -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_safe_infra_change -->|available_in_artifact_group| artifact_group_support_resources
  skill_aoa_safe_infra_change -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_sanitized_share -->|maturity| status_canonical
  skill_aoa_sanitized_share -->|scope| scope_risk
  skill_aoa_sanitized_share -->|lineage| lineage_published
  skill_aoa_sanitized_share -->|invocation_policy| policy_explicit_only
  skill_aoa_sanitized_share -->|depends_on| technique_AOA_T_0034
  skill_aoa_sanitized_share -->|depends_on| technique_AOA_T_0002
  skill_aoa_sanitized_share -->|included_in_profile| profile_repo_default
  skill_aoa_sanitized_share -->|included_in_profile| profile_repo_risk_explicit
  skill_aoa_sanitized_share -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_sanitized_share -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_sanitized_share -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_sanitized_share -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_sanitized_share -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_session_donor_harvest -->|maturity| status_scaffold
  skill_aoa_session_donor_harvest -->|scope| scope_core
  skill_aoa_session_donor_harvest -->|lineage| lineage_pending
  skill_aoa_session_donor_harvest -->|invocation_policy| policy_explicit_only
  skill_aoa_session_donor_harvest -->|depends_on| technique_AOA_T_PENDING_SESSION_DONOR_HARVEST
  skill_aoa_session_donor_harvest -->|depends_on| technique_AOA_T_PENDING_OWNER_LAYER_TRIAGE
  skill_aoa_session_donor_harvest -->|included_in_profile| profile_repo_core_only
  skill_aoa_session_donor_harvest -->|included_in_profile| profile_repo_default
  skill_aoa_session_donor_harvest -->|included_in_profile| profile_repo_session_donor_harvest_only
  skill_aoa_session_donor_harvest -->|included_in_profile| profile_user_curated_core
  skill_aoa_session_donor_harvest -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_session_donor_harvest -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_session_donor_harvest -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_session_donor_harvest -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_session_donor_harvest -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_source_of_truth_check -->|maturity| status_canonical
  skill_aoa_source_of_truth_check -->|scope| scope_core
  skill_aoa_source_of_truth_check -->|lineage| lineage_published
  skill_aoa_source_of_truth_check -->|invocation_policy| policy_explicit_preferred
  skill_aoa_source_of_truth_check -->|depends_on| technique_AOA_T_0013
  skill_aoa_source_of_truth_check -->|depends_on| technique_AOA_T_0002
  skill_aoa_source_of_truth_check -->|depends_on| technique_AOA_T_0009
  skill_aoa_source_of_truth_check -->|included_in_profile| profile_repo_core_only
  skill_aoa_source_of_truth_check -->|included_in_profile| profile_repo_default
  skill_aoa_source_of_truth_check -->|included_in_profile| profile_user_curated_core
  skill_aoa_source_of_truth_check -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_source_of_truth_check -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_source_of_truth_check -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_source_of_truth_check -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_source_of_truth_check -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_tdd_slice -->|maturity| status_canonical
  skill_aoa_tdd_slice -->|scope| scope_core
  skill_aoa_tdd_slice -->|lineage| lineage_published
  skill_aoa_tdd_slice -->|invocation_policy| policy_explicit_preferred
  skill_aoa_tdd_slice -->|depends_on| technique_AOA_T_0014
  skill_aoa_tdd_slice -->|depends_on| technique_AOA_T_0001
  skill_aoa_tdd_slice -->|included_in_profile| profile_repo_core_only
  skill_aoa_tdd_slice -->|included_in_profile| profile_repo_default
  skill_aoa_tdd_slice -->|included_in_profile| profile_user_curated_core
  skill_aoa_tdd_slice -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_tdd_slice -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_tdd_slice -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_tdd_slice -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_tdd_slice -->|available_in_artifact_group| artifact_group_tiny_router
  skill_atm10_change_protocol -->|maturity| status_evaluated
  skill_atm10_change_protocol -->|scope| scope_project
  skill_atm10_change_protocol -->|lineage| lineage_published
  skill_atm10_change_protocol -->|invocation_policy| policy_explicit_preferred
  skill_atm10_change_protocol -->|depends_on| technique_AOA_T_0001
  skill_atm10_change_protocol -->|depends_on| technique_AOA_T_0002
  skill_atm10_change_protocol -->|included_in_profile| profile_repo_atm10_overlay
  skill_atm10_change_protocol -->|included_in_profile| profile_repo_default
  skill_atm10_change_protocol -->|available_in_artifact_group| artifact_group_portable_export
  skill_atm10_change_protocol -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_atm10_change_protocol -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_atm10_change_protocol -->|available_in_artifact_group| artifact_group_description_trigger
  skill_atm10_change_protocol -->|available_in_artifact_group| artifact_group_tiny_router
  skill_atm10_source_of_truth_check -->|maturity| status_evaluated
  skill_atm10_source_of_truth_check -->|scope| scope_project
  skill_atm10_source_of_truth_check -->|lineage| lineage_published
  skill_atm10_source_of_truth_check -->|invocation_policy| policy_explicit_preferred
  skill_atm10_source_of_truth_check -->|depends_on| technique_AOA_T_0013
  skill_atm10_source_of_truth_check -->|depends_on| technique_AOA_T_0002
  skill_atm10_source_of_truth_check -->|included_in_profile| profile_repo_atm10_overlay
  skill_atm10_source_of_truth_check -->|included_in_profile| profile_repo_default
  skill_atm10_source_of_truth_check -->|available_in_artifact_group| artifact_group_portable_export
  skill_atm10_source_of_truth_check -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_atm10_source_of_truth_check -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_atm10_source_of_truth_check -->|available_in_artifact_group| artifact_group_description_trigger
  skill_atm10_source_of_truth_check -->|available_in_artifact_group| artifact_group_tiny_router
```

| name | status | scope | invocation | lineage | profiles | artifact groups | techniques |
|---|---|---|---|---|---|---|---|
| abyss-safe-infra-change | evaluated | project | explicit-only | published | repo-abyss-overlay, repo-default | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0028, AOA-T-0001 |
| abyss-sanitized-share | evaluated | project | explicit-only | published | repo-abyss-overlay, repo-default | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0034, AOA-T-0002 |
| aoa-adr-write | canonical | core | explicit-preferred | published | repo-core-only, repo-default, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0033, AOA-T-0002 |
| aoa-approval-gate-check | canonical | risk | explicit-only | published | repo-default, repo-risk-explicit | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0028 |
| aoa-bounded-context-map | canonical | core | explicit-preferred | published | repo-core-only, repo-default, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0016, AOA-T-0002 |
| aoa-change-protocol | canonical | core | explicit-preferred | published | repo-core-only, repo-default, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0001, AOA-T-0002 |
| aoa-contract-test | canonical | core | explicit-preferred | published | repo-core-only, repo-default, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0003, AOA-T-0015 |
| aoa-core-logic-boundary | evaluated | core | explicit-preferred | published | repo-core-only, repo-default, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0016, AOA-T-0015 |
| aoa-dry-run-first | canonical | risk | explicit-only | published | repo-default, repo-risk-explicit | portable_export, runtime_seam, runtime_guardrails, description_trigger, support_resources, tiny_router | AOA-T-0004, AOA-T-0028 |
| aoa-invariant-coverage-audit | canonical | core | explicit-preferred | published | repo-core-only, repo-default | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0017 |
| aoa-local-stack-bringup | evaluated | risk | explicit-only | published | repo-default, repo-risk-explicit | portable_export, runtime_seam, runtime_guardrails, description_trigger, support_resources, tiny_router | AOA-T-0036, AOA-T-0037, AOA-T-0028, AOA-T-0038 |
| aoa-port-adapter-refactor | evaluated | core | explicit-preferred | published | repo-core-only, repo-default, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0016, AOA-T-0015 |
| aoa-property-invariants | canonical | core | explicit-preferred | published | repo-core-only, repo-default, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0017, AOA-T-0007 |
| aoa-quest-harvest | scaffold | core | explicit-only | pending | repo-core-only, repo-default, repo-quest-harvest-only, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-PENDING-QUEST-HARVEST, AOA-T-PENDING-PROMOTION-TRIAGE |
| aoa-safe-infra-change | canonical | risk | explicit-only | published | repo-default, repo-risk-explicit | portable_export, runtime_seam, runtime_guardrails, description_trigger, support_resources, tiny_router | AOA-T-0028, AOA-T-0001 |
| aoa-sanitized-share | canonical | risk | explicit-only | published | repo-default, repo-risk-explicit | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0034, AOA-T-0002 |
| aoa-session-donor-harvest | scaffold | core | explicit-only | pending | repo-core-only, repo-default, repo-session-donor-harvest-only, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-PENDING-SESSION-DONOR-HARVEST, AOA-T-PENDING-OWNER-LAYER-TRIAGE |
| aoa-source-of-truth-check | canonical | core | explicit-preferred | published | repo-core-only, repo-default, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0013, AOA-T-0002, AOA-T-0009 |
| aoa-tdd-slice | canonical | core | explicit-preferred | published | repo-core-only, repo-default, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0014, AOA-T-0001 |
| atm10-change-protocol | evaluated | project | explicit-preferred | published | repo-atm10-overlay, repo-default | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0001, AOA-T-0002 |
| atm10-source-of-truth-check | evaluated | project | explicit-preferred | published | repo-atm10-overlay, repo-default | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0013, AOA-T-0002 |

