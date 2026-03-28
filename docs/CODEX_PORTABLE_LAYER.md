# Codex portable layer for aoa-skills

This document defines the portable Agent Skills layer that makes `aoa-skills` directly discoverable by Codex under `.agents/skills/`.

## Intent

The target shape is:

- canonical AoA authoring remains in `skills/*/SKILL.md` plus generated AoA catalogs
- Codex-facing export lives in `.agents/skills/*`
- local-friendly runtimes wrap or mirror the Codex-facing export rather than replacing it

## Source surfaces

The builder reads:

- `generated/skill_sections.full.json`
- `generated/skill_catalog.min.json`
- `config/portable_skill_overrides.json`
- optional `config/openai_skill_extensions.json`
- `config/skill_pack_profiles.json`
- `config/skill_policy_matrix.json`
- `config/description_trigger_eval_policy.json`

These files supply the current instruction body, scope, status, invocation mode,
technique dependencies, trigger descriptions, optional OpenAI-facing metadata,
install posture, and trust posture for each AoA skill.

## Mapping rules

### SKILL.md frontmatter

Portable `SKILL.md` files use standard Agent Skills frontmatter:

- `name`: identical to the AoA skill directory name
- `description`: curated Codex trigger text describing what the skill does and when to use it
- `license`: `Apache-2.0`
- `compatibility`: generic compatibility note for Codex or similar coding agents
- `metadata`: AoA-specific fields moved under namespaced keys

### AoA metadata mapping

- `scope` -> `metadata.aoa_scope`
- `status` -> `metadata.aoa_status`
- `invocation_mode` -> `metadata.aoa_invocation_mode`
- `skill_path` -> `metadata.aoa_source_skill_path`
- `technique_dependencies[]` -> `metadata.aoa_technique_dependencies` as a comma-separated string
- source repo marker -> `metadata.aoa_source_repo`
- portable export profile marker -> `metadata.aoa_portable_profile`

### Invocation policy and UI metadata

The portable layer mirrors AoA invocation mode in `agents/openai.yaml`:

- `explicit-only` -> `policy.allow_implicit_invocation: false`
- `explicit-preferred` -> `policy.allow_implicit_invocation: true`

Wave 3 also fills in:

- `interface.icon_small`
- `interface.icon_large`
- `interface.brand_color`

That keeps risk posture canonical while making the export more native in selector UIs.

## Support artifacts around the export

Wave 3 adds generated support layers that remain subordinate to the export:

- `generated/agent_skill_catalog*.json`
- `generated/portable_export_map.json`
- `generated/local_adapter_manifest*.json`
- `generated/skill_handoff_contracts.json`
- `generated/context_retention_manifest.json`
- `generated/trust_policy_matrix.json`
- `generated/skill_runtime_contracts.json`
- `generated/skill_pack_profiles.resolved.json`
- `generated/codex_config_snippets.json`
- `generated/mcp_dependency_manifest.json`
- `generated/release_manifest.json`

These surfaces make installation, local adaptation, trust checks, and context retention easier without becoming a new authoring layer.
`generated/skill_handoff_contracts.json` is the only wave-5 bridge kept in `aoa-skills`: it remains skill-derived and exists so downstream playbook layers can consume compact per-skill handoff contracts without moving scenario composition back into this repository.

Wave 4 adds a second-path dedicated-tool runtime seam around the same export:

- `generated/runtime_discovery_index*.json`
- `generated/runtime_disclosure_index.json`
- `generated/runtime_activation_aliases.json`
- `generated/runtime_tool_schemas.json`
- `generated/runtime_session_contract.json`
- `generated/runtime_prompt_blocks.json`
- `generated/runtime_router_hints.json`
- `generated/runtime_seam_manifest.json`

Those runtime files still sit downstream of `.agents/skills/*` and do not introduce a second authoring format.

Wave 6 adds a governed runtime layer above the raw seam:

- `generated/repo_trust_gate_manifest.json`
- `generated/permission_allowlist_manifest.json`
- `generated/skill_context_guard_manifest.json`
- `generated/runtime_guardrail_tool_schemas.json`
- `generated/runtime_guardrail_prompt_blocks.json`
- `generated/runtime_guardrail_manifest.json`

Those guardrail files keep trust, allowlists, and compaction-safe reuse repo-owned and still subordinate to the same export.

Wave 7 adds an activation-quality layer above the same export:

- `generated/skill_description_signals.json`
- `generated/description_trigger_eval_cases.jsonl`
- `generated/description_trigger_eval_cases.csv`
- `generated/description_trigger_eval_manifest.json`
- `generated/skills_ref_validation_manifest.json`

Those files make description quality and open-surface conformance testable without introducing a second authoring format or a second release identity.

Wave 8 adds a deterministic support-resource bridge for three high-risk skills:

- `generated/deterministic_resource_manifest.json`
- `generated/support_resource_index.json`
- `generated/structured_output_schema_index.json`
- `generated/support_resource_bridge_map.json`
- `generated/deterministic_resource_eval_cases.jsonl`
- `generated/expected_existing_aoa_support_dirs.json`

Wave 9 adds a tiny-router compression bridge for downstream two-stage routing:

- `generated/tiny_router_skill_signals.json`
- `generated/tiny_router_candidate_bands.json`
- `generated/tiny_router_capsules.min.json`
- `generated/tiny_router_eval_cases.jsonl`
- `generated/tiny_router_overlay_manifest.json`

These files remain skill-derived compression surfaces only. They are not routing
policy authority and they must not turn `aoa-skills` into a second router canon.

Those files describe canonical `skills/*/{scripts,references,assets}` resources and their bridge back to existing AoA support dirs.
The portable export still stays generated from canonical skill roots; `scripts/build_support_resources.py` records the support layer, but it does not become a second portable-sync authority.

## Build and validation

Rebuild the portable layer from repo root:

    python scripts/build_agent_skills.py --repo-root .

Validate the result:

    python scripts/validate_agent_skills.py --repo-root .

Lint the policy-aware trigger dataset:

    python scripts/lint_trigger_evals.py --repo-root .

Lint pack-profile authoring:

    python scripts/lint_pack_profiles.py --repo-root .

Build the wave-4 runtime seam:

    python scripts/build_runtime_seam.py --repo-root .

Build the wave-6 runtime guardrails:

    python scripts/build_runtime_guardrails.py --repo-root .

Build the wave-7 description-trigger suite:

    python scripts/build_description_trigger_evals.py --repo-root .

Build the wave-8 support-resource manifests:

    python scripts/build_support_resources.py --repo-root .

Lint the wave-7 description-trigger suite:

    python scripts/lint_description_trigger_evals.py --repo-root .

Validate the wave-8 support-resource bridge:

    python scripts/validate_support_resources.py --repo-root . --check-portable

Lint the wave-8 support-resource bridge:

    python scripts/lint_support_resources.py --repo-root .

Run the soft standards-conformance wrapper:

    python scripts/run_skills_ref_validation.py --repo-root .

Inspect one activated raw runtime-seam payload:

    python scripts/skill_runtime_seam.py activate --repo-root . --skill aoa-change-protocol --format json

Inspect one activated governed runtime payload:

    python scripts/skill_runtime_guardrails.py activate --repo-root . --skill aoa-change-protocol --trust-store .aoa/repo-trust-store.json --format json

Inspect one activated local-adapter compatibility payload:

    python scripts/activate_skill.py --repo-root . --skill aoa-change-protocol --format json

## Future local-friendly path

The Codex-facing layer is the common portable surface. Local runtimes should adapt around it by:

- reading `generated/agent_skill_catalog*.json` for discovery
- using `generated/runtime_discovery_index*.json` and `generated/runtime_disclosure_index.json` for shortlist and preview
- using `scripts/skill_runtime_guardrails.py` as the default runtime path for trust-gated discover, disclose, activate, allowlist, compact, and rehydrate
- using `scripts/skill_runtime_seam.py` only as the raw/debug seam
- respecting `policy.allow_implicit_invocation`
- preserving AoA metadata from frontmatter `metadata`
- consulting runtime/context/trust contracts instead of inventing a second local format
- treating `scripts/activate_skill.py` as the legacy compatibility shim for older local wrappers
