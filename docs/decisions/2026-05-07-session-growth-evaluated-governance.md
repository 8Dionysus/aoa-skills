# Session Growth Evaluated Governance

Date: 2026-05-07

Status: accepted

## Context

The core session-growth skills were already installed, dispatched, cited in
session history, and covered by trigger and snapshot fixtures, but several of
them still carried `scaffold` status. That made lived use depend on manual
memory and left the promotion-pressure report saying "review soon" without an
explicit governance landing.

The repository's maturity model separates skill-native evidence from technique
bridge evidence. Pending technique lineage may require upstream extraction or
bridge repair, but it should not by itself keep a self-contained skill workflow
at scaffold.

## Decision

Promote the actively used core session-growth family to `evaluated` and record
one governance lane with `stay_evaluated` decisions:

- `aoa-summon`
- `aoa-checkpoint-closeout-bridge`
- `aoa-automation-opportunity-scan`
- `aoa-session-route-forks`
- `aoa-session-self-repair`
- `aoa-quest-harvest`
- `aoa-session-donor-harvest`
- `aoa-session-self-diagnose`
- `aoa-session-progression-lift`
- `aoa-commit-growth-seam`

The chosen path is evaluated maturity, not canonical promotion. Canonical or
default-reference decisions remain separate comparative reviews.

## Consequences

- Lived-use pressure now lands in explicit status-promotion records instead of
  staying as scaffold backlog.
- `generated/skill_promotion_pressure.*` no longer has `blockers_first`
  entries for this wave.
- `aoa-summon` keeps pending technique lineage visible as bridge follow-up
  while still being evaluated as a self-contained workflow.
- Titan project overlays keep scaffold status; this wave only gives them
  autonomy evidence and preserves their pending-lineage signal for later owner
  adoption review.

## Verification

Verified with:

```bash
python scripts/release_check.py
python -m pytest -q tests
python scripts/audit_skill_quality.py --repo-root . --write-json generated/skill_quality_audit.json --write-markdown generated/skill_quality_audit.md --format json
python scripts/report_skill_promotion_pressure.py --repo-root . --workspace-root /srv/AbyssOS --write-json generated/skill_promotion_pressure.json --write-markdown generated/skill_promotion_pressure.md --format json
```
