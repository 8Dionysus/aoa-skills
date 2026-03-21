# Docs map

`aoa-skills` is the Codex-facing companion to `aoa-techniques`.

Where `aoa-techniques` stores public, reusable, validated engineering techniques,
`aoa-skills` stores reusable agent skills that compose one or more techniques into
an executable workflow for Codex.

## Read in this order

1. `RUNTIME_PATH.md` — the runtime inspection guide for `pick -> inspect -> expand -> object use`.
2. `PUBLIC_SURFACE.md` — the derived public-product and governance layer, kept separate from runtime inspection.
3. `ARCHITECTURE.md` — high-level model of the repository.
4. `BRIDGE_SPEC.md` — how skills reference and compose techniques.
5. `REPOSITORY_STRUCTURE.md` — folder layout and conventions.
6. `ROADMAP.md` — canonical public roadmap for repository evolution.
7. `MATURITY_MODEL.md` — documented status ladder, promotion rules, and canonical-candidate review guidance.
8. `PROMOTION_PATH.md` — public convention for moving skills through the maturity ladder.
9. `reviews/README.md` — public review-record conventions and review surfaces.
10. `PHASED_SKILL_PLAN.md` — supplemental public plan for the scaffold expansion pass that established the current core.

## Core ideas

- techniques are the canonical source of reusable engineering knowledge
- skills are the agent-facing operational interface
- skills should be self-contained at runtime
- technique composition should happen at build time, not by live remote fetch
- project-specific overlays belong in project repositories, not in the public core
- runtime inspection lives in `RUNTIME_PATH.md`
- `scripts/inspect_skill.py` is the read-only CLI entrypoint for the same runtime path
- `../generated/skill_walkthroughs.md` is the human-readable walkthrough matrix for that path
- public-product and governance signals live in `PUBLIC_SURFACE.md`
- the two layers are intentionally separate: one is for selecting and using an object, the other is for reading derived public state
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
The repository now also has a runtime inspection guide in `RUNTIME_PATH.md` and a separate derived public-surface layer in `PUBLIC_SURFACE.md` and `../generated/public_surface.md`.
The next focus is keeping selection and execution in `RUNTIME_PATH.md` while using the derived governance layer to drive pending-lineage closure, candidate review, and stronger public product-surface clarity.
`ROADMAP.md` remains the canonical public roadmap.
`PHASED_SKILL_PLAN.md` records the scaffold expansion that established the original 13-skill surface.
