# Docs map

`aoa-skills` is the Codex-facing companion to `aoa-techniques`.

Where `aoa-techniques` stores public, reusable, validated engineering techniques,
`aoa-skills` stores reusable agent skills that compose one or more techniques into
an executable workflow for Codex.

## Read in this order

1. `ARCHITECTURE.md` — high-level model of the repository.
2. `BRIDGE_SPEC.md` — how skills reference and compose techniques.
3. `REPOSITORY_STRUCTURE.md` — folder layout and conventions.
4. `ROADMAP.md` — canonical public roadmap for repository evolution.
5. `PHASED_SKILL_PLAN.md` — supplemental public plan for the current scaffold expansion pass.

## Core ideas

- techniques are the canonical source of reusable engineering knowledge
- skills are the agent-facing operational interface
- skills should be self-contained at runtime
- technique composition should happen at build time, not by live remote fetch
- project-specific overlays belong in project repositories, not in the public core

## Layers

- `aoa-techniques` — technique canon
- `aoa-skills` — Codex skill canon
- project `.agents/skills` — repo-specific overlays and risk policies

## Current repository phase

This repository now has a public core of 13 scaffold skills with first support artifacts,
honest bridge manifests, and local validation coverage.
The next focus is public-core hardening through autonomy checks, evaluation, and clearer governance.
`ROADMAP.md` remains the canonical public roadmap.
`PHASED_SKILL_PLAN.md` records the scaffold expansion that established the current 13-skill surface.
