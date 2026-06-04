# Changelog

All notable changes to `aoa-skills` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

### Added

- Codex Spark now has a validated `.agents/spark/` fast-session lane with a
  registry, scenario packets, result and handoff templates, schemas, validator,
  tests, and shared release-lane wiring.
- Growth-first CI lanes now route through `scripts/ci_gate.py`, with explicit
  source-fast, generated, export, release, and nightly sentinel modes.
- Release and nightly workflows now separate frozen `v*` release checks from
  moving-`main` growth checks.
- Shared validation lane definitions now route through
  `config/validation_lanes.json` and `scripts/validation_lanes.py`, and
  validator contract data now has manifest-backed homes under
  `scripts/validation/validators/`.
- Validator topology now has a human map and machine inventory under
  `docs/validation/`, with tests that guard owner, lane, mode, and next-route
  declarations for validation-like entrypoints.
- Validation command authority now has a dedicated
  `docs/validation/COMMAND_AUTHORITY.md` route that keeps full lane sequences in
  the manifest and focused local checks in nearest `AGENTS.md` cards.
- Test topology now has a human route map and machine inventory under
  `docs/testing/`, plus pytest markers for source, generated, export, router,
  release, advisory, live, and slow checks.
- A new `AOA-SK-D-0029` decision records the validator topology and owner-module
  route.
- A new `AOA-SK-D-0030` decision records the test topology, lane split, and
  agentic route/fault contract posture.
- A new `AOA-SK-D-0031` decision records the script source-home topology and
  root ingress compatibility route.
- A new `AOA-SK-D-0032` decision records the command-authority migration from
  root compatibility wrappers to script organ paths.

### Changed

- The old root `Spark/` companion lane moved under `.agents/spark/`, matching
  the agent-lane topology used by `Agents-of-Abyss` and `aoa-techniques`.
- Single-skill validation no longer checks aggregate generated surfaces unless
  `--with-generated` is requested.
- `Repo Validation` now uses a growth-safe source-fast gate, while release
  packaging smoke moves to the release lane.
- `validate_agent_skills.py` is now a thin CLI adapter over the Agent Skills
  export/runtime validator surface.
- The Spark lane validator now checks `scripts/lanes/validation_lanes.py`
  instead of treating `scripts/release_check.py` text as the release command
  source.
- Full export validation now rebuilds and drift-checks trigger-eval seed data
  before dependent description, runtime, and tiny-router surfaces.
- `validate_agent_skills.py` and the questbook section of `validate_skills.py`
  now load contract data from validator manifests instead of carrying those
  lists directly in Python.
- Generated/read-model, questbook, and Agent Skills export/runtime validation
  now execute from owner modules under `scripts/validation/validators/`, leaving the
  script entrypoints as CLI/orchestration adapters.
- The Agent Skills export builder and validator now delegate local-adapter and
  catalog-entry phases to export/validation owner modules instead of keeping
  those phases in the main bodies.
- Agent Skills project kernel, outer-ring, risk-ring, and foundation-profile
  export document builders now live in their own export project-surface module.
- The Agent Skills export builder `main()` now routes through explicit load,
  portable-export, generated-text, and write phases.
- Per-skill Agent Skills portable export assembly now lives in its own export
  owner module, with the main builder retaining compatibility aliases.
- Agent Skills project kernel, outer-ring, risk-ring, and foundation-profile
  validation now lives in its own project-surface owner module.
- Questbook surface validation is now split into explicit schema, quest YAML,
  generated catalog, and dispatch phases inside its owner module.
- Agent Skills export/runtime validation is now phase-split into document
  loading, index building, skill-set parity, per-skill resource/runtime/router
  phases, project ring checks, release relationship checks, and runtime
  guardrail checks.
- Tiny-router, support-resource, trigger-eval, description-trigger, and pack
  profile checks now execute from owner modules under `scripts/validation/validators/`;
  the root entrypoints are thin CLI adapters.
- The former semantic AGENTS validator has been folded into the manifest-backed
  nested AGENTS contract instead of remaining as a separate one-off script.
- Active route, audit, quest, and Spark scenario docs now point to lane ids,
  owner surfaces, or nearest `AGENTS.md` routes instead of carrying validation
  command blocks outside the command-authority surfaces.
- Blocking validation lane sequences now execute family-scoped script organ
  paths under `scripts/lanes/`, `scripts/builders/`, `scripts/validation/`,
  `scripts/runtime/`, and related command organs instead of root compatibility
  wrappers.
- Release checks now execute the default pytest test lane, while
  `tests/AGENTS.md` and the lane manifest share the same command authority.
- The former monolithic validation and catalog tests are split by owner
  surface, with shared fixture, temp-repo, generated-fixture, and CLI helpers
  routed through `tests/support/`.
- Historical wave-named tests now use owner-surface names where the active
  contract meaning is no longer a landing-history artifact.
- Ordinary contract tests no longer replay a broad release-validator batch;
  they check lane composition or the directly owned contract instead.
- Root `scripts/*.py` files now act as command/front-door compatibility ingress
  wrappers, while implementation and helper libraries live under organ
  directories such as `builders/`, `runtime/`, `bundles/`, `skill_model/`, and
  `validation/`.

### Fixed

- Root script ingress now treats `--help` as a safe command surface, including
  `validate_agents_design.py` and the validation-lane manifest inspector.
- The duplicate standalone local-adapter manifest builder was folded into the
  export builder path, leaving `scripts/build_agent_skills.py` as the single
  source for `generated/local_adapter_manifest*.json`.

## [0.4.0] - 2026-05-18

### Summary

- this release turns `aoa-skills` from a flatter skill corpus into a routed
  skill system with clearer source topology, AGENTS guidance, mechanics lanes,
  generated companions, and portable export posture
- skill execution meaning is now more explicitly self-contained: technique
  bridges remain visible, but they no longer act as universal validity or
  runtime dependency blockers
- the release adds the first Skill Intelligence registry slice, closes the core
  skill audit policy gates, and tightens session-growth, project-overlay,
  summon, and diagnosis contract surfaces

### Added

- Root `DESIGN.md` and `DESIGN.AGENTS.md` now define the skill-layer system
  form and the agent-facing guidance form adapted from the AoA center pattern.
- The `AGENTS.md` mesh now covers source, docs, mechanics, parts, legacy,
  generated/export, tests, scripts, and portable pack districts with the
  canonical six-section route-card shape.
- `scripts/validate_agents_design.py` and its tests now enforce required
  AGENTS card placement, heading order, and non-empty canonical sections.
- `mechanics/OWNER_REQUEST_RECEIPTS.md` records owner-local AoA request
  receipts for skill-layer mechanics, separating landed requests from
  accepted-but-not-landed future package pressure.
- mechanics packages for audit, boundary-bridge, experience, and
  release-support now provide local route cards, provenance, landing logs, and
  active docs maps for previously flat mechanics surfaces.
- `generated/skill_intelligence_registry*.json` and
  `scripts/skill_intelligence.py` add a source-derived registry, lexical search,
  candidate explanation, and status surface for the first Skill Intelligence
  layer slice without adding a semantic backend or changing skill authority.

### Changed

- Root `AGENTS.md` now follows the canonical route-card shell with route modes,
  post-change review, hard boundaries, and review-critical drift for
  `aoa-skills`.
- Root and docs entry surfaces now stay route-focused: public overview,
  docs-map, architecture, mechanics, release-support, and adapter surfaces route
  to their owners without carrying package atlases, legacy wave language, or
  sibling-repo doctrine.
- `scripts/release_check.py` now validates the AGENTS design mesh before the
  nested and semantic AGENTS checks.
- mechanics-shaped root and flat-doc surfaces now route through `mechanics/`,
  including `mechanics/ROADMAP.md`, `mechanics/questbook/QUESTBOOK.md`,
  audit evidence, boundary bridge overlays, experience workflow posture,
  method-growth maturity docs, and release-support runtime/release surfaces.
- Growth-cycle now owns committed session-harvest notes and the
  candidate-harvest template under package-local lanes; `docs/` keeps only a
  route to that evidence surface.
- Root `legacy/` is retired as a tracked active district; raw reformation
  evidence now lives under package-local mechanics legacy lanes, with durable
  rationale in `docs/decisions/` and distilled learning in
  `mechanics/growth-cycle/session-harvests/`.
- `aoa-automation-opportunity-scan` packet contracts now require explicit
  determinism and secret-coupling posture, and `aoa-session-donor-harvest`
  only routes to self-repair after a reviewed diagnosis exists.
- Canonical skills, project overlays, release-support docs, and portable
  exports now use neutral local-agent wording except where adapter compatibility
  surfaces require a platform-specific name.
- `aoa-summon`, session-growth skills, Titan overlays, and diagnosis receipt
  examples now have tighter runtime contracts and clearer stop-lines.

### Included in this release

- mechanics topology reformation across `mechanics/`, `quests/`, `generated/`,
  route cards, roadmaps, landing logs, provenance, and owner request receipts
- skills source topology reformation across `skills/core`, `skills/risk`, and
  `skills/project`, including lane-local `AGENTS.md` cards and bundle support
  artifacts
- core engineering and session-growth skill audit follow-through, including
  activation policy separation, portable export completeness, runtime examples,
  quality audit blockers, and downstream install parity
- GitHub-facing repository metadata, release-support surfaces, and generated
  skill-intelligence discovery surfaces

### Validation

- `python scripts/release_check.py`
- `python scripts/release_check.py --include-packaging-smoke`

### Notes

- this release keeps `aoa-skills` as the bounded execution canon: not the
  technique owner, proof owner, route owner, memory owner, runtime owner, or
  downstream adoption authority

## [0.3.3] - 2026-04-23

### Summary

- this patch adds Agon skill binding candidates, recurrence skill manifests,
  Wave XV skill candidates, and recurrence observation boundaries across the
  bounded workflow layer
- Titan service-cohort skills and Experience wave3-wave5 workflow contracts
  land beside adoption, governance, installation, office task, receipt
  generation, sovereign-office, invocation, policy, and datetime guards
- `aoa-skills` remains the reusable execution-workflow canon rather than a
  routing, playbook, proof, or runtime authority

### Added

- Agon Wave IV skill candidate bridge docs, seed/config, generated index, and
  explicit builder / validator / test surfaces
- Agon recurrence skill manifests, Wave XV skill candidates, recurrence
  live-observation and review-decision closure notes, and recurrence skill
  observation boundaries
- Titan service-cohort skills plus Experience adoption, governance runtime,
  installation, office task boundary, receipt generation, sovereign-office,
  and skill adoption/governance contract surfaces
- release-facing skill-pack, portable-contract, install-profile, policy
  matrix, tiny-router, and generated manifest surfaces for downstream Codex
  and workspace installs

### Changed

- root and docs entry routes now expose the Agon bounded-workflow companion
  bridge as a requested-not-landed surface rather than leaving it implicit
- workspace closeout caution, Agon review follow-ups, skill adoption
  regression gates, governance invocation checks, install/profile contracts,
  generated release manifests, and Wave5 RFC3339 datetime validation were
  tightened

### Validation

- `python scripts/release_check.py`
- `python scripts/build_agon_skill_binding_candidates.py --check`
- `python scripts/validate_agon_skill_binding_candidates.py`
- `python -m pytest -q tests/test_agon_skill_binding_candidates.py`

### Notes

- this patch expands skill-owned workflow surfaces while keeping scenario
  composition in `aoa-playbooks`, routing in `aoa-routing`, and proof in
  `aoa-evals`

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
  `.agents/`, `.github/`, `README.md`, `AGENTS.md`, `mechanics/audit/docs/AUDIT_CONTRACT.md`, `templates/`,
  `tests/`, `mechanics/questbook/QUESTBOOK.md`, and `quests/`, including project-core kernel and
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
- repo-level release foundation through `mechanics/release-support/docs/RELEASING.md` and `python scripts/release_check.py`
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
