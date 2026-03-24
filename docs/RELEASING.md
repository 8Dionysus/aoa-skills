# Releasing `aoa-skills`

This repository is released as a public skill-and-documentation corpus.

Releases should stay small, explicit, and easy to verify.

See also:
- [Documentation Map](README.md)
- [Public Surface](PUBLIC_SURFACE.md)
- [CHANGELOG](../CHANGELOG.md)

## Release goals

A release should make it easy to answer:

- what changed
- why it matters
- how it was validated
- what is intentionally not included

## Recommended release flow

1. Confirm the target release scope.
2. Update `CHANGELOG.md`.
3. Run the bounded repo-level release check:
   - `python scripts/release_check.py`
   - the current script runs:
     - `python scripts/build_catalog.py`
     - `python -m unittest discover -s tests`
     - `python scripts/validate_skills.py`
     - `python scripts/build_catalog.py --check`
   - if the first pass materializes tracked updates, the script reruns the same bounded sequence once and requires the second pass to leave the git-backed worktree snapshot unchanged
   - when the repo starts clean, that same bounded drift check also confirms `git diff --exit-code`
4. Confirm `SKILL_INDEX.md` still matches the current public skill surface.
5. Confirm generated surfaces are current if the release includes skill or generated-surface changes.
6. Review public-safety hygiene:
   - no secrets
   - no internal-only URLs
   - no private infrastructure details
   - no raw sensitive logs
7. Merge the release-prep PR to `main`.
8. Create a Git tag such as `v0.1.0`.
9. Publish GitHub release notes using the matching changelog section or a clearly equivalent human-first shape.

## Release note shape

Recommended changelog and GitHub release note sections:

- summary
- added
- changed
- included in this release
- validation
- notes

Exact headings do not need to be rigid, but the changelog entry and the published GitHub release should answer the same release-goal questions in roughly the same shape.

## Versioning guidance

Suggested interpretation:

- `0.x.y` for early public shaping and structure refinement
- `1.0.0` only when repository structure, contribution path, release posture, and validation surface feel stable enough to promise a durable public baseline

## What not to optimize yet

Do not overbuild release machinery too early.

For now, avoid:

- registry packaging theater without a real package artifact
- automated policy claims that exceed current validation
- heavyweight semantic version promises unsupported by the repo's current purpose
- per-skill release metadata that would duplicate derived public-surface or manifest truth

## Current stance

Right now, `aoa-skills` is best released as:

- a curated public skill corpus
- a self-serve repo with one bounded repo-owned release-check entrypoint
- a validated repository structure with generated reader/runtime/governance surfaces
- a repo-level release identity separate from per-skill status and derived public-surface signaling
