---
name: abyss-self-diagnostic-spine
scope: project
status: scaffold
summary: Thin abyss overlay for turning runtime-body evidence plus optional reviewed session references into one bounded diagnostic session artifact and an honest next-move class without granting silent self-mutation.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-0080
  - AOA-T-0081
---

# abyss-self-diagnostic-spine

## Intent

Use this skill to adapt `aoa-session-self-diagnose` to an `abyss-*` repository
when the local repo needs one runtime-owned diagnostic session artifact that can
cite runtime evidence, compare against last-good posture, and hand off honestly
toward the reviewed session diagnosis family.

## Trigger boundary

Use this skill when:
- the base `aoa-session-self-diagnose` workflow is already correct, but an `abyss-*` repo needs one runtime-owned diagnostic session artifact with repo-relative evidence refs
- a concrete runtime path must be diagnosed before any repair claim becomes honest
- multiple runtime-body signals exist but remain scattered across local docs, logs, or checks
- reviewed session evidence exists and should be cited rather than absorbed into runtime canon
- the next honest move may be retest, governed repair, quest follow-up, progression lift, or manual regrounding

Do not use this skill when:
- the route is asking for immediate silent repair; use `aoa-session-self-repair` only after reviewed diagnosis exists
- there is no concrete target path to diagnose
- the material is still a live unreviewed session that belongs in the session-harvest family first
- no `abyss-*` repo adaptation is needed and the base `aoa-session-self-diagnose` skill is sufficient
- the work would widen into broader project doctrine instead of a thin local overlay

## Inputs

- resolved or requested preset / profile selectors
- runtime-body signals such as doctor, machine-fit, render-truth, smoke, autonomy, or related evidence refs
- optional reviewed session or harvest packet refs
- optional last-good comparison ref
- base skill reference

## Outputs

- one bounded runtime-owned `diagnostic_session_v1`
- one explicit `exit_class`
- named drift classes with evidence refs and unknowns when needed
- optional handoff recommendation toward:
  - `aoa-session-self-diagnose`
  - `aoa-session-self-repair`
  - `aoa-session-progression-lift`
  - `aoa-quest-harvest`
- a concise verification note for the local repo surface

## Procedure

1. start from `aoa-session-self-diagnose` instead of inventing a new project-family workflow
2. resolve the diagnostic target before interpreting symptoms
3. gather repo-relative runtime-body evidence refs without widening ownership
4. normalize the evidence into multi-axis verdicts and explicit drift classes
5. compare against last-good posture when a bounded anchor exists
6. choose one exit class
7. if reviewed session evidence exists, cite the next honest owner-facing handoff
8. emit the artifact without mutating quest, repair, or progression authority

## Contracts

- preserve the base skill meaning
- the overlay stays read-only and citation-friendly
- this overlay does not replace `aoa-doctor`
- this overlay does not grant free self-repair
- reviewed session packets remain packet-shaped and owner-aware
- quest state is not auto-mutated by this overlay
- public-safe defaults stay strong

## Risks and anti-patterns

- treating one axis failure as total collapse
- confusing runtime drift with source-owned doctrine drift
- using diagnosis to smuggle mutation authority
- turning every repeated issue into automatic progression or quest promotion
- hiding unknowns instead of naming them
- silently changing the base workflow instead of adapting the local repo surface

## Verification

- confirm the base skill is still the correct workflow
- confirm a concrete target exists
- confirm the produced artifact stays runtime-owned and citation-friendly
- confirm drift classes are named explicitly
- confirm one exit class is chosen
- confirm any handoff points to the right owner layer
- confirm no silent repair authority was added

## Technique traceability

Manifest-backed techniques:
- AOA-T-0080 from `8Dionysus/aoa-techniques` at `364da8f4e97d0c29f4b31c59d7bfd91585633f2a` using path `techniques/agent-workflows/session-drift-taxonomy/TECHNIQUE.md` and sections: Intent, Outputs, Risks, Validation
- AOA-T-0081 from `8Dionysus/aoa-techniques` at `364da8f4e97d0c29f4b31c59d7bfd91585633f2a` using path `techniques/agent-workflows/diagnosis-from-reviewed-evidence/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Validation

## Adaptation points

- repo-relative runtime evidence refs
- local diagnostic target and last-good posture
- local drift-taxonomy examples
- local handoff notes toward reviewed diagnosis, repair, progression, and quest surfaces
- family review doc and bundle-local review checklist
