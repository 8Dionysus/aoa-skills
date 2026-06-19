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
  skill_abyss_self_diagnostic_spine["abyss-self-diagnostic-spine"]
  status_scaffold["status: scaffold"]
  policy_explicit_preferred["invocation: explicit-preferred"]
  technique_AOA_T_0080["AOA-T-0080"]
  technique_AOA_T_0081["AOA-T-0081"]
  skill_aoa_adr_write["aoa-adr-write"]
  status_canonical["status: canonical"]
  scope_core["scope: core"]
  technique_AOA_T_0033["AOA-T-0033"]
  profile_repo_core_only["profile: repo-core-only"]
  profile_repo_project_core_outer_ring["profile: repo-project-core-outer-ring"]
  profile_repo_project_foundation["profile: repo-project-foundation"]
  profile_user_aoa_foundation["profile: user-aoa-foundation"]
  profile_user_curated_core["profile: user-curated-core"]
  skill_aoa_approval_gate_check["aoa-approval-gate-check"]
  scope_risk["scope: risk"]
  profile_repo_project_risk_guard_ring["profile: repo-project-risk-guard-ring"]
  profile_repo_risk_explicit["profile: repo-risk-explicit"]
  skill_aoa_automation_opportunity_scan["aoa-automation-opportunity-scan"]
  technique_AOA_T_0086["AOA-T-0086"]
  technique_AOA_T_0087["AOA-T-0087"]
  technique_AOA_T_0088["AOA-T-0088"]
  profile_repo_automation_opportunity_scan_only["profile: repo-automation-opportunity-scan-only"]
  profile_repo_project_core_kernel["profile: repo-project-core-kernel"]
  profile_repo_session_growth["profile: repo-session-growth"]
  profile_repo_session_harvest_family["profile: repo-session-harvest-family"]
  skill_aoa_bounded_context_map["aoa-bounded-context-map"]
  technique_AOA_T_0016["AOA-T-0016"]
  skill_aoa_change_protocol["aoa-change-protocol"]
  skill_aoa_checkpoint_closeout_bridge["aoa-checkpoint-closeout-bridge"]
  technique_AOA_T_0075["AOA-T-0075"]
  technique_AOA_T_0084["AOA-T-0084"]
  technique_AOA_T_0089["AOA-T-0089"]
  skill_aoa_commit_growth_seam["aoa-commit-growth-seam"]
  skill_aoa_contract_test["aoa-contract-test"]
  technique_AOA_T_0003["AOA-T-0003"]
  technique_AOA_T_0015["AOA-T-0015"]
  skill_aoa_core_logic_boundary["aoa-core-logic-boundary"]
  skill_aoa_decision["aoa-decision"]
  skill_aoa_decision_correct["aoa-decision-correct"]
  skill_aoa_decision_create["aoa-decision-create"]
  skill_aoa_decision_find["aoa-decision-find"]
  skill_aoa_dry_run_first["aoa-dry-run-first"]
  technique_AOA_T_0004["AOA-T-0004"]
  artifact_group_support_resources["artifact group: support_resources"]
  skill_aoa_eval["aoa-eval"]
  technique_AOA_T_0076["AOA-T-0076"]
  technique_AOA_T_0094["AOA-T-0094"]
  skill_aoa_eval_apply["aoa-eval-apply"]
  technique_AOA_T_0007["AOA-T-0007"]
  technique_AOA_T_0096["AOA-T-0096"]
  skill_aoa_eval_design["aoa-eval-design"]
  technique_AOA_T_0017["AOA-T-0017"]
  skill_aoa_eval_local_need["aoa-eval-local-need"]
  technique_AOA_T_0105["AOA-T-0105"]
  skill_aoa_eval_select["aoa-eval-select"]
  skill_aoa_eval_session_mining["aoa-eval-session-mining"]
  technique_AOA_T_0067["AOA-T-0067"]
  skill_aoa_invariant_coverage_audit["aoa-invariant-coverage-audit"]
  skill_aoa_local_stack_bringup["aoa-local-stack-bringup"]
  technique_AOA_T_0036["AOA-T-0036"]
  technique_AOA_T_0037["AOA-T-0037"]
  technique_AOA_T_0038["AOA-T-0038"]
  skill_aoa_memo_writeback["aoa-memo-writeback"]
  technique_AOA_T_0026["AOA-T-0026"]
  technique_AOA_T_0106["AOA-T-0106"]
  skill_aoa_port_adapter_refactor["aoa-port-adapter-refactor"]
  skill_aoa_property_invariants["aoa-property-invariants"]
  skill_aoa_quest_harvest["aoa-quest-harvest"]
  technique_AOA_T_0090["AOA-T-0090"]
  profile_repo_quest_harvest_only["profile: repo-quest-harvest-only"]
  skill_aoa_safe_infra_change["aoa-safe-infra-change"]
  skill_aoa_sanitized_share["aoa-sanitized-share"]
  skill_aoa_session_donor_harvest["aoa-session-donor-harvest"]
  technique_AOA_T_0077["AOA-T-0077"]
  profile_repo_session_donor_harvest_only["profile: repo-session-donor-harvest-only"]
  skill_aoa_session_progression_lift["aoa-session-progression-lift"]
  technique_AOA_T_0085["AOA-T-0085"]
  skill_aoa_session_route_forks["aoa-session-route-forks"]
  technique_AOA_T_0078["AOA-T-0078"]
  technique_AOA_T_0079["AOA-T-0079"]
  skill_aoa_session_self_diagnose["aoa-session-self-diagnose"]
  skill_aoa_session_self_repair["aoa-session-self-repair"]
  technique_AOA_T_0082["AOA-T-0082"]
  technique_AOA_T_0083["AOA-T-0083"]
  skill_aoa_source_of_truth_check["aoa-source-of-truth-check"]
  technique_AOA_T_0013["AOA-T-0013"]
  technique_AOA_T_0009["AOA-T-0009"]
  skill_aoa_summon["aoa-summon"]
  technique_AOA_T_0062["AOA-T-0062"]
  technique_AOA_T_0058["AOA-T-0058"]
  profile_repo_summon_only["profile: repo-summon-only"]
  skill_aoa_tdd_slice["aoa-tdd-slice"]
  technique_AOA_T_0014["AOA-T-0014"]
  skill_atm10_change_protocol["atm10-change-protocol"]
  profile_repo_atm10_overlay["profile: repo-atm10-overlay"]
  skill_atm10_source_of_truth_check["atm10-source-of-truth-check"]
  skill_titan_approval_ledger["titan-approval-ledger"]
  technique_AOA_T_0045["AOA-T-0045"]
  profile_repo_titan_overlay["profile: repo-titan-overlay"]
  skill_titan_approval_loom["titan-approval-loom"]
  skill_titan_appserver_bridge["titan-appserver-bridge"]
  technique_AOA_T_0066["AOA-T-0066"]
  technique_AOA_T_0043["AOA-T-0043"]
  skill_titan_appserver_plan["titan-appserver-plan"]
  technique_AOA_T_0091["AOA-T-0091"]
  skill_titan_closeout["titan-closeout"]
  skill_titan_console["titan-console"]
  skill_titan_event_replay["titan-event-replay"]
  skill_titan_memory_loom["titan-memory-loom"]
  technique_AOA_T_0053["AOA-T-0053"]
  skill_titan_memory_prune["titan-memory-prune"]
  technique_AOA_T_0103["AOA-T-0103"]
  technique_AOA_T_0104["AOA-T-0104"]
  skill_titan_mutation_gate["titan-mutation-gate"]
  skill_titan_recall["titan-recall"]
  skill_titan_receipt["titan-receipt"]
  skill_titan_runtime_gate["titan-runtime-gate"]
  skill_titan_summon["titan-summon"]
  technique_AOA_T_0060["AOA-T-0060"]
  skill_titan_thread_turn_binding["titan-thread-turn-binding"]
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
  skill_abyss_self_diagnostic_spine -->|maturity| status_scaffold
  skill_abyss_self_diagnostic_spine -->|scope| scope_project
  skill_abyss_self_diagnostic_spine -->|lineage| lineage_published
  skill_abyss_self_diagnostic_spine -->|invocation_policy| policy_explicit_preferred
  skill_abyss_self_diagnostic_spine -->|depends_on| technique_AOA_T_0080
  skill_abyss_self_diagnostic_spine -->|depends_on| technique_AOA_T_0081
  skill_abyss_self_diagnostic_spine -->|included_in_profile| profile_repo_abyss_overlay
  skill_abyss_self_diagnostic_spine -->|included_in_profile| profile_repo_default
  skill_abyss_self_diagnostic_spine -->|available_in_artifact_group| artifact_group_portable_export
  skill_abyss_self_diagnostic_spine -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_abyss_self_diagnostic_spine -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_abyss_self_diagnostic_spine -->|available_in_artifact_group| artifact_group_description_trigger
  skill_abyss_self_diagnostic_spine -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_adr_write -->|maturity| status_canonical
  skill_aoa_adr_write -->|scope| scope_core
  skill_aoa_adr_write -->|lineage| lineage_published
  skill_aoa_adr_write -->|invocation_policy| policy_explicit_preferred
  skill_aoa_adr_write -->|depends_on| technique_AOA_T_0033
  skill_aoa_adr_write -->|depends_on| technique_AOA_T_0002
  skill_aoa_adr_write -->|included_in_profile| profile_repo_core_only
  skill_aoa_adr_write -->|included_in_profile| profile_repo_default
  skill_aoa_adr_write -->|included_in_profile| profile_repo_project_core_outer_ring
  skill_aoa_adr_write -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_adr_write -->|included_in_profile| profile_user_aoa_foundation
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
  skill_aoa_approval_gate_check -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_approval_gate_check -->|included_in_profile| profile_repo_project_risk_guard_ring
  skill_aoa_approval_gate_check -->|included_in_profile| profile_repo_risk_explicit
  skill_aoa_approval_gate_check -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_approval_gate_check -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_approval_gate_check -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_approval_gate_check -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_approval_gate_check -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_approval_gate_check -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_automation_opportunity_scan -->|maturity| status_evaluated
  skill_aoa_automation_opportunity_scan -->|scope| scope_core
  skill_aoa_automation_opportunity_scan -->|lineage| lineage_published
  skill_aoa_automation_opportunity_scan -->|invocation_policy| policy_explicit_only
  skill_aoa_automation_opportunity_scan -->|depends_on| technique_AOA_T_0086
  skill_aoa_automation_opportunity_scan -->|depends_on| technique_AOA_T_0087
  skill_aoa_automation_opportunity_scan -->|depends_on| technique_AOA_T_0088
  skill_aoa_automation_opportunity_scan -->|included_in_profile| profile_repo_automation_opportunity_scan_only
  skill_aoa_automation_opportunity_scan -->|included_in_profile| profile_repo_core_only
  skill_aoa_automation_opportunity_scan -->|included_in_profile| profile_repo_default
  skill_aoa_automation_opportunity_scan -->|included_in_profile| profile_repo_project_core_kernel
  skill_aoa_automation_opportunity_scan -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_automation_opportunity_scan -->|included_in_profile| profile_repo_session_growth
  skill_aoa_automation_opportunity_scan -->|included_in_profile| profile_repo_session_harvest_family
  skill_aoa_automation_opportunity_scan -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_automation_opportunity_scan -->|included_in_profile| profile_user_curated_core
  skill_aoa_automation_opportunity_scan -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_automation_opportunity_scan -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_automation_opportunity_scan -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_automation_opportunity_scan -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_automation_opportunity_scan -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_bounded_context_map -->|maturity| status_canonical
  skill_aoa_bounded_context_map -->|scope| scope_core
  skill_aoa_bounded_context_map -->|lineage| lineage_published
  skill_aoa_bounded_context_map -->|invocation_policy| policy_explicit_preferred
  skill_aoa_bounded_context_map -->|depends_on| technique_AOA_T_0016
  skill_aoa_bounded_context_map -->|depends_on| technique_AOA_T_0002
  skill_aoa_bounded_context_map -->|included_in_profile| profile_repo_core_only
  skill_aoa_bounded_context_map -->|included_in_profile| profile_repo_default
  skill_aoa_bounded_context_map -->|included_in_profile| profile_repo_project_core_outer_ring
  skill_aoa_bounded_context_map -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_bounded_context_map -->|included_in_profile| profile_user_aoa_foundation
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
  skill_aoa_change_protocol -->|included_in_profile| profile_repo_project_core_outer_ring
  skill_aoa_change_protocol -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_change_protocol -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_change_protocol -->|included_in_profile| profile_user_curated_core
  skill_aoa_change_protocol -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_change_protocol -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_change_protocol -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_change_protocol -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_change_protocol -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_checkpoint_closeout_bridge -->|maturity| status_evaluated
  skill_aoa_checkpoint_closeout_bridge -->|scope| scope_core
  skill_aoa_checkpoint_closeout_bridge -->|lineage| lineage_published
  skill_aoa_checkpoint_closeout_bridge -->|invocation_policy| policy_explicit_preferred
  skill_aoa_checkpoint_closeout_bridge -->|depends_on| technique_AOA_T_0075
  skill_aoa_checkpoint_closeout_bridge -->|depends_on| technique_AOA_T_0084
  skill_aoa_checkpoint_closeout_bridge -->|depends_on| technique_AOA_T_0089
  skill_aoa_checkpoint_closeout_bridge -->|included_in_profile| profile_repo_core_only
  skill_aoa_checkpoint_closeout_bridge -->|included_in_profile| profile_repo_default
  skill_aoa_checkpoint_closeout_bridge -->|included_in_profile| profile_repo_project_core_kernel
  skill_aoa_checkpoint_closeout_bridge -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_checkpoint_closeout_bridge -->|included_in_profile| profile_repo_session_growth
  skill_aoa_checkpoint_closeout_bridge -->|included_in_profile| profile_repo_session_harvest_family
  skill_aoa_checkpoint_closeout_bridge -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_checkpoint_closeout_bridge -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_checkpoint_closeout_bridge -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_checkpoint_closeout_bridge -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_checkpoint_closeout_bridge -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_checkpoint_closeout_bridge -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_commit_growth_seam -->|maturity| status_evaluated
  skill_aoa_commit_growth_seam -->|scope| scope_core
  skill_aoa_commit_growth_seam -->|lineage| lineage_published
  skill_aoa_commit_growth_seam -->|invocation_policy| policy_explicit_only
  skill_aoa_commit_growth_seam -->|depends_on| technique_AOA_T_0001
  skill_aoa_commit_growth_seam -->|depends_on| technique_AOA_T_0028
  skill_aoa_commit_growth_seam -->|included_in_profile| profile_repo_default
  skill_aoa_commit_growth_seam -->|included_in_profile| profile_repo_session_growth
  skill_aoa_commit_growth_seam -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_commit_growth_seam -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_commit_growth_seam -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_commit_growth_seam -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_commit_growth_seam -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_commit_growth_seam -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_contract_test -->|maturity| status_canonical
  skill_aoa_contract_test -->|scope| scope_core
  skill_aoa_contract_test -->|lineage| lineage_published
  skill_aoa_contract_test -->|invocation_policy| policy_explicit_preferred
  skill_aoa_contract_test -->|depends_on| technique_AOA_T_0003
  skill_aoa_contract_test -->|depends_on| technique_AOA_T_0015
  skill_aoa_contract_test -->|included_in_profile| profile_repo_core_only
  skill_aoa_contract_test -->|included_in_profile| profile_repo_default
  skill_aoa_contract_test -->|included_in_profile| profile_repo_project_core_outer_ring
  skill_aoa_contract_test -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_contract_test -->|included_in_profile| profile_user_aoa_foundation
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
  skill_aoa_core_logic_boundary -->|included_in_profile| profile_repo_project_core_outer_ring
  skill_aoa_core_logic_boundary -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_core_logic_boundary -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_core_logic_boundary -->|included_in_profile| profile_user_curated_core
  skill_aoa_core_logic_boundary -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_core_logic_boundary -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_core_logic_boundary -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_core_logic_boundary -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_core_logic_boundary -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_decision -->|maturity| status_evaluated
  skill_aoa_decision -->|scope| scope_core
  skill_aoa_decision -->|lineage| lineage_published
  skill_aoa_decision -->|invocation_policy| policy_explicit_preferred
  skill_aoa_decision -->|depends_on| technique_AOA_T_0033
  skill_aoa_decision -->|depends_on| technique_AOA_T_0002
  skill_aoa_decision -->|included_in_profile| profile_repo_core_only
  skill_aoa_decision -->|included_in_profile| profile_repo_default
  skill_aoa_decision -->|included_in_profile| profile_repo_project_core_outer_ring
  skill_aoa_decision -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_decision -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_decision -->|included_in_profile| profile_user_curated_core
  skill_aoa_decision -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_decision -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_decision -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_decision -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_decision -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_decision_correct -->|maturity| status_evaluated
  skill_aoa_decision_correct -->|scope| scope_core
  skill_aoa_decision_correct -->|lineage| lineage_published
  skill_aoa_decision_correct -->|invocation_policy| policy_explicit_preferred
  skill_aoa_decision_correct -->|depends_on| technique_AOA_T_0001
  skill_aoa_decision_correct -->|depends_on| technique_AOA_T_0033
  skill_aoa_decision_correct -->|depends_on| technique_AOA_T_0002
  skill_aoa_decision_correct -->|included_in_profile| profile_repo_core_only
  skill_aoa_decision_correct -->|included_in_profile| profile_repo_default
  skill_aoa_decision_correct -->|included_in_profile| profile_repo_project_core_outer_ring
  skill_aoa_decision_correct -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_decision_correct -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_decision_correct -->|included_in_profile| profile_user_curated_core
  skill_aoa_decision_correct -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_decision_correct -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_decision_correct -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_decision_correct -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_decision_correct -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_decision_create -->|maturity| status_evaluated
  skill_aoa_decision_create -->|scope| scope_core
  skill_aoa_decision_create -->|lineage| lineage_published
  skill_aoa_decision_create -->|invocation_policy| policy_explicit_preferred
  skill_aoa_decision_create -->|depends_on| technique_AOA_T_0033
  skill_aoa_decision_create -->|depends_on| technique_AOA_T_0002
  skill_aoa_decision_create -->|included_in_profile| profile_repo_core_only
  skill_aoa_decision_create -->|included_in_profile| profile_repo_default
  skill_aoa_decision_create -->|included_in_profile| profile_repo_project_core_outer_ring
  skill_aoa_decision_create -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_decision_create -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_decision_create -->|included_in_profile| profile_user_curated_core
  skill_aoa_decision_create -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_decision_create -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_decision_create -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_decision_create -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_decision_create -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_decision_find -->|maturity| status_evaluated
  skill_aoa_decision_find -->|scope| scope_core
  skill_aoa_decision_find -->|lineage| lineage_published
  skill_aoa_decision_find -->|invocation_policy| policy_explicit_preferred
  skill_aoa_decision_find -->|depends_on| technique_AOA_T_0002
  skill_aoa_decision_find -->|included_in_profile| profile_repo_core_only
  skill_aoa_decision_find -->|included_in_profile| profile_repo_default
  skill_aoa_decision_find -->|included_in_profile| profile_repo_project_core_outer_ring
  skill_aoa_decision_find -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_decision_find -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_decision_find -->|included_in_profile| profile_user_curated_core
  skill_aoa_decision_find -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_decision_find -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_decision_find -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_decision_find -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_decision_find -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_dry_run_first -->|maturity| status_canonical
  skill_aoa_dry_run_first -->|scope| scope_risk
  skill_aoa_dry_run_first -->|lineage| lineage_published
  skill_aoa_dry_run_first -->|invocation_policy| policy_explicit_only
  skill_aoa_dry_run_first -->|depends_on| technique_AOA_T_0004
  skill_aoa_dry_run_first -->|depends_on| technique_AOA_T_0028
  skill_aoa_dry_run_first -->|included_in_profile| profile_repo_default
  skill_aoa_dry_run_first -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_dry_run_first -->|included_in_profile| profile_repo_project_risk_guard_ring
  skill_aoa_dry_run_first -->|included_in_profile| profile_repo_risk_explicit
  skill_aoa_dry_run_first -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_dry_run_first -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_dry_run_first -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_dry_run_first -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_dry_run_first -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_dry_run_first -->|available_in_artifact_group| artifact_group_support_resources
  skill_aoa_dry_run_first -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_eval -->|maturity| status_scaffold
  skill_aoa_eval -->|scope| scope_core
  skill_aoa_eval -->|lineage| lineage_published
  skill_aoa_eval -->|invocation_policy| policy_explicit_preferred
  skill_aoa_eval -->|depends_on| technique_AOA_T_0003
  skill_aoa_eval -->|depends_on| technique_AOA_T_0076
  skill_aoa_eval -->|depends_on| technique_AOA_T_0094
  skill_aoa_eval -->|included_in_profile| profile_repo_default
  skill_aoa_eval -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_eval -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_eval -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_eval -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_eval -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_eval -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_eval_apply -->|maturity| status_scaffold
  skill_aoa_eval_apply -->|scope| scope_core
  skill_aoa_eval_apply -->|lineage| lineage_published
  skill_aoa_eval_apply -->|invocation_policy| policy_explicit_preferred
  skill_aoa_eval_apply -->|depends_on| technique_AOA_T_0003
  skill_aoa_eval_apply -->|depends_on| technique_AOA_T_0007
  skill_aoa_eval_apply -->|depends_on| technique_AOA_T_0096
  skill_aoa_eval_apply -->|included_in_profile| profile_repo_default
  skill_aoa_eval_apply -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_eval_apply -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_eval_apply -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_eval_apply -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_eval_apply -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_eval_apply -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_eval_design -->|maturity| status_scaffold
  skill_aoa_eval_design -->|scope| scope_core
  skill_aoa_eval_design -->|lineage| lineage_published
  skill_aoa_eval_design -->|invocation_policy| policy_explicit_preferred
  skill_aoa_eval_design -->|depends_on| technique_AOA_T_0015
  skill_aoa_eval_design -->|depends_on| technique_AOA_T_0017
  skill_aoa_eval_design -->|depends_on| technique_AOA_T_0007
  skill_aoa_eval_design -->|included_in_profile| profile_repo_default
  skill_aoa_eval_design -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_eval_design -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_eval_design -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_eval_design -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_eval_design -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_eval_design -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_eval_local_need -->|maturity| status_scaffold
  skill_aoa_eval_local_need -->|scope| scope_core
  skill_aoa_eval_local_need -->|lineage| lineage_published
  skill_aoa_eval_local_need -->|invocation_policy| policy_explicit_preferred
  skill_aoa_eval_local_need -->|depends_on| technique_AOA_T_0076
  skill_aoa_eval_local_need -->|depends_on| technique_AOA_T_0094
  skill_aoa_eval_local_need -->|depends_on| technique_AOA_T_0105
  skill_aoa_eval_local_need -->|included_in_profile| profile_repo_default
  skill_aoa_eval_local_need -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_eval_local_need -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_eval_local_need -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_eval_local_need -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_eval_local_need -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_eval_local_need -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_eval_select -->|maturity| status_scaffold
  skill_aoa_eval_select -->|scope| scope_core
  skill_aoa_eval_select -->|lineage| lineage_published
  skill_aoa_eval_select -->|invocation_policy| policy_explicit_preferred
  skill_aoa_eval_select -->|depends_on| technique_AOA_T_0003
  skill_aoa_eval_select -->|depends_on| technique_AOA_T_0076
  skill_aoa_eval_select -->|depends_on| technique_AOA_T_0094
  skill_aoa_eval_select -->|included_in_profile| profile_repo_default
  skill_aoa_eval_select -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_eval_select -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_eval_select -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_eval_select -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_eval_select -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_eval_select -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_eval_session_mining -->|maturity| status_scaffold
  skill_aoa_eval_session_mining -->|scope| scope_core
  skill_aoa_eval_session_mining -->|lineage| lineage_published
  skill_aoa_eval_session_mining -->|invocation_policy| policy_explicit_preferred
  skill_aoa_eval_session_mining -->|depends_on| technique_AOA_T_0075
  skill_aoa_eval_session_mining -->|depends_on| technique_AOA_T_0067
  skill_aoa_eval_session_mining -->|depends_on| technique_AOA_T_0081
  skill_aoa_eval_session_mining -->|included_in_profile| profile_repo_default
  skill_aoa_eval_session_mining -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_eval_session_mining -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_eval_session_mining -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_eval_session_mining -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_eval_session_mining -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_eval_session_mining -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_invariant_coverage_audit -->|maturity| status_canonical
  skill_aoa_invariant_coverage_audit -->|scope| scope_core
  skill_aoa_invariant_coverage_audit -->|lineage| lineage_published
  skill_aoa_invariant_coverage_audit -->|invocation_policy| policy_explicit_preferred
  skill_aoa_invariant_coverage_audit -->|depends_on| technique_AOA_T_0017
  skill_aoa_invariant_coverage_audit -->|included_in_profile| profile_repo_core_only
  skill_aoa_invariant_coverage_audit -->|included_in_profile| profile_repo_default
  skill_aoa_invariant_coverage_audit -->|included_in_profile| profile_repo_project_core_outer_ring
  skill_aoa_invariant_coverage_audit -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_invariant_coverage_audit -->|included_in_profile| profile_user_aoa_foundation
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
  skill_aoa_local_stack_bringup -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_local_stack_bringup -->|included_in_profile| profile_repo_project_risk_guard_ring
  skill_aoa_local_stack_bringup -->|included_in_profile| profile_repo_risk_explicit
  skill_aoa_local_stack_bringup -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_local_stack_bringup -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_local_stack_bringup -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_local_stack_bringup -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_local_stack_bringup -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_local_stack_bringup -->|available_in_artifact_group| artifact_group_support_resources
  skill_aoa_local_stack_bringup -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_memo_writeback -->|maturity| status_scaffold
  skill_aoa_memo_writeback -->|scope| scope_core
  skill_aoa_memo_writeback -->|lineage| lineage_published
  skill_aoa_memo_writeback -->|invocation_policy| policy_explicit_preferred
  skill_aoa_memo_writeback -->|depends_on| technique_AOA_T_0026
  skill_aoa_memo_writeback -->|depends_on| technique_AOA_T_0106
  skill_aoa_memo_writeback -->|depends_on| technique_AOA_T_0076
  skill_aoa_memo_writeback -->|included_in_profile| profile_repo_core_only
  skill_aoa_memo_writeback -->|included_in_profile| profile_repo_default
  skill_aoa_memo_writeback -->|included_in_profile| profile_repo_project_core_kernel
  skill_aoa_memo_writeback -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_memo_writeback -->|included_in_profile| profile_repo_session_growth
  skill_aoa_memo_writeback -->|included_in_profile| profile_repo_session_harvest_family
  skill_aoa_memo_writeback -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_memo_writeback -->|included_in_profile| profile_user_curated_core
  skill_aoa_memo_writeback -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_memo_writeback -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_memo_writeback -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_memo_writeback -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_memo_writeback -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_port_adapter_refactor -->|maturity| status_evaluated
  skill_aoa_port_adapter_refactor -->|scope| scope_core
  skill_aoa_port_adapter_refactor -->|lineage| lineage_published
  skill_aoa_port_adapter_refactor -->|invocation_policy| policy_explicit_preferred
  skill_aoa_port_adapter_refactor -->|depends_on| technique_AOA_T_0016
  skill_aoa_port_adapter_refactor -->|depends_on| technique_AOA_T_0015
  skill_aoa_port_adapter_refactor -->|included_in_profile| profile_repo_core_only
  skill_aoa_port_adapter_refactor -->|included_in_profile| profile_repo_default
  skill_aoa_port_adapter_refactor -->|included_in_profile| profile_repo_project_core_outer_ring
  skill_aoa_port_adapter_refactor -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_port_adapter_refactor -->|included_in_profile| profile_user_aoa_foundation
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
  skill_aoa_property_invariants -->|included_in_profile| profile_repo_project_core_outer_ring
  skill_aoa_property_invariants -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_property_invariants -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_property_invariants -->|included_in_profile| profile_user_curated_core
  skill_aoa_property_invariants -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_property_invariants -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_property_invariants -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_property_invariants -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_property_invariants -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_quest_harvest -->|maturity| status_evaluated
  skill_aoa_quest_harvest -->|scope| scope_core
  skill_aoa_quest_harvest -->|lineage| lineage_published
  skill_aoa_quest_harvest -->|invocation_policy| policy_explicit_only
  skill_aoa_quest_harvest -->|depends_on| technique_AOA_T_0089
  skill_aoa_quest_harvest -->|depends_on| technique_AOA_T_0090
  skill_aoa_quest_harvest -->|included_in_profile| profile_repo_core_only
  skill_aoa_quest_harvest -->|included_in_profile| profile_repo_default
  skill_aoa_quest_harvest -->|included_in_profile| profile_repo_project_core_kernel
  skill_aoa_quest_harvest -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_quest_harvest -->|included_in_profile| profile_repo_quest_harvest_only
  skill_aoa_quest_harvest -->|included_in_profile| profile_repo_session_growth
  skill_aoa_quest_harvest -->|included_in_profile| profile_repo_session_harvest_family
  skill_aoa_quest_harvest -->|included_in_profile| profile_user_aoa_foundation
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
  skill_aoa_safe_infra_change -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_safe_infra_change -->|included_in_profile| profile_repo_project_risk_guard_ring
  skill_aoa_safe_infra_change -->|included_in_profile| profile_repo_risk_explicit
  skill_aoa_safe_infra_change -->|included_in_profile| profile_user_aoa_foundation
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
  skill_aoa_sanitized_share -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_sanitized_share -->|included_in_profile| profile_repo_project_risk_guard_ring
  skill_aoa_sanitized_share -->|included_in_profile| profile_repo_risk_explicit
  skill_aoa_sanitized_share -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_sanitized_share -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_sanitized_share -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_sanitized_share -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_sanitized_share -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_sanitized_share -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_session_donor_harvest -->|maturity| status_evaluated
  skill_aoa_session_donor_harvest -->|scope| scope_core
  skill_aoa_session_donor_harvest -->|lineage| lineage_published
  skill_aoa_session_donor_harvest -->|invocation_policy| policy_explicit_only
  skill_aoa_session_donor_harvest -->|depends_on| technique_AOA_T_0075
  skill_aoa_session_donor_harvest -->|depends_on| technique_AOA_T_0076
  skill_aoa_session_donor_harvest -->|depends_on| technique_AOA_T_0077
  skill_aoa_session_donor_harvest -->|included_in_profile| profile_repo_core_only
  skill_aoa_session_donor_harvest -->|included_in_profile| profile_repo_default
  skill_aoa_session_donor_harvest -->|included_in_profile| profile_repo_project_core_kernel
  skill_aoa_session_donor_harvest -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_session_donor_harvest -->|included_in_profile| profile_repo_session_donor_harvest_only
  skill_aoa_session_donor_harvest -->|included_in_profile| profile_repo_session_growth
  skill_aoa_session_donor_harvest -->|included_in_profile| profile_repo_session_harvest_family
  skill_aoa_session_donor_harvest -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_session_donor_harvest -->|included_in_profile| profile_user_curated_core
  skill_aoa_session_donor_harvest -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_session_donor_harvest -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_session_donor_harvest -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_session_donor_harvest -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_session_donor_harvest -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_session_progression_lift -->|maturity| status_evaluated
  skill_aoa_session_progression_lift -->|scope| scope_core
  skill_aoa_session_progression_lift -->|lineage| lineage_published
  skill_aoa_session_progression_lift -->|invocation_policy| policy_explicit_only
  skill_aoa_session_progression_lift -->|depends_on| technique_AOA_T_0084
  skill_aoa_session_progression_lift -->|depends_on| technique_AOA_T_0085
  skill_aoa_session_progression_lift -->|included_in_profile| profile_repo_core_only
  skill_aoa_session_progression_lift -->|included_in_profile| profile_repo_default
  skill_aoa_session_progression_lift -->|included_in_profile| profile_repo_project_core_kernel
  skill_aoa_session_progression_lift -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_session_progression_lift -->|included_in_profile| profile_repo_session_growth
  skill_aoa_session_progression_lift -->|included_in_profile| profile_repo_session_harvest_family
  skill_aoa_session_progression_lift -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_session_progression_lift -->|included_in_profile| profile_user_curated_core
  skill_aoa_session_progression_lift -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_session_progression_lift -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_session_progression_lift -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_session_progression_lift -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_session_progression_lift -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_session_route_forks -->|maturity| status_evaluated
  skill_aoa_session_route_forks -->|scope| scope_core
  skill_aoa_session_route_forks -->|lineage| lineage_published
  skill_aoa_session_route_forks -->|invocation_policy| policy_explicit_only
  skill_aoa_session_route_forks -->|depends_on| technique_AOA_T_0078
  skill_aoa_session_route_forks -->|depends_on| technique_AOA_T_0079
  skill_aoa_session_route_forks -->|included_in_profile| profile_repo_core_only
  skill_aoa_session_route_forks -->|included_in_profile| profile_repo_default
  skill_aoa_session_route_forks -->|included_in_profile| profile_repo_project_core_kernel
  skill_aoa_session_route_forks -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_session_route_forks -->|included_in_profile| profile_repo_session_growth
  skill_aoa_session_route_forks -->|included_in_profile| profile_repo_session_harvest_family
  skill_aoa_session_route_forks -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_session_route_forks -->|included_in_profile| profile_user_curated_core
  skill_aoa_session_route_forks -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_session_route_forks -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_session_route_forks -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_session_route_forks -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_session_route_forks -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_session_self_diagnose -->|maturity| status_evaluated
  skill_aoa_session_self_diagnose -->|scope| scope_core
  skill_aoa_session_self_diagnose -->|lineage| lineage_published
  skill_aoa_session_self_diagnose -->|invocation_policy| policy_explicit_only
  skill_aoa_session_self_diagnose -->|depends_on| technique_AOA_T_0080
  skill_aoa_session_self_diagnose -->|depends_on| technique_AOA_T_0081
  skill_aoa_session_self_diagnose -->|included_in_profile| profile_repo_core_only
  skill_aoa_session_self_diagnose -->|included_in_profile| profile_repo_default
  skill_aoa_session_self_diagnose -->|included_in_profile| profile_repo_project_core_kernel
  skill_aoa_session_self_diagnose -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_session_self_diagnose -->|included_in_profile| profile_repo_session_growth
  skill_aoa_session_self_diagnose -->|included_in_profile| profile_repo_session_harvest_family
  skill_aoa_session_self_diagnose -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_session_self_diagnose -->|included_in_profile| profile_user_curated_core
  skill_aoa_session_self_diagnose -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_session_self_diagnose -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_session_self_diagnose -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_session_self_diagnose -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_session_self_diagnose -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_session_self_repair -->|maturity| status_evaluated
  skill_aoa_session_self_repair -->|scope| scope_core
  skill_aoa_session_self_repair -->|lineage| lineage_published
  skill_aoa_session_self_repair -->|invocation_policy| policy_explicit_only
  skill_aoa_session_self_repair -->|depends_on| technique_AOA_T_0082
  skill_aoa_session_self_repair -->|depends_on| technique_AOA_T_0083
  skill_aoa_session_self_repair -->|included_in_profile| profile_repo_core_only
  skill_aoa_session_self_repair -->|included_in_profile| profile_repo_default
  skill_aoa_session_self_repair -->|included_in_profile| profile_repo_project_core_kernel
  skill_aoa_session_self_repair -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_session_self_repair -->|included_in_profile| profile_repo_session_growth
  skill_aoa_session_self_repair -->|included_in_profile| profile_repo_session_harvest_family
  skill_aoa_session_self_repair -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_session_self_repair -->|included_in_profile| profile_user_curated_core
  skill_aoa_session_self_repair -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_session_self_repair -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_session_self_repair -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_session_self_repair -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_session_self_repair -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_source_of_truth_check -->|maturity| status_canonical
  skill_aoa_source_of_truth_check -->|scope| scope_core
  skill_aoa_source_of_truth_check -->|lineage| lineage_published
  skill_aoa_source_of_truth_check -->|invocation_policy| policy_explicit_preferred
  skill_aoa_source_of_truth_check -->|depends_on| technique_AOA_T_0013
  skill_aoa_source_of_truth_check -->|depends_on| technique_AOA_T_0002
  skill_aoa_source_of_truth_check -->|depends_on| technique_AOA_T_0009
  skill_aoa_source_of_truth_check -->|included_in_profile| profile_repo_core_only
  skill_aoa_source_of_truth_check -->|included_in_profile| profile_repo_default
  skill_aoa_source_of_truth_check -->|included_in_profile| profile_repo_project_core_outer_ring
  skill_aoa_source_of_truth_check -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_source_of_truth_check -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_source_of_truth_check -->|included_in_profile| profile_user_curated_core
  skill_aoa_source_of_truth_check -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_source_of_truth_check -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_source_of_truth_check -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_source_of_truth_check -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_source_of_truth_check -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_summon -->|maturity| status_evaluated
  skill_aoa_summon -->|scope| scope_core
  skill_aoa_summon -->|lineage| lineage_published
  skill_aoa_summon -->|invocation_policy| policy_explicit_only
  skill_aoa_summon -->|depends_on| technique_AOA_T_0078
  skill_aoa_summon -->|depends_on| technique_AOA_T_0079
  skill_aoa_summon -->|depends_on| technique_AOA_T_0062
  skill_aoa_summon -->|depends_on| technique_AOA_T_0058
  skill_aoa_summon -->|included_in_profile| profile_repo_default
  skill_aoa_summon -->|included_in_profile| profile_repo_session_growth
  skill_aoa_summon -->|included_in_profile| profile_repo_summon_only
  skill_aoa_summon -->|included_in_profile| profile_user_aoa_foundation
  skill_aoa_summon -->|available_in_artifact_group| artifact_group_portable_export
  skill_aoa_summon -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_aoa_summon -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_aoa_summon -->|available_in_artifact_group| artifact_group_description_trigger
  skill_aoa_summon -->|available_in_artifact_group| artifact_group_tiny_router
  skill_aoa_tdd_slice -->|maturity| status_canonical
  skill_aoa_tdd_slice -->|scope| scope_core
  skill_aoa_tdd_slice -->|lineage| lineage_published
  skill_aoa_tdd_slice -->|invocation_policy| policy_explicit_preferred
  skill_aoa_tdd_slice -->|depends_on| technique_AOA_T_0014
  skill_aoa_tdd_slice -->|depends_on| technique_AOA_T_0001
  skill_aoa_tdd_slice -->|included_in_profile| profile_repo_core_only
  skill_aoa_tdd_slice -->|included_in_profile| profile_repo_default
  skill_aoa_tdd_slice -->|included_in_profile| profile_repo_project_core_outer_ring
  skill_aoa_tdd_slice -->|included_in_profile| profile_repo_project_foundation
  skill_aoa_tdd_slice -->|included_in_profile| profile_user_aoa_foundation
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
  skill_atm10_source_of_truth_check -->|depends_on| technique_AOA_T_0009
  skill_atm10_source_of_truth_check -->|included_in_profile| profile_repo_atm10_overlay
  skill_atm10_source_of_truth_check -->|included_in_profile| profile_repo_default
  skill_atm10_source_of_truth_check -->|available_in_artifact_group| artifact_group_portable_export
  skill_atm10_source_of_truth_check -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_atm10_source_of_truth_check -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_atm10_source_of_truth_check -->|available_in_artifact_group| artifact_group_description_trigger
  skill_atm10_source_of_truth_check -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_approval_ledger -->|maturity| status_scaffold
  skill_titan_approval_ledger -->|scope| scope_project
  skill_titan_approval_ledger -->|lineage| lineage_published
  skill_titan_approval_ledger -->|invocation_policy| policy_explicit_only
  skill_titan_approval_ledger -->|depends_on| technique_AOA_T_0028
  skill_titan_approval_ledger -->|depends_on| technique_AOA_T_0045
  skill_titan_approval_ledger -->|depends_on| technique_AOA_T_0058
  skill_titan_approval_ledger -->|included_in_profile| profile_repo_default
  skill_titan_approval_ledger -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_approval_ledger -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_approval_ledger -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_approval_ledger -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_approval_ledger -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_approval_ledger -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_approval_loom -->|maturity| status_scaffold
  skill_titan_approval_loom -->|scope| scope_project
  skill_titan_approval_loom -->|lineage| lineage_published
  skill_titan_approval_loom -->|invocation_policy| policy_explicit_only
  skill_titan_approval_loom -->|depends_on| technique_AOA_T_0028
  skill_titan_approval_loom -->|depends_on| technique_AOA_T_0045
  skill_titan_approval_loom -->|depends_on| technique_AOA_T_0062
  skill_titan_approval_loom -->|included_in_profile| profile_repo_default
  skill_titan_approval_loom -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_approval_loom -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_approval_loom -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_approval_loom -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_approval_loom -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_approval_loom -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_appserver_bridge -->|maturity| status_scaffold
  skill_titan_appserver_bridge -->|scope| scope_project
  skill_titan_appserver_bridge -->|lineage| lineage_published
  skill_titan_appserver_bridge -->|invocation_policy| policy_explicit_only
  skill_titan_appserver_bridge -->|depends_on| technique_AOA_T_0045
  skill_titan_appserver_bridge -->|depends_on| technique_AOA_T_0066
  skill_titan_appserver_bridge -->|depends_on| technique_AOA_T_0043
  skill_titan_appserver_bridge -->|included_in_profile| profile_repo_default
  skill_titan_appserver_bridge -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_appserver_bridge -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_appserver_bridge -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_appserver_bridge -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_appserver_bridge -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_appserver_bridge -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_appserver_plan -->|maturity| status_scaffold
  skill_titan_appserver_plan -->|scope| scope_project
  skill_titan_appserver_plan -->|lineage| lineage_published
  skill_titan_appserver_plan -->|invocation_policy| policy_explicit_only
  skill_titan_appserver_plan -->|depends_on| technique_AOA_T_0004
  skill_titan_appserver_plan -->|depends_on| technique_AOA_T_0091
  skill_titan_appserver_plan -->|depends_on| technique_AOA_T_0045
  skill_titan_appserver_plan -->|included_in_profile| profile_repo_default
  skill_titan_appserver_plan -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_appserver_plan -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_appserver_plan -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_appserver_plan -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_appserver_plan -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_appserver_plan -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_closeout -->|maturity| status_scaffold
  skill_titan_closeout -->|scope| scope_project
  skill_titan_closeout -->|lineage| lineage_published
  skill_titan_closeout -->|invocation_policy| policy_explicit_only
  skill_titan_closeout -->|depends_on| technique_AOA_T_0058
  skill_titan_closeout -->|depends_on| technique_AOA_T_0076
  skill_titan_closeout -->|depends_on| technique_AOA_T_0045
  skill_titan_closeout -->|included_in_profile| profile_repo_default
  skill_titan_closeout -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_closeout -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_closeout -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_closeout -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_closeout -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_closeout -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_console -->|maturity| status_scaffold
  skill_titan_console -->|scope| scope_project
  skill_titan_console -->|lineage| lineage_published
  skill_titan_console -->|invocation_policy| policy_explicit_only
  skill_titan_console -->|depends_on| technique_AOA_T_0045
  skill_titan_console -->|depends_on| technique_AOA_T_0062
  skill_titan_console -->|depends_on| technique_AOA_T_0028
  skill_titan_console -->|included_in_profile| profile_repo_default
  skill_titan_console -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_console -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_console -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_console -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_console -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_console -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_event_replay -->|maturity| status_scaffold
  skill_titan_event_replay -->|scope| scope_project
  skill_titan_event_replay -->|lineage| lineage_published
  skill_titan_event_replay -->|invocation_policy| policy_explicit_only
  skill_titan_event_replay -->|depends_on| technique_AOA_T_0066
  skill_titan_event_replay -->|depends_on| technique_AOA_T_0045
  skill_titan_event_replay -->|depends_on| technique_AOA_T_0043
  skill_titan_event_replay -->|included_in_profile| profile_repo_default
  skill_titan_event_replay -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_event_replay -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_event_replay -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_event_replay -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_event_replay -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_event_replay -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_memory_loom -->|maturity| status_scaffold
  skill_titan_memory_loom -->|scope| scope_project
  skill_titan_memory_loom -->|lineage| lineage_published
  skill_titan_memory_loom -->|invocation_policy| policy_explicit_only
  skill_titan_memory_loom -->|depends_on| technique_AOA_T_0053
  skill_titan_memory_loom -->|depends_on| technique_AOA_T_0043
  skill_titan_memory_loom -->|depends_on| technique_AOA_T_0045
  skill_titan_memory_loom -->|included_in_profile| profile_repo_default
  skill_titan_memory_loom -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_memory_loom -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_memory_loom -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_memory_loom -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_memory_loom -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_memory_loom -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_memory_prune -->|maturity| status_scaffold
  skill_titan_memory_prune -->|scope| scope_project
  skill_titan_memory_prune -->|lineage| lineage_published
  skill_titan_memory_prune -->|invocation_policy| policy_explicit_only
  skill_titan_memory_prune -->|depends_on| technique_AOA_T_0103
  skill_titan_memory_prune -->|depends_on| technique_AOA_T_0104
  skill_titan_memory_prune -->|depends_on| technique_AOA_T_0043
  skill_titan_memory_prune -->|included_in_profile| profile_repo_default
  skill_titan_memory_prune -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_memory_prune -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_memory_prune -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_memory_prune -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_memory_prune -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_memory_prune -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_mutation_gate -->|maturity| status_scaffold
  skill_titan_mutation_gate -->|scope| scope_project
  skill_titan_mutation_gate -->|lineage| lineage_published
  skill_titan_mutation_gate -->|invocation_policy| policy_explicit_only
  skill_titan_mutation_gate -->|depends_on| technique_AOA_T_0028
  skill_titan_mutation_gate -->|depends_on| technique_AOA_T_0004
  skill_titan_mutation_gate -->|depends_on| technique_AOA_T_0091
  skill_titan_mutation_gate -->|included_in_profile| profile_repo_default
  skill_titan_mutation_gate -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_mutation_gate -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_mutation_gate -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_mutation_gate -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_mutation_gate -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_mutation_gate -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_recall -->|maturity| status_scaffold
  skill_titan_recall -->|scope| scope_project
  skill_titan_recall -->|lineage| lineage_published
  skill_titan_recall -->|invocation_policy| policy_explicit_only
  skill_titan_recall -->|depends_on| technique_AOA_T_0053
  skill_titan_recall -->|depends_on| technique_AOA_T_0043
  skill_titan_recall -->|depends_on| technique_AOA_T_0045
  skill_titan_recall -->|included_in_profile| profile_repo_default
  skill_titan_recall -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_recall -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_recall -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_recall -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_recall -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_recall -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_receipt -->|maturity| status_scaffold
  skill_titan_receipt -->|scope| scope_project
  skill_titan_receipt -->|lineage| lineage_published
  skill_titan_receipt -->|invocation_policy| policy_explicit_only
  skill_titan_receipt -->|depends_on| technique_AOA_T_0058
  skill_titan_receipt -->|depends_on| technique_AOA_T_0045
  skill_titan_receipt -->|depends_on| technique_AOA_T_0043
  skill_titan_receipt -->|included_in_profile| profile_repo_default
  skill_titan_receipt -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_receipt -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_receipt -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_receipt -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_receipt -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_receipt -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_runtime_gate -->|maturity| status_scaffold
  skill_titan_runtime_gate -->|scope| scope_project
  skill_titan_runtime_gate -->|lineage| lineage_published
  skill_titan_runtime_gate -->|invocation_policy| policy_explicit_only
  skill_titan_runtime_gate -->|depends_on| technique_AOA_T_0028
  skill_titan_runtime_gate -->|depends_on| technique_AOA_T_0058
  skill_titan_runtime_gate -->|depends_on| technique_AOA_T_0091
  skill_titan_runtime_gate -->|included_in_profile| profile_repo_default
  skill_titan_runtime_gate -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_runtime_gate -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_runtime_gate -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_runtime_gate -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_runtime_gate -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_runtime_gate -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_summon -->|maturity| status_scaffold
  skill_titan_summon -->|scope| scope_project
  skill_titan_summon -->|lineage| lineage_published
  skill_titan_summon -->|invocation_policy| policy_explicit_only
  skill_titan_summon -->|depends_on| technique_AOA_T_0060
  skill_titan_summon -->|depends_on| technique_AOA_T_0058
  skill_titan_summon -->|depends_on| technique_AOA_T_0028
  skill_titan_summon -->|included_in_profile| profile_repo_default
  skill_titan_summon -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_summon -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_summon -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_summon -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_summon -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_summon -->|available_in_artifact_group| artifact_group_tiny_router
  skill_titan_thread_turn_binding -->|maturity| status_scaffold
  skill_titan_thread_turn_binding -->|scope| scope_project
  skill_titan_thread_turn_binding -->|lineage| lineage_published
  skill_titan_thread_turn_binding -->|invocation_policy| policy_explicit_only
  skill_titan_thread_turn_binding -->|depends_on| technique_AOA_T_0062
  skill_titan_thread_turn_binding -->|depends_on| technique_AOA_T_0066
  skill_titan_thread_turn_binding -->|depends_on| technique_AOA_T_0045
  skill_titan_thread_turn_binding -->|included_in_profile| profile_repo_default
  skill_titan_thread_turn_binding -->|included_in_profile| profile_repo_titan_overlay
  skill_titan_thread_turn_binding -->|available_in_artifact_group| artifact_group_portable_export
  skill_titan_thread_turn_binding -->|available_in_artifact_group| artifact_group_runtime_seam
  skill_titan_thread_turn_binding -->|available_in_artifact_group| artifact_group_runtime_guardrails
  skill_titan_thread_turn_binding -->|available_in_artifact_group| artifact_group_description_trigger
  skill_titan_thread_turn_binding -->|available_in_artifact_group| artifact_group_tiny_router
```

| name | status | scope | invocation | lineage | profiles | artifact groups | techniques |
|---|---|---|---|---|---|---|---|
| abyss-safe-infra-change | evaluated | project | explicit-only | published | repo-abyss-overlay, repo-default | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0028, AOA-T-0001 |
| abyss-sanitized-share | evaluated | project | explicit-only | published | repo-abyss-overlay, repo-default | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0034, AOA-T-0002 |
| abyss-self-diagnostic-spine | scaffold | project | explicit-preferred | published | repo-abyss-overlay, repo-default | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0080, AOA-T-0081 |
| aoa-adr-write | canonical | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-outer-ring, repo-project-foundation, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0033, AOA-T-0002 |
| aoa-approval-gate-check | canonical | risk | explicit-only | published | repo-default, repo-project-foundation, repo-project-risk-guard-ring, repo-risk-explicit, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0028 |
| aoa-automation-opportunity-scan | evaluated | core | explicit-only | published | repo-automation-opportunity-scan-only, repo-core-only, repo-default, repo-project-core-kernel, repo-project-foundation, repo-session-growth, repo-session-harvest-family, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0086, AOA-T-0087, AOA-T-0088 |
| aoa-bounded-context-map | canonical | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-outer-ring, repo-project-foundation, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0016, AOA-T-0002 |
| aoa-change-protocol | canonical | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-outer-ring, repo-project-foundation, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0001, AOA-T-0002 |
| aoa-checkpoint-closeout-bridge | evaluated | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-kernel, repo-project-foundation, repo-session-growth, repo-session-harvest-family, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0075, AOA-T-0084, AOA-T-0089 |
| aoa-commit-growth-seam | evaluated | core | explicit-only | published | repo-default, repo-session-growth, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0001, AOA-T-0028 |
| aoa-contract-test | canonical | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-outer-ring, repo-project-foundation, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0003, AOA-T-0015 |
| aoa-core-logic-boundary | evaluated | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-outer-ring, repo-project-foundation, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0016, AOA-T-0015 |
| aoa-decision | evaluated | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-outer-ring, repo-project-foundation, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0033, AOA-T-0002 |
| aoa-decision-correct | evaluated | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-outer-ring, repo-project-foundation, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0001, AOA-T-0033, AOA-T-0002 |
| aoa-decision-create | evaluated | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-outer-ring, repo-project-foundation, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0033, AOA-T-0002 |
| aoa-decision-find | evaluated | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-outer-ring, repo-project-foundation, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0002 |
| aoa-dry-run-first | canonical | risk | explicit-only | published | repo-default, repo-project-foundation, repo-project-risk-guard-ring, repo-risk-explicit, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, support_resources, tiny_router | AOA-T-0004, AOA-T-0028 |
| aoa-eval | scaffold | core | explicit-preferred | published | repo-default, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0003, AOA-T-0076, AOA-T-0094 |
| aoa-eval-apply | scaffold | core | explicit-preferred | published | repo-default, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0003, AOA-T-0007, AOA-T-0096 |
| aoa-eval-design | scaffold | core | explicit-preferred | published | repo-default, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0015, AOA-T-0017, AOA-T-0007 |
| aoa-eval-local-need | scaffold | core | explicit-preferred | published | repo-default, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0076, AOA-T-0094, AOA-T-0105 |
| aoa-eval-select | scaffold | core | explicit-preferred | published | repo-default, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0003, AOA-T-0076, AOA-T-0094 |
| aoa-eval-session-mining | scaffold | core | explicit-preferred | published | repo-default, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0075, AOA-T-0067, AOA-T-0081 |
| aoa-invariant-coverage-audit | canonical | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-outer-ring, repo-project-foundation, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0017 |
| aoa-local-stack-bringup | evaluated | risk | explicit-only | published | repo-default, repo-project-foundation, repo-project-risk-guard-ring, repo-risk-explicit, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, support_resources, tiny_router | AOA-T-0036, AOA-T-0037, AOA-T-0028, AOA-T-0038 |
| aoa-memo-writeback | scaffold | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-kernel, repo-project-foundation, repo-session-growth, repo-session-harvest-family, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0026, AOA-T-0106, AOA-T-0076 |
| aoa-port-adapter-refactor | evaluated | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-outer-ring, repo-project-foundation, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0016, AOA-T-0015 |
| aoa-property-invariants | canonical | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-outer-ring, repo-project-foundation, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0017, AOA-T-0007 |
| aoa-quest-harvest | evaluated | core | explicit-only | published | repo-core-only, repo-default, repo-project-core-kernel, repo-project-foundation, repo-quest-harvest-only, repo-session-growth, repo-session-harvest-family, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0089, AOA-T-0090 |
| aoa-safe-infra-change | canonical | risk | explicit-only | published | repo-default, repo-project-foundation, repo-project-risk-guard-ring, repo-risk-explicit, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, support_resources, tiny_router | AOA-T-0028, AOA-T-0001 |
| aoa-sanitized-share | canonical | risk | explicit-only | published | repo-default, repo-project-foundation, repo-project-risk-guard-ring, repo-risk-explicit, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0034, AOA-T-0002 |
| aoa-session-donor-harvest | evaluated | core | explicit-only | published | repo-core-only, repo-default, repo-project-core-kernel, repo-project-foundation, repo-session-donor-harvest-only, repo-session-growth, repo-session-harvest-family, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0075, AOA-T-0076, AOA-T-0077 |
| aoa-session-progression-lift | evaluated | core | explicit-only | published | repo-core-only, repo-default, repo-project-core-kernel, repo-project-foundation, repo-session-growth, repo-session-harvest-family, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0084, AOA-T-0085 |
| aoa-session-route-forks | evaluated | core | explicit-only | published | repo-core-only, repo-default, repo-project-core-kernel, repo-project-foundation, repo-session-growth, repo-session-harvest-family, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0078, AOA-T-0079 |
| aoa-session-self-diagnose | evaluated | core | explicit-only | published | repo-core-only, repo-default, repo-project-core-kernel, repo-project-foundation, repo-session-growth, repo-session-harvest-family, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0080, AOA-T-0081 |
| aoa-session-self-repair | evaluated | core | explicit-only | published | repo-core-only, repo-default, repo-project-core-kernel, repo-project-foundation, repo-session-growth, repo-session-harvest-family, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0082, AOA-T-0083 |
| aoa-source-of-truth-check | canonical | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-outer-ring, repo-project-foundation, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0013, AOA-T-0002, AOA-T-0009 |
| aoa-summon | evaluated | core | explicit-only | published | repo-default, repo-session-growth, repo-summon-only, user-aoa-foundation | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0078, AOA-T-0079, AOA-T-0062, AOA-T-0058 |
| aoa-tdd-slice | canonical | core | explicit-preferred | published | repo-core-only, repo-default, repo-project-core-outer-ring, repo-project-foundation, user-aoa-foundation, user-curated-core | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0014, AOA-T-0001 |
| atm10-change-protocol | evaluated | project | explicit-preferred | published | repo-atm10-overlay, repo-default | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0001, AOA-T-0002 |
| atm10-source-of-truth-check | evaluated | project | explicit-preferred | published | repo-atm10-overlay, repo-default | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0013, AOA-T-0002, AOA-T-0009 |
| titan-approval-ledger | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0028, AOA-T-0045, AOA-T-0058 |
| titan-approval-loom | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0028, AOA-T-0045, AOA-T-0062 |
| titan-appserver-bridge | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0045, AOA-T-0066, AOA-T-0043 |
| titan-appserver-plan | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0004, AOA-T-0091, AOA-T-0045 |
| titan-closeout | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0058, AOA-T-0076, AOA-T-0045 |
| titan-console | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0045, AOA-T-0062, AOA-T-0028 |
| titan-event-replay | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0066, AOA-T-0045, AOA-T-0043 |
| titan-memory-loom | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0053, AOA-T-0043, AOA-T-0045 |
| titan-memory-prune | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0103, AOA-T-0104, AOA-T-0043 |
| titan-mutation-gate | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0028, AOA-T-0004, AOA-T-0091 |
| titan-recall | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0053, AOA-T-0043, AOA-T-0045 |
| titan-receipt | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0058, AOA-T-0045, AOA-T-0043 |
| titan-runtime-gate | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0028, AOA-T-0058, AOA-T-0091 |
| titan-summon | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0060, AOA-T-0058, AOA-T-0028 |
| titan-thread-turn-binding | scaffold | project | explicit-only | published | repo-default, repo-titan-overlay | portable_export, runtime_seam, runtime_guardrails, description_trigger, tiny_router | AOA-T-0062, AOA-T-0066, AOA-T-0045 |

