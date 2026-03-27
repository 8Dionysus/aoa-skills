# Eighth wave: deterministic support bundles

This wave hardens three high-risk or frequently repeated skills with explicit
resource bundles that reduce execution drift in both Codex and local-friendly
runtimes.

## Why this wave exists

The repo already has support artifacts in AoA-shaped directories such as
`agents/`, `checks/`, and `examples/`. This wave does not replace those
surfaces. It adds the standard bundle directories that skills-oriented runtimes
understand natively:

- `scripts/`
- `references/`
- `assets/`

## Targeted skills

- `aoa-safe-infra-change`
- `aoa-local-stack-bringup`
- `aoa-dry-run-first`

## Deliverables

For each targeted skill:

- deterministic helper scripts with JSON I/O
- short references that state limits and review posture
- structured output schemas and input templates

At the repo level:

- support-bundle builder
- support-bundle validator
- support-bundle linter
- generated manifests and schema indexes
- portable export integration through the existing export builder
- unit tests and release-check coverage

## Integration rule

Canonical support bundles live under `skills/*/{scripts,references,assets}`.
Portable resource bundles under `.agents/skills/*/{scripts,references,assets}`
remain generated mirrors owned by `scripts/build_agent_skills.py`.

## What this wave is not

- not a rewrite of existing `SKILL.md`
- not a replacement for `checks/review.md`
- not a replacement for `examples/runtime.md`
- not a separate portable-sync authority
- not a new runtime seam or playbook layer
