# Mechanics Reformation Rhythm

This file is a route-holding notebook for a long `aoa-skills` mechanics
reformation pass. It exists under root `legacy/` so it can survive context
compaction and session handoff while the work is in progress.

## North Star

Reform `aoa-skills` from accumulated flat surfaces into a legible execution
canon that future agents can navigate without guessing.

The project-level goal is not to make `aoa-skills` look like
`Agents-of-Abyss` or `aoa-techniques`. The goal is to understand their deeper
shape and translate the right discipline into the bounded execution layer:

- `Agents-of-Abyss` owns center law, mechanics posture, owner splits, and
  package route grammar.
- `aoa-techniques` owns reusable practice leaf bundles and has already proven a
  tree migration rhythm.
- `aoa-skills` owns reusable Codex-facing execution bundles and the adapter,
  generated, export, and downstream seams around them.

The future skill tree should make the skill canon easier to browse, route, and
grow. The mechanics reformation comes first because mechanics explain movement
around skill canon without relocating skill canon into mechanics.

## Absolute Boundaries

- Do not put skill bundles inside `mechanics/`.
- Do not make `mechanics/` a second `skills/` tree.
- Do not make `docs/` a legacy archive.
- Do not use `legacy/docs-root/` as a mechanic legacy pattern.
- Do not treat generated, exported, compact, runtime, or adapter surfaces as
  authored truth.
- Do not move broad surfaces in one wave.
- Do not move files because their names look similar.
- Do not copy AoA center wording such as `Center owns` into `aoa-skills`;
  use local owner language such as `Local owns`.
- Do not import stronger-owner authority into this repository.
- Do not turn a temporary rhythm into public doctrine.
- Do not leave duplicate active doors behind after a move.
- Do not land placeholders, empty districts, orphaned links, or validation
  claims that are not backed by real checks.

## Source Stack

Always enter through the current source stack before changing a mechanics
surface:

1. root workspace `AGENTS.md`
2. `aoa-skills/AGENTS.md`
3. `aoa-skills/README.md`
4. `aoa-skills/ROADMAP.md`
5. `aoa-skills/docs/ARCHITECTURE.md`
6. `aoa-skills/mechanics/boundary-bridge/docs/LAYER_POSITION.md`
7. `aoa-skills/mechanics/boundary-bridge/docs/BRIDGE_SPEC.md`
8. `aoa-skills/mechanics/release-support/docs/RUNTIME_PATH.md`
9. `aoa-skills/mechanics/AGENTS.md`
10. `aoa-skills/mechanics/README.md`
11. target package card and nearest local `AGENTS.md`
12. touched canonical skill bundles only if skill meaning is in scope
13. affected config, generated, export, manifest, docs, and tests

Return to `Agents-of-Abyss` when the work needs to answer:

- Does this mechanic route match the center's owner split posture?
- Is this active/provenance/legacy/generated distinction honest?
- Does this make the center feel more powerful instead of making owner routing
  easier?
- Would the same move violate AoA's package route standard?

Return to `aoa-techniques` when the work needs to answer:

- Is the pass projection-first rather than movement-first?
- Has direct reading accepted the target group?
- Is there a receipt for path movement?
- Are generated projections weaker than authored bundle meaning?
- Are we preserving useful axes instead of collapsing every axis into the tree?

## Reformation Rhythm

Use this rhythm for every substantial pass. It is a cadence, not a railroad.
If a step reveals that another route is more honest, pause and route there.

### 0. Re-enter

- Read this file after compaction or long pause.
- Read the current root and repo `AGENTS.md` stack.
- Run `git status --short` in `aoa-skills`.
- Name existing dirty work before adding anything.
- Identify whether the current task is study, planning, or mutation.
- If mutation is not explicitly in scope, stay read-only.

### 1. Choose One Owner Surface

For a mechanics pass, name exactly one owner surface:

- a mechanics package such as `mechanics/agon`
- the mechanics atlas `mechanics/README.md`
- one future package pressure group
- one validation or generated seam tied to that package
- one legacy/provenance correction

If the pass touches skill bundle meaning, the owner surface becomes the
canonical skill bundle and mechanics becomes context, not owner.

### 2. Direct-Read Before Movement

Read the actual source surfaces, not just filenames:

- package card and local route surfaces
- old flat docs or source files
- related config seeds
- generated companions
- manifests and hooks
- tests
- README, ROADMAP, docs map, and current direction references
- affected canonical skills if any

Write a source map before moving any path:

```text
source surface -> current role -> active destination -> provenance route -> generated/export consumers -> validation
```

### 3. Name The Mechanic Pressure

Use mechanics as movement grammar, not as a storage target.

Ask:

- What is trying to move?
- Is it candidate intake, validation, recurrence, checkpoint carry, release
  support, adoption, audit, bridge pressure, risk posture, or public route
  pressure?
- What does `aoa-skills` own locally?
- Which stronger owner keeps final truth?
- What must not be claimed?
- What can leave the package without becoming skill canon?

### 4. Compare Against AoA

Open the corresponding AoA mechanic when available.

Check:

- package card headings
- active route shape
- functioning parts
- provenance bridge
- legacy raw/artifacts split
- landing log
- roadmap
- owner split
- validation lane
- stop-lines

Translate the pattern. Do not copy the authority.

### 5. Compare Against Techniques

Use `aoa-techniques` for migration discipline:

- projection-first
- direct-read review
- bounded subtree
- root legacy receipt for authored path movement
- link repair in the same wave
- generated rebuild when derived surfaces depend on source movement
- validation before next move

Do not copy technique tree shape into mechanics. Do not copy mechanic package
shape into skill bundles.

### 6. Decide The Smallest Honest Move

Choose the smallest pass that makes the repo easier to enter:

- correct one wrong legacy route
- land one package-local active part
- move one bounded flat-doc family into one package
- repair one route map after a move
- add one validation expectation that actually runs
- add one provenance bridge that reduces duplication
- defer when direct reading does not justify movement

Reject the move when:

- the result creates a second active door
- the group is only connected by filename
- the destination would be a junk drawer
- generated surfaces would become source truth
- a stronger owner would be overwritten locally
- validation cannot honestly cover the claim

### 7. Mutate Cleanly

When mutation is in scope:

- announce the intended touched paths.
- use `apply_patch` for manual file edits.
- move only the bounded set chosen by direct reading.
- preserve history through a clear legacy/provenance route.
- keep active docs concise and functional.
- keep old wording as raw/provenance, not active route language.
- update links in the same pass.
- update tests and validators only for real routes.
- do not edit unrelated dirty files.

### 8. Verify Narrowly

Pick checks based on the changed surface:

- mechanics `AGENTS.md` changes:
  `python scripts/validate_nested_agents.py`
- Agon candidate surfaces:
  `python scripts/build_agon_skill_binding_candidates.py --check`
  `python scripts/validate_agon_skill_binding_candidates.py`
  `python scripts/build_agon_epistemic_skill_candidates.py --check`
  `python scripts/validate_agon_epistemic_skill_candidates.py`
- skill bundle source changes:
  `python scripts/build_catalog.py`
  `python scripts/validate_skills.py`
  `python scripts/build_catalog.py --check`
- generated/export changes:
  run the specific builder in `--check` mode first, then write only when
  source change requires it.
- broad mechanics topology:
  use the local topology test if present, plus relevant root docs route tests.

If a check is skipped, record why. Do not claim a check passed if it was not
run.

### 9. Close The Loop

Before ending a pass:

- re-run `git status --short`
- list touched files
- identify active source truth
- identify legacy/provenance route
- identify generated/export consumers
- identify tests run and skipped
- identify any remaining risk or next bounded package
- if a structural decision will matter later, add or update a decision record
  only after the actual decision is clear

## Mechanics Inventory Rhythm

Build the mechanics inventory before reforming the skill tree.

For each candidate mechanic, produce a compact map:

```text
mechanic:
  current pressure:
  current surfaces:
  canonical skill surfaces touched:
  config seeds:
  generated/export consumers:
  tests/validators:
  stronger owners:
  must not claim:
  possible package parts:
  legacy/provenance need:
  first honest move:
  stop-line:
```

### Agon

Current status: first package exists, but the current dirty attempt uses the
wrong legacy route vocabulary.

Known pressure:

- requested-only bounded workflow candidates behind lawful moves
- skill-binding candidate seeds
- epistemic workflow candidate seeds
- observation-only recurrence pressure
- validation routes

Known risk:

- `legacy/docs-root/` is not AoA mechanic legacy language.
- Old flat `docs/AGON_*.md` files must become raw/provenance lineage or active
  functional parts, not a duplicate active docs root.

Likely active parts:

- workflow candidate bridge
- candidate validation gate
- recurrence observation
- epistemic candidate boundary

First correction when mutation resumes:

- replace `mechanics/agon/legacy/docs-root/` with a package-local legacy model
  aligned to AoA, likely `legacy/raw/` for old flat source snapshots.
- add or align `legacy/INDEX.md` and possibly `DISTILLATION_LOG.md` if source
  accounting needs dated decisions.
- keep functional active part names.

### Distillation

Pressure to inventory:

- candidate lineage
- candidate-ref refinery
- session harvest notes
- skill-shaped donor intake
- source-to-active accounting for candidate material

Likely sources to inspect:

- session donor harvest skill family
- automation opportunity scan
- quest harvest
- docs around governed followthrough and owner status
- references carrying receipt schemas

## Current Mechanics Inventory Pass

This pass is a working map for the mechanics reformation. It is not a public
index and not a replacement for package-local cards.

### Agon

mechanic:
  current pressure: requested-only skill-layer workflow candidates behind
    center-side lawful moves; generated Agon candidate surfaces; recurrence
    observation around candidate pressure.
  current surfaces: `mechanics/agon/`, `config/agon_*_candidates.seed.json`,
    generated Agon companions, recurrence manifests, former flat
    `docs/AGON_*.md` snapshots preserved under package-local `legacy/raw/`.
  canonical skill surfaces touched: none by design.
  config seeds: `config/agon_skill_binding_candidates.seed.json`,
    `config/agon_epistemic_skill_candidates.seed.json`.
  generated/export consumers: generated Agon candidates and recurrence
    manifests; no `.agents/skills/` meaning change.
  tests/validators: Agon builders, Agon validators, mechanics topology,
    current-direction routes, roadmap parity, nested AGENTS.
  stronger owners: `Agents-of-Abyss` for Agon law, `aoa-techniques` for
    practice candidates, `aoa-evals` for proof, `aoa-routing` for routing,
    `aoa-agents` for actors, `Tree-of-Sophia` for canon-facing meaning.
  must not claim: lawful move vocabulary, proof verdict, scars, routing
    sovereignty, runtime activation, automatic skill promotion.
  possible package parts: workflow candidate bridge, candidate validation
    gate, recurrence observation, epistemic candidate boundary.
  legacy/provenance need: package-local `legacy/raw/`, `legacy/INDEX.md`, and
    `legacy/DISTILLATION_LOG.md` account for former flat docs without keeping a
    duplicate active docs route.
  first honest move: corrected in this pass by removing the `docs-root`
    vocabulary and reanchoring preserved Agon material as raw lineage.
  stop-line: no skill bundle moves; normal skill review remains the only route
    to skill canon.

### Distillation

mechanic:
  current pressure: candidate lineage, candidate-ref refinement, reviewed
    donor harvest, source-to-active accounting, and owner-safe extraction from
    session or checkpoint material.
  current surfaces: `docs/session-harvests/`, session-harvest skill
    references, candidate-harvest templates, and source material that needs
    active extraction without becoming final owner truth. The reviewed
    `candidate_ref` lineage docs moved to method-growth because their function
    is Growth Refinery identity and owner landing, not raw-to-active
    distillation.
  canonical skill surfaces touched: session-growth kernel skills only as
    source truth to read, not as mechanics destinations.
  config seeds: project-core kernel and governance surfaces provide the guard
    around donor/route/progression/quest receipts.
  generated/export consumers: project-core kernel governance, quest catalog,
    runtime discovery, generated skill catalogs, and stats-event compatible
    receipts.
  tests/validators: session checkpoint tests, session growth maturity tests,
    generated surface schema checks, skill validation, catalog checks.
  stronger owners: `Agents-of-Abyss` for center distillation law,
    `aoa-memo` for memory, `aoa-evals` for proof, `Dionysus` for seed/donor
    staging, `aoa-playbooks` for recurring scenarios, final owner repos for
    accepted object truth.
  must not claim: summary-as-proof, memory canon, owner acceptance, runtime
    activation, final skill truth, ToS canon, raw deletion authority.
  possible package parts: raw intake, raw preservation, provenance bridge,
    active extraction, noise pruning, receipt index, candidate handoff,
    validation gate.
  legacy/provenance need: likely high, because existing session harvests and
    candidate references need source-to-active accounting rather than flat
    relocation.
  first honest move: direct-read the session-harvest family before creating a
    package; do not move session-harvest docs until the active package route
    can explain what stays under skill canon and what becomes movement grammar.
  stop-line: distillation may prepare candidate handoff; it may not mint final
    skill, memory, proof, seed, or playbook truth.

### Method-Growth

mechanic:
  current pressure: governance consent, maturity, promotion, public status,
    reviewed candidate identity, owner-status landing, route followthrough, and
    adopted-skill retention after the adoption lifecycle slice.
  current surfaces:
    `mechanics/method-growth/parts/adoption-boundary/README.md`,
    `mechanics/method-growth/parts/adoption-evidence-receipts/README.md`,
    `mechanics/method-growth/parts/retention-regression-retirement/README.md`,
    `mechanics/method-growth/parts/pattern-adoption-handoff/README.md`,
    `mechanics/method-growth/legacy/adoption-wave/INDEX.md`,
    `mechanics/experience/docs/GOVERNANCE_SKILL_ADOPTION.md`,
    `mechanics/method-growth/docs/CANDIDATE_LINEAGE_CONTRACT.md`,
    `mechanics/method-growth/docs/CANDIDATE_REF_REFINERY.md`,
    `mechanics/method-growth/docs/OWNER_STATUS_SURFACES.md`,
    `mechanics/method-growth/docs/GOVERNED_FOLLOWTHROUGH.md`,
    `mechanics/method-growth/docs/MATURITY_MODEL.md`, `mechanics/method-growth/docs/PROMOTION_PATH.md`,
    review candidate/status promotion docs, and project-core ring governance.
  canonical skill surfaces touched: only when adoption pressure becomes an
    actual skill edit through normal review.
  config seeds: `config/project_core_skill_kernel.json`,
    `config/project_core_outer_ring.json`,
    `config/project_risk_guard_ring.json`, `config/skill_pack_profiles.json`,
    `config/skill_policy_matrix.json`.
  generated/export consumers: project-core kernel governance, outer-ring
    readiness, risk-guard governance, skill evaluation matrix, governance
    backlog, pack profiles, local adapter manifests.
  tests/validators: canonical gate checks, evaluated status checks, maturity
    model docs, promotion path governance, project-core governance, pack
    profile linting, full skill validation.
  stronger owners: `Agents-of-Abyss` for center method-growth route,
    `aoa-techniques` for reusable practice truth, `aoa-evals` for proof,
    downstream owner repos for adoption acceptance.
  must not claim: hidden assistant self-adoption, automatic owner consent,
    adoption by generated readout, durable behavior change without evidence and
    rollback.
  landed package parts: candidate lineage, owner-status landing, governed
    followthrough, adoption boundary, adoption evidence receipts,
    retention/regression/retirement, and pattern adoption handoff.
  possible remaining parts: governance consent, maturity ladder, public status
    bridge, promotion review route, adopted-skill retention refinement.
  legacy/provenance need: moderate; the first lineage slice keeps active docs
    under package-local `docs/` and records moved-path accounting in
    `PROVENANCE.md`. The adoption lifecycle slice preserved repetitive v0.7
    downstream adoption docs under `legacy/adoption-wave/raw/` and distilled
    active behavior into parts. Governance v0.8 stayed flat for later
    experience/governance review.
  first honest move: landed candidate-lineage first, then landed adoption
    lifecycle after direct reading separated v0.7 adoption from v0.8 governance.
  stop-line: method-growth routes skill change; it does not approve local
    adoption for another repository.

### Audit

mechanic:
  current pressure: evaluation path, trigger quality, public surface, maturity,
    promotion review, governance backlog, description-first activation checks,
    skills-ref conformance, and collision stress.
  current surfaces: `mechanics/audit/docs/EVALUATION_PATH.md`, `mechanics/audit/docs/PUBLIC_SURFACE.md`,
    `mechanics/audit/docs/TRIGGER_EVALS.md`, `mechanics/audit/docs/DESCRIPTION_TRIGGER_EVALS.md`,
    `mechanics/audit/docs/SKILLS_REF_VALIDATION.md`,
    `mechanics/antifragility/parts/collision-stress-program/README.md`,
    `mechanics/method-growth/docs/MATURITY_MODEL.md`,
    `mechanics/method-growth/docs/PROMOTION_PATH.md`, `docs/reviews/`, and generated evaluation
    readouts.
  canonical skill surfaces touched: none unless an audit finding becomes a
    reviewed skill wording change.
  config seeds: `config/description_trigger_eval_policy.json`,
    `config/skill_policy_matrix.json`, tiny-router bands when routing pressure
    is in scope.
  generated/export consumers: skill evaluation matrix, trigger eval cases,
    description trigger eval cases, skills-ref validation manifest, governance
    backlog, public surface.
  tests/validators: report skill evaluation, trigger lint, description-trigger
    lint, skills-ref wrapper, generated schema checks, review/status-promotion
    tests.
  stronger owners: `aoa-evals` for proof doctrine; `aoa-routing` for routing
    policy; `Agents-of-Abyss` for center audit posture.
  must not claim: proof verdict, public promise without support evidence,
    downstream activation, routing sovereignty.
  possible package parts: evaluation lane, public-surface readout,
    trigger-quality audit, review truth-sync, status promotion review,
    conformance lane, collision stress.
  legacy/provenance need: moderate; old wave docs should become active audit
    routes or raw history, not another flat audit pile.
  first honest move: package later after deciding whether audit owns
    review-truth surfaces or whether they remain under `docs/reviews/` as
    source evidence.
  stop-line: audit sees and routes; it does not prove final truth.

### Growth-Cycle

mechanic:
  current pressure: adaptive orchestration, session-growth kernel maturity,
    checkpoint-aware closeout, donor harvest, route forks, self-diagnose,
    self-repair, progression lift, quest harvest, and automation scan.
  current surfaces: `mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md`,
    `mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md`,
    `mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md`, `mechanics/questbook/QUESTBOOK.md`,
    session-harvest docs, kernel skill references, and project-core kernel
    governance.
  canonical skill surfaces touched: session-growth kernel bundles remain
    canonical under `skills/` and `.agents/skills/`; mechanics may only route
    their family posture.
  config seeds: `config/project_core_skill_kernel.json`, session checkpoint
    schemas, quest schemas.
  generated/export consumers: project core kernel governance,
    generated quest catalog/dispatch, runtime discovery, stats-event receipt
    surfaces.
  tests/validators: session growth maturity, session checkpoint, project-core
    kernel governance, generated schema checks, quest catalog checks.
  stronger owners: `Agents-of-Abyss` for center growth-cycle law,
    `aoa-agents` for checkpoint/role posture, `aoa-playbooks` for recurring
    scenarios, `aoa-memo` for memory, `aoa-stats` for derived stats.
  must not claim: hidden scheduler, live runtime state, universal progression
    score, proof verdict, memory canon, automatic repair.
  possible package parts: adaptive orchestration, session kernel maturity,
    harvest note boundary, reviewed closeout chain, donor harvest entry, route
    forks, self-diagnose, self-repair, progression lift, quest harvest,
    automation scan.
  legacy/provenance need: high; the first orchestration slice moved only active
    guidance docs. Session-harvest docs are evidence-bearing and must not be
    flattened into active route text.
  first honest move: landed adaptive orchestration and session-kernel maturity.
    Next work should decide whether session-harvest notes move through a
    provenance-heavy pass or remain as docs evidence.
  stop-line: growth-cycle can require reviewed evidence and order of execution;
    it cannot silently mutate the repo or decide final promotion.

### Questbook

mechanic:
  current pressure: durable skill obligations that survive a bounded diff,
    quest dispatch, promotion/harvest verdicts, and project-core follow-through.
  current surfaces: `mechanics/questbook/QUESTBOOK.md`,
    `mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md`,
    `quests/*.yaml`, quest schemas, generated quest catalog and dispatch
    examples, `aoa-quest-harvest` references.
  canonical skill surfaces touched: `aoa-quest-harvest` only as source truth
    for allowed verdicts.
  config seeds: quest schemas and project-core kernel surfaces.
  generated/export consumers: generated quest catalog, quest dispatch, public
    backlog/readouts where relevant.
  tests/validators: quest schema/generated surface tests and kernel governance
    tests.
  stronger owners: `aoa-playbooks` for recurring scenario composition,
    `aoa-evals` for proof follow-through, owner repos for closing their own
    obligations.
  must not claim: second roadmap, hidden backlog authority, private scratchpad,
    automatic promotion.
  landed package parts: source index boundary, session-harvest posture, and
    dispatch projection.
  legacy/provenance need: low-to-moderate; `mechanics/questbook/QUESTBOOK.md` may remain package-local
    if it is the public tracked obligation surface.
  first honest move: landed the integration posture slice after
    growth-cycle/checkpoint split became clear. `mechanics/questbook/QUESTBOOK.md`,
    `quests/`, schemas, and generated projections stayed in place.
  next honest move: decide later whether root quest object route receipts or
    generated quest validation notes need a package-local companion. Do not
    move the root questbook just to match AoA.
  stop-line: questbook keeps obligations visible; it does not close them.

### Checkpoint

mechanic:
  current pressure: lower-authority checkpoint notes, reviewed-closeout bridge,
    owner-promotion follow-through, and pre-harvest carry through context
    compaction.
  current surfaces: `mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md`,
    `aoa-checkpoint-closeout-bridge` references, session checkpoint schema and
    tests, runtime checkpoint notes produced by `aoa skills enter`.
  canonical skill surfaces touched: bridge skill remains canonical; mechanics
    may expose route boundaries only.
  config seeds: session checkpoint schema; project-core kernel governance.
  generated/export consumers: runtime/session-growth notes and stats-refresh
    hints; no generated surface should become authority.
  tests/validators: session checkpoint tests, bridge evaluation snapshots,
    kernel governance, validation of agent skills.
  stronger owners: `aoa-agents` for checkpoint contract posture,
    `aoa-memo` for durable memory, `aoa-stats` for derived summaries,
    final owner repo for accepted follow-through.
  must not claim: final harvest, progression verdict, quest authority, memory
    canon, owner acceptance.
  possible package parts: checkpoint note lane, closeout bridge boundary,
    compaction carry, owner follow-through, stats-refresh boundary.
  legacy/provenance need: moderate; the first checkpoint slice keeps the active
    note doc under package-local `docs/` and records moved-path accounting in
    `PROVENANCE.md`. Runtime-produced notes are evidence but should not be made
    source truth.
  first honest move: landed the checkpoint-note and closeout-bridge-boundary
    slice. Later work should not absorb SDK controls, session-growth maturity,
    or runtime exports until their owner split is explicit.
  stop-line: checkpoint preserves and routes; it does not decide.

### Release-Support

mechanic:
  current pressure: Codex portable export, install profiles, local adapter,
    runtime seam, governed runtime guardrails, support resources, release
    manifest, import/export/stage/verify pack scripts, and downstream feeds.
  current surfaces: `mechanics/release-support/docs/CODEX_PORTABLE_LAYER.md`,
    `mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md`, `mechanics/release-support/docs/LOCAL_ADAPTER_CONTRACT.md`,
    `mechanics/release-support/docs/RUNTIME_PATH.md`, `mechanics/release-support/docs/INSTALL_AND_PROFILES.md`,
    `mechanics/release-support/docs/DETERMINISTIC_RESOURCE_BUNDLES.md`,
    `mechanics/release-support/docs/RUNTIME_SEAM_SECOND_PATH.md`,
    `mechanics/release-support/docs/RUNTIME_TOOL_CONTRACTS.md`,
    `mechanics/release-support/docs/RUNTIME_GOVERNANCE_LAYER.md`,
    `mechanics/release-support/docs/TRUST_GATE_AND_ALLOWLIST.md`,
    `mechanics/release-support/docs/CONTEXT_RETENTION.md`, `mechanics/release-support/docs/SESSION_COMPACTION.md`,
    `mechanics/release-support/docs/SKILL_CONTEXT_GUARD.md`, `mechanics/release-support/docs/RELEASING.md`,
    generated runtime/export manifests, support resource manifests, and pack
    scripts.
  canonical skill surfaces touched: support bundles under `skills/*` only when
    resource truth changes; `.agents/skills/*` remains generated export.
  config seeds: skill pack profiles, policy matrix, runtime guardrail policy,
    portable overrides, OpenAI extensions.
  generated/export consumers: `.agents/skills/`, local adapter manifests,
    runtime seam manifests, guardrail manifests, release manifest, support
    resource index, downstream feed contracts.
  tests/validators: build/validate agent skills, runtime seam tests,
    guardrail tests, support resource tests, import/export/stage/verify tests,
    release check.
  stronger owners: `abyss-stack` for runtime infrastructure, `aoa-sdk` for
    typed helpers and workspace control, downstream repos for adoption, Codex
    runtime for host behavior.
  must not claim: release approval, runtime authority, second authoring format,
    generated export as source truth, hidden auto-activation.
  possible package parts: portable export, install profiles, local adapter,
    runtime seam, governed guardrails, support bundles, release manifest,
    downstream feed.
  legacy/provenance need: high; many wave docs are still active support
    contracts, not raw history.
  first honest move: do not move as one package yet. It is too broad and should
    likely be split after smaller mechanics stabilize.
  stop-line: release-support packages and exports; it does not own runtime
    behavior or public release truth by itself.

### Boundary-Bridge

mechanic:
  current pressure: layer position, bridge spec, support-dir bridge, overlays,
    two-stage skill selection, tiny-router downstream cues, OpenAI/MCP wiring,
    and owner stop-lines.
  current surfaces: `mechanics/boundary-bridge/docs/LAYER_POSITION.md`, `mechanics/boundary-bridge/docs/BRIDGE_SPEC.md`,
    `mechanics/boundary-bridge/docs/BRIDGE_FROM_AOA_SUPPORT_DIRS.md`,
    `mechanics/boundary-bridge/docs/TWO_STAGE_SKILL_SELECTION.md`, `mechanics/boundary-bridge/docs/OVERLAY_SPEC.md`,
    `mechanics/boundary-bridge/docs/CODEX_SKILL_MCP_WIRING.md`,
    `mechanics/boundary-bridge/docs/OPENAI_SKILL_EXTENSIONS.md`, overlay docs, tiny-router config and
    generated capsules.
  canonical skill surfaces touched: only when a real skill dependency or
    overlay changes through its source policy path.
  config seeds: `config/tiny_router_skill_bands.json`,
    `config/openai_skill_extensions.json`, portable overrides, pack profiles.
  generated/export consumers: tiny-router signals, overlay manifests,
    local adapter manifests, generated OpenAI YAML exports.
  tests/validators: tiny-router input validation, MCP wiring validation,
    overlay contract tests, generated export validation.
  stronger owners: `aoa-routing` for routing policy, `Agents-of-Abyss` for
    center layer law, downstream project repos for local overlay truth.
  must not claim: routing sovereignty, owner acceptance, generated metadata as
    doctrine, identity collapse between base skill and overlay.
  possible package parts: layer boundary, bridge spec, support-dir bridge,
    overlay boundary, two-stage selection, MCP wiring, tiny-router feed.
  legacy/provenance need: moderate; many docs are active bridge contracts and
    should not be archived prematurely.
  first honest move: wait until mechanics atlas and Agon are stable; package
    only a narrow bridge slice when link repair can be verified.
  stop-line: bridge connects surfaces without transferring authority.

### Recurrence

mechanic:
  current pressure: live observation producers, recurrence review decision
    closure, component refresh law, Agon recurrence observation, recurring
    candidate watchers, and downstream refresh routes.
  current surfaces:
    `mechanics/recurrence/parts/live-observation-producers/README.md`,
    `mechanics/recurrence/parts/review-decision-closure/README.md`,
    `mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md`, recurrence manifests, Agon recurrence
    part, and refresh scripts.
  canonical skill surfaces touched: none unless a recurring observation becomes
    reviewed skill change.
  config seeds: recurrence manifests and component hook manifests.
  generated/export consumers: recurrence component readouts and downstream
    refresh signals.
  tests/validators: recurrence-related manifest tests, component refresh law
    tests, Agon recurrence validation where applicable.
  stronger owners: `Agents-of-Abyss` for recurrence law, owner repos for
    accepted refreshes, `aoa-stats` for derived movement visibility.
  must not claim: ambient continuity, automatic refresh, automatic recursor
    spawn, hidden memory sovereignty.
  landed package parts: observation producers and review decision closure.
  possible remaining parts: component refresh, owner refresh handoff, downstream
    drift watch, and manifest validation notes.
  legacy/provenance need: moderate.
  first honest move: landed observation/closure around cross-mechanic skill
    pressure. Kept Agon recurrence inside Agon and left component refresh law
    for a later release-support or recurrence pass.
  stop-line: recurrence observes and re-enters; it does not self-author fixes.

### Experience

mechanic:
  current pressure: office/service handoff, receipt generation, task
    boundaries, installation surfaces, runtime governance skills, stay orders,
    skill policy holds, governed adoption, and local owner consent.
  current surfaces: `mechanics/experience/docs/SERVICE_HANDOFF_SKILLS.md`,
    `mechanics/experience/docs/OFFICE_TASK_BOUNDARY_SKILLS.md`,
    `mechanics/experience/docs/RECEIPT_GENERATION_SKILLS.md`,
    `mechanics/experience/docs/INSTALLATION_SKILL_SURFACES.md`,
    `mechanics/experience/docs/GOVERNANCE_RUNTIME_SKILLS.md`,
    `mechanics/experience/docs/STAY_ORDER_SKILL.md`, `mechanics/experience/docs/SKILL_POLICY_HOLD.md`,
    `mechanics/experience/docs/GOVERNANCE_SKILL_ADOPTION.md`, adoption docs, and governance lanes.
  canonical skill surfaces touched: only if a live skill contract changes
    through normal review.
  config seeds: governance lanes, policy matrix, install profiles.
  generated/export consumers: governance backlog, public surface, release
    manifest, pack profiles, skill policy readouts.
  tests/validators: experience wave seed tests, governance lane tests, release
    docs/checks, adoption schema tests.
  stronger owners: `Agents-of-Abyss` for experience law,
    `Tree-of-Sophia` for no-runtime-write/canon boundaries, downstream office
    or service repos for activation.
  must not claim: release approval, assistant self-authority, runtime ToS write
    authority, local owner consent for another repo.
  possible package parts: service handoff, office task boundary, receipt
    generation, installation surface, governance runtime, stay/hold, adoption
    consent.
  legacy/provenance need: high; many wave docs are terse owner-local contract
    surfaces that need distillation before movement.
  first honest move: likely after method-growth and release-support split,
    because experience overlaps adoption and install/release pressure.
  stop-line: experience contracts stay owner-local and consent-bound.

### Antifragility

mechanic:
  current pressure: degraded-mode guidance, via negativa, rollback drills,
    trigger-collision stress, explicit risk posture, and safety perimeter.
  current surfaces:
    `mechanics/antifragility/parts/fallback-authoring-posture/README.md`,
    `mechanics/antifragility/parts/via-negativa-pruning/README.md`,
    `mechanics/experience/docs/ROLLBACK_DRILL_SKILL.md`,
    `mechanics/antifragility/parts/collision-stress-program/README.md`,
    risk-guard ring config, risk skill bundles and deterministic resource
    bundles.
  canonical skill surfaces touched: risk guard skills only through normal
    bundle/support-resource review.
  config seeds: `config/project_risk_guard_ring.json`,
    `config/skill_policy_matrix.json`, runtime guardrail policy.
  generated/export consumers: risk guard governance, trigger collision matrix,
    runtime contracts, support resource manifests.
  tests/validators: risk guard governance, collision eval tests, support
    resource tests, dry-run/infra/local-stack support tests.
  stronger owners: `Agents-of-Abyss` for center antifragility law, owner repos
    for operational rollback or cleanup, `aoa-evals` for proof.
  must not claim: one-score health, deletion theater, unsafe rollback,
    owner-local cleanup authority, hidden mutation.
  landed package parts: fallback authoring posture, via negativa pruning, and
    collision stress program.
  possible remaining parts: rollback drill release/experience boundary, risk
    perimeter, risk-ring validation notes, and support-resource hardening.
  legacy/provenance need: moderate; the first landing moved active route docs
    directly into parts and kept rollback drill flat because its own text routes
    to installation and first sovereign release posture.
  first honest move: landed fallback/pruning/collision after direct reading.
    Do not absorb rollback drill until release-support or experience boundaries
    are clearer.
  stop-line: stress reveals and constrains; it does not perform cleanup without
    owner authority.

### RPG

mechanic:
  current pressure: ability card/loadout reader surfaces, pack-profile-aware
    unlock posture, session progression reflection, and quest/progression
    vocabulary around skills.
  current surfaces:
    `mechanics/rpg/parts/ability-reader-boundary/README.md`,
    `mechanics/rpg/parts/loadout-posture/README.md`,
    ability schemas/examples, generated ability catalogs, progression skill
    references, questbook surfaces.
  canonical skill surfaces touched: none unless skill descriptions or metadata
    change through normal review.
  config seeds: pack profiles and ability/loadout schemas.
  generated/export consumers: ability catalog/readers and profile-derived
    views.
  tests/validators: skill ability catalog schema tests, pack profile tests,
    progression evaluation snapshots.
  stronger owners: `Agents-of-Abyss` for RPG adjunct posture,
    `aoa-agents` for role/progression contracts, `aoa-playbooks` for
    questline/campaign composition.
  must not claim: runtime ledger, hidden ontology, decorative game skin,
    universal progression score.
  landed package parts: ability-reader boundary and loadout posture.
  possible remaining parts: progression reflection, quest/ability bridge,
    generated ability validation notes, and owner handoff cues.
  legacy/provenance need: low-to-moderate.
  first honest move: landed the ability/loadout reader slice after recurrence
    and questbook were separated. Kept generated examples, schemas, pack
    profiles, and progression artifacts in place.
  stop-line: RPG reads and reflects; it does not rewrite skill truth.

## Current Ordering Hypothesis

The next mechanics work should not chase the widest or flashiest package.

1. Finish Agon as the first local proof of package rhythm.
2. Use the inventory above to avoid turning `mechanics/` into a dumping ground.
3. Prefer a compact package only when direct reading can name active parts,
   provenance route, generated/export consumers, and validation.
4. Method-growth candidate lineage and Checkpoint note/bridge boundary have now
   landed as narrow packages because direct reading justified them.
5. Growth-cycle orchestration and kernel maturity have now landed as a narrow
   package. The remaining overlap is mainly distillation versus harvest-note
   evidence and questbook/automation pressure.
6. `release-support`, `experience`, and `boundary-bridge` are important but too
   wide for a second package unless split into a narrow bounded slice.
7. `questbook`, `recurrence`, `rpg`, and `antifragility` now have bounded first
   packages. Their remaining pressure should stay package-local or route to
   release-support, experience, audit, or downstream owners after direct
   reading.

## Stop Condition For The Next Move

Before creating or moving another mechanics package, the agent must be able to
write this in one breath:

```text
I am moving <bounded source family> into mechanics/<slug> because it describes
<movement grammar>, not skill meaning. The active route will be <parts>. The
source lineage will be preserved by <provenance/legacy route>. The generated or
export consumers are <surfaces>. The stronger owners are <owners>. The
validation is <checks>. The stop-line is <what this cannot claim>.
```

If that sentence is not true, keep studying or record a hold instead of moving
files.
- generated runtime discovery and governance surfaces

Useful AoA return:

- `mechanics/distillation`
- raw intake, raw preservation, provenance bridge, active extraction,
  validation gate, candidate handoff

Do not claim:

- proof verdict
- memory canon
- owner acceptance
- technique publication

### Method-Growth

Pressure to inventory:

- governance consent after the v0.8 adoption/governance split
- maturity model and promotion path
- public status and governance backlog
- default-reference decisions
- adopted-skill retention refinement after the landed v0.7 lifecycle slice

Likely sources to inspect:

- `mechanics/method-growth/parts/adoption-boundary/README.md`
- `mechanics/method-growth/parts/adoption-evidence-receipts/README.md`
- `mechanics/method-growth/parts/retention-regression-retirement/README.md`
- `mechanics/method-growth/parts/pattern-adoption-handoff/README.md`
- `mechanics/experience/docs/GOVERNANCE_SKILL_ADOPTION.md`
- maturity model
- promotion path
- governance backlog
- public surface
- skill evaluation matrix
- default-reference roadmap sections
- canonical/evaluated/scaffold status rules

Do not claim:

- technique canon
- public proof beyond available evaluation evidence
- owner-local adoption outside this repo

### Audit

Pressure to inventory:

- evaluation path
- public surface
- maturity model
- promotion reviews
- trigger evaluations
- governance backlog
- review records

Likely sources to inspect:

- `mechanics/audit/docs/EVALUATION_PATH.md`
- trigger eval docs and fixtures
- generated evaluation matrix
- governance backlog
- public surface generated outputs
- validation scripts

Do not claim:

- proof doctrine that belongs in `aoa-evals`
- owner remediation
- generated report as source truth

### Growth-Cycle

Pressure to inventory:

- adaptive skill orchestration
- session-growth kernel maturity
- checkpoint-aware closeout
- progression-adjacent workflow pressure
- post-session harvest chain

Likely sources to inspect:

- `mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md`
- `mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md`
- checkpoint closeout bridge
- session donor harvest
- session progression lift
- route forks
- self diagnose and self repair
- quest harvest

Do not claim:

- hidden scheduler
- progression canon
- memory canon
- owner acceptance

### Questbook

Pressure to inventory:

- `mechanics/questbook/QUESTBOOK.md`
- quest dispatch
- durable skill obligations
- recurring cross-repo follow-through

Likely sources to inspect:

- `mechanics/questbook/QUESTBOOK.md`
- `mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md`
- generated quest catalog and dispatch
- quest harvest skill

Do not claim:

- second roadmap
- private scratchpad
- playbook scenario canon

### Checkpoint

Pressure to inventory:

- checkpoint notes
- reviewed-closeout bridge posture
- lower-authority pre-harvest carry
- checkpoint-to-closeout handoff

Likely sources to inspect:

- `mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md`
- checkpoint closeout bridge skill
- templates and examples for checkpoint notes
- `mechanics/method-growth/docs/GOVERNED_FOLLOWTHROUGH.md`

Do not claim:

- checkpoint implementation authority
- final harvest/progression/quest truth from provisional notes alone

### Release-Support

Pressure to inventory:

- portable export
- install profiles
- local adapter
- runtime seam
- support resources
- release manifest packaging
- OpenAI/Codex export compatibility

Likely sources to inspect:

- `mechanics/release-support/docs/CODEX_PORTABLE_LAYER.md`
- `mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md`
- `mechanics/release-support/docs/LOCAL_ADAPTER_CONTRACT.md`
- `mechanics/release-support/docs/RUNTIME_PATH.md`
- `mechanics/release-support/docs/INSTALL_AND_PROFILES.md`
- generated release manifest
- `.agents/skills/*`
- export builders

Do not claim:

- GitHub release as the only definition of runtime support
- downstream install success without evidence
- generated export as canonical skill wording

### Boundary-Bridge

Pressure to inventory:

- layer boundaries
- overlays
- downstream tiny-router bridge
- cross-repo owner stop-lines
- bridge from AoA support dirs

Likely sources to inspect:

- `mechanics/boundary-bridge/docs/LAYER_POSITION.md`
- `mechanics/boundary-bridge/docs/OVERLAY_SPEC.md`
- `mechanics/boundary-bridge/docs/BRIDGE_FROM_AOA_SUPPORT_DIRS.md`
- `mechanics/boundary-bridge/docs/TWO_STAGE_SKILL_SELECTION.md`
- overlay docs
- config skill pack profiles
- generated tiny-router and support bridge maps

Do not claim:

- downstream authority
- route policy belonging to `aoa-routing`
- project owner truth from a public overlay

### Recurrence

Pressure to inventory:

- live observation producers
- recurrence decision closure
- recurring skill-pressure watchers
- recurrence manifests and hooks

Likely sources to inspect:

- recurrence manifests
- hooks manifests
- Agon recurrence adapter surfaces
- component refresh law
- session compaction docs

Do not claim:

- automatic activation
- hidden memory sovereignty
- silent recursor spawn

### Experience

Pressure to inventory:

- governance and service handoff
- office-task boundaries
- adoption consent surfaces
- runtime-body evidence and local diagnostic overlays

Likely sources to inspect:

- abyss overlays
- local stack bringup
- safe infra change
- self diagnostic spine
- runtime contracts

Do not claim:

- live runtime authority
- infrastructure truth
- owner-local service acceptance

### Antifragility

Pressure to inventory:

- degraded-mode guidance
- rollback drills
- trigger-collision stress
- explicit risk posture
- failure analysis and repair loops

Likely sources to inspect:

- safe infra change
- dry run first
- approval gate check
- local stack bringup
- session self diagnose
- session self repair
- trigger collision docs

Do not claim:

- one-score health
- deletion theater
- silent mutation as repair

### RPG

Pressure to inventory:

- ability-card reader surfaces
- loadout posture
- adjunct progression language
- quest reflection cues

Likely sources to inspect:

- `mechanics/rpg/parts/ability-reader-boundary/README.md`
- `mechanics/rpg/parts/loadout-posture/README.md`
- generated ability examples
- session progression lift
- quest harvest

Do not claim:

- hidden ontology
- runtime ledger
- decorative game skin over owner truth

## Skill Tree Reform Later

Do not start the `skills/` tree migration until mechanics inventory is honest.

The future skill tree should be inspired by `aoa-techniques`, but should answer
skill questions:

- What kind of execution workflow is this?
- What risk or authority posture does it require?
- Is it public core, risk guard, continuity/growth, runtime/release, bridge,
  or project overlay?
- What canonical skill bundle owns the workflow?
- Which support artifacts stay with the bundle?
- Which generated/export surfaces consume it?

Possible future trunk vocabulary must be treated as hypothesis until direct
reading and projection:

- `execution`
- `proof`
- `governance-risk`
- `continuity-growth`
- `runtime-release`
- `bridge`
- `public-surface`
- `overlays`

Do not freeze these names early. Build a projection first.

## Projection-First Skill Tree Rhythm

When mechanics inventory is complete:

1. generate or hand-build a review projection without moving skill files
2. classify every skill by current path, name, scope, status, invocation mode,
   technique dependencies, support artifact shape, generated/export consumers,
   and direct-read function
3. propose trunk and shelf candidates
4. mark holds, splits, singletons, overlays, and unresolved owner questions
5. review one bounded shelf by direct reading
6. move only accepted bundles
7. preserve a root legacy receipt for path movement
8. repair links and generated consumers in the same wave
9. validate
10. repeat

Skill bundle shape remains:

```text
skills/<future-tree>/<skill-slug>/
  SKILL.md
  techniques.yaml
  agents/openai.yaml
  checks/
  examples/
  references/
  assets/
  scripts/
```

The exact future path is not decided here.

## Language Check

Before accepting a sentence into an active surface, ask:

- Does this sound like `aoa-skills`, the bounded execution canon?
- Does it speak in trigger boundaries, inputs, outputs, contracts, risks, and
  verification?
- Does it distinguish local owner authority from stronger owner truth?
- Does it avoid mythic language where operational clarity is needed?
- Does it avoid sterile bureaucracy where a concise route card is enough?
- Does it make future agents more capable rather than more obedient to a maze?
- Does it remove a tail or create one?

## Good Move Signals

A move is probably good when:

- the next reader has fewer plausible first doors
- active surfaces are shorter and more functional
- old material is preserved without staying active
- generated/export consumers are either updated or explicitly unaffected
- tests name the actual topology
- stronger owners are named without being copied
- the move creates a reusable pattern for the next bounded package

## Bad Move Signals

A move is probably bad when:

- it starts from path aesthetics rather than source reading
- it duplicates active text into legacy
- it invents a package because a filename contains a familiar word
- it creates a new root index that will need constant manual sync
- it moves support artifacts away from the canonical skill that needs them
- it treats a generated report as an authoring source
- it imports AoA center doctrine instead of translating owner posture
- it makes skill activation easier while making skill authority less clear

## Compaction Re-entry Packet

If context compacts, resume with this short packet:

1. Read `aoa-skills/AGENTS.md`.
2. Read `aoa-skills/mechanics/AGENTS.md`.
3. Read this file.
4. Run `git status --short`.
5. Confirm whether the current task is study, plan, or mutation.
6. Identify the one owner surface for the next pass.
7. Re-open AoA's matching mechanic before changing local mechanics.
8. Keep skill bundles in `skills/`.
9. Keep generated/export subordinate.
10. Close every move with source, provenance, validation, and next route.

## Current Immediate Focus

The next honest mechanics work should not start with a skill-tree migration.
It should finish understanding and correcting the mechanics layer.

Immediate bounded sequence:

1. Stabilize the Agon package shape.
2. Correct the wrong `docs-root` legacy vocabulary and path.
3. Add source-to-active accounting for old `docs/AGON_*.md` surfaces.
4. Verify Agon candidate builders, validators, route tests, and nested AGENTS.
5. Inventory future mechanics pressure groups without moving them.
6. Pick the next mechanics package only after direct reading shows a compact
   source group.
7. After mechanics inventory is clean, start skill-tree projection without
   moving skill files.

## Closeout Rule

Every pass should leave one of these honest states:

- no change, because direct reading rejected movement
- one bounded plan artifact
- one bounded mechanics package improvement
- one bounded legacy/provenance correction
- one bounded generated/export refresh from source
- one bounded validation/test repair

Never leave:

- half-moved active doors
- orphaned legacy snapshots
- broken links hidden behind a future promise
- generated drift without an owner note
- a route map that points to a surface that does not exist
- a claim that the next agent must trust without evidence
