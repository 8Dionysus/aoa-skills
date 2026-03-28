# Roadmap

## Current baseline

Current public foundation:
- coherent docs surface
- 19 public skills across core, risk, and live project-overlay categories
- live governance counts kept in `generated/public_surface.md` and `generated/governance_backlog.md` rather than duplicated in source docs
- honest `techniques.yaml` coverage with pinned source refs across the skill surface
- first examples or checks for every current skill
- local validator for bundle shape, policy, and `SKILL_INDEX.md` coverage
- autonomy and trigger-boundary evaluation checks across the full current skill surface
- documented maturity ladder and promotion guidance for future status changes
- derived public-surface signaling in `docs/PUBLIC_SURFACE.md` and `generated/public_surface.*`
- repo-level baseline release identity in `CHANGELOG.md`, `docs/RELEASING.md`, tags, and GitHub release notes
- bounded release validation in `scripts/release_check.py`

Already-shipped repo-owned support layers now include:
- wave-3 Codex-facing portable export, install-profile, and local-adapter surfaces
- wave-4 raw runtime seam
- wave-5 limited skill-handoff bridge only; scenario canon lives in `aoa-playbooks`
- wave-6 governed runtime guardrails
- wave-7 description-first activation contract and soft conformance lane
- wave-8 deterministic support-resource bundles for three high-risk skills
- wave-9 tiny-router compression bridge for downstream routing

The next steps should use that derived governance layer to keep core governance decisions honest, keep live overlay families aligned under one contract, and push packaging prep rather than only increase skill count.
Overlay preparation and packaging remain intentionally repo-local and thin: they should surface contracts and export primitives without introducing live downstream integrations or registries.

## Near-term sequence

The nearest waves should now be read in this order:

1. `v0.5` maturity and governance consolidation
2. `v0.6` project-overlay maturity
3. `v0.7` packaging and distribution prep

Repo-level semver releases such as `v0.1.0` describe bounded public baselines.
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
- compatibility and lineage metadata across skills and techniques
- skill graph views for dependency, maturity, and policy relationships
- import/export and offline bundle use
- verifiable distribution of reusable public skill bundles
- explicit cross-repo bridge rollout notes for source-owned bridge waves that downstream repos consume from `main`
- keep this wave repo-local for the public core; GitHub releases and tags may continue for bounded repository baselines, while remote registries remain out of scope

## Long-term direction

- reusable public core
- self-contained runtime skills with controlled build-time refresh from `aoa-techniques`
- clear separation between canonical techniques and executable skills
- evaluation-backed trust in agent workflows
- thin overlays and stronger governance without hidden bureaucracy
- portable reusable skills across projects, teams, and model families
