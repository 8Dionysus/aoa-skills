# Docs map

`aoa-skills` is the Codex-facing companion to `aoa-techniques`.

Where `aoa-techniques` stores public, reusable, validated engineering techniques,
`aoa-skills` stores reusable agent skills that compose one or more techniques into
an executable workflow for Codex.

## Quick route by question

- If you want one concrete source-authored skill before any derived layer, start with `../skills/aoa-change-protocol/SKILL.md` and then `RUNTIME_PATH.md`.
- If you want the current canonical surface at a glance, start with `../SKILL_INDEX.md`.
- If you are choosing or using a skill, start with `RUNTIME_PATH.md`.
- If you need named MCP dependency wiring or workspace-server alignment for the generated Codex export, start with `CODEX_SKILL_MCP_WIRING.md` and `OPENAI_SKILL_EXTENSIONS.md`.
- If you are checking repeated export drift, stale generated discovery surfaces, or owner refresh posture for the portable layer, start with `COMPONENT_REFRESH_LAW.md`, then `CODEX_PORTABLE_LAYER.md`, and then `LOCAL_ADAPTER_CONTRACT.md`.
- If you need to decide which skills apply now, which belong to closeout, and which belong to harvest, start with `ADAPTIVE_SKILL_ORCHESTRATION.md`.
- If you need a committed bounded note for reusable session outputs that are not yet skill reviews or owner-layer truth, start with `session-harvests/README.md`.
- If you need additive degraded, fallback, or receipt-authoring posture for future skills, start with `ANTIFRAGILITY_SKILL_ADDENDUM.md`.
- If you need a lightweight checkpoint-aware note before post-session harvest, start with `CHECKPOINT_NOTE_PATH.md`.
- If you need the checkpoint-to-reviewed-candidate identity seam, start with `CANDIDATE_LINEAGE_CONTRACT.md`, then `CANDIDATE_REF_REFINERY.md`, and then `CHECKPOINT_NOTE_PATH.md`.
- If you need the first reviewed owner-status landing and the next bounded verdict after `candidate_ref` exists, start with `OWNER_STATUS_SURFACES.md`, then `GOVERNED_FOLLOWTHROUGH.md`, and then `CANDIDATE_REF_REFINERY.md`.
- If you need the later reviewed session-growth kernel packet and receipt examples after closeout carry and `candidate_ref` already exist, start with `SESSION_GROWTH_KERNEL_MATURITY.md`.
- If you are checking evidence, fixtures, or snapshot-backed coverage, start with `EVALUATION_PATH.md`.
- If you are reading status, promotion, or governance state, start with `PUBLIC_SURFACE.md`.
- If you are reading live project-overlay family maturity, use `PUBLIC_SURFACE.md` and then `../generated/overlay_readiness.md`.
- If you are reading per-skill packaging membership or relationship topology, use `../generated/skill_bundle_index.md`, `../generated/skill_graph.md`, and then `../generated/release_manifest.json`.
- If you need one bounded ability-reader layer that stays subordinate to live skill bundles, use `SKILL_ABILITY_MODEL.md`, `ABILITY_LOADOUT_POSTURE.md`, and `../generated/skill_ability_cards.min.example.json`.
- If you are reading deferred workflow, recurring cross-repo follow-through, or session-harvest aftermath, start with `../QUESTBOOK.md` and `QUESTBOOK_SKILL_INTEGRATION.md`.

## Shortest canonical route

1. `../skills/aoa-change-protocol/SKILL.md` - one concrete source-authored skill bundle.
2. `../SKILL_INDEX.md` - the current repo-wide skill map.
3. `RUNTIME_PATH.md` - how to inspect and use a bounded skill object.
4. `ADAPTIVE_SKILL_ORCHESTRATION.md` - how to build applicability maps, close out a session honestly, and hand off to harvest only when needed.
5. `session-harvests/README.md` - where bounded public candidate-harvest notes live before promotion.
6. `EVALUATION_PATH.md` - how to read behavior evidence.
7. `PUBLIC_SURFACE.md` - how to read derived status and governance.
8. `RELEASING.md` - the bounded repo-level verification and release path.

## Read in this order

1. `../skills/aoa-change-protocol/SKILL.md` - one concrete source-authored starter bundle.
2. `../SKILL_INDEX.md` - the current skill map across the repo.
3. `RUNTIME_PATH.md` - the runtime inspection guide for `pick -> inspect -> expand -> object use`.
4. `ADAPTIVE_SKILL_ORCHESTRATION.md` - adaptive protocol for applicability maps, closeout, and harvest handoff.
5. `EVALUATION_PATH.md` - the evaluation evidence guide for matrix outputs and snapshot-backed coverage.
6. `PUBLIC_SURFACE.md` - the derived public-product and governance layer, kept separate from runtime inspection and evaluation evidence.
7. `LAYER_POSITION.md` - repo-owned layer-position note for the boundary between techniques, skills, and playbooks.
8. `ARCHITECTURE.md` - high-level model of the repository.
9. `BRIDGE_SPEC.md` - how skills reference and compose techniques.
10. `REPOSITORY_STRUCTURE.md` - folder layout and conventions.
11. `ROADMAP.md` - canonical public roadmap for repository evolution.
12. `RELEASING.md` - bounded release flow, release note shape, and repo-level validation path.
13. `CODEX_PORTABLE_LAYER.md` - generated Codex-facing export contract for `.agents/skills/*`.
14. `COMPONENT_REFRESH_LAW.md` - owner refresh law for the portable export foundation when generated or adapter-facing surfaces drift.
15. `LOCAL_ADAPTER_CONTRACT.md` - local runtime seams around that export, including the legacy activation shim.
16. `OPENAI_SKILL_EXTENSIONS.md` and `CODEX_SKILL_MCP_WIRING.md` - optional OpenAI metadata seam plus named MCP wiring guidance for the generated export.
17. `INSTALL_AND_PROFILES.md` - install roots, skill-pack profiles, and disable-snippet helpers.
18. `CONTEXT_RETENTION.md` - generated retention-support metadata around the export.
19. `UI_METADATA_AND_ASSETS.md` - icon and UI metadata rules for the export.
20. `CODEX_CONFIG_SNIPPETS.md` - generated disable-profile snippets and example config surfaces.
21. `THIRD_WAVE.md` - portable-layer hardening for install, trust, and config surfaces.
22. `FOURTH_WAVE.md` - dedicated-tool runtime seam added around the same export.
23. `RUNTIME_SEAM_SECOND_PATH.md` - primary wave-4 runtime path for discover, disclose, activate, and compact.
24. `RUNTIME_TOOL_CONTRACTS.md` - tool-shaped contract for the wave-4 runtime seam.
25. `SESSION_COMPACTION.md` - session state and compaction behavior for long-running local wrappers.
26. `TRIGGER_EVALS.md` - policy-aware trigger-eval dataset and collision-family guidance.
27. `SEVENTH_WAVE.md` - activation-quality wave for description-first evals and soft standards-conformance.
28. `DESCRIPTION_TRIGGER_EVALS.md` - description-first activation-contract dataset and coverage rules.
29. `SKILLS_REF_VALIDATION.md` - soft standards-conformance lane for the generated export.
30. `EIGHTH_WAVE.md` - deterministic support-bundle wave for three high-risk skills.
31. `DETERMINISTIC_RESOURCE_BUNDLES.md` - support-resource contract for canonical `scripts/`, `references/`, and `assets/`.
32. `BRIDGE_FROM_AOA_SUPPORT_DIRS.md` - bridge posture between existing AoA support dirs and the wave-8 standard dirs.
33. `CHECKPOINT_NOTE_PATH.md` - additive checkpoint-note contract that prepares reviewed closeout without replacing the explicit session-harvest family.
34. `MATURITY_MODEL.md` - documented status ladder, promotion rules, and canonical-candidate review guidance.
35. `PROMOTION_PATH.md` - public convention for moving skills through the maturity ladder.
36. `OVERLAY_SPEC.md` - repo-local contract for thin project overlays, including fixture stubs and live exemplar packs.
37. `overlays/atm10/PROJECT_OVERLAY.md` - one current live family overlay pack.
38. `overlays/atm10/REVIEW.md` - family-level review surface for that live pack.
39. `overlays/abyss/PROJECT_OVERLAY.md` - another current live family overlay pack.
40. `overlays/abyss/REVIEW.md` - family-level review surface for that live pack.
41. `reviews/README.md` - public review-record conventions and review surfaces.
42. `PHASED_SKILL_PLAN.md` - supplemental public plan for the scaffold expansion pass that established the early skill core.

## Core ideas

- techniques are the canonical source of reusable engineering knowledge
- skills are the agent-facing operational interface
- `LAYER_POSITION.md` is the repo-owned boundary note for how skills inherit reusable practice from `aoa-techniques` while recurring scenario method stays in `aoa-playbooks`
- skills should be self-contained at runtime
- technique composition should happen at build time, not by live remote fetch
- live exemplar overlay packs may live here as repo-local examples
- live exemplar overlay packs should include a family-level review doc and bundle-local review checklists
- real downstream overlay adoption still belongs in downstream repositories
- runtime inspection lives in `RUNTIME_PATH.md`
- `scripts/inspect_skill.py` is the read-only CLI entrypoint for the same runtime path
- `../generated/skill_walkthroughs.md` is the human-readable walkthrough matrix for that path
- evaluation evidence lives in `EVALUATION_PATH.md`
- `scripts/report_skill_evaluation.py` is the read-only CLI entrypoint for the evaluation matrix layer
- `../generated/skill_evaluation_matrix.md` is the human-readable derived evidence matrix for that layer
- `scripts/report_technique_drift.py` is a related bridge report CLI when upstream technique drift must be checked before interpreting skill evidence
- `tests/fixtures/skill_evaluation_cases.yaml` is the committed evaluation matrix input
- public-product and governance signals live in `PUBLIC_SURFACE.md`
- `../generated/public_surface.md` is the derived status and promotion surface
- `../generated/governance_backlog.md` is the per-skill maintenance and readiness surface
- `../generated/overlay_readiness.md` is the family-maturity surface for repo-local project overlays
- `../generated/skill_bundle_index.md` is the per-skill packaging, profile-membership, and technique-lineage surface
- `../generated/skill_graph.md` is the relationship topology surface across skills, techniques, install profiles, and portable artifact groups
- the three layers are intentionally separate: one is for selecting and using an object, one is for reading evaluation evidence, and one is for reading derived public state
- generated catalogs, capsules, and full sections are derived reader/runtime surfaces, not source-of-truth artifacts
- public governance signaling should stay derived from existing status, review, lineage, and evaluation facts
- repo-level release identity lives separately in `../CHANGELOG.md`, `RELEASING.md`, the Git tag, and the GitHub release body

## Layers

- `aoa-techniques` - technique canon
- `aoa-skills` - Codex skill canon
- `aoa-playbooks` - recurring scenario method and executable route canon
- repo `.agents/skills` - generated Codex-facing export derived from canonical skill sources

## Current repository phase

This repository now has a mixed-status public core of 20 skills with first support artifacts,
honest bridge manifests with pinned source refs, and local validation coverage.
The live governance counts now belong to `../generated/public_surface.md` and `../generated/governance_backlog.md`, while this docs map stays focused on how to read the layers.
The repository now also has a documented maturity ladder and promotion guidance.
The repository now also has a documented public promotion path in `PROMOTION_PATH.md`.
The repository now also has a repo-level release runbook in `RELEASING.md` and a bounded release-check CLI at `../scripts/release_check.py`.
The repository now also has a runtime inspection guide in `RUNTIME_PATH.md`, an evaluation evidence guide in `EVALUATION_PATH.md`, a derived evaluation matrix in `../generated/skill_evaluation_matrix.md`, and a separate derived public-surface layer in `PUBLIC_SURFACE.md` and `../generated/public_surface.md`.
The repository now also has a generated Codex-facing export in `../.agents/skills/`, portable discovery surfaces in `../generated/agent_skill_catalog*.json`, a legacy-compatible local adapter seam in `LOCAL_ADAPTER_CONTRACT.md` and `../generated/local_adapter_manifest*.json`, named MCP dependency wiring guidance in `CODEX_SKILL_MCP_WIRING.md` plus example scaffolds under `../examples/openai.*.example.yaml`, a wave-4 runtime seam in `FOURTH_WAVE.md`, `RUNTIME_SEAM_SECOND_PATH.md`, `RUNTIME_TOOL_CONTRACTS.md`, `SESSION_COMPACTION.md`, and `../generated/runtime_*.json`, wave-3 install and trust surfaces in `INSTALL_AND_PROFILES.md`, `CONTEXT_RETENTION.md`, `UI_METADATA_AND_ASSETS.md`, `CODEX_CONFIG_SNIPPETS.md`, policy-aware trigger-eval data documented in `TRIGGER_EVALS.md`, and a wave-8 deterministic support-resource bridge documented in `EIGHTH_WAVE.md`, `DETERMINISTIC_RESOURCE_BUNDLES.md`, `BRIDGE_FROM_AOA_SUPPORT_DIRS.md`, and `../generated/deterministic_resource_manifest.json`.
The next focus is keeping selection, evidence reading, public status, and live overlay family maturity in their own layers while using the derived governance layer for cross-family overlay maintenance and packaging prep through `../generated/governance_backlog.md`, `../generated/overlay_readiness.md`, `../generated/skill_bundle_index.md`, `../generated/skill_graph.md`, and `../generated/release_manifest.json`.
The repository now also permits thin live exemplar overlay packs such as `docs/overlays/atm10/PROJECT_OVERLAY.md`, `docs/overlays/abyss/PROJECT_OVERLAY.md`, and matching `skills/atm10-*` plus `skills/abyss-*` bundles.
Those live exemplar packs also have family-level review docs at `docs/overlays/atm10/REVIEW.md` and `docs/overlays/abyss/REVIEW.md`.
Those overlays remain repo-local examples rather than live downstream integrations, and their maturity is read through `../generated/overlay_readiness.md` rather than core governance lanes.
`ROADMAP.md` remains the canonical public roadmap, and the next packaging follow-up after compatibility/lineage depth is import/export polish rather than another packaging-contract bootstrap.
`PHASED_SKILL_PLAN.md` records the scaffold expansion that established the original skill-core rollout.
