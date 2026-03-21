# Overlay Spec

`OVERLAY_SPEC.md` defines the repo-local contract for thin project overlays in `aoa-skills`.
It is for downstream repository adaptation only. It does not redefine techniques, status floors, or public skill meaning.

## Purpose

Project overlays exist so a downstream repo can adapt a public skill bundle to its own:

- local paths
- local commands
- source-of-truth files
- approval posture
- verification steps

An overlay is thin by design. It should explain how a skill changes shape in a target repository without silently widening the skill into a playbook.

## What an overlay may change

An overlay may adjust:

- repository-relative paths
- local command examples
- explicit approval rules
- verification or rollback steps
- repository-specific notes that stay public-safe

An overlay may not:

- invent new upstream technique meaning
- add hidden authority
- weaken the bounded trigger boundary of the base skill
- depend on live remote fetches
- store private project instructions or secrets

## Contract shape

A thin overlay pack should normally include:

- a project overlay document
- one or more overlayed skill documents
- optional stubs that show how the overlay stays bounded

This repository keeps those examples local and public-safe. The examples are fixtures, not live project integrations.

## Validation intent

Future overlay validation should be able to answer these questions:

1. Is the overlay named explicitly and repo-locally?
2. Does the overlay preserve the base skill boundary?
3. Are authority and approval rules clear?
4. Are all paths and commands repository-relative and public-safe?
5. Are any cross-repo ideas clearly marked as stubs only?

## Recommended fixture layout

The current fixture packs in `tests/fixtures/overlay_stubs/` show the expected minimum shape:

- `tests/fixtures/overlay_stubs/atm10-demo/PROJECT_OVERLAY.md`
- `tests/fixtures/overlay_stubs/atm10-demo/PROJECT_OVERLAY_SKILL.md`
- `tests/fixtures/overlay_stubs/abyss-demo/PROJECT_OVERLAY.md`
- `tests/fixtures/overlay_stubs/abyss-demo/PROJECT_OVERLAY_SKILL.md`

These packs are intentionally small. They exist to support validator coverage without adding real project-family skills.

## Future stubs

TODO: if a richer overlay contract is needed later, keep it repo-local and schema-first.

TODO: if a downstream project needs more than a thin overlay, that work belongs in the downstream repository, not here.

TODO: if overlay validation later needs project-specific exceptions, encode them as explicit fields or stubs instead of hidden prose rules.
