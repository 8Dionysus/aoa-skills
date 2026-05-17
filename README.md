# aoa-skills

Public library of reusable local coding-agent skills for agentic coding work
and human review.

`aoa-skills` is the operational companion to `aoa-techniques`. Where `aoa-techniques` stores reusable engineering practice, `aoa-skills` stores **skill bundles**: self-contained workflows an agent can execute. A skill may package techniques and bounded actions, and a mature skill may also produce technique extraction work. Technique links are bridge evidence, not runtime dependency or automatic status blockers. A single-technique skill is an explicit reviewed exception, not the default shape.

A skill here is not a random prompt and not a hidden project hack. It is a reusable agent-facing workflow with clear trigger boundaries, explicit contracts, risks, verification guidance, and honest technique bridge traceability when such a bridge is declared.

> Current release: `v0.3.3`. See [CHANGELOG](CHANGELOG.md) for release notes.

## Start here

Use the shortest route by need:

- first starter bundle: `skills/core/engineering/aoa-change-protocol/SKILL.md`
- skill-layer design form: `DESIGN.md`
- agent-facing guidance design: `DESIGN.AGENTS.md`
- source topology: `skills/README.md`
- current skill surface: `SKILL_INDEX.md`
- current direction router: `mechanics/ROADMAP.md`, then the nearest mechanic
  package `ROADMAP.md`
- runtime path: `mechanics/release-support/docs/RUNTIME_PATH.md`
- orchestration and closeout path: `mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md`
- evaluation path: `mechanics/audit/docs/EVALUATION_PATH.md`
- public status and governance: `mechanics/audit/docs/PUBLIC_SURFACE.md`
- verify current repo state: `python scripts/build_catalog.py --check`, `python scripts/validate_skills.py --fail-on-review-truth-sync`, `python scripts/report_skill_evaluation.py --fail-on-canonical-gaps`, `python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques --fail-on-drift`, `python scripts/validate_agent_skills.py --repo-root .`, `python scripts/validate_support_resources.py --repo-root . --check-portable`, `python scripts/validate_tiny_router_inputs.py --repo-root .`, and `python -m pytest -q tests`
- docs map: `docs/README.md`
- layer position and boundaries: `mechanics/boundary-bridge/docs/LAYER_POSITION.md`

## Route by need

- packaging, relationship, and release-manifest views: `generated/skill_bundle_index.md`, `generated/skill_graph.md`, `generated/skill_composition_audit.md`, and `generated/release_manifest.json`
- public status, governance, and overlay-maturity readouts: `generated/public_surface.md`, `generated/governance_backlog.md`, and `generated/overlay_readiness.md`
- via negativa pruning checklist: `mechanics/antifragility/parts/via-negativa-pruning/README.md`
- runtime inspect and walkthrough surfaces: `generated/skill_walkthroughs.md` and `scripts/inspect_skill.py`
- additive degraded and receipt-authoring guidance for future skill bundles: `mechanics/antifragility/parts/fallback-authoring-posture/README.md`
- checkpoint-aware pre-harvest session-growth capture: `mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md`, `mechanics/checkpoint/schemas/session_checkpoint_note.schema.json`, and `mechanics/checkpoint/examples/session_checkpoint_note.example.json`
- reviewed owner-status landing and bounded next-step followthrough after `candidate_ref` exists: `mechanics/method-growth/docs/OWNER_STATUS_SURFACES.md`, `mechanics/method-growth/docs/GOVERNED_FOLLOWTHROUGH.md`, `mechanics/method-growth/schemas/reviewed_owner_landing_bundle.schema.json`, `mechanics/method-growth/schemas/route_followthrough_decision.schema.json`, and matching examples under `mechanics/method-growth/examples/`
- explicit skill adoption lifecycle posture: `mechanics/method-growth/parts/adoption-boundary/README.md`, `mechanics/method-growth/parts/adoption-evidence-receipts/README.md`, `mechanics/method-growth/parts/retention-regression-retirement/README.md`, and `mechanics/method-growth/parts/pattern-adoption-handoff/README.md`
- owner-local mechanics, AoA owner-request receipts, Checkpoint carry, Method-growth candidate/adoption movement, Questbook integration, Recurrence observation, Antifragility risk posture, and Agon bounded-workflow companion bridge: `mechanics/README.md`, `mechanics/OWNER_REQUEST_RECEIPTS.md`, `mechanics/checkpoint/README.md`, `mechanics/checkpoint/parts/checkpoint-note-lane/README.md`, `mechanics/method-growth/README.md`, `mechanics/method-growth/parts/candidate-lineage/README.md`, `mechanics/method-growth/parts/adoption-boundary/README.md`, `mechanics/method-growth/parts/adoption-evidence-receipts/README.md`, `mechanics/method-growth/parts/retention-regression-retirement/README.md`, `mechanics/method-growth/parts/pattern-adoption-handoff/README.md`, `mechanics/questbook/README.md`, `mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md`, `mechanics/recurrence/README.md`, `mechanics/recurrence/parts/live-observation-producers/README.md`, `mechanics/recurrence/parts/review-decision-closure/README.md`, `mechanics/antifragility/README.md`, `mechanics/antifragility/parts/fallback-authoring-posture/README.md`, `mechanics/antifragility/parts/via-negativa-pruning/README.md`, `mechanics/antifragility/parts/collision-stress-program/README.md`, `mechanics/agon/README.md`, `mechanics/agon/parts/workflow-candidate-bridge/README.md`, `mechanics/agon/parts/candidate-validation-gate/README.md`, `generated/agon_skill_binding_candidates.min.json`, `python mechanics/agon/parts/workflow-candidate-bridge/scripts/build_agon_skill_binding_candidates.py --check`, `python mechanics/agon/parts/workflow-candidate-bridge/scripts/validate_agon_skill_binding_candidates.py`, and `python -m pytest -q mechanics/agon/parts/workflow-candidate-bridge/tests/test_agon_skill_binding_candidates.py`
- adaptive applicability, closeout, and harvest routing for multi-skill sessions: `mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md`, `templates/SKILL_APPLICABILITY_MAP.template.md`, and `templates/SESSION_CANDIDATE_HARVEST.template.md`
- checkpoint-to-closeout bridge orchestration: `skills/core/session-growth/aoa-checkpoint-closeout-bridge/SKILL.md`, `mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md`, and `mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md`
- ability-reader and loadout surfaces: `mechanics/rpg/parts/ability-reader-boundary/README.md`, `mechanics/rpg/parts/loadout-posture/README.md`, and `generated/skill_ability_cards.min.example.json`
- evaluation evidence and matrix outputs: `generated/skill_evaluation_matrix.md`, `tests/fixtures/skill_evaluation_cases.yaml`, and `scripts/report_skill_evaluation.py`
- authored skill quality audit across bodies, evidence, runtime, lineage, and upgrade targets: `scripts/audit_skill_quality.py`, `generated/skill_quality_audit.md`, and `generated/skill_quality_audit.json`
- real repository skill-dispatch trials: `scripts/run_skill_reality_trials.py`, `generated/skill_reality_trials.md`, and `generated/skill_reality_trials.json`
- lived-use promotion pressure for non-canonical skills: `mechanics/method-growth/docs/PROMOTION_PRESSURE.md`, `scripts/report_skill_promotion_pressure.py`, `generated/skill_promotion_pressure.md`, and `generated/skill_promotion_pressure.json`
- deferred workflow, checkpoint-note promotion, recurring cross-repo follow-through, and quest dispatch: `QUESTBOOK.md`, `mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md`, `generated/quest_catalog.min.json`, and `generated/quest_dispatch.min.json`
- portable export, component refresh law, and local runtime seams: `mechanics/release-support/docs/CODEX_PORTABLE_LAYER.md`, `mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md`, `mechanics/release-support/docs/LOCAL_ADAPTER_CONTRACT.md`, `mechanics/boundary-bridge/docs/OPENAI_SKILL_EXTENSIONS.md`, `mechanics/boundary-bridge/docs/CODEX_SKILL_MCP_WIRING.md`, `mechanics/release-support/docs/RUNTIME_SEAM_SECOND_PATH.md`, `mechanics/release-support/docs/RUNTIME_TOOL_CONTRACTS.md`, `mechanics/release-support/docs/SESSION_COMPACTION.md`, and `.agents/skills/*`
- workspace and repo adoption audit before rollout: `mechanics/release-support/docs/INSTALL_AND_PROFILES.md`, `scripts/audit_workspace_skill_adoption.py`, `generated/workspace_skill_adoption_audit.md`, and `generated/workspace_skill_adoption_audit.json`
- named MCP dependency scaffolds and workspace-alignment checks: `mechanics/boundary-bridge/examples/skill_mcp_wiring.map.json`, `mechanics/boundary-bridge/examples/openai.*.example.yaml`, `scripts/build_openai_yaml_examples.py`, and `scripts/validate_skill_mcp_wiring.py`
- install, trust, config, and UI surfaces: `mechanics/release-support/docs/INSTALL_AND_PROFILES.md`, `mechanics/release-support/docs/CONTEXT_RETENTION.md`, `mechanics/release-support/docs/UI_METADATA_AND_ASSETS.md`, `mechanics/release-support/docs/CODEX_CONFIG_SNIPPETS.md`, `mechanics/release-support/docs/TRUST_GATE_AND_ALLOWLIST.md`, `mechanics/release-support/docs/SKILL_CONTEXT_GUARD.md`, and `mechanics/release-support/docs/RUNTIME_GOVERNANCE_LAYER.md`
- activation quality and conformance: `mechanics/audit/docs/TRIGGER_EVALS.md`, `mechanics/antifragility/parts/collision-stress-program/README.md`, `mechanics/audit/docs/DESCRIPTION_TRIGGER_EVALS.md`, and `mechanics/audit/docs/SKILLS_REF_VALIDATION.md`
- deterministic resources and downstream tiny-router bridge: `mechanics/release-support/docs/DETERMINISTIC_RESOURCE_BUNDLES.md`, `mechanics/boundary-bridge/docs/BRIDGE_FROM_AOA_SUPPORT_DIRS.md`, and `mechanics/boundary-bridge/docs/TWO_STAGE_SKILL_SELECTION.md`
- project-core kernel receipts, maturity guidance, and bounded follow-up surface context: `config/project_core_skill_kernel.json`, `scripts/publish_core_skill_receipts.py`, `skills/**/references/core-skill-application-receipt-schema.yaml`, `mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md`, and `mechanics/growth-cycle/examples/session_growth_artifacts/*.wave4.json`
- promotion, maturity, and release posture: `mechanics/method-growth/docs/MATURITY_MODEL.md`, `mechanics/method-growth/docs/PROMOTION_PATH.md`, and `mechanics/release-support/docs/RELEASING.md`
- thin downstream overlays: `mechanics/boundary-bridge/docs/OVERLAY_SPEC.md` and `mechanics/boundary-bridge/overlays/*`

## What belongs here

Good candidates:

- reusable local coding-agent workflows
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

`origin project -> technique canon <-> skill canon -> project overlay`

The runtime path for public skill use remains:

`pick -> inspect -> expand -> object use`

Authored markdown still owns meaning. Generated catalogs, capsules, portable exports, and bridge manifests help routing and activation, but they do not replace the canonical skill bundle.

When project-core kernel receipts carry `surface_detection_context`, that
payload stays advisory. It may preserve shortlist, ambiguity, and closeout-link
truth for follow-up surface detection, but it does not let `aoa-skills`
claim non-skill activation authority.

## Repository layout

- `skills/` for canonical skill bundles and deterministic support resources
- `mechanics/` for owner-local skill-layer movement surfaces around AoA mechanics
- `.agents/skills/` for the generated Codex-compatible export layer
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
python scripts/build_openai_yaml_examples.py --map mechanics/boundary-bridge/examples/skill_mcp_wiring.map.json --output-dir mechanics/boundary-bridge/examples --check
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

When the task specifically touches named MCP dependency wiring, also validate the
workspace seam against a real workspace config:

```bash
python scripts/validate_skill_mcp_wiring.py --workspace-config /path/to/.codex/config.toml --format text
```

## Go elsewhere when...

- you need reusable practice meaning: `aoa-techniques`
- you need proof doctrine or quality claims: `aoa-evals`
- you need routing and dispatch logic: `aoa-routing`
- you need role contracts: `aoa-agents`
- you need scenario composition: `aoa-playbooks`

## License

Apache-2.0
