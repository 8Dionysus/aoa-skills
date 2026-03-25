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
   - `python scripts/build_agent_skills.py --repo-root .`
   - `python -m unittest discover -s tests`
   - `python scripts/validate_nested_agents.py`
   - `python scripts/validate_skills.py`
   - `python scripts/validate_agent_skills.py --repo-root .`
   - `python scripts/lint_trigger_evals.py --repo-root .`
   - `python scripts/lint_pack_profiles.py --repo-root .`
   - `python scripts/build_catalog.py --check`
   - if the first pass materializes tracked updates, the script reruns the same bounded sequence once and requires the second pass to leave the git-backed worktree snapshot unchanged
   - when the repo starts with no tracked diff, that same bounded drift check also confirms `git diff --exit-code`
4. Confirm `SKILL_INDEX.md` still matches the current public skill surface.
5. Confirm generated surfaces are current if the release includes skill, portable export, or generated-surface changes.
   - this includes `.agents/skills/*`, `generated/agent_skill_catalog*.json`, `generated/portable_export_map.json`, `generated/local_adapter_manifest*.json`, `generated/context_retention_manifest.json`, `generated/trust_policy_matrix.json`, `generated/skill_runtime_contracts.json`, `generated/skill_pack_profiles.resolved.json`, `generated/codex_config_snippets.json`, `generated/mcp_dependency_manifest.json`, `generated/release_manifest.json`, and trigger-eval seed data when trigger boundaries changed
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
- a validated repository structure with generated reader/runtime/governance surfaces plus a generated Codex-facing portable export and local adapter seam
- a repo-level release identity separate from per-skill status and derived public-surface signaling
