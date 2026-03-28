---
name: abyss-sanitized-share
scope: project
status: evaluated
summary: Thin abyss overlay for turning raw repo-local technical material into a shareable public-safe surface with explicit local thresholds and canonical placement notes.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-0034
  - AOA-T-0002
---

# abyss-sanitized-share

## Intent

Use this skill to adapt `aoa-sanitized-share` to an `abyss-*` repository when the base sanitization workflow is right but the local repo still needs repo-relative sharing surfaces, thresholds, and review posture.

## Trigger boundary

Use this skill when:
- the base `aoa-sanitized-share` workflow is already correct, but an `abyss-*` repo needs local sharing surfaces, repo-relative paths, or explicit sanitization thresholds
- raw logs, diagnostics, config snippets, or incident notes from one `abyss-*` repo need a bounded public-safe or wider-shareable form
- the local repo needs a canonical place or review posture for the sanitized output
- the family review doc and bundle-local checklist still need to stay aligned

Do not use this skill when:
- the real task is the underlying operational or configuration mutation itself; use `abyss-safe-infra-change`
- no `abyss-*` repo adaptation is needed and the base `aoa-sanitized-share` skill is sufficient
- the overlay would only restate the base sanitization workflow without adding a real local sharing surface
- the main question is whether the underlying action should be allowed at all; use `aoa-approval-gate-check`
- the material is already clearly public-safe and no local sharing surface or threshold needs clarification
- the work would widen into broader project doctrine instead of a thin local overlay

## Inputs

- raw material to sanitize
- intended audience or sharing context
- repo-relative destination or canonical sharing surface
- local sensitivity thresholds or review posture
- base skill reference

## Outputs

- sanitized local shareable artifact
- note on what was generalized or removed
- repo-relative placement or reference
- pointer to the family review surface
- concise warning about any remaining sensitive edge

## Procedure

1. start from `aoa-sanitized-share` rather than inventing a new family-specific sharing workflow
2. name the repo-relative output surface, audience, and local sensitivity thresholds that matter
3. keep the adaptation bounded to one local repo family surface
4. preserve the base raw-vs-shareable split and caution-first sanitization posture
5. make explicit what still requires downstream human review or unpublished local judgment

## Contracts

- preserve the base skill meaning
- keep local paths and output placement repo-relative and explicit
- keep local review posture visible rather than implied
- keep the overlay explicit-only, public-safe, and reviewable

## Risks and anti-patterns

- hiding local sharing thresholds in vague prose
- collapsing a thin overlay into project doctrine or incident policy
- naming a repo-relative destination without enough sanitization or audience context
- silently replacing the base workflow instead of adapting the local repo surface

## Verification

- confirm the base skill is still the correct workflow
- confirm the repo-relative sharing surface is named explicitly
- confirm local thresholds and review posture are visible rather than implied
- confirm the adaptation stays bounded to one local repo family surface
- confirm the family review doc and bundle-local checklist stay aligned

## Technique traceability

Manifest-backed techniques:
- AOA-T-0034 from `8Dionysus/aoa-techniques` at `06303d62e9cd614295a63b6543a4191e808e879c` using path `techniques/docs/public-safe-artifact-sanitization/TECHNIQUE.md` and sections: Intent, When to use, When not to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `06303d62e9cd614295a63b6543a4191e808e879c` using path `techniques/docs/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

- repo-relative sharing surfaces
- local sanitization thresholds
- local review posture for sharing
- project-specific output placement examples
- family review doc and bundle-local review checklist
