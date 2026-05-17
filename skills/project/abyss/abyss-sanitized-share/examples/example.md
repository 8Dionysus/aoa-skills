# Example

## Scenario

You need to share an `abyss-*` incident note that contains repo-relative paths, internal hostnames, local debug commands, environment values, and timing traces. The team wants a useful public-safe summary in one repo-relative destination while the raw note remains owner-local.

## Why this skill fits

The base sanitization workflow is correct, but the remaining work is a thin local adaptation for one `abyss-*` repo. The overlay keeps the artifact bounded, repo-relative, and explicit about local sharing posture.

## Expected inputs

- the raw material to sanitize
- the intended audience
- the repo-relative destination or sharing surface
- the raw-source location and the sanitized-output location
- any local thresholds about what must be removed, generalized, summarized, or retained
- the retention or review posture for raw material and sanitized output

## Expected outputs

- a sanitized shareable artifact
- notes about what was generalized, removed, summarized, or retained
- repo-relative placement guidance
- an audience and remaining-review note
- a raw-vs-sanitized separation note
- any remaining sensitivity warning

## Boundary notes

- If the real task is the underlying operational mutation, use `abyss-safe-infra-change` instead.
- If the real task is owner-local runtime diagnosis, keep the raw evidence in the diagnostic route instead of turning it into a public artifact too early.
- If the base `aoa-sanitized-share` skill is already sufficient, do not force the overlay.
- Keep the local adaptation thin and avoid widening into project doctrine.

## Verification notes

- Confirm the repo-relative output surface was named clearly.
- Confirm audience, thresholds, retention, and review posture stayed explicit.
- Confirm raw material and sanitized output stayed separate.
- Confirm the artifact remained useful after sanitization.
- Confirm the artifact did not preserve host, account, secret, token, environment, or unpublished operational detail unnecessarily.
- Confirm no broader incident-policy doctrine was introduced.
