# Overlay readiness

This derived file summarizes live overlay-family maturity and project-skill readiness
for the thin overlay layer in `aoa-skills`.
`reviewable` is the current mature exemplar target for a live project-overlay family in this repo.
Use this surface for family maturity and `generated/governance_backlog.md` for per-skill maintenance readout.

## Summary

- live overlay families: 2
- reviewable families: 2
- project overlay skills: 4
- project skills with review checklists: 4
- eval-ready project skills: 4

## Families

| family | skills | listed parity | family review | bundle review checks | eval-ready skills | repo-relative evidence | boundary evidence | readiness |
|---|---:|---|---|---:|---:|---|---|---|
| abyss | 2 | true | docs/overlays/abyss/REVIEW.md | 2 | 2 | true | true | reviewable |
| atm10 | 2 | true | docs/overlays/atm10/REVIEW.md | 2 | 2 | true | true | reviewable |

## Project skills

| name | family | status | review checklist | runtime examples | adaptation points | policy file | eval ready | blockers |
|---|---|---|---|---:|---|---|---|---|
| abyss-safe-infra-change | abyss | evaluated | skills/abyss-safe-infra-change/checks/review.md | 1 | true | true | true | - |
| abyss-sanitized-share | abyss | evaluated | skills/abyss-sanitized-share/checks/review.md | 1 | true | true | true | - |
| atm10-change-protocol | atm10 | evaluated | skills/atm10-change-protocol/checks/review.md | 1 | true | true | true | - |
| atm10-source-of-truth-check | atm10 | evaluated | skills/atm10-source-of-truth-check/checks/review.md | 1 | true | true | true | - |

