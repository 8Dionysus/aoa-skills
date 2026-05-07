# Promotion pressure

This document defines the local `aoa-skills` readout that connects repeated
skill use to the formal promotion path.

Runtime use, workspace installation, dispatch selection, hook prompts, and
session mentions are evidence. They do not promote a skill by themselves.
They should create visible review pressure so heavily used non-canonical skills
do not depend on manual memory.

Technique bridge findings are interpreted beside this evidence. A pending or
drifted bridge may require refresh or extraction work, but it is not treated as
the whole measure of whether the skill workflow itself is mature.

## Source surfaces

The promotion-pressure report reads:

- `generated/public_surface.json` for status, default-reference readiness, and
  governance decisions
- `generated/governance_backlog.json` for readiness reconciliation
- `generated/skill_quality_audit.json` for body, lineage, evaluation, and
  technique-drift findings
- `generated/workspace_skill_adoption_audit.json` for installed repo surfaces
- `generated/skill_reality_trials.json` for live dispatch trials
- local Codex session logs, hook prompts, and `aoa-sdk` skill-dispatch reports
  when those local evidence roots exist

The source skill bundle remains `skills/**/SKILL.md`.
The report is evidence and queue pressure, not canonical authority.

## Readout

Generate the local readout with:

```bash
python scripts/report_skill_promotion_pressure.py \
  --repo-root . \
  --workspace-root /srv/AbyssOS \
  --write-json generated/skill_promotion_pressure.json \
  --write-markdown generated/skill_promotion_pressure.md \
  --format markdown
```

For a fast deterministic check without local transcript, hook, or dispatch
scans, use:

```bash
python scripts/report_skill_promotion_pressure.py \
  --repo-root . \
  --workspace-root /srv/AbyssOS \
  --skip-session-scan \
  --skip-hooks-scan \
  --skip-dispatch-scan \
  --format json
```

## Pressure classes

- `canonical_monitor`: already canonical; keep drift and maintenance visible.
- `canonical_review_now`: machine gates and usage pressure justify canonical
  review.
- `promotion_review_now`: repeated use should open the next status or promotion
  review before canonical review.
- `revisit_stay_evaluated`: the skill was kept evaluated, but live use now
  justifies revisiting that decision.
- `blockers_first`: live use exists, but hard skill-native blockers such as
  missing required sections, missing trigger evidence, missing snapshots, or
  unresolved placeholders must be cleared before promotion review.
- `overlay_adoption_review`: a project overlay is used enough to require owner
  adoption review, not core canonical promotion.
- `overlay_watch`: project overlay evidence remains weak or blocked.
- `watch`: no repeated usage pressure yet.

## Rule

Repeated use is not a shortcut around the maturity ladder.
It is the signal that the ladder must be applied soon.

When `generated/skill_promotion_pressure.md` lists a non-canonical skill under
review pressure, the next honest move is a bounded promotion review or blocker
repair. When it lists `blockers_first`, do not relabel the skill; clear the
named blockers and rerun quality, evaluation, and promotion-pressure reports.
When it lists technique bridge findings without hard skill-native blockers,
keep the promotion review open and route bridge refresh or technique extraction
as a parallel owner move.
