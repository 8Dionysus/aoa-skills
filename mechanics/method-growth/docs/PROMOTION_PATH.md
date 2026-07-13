# Promotion path

This document defines the public repository convention for moving a skill through the maturity ladder.

Status changes are governance changes, not cosmetic relabeling.
Machine-checkable floors make promotion safer, but they do not replace human review and explicit promotion decisions.

Repeated live use is tracked separately in `PROMOTION_PRESSURE.md` and
`generated/skill_promotion_pressure.md`. That evidence does not promote a skill
automatically. It tells reviewers when a non-canonical skill is used enough that
the next status or canonical review should stop being manual memory.

Technique bridge evidence is adjacent to this path, not identical with it.
Skills can be composed from techniques, and stable skill workflows can be
decomposed into technique extraction requests. Pending or drifted bridge state
routes bridge repair or upstream technique work; it does not by itself settle
whether the skill execution object is mature.

## `scaffold -> linked`

- machine-checkable floor:
  the skill keeps an honest bridge manifest when a technique relationship is
  declared; pending techniques may remain honest `AOA-T-PENDING-*` entries with
  `path: TBD` and `source_ref: TBD`
- required public review surface:
  no dedicated review record is required in this first step; the change may land as traceability hardening if the PR makes the bridge update explicit
- still requires human judgment:
  whether the linked manifest still reflects the real runtime meaning and whether the bridge metadata is honest enough to become the next baseline

## `linked -> reviewed`

- machine-checkable floor:
  review evidence exists either as `checks/review.md` in the bundle or as a public review record
- required public review surface:
  either in-bundle `checks/review.md` or `docs/reviews/status-promotions/<skill-name>.md`
- still requires human judgment:
  whether the review evidence is substantive, whether the skill boundary is coherent, and whether remaining gaps are acceptable for the target use

## `reviewed -> evaluated`

- machine-checkable floor:
  the skill passes the lower floors and has evaluation coverage with one autonomy check, at least one `use` trigger case, at least one `do_not_use` trigger case, and snapshot-backed matrix coverage that can be read in `mechanics/audit/docs/EVALUATION_PATH.md`
- required public review surface:
  `docs/reviews/status-promotions/<skill-name>.md`
- still requires human judgment:
  whether the evidence demonstrates real behavioral trust rather than nominal fixture coverage, and whether the runtime `SKILL.md` meaning changed during the reviewed/evaluated work

Read the current derived evidence layer with:

- `generated/skill_evaluation_matrix.md`
- the readout owned by `scripts/reports/report_skill_evaluation.py`

## `evaluated -> canonical`

- machine-checkable floor:
  the skill passes the lower floors, remains self-contained, separates
  skill-native evidence from technique bridge findings, and retains full
  evaluation coverage
- required public review surface:
  `docs/reviews/canonical-candidates/<skill-name>.md`
- still requires human judgment:
  whether the skill should become the default public reference for its workflow class, whether alternatives remain materially better, and what blocks the next maintenance review after promotion

## Review record expectations

Public review records should say:

- whether the current machine-checkable floors pass
- whether the runtime `SKILL.md` meaning changed or only metadata/evidence changed
- whether any technique bridge finding is a blocker for a bridge-completeness
  claim or only a follow-up route to `aoa-techniques`
- what still blocks the next status step after the current decision
- where to read the evaluation matrix and snapshot-backed coverage before making the promotion claim

Use:

- `templates/STATUS_PROMOTION_REVIEW.template.md` for non-canonical promotion work
- `templates/CANDIDATE_REVIEW.template.md` for canonical-candidate and canonical-promotion work

Before deciding that a heavily used skill should remain non-canonical, read:

- `generated/skill_promotion_pressure.md`
- `generated/skill_quality_audit.md`
- `generated/governance_backlog.md`
