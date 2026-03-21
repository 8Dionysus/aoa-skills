# Docs map

`aoa-skills` is the Codex-facing companion to `aoa-techniques`.

Where `aoa-techniques` stores public, reusable, validated engineering techniques,
`aoa-skills` stores reusable agent skills that compose one or more techniques into
an executable workflow for Codex.

## Read in this order

1. `PUBLIC_SURFACE.md` — how to read the current public-product and governance signals.
2. `ARCHITECTURE.md` — high-level model of the repository.
3. `BRIDGE_SPEC.md` — how skills reference and compose techniques.
4. `REPOSITORY_STRUCTURE.md` — folder layout and conventions.
5. `ROADMAP.md` — canonical public roadmap for repository evolution.
6. `MATURITY_MODEL.md` — documented status ladder, promotion rules, and canonical-candidate review guidance.
7. `PROMOTION_PATH.md` — public convention for moving skills through the maturity ladder.
8. `reviews/README.md` — public review-record conventions and review surfaces.
9. `PHASED_SKILL_PLAN.md` — supplemental public plan for the scaffold expansion pass that established the current core.

## Core ideas

- techniques are the canonical source of reusable engineering knowledge
- skills are the agent-facing operational interface
- skills should be self-contained at runtime
- technique composition should happen at build time, not by live remote fetch
- project-specific overlays belong in project repositories, not in the public core
- generated catalogs, capsules, and full sections are derived reader/runtime surfaces, not source-of-truth artifacts
- public governance and release signaling should stay derived from existing status, review, lineage, and evaluation facts

The current runtime path is:

`pick -> inspect -> expand -> object use`

## Layers

- `aoa-techniques` — technique canon
- `aoa-skills` — Codex skill canon
- project `.agents/skills` — repo-specific overlays and risk policies

## Current repository phase

This repository now has a non-scaffold public core of 13 skills with first support artifacts,
honest bridge manifests with pinned source refs, and local validation coverage.
The repository now also has its first `canonical` skills, evaluated coverage across the remaining current skill surface, and autonomy and trigger-boundary evaluation checks across that public core.
The repository now also has a documented maturity ladder and promotion guidance.
The repository now also has a documented public promotion path in `PROMOTION_PATH.md`.
The repository now also has a derived public-surface layer in `PUBLIC_SURFACE.md` and `../generated/public_surface.md`.
The next focus is using that derived governance layer to drive pending-lineage closure, candidate review, and stronger public product-surface clarity.
`ROADMAP.md` remains the canonical public roadmap.
`PHASED_SKILL_PLAN.md` records the scaffold expansion that established the current 13-skill surface.
