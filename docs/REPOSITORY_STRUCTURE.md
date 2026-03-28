# Repository structure

## Top level

- `README.md` — project entry point
- `SKILL_INDEX.md` — public map of current skills and their maturity
- `docs/` — architecture, bridge rules, roadmap, conventions
- `docs/RUNTIME_PATH.md` — main runtime guide for `pick -> inspect -> expand -> object use`
- `docs/PUBLIC_SURFACE.md` — public guide to the current governance and product-signaling layer
- `docs/PROMOTION_PATH.md` — public repository convention for maturity transitions
- `docs/OVERLAY_SPEC.md` — repo-local contract for thin project overlays and stub-only downstream adaptation
- `docs/reviews/` — public review records for candidate and promotion work
- `docs/reviews/canonical-candidates/` — canonical-candidate review records
- `docs/reviews/status-promotions/` — review records for non-canonical promotion steps
- `templates/` — templates for authoring skills and related files
- `templates/RUNTIME_EXAMPLE.template.md` — canonical runtime example scaffold
- `templates/PROJECT_OVERLAY.template.md` — canonical project overlay scaffold
- `templates/PROJECT_OVERLAY_SKILL.template.md` — canonical overlayed skill scaffold
- `.agents/` — generated Codex-facing export layer
- `config/` — portable export description overrides, optional OpenAI metadata extensions, and wave-3 pack/trust authoring inputs
- `examples/` — sample Codex config snippets for profile disable and install scenarios
- `skills/` — skill bundles
- `generated/` — derived reader catalogs plus portable export discovery, local-adapter manifests, wave-3 support manifests, wave-4 runtime seam surfaces, wave-8 support-resource manifests, and trigger-eval seed data
- `scripts/` — optional generation or validation helpers
- `schemas/` — optional machine-readable schemas

## Skill bundle shape

Each skill lives in:

`skills/<skill-name>/`

Recommended contents:

- `SKILL.md` — main Codex-facing runtime skill document
- `techniques.yaml` — bridge manifest that records which techniques shape the skill
- `agents/openai.yaml` — optional invocation and policy settings
- `references/` — optional reference docs or excerpts
- `scripts/` — optional deterministic helper utilities for skill-owned support bundles
- `assets/` — optional structured templates or schemas for skill-owned support bundles
- `examples/` — optional runtime examples or bounded mini scenarios
- `checks/` — optional review checklist or validation notes, with `checks/review.md` as the canonical checklist path

## Initial naming convention

Use one of these prefixes:
- `aoa-` for public core skills
- `atm10-` for project-family skills around `atm10-agent`
- `abyss-` for project-family skills around `abyss-stack`

Examples:
- `aoa-change-protocol`
- `aoa-tdd-slice`
- `aoa-contract-test`
- `atm10-perception-tests`
- `abyss-port-exposure-guard`

## Files that belong in the skill

Belong in `SKILL.md`:
- intent for the agent
- trigger boundary
- expected inputs
- expected outputs
- concrete step-by-step procedure
- explicit anti-patterns
- done criteria or verification guidance

Belong in `techniques.yaml`:
- upstream technique IDs
- source paths and pinned source refs
- selected sections
- composition notes

Belong in `generated/skill_catalog*.json`:
- derived routing and reader surfaces
- deterministic projections of committed `SKILL.md` and `techniques.yaml`
- no new authority beyond the source files

Belong in `.agents/skills/*`:
- generated Codex-facing skill export files
- frontmatter and `agents/openai.yaml` derived from canonical skills plus portable export config
- no new authority beyond the source files and portable export config

Belong in `generated/skill_walkthroughs.json` and `generated/skill_walkthroughs.md`:
- derived runtime inspect surfaces
- support-artifact aware entry points for `pick -> inspect -> expand -> object use`
- no new authority beyond committed `SKILL.md`, local support artifacts, and public review records

Belong in `generated/public_surface.json` and `generated/public_surface.md`:
- derived governance and public-product signaling
- cohort views such as default references, candidate-ready skills, and pending-lineage blockers
- no status change authority beyond the source files, review records, and evaluation fixtures

Belong in `generated/agent_skill_catalog*.json`, `generated/portable_export_map.json`, `generated/local_adapter_manifest*.json`, `generated/context_retention_manifest.json`, `generated/trust_policy_matrix.json`, `generated/skill_runtime_contracts.json`, `generated/skill_pack_profiles.resolved.json`, `generated/codex_config_snippets.json`, `generated/mcp_dependency_manifest.json`, `generated/runtime_discovery_index*.json`, `generated/runtime_disclosure_index.json`, `generated/runtime_activation_aliases.json`, `generated/runtime_tool_schemas.json`, `generated/runtime_session_contract.json`, `generated/runtime_prompt_blocks.json`, `generated/runtime_router_hints.json`, `generated/runtime_seam_manifest.json`, `generated/deterministic_resource_manifest.json`, `generated/support_resource_index.json`, `generated/structured_output_schema_index.json`, `generated/support_resource_bridge_map.json`, `generated/expected_existing_aoa_support_dirs.json`, and `generated/release_manifest.json`:
- portable discovery, activation, install, and trust surfaces
- deterministic projections of `.agents/skills/*`, canonical invocation policy, and repo-owned portable-layer config
- no new authority beyond source bundles and portable export config

Belong in `agents/openai.yaml`:
- invocation mode
- policy
- future Codex-specific metadata

Belong in `docs/reviews/`:
- candidate review records
- promotion review records
- public evidence notes about repository-level review decisions
- explicit notes about whether machine floors pass, whether skill meaning changed, and what blocks the next status step

## What should not live here

- private secrets
- environment-specific sensitive paths
- one-off hacks that were not generalized
- techniques that should live in `aoa-techniques`
- project runtime state or logs

## Local-only surfaces

- `TODO.local.md` and `PLANS.local.md` are clone-local planning notes and stay gitignored
- `seeds/` is a clone-local scratch area for seed files and stays gitignored
