# Method-Growth Provenance

This bridge keeps the current active route tied to the source surfaces that
landed it. Use it for auditing, not as the main entry route.

## Moved Active Docs

The first method-growth package landing moved these active docs out of flat
`docs/` and into package-local active docs:

| Former path | Current path | Active route |
|---|---|---|
| `docs/CANDIDATE_LINEAGE_CONTRACT.md` | `mechanics/method-growth/docs/CANDIDATE_LINEAGE_CONTRACT.md` | [Candidate Lineage](parts/candidate-lineage/README.md) |
| `docs/CANDIDATE_REF_REFINERY.md` | `mechanics/method-growth/docs/CANDIDATE_REF_REFINERY.md` | [Candidate Lineage](parts/candidate-lineage/README.md) |
| `docs/OWNER_STATUS_SURFACES.md` | `mechanics/method-growth/docs/OWNER_STATUS_SURFACES.md` | [Owner Status Landing](parts/owner-status-landing/README.md) |
| `docs/GOVERNED_FOLLOWTHROUGH.md` | `mechanics/method-growth/docs/GOVERNED_FOLLOWTHROUGH.md` | [Governed Followthrough](parts/governed-followthrough/README.md) |

These docs were not archived as raw legacy because they remain active contract
surfaces. The move changes their route, not their authority level.

## Canonical Skill Companions

Canonical skill meaning remains in:

- `skills/aoa-session-donor-harvest/SKILL.md`
- `skills/aoa-session-donor-harvest/references/harvest-packet-receipt-schema.yaml`
- `skills/aoa-session-donor-harvest/references/candidate-lineage-receipt-schema.yaml`

This package may point to those surfaces, but it must not copy their skill
bundle meaning into mechanics.

## Preserved Adoption Sources

The adoption lifecycle landing preserved the v0.7 downstream adoption
source docs as raw package-local lineage:

| Former path | Preserved raw path | Active route |
|---|---|---|
| `docs/SKILL_ADOPTION_COMPATIBILITY.md` | `mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_COMPATIBILITY.md` | [Adoption Boundary](parts/adoption-boundary/README.md) |
| `docs/SKILL_ADOPTION_RECEIPTS.md` | `mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_RECEIPTS.md` | [Adoption Evidence Receipts](parts/adoption-evidence-receipts/README.md) |
| `docs/SKILL_ADOPTION_REGRESSION.md` | `mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_REGRESSION.md` | [Retention, Regression, Retirement](parts/retention-regression-retirement/README.md) |
| `docs/SKILL_ADOPTION_RETIREMENT.md` | `mechanics/method-growth/legacy/adoption-wave/raw/SKILL_ADOPTION_RETIREMENT.md` | [Retention, Regression, Retirement](parts/retention-regression-retirement/README.md) |
| `docs/SKILL_PATTERN_ADOPTION.md` | `mechanics/method-growth/legacy/adoption-wave/raw/SKILL_PATTERN_ADOPTION.md` | [Pattern Adoption Handoff](parts/pattern-adoption-handoff/README.md) |

The active parts distill the old source language. The raw docs are audit lineage,
not current entrypoints.

## Schema And Example Companions

The first owner-status and followthrough route is checked by:

- `schemas/reviewed_owner_landing_bundle.schema.json`
- `schemas/route_followthrough_decision.schema.json`
- `examples/reviewed_owner_landing_bundle.example.json`
- `examples/route_followthrough_decision.example.json`
- `examples/session_growth_artifacts/candidate_lineage_receipt.alpha.json`
- `schemas/skill_adoption_compatibility_report_v1.json`
- `schemas/skill_adoption_owner_decision_v1.json`
- `schemas/skill_adoption_receipt_v1.json`
- `schemas/skill_adoption_regression_case_v1.json`
- `schemas/skill_adoption_retirement_v1.json`
- `schemas/skill_pattern_adoption_patch_v1.json`

## Neighbor Routes

- `mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md` owns lower-authority
  checkpoint carry before harvest.
- `mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md` owns later
  session-growth packet and receipt examples after `candidate_ref` already
  exists.
- `QUESTBOOK.md` and `mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md` own durable
  obligations and quest-harvest posture.
- `docs/GOVERNANCE_SKILL_ADOPTION.md` remains a governance and experience
  pressure surface. It was not part of the v0.7 adoption lifecycle landing.
- Experience and release-support own operator-facing installation, consent, or
  release posture when adoption leaves skill-layer method-growth.

## Stop-Line

The method-growth package preserves lineage, decision, and adoption movement.
It does not prove, seed, accept, schedule, adopt, or promote the candidate by
itself.
