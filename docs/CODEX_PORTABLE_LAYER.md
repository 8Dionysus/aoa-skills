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

Inspect one activated runtime-seam payload:

    python scripts/skill_runtime_seam.py activate --repo-root . --skill aoa-change-protocol --format json

Inspect one activated local-adapter compatibility payload:

    python scripts/activate_skill.py --repo-root . --skill aoa-change-protocol --format json

## Future local-friendly path

The Codex-facing layer is the common portable surface. Local runtimes should adapt around it by:

- reading `generated/agent_skill_catalog*.json` for discovery
- using `generated/runtime_discovery_index*.json` and `generated/runtime_disclosure_index.json` for shortlist and preview
- using `scripts/skill_runtime_seam.py activate` for full runtime activation
- respecting `policy.allow_implicit_invocation`
- preserving AoA metadata from frontmatter `metadata`
- consulting runtime/context/trust contracts instead of inventing a second local format
- treating `scripts/activate_skill.py` as the legacy compatibility shim for older local wrappers
