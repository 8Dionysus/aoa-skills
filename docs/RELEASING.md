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
     - `python scripts/build_runtime_seam.py --repo-root .`
     - `python scripts/build_runtime_guardrails.py --repo-root .`
     - `python scripts/build_description_trigger_evals.py --repo-root .`
     - `python scripts/build_support_resources.py --repo-root .`
     - `python scripts/build_tiny_router_inputs.py --repo-root .`
     - `python -m unittest discover -s tests`
     - `python scripts/validate_nested_agents.py`
     - `python scripts/validate_skills.py`
     - `python scripts/validate_agent_skills.py --repo-root .`
     - `python scripts/validate_support_resources.py --repo-root . --check-portable`
     - `python scripts/validate_tiny_router_inputs.py --repo-root .`
     - `python scripts/lint_trigger_evals.py --repo-root .`
     - `python scripts/lint_description_trigger_evals.py --repo-root .`
     - `python scripts/lint_pack_profiles.py --repo-root .`
     - `python scripts/lint_support_resources.py --repo-root .`
     - `python scripts/run_skills_ref_validation.py --repo-root .`
     - `python scripts/build_tiny_router_inputs.py --repo-root . --check`
     - `python scripts/build_support_resources.py --repo-root . --check`
     - `python scripts/build_description_trigger_evals.py --repo-root . --check`
     - `python scripts/build_runtime_guardrails.py --repo-root . --check`
     - `python scripts/build_runtime_seam.py --repo-root . --check`
     - `python scripts/build_catalog.py --check`
   - if the first pass materializes tracked updates, the script reruns the same bounded sequence once and requires the second pass to leave the git-backed worktree snapshot unchanged
   - when the repo starts with no tracked diff, that same bounded drift check also confirms `git diff --exit-code`
4. Confirm `SKILL_INDEX.md` still matches the current public skill surface.
5. Confirm generated surfaces are current if the release includes skill, portable export, or generated-surface changes.
  - this includes `.agents/skills/*`, `generated/agent_skill_catalog*.json`, `generated/portable_export_map.json`, `generated/local_adapter_manifest*.json`, `generated/context_retention_manifest.json`, `generated/trust_policy_matrix.json`, `generated/skill_runtime_contracts.json`, `generated/skill_pack_profiles.resolved.json`, `generated/codex_config_snippets.json`, `generated/mcp_dependency_manifest.json`, `generated/runtime_*.json`, `generated/*guardrail*.json`, `generated/skill_description_signals.json`, `generated/description_trigger_eval_cases.*`, `generated/description_trigger_eval_manifest.json`, `generated/skills_ref_validation_manifest.json`, `generated/deterministic_resource_manifest.json`, `generated/support_resource_index.json`, `generated/structured_output_schema_index.json`, `generated/support_resource_bridge_map.json`, `generated/deterministic_resource_eval_cases.jsonl`, `generated/expected_existing_aoa_support_dirs.json`, `generated/tiny_router_skill_signals.json`, `generated/tiny_router_candidate_bands.json`, `generated/tiny_router_capsules.min.json`, `generated/tiny_router_eval_cases.jsonl`, `generated/tiny_router_overlay_manifest.json`, `generated/release_manifest.json`, and trigger-eval seed data when trigger boundaries changed
  - for portable/export changes, read `generated/release_manifest.json` as the packaging-verification surface: it pins artifact groups, relationship views, input digests, generated-file digests, bundle revisions, profile revisions, and changelog-derived release identity
  - read `generated/skill_bundle_index.json` for per-skill packaging membership and technique-lineage detail
  - read `generated/skill_graph.json` for profile and artifact-group topology across the same bundle set
  - use `python scripts/verify_skill_pack.py --repo-root . --profile repo-default --format json` when you want one repo-local install verification check over the live `.agents/skills` root
  - if the release touches staged-handoff flows, read the generated bundle `README.md` as the human-facing companion and smoke-test one profile bundle with `python scripts/stage_skill_pack.py --repo-root . --profile repo-core-only --output-root /tmp/repo-core-only-bundle --execute --overwrite --format json`, then inspect it with `python scripts/inspect_skill_pack.py --bundle-root ...`
  - if the release touches archive handoff flows, optionally extend that smoke path with `--archive-path /tmp/repo-core-only.zip`, then install and verify directly against the ZIP via `install_skill_pack.py --bundle-archive ...` and `verify_skill_pack.py --bundle-archive ...`
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
- a validated repository structure with generated reader/runtime/governance surfaces plus a generated Codex-facing portable export, a wave-4 raw runtime seam, a wave-6 governed runtime layer, a wave-7 description-first activation-eval layer, a wave-8 deterministic support-resource bridge, a wave-9 tiny-router compression bridge for downstream routing, and a legacy-compatible local adapter seam
- a machine-readable portable release contract in `generated/release_manifest.json` that stays subordinate to the changelog/tag/release-note identity
- a self-contained staged-bundle inspection step in `scripts/inspect_skill_pack.py` before install-side verification
- optional staged ZIP handoff over the same profile-bundle contract for repo-local offline transfer, install, and verification
- a repo-level release identity separate from per-skill status and derived public-surface signaling
