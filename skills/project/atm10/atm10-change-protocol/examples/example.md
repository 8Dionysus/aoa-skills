# Example

## Scenario

An `atm10-*` repository needs a bounded code-and-doc change that touches `README.md`,
`docs/RUNBOOK.md`, `scripts/gateway_v1_smoke.py`, and a matching test, and the maintainer wants the local
route cards, commands, approval posture, recovery anchor, and review surface named explicitly before editing.

## Why this skill fits

- the base `aoa-change-protocol` workflow is already the right shape
- the repo still needs repo-relative files, commands, and review rules spelled out locally
- the task is a thin local adaptation, not a new workflow or playbook
- `ATM10-Agent` has local route law for docs, scripts, tests, dry-run safety, and public support claims
- the family review doc and bundle-local checklist need to stay aligned

## Expected inputs

- the local files or surfaces under change, plus the nearest `AGENTS.md` cards for those paths
- `docs/SOURCE_OF_TRUTH.md` when public docs move, `docs/RUNBOOK.md` when runnable commands move, and `docs/PRODUCT_EDGE_POSTURE.md` when support/test-tier claims move
- the smallest repo-relative check, such as `python -m pytest`, public-doc hardening tests, or a targeted script smoke
- any local approval or review rule that still requires a maintainer decision
- the rollback or recovery anchor for the touched surface
- the family review doc at `mechanics/boundary-bridge/overlays/atm10/REVIEW.md`

## Expected outputs

- a bounded local change plan
- route-card evidence inspected before apply
- repo-relative command, verification, and recovery notes
- an explicit stop-line for runtime, operator automation, service exposure, or host-specific assumptions
- a short report that names what remains explicitly downstream

## Boundary notes

- do not use this overlay if the base skill can be used directly with no local adaptation
- do not widen the request into project doctrine or cross-repo automation
- do not use this overlay to authorize live input events or stronger-than-dry-run automation
- do not publish private workstation paths, tokens, local model paths, or private run logs as portable facts

## Verification notes

- verify that the plan still follows the base `plan -> scoped change -> verify -> report` shape
- verify that all local files and commands stay repo-relative and reviewable
- verify that the chosen check matches the touched surface and any skipped check is named
- verify that dry-run or report-only safety is preserved unless ATM10-owned evidence says otherwise
- verify that the family review doc and bundle-local checklist still agree
