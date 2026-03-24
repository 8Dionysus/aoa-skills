# AGENTS.md

Guidance for coding agents and humans working under `docs/overlays/`.

## Purpose

`docs/overlays/` stores family-level live exemplar overlay packs for `aoa-skills`. These documents explain how a public base skill is adapted to a repository family without pretending to be a downstream integration or a playbook.

This directory owns family overlay docs such as `PROJECT_OVERLAY.md` and `REVIEW.md`. It does not own the base skill boundary, upstream technique meaning, or downstream project authority.

## Read this first

Before editing an overlay family doc, read in this order:

1. `../../AGENTS.md`
2. `../OVERLAY_SPEC.md`
3. `../README.md`
4. the target `docs/overlays/<family>/PROJECT_OVERLAY.md`
5. the target `docs/overlays/<family>/REVIEW.md`
6. the matching `skills/<family>-*/SKILL.md`
7. any matching bundle-local review checklists such as `skills/<family>-*/checks/review.md`

## Directory contract

A live thin overlay pack should stay family-scoped and reviewable. It normally includes:

- `docs/overlays/<family>/PROJECT_OVERLAY.md`
- `docs/overlays/<family>/REVIEW.md`
- one or more matching `skills/<family>-*` bundles
- bundle-local review checklists when the family review surface names them

Keep the overlay thin. Keep it repo-local. Keep it public-safe.

## Allowed changes

Safe, normal contributions here include:

- tightening the family entrypoint so paths, commands, approval posture, and verification stay explicit
- aligning the family review doc with the committed overlay skills
- adding a new family pack when the matching overlay bundles already exist and remain bounded
- correcting stale repo-relative paths or review references

## Changes requiring extra care

Use extra caution when:

- changing the overlay family name
- changing the list of matching `skills/<family>-*` bundles
- changing family-level approval language or authority posture
- changing wording that could imply the overlay changes the base skill boundary

## Hard NO

Do not:

- present a live exemplar overlay as a downstream integration
- hide private instructions, secrets, or internal hostnames in overlay docs
- turn a family overlay into project doctrine or a playbook
- claim authority that belongs to the downstream repository
- imply that `PROJECT_OVERLAY.md` or `REVIEW.md` replaces the matching skill bundles

## Validation

When overlay docs change, confirm:

- every listed overlay skill has a matching `skills/<family>-*` bundle
- family review notes still match bundle-local review checklists
- repo-relative commands and paths stay public-safe
- the overlay still describes a thin overlay rather than a downstream integration

Then run:

- `python -m unittest discover -s tests`
- `python scripts/validate_nested_agents.py`
- `python scripts/validate_skills.py`

## Output expectations

When reporting work in `docs/overlays/`, include:

- which family pack changed
- which matching `skills/<family>-*` bundles were checked
- whether the overlay boundary changed or only examples/review notes changed
- any follow-up needed in overlay skills or family review docs
