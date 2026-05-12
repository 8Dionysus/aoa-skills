# Example

## Scenario

You need to share an `abyss-*` incident note that contains repo-relative paths, internal hostnames, and a local debug command, and the team wants the sanitized output placed in one canonical repo-relative location.

## Why this skill fits

The base sanitization workflow is correct, but the remaining work is a thin local adaptation for one `abyss-*` repo. The overlay keeps the artifact bounded, repo-relative, and explicit about local sharing posture.

## Expected inputs

- the raw material to sanitize
- the intended audience
- the repo-relative destination or sharing surface
- any local thresholds about what must be generalized or removed

## Expected outputs

- a sanitized shareable artifact
- notes about what was generalized or removed
- repo-relative placement guidance
- any remaining sensitivity warning

## Boundary notes

- If the real task is the underlying operational mutation, use `abyss-safe-infra-change` instead.
- If the base `aoa-sanitized-share` skill is already sufficient, do not force the overlay.
- Keep the local adaptation thin and avoid widening into project doctrine.

## Verification notes

- Confirm the repo-relative output surface was named clearly.
- Confirm local thresholds and review posture stayed explicit.
- Confirm the artifact remained useful after sanitization.
- Confirm no broader incident-policy doctrine was introduced.
