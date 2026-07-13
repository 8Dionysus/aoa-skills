# Mechanics Method-Growth Adoption Lifecycle

- Decision ID: AOA-SK-D-0008

## Index Metadata

- Original date: 2026-05-06
- Surface classes: mechanic package, review/governance
- Skill lanes: none
- Mechanic parents: method-growth
- Guard families: skill maturity, source topology
- Posture: accepted adoption lifecycle

Date: 2026-05-06

Status: accepted

## Context

Five v0.7 downstream adoption docs remained flat in `docs/`: compatibility,
receipts, regression, retirement, and pattern adoption. Direct reading showed
they share one adoption lifecycle law: adoption must be explicit, local owner
consent is required, and durable behavior change needs evidence, rollback, and
retention.

The old docs were repetitive and wave-shaped. Copying them into active parts
would preserve legacy language rather than making the route clearer.

`mechanics/method-growth/` already owns candidate lineage, owner-status
landing, and governed followthrough. Adoption lifecycle is the next local
method-growth slice when a pattern or skill-shaped object moves toward durable
uptake.

## Decision

Keep adoption lifecycle inside `mechanics/method-growth/`, but preserve the
v0.7 source docs as raw package-local legacy:

- `docs/SKILL_ADOPTION_COMPATIBILITY.md` -> `mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_COMPATIBILITY.md`
- `docs/SKILL_ADOPTION_RECEIPTS.md` -> `mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_RECEIPTS.md`
- `docs/SKILL_ADOPTION_REGRESSION.md` -> `mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_REGRESSION.md`
- `docs/SKILL_ADOPTION_RETIREMENT.md` -> `mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_RETIREMENT.md`
- `docs/SKILL_PATTERN_ADOPTION.md` -> `mechanics/method-growth/legacy/adoption-wave/raw/SKILL_PATTERN_ADOPTION.md`

Distill active behavior into four parts:

- `parts/adoption-boundary/`
- `parts/adoption-evidence-receipts/`
- `parts/retention-regression-retirement/`
- `parts/pattern-adoption-handoff/`

Keep `mechanics/experience/docs/GOVERNANCE_SKILL_ADOPTION.md` in place because it belongs to the
later v0.8 experience/polis-governance contour, not this v0.7 adoption
lifecycle slice.

## Consequences

- Flat `docs/` no longer owns the v0.7 adoption lifecycle route.
- Old adoption wave language stays auditable without becoming the active route.
- Method-growth now carries adoption posture after candidate lineage without
  claiming downstream owner consent.
- Governance adoption pressure remains separate for a later experience,
  governance, or audit pass.

## Verification

Verification covered the experience lifecycle contracts, mechanics routes and
topology, and nested agent cards.
