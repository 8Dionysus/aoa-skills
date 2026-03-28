# abyss overlay

## Purpose

This live exemplar overlay pack adapts a small `abyss-*` family of risk-shaped skills to repo-relative paths,
commands, sharing surfaces, and local authority notes without pretending to be a downstream integration.
It does not change the base skill boundary.

## Authority

- overlay family: `abyss`
- canonical overlay doc: `docs/overlays/abyss/PROJECT_OVERLAY.md`
- base skill canon: `aoa-skills`
- upstream technique canon: `aoa-techniques`
- maturity posture: `generated/overlay_readiness.md` is the family-level maturity surface; `generated/governance_backlog.md` may expose `project_overlay_federation_ready` as a downstream bridge signal, but no governance lane is expected for these project overlays
- explicit approval rules: downstream maintainers keep command execution, sharing thresholds, risk acceptance, and final local authority explicit

## Local surface

- source-of-truth files: repo-relative operational and reporting docs such as `README.md`, `docs/ARCHITECTURE.md`, and `docs/[canonical-guide].md`
- commands: repo-relative checks such as `python scripts/validate_skills.py`, `python scripts/build_catalog.py --check`, or another local validator chosen downstream
- rollback path: revert the bounded local change or withhold the raw shareable material and re-run the smallest relevant local check
- verification path: use the smallest repo-relative check that matches the touched operational or sharing surface
- family review doc: `docs/overlays/abyss/REVIEW.md`
- maintenance readout: use `generated/overlay_readiness.md` for family maturity and `generated/governance_backlog.md` for per-skill maintenance
- bundle-local review checklists: `skills/abyss-safe-infra-change/checks/review.md`, `skills/abyss-sanitized-share/checks/review.md`

## Overlayed skills

- `abyss-safe-infra-change` - adapts `aoa-safe-infra-change` to repo-relative operational surfaces, explicit local authority notes, and local validation commands
- `abyss-sanitized-share` - adapts `aoa-sanitized-share` to repo-relative sharing surfaces, explicit local thresholds, and local review posture

## Risks and anti-patterns

- do not widen the overlay into project doctrine or a scenario bundle
- do not hide downstream authority or sharing thresholds inside local convenience prose
- do not replace the base skills with family-specific rules that belong upstream or downstream
- do not present this exemplar pack as a live downstream integration
- do not treat the missing governance lane for `abyss-*` as a hidden canonical-promotion gap

## Validation

- confirm the overlay does not change the base skill boundary
- confirm every listed overlay skill has a matching `skills/abyss-*` bundle
- confirm the family review doc and bundle-local review checklists stay aligned
- confirm repo-relative paths, commands, and sharing surfaces stay public-safe and reviewable
- confirm downstream authority remains explicit
- confirm the family stays reviewable as a repo-local exemplar even when downstream consumers read `project_overlay_federation_ready` without a governance lane
