# Roadmap

## Current baseline

Current public foundation:
- coherent docs surface
- 16 public skills across core, risk, and first live project-overlay categories
- live governance counts kept in `generated/public_surface.md` and `generated/governance_backlog.md` rather than duplicated in source docs
- honest `techniques.yaml` coverage with pinned source refs across the skill surface
- first examples or checks for every current skill
- local validator for bundle shape, policy, and `SKILL_INDEX.md` coverage
- autonomy and trigger-boundary evaluation checks across the full current skill surface
- documented maturity ladder and promotion guidance for future status changes
- derived public-surface signaling in `docs/PUBLIC_SURFACE.md` and `generated/public_surface.*`

The next steps should use that derived governance layer to drive candidate review and promotion decisions, overlay maturity, stronger public product-surface clarity, and packaging prep rather than only increase skill count.
Overlay preparation and packaging remain intentionally repo-local and thin: they should surface contracts and export primitives without introducing live downstream integrations, releases, or registries.

## Near-term sequence

The nearest waves should now be read in this order:

1. `v0.5` maturity and governance consolidation
2. `v0.6` project-overlay maturity
3. `v0.7` packaging and distribution prep

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

Continue thin project-shaped overlays now that the public core has a first live exemplar pack:
- deepen `atm10-*` from initial scaffold overlays into a clearer project-family surface with explicit maturity goals
- move `atm10-*` from "exists and evaluates" toward reviewable overlay-family guidance that can justify status advancement
- add first `abyss-*` exemplar overlays after the `atm10` pattern is stable

Target shape:
- repository-local commands and source-of-truth files
- explicit local authority and approval rules
- local validation commands and evidence paths
- no silent fork of the public core meaning
- `docs/OVERLAY_SPEC.md` and `docs/overlays/atm10/PROJECT_OVERLAY.md` define the repo-local overlay contract for live exemplar packs without turning them into downstream integrations

Recommended sequencing inside this wave:
- finish the `atm10` maturity pattern first
- only then add the first `abyss-*` exemplar family
- prefer a second family only if it clarifies the overlay contract rather than merely increasing bundle count

## v0.7 packaging and distribution

Explore:
- machine-readable bundle metadata and stronger version pinning
- compatibility and lineage metadata across skills and techniques
- skill graph views for dependency, maturity, and policy relationships
- import/export and offline bundle use
- verifiable distribution of reusable public skill bundles
- keep this wave repo-local and read-only for the public core; no GitHub releases, tags, or remote registries are implied

## Long-term direction

- reusable public core
- self-contained runtime skills with controlled build-time refresh from `aoa-techniques`
- clear separation between canonical techniques and executable skills
- evaluation-backed trust in agent workflows
- thin overlays and stronger governance without hidden bureaucracy
- portable reusable skills across projects, teams, and model families
