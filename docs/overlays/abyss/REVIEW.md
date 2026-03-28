# abyss overlay family review

## Current status

- overlay family: `abyss`
- family posture: live exemplar overlay pack
- evaluated skills: `abyss-safe-infra-change`, `abyss-sanitized-share`
- base skill canon: `aoa-skills`
- upstream technique canon: `aoa-techniques`
- family review surface: `docs/overlays/abyss/PROJECT_OVERLAY.md`, `docs/overlays/abyss/REVIEW.md`, `skills/abyss-safe-infra-change/checks/review.md`, `skills/abyss-sanitized-share/checks/review.md`

## Evidence reviewed

- `docs/OVERLAY_SPEC.md`
- `docs/overlays/abyss/PROJECT_OVERLAY.md`
- `skills/abyss-safe-infra-change/SKILL.md`
- `skills/abyss-sanitized-share/SKILL.md`
- bundle-local review checklists under `skills/abyss-*/checks/review.md`
- overlay evaluation fixtures in `tests/fixtures/skill_evaluation_cases.yaml`

## Findings

- the overlay remains thin, repo-local, and public-safe
- the two abyss bundles stay bounded, explicit-only, and clear the evaluated floor through bundle-local review evidence plus overlay evaluation fixtures
- the family entrypoint names repo-relative commands, sharing surfaces, and local review posture without inventing a new workflow
- bundle-local review checklists give a human review surface without adding hidden authority
- `reviewable` is the current target maturity for a live project-overlay exemplar family in this repo
- family maturity belongs in `generated/overlay_readiness.*`, while per-skill maintenance belongs in `generated/governance_backlog.*`

## Gaps and blockers

- no governance lane is expected for this project-overlay family and should not be read as a missing canonical decision
- no downstream integration is implied
- no live remote dependency is needed
- the family should stay narrow until additional `abyss-*` bundles are intentionally added

## Recommendation

Keep `abyss` as a reviewable thin overlay exemplar and second-family template check, not as a playbook, project doctrine, or hidden canonical-promotion track.
