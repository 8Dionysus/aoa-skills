# Docs map

`aoa-skills` is the Codex-facing companion to `aoa-techniques`.

Where `aoa-techniques` stores public, reusable, validated engineering techniques,
`aoa-skills` stores reusable agent skills that compose one or more techniques into
an executable workflow for Codex.

## Read in this order

1. `RUNTIME_PATH.md` — the runtime inspection guide for `pick -> inspect -> expand -> object use`.
2. `EVALUATION_PATH.md` — the evaluation evidence guide for matrix outputs and snapshot-backed coverage.
3. `PUBLIC_SURFACE.md` — the derived public-product and governance layer, kept separate from runtime inspection and evaluation evidence.
4. `ARCHITECTURE.md` — high-level model of the repository.
5. `BRIDGE_SPEC.md` — how skills reference and compose techniques.
6. `REPOSITORY_STRUCTURE.md` — folder layout and conventions.
7. `ROADMAP.md` — canonical public roadmap for repository evolution.
8. `MATURITY_MODEL.md` — documented status ladder, promotion rules, and canonical-candidate review guidance.
9. `PROMOTION_PATH.md` — public convention for moving skills through the maturity ladder.
10. `OVERLAY_SPEC.md` — repo-local contract for thin project overlays, including fixture stubs and live exemplar packs.
11. `overlays/atm10/PROJECT_OVERLAY.md` — first live exemplar family overlay pack.
12. `reviews/README.md` — public review-record conventions and review surfaces.
13. `PHASED_SKILL_PLAN.md` — supplemental public plan for the scaffold expansion pass that established the early skill core.

## Core ideas

- techniques are the canonical source of reusable engineering knowledge
- skills are the agent-facing operational interface
- skills should be self-contained at runtime
- technique composition should happen at build time, not by live remote fetch
- live exemplar overlay packs may live here as repo-local examples
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
- public governance and release signaling should stay derived from existing status, review, lineage, and evaluation facts

## Layers

- `aoa-techniques` — technique canon
- `aoa-skills` — Codex skill canon
- project `.agents/skills` — repo-specific overlays and risk policies

## Current repository phase

This repository now has a non-scaffold public core of 14 skills with first support artifacts,
honest bridge manifests with pinned source refs, and local validation coverage.
The repository now also has its first `canonical` skills, evaluated coverage across the remaining current skill surface, and autonomy and trigger-boundary evaluation checks across that public core.
The repository now also has a documented maturity ladder and promotion guidance.
The repository now also has a documented public promotion path in `PROMOTION_PATH.md`.
The repository now also has a runtime inspection guide in `RUNTIME_PATH.md`, an evaluation evidence guide in `EVALUATION_PATH.md`, a derived evaluation matrix in `../generated/skill_evaluation_matrix.md`, and a separate derived public-surface layer in `PUBLIC_SURFACE.md` and `../generated/public_surface.md`.
The next focus is keeping selection, evidence reading, and public status in their own layers while using the derived governance layer to drive pending-lineage closure, candidate review, and stronger public product-surface clarity through `../generated/governance_backlog.md`, `../generated/skill_bundle_index.md`, and `../generated/skill_graph.md`.
The repository now also permits thin live exemplar overlay packs such as `docs/overlays/atm10/PROJECT_OVERLAY.md` and matching `skills/atm10-*` bundles.
Those overlays remain repo-local examples rather than live downstream integrations.
`ROADMAP.md` remains the canonical public roadmap.
`PHASED_SKILL_PLAN.md` records the scaffold expansion that established the original skill-core rollout.
