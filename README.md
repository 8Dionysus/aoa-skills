# aoa-skills

Public library of reusable Codex-facing skills for coding agents and humans.

`aoa-skills` is the operational companion to `aoa-techniques`.
Where `aoa-techniques` stores public, reusable, validated engineering techniques,
`aoa-skills` stores **skill bundles** that compose techniques and bounded
actions into reviewable workflows for Codex. Skills normally package multiple
techniques and/or multiple operational steps; a single-technique skill is an
explicit reviewed exception, not the default shape.

A skill here is not a random prompt and not a hidden project hack.
It is a reusable agent-facing workflow with clear trigger boundaries,
explicit contracts, risks, verification guidance, and technique traceability.

## Start here

If you are new to this repository, follow this short path:

1. Read `docs/README.md` for the docs map.
2. Read `docs/RUNTIME_PATH.md` for the runtime path: `pick -> inspect -> expand -> object use`.
3. Read `docs/EVALUATION_PATH.md` for evaluation evidence, matrix outputs, and snapshot-backed coverage.
4. Read `docs/PUBLIC_SURFACE.md` for status, promotion, and governance entrypoints.
5. Read `docs/LAYER_POSITION.md` for the repo's place in the AoA layer map and the boundary between skills, techniques, and playbooks.
6. Read `generated/public_surface.md` and `generated/governance_backlog.md` for the current derived governance readout.
7. Read `generated/skill_composition_audit.md` if you want the current skill-vs-technique composition readout.
8. Read `generated/skill_bundle_index.md` and `generated/skill_graph.md` if you want packaging or relationship views.
9. Read `generated/skill_walkthroughs.md` for the current derived runtime walkthrough surface.
10. Read `generated/skill_evaluation_matrix.md` for the current derived evaluation evidence surface.
11. Read `docs/ARCHITECTURE.md` for the high-level model.
12. Read `docs/BRIDGE_SPEC.md` to understand how skills relate to `aoa-techniques`.
13. Read `docs/OVERLAY_SPEC.md` if you are thinking about thin downstream overlays or live exemplar overlay packs.
14. Read `docs/overlays/atm10/PROJECT_OVERLAY.md` for the first live exemplar family overlay pack.
15. Read `docs/RELEASING.md` if you need the bounded repo-level release flow.
16. Read `docs/CODEX_PORTABLE_LAYER.md` for the generated Codex-facing export under `.agents/skills/`.
17. Read `docs/LOCAL_ADAPTER_CONTRACT.md` if you need the runtime seams around that export.
18. Read `docs/INSTALL_AND_PROFILES.md`, `docs/CONTEXT_RETENTION.md`, `docs/UI_METADATA_AND_ASSETS.md`, and `docs/CODEX_CONFIG_SNIPPETS.md` if you are touching portable install, runtime-contract, or UI surfaces.
19. Read `docs/THIRD_WAVE.md` for the portable-layer hardening that added install, trust, and config surfaces.
20. Read `docs/FOURTH_WAVE.md`, `docs/RUNTIME_SEAM_SECOND_PATH.md`, `docs/RUNTIME_TOOL_CONTRACTS.md`, and `docs/SESSION_COMPACTION.md` if you are touching dedicated-tool runtime activation or long-running local wrappers.
21. Read `docs/SIXTH_WAVE.md`, `docs/TRUST_GATE_AND_ALLOWLIST.md`, `docs/SKILL_CONTEXT_GUARD.md`, and `docs/RUNTIME_GOVERNANCE_LAYER.md` if you are touching trust-gated activation, allowlists, or governed compaction/rehydration.
22. Read `docs/SEVENTH_WAVE.md`, `docs/DESCRIPTION_TRIGGER_EVALS.md`, and `docs/SKILLS_REF_VALIDATION.md` if you are touching activation-quality evals or soft standards-conformance checks.
23. Read `docs/EIGHTH_WAVE.md`, `docs/DETERMINISTIC_RESOURCE_BUNDLES.md`, and `docs/BRIDGE_FROM_AOA_SUPPORT_DIRS.md` if you are touching canonical skill resources under `skills/*/{scripts,references,assets}`.
24. Read `docs/NINTH_WAVE.md` and `docs/TWO_STAGE_SKILL_SELECTION.md` if you are touching the tiny-router compression layer used by downstream two-stage routing.
25. Read `SKILL_INDEX.md` for the current skill surface.
26. Open `skills/aoa-change-protocol/SKILL.md` as the first starter skill.
27. Use `templates/SKILL.template.md`, `templates/RUNTIME_EXAMPLE.template.md`, `templates/EVALUATION_SNAPSHOT.template.md`, `templates/PROJECT_OVERLAY.template.md`, and `templates/SKILL_COMPOSITION_EXCEPTION_REVIEW.template.md` when authoring new review surfaces.

## Quick routes

- if you need the shortest repo-owned explanation of how skills relate to techniques and playbooks, open `docs/LAYER_POSITION.md`
- if you need the upstream reusable practice canon, go to [aoa-techniques](https://github.com/8Dionysus/aoa-techniques)
- if you need portable proof surfaces for skill quality, boundaries, or regressions, go to [aoa-evals](https://github.com/8Dionysus/aoa-evals)
- if you need the smallest next object by task type, go to [aoa-routing](https://github.com/8Dionysus/aoa-routing)
- if you need explicit role contracts, handoff posture, or persona surfaces, go to [aoa-agents](https://github.com/8Dionysus/aoa-agents)
- if you need higher-level scenario composition, go to [aoa-playbooks](https://github.com/8Dionysus/aoa-playbooks)

## What belongs here

Good candidates:
- reusable Codex-facing workflows
- bounded change-protocol skills
- testing and validation skills
- architecture and context-mapping skills
- contract and invariant skills
- project overlay examples that stay thin and explicit
- skill generation or refresh helpers

Bad candidates:
- private infrastructure instructions
- secret-bearing examples
- raw project dumps
- one-off prompts without reusable boundaries
- techniques that should live in `aoa-techniques`
- undocumented scripts
- skills that silently widen the task without naming it

## Core distinction

### `aoa-techniques`
Stores the public canon of reusable engineering techniques.
A technique is a minimal reproducible unit of engineering practice.

### `aoa-skills`
Stores the Codex-facing execution layer.
A skill may depend on one or more techniques and package them into an
executable workflow for agents. When a skill is only a lift of one technique,
it should carry an explicit exception review explaining why it still needs a
skill layer.

In short:

`origin project -> technique canon -> skill canon -> project overlay`

The current repo-local surface stack is:

- runtime selection and object use: `docs/RUNTIME_PATH.md`, `generated/skill_walkthroughs.*`, `scripts/inspect_skill.py`
- evaluation evidence and matrix reading: `docs/EVALUATION_PATH.md`, `generated/skill_evaluation_matrix.*`, `tests/fixtures/skill_evaluation_cases.yaml`, `scripts/report_skill_evaluation.py`
- public-product and governance signals: `docs/PUBLIC_SURFACE.md`, `generated/public_surface.*`, `generated/governance_backlog.*`, `generated/skill_bundle_index.*`, `generated/skill_graph.*`
- Codex-facing portable export and runtime seams: `docs/CODEX_PORTABLE_LAYER.md`, `docs/LOCAL_ADAPTER_CONTRACT.md`, `docs/RUNTIME_SEAM_SECOND_PATH.md`, `docs/SIXTH_WAVE.md`, `docs/TRUST_GATE_AND_ALLOWLIST.md`, `docs/SKILL_CONTEXT_GUARD.md`, `docs/RUNTIME_GOVERNANCE_LAYER.md`, `docs/SEVENTH_WAVE.md`, `docs/DESCRIPTION_TRIGGER_EVALS.md`, `docs/SKILLS_REF_VALIDATION.md`, `docs/EIGHTH_WAVE.md`, `docs/DETERMINISTIC_RESOURCE_BUNDLES.md`, `docs/BRIDGE_FROM_AOA_SUPPORT_DIRS.md`, `docs/NINTH_WAVE.md`, `docs/TWO_STAGE_SKILL_SELECTION.md`, `.agents/skills/*`, `generated/agent_skill_catalog*.json`, `generated/local_adapter_manifest*.json`, `generated/skill_handoff_contracts.json`, `generated/context_retention_manifest.json`, `generated/trust_policy_matrix.json`, `generated/skill_runtime_contracts.json`, `generated/skill_pack_profiles.resolved.json`, `generated/codex_config_snippets.json`, `generated/runtime_*.json`, `generated/*guardrail*.json`, `generated/skill_description_signals.json`, `generated/description_trigger_eval_cases.*`, `generated/skills_ref_validation_manifest.json`, `generated/deterministic_resource_manifest.json`, `generated/support_resource_index.json`, `generated/structured_output_schema_index.json`, `generated/support_resource_bridge_map.json`, `generated/deterministic_resource_eval_cases.jsonl`, `generated/expected_existing_aoa_support_dirs.json`, `generated/tiny_router_skill_signals.json`, `generated/tiny_router_candidate_bands.json`, `generated/tiny_router_capsules.min.json`, `generated/tiny_router_eval_cases.jsonl`, `generated/tiny_router_overlay_manifest.json`, `scripts/build_agent_skills.py`, `scripts/build_runtime_seam.py`, `scripts/build_runtime_guardrails.py`, `scripts/build_description_trigger_evals.py`, `scripts/build_support_resources.py`, `scripts/build_tiny_router_inputs.py`, `scripts/validate_support_resources.py`, `scripts/validate_tiny_router_inputs.py`, `scripts/lint_support_resources.py`, `scripts/lint_description_trigger_evals.py`, `scripts/run_skills_ref_validation.py`, `scripts/skill_runtime_seam.py`, `scripts/skill_runtime_guardrails.py`, `scripts/activate_skill.py`, `scripts/install_skill_pack.py`, `scripts/render_codex_config.py`
- composition-boundary and exception-review signals: `generated/skill_composition_audit.*`, `docs/reviews/skill-composition-exceptions/*.md`, `templates/SKILL_COMPOSITION_EXCEPTION_REVIEW.template.md`
- overlay preparation and thin downstream adaptation: `docs/OVERLAY_SPEC.md`, `docs/overlays/atm10/PROJECT_OVERLAY.md`, `templates/PROJECT_OVERLAY.template.md`, `templates/PROJECT_OVERLAY_SKILL.template.md`

The runtime path for public skill use is:

`pick -> inspect -> expand -> object use`

For KAG/source-lift consumers, `AOA-T-0019` is the canonical bundle-level metadata spine and `AOA-T-0018` is the bounded section-lift layer. The authored markdown bundle still owns the meaning; derived metadata and section surfaces only help routing.

## Core principles

- techniques are the source of truth for reusable practice
- skills are the agent-facing operational interface
- public by design, sanitized by default
- bounded scope over vague power
- runtime skills should stay self-contained and reviewable
- build-time composition over runtime remote dependency
- thin overlays over hidden project assumptions
- validation matters
- traceability matters

## Repository structure

- `.agents/` — generated Codex-facing export layer built from canonical skill surfaces
- `config/` — portable export description overrides, optional OpenAI metadata extensions, and wave-3 install/trust authoring inputs
- `examples/` — sample Codex config snippets for profile disable and install scenarios
- `docs/` — architecture, bridge rules, roadmap, conventions
- `templates/` — templates for skill authoring and composition metadata
- `skills/` — skill bundles
- `generated/` — derived reader catalogs, local runtime cards, section surfaces, walkthrough surfaces, snapshot-backed evaluation matrix surfaces, public-product surfaces, and portable export/adaptation manifests built from committed skill markdown, manifests, support artifacts, review records, evaluation fixtures, and portable-layer config
- `scripts/` — local validation and refresh helpers
- `schemas/` — machine-readable bundle contracts
- `tests/` — local validator and evaluation tests
- `SKILL_INDEX.md` — repository-wide skill map

Local working notes such as `TODO.local.md` and `PLANS.local.md` stay gitignored in each clone.
The public planning artifact for this repository is `docs/ROADMAP.md`, which remains tracked.

A typical skill bundle contains:
- `SKILL.md`
- `techniques.yaml`
- optional `agents/openai.yaml`
- optional `examples/`, `references/`, `checks/`, `scripts/`, or `assets/`

`SKILL.md` and `techniques.yaml` remain authoritative.
`generated/skill_catalog.json` and `generated/skill_catalog.min.json` are derived reader surfaces for routing and indexing.
`generated/skill_capsules.json` is a derived local runtime-card surface with bounded per-skill summaries.
`generated/skill_sections.full.json` is the source-owned section payload surface for bounded expand-time reads.
`generated/skill_walkthroughs.json` and `generated/skill_walkthroughs.md` are derived runtime inspect surfaces built from skill markdown and support artifacts.
`generated/skill_evaluation_matrix.json` and `generated/skill_evaluation_matrix.md` are derived evaluation evidence surfaces built from committed fixtures, snapshot cases, runtime artifacts, and review records.
`generated/public_surface.json` and `generated/public_surface.md` are derived governance and public-product surfaces.
`.agents/skills/*` is a generated Codex-facing export layer built from canonical skill bundles plus `config/portable_skill_overrides.json`, optional `config/openai_skill_extensions.json`, and support config in `config/skill_pack_profiles.json`, `config/skill_policy_matrix.json`, `config/description_trigger_eval_policy.json`, and `config/tiny_router_skill_bands.json`.
`generated/agent_skill_catalog*.json`, `generated/portable_export_map.json`, `generated/local_adapter_manifest*.json`, `generated/skill_handoff_contracts.json`, `generated/context_retention_manifest.json`, `generated/trust_policy_matrix.json`, `generated/skill_runtime_contracts.json`, `generated/skill_pack_profiles.resolved.json`, `generated/codex_config_snippets.json`, `generated/mcp_dependency_manifest.json`, `generated/runtime_discovery_index*.json`, `generated/runtime_disclosure_index.json`, `generated/runtime_activation_aliases.json`, `generated/runtime_tool_schemas.json`, `generated/runtime_session_contract.json`, `generated/runtime_prompt_blocks.json`, `generated/runtime_router_hints.json`, `generated/runtime_seam_manifest.json`, `generated/skill_description_signals.json`, `generated/description_trigger_eval_cases.*`, `generated/description_trigger_eval_manifest.json`, `generated/skills_ref_validation_manifest.json`, `generated/deterministic_resource_manifest.json`, `generated/support_resource_index.json`, `generated/structured_output_schema_index.json`, `generated/support_resource_bridge_map.json`, `generated/deterministic_resource_eval_cases.jsonl`, `generated/expected_existing_aoa_support_dirs.json`, `generated/tiny_router_skill_signals.json`, `generated/tiny_router_candidate_bands.json`, `generated/tiny_router_capsules.min.json`, `generated/tiny_router_eval_cases.jsonl`, `generated/tiny_router_overlay_manifest.json`, and `generated/release_manifest.json` are derived portable discovery, activation, install, trust, runtime, activation-quality, support-resource, tiny-router bridge, and playbook-bridge surfaces.
`generated/release_manifest.json` inventories portable artifacts only and does not replace repo-level release identity in `CHANGELOG.md`, the Git tag, or the GitHub release body.
`generated/skill_trigger_eval_cases.jsonl` and `generated/skill_trigger_collision_matrix.json` are versioned trigger-eval seed data validated against the canonical invocation policy.

## Skill categories

- `core` — public reusable skills across many repositories
- `project` — skills shaped for a repository family such as `atm10-*` or `abyss-*`
- `risk` — operationally sensitive skills that should usually be explicit-only

## Current repository phase

This repository now has a mixed-status public core of 17 skills with first support artifacts, pinned bridge manifests, local validation for bundle shape and policy coherence, and source-owned section surfaces for bounded expand-time reads.
The first public baseline release is `v0.1.0`, and repo-level release identity now lives in `CHANGELOG.md`, `docs/RELEASING.md`, the Git tag, and the GitHub release body rather than in per-skill metadata.
The current derived baseline in `generated/public_surface.md` and `generated/governance_backlog.md` tracks the live default-reference cohort, candidate-review cohort, and zero pending-lineage blockers.
It now also includes a runtime inspection layer in `docs/RUNTIME_PATH.md`, `generated/skill_walkthroughs.*`, and `scripts/inspect_skill.py`, kept separate from the evaluation evidence and governance/public-surface layers.
The current focus is candidate review and promotion decisions, overlay maturity, public/docs clarity, and packaging prep through derived maintenance surfaces such as `generated/governance_backlog.*`, `generated/skill_bundle_index.*`, and `generated/skill_graph.*`.
Overlay adoption remains intentionally thin, public-safe, and repo-local.
`docs/OVERLAY_SPEC.md`, `docs/overlays/atm10/PROJECT_OVERLAY.md`, `docs/overlays/abyss/PROJECT_OVERLAY.md`, and the overlay templates now describe live exemplar overlay packs without pretending to be live downstream integrations.
The repo now also publishes a generated Codex-facing export under `.agents/skills/*`, a legacy-compatible local adapter seam in `generated/local_adapter_manifest*.json` and `scripts/activate_skill.py`, a wave-4 raw runtime seam in `scripts/skill_runtime_seam.py` plus `generated/runtime_*.json`, a wave-6 governed runtime layer in `scripts/skill_runtime_guardrails.py` plus `generated/*guardrail*.json`, a wave-7 description-first activation-eval layer in `generated/skill_description_signals.json`, `generated/description_trigger_eval_cases.*`, and `generated/skills_ref_validation_manifest.json`, a wave-8 deterministic support-resource bridge in `generated/deterministic_resource_manifest.json`, `generated/support_resource_index.json`, `generated/structured_output_schema_index.json`, `generated/support_resource_bridge_map.json`, and `generated/expected_existing_aoa_support_dirs.json`, a skill-derived handoff bridge for downstream playbook layers in `generated/skill_handoff_contracts.json`, wave-3 install and trust surfaces in `generated/skill_pack_profiles.resolved.json`, `generated/context_retention_manifest.json`, `generated/trust_policy_matrix.json`, `generated/skill_runtime_contracts.json`, and policy-aware trigger-eval data in `generated/skill_trigger_eval_cases.jsonl` and `generated/skill_trigger_collision_matrix.json`.

## When not to use this repository

Do not use `aoa-skills` as:

- the source canon for reusable techniques
- the proof layer for quality claims
- the memory layer
- the role-contract layer
- the scenario-composition layer

Use it when you need a bounded, reviewable workflow bundle that an agent can execute.

## Local validation

Install the validator dependency:

```bash
python -m pip install -r requirements-dev.txt
```

Run the full repository check:

```bash
python scripts/release_check.py
```

For day-to-day iteration, the underlying commands remain available:

```bash
python scripts/build_catalog.py
python scripts/validate_skills.py
python scripts/build_catalog.py --check
```

For portable export work or any change to skill bodies, invocation modes, portable overrides, OpenAI extensions, pack profiles, policy posture, or skill assets, also use:

```bash
python scripts/build_agent_skills.py --repo-root .
python scripts/build_runtime_seam.py --repo-root .
python scripts/build_runtime_guardrails.py --repo-root .
python scripts/validate_agent_skills.py --repo-root .
python scripts/lint_trigger_evals.py --repo-root .
python scripts/build_description_trigger_evals.py --repo-root .
python scripts/lint_description_trigger_evals.py --repo-root .
python scripts/lint_pack_profiles.py --repo-root .
python scripts/build_support_resources.py --repo-root .
python scripts/validate_support_resources.py --repo-root . --check-portable
python scripts/lint_support_resources.py --repo-root .
python scripts/build_tiny_router_inputs.py --repo-root .
python scripts/validate_tiny_router_inputs.py --repo-root .
python scripts/run_skills_ref_validation.py --repo-root .
```

Refresh the derived catalogs, capsules, sections, walkthroughs, evaluation matrix, and public surface directly:

```bash
python scripts/build_catalog.py
```

Refresh the generated Codex-facing export, raw runtime seam, governed runtime layer, and local-adapter manifests directly:

```bash
python scripts/build_agent_skills.py --repo-root .
python scripts/build_runtime_seam.py --repo-root .
python scripts/build_runtime_guardrails.py --repo-root .
python scripts/build_description_trigger_evals.py --repo-root .
python scripts/build_support_resources.py --repo-root .
```

Inspect a skill through the runtime path:

```bash
python scripts/inspect_skill.py --skill aoa-change-protocol
```

Inspect the same skill's support artifacts and review evidence:

```bash
python scripts/inspect_skill.py --skill aoa-change-protocol --view evidence
```

Inspect the corresponding local activation payload for the generated portable export:

```bash
python scripts/skill_runtime_seam.py activate --repo-root . --skill aoa-change-protocol --format json
```

Preview a disable snippet for one install profile:

```bash
python scripts/render_codex_config.py --repo-root . --profile repo-risk-explicit
```

Preview or apply one install profile:

```bash
python scripts/install_skill_pack.py --repo-root . --profile repo-core-only
python scripts/install_skill_pack.py --repo-root . --profile repo-core-only --dest-root /tmp/aoa-skills --mode copy --execute
```

Run a single skill check:

```bash
python scripts/validate_skills.py --skill aoa-change-protocol
```

The validator now uses repository schemas from `schemas/` as the contract layer for
front matter, `techniques.yaml`, and `agents/openai.yaml`.
It also checks that the generated catalogs, capsules, full section surfaces, walkthrough surfaces, evaluation matrix surfaces, and derived public-surface JSON/Markdown exist, stay current, that the min catalog is an exact projection of the full catalog, and that capsules, sections, walkthroughs, and evaluation surfaces stay aligned with the same source bundles.

Read the derived evaluation matrix directly:

```bash
python scripts/report_skill_evaluation.py
```

Fail fast if any canonical skill has snapshot-backed evaluation gaps:

```bash
python scripts/report_skill_evaluation.py --fail-on-canonical-gaps
```

Preview a manifest-driven `SKILL.md` refresh without rewriting files:

```bash
python scripts/refresh_skill_from_manifest.py --skill aoa-change-protocol
```

Apply a manifest-driven refresh to one explicitly named skill:

```bash
python scripts/refresh_skill_from_manifest.py --skill aoa-change-protocol --write
```

The first write mode is intentionally bounded to a single skill per run.

Check whether published technique refs have drifted against a local `aoa-techniques` checkout:

```bash
python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques
```

Preview an upstream-driven refresh for explicitly named skills:

```bash
python scripts/refresh_skill_from_techniques.py --skill aoa-change-protocol --techniques-repo ../aoa-techniques
```

Recommended bridge refresh order:

1. `python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques`
2. `python scripts/refresh_skill_from_techniques.py --skill aoa-change-protocol --techniques-repo ../aoa-techniques`
3. manually review whether upstream technique drift requires runtime wording changes beyond traceability and pinned refs
4. `python scripts/build_catalog.py`
5. `python scripts/validate_skills.py`

The drift and refresh tools intentionally use CLI output and git diff as the review surface.
They do not add committed drift-report artifacts, and the upstream refresh flow remains bounded to explicitly named skills.

## Contribution model

A skill is usually shaped from one or more real techniques and a bounded
sequence of actions. Thin one-technique imports should be the exception, not
the norm.
Those techniques are first born and validated in a real project,
then promoted into `aoa-techniques`, and only then packaged here
into a Codex-facing skill.

In short:

`project -> validation -> sanitization -> promotion -> technique canon -> skill composition`

## Intended users

- coding agents
- solo builders
- infra engineers
- product engineers
- AI workflow designers
- teams that want reusable agent workflows

## License

Apache-2.0
