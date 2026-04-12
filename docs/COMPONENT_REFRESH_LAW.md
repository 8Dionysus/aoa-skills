# COMPONENT_REFRESH_LAW

## Purpose

This document is the owner refresh law for
`component:skills-export:foundation`.

Use it when canonical skill inputs stay intact but the generated Codex-facing
export, adapter-facing discovery surfaces, or runtime discovery views drift,
repeat the same repair, or block adjacent routes.

## Boundary

Keep this order:

1. `skills/*/SKILL.md`
2. repo-owned export config under `config/`
3. generated export and discovery surfaces under `.agents/skills/` and
   `generated/`
4. downstream wrappers, workspace installs, or consumer routes

If the component drifts, source-authored skill bundles and repo-owned config
win.

This law complements `CODEX_PORTABLE_LAYER.md`. It does not make `aoa-skills`
a hidden auto-mutator, scheduler, or owner of downstream workspace installs.

## Component scope

- `component_ref`: `component:skills-export:foundation`
- `owner_repo`: `aoa-skills`
- source-authored inputs:
  - `skills/*/SKILL.md`
  - `config/portable_skill_overrides.json`
  - `config/openai_skill_extensions.json`
  - `config/skill_pack_profiles.json`
  - `config/skill_policy_matrix.json`
  - `config/description_trigger_eval_policy.json`
- generated surfaces:
  - `.agents/skills/*`
  - `generated/agent_skill_catalog.min.json`
  - `generated/local_adapter_manifest.min.json`
  - `generated/runtime_discovery_index.json`
  - `generated/mcp_dependency_manifest.json`
- projected or installed surfaces:
  - `.agents/skills/`
- followthrough home:
  - `aoa-playbooks:component-refresh-cycle`

## Drift signals

- `skill_source_changed_without_export_refresh`
  - drift class: `export_drift`
  - meaning: canonical `SKILL.md` content changed while exported skill files or
    compact discovery views stayed stale
  - recommended route class: `reexport`
- `openai_yaml_dependency_drift`
  - drift class: `wiring_drift`
  - meaning: generated OpenAI-facing metadata or named MCP dependency guidance
    no longer matches repo-owned export inputs
  - recommended route class: `reexport`
- `runtime_discovery_surface_stale`
  - drift class: `runtime_drift`
  - meaning: runtime discovery or adapter-facing views no longer describe the
    current export accurately
  - recommended route class: `rebuild`
- `portable_policy_matrix_drift`
  - drift class: `policy_drift`
  - meaning: invocation posture or trust-facing export data diverged from
    source-owned policy inputs
  - recommended route class: `repair`
- `skill_validation_failed`
  - drift class: `validation_drift`
  - meaning: repo validation found a mismatch in the export or its dependent
    discovery surfaces
  - recommended route class: `rebuild`

## Refresh routes

- check:
  - `python scripts/build_catalog.py --check`
- execute:
  - `python scripts/build_catalog.py`
- validate:
  - `python scripts/validate_skills.py --fail-on-review-truth-sync`
  - `python scripts/validate_agent_skills.py --repo-root .`
  - `python scripts/validate_support_resources.py --repo-root . --check-portable`
  - `python scripts/validate_tiny_router_inputs.py --repo-root .`

Use `repair` only for a bounded owner fix that keeps source authorship in
`skills/*` or `config/`. Use `reexport` or `rebuild` when the generated layer
itself is stale.

## Proof and rollback

Proof commands:

- `python scripts/build_catalog.py --check`
- `python scripts/validate_skills.py --fail-on-review-truth-sync`
- `python scripts/report_skill_evaluation.py --fail-on-canonical-gaps`
- `python scripts/validate_agent_skills.py --repo-root .`
- `python scripts/validate_support_resources.py --repo-root . --check-portable`
- `python scripts/validate_tiny_router_inputs.py --repo-root .`
- `python -m pytest -q tests`

Rollback anchors:

- `docs/CODEX_PORTABLE_LAYER.md`
- `docs/LOCAL_ADAPTER_CONTRACT.md`
- `generated/local_adapter_manifest.min.json`
- `generated/runtime_discovery_index.json`

Refresh window:

- `stale_after_days`: `7`
- `repeat_trigger_threshold`: `2`
- `open_window_days`: `5`

## Negative rules

- Do not hand-edit `.agents/skills/*` as the source of truth.
- Do not treat `generated/*` export or discovery views as a second authoring
  layer.
- Do not rewrite canonical skill meaning just to preserve a stale export.
- Do not let `aoa-sdk`, `aoa-stats`, `aoa-playbooks`, or local wrappers
  overrule owner validation here.
- Do not turn repeated refresh work into hidden automatic mutation.
