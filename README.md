# aoa-skills

Public library of reusable Codex-facing skills for coding agents and humans.

`aoa-skills` is the operational companion to `aoa-techniques`. Where `aoa-techniques` stores reusable engineering practice, `aoa-skills` stores **skill bundles** that package one or more techniques and bounded actions into reviewable workflows for agents. A skill is normally a multi-technique or multi-step package. A single-technique skill is an explicit reviewed exception, not the default shape.

A skill here is not a random prompt and not a hidden project hack. It is a reusable agent-facing workflow with clear trigger boundaries, explicit contracts, risks, verification guidance, and technique traceability.

## Start here

Use the shortest route by need:

- first starter bundle: `skills/aoa-change-protocol/SKILL.md`
- current skill surface: `SKILL_INDEX.md`
- runtime path: `docs/RUNTIME_PATH.md`
- evaluation path: `docs/EVALUATION_PATH.md`
- public status and governance: `docs/PUBLIC_SURFACE.md`
- verify current repo state: `python scripts/build_catalog.py --check`, `python scripts/validate_skills.py --fail-on-review-truth-sync`, `python scripts/report_skill_evaluation.py --fail-on-canonical-gaps`, `python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques --fail-on-drift`, `python scripts/validate_agent_skills.py --repo-root .`, `python scripts/validate_support_resources.py --repo-root . --check-portable`, `python scripts/validate_tiny_router_inputs.py --repo-root .`, and `python -m pytest -q tests`
- docs map: `docs/README.md`
- layer position and boundaries: `docs/LAYER_POSITION.md`

## Route by need

- packaging, relationship, and release-manifest views: `generated/skill_bundle_index.md`, `generated/skill_graph.md`, `generated/skill_composition_audit.md`, and `generated/release_manifest.json`
- public status, governance, and overlay-maturity readouts: `generated/public_surface.md`, `generated/governance_backlog.md`, and `generated/overlay_readiness.md`
- runtime inspect and walkthrough surfaces: `generated/skill_walkthroughs.md` and `scripts/inspect_skill.py`
- additive degraded and receipt-authoring guidance for future skill bundles: `docs/ANTIFRAGILITY_SKILL_ADDENDUM.md`
- ability-reader and loadout surfaces: `docs/SKILL_ABILITY_MODEL.md`, `docs/ABILITY_LOADOUT_POSTURE.md`, and `generated/skill_ability_cards.min.example.json`
- evaluation evidence and matrix outputs: `generated/skill_evaluation_matrix.md`, `tests/fixtures/skill_evaluation_cases.yaml`, and `scripts/report_skill_evaluation.py`
- portable export and local runtime seams: `docs/CODEX_PORTABLE_LAYER.md`, `docs/LOCAL_ADAPTER_CONTRACT.md`, `docs/OPENAI_SKILL_EXTENSIONS.md`, `docs/RUNTIME_SEAM_SECOND_PATH.md`, `docs/RUNTIME_TOOL_CONTRACTS.md`, `docs/SESSION_COMPACTION.md`, and `.agents/skills/*`
- install, trust, config, and UI surfaces: `docs/INSTALL_AND_PROFILES.md`, `docs/CONTEXT_RETENTION.md`, `docs/UI_METADATA_AND_ASSETS.md`, `docs/CODEX_CONFIG_SNIPPETS.md`, `docs/TRUST_GATE_AND_ALLOWLIST.md`, `docs/SKILL_CONTEXT_GUARD.md`, and `docs/RUNTIME_GOVERNANCE_LAYER.md`
- activation quality and conformance: `docs/TRIGGER_EVALS.md`, `docs/DESCRIPTION_TRIGGER_EVALS.md`, and `docs/SKILLS_REF_VALIDATION.md`
- deterministic resources and downstream tiny-router bridge: `docs/DETERMINISTIC_RESOURCE_BUNDLES.md`, `docs/BRIDGE_FROM_AOA_SUPPORT_DIRS.md`, and `docs/TWO_STAGE_SKILL_SELECTION.md`
- project-core kernel receipts and bounded second-wave surface context: `config/project_core_skill_kernel.json`, `scripts/publish_core_skill_receipts.py`, and `skills/*/references/core-skill-application-receipt-schema.yaml`
- promotion, maturity, and release posture: `docs/MATURITY_MODEL.md`, `docs/PROMOTION_PATH.md`, and `docs/RELEASING.md`
- thin downstream overlays: `docs/OVERLAY_SPEC.md` and `docs/overlays/*`

## What belongs here

Good candidates:

- reusable Codex-facing workflows
- bounded change-protocol skills
- testing and validation skills
- architecture and context-mapping skills
- contract and invariant skills
- thin project overlays
- refresh helpers for canonical skill surfaces

Bad candidates:

- private infrastructure instructions
- secret-bearing examples
- raw project dumps
- one-off prompts with no reusable boundary
- techniques that belong in `aoa-techniques`
- undocumented scripts
- skills that silently widen the task

## Core distinction

- `aoa-techniques` owns reusable practice meaning
- `aoa-skills` owns bounded execution meaning
- `aoa-playbooks` owns scenario composition

In short:

`origin project -> technique canon -> skill canon -> project overlay`

The runtime path for public skill use remains:

`pick -> inspect -> expand -> object use`

Authored markdown still owns meaning. Generated catalogs, capsules, portable exports, and bridge manifests help routing and activation, but they do not replace the canonical skill bundle.

When project-core kernel receipts carry `surface_detection_context`, that
payload stays advisory. It may preserve shortlist, ambiguity, and closeout-link
truth for second-wave surface detection, but it does not let `aoa-skills`
claim non-skill activation authority.

## Repository layout

- `skills/` for canonical skill bundles and deterministic support resources
- `.agents/skills/` for the generated Codex-facing export layer
- `config/` for portable export, policy, and profile inputs
- `generated/` for derived catalogs, capsules, walkthroughs, evaluation matrices, and runtime manifests
- `docs/`, `templates/`, `schemas/`, `scripts/`, and `tests/` for architecture, authoring, validation, and generation

## Local validation

Install local dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the bounded repo check:

```bash
python scripts/release_check.py
```

For a read-only/current-state verify pass, use:

```bash
python scripts/build_catalog.py --check
python scripts/validate_skills.py --fail-on-review-truth-sync
python scripts/report_skill_evaluation.py --fail-on-canonical-gaps
python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques --fail-on-drift
python scripts/validate_agent_skills.py --repo-root .
python scripts/validate_support_resources.py --repo-root . --check-portable
python scripts/validate_tiny_router_inputs.py --repo-root .
python -m pytest -q tests
```

For day-to-day iteration, the smallest core loop remains:

```bash
python scripts/build_catalog.py
python scripts/validate_skills.py
python scripts/build_catalog.py --check
```

If you change skill bodies, portable export, policy posture, descriptions, deterministic resources, or tiny-router bridge inputs, also run the documented build and validation commands for those families.

## Go elsewhere when...

- you need reusable practice meaning: `aoa-techniques`
- you need proof doctrine or quality claims: `aoa-evals`
- you need routing and dispatch logic: `aoa-routing`
- you need role contracts: `aoa-agents`
- you need scenario composition: `aoa-playbooks`

## License

Apache-2.0
