# Docs map

`aoa-skills` is the Codex-facing companion to `aoa-techniques`.

Where `aoa-techniques` stores public, reusable, validated engineering techniques,
`aoa-skills` stores reusable agent skills: self-contained executable workflows
for Codex. Skills may compose techniques into workflows, and repeated skill
execution may also produce technique extraction requests.

## Quick route by question

- If you want one concrete source-authored skill before any derived layer, start with `../skills/core/engineering/aoa-change-protocol/SKILL.md` and then `../mechanics/release-support/docs/RUNTIME_PATH.md`.
- If you need to navigate source bundle placement, start with `../skills/README.md`.
- If you want the current canonical surface at a glance, start with `../SKILL_INDEX.md`.
- If you are choosing or using a skill, start with `../mechanics/release-support/docs/RUNTIME_PATH.md`.
- If you need named MCP dependency wiring or workspace-server alignment for the generated Codex export, start with `../mechanics/boundary-bridge/docs/CODEX_SKILL_MCP_WIRING.md` and `../mechanics/boundary-bridge/docs/OPENAI_SKILL_EXTENSIONS.md`.
- If you are checking repeated export drift, stale generated discovery surfaces, or owner refresh posture for the portable layer, start with `../mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md`, then `../mechanics/release-support/docs/CODEX_PORTABLE_LAYER.md`, and then `../mechanics/release-support/docs/LOCAL_ADAPTER_CONTRACT.md`.
- If you need to decide which skills apply now, which belong to closeout, and which belong to harvest, start with `../mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md`.
- If you need a committed bounded note for reusable session outputs that are not yet skill reviews or owner-layer truth, start with `session-harvests/README.md`.
- If you need additive degraded, fallback, or receipt-authoring posture for future skills, start with `../mechanics/antifragility/parts/fallback-authoring-posture/README.md`.
- If you need a lightweight checkpoint-aware note before post-session harvest, start with `../mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md`.
- If you need the checkpoint-to-reviewed-candidate identity seam, start with `../mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md`, then `../mechanics/method-growth/docs/CANDIDATE_LINEAGE_CONTRACT.md`, and then `../mechanics/method-growth/docs/CANDIDATE_REF_REFINERY.md`.
- If you need the first reviewed owner-status landing and the next bounded verdict after `candidate_ref` exists, start with `../mechanics/method-growth/docs/OWNER_STATUS_SURFACES.md`, then `../mechanics/method-growth/docs/GOVERNED_FOLLOWTHROUGH.md`, and then `../mechanics/method-growth/docs/CANDIDATE_REF_REFINERY.md`.
- If you need explicit skill adoption lifecycle posture, start with `../mechanics/method-growth/parts/adoption-boundary/README.md`, then `../mechanics/method-growth/parts/adoption-evidence-receipts/README.md`, `../mechanics/method-growth/parts/retention-regression-retirement/README.md`, or `../mechanics/method-growth/parts/pattern-adoption-handoff/README.md`.
- If you need owner-local skill mechanics, start with `../mechanics/README.md`; for AoA center owner-request receipts, use `../mechanics/OWNER_REQUEST_RECEIPTS.md`; for Method-growth candidate and adoption movement, continue to `../mechanics/method-growth/README.md`; for Recurrence observation, continue to `../mechanics/recurrence/README.md`; for Antifragility risk posture, continue to `../mechanics/antifragility/README.md`; and for the Agon bounded-workflow companion bridge, continue to `../mechanics/agon/README.md`, `../mechanics/agon/parts/workflow-candidate-bridge/README.md`, `../mechanics/agon/parts/candidate-validation-gate/README.md`, and `../generated/agon_skill_binding_candidates.min.json`.
- If you need the later reviewed session-growth kernel packet and receipt examples after closeout carry and `candidate_ref` already exist, start with `../mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md`.
- If you are checking evidence, fixtures, or snapshot-backed coverage, start with `../mechanics/audit/docs/EVALUATION_PATH.md`.
- If you need the stress-era trigger and collision extension for timeout chaos, source-of-truth wins, and one-off incident suppression, start with `../mechanics/audit/docs/TRIGGER_EVALS.md` and then `../mechanics/antifragility/parts/collision-stress-program/README.md`.
- If you are reading status, promotion, or governance state, start with `../mechanics/audit/docs/PUBLIC_SURFACE.md`.
- If you are asking why a repeatedly used skill is not canonical yet, start with `../mechanics/method-growth/docs/PROMOTION_PRESSURE.md` and `../generated/skill_promotion_pressure.md`.
- If you are reading live project-overlay family maturity, use `../mechanics/audit/docs/PUBLIC_SURFACE.md` and then `../generated/overlay_readiness.md`.
- If you are reading per-skill packaging membership or relationship topology, use `../generated/skill_bundle_index.md`, `../generated/skill_graph.md`, and then `../generated/release_manifest.json`.
- If you need one bounded ability-reader layer that stays subordinate to live skill bundles, use `../mechanics/rpg/parts/ability-reader-boundary/README.md`, `../mechanics/rpg/parts/loadout-posture/README.md`, and `../generated/skill_ability_cards.min.example.json`.
- If you are reading deferred workflow, recurring cross-repo follow-through, or session-harvest aftermath, start with `../QUESTBOOK.md` and `../mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md`.

## Shortest canonical route

1. `../skills/core/engineering/aoa-change-protocol/SKILL.md` - one concrete source-authored skill bundle.
2. `../SKILL_INDEX.md` - the current repo-wide skill map.
3. `../mechanics/release-support/docs/RUNTIME_PATH.md` - how to inspect and use a bounded skill object.
4. `../mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md` - how to build applicability maps, close out a session honestly, and hand off to harvest only when needed.
5. `session-harvests/README.md` - where bounded public candidate-harvest notes live before promotion.
6. `../mechanics/audit/docs/EVALUATION_PATH.md` - how to read behavior evidence.
7. `../mechanics/audit/docs/PUBLIC_SURFACE.md` - how to read derived status and governance.
8. `../mechanics/release-support/docs/RELEASING.md` - the bounded repo-level verification and release path.

## Read in this order

1. `../skills/core/engineering/aoa-change-protocol/SKILL.md` - one concrete source-authored starter bundle.
2. `../SKILL_INDEX.md` - the current skill map across the repo.
3. `../mechanics/release-support/docs/RUNTIME_PATH.md` - the runtime inspection guide for `pick -> inspect -> expand -> object use`.
4. `../mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md` - adaptive protocol for applicability maps, closeout, and harvest handoff.
5. `../mechanics/audit/docs/EVALUATION_PATH.md` - the evaluation evidence guide for matrix outputs and snapshot-backed coverage.
6. `../mechanics/audit/docs/PUBLIC_SURFACE.md` - the derived public-product and governance layer, kept separate from runtime inspection and evaluation evidence.
7. `../mechanics/boundary-bridge/docs/LAYER_POSITION.md` - repo-owned layer-position note for the boundary between techniques, skills, and playbooks.
8. `../mechanics/README.md` - owner-local skill mechanics route and package-card standard.
9. `../mechanics/OWNER_REQUEST_RECEIPTS.md` - owner-local receipts for AoA center requests assigned to `aoa-skills`.
10. `../mechanics/growth-cycle/README.md` - adaptive orchestration and session-growth lifecycle movement.
11. `../mechanics/checkpoint/README.md` - checkpoint-note protocol and reviewed closeout bridge boundary.
12. `../mechanics/method-growth/README.md` - reviewed candidate-lineage, owner-status, followthrough, and adoption lifecycle movement.
13. `../mechanics/rpg/README.md` - ability-card and loadout reader posture.
14. `../mechanics/antifragility/README.md` - fallback, via negativa, and collision-stress posture.
15. `../mechanics/agon/README.md` - Agon package-local mechanics route.
16. `ARCHITECTURE.md` - high-level model of the repository.
17. `../mechanics/boundary-bridge/docs/BRIDGE_SPEC.md` - how skills reference and compose techniques.
18. `REPOSITORY_STRUCTURE.md` - folder layout and conventions.
19. `../mechanics/ROADMAP.md` - roadmap router; package `ROADMAP.md` files own
    future contours.
20. `../mechanics/release-support/docs/RELEASING.md` - bounded release flow, release note shape, and repo-level validation path.
21. `../mechanics/release-support/docs/CODEX_PORTABLE_LAYER.md` - generated Codex-facing export contract for `.agents/skills/*`.
22. `../mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md` - owner refresh law for the portable export foundation when generated or adapter-facing surfaces drift.
23. `../mechanics/release-support/docs/LOCAL_ADAPTER_CONTRACT.md` - local runtime seams around that export, including the legacy activation shim.
24. `../mechanics/boundary-bridge/docs/OPENAI_SKILL_EXTENSIONS.md` and `../mechanics/boundary-bridge/docs/CODEX_SKILL_MCP_WIRING.md` - optional OpenAI metadata seam plus named MCP wiring guidance for the generated export.
25. `../mechanics/release-support/docs/INSTALL_AND_PROFILES.md` - install roots, skill-pack profiles, and disable-snippet helpers.
26. `../mechanics/release-support/docs/CONTEXT_RETENTION.md` - generated retention-support metadata around the export.
27. `../mechanics/release-support/docs/UI_METADATA_AND_ASSETS.md` - icon and UI metadata rules for the export.
28. `../mechanics/release-support/docs/CODEX_CONFIG_SNIPPETS.md` - generated disable-profile snippets and example config surfaces.
29. `../mechanics/release-support/legacy/waves/THIRD_WAVE.md` - portable-layer hardening for install, trust, and config surfaces.
30. `../mechanics/release-support/legacy/waves/FOURTH_WAVE.md` - dedicated-tool runtime seam added around the same export.
31. `../mechanics/release-support/docs/RUNTIME_SEAM_SECOND_PATH.md` - primary wave-4 runtime path for discover, disclose, activate, and compact.
32. `../mechanics/release-support/docs/RUNTIME_TOOL_CONTRACTS.md` - tool-shaped contract for the wave-4 runtime seam.
33. `../mechanics/release-support/docs/SESSION_COMPACTION.md` - session state and compaction behavior for long-running local wrappers.
34. `../mechanics/audit/docs/TRIGGER_EVALS.md` - policy-aware trigger-eval dataset and collision-family guidance.
35. `../mechanics/antifragility/parts/collision-stress-program/README.md` - additive stress-era collision coverage for timeout chaos, source-of-truth wins, and thin incident suppression.
36. `../mechanics/release-support/legacy/waves/SEVENTH_WAVE.md` - activation-quality wave for description-first evals and soft standards-conformance.
37. `../mechanics/audit/docs/DESCRIPTION_TRIGGER_EVALS.md` - description-first activation-contract dataset and coverage rules.
38. `../mechanics/audit/docs/SKILLS_REF_VALIDATION.md` - soft standards-conformance lane for the generated export.
39. `../mechanics/release-support/legacy/waves/EIGHTH_WAVE.md` - deterministic support-bundle wave for three high-risk skills.
40. `../mechanics/release-support/docs/DETERMINISTIC_RESOURCE_BUNDLES.md` - support-resource contract for canonical `scripts/`, `references/`, and `assets/`.
41. `../mechanics/boundary-bridge/docs/BRIDGE_FROM_AOA_SUPPORT_DIRS.md` - bridge posture between existing AoA support dirs and the wave-8 standard dirs.
42. `../mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md` - additive checkpoint-note contract that prepares reviewed closeout without replacing the explicit session-harvest family.
43. `../mechanics/method-growth/docs/MATURITY_MODEL.md` - documented status ladder, promotion rules, and canonical-candidate review guidance.
44. `../mechanics/method-growth/docs/PROMOTION_PATH.md` - public convention for moving skills through the maturity ladder.
45. `../mechanics/method-growth/docs/PROMOTION_PRESSURE.md` - lived-use review-pressure readout for non-canonical skills.
46. `../mechanics/boundary-bridge/docs/OVERLAY_SPEC.md` - repo-local contract for thin project overlays, including validator fixture packs and live exemplar packs.
47. `../mechanics/boundary-bridge/overlays/atm10/PROJECT_OVERLAY.md` - one current live family overlay pack.
48. `../mechanics/boundary-bridge/overlays/atm10/REVIEW.md` - family-level review surface for that live pack.
49. `../mechanics/boundary-bridge/overlays/abyss/PROJECT_OVERLAY.md` - another current live family overlay pack.
50. `../mechanics/boundary-bridge/overlays/abyss/REVIEW.md` - family-level review surface for that live pack.
51. `reviews/README.md` - public review-record conventions and review surfaces.
52. `../mechanics/release-support/legacy/waves/PHASED_SKILL_PLAN.md` - supplemental public plan for the scaffold expansion pass that established the early skill core.

## Core ideas

- techniques are the canonical source of reusable engineering knowledge
- skills are the agent-facing operational interface with self-contained execution meaning
- `../mechanics/boundary-bridge/docs/LAYER_POSITION.md` is the repo-owned boundary note for how skills inherit reusable practice from `aoa-techniques` while recurring scenario method stays in `aoa-playbooks`
- skills should be self-contained at runtime
- technique links are bridge evidence, not live runtime dependencies or automatic promotion blockers
- technique composition should happen at build time, not by live remote fetch
- stable skill execution may later be decomposed into techniques when it reveals reusable practice
- live exemplar overlay packs may live here as repo-local examples
- live exemplar overlay packs should include a family-level review doc and bundle-local review checklists
- real downstream overlay adoption still belongs in downstream repositories
- runtime inspection lives in `../mechanics/release-support/docs/RUNTIME_PATH.md`
- `scripts/inspect_skill.py` is the read-only CLI entrypoint for the same runtime path
- `../generated/skill_walkthroughs.md` is the human-readable walkthrough matrix for that path
- evaluation evidence lives in `../mechanics/audit/docs/EVALUATION_PATH.md`
- `scripts/report_skill_evaluation.py` is the read-only CLI entrypoint for the evaluation matrix layer
- `../generated/skill_evaluation_matrix.md` is the human-readable derived evidence matrix for that layer
- `scripts/report_technique_drift.py` is a related bridge report CLI when upstream technique drift must be checked before interpreting skill evidence
- `tests/fixtures/skill_evaluation_cases.yaml` is the committed evaluation matrix input
- public-product and governance signals live in `../mechanics/audit/docs/PUBLIC_SURFACE.md`
- `../generated/public_surface.md` is the derived status and promotion surface
- `../generated/governance_backlog.md` is the per-skill maintenance and readiness surface
- `../generated/skill_promotion_pressure.md` is the derived lived-use pressure surface that routes heavily used non-canonical skills to review or blocker repair
- `../generated/overlay_readiness.md` is the family-maturity surface for repo-local project overlays
- `../generated/skill_bundle_index.md` is the per-skill packaging, profile-membership, and technique-lineage surface
- `../generated/skill_graph.md` is the relationship topology surface across skills, techniques, install profiles, and portable artifact groups
- the three layers are intentionally separate: one is for selecting and using an object, one is for reading evaluation evidence, and one is for reading derived public state
- generated catalogs, capsules, and full sections are derived reader/runtime surfaces, not source-of-truth artifacts
- public governance signaling should stay derived from existing status, review, lineage, and evaluation facts
- repo-level release identity lives separately in `../CHANGELOG.md`, `../mechanics/release-support/docs/RELEASING.md`, the Git tag, and the GitHub release body

## Layers

- `aoa-techniques` - technique canon
- `aoa-skills` - Codex skill canon
- `aoa-playbooks` - recurring scenario method and executable route canon
- repo `mechanics/` - owner-local skill-layer movement around AoA mechanics
- repo `.agents/skills` - generated Codex-facing export derived from canonical skill sources

## Current repository phase

This repository now has a mixed-status public core with first support artifacts,
honest bridge manifests with pinned source refs, and local validation coverage.
The live governance counts now belong to `../generated/public_surface.md` and `../generated/governance_backlog.md`, while this docs map stays focused on how to read the layers.
The repository now also has a documented maturity ladder and promotion guidance.
The repository now also has a documented public promotion path in `../mechanics/method-growth/docs/PROMOTION_PATH.md`.
The repository now also has a lived-use promotion-pressure readout in `../mechanics/method-growth/docs/PROMOTION_PRESSURE.md` and `../generated/skill_promotion_pressure.md`.
The repository now also has a repo-level release runbook in `../mechanics/release-support/docs/RELEASING.md` and a bounded release-check CLI at `../scripts/release_check.py`.
The repository now also has a runtime inspection guide in `../mechanics/release-support/docs/RUNTIME_PATH.md`, an evaluation evidence guide in `../mechanics/audit/docs/EVALUATION_PATH.md`, a derived evaluation matrix in `../generated/skill_evaluation_matrix.md`, and a separate derived public-surface layer in `../mechanics/audit/docs/PUBLIC_SURFACE.md` and `../generated/public_surface.md`.
The repository now also has a generated Codex-facing export in `../.agents/skills/`, portable discovery surfaces in `../generated/agent_skill_catalog*.json`, a legacy-compatible local adapter seam in `../mechanics/release-support/docs/LOCAL_ADAPTER_CONTRACT.md` and `../generated/local_adapter_manifest*.json`, named MCP dependency wiring guidance in `../mechanics/boundary-bridge/docs/CODEX_SKILL_MCP_WIRING.md` plus example scaffolds under `../mechanics/boundary-bridge/examples/openai.*.example.yaml`, a wave-4 runtime seam in `../mechanics/release-support/legacy/waves/FOURTH_WAVE.md`, `../mechanics/release-support/docs/RUNTIME_SEAM_SECOND_PATH.md`, `../mechanics/release-support/docs/RUNTIME_TOOL_CONTRACTS.md`, `../mechanics/release-support/docs/SESSION_COMPACTION.md`, and `../generated/runtime_*.json`, wave-3 install and trust surfaces in `../mechanics/release-support/docs/INSTALL_AND_PROFILES.md`, `../mechanics/release-support/docs/CONTEXT_RETENTION.md`, `../mechanics/release-support/docs/UI_METADATA_AND_ASSETS.md`, `../mechanics/release-support/docs/CODEX_CONFIG_SNIPPETS.md`, policy-aware trigger-eval data documented in `../mechanics/audit/docs/TRIGGER_EVALS.md`, and a wave-8 deterministic support-resource bridge documented in `../mechanics/release-support/legacy/waves/EIGHTH_WAVE.md`, `../mechanics/release-support/docs/DETERMINISTIC_RESOURCE_BUNDLES.md`, `../mechanics/boundary-bridge/docs/BRIDGE_FROM_AOA_SUPPORT_DIRS.md`, and `../generated/deterministic_resource_manifest.json`.
The next focus is keeping selection, evidence reading, public status, and live overlay family maturity in their own layers while using the derived governance layer for cross-family overlay maintenance and packaging prep through `../generated/governance_backlog.md`, `../generated/overlay_readiness.md`, `../generated/skill_bundle_index.md`, `../generated/skill_graph.md`, and `../generated/release_manifest.json`.
The repository now also permits thin live exemplar overlay packs such as `mechanics/boundary-bridge/overlays/atm10/PROJECT_OVERLAY.md`, `mechanics/boundary-bridge/overlays/abyss/PROJECT_OVERLAY.md`, and matching `skills/project/atm10/<skill>/` plus `skills/project/abyss/<skill>/` bundles.
Those live exemplar packs also have family-level review docs at `mechanics/boundary-bridge/overlays/atm10/REVIEW.md` and `mechanics/boundary-bridge/overlays/abyss/REVIEW.md`.
Those overlays remain repo-local examples rather than live downstream integrations, and their maturity is read through `../generated/overlay_readiness.md` rather than core governance lanes.
`../mechanics/ROADMAP.md` remains the mechanics roadmap router. Package
roadmaps own their future contours, and release-support owns the next packaging
follow-up after compatibility/lineage depth: import/export polish rather than
another packaging-contract bootstrap.
`../mechanics/release-support/legacy/waves/PHASED_SKILL_PLAN.md` records the scaffold expansion that established the original skill-core rollout.
