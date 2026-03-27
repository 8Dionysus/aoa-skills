# Deterministic resource bundles

This document defines the support-bundle contract introduced in wave 8.

## Goal

Move fragile workflow logic out of prose-only instructions and into compact,
reviewable, load-on-demand resources.

## Per-skill contract

Each targeted skill should have:

1. `scripts/`
   - self-contained helpers
   - CLI-friendly
   - JSON in / JSON out where practical
   - no hidden network access
   - deterministic exit behavior
2. `references/`
   - short bounded guides
   - operator-facing
   - explicit limits, not motivational text
3. `assets/`
   - JSON schema or template
   - stable structured output targets
   - portable between Codex and local adapters

## Script design rules

- prefer one bounded responsibility per script
- accept file input or stdin
- emit machine-readable JSON
- print nothing extra to stdout besides the result payload
- reserve stderr for human-readable errors
- fail closed when required inputs are missing

## Reference design rules

- explain what the resource helps with
- keep it short enough to load on demand
- point to failure modes and boundaries
- avoid duplicating the full `SKILL.md`

## Asset design rules

- schemas describe report contracts or decision outputs
- templates give the model a concrete starting shape
- filenames are stable and predictable

## Portable mirror rule

Portable copies under `.agents/skills/*` are generated from canonical support
resources under `skills/*`. Byte-identical parity is required for the canonical
support files themselves, while generated logo assets remain additive extras in
portable `assets/`.
