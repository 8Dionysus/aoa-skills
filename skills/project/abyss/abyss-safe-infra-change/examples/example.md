# Example

## Scenario

You need to update a repo-local deployment toggle and restart policy inside an `abyss-*` repository, and the team wants the exact command path, local approval note, and rollback check named explicitly before the change runs.

## Why this skill fits

The base infra-change workflow is correct, but the remaining work is a thin local adaptation for one `abyss-*` repo. The overlay keeps the change bounded, repo-relative, and explicit about local authority.

## Expected inputs

- the target operational surface
- the repo-relative file or command path
- the stated local authority or approval posture
- the validation path
- the rollback or recovery idea

## Expected outputs

- a bounded local infra-change plan
- repo-relative command or path notes
- explicit authority and rollback reminders
- a concise verification summary

## Boundary notes

- If the real task is preparing a public-safe summary or artifact, use `abyss-sanitized-share` instead.
- If the base `aoa-safe-infra-change` workflow is already sufficient, do not force the overlay.
- Keep the local adaptation thin and avoid widening into project doctrine.

## Verification notes

- Confirm the repo-relative operational surface was named clearly.
- Confirm the local authority and rollback posture stayed explicit.
- Confirm the change remained bounded to one local repo surface.
- Confirm no broader operational doctrine was introduced.
