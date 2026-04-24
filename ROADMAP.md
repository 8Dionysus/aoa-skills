# Roadmap

## Current baseline

Current public foundation:
- coherent docs surface
- public skill coverage across core, risk, and live project-overlay categories
- live governance counts kept in `generated/public_surface.md` and `generated/governance_backlog.md` rather than duplicated in source docs
- honest `techniques.yaml` coverage with pinned source refs across the skill surface
- first examples or checks for every current skill
- local validator for bundle shape, policy, and `SKILL_INDEX.md` coverage
- autonomy and trigger-boundary evaluation checks across the full current skill surface
- documented maturity ladder and promotion guidance for future status changes
- derived public-surface signaling in `docs/PUBLIC_SURFACE.md` and `generated/public_surface.*`
- repo-level baseline release identity in `CHANGELOG.md`, `docs/RELEASING.md`, tags, and GitHub release notes
- bounded release validation in `scripts/release_check.py`

The current `v0.3.x` release line also already carries:
- checkpoint-closeout and commit-growth follow-through skills such as `aoa-checkpoint-closeout-bridge`, `aoa-commit-growth-seam`, `aoa-automation-opportunity-scan`, `aoa-session-donor-harvest`, and the wider session-harvest family surfaced through `generated/runtime_discovery_index.json`
- checkpoint-aware and reviewed owner-status follow-through guidance in `docs/CHECKPOINT_NOTE_PATH.md`, `docs/OWNER_STATUS_SURFACES.md`, and `docs/GOVERNED_FOLLOWTHROUGH.md`
- Agon Wave IV bounded-workflow companion bridge surfaces in
  `docs/AGON_MOVE_SKILL_BRIDGE.md`, `docs/AGON_WAVE4_SKILL_LANDING.md`, and
  `generated/agon_skill_binding_candidates.min.json`, with all requests kept
  `requested_not_landed` until normal skill review accepts them
- quest carry-forward and dispatch adjuncts in `generated/quest_catalog.min.json` and `generated/quest_dispatch.min.json`
- local Codex or MCP disclosure plus adapter and compaction guidance in `docs/CODEX_SKILL_MCP_WIRING.md`, `docs/LOCAL_ADAPTER_CONTRACT.md`, and `docs/SESSION_COMPACTION.md`
- packaging, governance, and overlay-maturity readouts in `generated/governance_backlog.md`, `generated/overlay_readiness.md`, `generated/skill_bundle_index.md`, `generated/skill_graph.md`, and `generated/release_manifest.json`

Already-shipped repo-owned support layers now include:
- wave-3 Codex-facing portable export, install-profile, and local-adapter surfaces
- wave-4 raw runtime seam
- wave-5 limited skill-handoff bridge only; scenario canon lives in `aoa-playbooks`
- wave-6 governed runtime guardrails
- wave-7 description-first activation contract and soft conformance lane
- wave-8 deterministic support-resource bundles for three high-risk skills
- wave-9 tiny-router compression bridge for downstream routing

The next steps should use that derived governance layer to keep core governance decisions honest, keep live overlay families aligned under one contract, and push packaging prep rather than only increase skill count.
The first packaging pass should harden the portable release contract itself, then follow with compatibility/lineage depth rather than inventing another catalog surface.
Overlay preparation and packaging remain intentionally repo-local and thin: they should surface contracts and export primitives without introducing live downstream integrations or registries.

## Near-term sequence

The nearest waves should now be read in this order:

1. `v0.5` maturity and governance consolidation
2. `v0.6` project-overlay maturity
3. `v0.7` packaging and distribution prep

Repo-level semver releases such as `v0.3.3` describe bounded public baselines.
The wave labels below still describe internal maturity and packaging lanes rather than replacing that release identity.

`v0.3` and `v0.4` are no longer the main expansion frontier.
They remain active as maintenance and depth-improvement lanes, but the repository already has:
- schema-backed validation
- pinned lineage and drift tooling
- autonomy and trigger-boundary evaluation coverage
- derived runtime, evaluation, and public-surface layers

The main near-term risk is no longer missing baseline scaffolding.
It is ambiguity about which skills are the default references in adjacent workflow lanes,
how thin project overlays should mature without widening scope,
and how the public bundle surface should eventually package for portable reuse.
Another near-term risk is roadmap drift: checkpoint follow-through, owner-status
landing, quest dispatch, and local Codex or MCP disclosure are now shipped
surfaces and should stay visible in current-direction docs rather than only in
release notes.
Another planning risk is cross-repo rollout choreography: when a future wave splits source-owned bridge meaning from downstream consumption, merge order and rerun policy should be planned explicitly rather than left to PR folklore.

## v0.3 public core hardening

Continue the public core hardening pass with:
- validator and index parity for declared multi-family skill prefixes such as `aoa-*`, `atm10-*`, and `abyss-*`
- stable schemas for `SKILL.md` front matter, `techniques.yaml`, and `agents/openai.yaml`
- status-aware validation so maturity levels have machine-checkable floors instead of only documented intent
- pinned traceability to upstream technique source refs
- stronger build-time refresh helpers that move from alignment-only toward reviewable bridge composition
- drift detection when a referenced technique changes materially
- stronger autonomy checks for self-contained runtime use without live remote dependency
- this phase is now residual hardening, not initial scaffold growth

## v0.4 evaluation harness

The baseline evaluation harness now exists across the current public surface through:
- prompt-fixture coverage in `tests/fixtures/skill_evaluation_cases.yaml`
- autonomy and trigger-boundary checks
- snapshot-backed use and `do_not_use` coverage
- derived evidence reporting in `generated/skill_evaluation_matrix.*`
- review checklists or support artifacts for risk-heavy surfaces

The next evaluation-depth pass should add:
- deeper comparative boundary fixtures for adjacent skills that are easy to confuse
- stronger fixture integrity checks for overlay-shaped bundles
- richer end-to-end walkthrough evidence where canonical/default-reference decisions still need comparative proof
- maintenance-oriented evidence refresh rules so canonical bundles keep their reference quality without widening into bureaucracy

## v0.5 maturity and governance

Add:
- explicit default-reference rationale across adjacent workflow lanes rather than promotion-by-gate-pass
- maintenance reviews for the current canonical cohort so default-reference drift stays visible
- explicit stay-`evaluated` or promote-to-`canonical` decisions for the current candidate-ready cohort
- stronger comparative guidance for neighboring skills such as:
  - `aoa-core-logic-boundary` vs `aoa-port-adapter-refactor` vs `aoa-bounded-context-map`
  - `aoa-dry-run-first` vs `aoa-safe-infra-change` vs `aoa-approval-gate-check`
  - `aoa-adr-write` vs `aoa-source-of-truth-check`
- governance-oriented skill and policy checks
- clearer release and stability signaling for reusable versus experimental surfaces
- a more explicit public promotion path that explains what evidence and review surface is expected at each maturity step
- clearer public product surface for external readers, including stronger entry points and usage-oriented documentation
- derived public-surface views should remain preferred over introducing a second explicit skill metadata layer in the public core
- candidate review records and governance backlog surfaces belong here, not in the runtime layer

## v0.6 project overlays

Continue thin project-shaped overlays now that the public core has two live exemplar packs:
- keep `atm10-*` and `abyss-*` aligned under one repo-state-discovered live-family contract
- treat `atm10` as the original template and `abyss` as the transfer check, but keep both as maintained live families rather than a first/second hierarchy
- treat shared docs, validation, and export expectations across both live families as maintained contract surfaces before adding any third family

Target shape:
- repository-local commands and source-of-truth files
- explicit local authority and approval rules
- local validation commands and evidence paths
- no silent fork of the public core meaning
- `docs/OVERLAY_SPEC.md` and `docs/overlays/atm10/PROJECT_OVERLAY.md` define the repo-local overlay contract for live exemplar packs without turning them into downstream integrations

Recommended sequencing inside this wave:
- keep cross-family parity green for `atm10` plus `abyss`
- move the next repo-wide frontier to `v0.7` packaging and distribution prep
- only then consider any additional live family
- prefer a third family only if it clarifies the overlay contract rather than merely increasing bundle count

## v0.7 packaging and distribution

Explore:
- machine-readable bundle metadata and stronger version pinning
- keep `generated/release_manifest.json` as the packaging-facing contract that pins portable artifact groups, bundle revisions, profile revisions, and changelog-derived release identity
- compatibility and lineage metadata across skills and techniques
- skill graph views for dependency, maturity, policy, install-profile, and artifact-group relationships
- import/export and offline bundle use
- verifiable distribution of reusable public skill bundles
- explicit cross-repo bridge rollout notes for source-owned bridge waves that downstream repos consume from `main`
- keep this wave repo-local for the public core; GitHub releases and tags may continue for bounded repository baselines, while remote registries remain out of scope

Near-term sequence inside this wave:

1. harden the release manifest and packaging verification contract
2. add compatibility/lineage depth on top of that contract
3. add profile-scoped install verification on top of the same release contract
4. add profile-scoped staged bundle handoff on top of the same contract
5. add ZIP handoff and direct archive install or verify on top of the same staged bundle contract
6. add self-contained staged-bundle inspection before install-side verification
7. add one-shot bundle import ergonomics on top of staged bundle or ZIP sources
8. add bundle-local README polish so staged handoffs are more self-explanatory for receivers
9. add a release-facing packaging smoke path over the same staged directory and ZIP transport
10. only then consider any broader export/import ergonomics or archival polish beyond the current import-plus-smoke path

The compatibility/lineage follow-up should stay inside existing packaging surfaces:
- `generated/skill_bundle_index.*` for per-skill profile membership, artifact-group coverage, and technique-lineage detail
- `generated/skill_graph.*` for relationship topology
- `generated/release_manifest.json` only as the release-facing pinning layer over those views

The next packaging frontier after the current import, bundle-README, and packaging-smoke passes is broader export or import ergonomics beyond the current staged directory plus ZIP transport plus preflight inspection plus release smoke, not another packaging-contract bootstrap.

## Long-term direction

- reusable public core
- self-contained runtime skills with controlled build-time refresh from `aoa-techniques`
- clear separation between canonical techniques and executable skills
- evaluation-backed trust in agent workflows
- thin overlays and stronger governance without hidden bureaucracy
- portable reusable skills across projects, teams, and model families
