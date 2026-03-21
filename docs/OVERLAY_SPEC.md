# Overlay Spec

`OVERLAY_SPEC.md` defines the repo-local contract for thin project overlays in `aoa-skills`.
It now covers both fixture stubs and live exemplar overlay packs.
It does not redefine techniques, status floors, or public skill meaning.

## Purpose

Project overlays exist so a downstream repo can adapt a public skill bundle to its own:

- local paths
- local commands
- source-of-truth files
- approval posture
- verification steps

An overlay is thin by design. It should explain how a skill changes shape in a target repository without silently widening the skill into a playbook.
Live overlay packs in this repository are exemplar surfaces only.
They are not downstream integrations and they do not replace project-local authority.

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

## Two-tier contract shape

Fixture-only stubs remain under `tests/fixtures/overlay_stubs/`.
They exist to keep the stub contract small, explicit, and validator-backed.

Live exemplar packs now live under `docs/overlays/<family>/`.

A live thin overlay pack should normally include:

- `docs/overlays/<family>/PROJECT_OVERLAY.md`
- one or more matching `skills/<family>-*` bundles
- repo-relative commands, paths, approval posture, and verification notes that stay public-safe

The project overlay document is the family-level entrypoint.
The matching `skills/<family>-*` bundles are the executable thin overlays.
Fixture stubs remain separate from live overlay packs and do not imply project adoption.

## Validation intent

Overlay validation should answer these questions:

1. Is the overlay named explicitly and repo-locally?
2. Does the overlay preserve the base skill boundary?
3. Are authority and approval rules clear?
4. Are all paths and commands repository-relative and public-safe?
5. Does the live family overlay document match the committed `skills/<family>-*` bundles?
6. Are fixture-only cross-repo ideas still clearly marked as stubs?

## Fixture layout

The current fixture packs in `tests/fixtures/overlay_stubs/` show the expected minimum shape:

- `tests/fixtures/overlay_stubs/atm10-demo/PROJECT_OVERLAY.md`
- `tests/fixtures/overlay_stubs/atm10-demo/PROJECT_OVERLAY_SKILL.md`
- `tests/fixtures/overlay_stubs/abyss-demo/PROJECT_OVERLAY.md`
- `tests/fixtures/overlay_stubs/abyss-demo/PROJECT_OVERLAY_SKILL.md`

These packs are intentionally small. They exist to support validator coverage for stub-only overlays without implying live family skills.

## Live exemplar layout

The current live family overlay layout is:

- `docs/overlays/atm10/PROJECT_OVERLAY.md`
- `skills/atm10-change-protocol/`
- `skills/atm10-source-of-truth-check/`

Future live packs should keep the same shape:

- `docs/overlays/<family>/PROJECT_OVERLAY.md`
- `skills/<family>-*/SKILL.md`
- `skills/<family>-*/techniques.yaml`
- optional `skills/<family>-*/agents/openai.yaml`
- at least one support artifact under the matching `skills/<family>-*/`

Live exemplar packs must:

- explicitly say that they do not change the base skill boundary
- list the matching `skills/<family>-*` bundles
- stay repo-local, public-safe, and reviewable
- avoid pretending to be a downstream integration or playbook

## Future stubs

TODO: if a richer overlay contract is needed later, keep it repo-local and schema-first.

TODO: if a downstream project needs more than a thin overlay, that work belongs in the downstream repository, not here.

TODO: if overlay validation later needs project-specific exceptions, encode them as explicit fields or stubs instead of hidden prose rules.
