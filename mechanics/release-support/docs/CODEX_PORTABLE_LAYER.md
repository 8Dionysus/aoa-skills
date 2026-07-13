# Codex portable layer for aoa-skills

This document defines the portable Agent Skills layer that makes `aoa-skills` directly discoverable by Codex under `.agents/skills/`.

## Intent

The target shape is:

- canonical AoA authoring remains in `skills/**/SKILL.md` plus generated AoA catalogs
- adapter export lives in `.agents/skills/*`
- local-friendly runtimes wrap or mirror the adapter export rather than replacing it

When repeated drift or stale generated surfaces show up around that export, use
`mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md` as the owner refresh route. That law stays
subordinate to the same source-authored skill bundles and repo-owned config
described here.

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
technique dependencies, trigger descriptions, optional adapter metadata,
install posture, and trust posture for each AoA skill.

## Mapping rules

### SKILL.md frontmatter

Portable `SKILL.md` files use standard Agent Skills frontmatter:

- `name`: identical to the AoA skill directory name
- `description`: curated trigger text describing what the skill does and when to use it
- `license`: `Apache-2.0`
- `compatibility`: generic compatibility note for local coding agents
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

The portable layer mirrors explicit implicit-activation policy in `agents/openai.yaml`:

- `invoke` -> `policy.allow_implicit_invocation: true`
- `suggest` -> `policy.allow_implicit_invocation: false`
- `manual` -> `policy.allow_implicit_invocation: false`

The adapter metadata also fills in:

- `interface.icon_small`
- `interface.icon_large`
- `interface.brand_color`

That keeps risk posture canonical while making the export more native in selector UIs.

## Support artifacts around the export

Generated support layers remain subordinate to the export:

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

These surfaces make installation, local adaptation, trust checks, and context
retention easier without becoming a new authoring layer.

- `generated/skill_handoff_contracts.json` remains skill-derived so downstream
  playbook layers can consume compact per-skill handoff contracts.
- `generated/release_manifest.json` is the packaging-facing contract for this
  export stack; it is not a second release ledger.
- `scripts/stage_skill_pack.py` materializes one profile-scoped bundle with a
  bundle-local `bundle_manifest.json` and a human-facing `README.md`.
- the staging owner's `--archive-path` option adds an optional ZIP transport
  wrapper over the same staged directory.
- `scripts/inspect_skill_pack.py` checks manifest integrity, staged file
  digests, bundle digest, and archive layout before an install step.
- `scripts/import_skill_pack.py` inspects first, then optionally installs and
  verifies one staged bundle or ZIP handoff as one repo-local flow.
- `scripts/install_skill_pack.py` and `scripts/verify_skill_pack.py` remain the
  lower-level advanced path when install and verification need to stay separate.
`scripts/audit/audit_workspace_skill_adoption.py` is the read-only workspace pass over
the same profile verification contract: it checks root and repo install
surfaces before rollout, but it does not install, approve, or accept skills for
downstream owners.

The dedicated-tool runtime seam adds these generated surfaces around the same export:

- `generated/runtime_discovery_index*.json`
- `generated/runtime_disclosure_index.json`
- `generated/runtime_activation_aliases.json`
- `generated/runtime_tool_schemas.json`
- `generated/runtime_session_contract.json`
- `generated/runtime_prompt_blocks.json`
- `generated/runtime_router_hints.json`
- `generated/runtime_seam_manifest.json`

Those runtime files still sit downstream of `.agents/skills/*` and do not introduce a second authoring format.

The governed runtime layer adds:

- `generated/repo_trust_gate_manifest.json`
- `generated/permission_allowlist_manifest.json`
- `generated/skill_context_guard_manifest.json`
- `generated/runtime_guardrail_tool_schemas.json`
- `generated/runtime_guardrail_prompt_blocks.json`
- `generated/runtime_guardrail_manifest.json`

Those guardrail files keep trust, allowlists, and compaction-safe reuse repo-owned and still subordinate to the same export.

The activation-quality layer adds:

- `generated/skill_description_signals.json`
- `generated/description_trigger_eval_cases.jsonl`
- `generated/description_trigger_eval_cases.csv`
- `generated/description_trigger_eval_manifest.json`
- `generated/skills_ref_validation_manifest.json`

Those files make description quality and open-surface conformance testable without introducing a second authoring format or a second release identity.

The deterministic support-resource bridge adds:

- `generated/deterministic_resource_manifest.json`
- `generated/support_resource_index.json`
- `generated/structured_output_schema_index.json`
- `generated/support_resource_bridge_map.json`
- `generated/deterministic_resource_eval_cases.jsonl`
- `generated/expected_existing_aoa_support_dirs.json`

The tiny-router compression bridge adds:

- `generated/tiny_router_skill_signals.json`
- `generated/tiny_router_candidate_bands.json`
- `generated/tiny_router_capsules.min.json`
- `generated/tiny_router_eval_cases.jsonl`
- `generated/tiny_router_overlay_manifest.json`

These files remain skill-derived compression surfaces only. They are not routing
policy authority and they must not turn `aoa-skills` into a second router canon.

Those files describe canonical `skills/**/{scripts,references,assets}` resources and their bridge back to existing AoA support dirs.
The portable export still stays generated from canonical skill roots; `scripts/builders/build_support_resources.py` records the support layer, but it does not become a second portable-sync authority.

## Release verification

Use `generated/release_manifest.json` when you need one machine-readable view over the portable release contract.

`mechanics/release-support/manifests/release_manifest.bundle.json` lets the
same subject pass through the OS Abyss `abyss-machine` artifact verifier as
`aoa_skills_release_manifest` without duplicating signing controls in this
repository.

It intentionally keeps three things separate:

- repo-level release identity still lives in `CHANGELOG.md`, `mechanics/release-support/docs/RELEASING.md`, tags, and GitHub release notes
- bundle-level meaning and per-skill compatibility still live in `skills/**/SKILL.md`, `generated/skill_bundle_index.*`, and `generated/skill_graph.*`
- the release manifest only pins which portable artifact groups and relationship views exist and which bundle/profile revisions they currently expose
- a staged profile bundle carries its own `bundle_manifest.json` as the narrow handoff contract over one profile subset
- a staged profile bundle also carries a generated `README.md` as the portable human-facing handoff guide
- a staged ZIP handoff is only a transport wrapper over that same bundle-local contract
- bundle inspection stays self-contained to the handoff object rather than reconciling against the live repo export
- `scripts/import_skill_pack.py` is the receiver-friendly `inspect -> install -> verify` path over that same handoff object
- install verification remains a runtime check over a real target root via `scripts/verify_skill_pack.py`; it is not a committed generated catalog

## Build and validation

Executable ownership remains split by operation:

- `scripts/export/build_agent_skills.py` owns portable export generation;
- `scripts/validation/validate_agent_skills.py` owns export validation;
- `scripts/stage_skill_pack.py`, `scripts/inspect_skill_pack.py`,
  `scripts/import_skill_pack.py`, `scripts/install_skill_pack.py`, and
  `scripts/verify_skill_pack.py` own staged handoff and install operations;
- `scripts/audit/audit_workspace_skill_adoption.py` owns workspace adoption
  inspection;
- builder, runtime, and validation modules under their named script organs own
  description-trigger, support-resource, profile, standards, and runtime
  surfaces;
- `scripts/skill_runtime_guardrails.py` owns the governed runtime path,
  `scripts/skill_runtime_seam.py` owns the raw/debug path, and
  `scripts/activate_skill.py` remains compatibility ingress.

Full blocking order lives in `config/validation_lanes.json`. Focused invocation
syntax belongs to the executable owner and the nearest relevant `AGENTS.md`,
not to this architectural description.

## Local-friendly path

The adapter export is the common portable surface. Local runtimes should adapt around it by:

- reading `generated/agent_skill_catalog*.json` for discovery
- using `generated/runtime_discovery_index*.json` and `generated/runtime_disclosure_index.json` for shortlist and preview
- using `scripts/skill_runtime_guardrails.py` as the default runtime path for trust-gated discover, disclose, activate, allowlist, compact, and rehydrate
- using `scripts/skill_runtime_seam.py` only as the raw/debug seam
- respecting `policy.allow_implicit_invocation`
- preserving AoA metadata from frontmatter `metadata`
- consulting runtime/context/trust contracts instead of inventing a second local format
- treating `scripts/activate_skill.py` as the legacy compatibility shim for older local wrappers
