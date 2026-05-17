# Example

## Scenario

You need to update a repo-local deployment toggle and restart policy inside an `abyss-*` repository. The affected files are a checked-in config template, a service wrapper, and a generated readiness receipt, and the team wants the exact repo-relative command path, local approval note, preflight, stop line, and rollback check named before anything runs.

## Why this skill fits

The base infra-change workflow is correct, but the remaining work is a thin local adaptation for one `abyss-*` repo. The overlay keeps the change bounded, repo-relative, and explicit about local authority.

## Expected inputs

- the target operational surface
- the repo-relative file, command, or receipt path
- the surface class and expected side effect
- the stated local authority, approval posture, and stop condition
- the validation path and the smallest preflight or preview
- the rollback or recovery idea
- any sensitivity note for raw logs, host details, or local environment values

## Expected outputs

- a bounded local infra-change plan
- repo-relative command, path, and receipt notes
- explicit authority, stop-line, and rollback reminders
- a proportional verification note that does not claim more than was tested
- a sanitization handoff note if the evidence needs to be shared
- a concise verification summary

## Boundary notes

- If the real task is preparing a public-safe summary or artifact, use `abyss-sanitized-share` instead.
- If the main uncertainty is permission to act, use `aoa-approval-gate-check` first.
- If the main uncertainty is whether a preview proves enough, use `aoa-dry-run-first` first.
- If the base `aoa-safe-infra-change` workflow is already sufficient, do not force the overlay.
- Keep the local adaptation thin and avoid widening into project doctrine.

## Verification notes

- Confirm the repo-relative operational surface was named clearly.
- Confirm the local authority, stop condition, and rollback posture stayed explicit.
- Confirm the selected preflight or preview matched the surface class.
- Confirm the change remained bounded to one local repo surface.
- Confirm raw runtime material was not copied into a shareable note without sanitization.
- Confirm no broader operational doctrine was introduced.
