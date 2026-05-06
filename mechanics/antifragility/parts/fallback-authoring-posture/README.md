# Fallback Authoring Posture

## Use When

Use this part when a future or changed skill bundle needs explicit degraded
behavior, fallback, safe-stop, receipt, or adaptation writeback posture.

## Do Not Use When

Do not use this part to replace an existing skill contract, introduce a broad
schema mandate, silently widen authority, or define owner-local degraded
runtime behavior.

## Route Check

- Which skill or future skill family needs visible failure posture?
- What degraded modes, fallback tree, reground sources, safe-stop threshold,
  mutation block conditions, receipt contract, or adaptation writeback contract
  are actually relevant?
- Which owner-local surfaces remain authoritative during degradation?
- Does the change belong in `SKILL.md`, support resources, runtime guardrails,
  or an owner repository instead?

## Active Outputs

- fallback authoring cue
- degraded-mode checklist
- receipt or safe-stop cue
- owner route for local behavior
- no canonical skill change by itself

## Next Route

When the posture becomes part of a real workflow, edit the canonical
`skills/**/SKILL.md` through normal review and validation. Route runtime
guardrails to runtime owners and proof claims to `aoa-evals`.
