---
name: aoa-sanitized-share
scope: risk
status: scaffold
summary: Prepare findings, logs, examples, or diagnostics for sharing without leaking secrets, private topology, or unsafe operational detail.
invocation_mode: explicit-only
technique_dependencies: []
---

# aoa-sanitized-share

## Intent

Use this skill to turn potentially sensitive technical material into a shareable, reviewable, public-safe form.

## Trigger boundary

Use this skill when:
- logs, configs, diagnostics, reports, or examples may contain sensitive details
- a result needs to be shared publicly or with a broader audience
- raw material may reveal secrets, topology, internal identifiers, or unsafe context

Do not use this skill when:
- the material is already clearly public-safe and minimal
- the task is to perform the underlying operational change rather than prepare a shareable surface
- the main task is deciding whether the underlying action should be allowed; use `aoa-approval-gate-check`
- the task is to preview or execute the operational change itself; use `aoa-dry-run-first` or `aoa-safe-infra-change`

## Inputs

- material to be shared
- sharing audience or context
- known sensitive surfaces
- acceptable level of abstraction

## Outputs

- sanitized shareable artifact, abstract summary, or recommendation not to share the raw material directly
- note on what was generalized or removed
- warning about any remaining ambiguity or sensitive edge

## Procedure

1. inspect the material for secrets, tokens, private paths, topology, internal identifiers, or unsafe operational detail
2. remove, redact, or generalize sensitive details
3. preserve the technical lesson or signal without preserving the sensitive surface
4. note what kind of sanitization was applied when that matters for interpretation
5. verify that the shared result remains useful without revealing what should stay private

## Contracts

- shareable output should not leak secrets or private infrastructure detail
- sanitization should preserve meaning where possible
- generalization should not silently change the core lesson beyond recognition
- uncertainty about sensitivity should lean toward caution

## Risks and anti-patterns

- over-sanitizing until the artifact becomes meaningless
- under-sanitizing because a value looks harmless in isolation
- forgetting that topology and naming can be sensitive even without tokens
- sharing raw excerpts when a bounded summary would be safer

## Verification

- confirm obvious sensitive surfaces were checked
- confirm the resulting artifact is still understandable
- confirm the sanitization level matches the intended audience
- confirm raw sensitive detail was not preserved by accident
- confirm remaining uncertainty is named rather than ignored

## Future traceability

Technique linkage is intentionally deferred for this scaffold.
Later revisions may connect this skill to reusable techniques in `aoa-techniques`.

## Adaptation points

Future project overlays may add:
- local sanitization rules
- examples of sensitive surfaces
- public versus private sharing thresholds
- project-specific reporting conventions
