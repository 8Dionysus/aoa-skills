# family-name overlay

## Purpose

Describe the project family this live exemplar overlay pack adapts to.
Keep the description public-safe, repo-local, and explicit.
State that the overlay does not change the base skill boundary.

## Authority

- overlay family: `[atm10|abyss|other repo-local family name]`
- canonical overlay doc: `docs/overlays/[family-name]/PROJECT_OVERLAY.md`
- base skill canon: `aoa-skills`
- upstream technique canon: `aoa-techniques`
- explicit approval rules: `[state the local rule]`

## Local surface

- source-of-truth files: `[list the repository-local files this overlay depends on]`
- commands: `[list the repository-local commands this overlay expects]`
- rollback path: `[state the smallest reversible step]`
- verification path: `[state the smallest meaningful check]`

## Overlayed skills

- `[family-skill-name]` - `[what changes in this repository and which base skill it adapts]`
- `[family-skill-name]` - `[what changes in this repository and which base skill it adapts]`

## Risks and anti-patterns

- do not widen the skill into a playbook
- do not hide authority in prose that should be explicit
- do not copy upstream technique prose into the overlay
- do not depend on live remote fetches during runtime use
- do not present this exemplar pack as a downstream integration

## Validation

- confirm all paths are repository-relative
- confirm all commands are local and reviewable
- confirm the overlay preserves the base skill boundary
- confirm the overlayed skills section exactly matches the committed `skills/<family>-*` bundles
