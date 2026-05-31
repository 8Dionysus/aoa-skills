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
3. Run the release lane:
   - `python scripts/ci_gate.py --mode release`
   - this is equivalent to the bounded repo-level release check with packaging
     smoke: `python scripts/release_check.py --include-packaging-smoke`
   - the authoritative command sequence lives in
     `scripts/validation_lanes.py` as `RELEASE_CHECK_COMMAND_SEQUENCE` plus
     `PACKAGING_SMOKE_COMMAND`
   - the release lane covers catalog and decision-index generation,
     portable/runtime/support/tiny-router builders, trigger and
     description-trigger eval builders and lints, Agon candidate checks,
     repository tests, AGENTS/skill/export validators, Spark lane validation,
     generated drift checks, and packaging smoke
   - if the first pass materializes tracked updates, the script reruns the same bounded sequence once and requires the second pass to leave the git-backed worktree snapshot unchanged
   - when the repo starts with no tracked diff, that same bounded drift check also confirms `git diff --exit-code`
4. Confirm `SKILL_INDEX.md` still matches the current public skill surface.
5. Confirm generated surfaces are current if the release includes skill, portable export, or generated-surface changes.
  - this includes portable exports, catalogs, local-adapter manifests, runtime
    seams, trust/guardrail surfaces, support-resource bundles, description
    triggers, tiny-router inputs, trigger-eval seed data, and the release
    manifest when their source inputs changed
  - for the exact packaging contract, read `generated/release_manifest.json`
    and the component map in `COMPONENT_REFRESH_LAW.md`
  - read `generated/skill_bundle_index.json` for per-skill packaging membership and technique-lineage detail
  - read `generated/skill_graph.json` for profile and artifact-group topology across the same bundle set
  - use `python scripts/verify_skill_pack.py --repo-root . --profile repo-default --format json` when you want one repo-local install verification check over the live `.agents/skills` root
  - if the release touches staged-handoff or archive flows, prefer one canonical packaging smoke command: `python scripts/release_check.py --include-packaging-smoke`
  - that optional smoke path runs `scripts/smoke_skill_pack_handoff.py` for `repo-core-only`, stages a bundle, inspects it, installs in `copy` mode, and verifies both directory and ZIP transports
  - read the generated bundle `README.md` as the human-facing companion when reviewing one staged handoff object; `bundle_manifest.json` remains the machine-readable bundle contract
6. Review public-safety hygiene:
   - no secrets
   - no internal-only URLs
   - no private infrastructure details
   - no raw sensitive logs
7. If the release includes a skill-derived bridge consumed by a neighboring repo, plan merge order explicitly.
   - merge the source-owned bridge repo first
   - rerun downstream PR checks after upstream `main` contains the new bridge surfaces
   - do not treat the downstream PR head SHA as independently valid when CI checks out neighboring repos from `main`
8. Merge the release-prep PR to `main`.
9. Create a Git tag such as `v0.1.0`.
10. Publish GitHub release notes using the matching changelog section or a clearly equivalent human-first shape.

## CI lane interpretation

`main` is the moving growth surface. It may legitimately differ from the latest
release tag immediately after a release. Treat `generated/release_manifest.json`
`has_unreleased_changes: true` as normal growth evidence on `main`, not as a
release failure.

Use the lanes this way:

- PR and ordinary growth work: `python scripts/ci_gate.py --mode source-fast`
- main integration generated/readout check: `python scripts/ci_gate.py --mode generated --group all`
- scoped generated/readout checks: `python scripts/ci_gate.py --mode generated --group reader|public|evaluation|governance|export|runtime`
- portable export/runtime/support check: `python scripts/ci_gate.py --mode export`
- frozen release or tag check: `python scripts/ci_gate.py --mode release`
- scheduled sentinel: `python scripts/ci_gate.py --mode nightly`

GitHub scheduled workflows run from the default branch, so the nightly sentinel
checks `main` as a growth surface and separately checks the latest `v*` tag as a
frozen release artifact. Do not make a scheduled workflow require `main` to
match the latest release.

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
- a validated repository structure with generated reader/runtime/governance surfaces, portable export, runtime guardrails, description-first activation checks, support-resource bridge, tiny-router compression bridge, and local adapter seam
- a machine-readable portable release contract in `generated/release_manifest.json` that stays subordinate to the changelog/tag/release-note identity
- a self-contained staged-bundle inspection step in `scripts/inspect_skill_pack.py` before install-side verification
- a release-facing packaging smoke helper in `scripts/smoke_skill_pack_handoff.py`, wired into `scripts/release_check.py --include-packaging-smoke`
- optional staged ZIP handoff over the same profile-bundle contract for repo-local offline transfer, install, and verification
- a repo-level release identity separate from per-skill status and derived public-surface signaling
