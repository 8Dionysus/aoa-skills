# Example

## Scenario

An `atm10-*` repository has `README.md`, `MANIFEST.md`, `docs/RUNBOOK.md`,
`docs/ARCHIVED_TRACKS.md`, `docs/PRODUCT_EDGE_POSTURE.md`, and `docs/SOURCE_OF_TRUTH.md`.
Contributors keep adding runnable commands and support-profile claims to the entrypoint, even though
the active commands, archived references, support claims, and document-role rules already have separate
repo-relative homes.

## Why this skill fits

- the base `aoa-source-of-truth-check` workflow is already correct
- the repo still needs a local canonical-file pattern and explicit doc review posture
- the task is a thin overlay on one repository family, not a broader policy redesign
- ATM10 public docs already define active, archived, support-profile, runtime-baseline, and local-only roles
- the family review doc and bundle-local checklist need to stay aligned

## Expected inputs

- the overlapping repo-relative docs
- the local concern under review, such as startup, deployment, recovery, support-profile claims, runtime baseline, or public status
- `docs/SOURCE_OF_TRUTH.md` as the local document-role map
- any local review rule that decides how doc changes are approved
- the family review doc at `mechanics/boundary-bridge/overlays/atm10/REVIEW.md`

## Expected outputs

- a local source-of-truth map
- an active versus archived/local-only/generated/internal placement note
- a repo-relative canonical-file recommendation
- a short entrypoint-trimming note when `README.md` or `MANIFEST.md` should route outward
- a short verification summary that explains why the docs surface is easier to navigate

## Boundary notes

- do not use this overlay for purely code-local work with no document-authority question
- do not turn the example into a family-wide governance doctrine
- do not use this overlay to decide runtime behavior, model-host selection, perception truth, service exposure, or operator automation authority
- do not move private paths, private logs, hostnames, tokens, screenshots, local model paths, or ignored maintainer scratch into tracked public docs

## Verification notes

- verify that each local concern now points to a named authoritative file
- verify that overview docs no longer silently compete with the canonical guide
- verify that active commands stay in `docs/RUNBOOK.md` and archived/recoverable references stay out of the active runbook
- verify that support-profile or runtime-baseline claims point to the owning ATM10 public surface
- verify that the family review doc and bundle-local checklist stay aligned
