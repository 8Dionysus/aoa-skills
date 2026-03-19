---
name: aoa-bounded-context-map
scope: core
status: scaffold
summary: Clarify or carve system and domain boundaries so changes stay semantically scoped and interface-aware.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-0016
  - AOA-T-0002
---

# aoa-bounded-context-map

## Intent

Use bounded-context thinking to reduce semantic drift, mixed responsibilities, and unclear interfaces.

## Trigger boundary

Use this skill when:
- a project mixes several domains or subsystems
- naming is drifting or overloaded
- the task needs a clearer boundary before coding safely
- an agent is likely to confuse nearby concepts without sharper separation

Do not use this skill when:
- the change is tiny and fully local
- the boundary is already clear and agreed on

## Inputs

- target area or subsystem
- current naming and responsibilities
- known neighboring contexts
- ambiguous or overloaded terms

## Outputs

- named contexts or subsystems
- rough boundary map
- interface notes between contexts
- ambiguity notes and recommended vocabulary

## Procedure

1. identify the target area and the terms people use for it
2. separate responsibilities into bounded contexts or subsystems
3. name what belongs inside each context and what stays outside
4. describe the interfaces or translations between contexts
5. note ambiguous terms and propose clearer language
6. report how the new boundary should shape future changes

## Contracts

- boundaries should reduce semantic confusion, not create ceremony for its own sake
- neighboring contexts should be named explicitly when relevant
- interface or translation points should be visible

## Risks and anti-patterns

- inventing too many contexts for a small problem
- renaming concepts without reducing confusion
- treating context maps as proof of good architecture when interfaces remain muddy

## Verification

- confirm the main ambiguity was reduced
- confirm interfaces or handoff points are named
- confirm the output helps future scoped changes

## Technique traceability

Manifest-backed techniques:
- AOA-T-0016 from `8Dionysus/aoa-techniques` at `a6f43089625afe286dda772e733b9d02d2759ac8` using path `techniques/docs/bounded-context-map/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `a6f43089625afe286dda772e733b9d02d2759ac8` using path `techniques/docs/source-of-truth-layout/TECHNIQUE.md` and sections: summary

## Adaptation points

Project overlays should add:
- local domain vocabulary
- canonical docs that define terminology
- local examples of context boundaries
