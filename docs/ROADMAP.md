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

Add:
- prompt fixtures for selected core and risk skills
- trigger-boundary tests
- expected output snapshots for selected skills
- autonomy and verification checks for runtime self-containment
- explicit evaluation-coverage enforcement for `evaluated` and `canonical` skills
- review checklists and behavior evidence for risk-heavy skills
- end-to-end walkthroughs that show how selected skills look in real use
- deeper boundary evidence and fixture integrity checks are preferred over adding more raw count coverage

## v0.5 maturity and governance

Add:
- explicit promotion decisions within the formal maturity ladder
- promotion criteria for moving from `scaffold` toward `evaluated` or `canonical` states
- governance-oriented skill and policy checks
- clearer release and stability signaling for reusable versus experimental surfaces
- a more explicit public promotion path that explains what evidence and review surface is expected at each maturity step
- clearer public product surface for external readers, including stronger entry points and usage-oriented documentation
- derived public-surface views should remain preferred over introducing a second explicit skill metadata layer in the public core
- candidate review records and governance backlog surfaces belong here, not in the runtime layer

## v0.6 project overlays

Continue thin project-shaped overlays now that the public core has a first live exemplar pack:
- deepen `atm10-*` from initial scaffold overlays into a clearer project-family surface
- add first `abyss-*` exemplar overlays after the `atm10` pattern is stable

Target shape:
- repository-local commands and source-of-truth files
- explicit local authority and approval rules
- local validation commands and evidence paths
- no silent fork of the public core meaning
- `docs/OVERLAY_SPEC.md` and `docs/overlays/atm10/PROJECT_OVERLAY.md` define the repo-local overlay contract for live exemplar packs without turning them into downstream integrations

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
