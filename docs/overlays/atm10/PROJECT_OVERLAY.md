# atm10 overlay

## Purpose

This live exemplar overlay pack adapts a small `atm10-*` family of skills to repo-relative paths,
commands, and local approval notes without pretending to be a downstream integration.
It does not change the base skill boundary.

## Authority

- overlay family: `atm10`
- canonical overlay doc: `docs/overlays/atm10/PROJECT_OVERLAY.md`
- base skill canon: `aoa-skills`
- upstream technique canon: `aoa-techniques`
- maturity posture: `generated/overlay_readiness.md` is the family-level maturity surface; `generated/governance_backlog.md` may expose `project_overlay_federation_ready` as a downstream bridge signal, but no governance lane is expected for these project overlays
- explicit approval rules: downstream maintainers keep command execution, risk acceptance, and final local authority explicit

## Local surface

- source-of-truth files: repo-relative docs such as `README.md`, `docs/ARCHITECTURE.md`, and `docs/[canonical-guide].md`
- commands: repo-relative checks such as `python -m pytest`, `python scripts/[local-check].py`, or another local validator chosen downstream
- rollback path: revert the bounded local change and re-run the smallest relevant local check
- verification path: use the smallest repo-relative check that matches the touched surface
- family review doc: `docs/overlays/atm10/REVIEW.md`
- maintenance readout: use `generated/overlay_readiness.md` for family maturity and `generated/governance_backlog.md` for per-skill maintenance
- bundle-local review checklists: `skills/atm10-change-protocol/checks/review.md`, `skills/atm10-source-of-truth-check/checks/review.md`

## Overlayed skills

- `atm10-change-protocol` - adapts `aoa-change-protocol` to repo-relative files, commands, and explicit local approval notes
- `atm10-source-of-truth-check` - adapts `aoa-source-of-truth-check` to local doc hierarchies, canonical-file patterns, and repo-relative review guidance

## Risks and anti-patterns

- do not widen the overlay into project doctrine or a scenario bundle
- do not hide downstream authority inside local convenience prose
- do not replace the base skill with family-specific rules that belong upstream or downstream
- do not present this exemplar pack as a live downstream integration
- do not treat the missing governance lane for `atm10-*` as a hidden canonical-promotion gap

## Validation

- confirm the overlay does not change the base skill boundary
- confirm every listed overlay skill has a matching `skills/atm10-*` bundle
- confirm the family review doc and bundle-local review checklists stay aligned
- confirm repo-relative paths and commands stay public-safe and reviewable
- confirm downstream authority remains explicit
- confirm the family stays reviewable as a repo-local exemplar even when downstream consumers read `project_overlay_federation_ready` without a governance lane
