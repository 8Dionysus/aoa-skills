# Review Checklist

## Purpose

Use this checklist when reviewing a shareable `abyss-*` artifact that claims to follow `abyss-sanitized-share`.

## When it applies

- raw technical material from an `abyss-*` repo needs a public-safe or wider-shareable form
- the review needs to confirm that repo-relative placement, local thresholds, and sanitization posture stayed explicit
- the family review doc and the local bundle still need to stay aligned

## Review checklist

- [ ] The repo-relative destination or canonical sharing surface is named explicitly.
- [ ] The audience, retention posture, and local review threshold are visible and still downstream.
- [ ] Raw-source and sanitized-output locations stay distinct.
- [ ] The redaction map names what was removed, generalized, summarized, or retained.
- [ ] The sanitized artifact preserves the lesson and evidence shape without preserving unsafe detail.
- [ ] Remaining uncertainty, review limits, or maintainer-only context are named clearly.
- [ ] The final note stays a thin local adaptation of `aoa-sanitized-share`, not a new project doctrine.

## Not a fit

- tasks that are really about performing the underlying operational mutation
- requests where the base `aoa-sanitized-share` skill is already sufficient without `abyss-*` local adaptation
- requests that need an owner-local runtime diagnosis rather than a shareable artifact
