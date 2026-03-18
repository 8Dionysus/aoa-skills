# Docs map

`aoa-skills` is the Codex-facing companion to `aoa-techniques`.

Where `aoa-techniques` stores public, reusable, validated engineering techniques,
`aoa-skills` stores reusable agent skills that compose one or more techniques into
an executable workflow for Codex.

## Read in this order

1. `ARCHITECTURE.md` — high-level model of the repository.
2. `BRIDGE_SPEC.md` — how skills reference and compose techniques.
3. `REPOSITORY_STRUCTURE.md` — folder layout and conventions.
4. `ROADMAP.md` — staged path for the first versions.

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

This repository is in bootstrap mode.
The initial goal is to define the skeleton, bridge rules, templates, and first starter skills.
