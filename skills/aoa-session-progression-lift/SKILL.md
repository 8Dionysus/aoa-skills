---
name: aoa-session-progression-lift
scope: core
status: scaffold
summary: Lift reviewed session evidence into a multi-axis progression delta with bounded unlock hints, quest reflection cues, and no fake single-score authority.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-PROGRESSION-EVIDENCE-LIFT
  - AOA-T-PENDING-MULTI-AXIS-QUEST-OVERLAY
---

# aoa-session-progression-lift

## Intent

Use this skill to author a `PROGRESSION_DELTA` from reviewed evidence.

This is not score inflation.
It is an evidence-backed overlay that says what mastery axes moved, what should
hold or reanchor, and what small unlock hints are now safer.

## Trigger boundary

Use this skill when:
- a reviewed session generated meaningful mastery evidence
- the route needs progression legibility without mutating source role profiles
- quest or RPG reflection would help continuation
- the output needs to stay small, evidence-backed, and multi-axis

Do not use this skill when:
- there is no reviewed evidence
- the request wants one global power number
- progression is being used as hidden routing policy
- the route is trying to mint authority rights without evidence

## Inputs

- reviewed session artifact or harvest packet
- named evidence refs
- relevant role or cohort context if known
- existing progression baseline if available

## Outputs

- `PROGRESSION_DELTA` with axis movement, verdict, and optional unlock hints
- optional rank reflection note if evidence is strong enough
- quest hooks or chronicle stub when useful
- negative or cautionary evidence when a hold, reanchor, or downgrade is more honest than advance

## Procedure

1. collect reviewed evidence refs
2. assess movement qualitatively across `boundary_integrity`,
   `execution_reliability`, `change_legibility`, `review_sharpness`,
   `proof_discipline`, `provenance_hygiene`, and `deep_readiness`
3. emit a verdict: advance, hold, reanchor, or downgrade
4. name small unlock hints only when evidence supports them
5. allow negative, zero, and cautionary movement
6. map ability or feat hints only as reflection, not as ownership transfer

## Contracts

- progression remains evidence-backed
- multi-axis only; no authoritative universal score
- rank labels are descriptive, not sovereign
- unlock hints must stay reviewable and small
- progression does not replace owner-layer truth or routing authority

## Risks and anti-patterns

- inventing progress from mood
- using progression as policy
- granting authority without cited evidence
- flattening multi-axis growth into one number
- confusing quest flavor with durable proof

## Verification

- confirm all meaningful axis claims cite reviewed evidence
- confirm the verdict matches the evidence
- confirm zero or negative movement remains allowed
- confirm unlock hints are small and explicit
- confirm no universal score is introduced

## Technique traceability

Pending manifest-backed techniques:
- AOA-T-PENDING-PROGRESSION-EVIDENCE-LIFT from `8Dionysus/aoa-techniques` with `path: TBD` and `source_ref: TBD`; intended sections: Intent, Inputs, Outputs, Contracts, Validation
- AOA-T-PENDING-MULTI-AXIS-QUEST-OVERLAY from `8Dionysus/aoa-techniques` with `path: TBD` and `source_ref: TBD`; intended sections: Outputs, Risks, Validation

## Adaptation points

Project overlays may add:
- local axis notes
- role-affinity hints
- local unlock classes
