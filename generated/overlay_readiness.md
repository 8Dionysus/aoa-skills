# Overlay readiness

This derived file summarizes live overlay-family maturity and project-skill readiness
for the thin overlay layer in `aoa-skills`.
`reviewable` is the current mature exemplar target for a live project-overlay family in this repo.
Use this surface for family maturity and `generated/governance_backlog.md` for per-skill maintenance readout.

## Summary

- live overlay families: 3
- reviewable families: 2
- project overlay skills: 20
- project skills with review checklists: 20
- eval-ready project skills: 5

## Families

| family | skills | listed parity | family review | bundle review checks | eval-ready skills | repo-relative evidence | boundary evidence | readiness |
|---|---:|---|---|---:|---:|---|---|---|
| abyss | 3 | true | docs/overlays/abyss/REVIEW.md | 3 | 3 | true | true | reviewable |
| atm10 | 2 | true | docs/overlays/atm10/REVIEW.md | 2 | 2 | true | true | reviewable |
| titan | 15 | true | docs/overlays/titan/REVIEW.md | 15 | 0 | true | true | baseline |

## Project skills

| name | family | status | review checklist | runtime examples | adaptation points | policy file | eval ready | blockers |
|---|---|---|---|---:|---|---|---|---|
| abyss-safe-infra-change | abyss | evaluated | skills/abyss-safe-infra-change/checks/review.md | 1 | true | true | true | - |
| abyss-sanitized-share | abyss | evaluated | skills/abyss-sanitized-share/checks/review.md | 1 | true | true | true | - |
| abyss-self-diagnostic-spine | abyss | scaffold | skills/abyss-self-diagnostic-spine/checks/review.md | 1 | true | true | true | - |
| atm10-change-protocol | atm10 | evaluated | skills/atm10-change-protocol/checks/review.md | 1 | true | true | true | - |
| atm10-source-of-truth-check | atm10 | evaluated | skills/atm10-source-of-truth-check/checks/review.md | 1 | true | true | true | - |
| titan-approval-ledger | titan | scaffold | skills/titan-approval-ledger/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |
| titan-approval-loom | titan | scaffold | skills/titan-approval-loom/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |
| titan-appserver-bridge | titan | scaffold | skills/titan-appserver-bridge/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |
| titan-appserver-plan | titan | scaffold | skills/titan-appserver-plan/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |
| titan-closeout | titan | scaffold | skills/titan-closeout/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |
| titan-console | titan | scaffold | skills/titan-console/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |
| titan-event-replay | titan | scaffold | skills/titan-event-replay/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |
| titan-memory-loom | titan | scaffold | skills/titan-memory-loom/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |
| titan-memory-prune | titan | scaffold | skills/titan-memory-prune/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |
| titan-mutation-gate | titan | scaffold | skills/titan-mutation-gate/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |
| titan-recall | titan | scaffold | skills/titan-recall/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |
| titan-receipt | titan | scaffold | skills/titan-receipt/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |
| titan-runtime-gate | titan | scaffold | skills/titan-runtime-gate/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |
| titan-summon | titan | scaffold | skills/titan-summon/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |
| titan-thread-turn-binding | titan | scaffold | skills/titan-thread-turn-binding/checks/review.md | 1 | true | true | false | missing_use_snapshot, missing_do_not_use_snapshot |

