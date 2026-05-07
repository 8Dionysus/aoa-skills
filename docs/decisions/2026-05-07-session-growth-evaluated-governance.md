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
- `aoa-summon` originally kept pending technique lineage visible as bridge
  follow-up while still being evaluated as a self-contained workflow; the
  follow-up is now closed by grounding summon in published bridge techniques.
- The route-forks/summon boundary is explicit: fork cards may expose a selected
  child-route candidate, but only `aoa-summon` may gate one anchored child
  route, and cross-boundary child work must name receipt or acceptance posture
  before parent continuation.
- Donor harvest and checkpoint closeout now make lower-authority hints
  explicit: checkpoint notes, closeout handoffs, and generated reports can
  focus attention, but reviewed evidence must accept or reject them before
  candidate refs or final stage verdicts appear.
- The checkpoint-closeout bridge keeps donor -> progression -> quest as a fixed
  dependency order, while allowing an evidence-linked stage status of
  `skipped`, `deferred`, or `stopped` instead of forcing a positive verdict.
- Progression lift now records baseline posture plus per-axis evidence posture
  so checkpoint or generated hints can stay useful without becoming fake
  comparative growth claims.
- Quest harvest now requires one isolated repeated reviewed unit and keeps the
  verdict smaller than downstream authoring or owner acceptance; repeat
  evidence posture stays visible before promotion target selection.
- Self-diagnose now records evidence posture for symptoms and probable causes
  so checkpoint, closeout, generated, stale, or contested hints cannot become
  settled root cause claims.
- Self-repair now records execution posture so prepared, executed, and verified
  repair states remain distinct.
- Automation opportunity scan now records automation-mode posture so
  `seed_ready` cannot masquerade as unattended scheduler or mutation authority.
- Commit growth seam now records commit authorization posture so a ready diff
  cannot masquerade as permission to commit, push, or publish.
- The full branch rollout profile is `repo-session-growth`: it carries the
  hard-gated kernel plus the explicit `aoa-commit-growth-seam` and
  `aoa-summon` companions without weakening the kernel receipt contract or
  pulling in engineering, risk, or project overlays.
- Growth-cycle example families use semantic names such as
  `reviewed-donor-harvest`, `derived-visibility-handoff`, and
  `kernel-maturity` instead of pass labels.
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
