# Review Checklist

## Purpose

Use this checklist when reviewing a bounded `abyss-*` operational or configuration change that claims to follow `abyss-safe-infra-change`.

## When it applies

- the change touches infrastructure, orchestration, runtime configuration, or operational surfaces inside an `abyss-*` repo
- the review needs to confirm that repo-relative commands, authority notes, and rollback posture stayed explicit
- the family review doc and the local bundle still need to stay aligned

## Review checklist

- [ ] The repo-relative operational surface and the main risk are named before execution.
- [ ] The surface class is clear: source config, runtime wrapper, generated receipt, launch command, environment template, deployment toggle, or verification script.
- [ ] The local authority, approval posture, stop condition, and any human confirmation remain visible and downstream.
- [ ] Verification is explicit, proportional to the side effect, and does not overclaim beyond the preflight or preview actually run.
- [ ] Rollback or recovery thinking is present before execution or recommendation, with a concrete repo-relative anchor where possible.
- [ ] Host paths, secrets, environment details, and raw logs are kept out of shareable review notes unless separately sanitized.
- [ ] The final note stays a thin local adaptation of `aoa-safe-infra-change`, not a new project doctrine.

## Not a fit

- tasks that are really about producing a shareable artifact rather than changing the operational surface
- requests where the base `aoa-safe-infra-change` skill is already sufficient without `abyss-*` local adaptation
- requests that need authority discovery, dry-run interpretation, or public sanitization more than an infra-change overlay
