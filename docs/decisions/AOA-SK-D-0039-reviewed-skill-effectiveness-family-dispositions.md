# Reviewed Skill-Effectiveness Family Dispositions

- Decision ID: AOA-SK-D-0039
- Status: Accepted
- Date: 2026-07-13
- Owner surface: `mechanics/method-growth/`, `docs/reviews/skill-effectiveness/`,
  and the source-fast validation route

## Index Metadata

- Original date: 2026-07-13
- Surface classes: review/governance, schema/contract, validation guard
- Skill lanes: none
- Mechanic parents: method-growth, audit, antifragility
- Guard families: promotion evidence, privacy boundary, validator topology
- Posture: accepted whole-family reviewed disposition boundary

## Context

The repository already had per-skill maturity, promotion, canonical-candidate,
quality-audit, promotion-pressure, fixture, snapshot, and live-dispatch
surfaces. Those surfaces could answer whether a particular floor passed or
whether review pressure existed. They did not require one reviewed record to
name exactly one lifecycle disposition for every current skill.

That omission mattered for two reasons. First, a family audit could repair a
few visible findings while silently leaving the remaining skills undecided.
Second, session mentions, prompt visibility, selection, full reads, procedure
disposition, verification, and bounded outcome were easy to collapse into one
informal claim even though they describe different stages and have different
failure meanings.

Raw `.aoa` sessions and private Codex traces may help a reviewer find an
episode, but they are not repository-owned proof. Public live-dispatch receipts
are stronger review inputs because their fields are bounded and sanitized, yet
they still remain candidate evidence and may describe a clean individual
measure inside a cohort-level `needs-rerun` receipt.

## Options Considered

- Keep family decisions in prose, issue comments, and session closeout notes.
- Generate dispositions automatically from quality scores, usage counts, or
  promotion pressure.
- Store a reviewed, source-exact family record with explicit evidence-stage
  posture and validate it without granting it proof or promotion authority.

## Decision

Choose the third option.

Method-Growth owns the disposition grammar and JSON Schema. The public review
district owns one current authored family record. The record must cover every
current `SKILL.md` exactly once and choose one of:

- `improve`
- `split`
- `merge`
- `promote`
- `retain`
- `retire`

Each row must preserve source path, scope, and maturity status parity. It must
name the chosen action state, rationale, nearest rejected alternative, next
review condition, and any disposition-specific target.

Episode evidence stays structured into separate prompt-visibility, selection,
load/read, procedure, verification, and outcome fields. Mentions and
co-occurrence remain separate non-authoritative signals. Missing live stages
remain visible even when repository-local evaluation fixtures satisfy the
`evaluated` maturity floor.

The family record is not a status mutation. `promote` requires a later
per-skill status-promotion review and ordinary owner gates. `improve` may point
to a landed repair, but it does not prove runtime adoption. Split, merge, and
retirement require their own bounded follow-through and cannot be inferred
from name similarity or low counts.

The validator must reject:

- missing, extra, or duplicate current skills;
- source path, scope, or status drift;
- decision-count drift;
- absent disposition-specific fields;
- private, absolute, raw-session, URI, or parent-traversal refs;
- episode refs outside the public reviewed `evals/reports/` surface;
- a promotion target that does not advance status, except when the same target
  is already recorded as landed.

## Rationale

This is the smallest durable layer that makes “review the whole AoA skill
family” falsifiable. It preserves human judgment while removing silent family
omission and ambiguous lifecycle language.

Keeping stage evidence explicit prevents a prompt-visible or mentioned skill
from being described as selected, loaded, followed, verified, or outcome
effective without the corresponding observation. Keeping the authority flags
false prevents the review record from replacing `aoa-evals`, runtime owners,
or per-skill promotion governance.

A source-exact current record is intentionally maintained rather than frozen
as a detached historical report. Git history preserves earlier cycles; the
current file must move when source status or a disposition action lands.

## Consequences

- Positive: every current skill receives one inspectable lifecycle decision.
- Positive: family counts and individual rows cannot drift independently.
- Positive: live gaps such as direct selection, full read, or bounded outcome
  remain visible beside repository-local evaluation readiness.
- Positive: raw or host-private evidence cannot leak into the public review
  record through an evidence ref.
- Tradeoff: adding, removing, moving, or reclassifying a skill now requires a
  reviewed update to the family record.
- Tradeoff: a green validator proves record completeness and boundary hygiene,
  not that the chosen judgment is centrally proven.
- Follow-up: land the seven pending `scaffold -> evaluated` status reviews,
  then update the current family record to their landed state without erasing
  remaining live-dispatch gaps.

## Current Applicability

As of 2026-07-13:

- current family: 57 skills;
- dispositions: 4 `improve`, 7 `promote`, 46 `retain`, and zero `split`,
  `merge`, or `retire`;
- the four improvements are landed source repairs from the preceding quality
  pass;
- the seven promotions are pending separate status-owner gates;
- no current evidence justifies collapsing the intentional root/child,
  diagnosis/repair, core/adapter, risk/overlay, or Titan service boundaries;
- direct live selection and bounded outcome remain explicitly unobserved for
  `aoa-eval-design` and `aoa-eval-local-need` even though their repository
  evaluated floors pass;
- superseded by: none.

## Review Log

### 2026-07-13 - Initial whole-family disposition cycle

- Previous assumption: complete quality and promotion readouts plus individual
  review surfaces were enough to show that the whole family had been decided.
- New reality: those surfaces classified pressure and floors but did not
  require exactly one reviewed lifecycle decision per skill.
- Reason: a repeated adaptive loop needs a stable current decision register,
  explicit revisit conditions, and machine-enforced evidence boundaries.
- Source surfaces updated: Method-Growth schema and docs, public review record,
  thin validator, validation topology, and focused tests.
- Validation posture: schema validation, source parity, disposition semantics,
  privacy-negative cases, lane wiring, decision indexes, and affected
  source/export/release gates.

## Boundaries

This decision does not turn raw sessions, mentions, co-occurrence, local
fixtures, live receipts, or the family record into proof authority. It does not
auto-promote a skill, choose a canonical default, accept a project overlay for
its downstream owner, or authorize runtime mutation.

The owning skill bundle remains authoritative for workflow meaning. Per-skill
promotion records remain authoritative for reviewed status transitions.
`aoa-evals` remains the stronger proof owner, and runtime owners remain
authoritative for live admission and behavior.

## Source Surfaces

- `mechanics/method-growth/docs/SKILL_EFFECTIVENESS_FAMILY_REVIEW.md`
- `mechanics/method-growth/schemas/skill_effectiveness_family_review_v1.json`
- `docs/reviews/skill-effectiveness/aoa-family-current.json`
- `scripts/validation/validate_skill_effectiveness_family_review.py`
- `scripts/validation/validators/skill_effectiveness_family_review_surface.py`
- `config/validation_lanes.json`
- `docs/validation/validator_inventory.json`

## Validation

- The focused family-review tests exercise schema validity, 57-skill source
  parity, decision counts, conditional disposition fields, private-ref
  rejection, and preserved eval-child live gaps.
- Validator-topology tests keep the CLI thin, inventoried, bounded, and wired
  through command authority.
- The direct validator must report 57 of 57 current skills with zero issues.
- Decision indexes and the affected source, generated/export, and release
  lanes must remain fresh.
