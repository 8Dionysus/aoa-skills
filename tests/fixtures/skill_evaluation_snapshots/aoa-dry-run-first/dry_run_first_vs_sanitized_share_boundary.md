# Evaluation Snapshot

## Prompt

Compare preview-first planning for a risky operational change with preparing a sanitized share of the same change and choose the clearer fit before execution.

## Expected selection

Decision: use `aoa-dry-run-first`.

## Why

- The task is still about how to inspect or simulate the risky change before it touches a live surface.
- A sanitized share can come later, but it is not the main execution decision here.

## Expected object

- This is a dry-run-first case, not a sanitized-share case.
- A preview-first recommendation that explains how to inspect the change before it touches the live surface.

## Boundary notes

- If the preview result later needs broader circulation, move to `aoa-sanitized-share` for the shareable artifact.

## Verification hooks

- Confirm the response names a preview path rather than a sharing workflow.
- Confirm it does not shift the task into artifact sanitization before the preview decision is made.
