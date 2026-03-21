# project-overlay-name overlay

## Purpose

Describe the downstream repository or project family this overlay adapts to.
Keep the description public-safe and explicit.

## Authority

- overlay repository or workspace: `[repo-relative path or short name]`
- base skill canon: `aoa-skills`
- upstream technique canon: `aoa-techniques`
- explicit approval rules: `[state the local rule]`

## Local surface

- source-of-truth files: `[list the repository-local files this overlay depends on]`
- commands: `[list the repository-local commands this overlay expects]`
- rollback path: `[state the smallest reversible step]`
- verification path: `[state the smallest meaningful check]`

## Overlayed skills

- `[skill-name]` - `[what changes in this repository]`
- `[skill-name]` - `[what changes in this repository]`

## Risks and anti-patterns

- do not widen the skill into a playbook
- do not hide authority in prose that should be explicit
- do not copy upstream technique prose into the overlay
- do not depend on live remote fetches during runtime use

## Validation

- confirm all paths are repository-relative
- confirm all commands are local and reviewable
- confirm the overlay preserves the base skill boundary
- confirm any cross-repo idea is clearly marked as a stub
