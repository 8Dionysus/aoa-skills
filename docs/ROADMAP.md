# Roadmap

## Current baseline

Current public foundation:
- coherent docs surface
- 13 public skills across core and risk categories, including the first `canonical` skills, the first `evaluated` risk skills, and the remaining scaffold surface
- honest `techniques.yaml` coverage with pinned source refs across the skill surface
- first examples or checks for every current skill
- local validator for bundle shape, policy, and `SKILL_INDEX.md` coverage
- autonomy and trigger-boundary evaluation checks for seven representative skills
- documented maturity ladder and promotion guidance for future status changes

The next steps should deepen autonomy, evaluation, and governance rather than only increase skill count.

## v0.3 public core hardening

Continue the public core hardening pass with:
- stable schemas for `SKILL.md` front matter, `techniques.yaml`, and `agents/openai.yaml`
- pinned traceability to upstream technique source refs
- build-time refresh helpers for reviewable `SKILL.md` updates
- drift detection when a referenced technique changes materially
- stronger autonomy checks for self-contained runtime use without live remote dependency

## v0.4 evaluation harness

Add:
- prompt fixtures for selected core and risk skills
- trigger-boundary tests
- expected output snapshots for selected skills
- autonomy and verification checks for runtime self-containment
- review checklists and behavior evidence for risk-heavy skills

## v0.5 maturity and governance

Add:
- explicit promotion decisions within the formal maturity ladder
- promotion criteria for moving from `scaffold` toward `evaluated` or `canonical` states
- governance-oriented skill and policy checks
- clearer release and stability signaling for reusable versus experimental surfaces

## v0.6 project overlays

Add first thin project-shaped overlays only after the public core is more stable:
- `atm10-*`
- `abyss-*`

Target shape:
- repository-local commands and source-of-truth files
- explicit local authority and approval rules
- local validation commands and evidence paths
- no silent fork of the public core meaning

## v0.7 packaging and distribution

Explore:
- machine-readable bundle metadata and stronger version pinning
- compatibility and lineage metadata across skills and techniques
- skill graph views for dependency, maturity, and policy relationships
- import/export and offline bundle use
- verifiable distribution of reusable public skill bundles

## Long-term direction

- reusable public core
- self-contained runtime skills with controlled build-time refresh from `aoa-techniques`
- clear separation between canonical techniques and executable skills
- evaluation-backed trust in agent workflows
- thin overlays and stronger governance without hidden bureaucracy
- portable reusable skills across projects, teams, and model families
