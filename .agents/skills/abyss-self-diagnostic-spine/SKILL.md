---
name: abyss-self-diagnostic-spine
description: 'Explicit activation required: do not invoke or load this skill from an implicit match; wait for explicit user or operator invocation or a source-authorized parent-route selection. Apply the aoa-session-self-diagnose workflow inside an abyss-* repository using repo-relative runtime evidence, bounded diagnostic-session artifacts, last-good comparison posture, and honest owner-aware handoff. Use when the base diagnosis workflow is correct but one abyss repo needs a thin runtime-owned diagnostic read model before any repair claim becomes honest. Do not use when the request is really for silent repair, when no concrete target path exists, or when the base skill is already sufficient without local adaptation.'
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: project
  aoa_status: scaffold
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/project/abyss/abyss-self-diagnostic-spine/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0080,AOA-T-0081
  aoa_portable_profile: codex-facing-wave-3
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
- multiple runtime-body signals exist but remain scattered across local docs, logs, checks, generated receipts, or run outputs
- the evidence spans axes such as doctor, machine-fit, render-truth, smoke, autonomy, config projection, route receipt, or last-good comparison and needs one bounded diagnostic shape
- reviewed session evidence exists and should be cited rather than absorbed into runtime canon
- the next honest move may be retest, governed repair, quest follow-up, progression lift, or manual regrounding

Do not use this skill when:
- the route is asking for immediate silent repair; use `aoa-session-self-repair` only after reviewed diagnosis exists
- there is no concrete target path to diagnose
- the material is still a live unreviewed session that belongs in the session-harvest family first
- the main confusion is which diagnostic doc, runbook, or route surface is authoritative; use `aoa-source-of-truth-check`
- the ask is only to run a generic doctor or health command without producing a reviewed diagnostic artifact
- the request needs a broad project doctrine change, quest mutation, progression update, or repair packet rather than read-only diagnosis
- no `abyss-*` repo adaptation is needed and the base `aoa-session-self-diagnose` skill is sufficient
- the work would widen into broader project doctrine instead of a thin local overlay

## Inputs
- resolved or requested diagnostic target, preset, profile, or repo-relative path
- runtime-body signals such as doctor, machine-fit, render-truth, smoke, autonomy, config projection, route receipt, or related evidence refs
- evidence timestamps, command refs, generated receipt refs, and known freshness limits
- optional reviewed session, harvest packet, closeout, or owner-facing handoff refs
- optional last-good comparison ref and the reason it is a valid anchor
- intended local truth goal and the stop line before repair or quest mutation
- base skill reference

## Outputs
- one bounded runtime-owned `diagnostic_session_v1`
- one explicit `exit_class` chosen from a locally named finite set, such as `retest`, `governed_repair`, `manual_regrounding`, `owner_handoff`, or `insufficient_evidence`
- named drift classes with evidence refs and unknowns when needed
- per-axis verdicts that preserve mixed states instead of flattening everything into one pass/fail result
- freshness and confidence notes for each major evidence family
- optional handoff recommendation toward:
  - `aoa-session-self-diagnose`
  - `aoa-session-self-repair`
  - `aoa-session-progression-lift`
  - `aoa-quest-harvest`
- a concise verification note for the local repo surface

## Procedure
1. start from `aoa-session-self-diagnose` instead of inventing a new project-family workflow
2. resolve the diagnostic target before interpreting symptoms or naming a drift class
3. confirm the nearest route card and source-of-truth surface so the artifact does not claim ownership over a stronger layer
4. gather repo-relative runtime-body evidence refs without widening ownership or copying raw sensitive material into the artifact
5. classify evidence by axis and freshness, including unknowns and missing checks
6. normalize the evidence into multi-axis verdicts and explicit drift classes
7. compare against last-good posture only when the anchor is bounded and still relevant
8. choose one exit class and name the smallest next owner route it permits
9. if reviewed session evidence exists, cite it as evidence or handoff context rather than absorbing it into runtime canon
10. emit the artifact without mutating quest, repair, or progression authority

## Contracts
- preserve the base skill meaning
- the overlay stays read-only and citation-friendly
- semantic matches do not silently activate this scaffold; use an explicit handle or deliberate manual route decision
- this overlay does not replace `aoa-doctor`
- this overlay does not grant free self-repair
- reviewed session packets remain packet-shaped and owner-aware
- quest state is not auto-mutated by this overlay
- source-owned doctrine, generated receipts, runtime facts, and reviewed session evidence keep distinct roles
- one failed axis cannot erase healthy axes, and one healthy axis cannot hide a blocker
- public-safe defaults stay strong

## Risks and anti-patterns
- treating one axis failure as total collapse
- confusing runtime drift with source-owned doctrine drift
- using diagnosis to smuggle mutation authority
- turning every repeated issue into automatic progression or quest promotion
- hiding unknowns instead of naming them
- treating generated receipts as current when their freshness is unknown
- absorbing reviewed session packets into runtime canon instead of citing them
- using the `abyss-*` overlay when the base session diagnosis skill or a source-of-truth check is the smaller route
- silently changing the base workflow instead of adapting the local repo surface

## Verification
- confirm the base skill is still the correct workflow
- confirm a concrete target exists
- confirm the produced artifact stays runtime-owned and citation-friendly
- confirm drift classes are named explicitly
- confirm per-axis verdicts, freshness, confidence, and unknowns are visible
- confirm one exit class is chosen
- confirm any handoff points to the right owner layer
- confirm no silent repair authority was added
- confirm no quest, progression, or source-of-truth mutation was implied

## Technique traceability
Manifest-backed techniques:
- AOA-T-0080 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/recovery/diagnosis-repair/session-drift-taxonomy/TECHNIQUE.md` and sections: Intent, Outputs, Risks, Validation
- AOA-T-0081 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/recovery/diagnosis-repair/diagnosis-from-reviewed-evidence/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Validation

## Adaptation points
- repo-relative runtime evidence refs
- local diagnostic target and last-good posture
- local drift-taxonomy examples
- local handoff notes toward reviewed diagnosis, repair, progression, and quest surfaces
- family review doc and bundle-local review checklist
