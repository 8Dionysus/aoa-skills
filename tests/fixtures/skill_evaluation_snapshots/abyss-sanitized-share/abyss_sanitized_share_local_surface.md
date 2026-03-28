# Evaluation Snapshot
## Prompt
Turn raw abyss incident material into a shareable artifact and place it in one repo-relative canonical location with explicit local sanitization thresholds.
## Expected selection
use
## Why
The base `aoa-sanitized-share` workflow is already correct, but the local repo still needs a repo-relative destination and explicit local sharing thresholds.
## Expected object
A sanitized local share artifact that names the repo-relative destination and explicit local sharing thresholds.
## Boundary notes
Use this overlay when the base sanitization workflow is right and the remaining work is a thin `abyss-*` local sharing adaptation.
## Verification hooks
The response should name the repo-relative destination, explain what was generalized or removed, and keep local review posture visible.
