# Changelog

All notable changes to `aoa-skills` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

### Added

- Agon Wave IV skill candidate bridge docs, seed/config, generated index, and
  explicit builder / validator / test surfaces

### Changed

- root and docs entry routes now expose the Agon bounded-workflow companion
  bridge as a requested-not-landed surface rather than leaving it implicit

### Validation

- `python scripts/build_agon_skill_binding_candidates.py --check`
- `python scripts/validate_agon_skill_binding_candidates.py`
- `python -m pytest -q tests/test_agon_skill_binding_candidates.py`

## [0.3.2] - 2026-04-19

### Summary

- this patch adds `aoa-summon`, chaos-wave collision coverage, and recurrence
  beacons across the skill corpus
- closeout authority contracts, export refresh posture, and release/reporting
  surfaces are tightened for current Codex and A2A flows
- `aoa-skills` remains the reusable skill canon rather than a routing or
  scenario authority

### Added

- the `aoa-summon` skill scaffold, A2A end-to-end fixture binding, chaos wave
  1 skill collision surfaces, and recurrence beacons with hook bindings
- closeout authority contract acceptance in core receipts and restored
  audit-report pull request template coverage

### Changed

- roadmap/current-direction docs, required-check plus Node24 workflow refs,
  and export refresh law are aligned with the current skill release line

### Validation

- `python scripts/release_check.py`

### Notes

- this patch extends reusable execution surfaces while keeping scenario
  ownership in `aoa-playbooks` and routing ownership in `aoa-routing`

## [0.3.1] - 2026-04-12

### Summary

- this release tightens checkpoint follow-through, candidate lineage, and
  local Codex/MCP disclosure across the current skill corpus
- wave-4 session-growth kernel maturity examples land beside the continuity
  and owner-landing follow-through work
- `aoa-skills` remains the reusable skill and runtime-export canon rather than
  a scenario or routing authority

### Validation

- `python scripts/release_check.py`

### Notes

- this patch keeps the current release line focused on follow-through,
  lineage, and local adapter disclosure without widening the layer boundary

### Added

- checkpoint owner follow-through quest surfaces and closeout-bridge contract
  follow-through for release-driven harvest.
- Codex skill MCP wiring surfaces and the matching generated dependency
  metadata for downstream local adapter use.
- reviewed candidate-lineage, owner-landing follow-through, and harvest
  lineage surfaces across the skill corpus.
- wave-4 session-growth kernel maturity examples and tests for the current
  session artifact family.

### Changed

- candidate lineage posture fields and donor-harvest lineage contracts are
  tightened across the current public skill surface.

## [0.3.0] - 2026-04-10

### Summary

- this release adds checkpoint-closeout bridging, commit-growth seams, adaptive orchestration, session-harvest note surfaces, and refreshed downstream support resources
- skill build and validation contracts, defer-case expectations, and technique-reference alignment are hardened across the public corpus
- `aoa-skills` remains the reusable skill and runtime-export canon rather than a scenario or routing authority

### Validation

- `python scripts/release_check.py`

### Notes

- detailed skill-corpus, generated-runtime, governance, and install-surface coverage for this release remains enumerated below under `Added`, `Changed`, and `Included in this release`

### Added

- `aoa-checkpoint-closeout-bridge`, `aoa-commit-growth-seam`, and
  `abyss-self-diagnostic-spine` together with matching eval fixtures and
  foundation-pack wiring
- adaptive skill-orchestration protocol, session-harvest note surfaces, and
  checkpoint-note growth contracts
- refreshed runtime, portable-receipt, deterministic support-resource, and
  tiny-router support surfaces for downstream routing and review

### Changed

- hardened skill build and validation contracts, defer-case expectations, and
  technique-reference alignment across the public corpus
- aligned docs and AGENTS guidance with next-wave execution posture,
  promotion-review revisions, and cross-repo refresh follow-through

### Included in this release

- new skill and runtime-export surfaces across `skills/`, `generated/`,
  `config/`, `schemas/`, `examples/`, and `scripts/`, including
  `aoa-quest-harvest`, the session-harvest family,
  `aoa-automation-opportunity-scan`, `aoa-checkpoint-closeout-bridge`,
  `aoa-commit-growth-seam`, and `abyss-self-diagnostic-spine`
- governance and install-profile refreshes across `docs/`, `SKILL_INDEX.md`,
  `.agents/`, `.github/`, `README.md`, `AGENTS.md`, `AUDIT.md`, `templates/`,
  `tests/`, `QUESTBOOK.md`, and `quests/`, including project-core kernel and
  risk rings, foundation-pack rollout, live receipt publication, via negativa
  guidance, checkpoint-note growth, and cross-repo follow-through capture

## [0.2.0] - 2026-04-01

Second public release of `aoa-skills`.

This changelog entry uses the release-prep merge date.

### Summary

- current public skill surface now ships `19` committed skill bundles, up from `17` in `v0.1.0`
- this release expands the runtime/export layer with staged bundle inspection and import, install profiles, guardrails, description-trigger evaluation, deterministic support resources, and tiny-router inputs
- the repo now exposes stronger downstream bridges for `aoa-playbooks`, questbook projections, and consumer feed contracts while keeping scenario ownership out of the skill layer

### Added

- inspect-first staged bundle import flow, bundle-local `README.md` handoff guides, and packaging smoke coverage for portable skill handoffs
- questbook manual-first skill pilot and live questbook projection surfaces
- skill downstream feed contracts and ability adjunct surfaces for current consumers
- wave-4 dedicated-tool runtime seam around the generated Codex-facing export, including discover, disclose, activate, session-status, deactivate, and compaction-safe rehydration surfaces
- wave-6 governed runtime guardrails with repo trust gating, read-only allowlists, and context-guard session metadata around skill activation
- wave-7 description-first activation-contract coverage, including description-trigger evals and the soft `skills-ref` conformance lane
- wave-8 deterministic support-resource bundles for `aoa-dry-run-first`, `aoa-safe-infra-change`, and `aoa-local-stack-bringup`
- wave-9 tiny-router compression surfaces for downstream stage-1 shortlist routing without moving routing policy into `aoa-skills`

### Changed

- hardened the generated Codex-facing portable layer with wave-3 install profiles, trust policy, context-retention metadata, runtime contracts, UI assets, and config snippets while keeping repo-level release identity separate from seed-pack metadata
- promoted `scripts/skill_runtime_guardrails.py` to the primary local-friendly runtime path while keeping `scripts/skill_runtime_seam.py` as the raw/debug seam and `scripts/activate_skill.py` as the backward-compatible shim
- kept wave-5 scenario canon out of `aoa-skills`, exposing only `generated/skill_handoff_contracts.json` as the downstream bridge for `aoa-playbooks`
- validation and generated-surface parity now cover the staged handoff, questbook, support-resource, and tiny-router families in the bounded release path

### Included in this release

- `19` total skills under `skills/` plus the generated Codex-facing export under `.agents/skills/`
- updated runtime, governance, evaluation, packaging, and tiny-router surfaces under `generated/`, `config/`, `scripts/`, and `docs/`

### Validation

- `python scripts/release_check.py`

### Notes

- release identity for this repository remains the changelog entry, Git tag, and GitHub release body
- package publishing and per-skill release metadata remain out of scope for `v0.2.0`

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
