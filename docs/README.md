# Docs map

`aoa-skills` is the Codex-facing companion to `aoa-techniques`.

Where `aoa-techniques` stores public, reusable, validated engineering techniques,
`aoa-skills` stores reusable agent skills that compose one or more techniques into
an executable workflow for Codex.

## Read in this order

1. `RUNTIME_PATH.md` — the runtime inspection guide for `pick -> inspect -> expand -> object use`.
2. `EVALUATION_PATH.md` — the evaluation evidence guide for matrix outputs and snapshot-backed coverage.
3. `PUBLIC_SURFACE.md` — the derived public-product and governance layer, kept separate from runtime inspection and evaluation evidence.
4. `LAYER_POSITION.md` — repo-owned layer-position note for the boundary between techniques, skills, and playbooks.
5. `ARCHITECTURE.md` — high-level model of the repository.
6. `BRIDGE_SPEC.md` — how skills reference and compose techniques.
7. `REPOSITORY_STRUCTURE.md` — folder layout and conventions.
8. `ROADMAP.md` — canonical public roadmap for repository evolution.
9. `RELEASING.md` — bounded release flow, release note shape, and repo-level validation path.
10. `CODEX_PORTABLE_LAYER.md` — generated Codex-facing export contract for `.agents/skills/*`.
11. `LOCAL_ADAPTER_CONTRACT.md` — local runtime seams around that export, including the legacy activation shim.
12. `OPENAI_SKILL_EXTENSIONS.md` — optional OpenAI metadata seam for portable export files.
13. `INSTALL_AND_PROFILES.md` — install roots, skill-pack profiles, and disable-snippet helpers.
14. `CONTEXT_RETENTION.md` — generated retention-support metadata around the export.
15. `UI_METADATA_AND_ASSETS.md` — icon and UI metadata rules for the export.
16. `CODEX_CONFIG_SNIPPETS.md` — generated disable-profile snippets and example config surfaces.
17. `THIRD_WAVE.md` — portable-layer hardening for install, trust, and config surfaces.
18. `FOURTH_WAVE.md` — dedicated-tool runtime seam added around the same export.
19. `RUNTIME_SEAM_SECOND_PATH.md` — primary wave-4 runtime path for discover, disclose, activate, and compact.
20. `RUNTIME_TOOL_CONTRACTS.md` — tool-shaped contract for the wave-4 runtime seam.
21. `SESSION_COMPACTION.md` — session state and compaction behavior for long-running local wrappers.
22. `TRIGGER_EVALS.md` — policy-aware trigger-eval dataset and collision-family guidance.
23. `SEVENTH_WAVE.md` — activation-quality wave for description-first evals and soft standards-conformance.
24. `DESCRIPTION_TRIGGER_EVALS.md` — description-first activation-contract dataset and coverage rules.
25. `SKILLS_REF_VALIDATION.md` — soft standards-conformance lane for the generated export.
26. `EIGHTH_WAVE.md` — deterministic support-bundle wave for three high-risk skills.
27. `DETERMINISTIC_RESOURCE_BUNDLES.md` — support-resource contract for canonical `scripts/`, `references/`, and `assets/`.
28. `BRIDGE_FROM_AOA_SUPPORT_DIRS.md` — bridge posture between existing AoA support dirs and the wave-8 standard dirs.
29. `MATURITY_MODEL.md` — documented status ladder, promotion rules, and canonical-candidate review guidance.
30. `PROMOTION_PATH.md` — public convention for moving skills through the maturity ladder.
31. `OVERLAY_SPEC.md` — repo-local contract for thin project overlays, including fixture stubs and live exemplar packs.
32. `overlays/atm10/PROJECT_OVERLAY.md` — first live exemplar family overlay pack.
33. `overlays/atm10/REVIEW.md` — family-level review surface for the live exemplar pack.
34. `reviews/README.md` — public review-record conventions and review surfaces.
35. `PHASED_SKILL_PLAN.md` — supplemental public plan for the scaffold expansion pass that established the early skill core.

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
- `../generated/governance_backlog.md` is the maintenance and readiness surface
- `../generated/skill_bundle_index.md` and `../generated/skill_graph.md` are packaging and relationship surfaces
- the three layers are intentionally separate: one is for selecting and using an object, one is for reading evaluation evidence, and one is for reading derived public state
- generated catalogs, capsules, and full sections are derived reader/runtime surfaces, not source-of-truth artifacts
- public governance signaling should stay derived from existing status, review, lineage, and evaluation facts
- repo-level release identity lives separately in `../CHANGELOG.md`, `RELEASING.md`, the Git tag, and the GitHub release body

## Layers

- `aoa-techniques` — technique canon
- `aoa-skills` — Codex skill canon
- `aoa-playbooks` — recurring scenario method and executable route canon
- repo `.agents/skills` — generated Codex-facing export derived from canonical skill sources

## Current repository phase

This repository now has a mixed-status public core of 17 skills with first support artifacts,
honest bridge manifests with pinned source refs, and local validation coverage.
The live governance counts now belong to `../generated/public_surface.md` and `../generated/governance_backlog.md`, while this docs map stays focused on how to read the layers.
The repository now also has a documented maturity ladder and promotion guidance.
The repository now also has a documented public promotion path in `PROMOTION_PATH.md`.
The repository now also has a repo-level release runbook in `RELEASING.md` and a bounded release-check CLI at `../scripts/release_check.py`.
The repository now also has a runtime inspection guide in `RUNTIME_PATH.md`, an evaluation evidence guide in `EVALUATION_PATH.md`, a derived evaluation matrix in `../generated/skill_evaluation_matrix.md`, and a separate derived public-surface layer in `PUBLIC_SURFACE.md` and `../generated/public_surface.md`.
The repository now also has a generated Codex-facing export in `../.agents/skills/`, portable discovery surfaces in `../generated/agent_skill_catalog*.json`, a legacy-compatible local adapter seam in `LOCAL_ADAPTER_CONTRACT.md` and `../generated/local_adapter_manifest*.json`, a wave-4 runtime seam in `FOURTH_WAVE.md`, `RUNTIME_SEAM_SECOND_PATH.md`, `RUNTIME_TOOL_CONTRACTS.md`, `SESSION_COMPACTION.md`, and `../generated/runtime_*.json`, wave-3 install and trust surfaces in `INSTALL_AND_PROFILES.md`, `CONTEXT_RETENTION.md`, `UI_METADATA_AND_ASSETS.md`, `CODEX_CONFIG_SNIPPETS.md`, policy-aware trigger-eval data documented in `TRIGGER_EVALS.md`, and a wave-8 deterministic support-resource bridge documented in `EIGHTH_WAVE.md`, `DETERMINISTIC_RESOURCE_BUNDLES.md`, `BRIDGE_FROM_AOA_SUPPORT_DIRS.md`, and `../generated/deterministic_resource_manifest.json`.
The next focus is keeping selection, evidence reading, and public status in their own layers while using the derived governance layer to drive candidate review, overlay maturity, stronger public product-surface clarity, and packaging prep through `../generated/governance_backlog.md`, `../generated/skill_bundle_index.md`, and `../generated/skill_graph.md`.
The repository now also permits thin live exemplar overlay packs such as `docs/overlays/atm10/PROJECT_OVERLAY.md` and matching `skills/atm10-*` bundles.
Those live exemplar packs also have a family-level review doc at `docs/overlays/atm10/REVIEW.md`.
Those overlays remain repo-local examples rather than live downstream integrations.
`ROADMAP.md` remains the canonical public roadmap.
`PHASED_SKILL_PLAN.md` records the scaffold expansion that established the original skill-core rollout.
