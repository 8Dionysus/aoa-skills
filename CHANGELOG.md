# Changelog

All notable changes to `aoa-skills` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

## [0.1.0] - 2026-03-23

First public baseline release.

This changelog entry uses the release-prep merge date.

### Summary

- first public baseline release of `aoa-skills` as a public library of reusable Codex-facing skills

### Added

- public baseline release of `17` committed skill bundles across core, risk, and project-overlay surfaces
- repo-level release foundation through `docs/RELEASING.md` and `python scripts/release_check.py`
- release-backed validation path in `.github/workflows/repo-validation.yml`
- public repository entry docs and community docs including `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and `SKILL_INDEX.md`

### Changed

- refreshed published technique refs for `aoa-sanitized-share`, `aoa-source-of-truth-check`, and `atm10-source-of-truth-check` against released `aoa-techniques v0.2.0`
- source docs now treat repo-level releases as separate from the derived public-surface signaling layer
- local validation guidance now centers on one bounded repo-level check while keeping lower-level build and validator commands available for iteration

### Included in this release

- `17` total skills under `skills/`, including `7` canonical default references, `7` evaluated candidate-ready skills, and `3` scaffold skills
- first live overlay family for `atm10`, tracked in `generated/overlay_readiness.*`
- derived reader, runtime, and governance surfaces under `generated/`, including the public surface, governance backlog, evaluation matrix, walkthroughs, lineage, boundary matrix, composition audit, bundle index, and skill graph

### Validation

- `python scripts/release_check.py`
- the bounded release check runs `python scripts/build_catalog.py`, `python -m unittest discover -s tests`, `python scripts/validate_skills.py`, and `python scripts/build_catalog.py --check`

### Notes

- release identity for this repository is the changelog entry, Git tag, and GitHub release body
- package publishing and per-skill release metadata remain out of scope for `v0.1.0`
- maturity promotions are not part of this release; current statuses come from the committed governance and evaluation surfaces
