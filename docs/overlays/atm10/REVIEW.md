# atm10 overlay family review

## Current status

- overlay family: `atm10`
- family posture: live exemplar overlay pack
- evaluated skills: `atm10-change-protocol`, `atm10-source-of-truth-check`
- base skill canon: `aoa-skills`
- upstream technique canon: `aoa-techniques`
- family review surface: `docs/overlays/atm10/PROJECT_OVERLAY.md`, `docs/overlays/atm10/REVIEW.md`, `skills/atm10-change-protocol/checks/review.md`, `skills/atm10-source-of-truth-check/checks/review.md`

## Evidence reviewed

- `docs/OVERLAY_SPEC.md`
- `docs/overlays/atm10/PROJECT_OVERLAY.md`
- `skills/atm10-change-protocol/SKILL.md`
- `skills/atm10-source-of-truth-check/SKILL.md`
- bundle-local review checklists under `skills/atm10-*/checks/review.md`
- overlay evaluation fixtures in `tests/fixtures/skill_evaluation_cases.yaml`

## Findings

- the overlay remains thin, repo-local, and public-safe
- the two atm10 bundles stay bounded, explicit-preferred, and now clear the evaluated floor through bundle-local review evidence plus existing overlay evaluation fixtures
- the family entrypoint names repo-relative paths, commands, and review posture
- bundle-local review checklists give a human review surface without adding hidden authority
- `reviewable` is the current target maturity for a live project-overlay exemplar family in this repo
- family maturity belongs in `generated/overlay_readiness.*`, while per-skill maintenance belongs in `generated/governance_backlog.*`
- if downstream consumers need federation-style closure, `generated/governance_backlog.*` may reconcile these ATM10 skills as `project_overlay_federation_ready` without creating a governance lane

## Gaps and blockers

- no governance lane is expected for this project-overlay family and should not be read as a missing canonical decision
- no downstream integration is implied
- no live remote dependency is needed
- the family should stay narrow until additional `atm10-*` bundles are intentionally added

## Recommendation

Keep `atm10` as a reviewable thin overlay exemplar and stable template for future families, not as a playbook, project doctrine, or hidden canonical-promotion track.
