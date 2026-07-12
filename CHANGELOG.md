# Changelog

All notable changes to `aoa-skills` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

### Added

- A source-locked live skill-dispatch harness now separates prompt visibility,
  implicit aided/control dispatch, activation and full reads, explicit
  root-child trajectories, structured App Server input, independent fixture
  execution/verification, selected-procedure disposition plus
  completion/deflection reports, route lift, selected-child trajectory lift,
  procedure-disposition lift, explicit unscored objective
  outcome posture, host gates, private raw receipts, and
  public-safe candidate
  projections without claiming central proof authority. Structured turns
  additionally require the exact enabled map for all 57 repo skills and prove
  that no configured MCP runtime started.
- The complete post-classifier-fix smoke now has a public-safe `needs-rerun`
  receipt. Model-visible user-skill contamination, a disabled full-read/shell
  path, and an ambiguous route/procedure grader make its former trigger,
  trajectory, procedure, and no-lift labels harness diagnostics rather than
  reviewed evidence of skill defects.
- The first protocol-v2 smoke now has a separate public-safe `needs-rerun`
  receipt. Its prompt gate passed, but the first CLI arm stopped before model
  spend because per-MCP overrides reconstructed incomplete tables under
  `--ignore-user-config`; it is adapter evidence only.
- The complete protocol-v2 smoke now has a public-safe `needs-rerun` receipt.
  Its implicit positive-lift pair remains candidate evidence, but the App arm
  used structured-only input instead of the official `$skill` plus `skill`
  pair, so its App load label is harness evidence only.
- The first source-locked protocol-v3 smoke now has a public-safe reviewed
  receipt. It preserves one candidate implicit positive-lift pair and a valid
  App native-load/procedure path while localizing the explicit root trajectory
  to one missing-child-read gap; it publishes neither central proof nor a
  promotion claim, and later protocols do not upgrade its historical grader
  semantics in place.
- The exact-merged-tree v3 rerun after the root-handoff repair now has a
  public-safe `needs-rerun` receipt. Its first three arms exposed self-report
  load gating, a missing dynamic-child read check, ambiguous read-versus-
  procedure wording, and output-contract/transport conflation; it publishes no
  pair, lift, skill-effect, or family conclusion.
- The exact-merged-tree v4 smoke now has a public-safe `needs-rerun` receipt.
  Its aided arm passed objective root and dynamic-child reads, but its control
  read a complete repo skill from an external canonical checkout before budget
  exhaustion. The historical budget label remains immutable; reviewed raw
  evidence routes the earlier fault to harness isolation and permits no pair,
  lift, skill-effect, or family conclusion.
- The exact-merged-tree v5 smoke now has a public-safe `needs-rerun` receipt.
  Fixture scope was clean and all four arms completed, but the aided target was
  fully read across two ordered command outputs that the v5 single-output
  grader rejected. V6 assembles continuous ordered exact-path source coverage,
  permits overlaps, ignores unrelated outputs, and keeps gaps or reverse-only
  coverage incomplete before repeating the live smoke.
- The exact-merged-tree v6 smoke now has a public-safe `needs-rerun` receipt.
  Prompt visibility and fixture scope passed, but the first CLI transport timed
  out at 180 seconds before any turn event, output, usage, or pair. V7 preserves
  elapsed failure duration and returns nonzero for an incomplete stopped-early
  cohort after safely writing its private receipt.
- The complete exact-merged-tree v7 smoke now has a reviewed public-safe
  receipt. Its generic positive pair field is explicitly bounded to route
  correctness because the v7 grader used only `route_contract_match`. V8
  replaces generic new-pair fields with distinct route/outcome lift, requires a
  source-authored smoke outcome contract before planning, and keeps missing
  contracts unscored instead of inferring an answer from live output. Pilot
  execution is blocked before preflight until all 11 implicit pairs have
  declared contracts.
- The complete exact-merged-tree v8 smoke now has a public-safe `needs-rerun`
  receipt. It preserves positive route lift, negative outcome lift, and one
  `bounded_outcome_miss` under the historical answer key. Source review found
  that key had graded deflection of the unavailable whole repository task even
  though the constrained output and fixture define disposition for the exact
  downstream procedure. V9 names that scope explicitly, corrects the
  pre-authored expectation from source, preserves v8 unchanged, and requires a
  grader replay plus fresh exact-merged smoke before pilot widening.
- The complete exact-merged-tree v9 smoke now has a public-safe `needs-rerun`
  receipt. It preserves the child-route and structured hierarchy observations
  that exposed the remaining grader ambiguity. V10 separates model selection
  report from transport dispatch/native load, selected-child trajectory from
  procedure-disposition report, requires both source-declared root and child
  for an equivalent hierarchy report, and separates the independent fixture
  probe from both. A report-only mismatch now has its own
  `selection_report_miss` return route without relabeling successful native
  dispatch or load evidence.
  Current pairs explicitly leave objective outcome unscored because the fixture
  has no observable external-task result.
- Two exact-merged v10 attempts now have public-safe `needs-rerun` receipts.
  The first stopped the aided arm after broad hidden fixture enumeration; the
  unchanged repeat completed the implicit pair but stopped the explicit root
  arm after broad listing and tree hashing. V11 keeps the 48k cap, source-locks
  a bounded inventory contract, permits exact route-required reads, and grades
  broad internal enumeration as `fixture_inventory_scope_violation` before a
  later budget marker or skill interpretation.
- The fresh exact-merged v11 smoke completed all four arms with zero broad
  inventory commands and no trial failures. Its reviewed candidate receipt
  reports route lift `+1`, selected-child trajectory lift `+1`, correct
  source-locked procedure disposition in both implicit arms (`0` lift), and an
  explicitly unscored objective outcome. Direct root-to-child and structured
  App Server activation also passed; pilot execution remains blocked at 1/11
  procedure contracts and 0/11 observable outcomes.
- `AOA-SK-D-0037` records why live cohorts remain operator-confirmed candidate
  evidence and now clarifies prompt-surface isolation and evidence-stage grading
  after the contaminated smoke; deterministic harness validation, not model
  calls, remains in the normal repository gate.

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
- A new `AOA-SK-D-0033` decision records the root ingress closure, with a
  strict evidenced allowlist and retired wrapper inventory.
- The evaluated decision graph skill chain now publishes `aoa-decision`,
  `aoa-decision-find`, `aoa-decision-create`, and `aoa-decision-correct` in the
  public skill index, core profiles, and generated export/runtime surfaces.
- The `aoa-eval` family now has an active local eval-port trigger corpus and
  session-mining report with `.aoa` refs, guarded by focused tests while central
  proof authority remains in `aoa-evals`.
- The generated release manifest now has an OS Abyss artifact bundle manifest
  and blocking release-lane `abyss-machine` verifier check for policy-driven
  ABI sidecars.

### Changed

- `aoa-eval` now reports live-workspace root/commit/dirty posture separately
  from exact-source evidence, and preserves dirty canonical checkouts.
  `aoa-eval-apply` now adopts the owner JIT contract for reviewed local-suite
  sidecars: exact typed invocation, environment capture, private source-linked
  receipt, inspect-only readiness/MCP, and explicit non-proof/non-reproducible
  boundaries. A trigger/snapshot regression covers the selected-sidecar route.
- `aoa-eval` now requires a complete read of exactly one selected child's
  `SKILL.md` before applying or claiming its procedure. A returned child name
  remains selection evidence only, and focused regression coverage protects
  the selected-to-loaded handoff exposed by the reviewed v3 smoke.
- Live dispatch now discovers exact external shadowing `SKILL.md` paths,
  including canonical targets behind user-skill symlinks, binds only their
  count and digest into confirmation/source locks, and disables the canonical
  paths in every adapter. Plugin surfaces are disabled; the configured MCP-name
  inventory is independently source-locked. CLI exec isolates it through
  `--ignore-user-config` without constructing partial MCP tables, while prompt
  inspection and App Server explicitly disable every configured name.
- Every model turn is gated by `codex debug prompt-input`. Aided fixtures must
  expose exactly the policy-visible repo skills (currently 12 of 57), controls
  expose zero, and the background inventory digest now fingerprints each
  model-visible name, path, and description rather than paths alone. Structured
  App Server turns separately require the exact fixture path for every one of
  the 57 repo skills before `turn/start`, reject any MCP startup event, and use
  the official dual invocation: an exact `$skill` text prefix plus the matching
  structured `skill` item.
- Read-only shell execution is now available to prove complete skill reads and
  run the exact hermetic `python3 fixture_validator.py` probe. A full read
  must name the exact fixture `SKILL.md` path and expose its complete content in
  one output or continuous ordered chunks;
  verification requires one atomic command event whose exact command, zero
  exit, sentinel JSON, and fixture-guidance digest all agree. Public measures
  keep selection, claimed load, accepted native input, transport-observed
  reads, dispatch, load,
  execution, verification, completion, and deflection distinct:
  `dispatch_policy_gap` means the activation decision was wrong, while
  `skill_load_gap` returns a correct selection with unproved activation/read to
  the same case.
- Objective load evidence no longer depends on the model's `claims_loaded`
  self-report. Expected and dynamically selected children require complete
  exact-path reads, read-only inspection commands are explicitly allowed and
  excluded from the one-command procedure count, and zero-return structured
  output failures are classified as `output_contract_invalid` rather than
  `transport_failure`.
- Live model commands are now confined to the hermetic fixture root. Absolute
  host, workspace, session-memory, user-config, other-repository, and
  parent-traversal paths set `fixture_filesystem_scope_match=false` and return
  `harness_contamination` before budget, dispatch, load, procedure, or pair
  interpretation; system executables and `/dev/null` remain tooling exceptions.
- Both executable local-suite sidecars now carry current tracked-source hashes:
  the live dispatch runner/schema/test surface and the `aoa-eval` trigger
  corpus after the landed child-handoff change. The central `aoa-evals`
  validator therefore reports the full local eval port source-contract-ready
  instead of silently retaining transitive stale state.
- Route, selected-child trajectory, and procedure-disposition lift are not
  scored when either arm has a transport, budget, runtime, or owner-boundary safety failure. Contamination
  is retained as a pair result without rewriting either arm's historical
  failure class, and public-receipt validation rejects absolute host paths even
  when embedded inside prose.
- Caught CLI and App Server transport exceptions retain elapsed duration,
  partial private stdout/stderr, recoverable JSONL events, and usage.
  Complete cohorts exit zero even for negative model evidence, while incomplete
  stopped-early cohorts publish their stop reason and exit nonzero after the
  private receipt is preserved.
- Source-locked route/procedure grading now binds `scope` to
  `selected_route_procedure_disposition`. The contract can declare an expected
  child and full read when the route has one, then separately declares the
  selected procedure's disposition report and owner boundary. This also fits
  direct pilot routes without inventing a child. Fixture execution is objective
  but independent; whole-task outcome remains explicitly unavailable.
  Historical v8-v10 receipts remain readable and immutable under their original
  graders.
- The source corpus and schema are now named
  `aoa-skill-live-dispatch-procedures.json` and
  `live-skill-dispatch-procedure-contracts.schema.json`; the old outcome names
  are retained only inside historical receipt vocabulary.
- The hermetic evidence contract is now
  `aoa_codex_app_server_skill_input_contract_v11` with protocol revision
  `codex-cli-0.144.1-live-dispatch-evidence-v11`; retained v1-v10 receipts remain
  immutable under their original protocol and review status.
- Live dispatch now locks and passes Codex rollout-budget reminder thresholds
  as a TOML list for both CLI and App Server arms, rejects invalid thresholds
  before transport startup, and preserves review compatibility with receipts
  created before that cap was published.
- Live dispatch plan loading now rejects model-output schemas that escape the
  Responses API strict subset, and the bounded output contract declares types
  for enum and const fields before a model request can start.
- All live arms now use a source-locked 48k weighted-token ceiling. Root-child
  reads first justified that floor; the corrected no-skill control then showed
  that an equal-background session-memory route also cannot complete its
  required owner reads under 28k. Aided/control caps remain equal, and
  shared-budget exhaustion keeps its own reviewed cap/context return route.
- Live dispatch classification now preserves valid zero-return model output
  despite late budget markers and excludes the expected target from its own
  collision-neighbourhood check; explicit authority claims also precede generic
  output invalidity, so semantic and safety failures are not hidden by harness
  artefacts.
- Description-trigger mirrors now retain negative `prefer-other` coverage for
  manual skills, while same-band tiny-router shortlists remain candidate-only
  and leave activation to the downstream policy gate.
- The OS Abyss artifact-trust skill now has matching positive and negative
  trigger/snapshot evidence, and export drift checks include the collision
  matrix they already declare as generated truth.
- Generated release manifests now use schema version 4 and carry an
  `artifact_identity` contract for portable export consumer checks.
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
- The generated skills-ref conformance manifest now publishes the
  export-required `--require-skills-ref` posture instead of a soft skip recipe.
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
- Root script ingress has been squeezed from the broad compatibility layer down
  to 13 public front doors for lanes, runtime/activation, and bundle handoff;
  internal builder, validator, audit, report, refresh, receipt, adapter, and
  skill-model tools now use organ paths.

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
