# Review Checklist

## Purpose

Use this checklist when reviewing a bounded `abyss-*` operational or configuration change that claims to follow `abyss-safe-infra-change`.

## When it applies

- the change touches infrastructure, orchestration, runtime configuration, or operational surfaces inside an `abyss-*` repo
- the review needs to confirm that repo-relative commands, authority notes, and rollback posture stayed explicit
- the family review doc and the local bundle still need to stay aligned

## Review checklist

- [ ] The repo-relative operational surface and the main risk are named before execution.
- [ ] The local authority or approval posture is visible and still downstream.
- [ ] Verification is explicit and proportional to the operational risk.
- [ ] Rollback or recovery thinking is present before execution or recommendation.
- [ ] The final note stays a thin local adaptation of `aoa-safe-infra-change`, not a new project doctrine.

## Not a fit

- tasks that are really about producing a shareable artifact rather than changing the operational surface
- requests where the base `aoa-safe-infra-change` skill is already sufficient without `abyss-*` local adaptation
