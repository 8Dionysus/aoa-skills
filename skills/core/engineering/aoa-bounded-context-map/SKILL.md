---
name: aoa-bounded-context-map
scope: core
status: canonical
summary: Clarify system, domain, layer, and owner boundaries so changes stay semantically scoped, interface-aware, and portable where needed.
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
- a repository has a dual posture, such as standalone public library and ecosystem organ
- mechanics, skills, techniques, evals, playbooks, generated surfaces, or owner-local implementations are easy to blur together

Do not use this skill when:
- the change is tiny and fully local
- the boundary is already clear and agreed on, and the real task is validating the interface contract; use `aoa-contract-test`
- the main problem is deciding whether logic belongs in the core or at the edge; use `aoa-core-logic-boundary` first

## Inputs

- target area or subsystem
- current naming and responsibilities
- known neighboring contexts
- ambiguous or overloaded terms
- owner layers, stronger owner repositories, or portability constraints that shape the boundary

## Outputs

- named contexts or subsystems
- rough boundary map
- interface notes between contexts
- ambiguity notes and recommended vocabulary
- owner split, stop-line, and portable-versus-integration vocabulary when those boundaries matter

## Procedure

1. identify the target area and the terms people use for it
2. separate responsibilities into bounded contexts, subsystems, layers, or owner repositories
3. name what belongs inside each context and what stays outside
4. distinguish portable core meaning from ecosystem integration, local implementation, generated projection, or historical provenance when those surfaces coexist
5. describe the interfaces, handoffs, stop-lines, or translations between contexts
6. note ambiguous terms and propose clearer language
7. report how the boundary should constrain the next change, including what should route away

## Contracts

- boundaries should reduce semantic confusion, not create ceremony for its own sake
- neighboring contexts should be named explicitly when relevant
- interface or translation points should be visible
- a context map should not transfer authority from a stronger owner into the local repository
- portable core wording should remain usable without hidden ecosystem dependencies when the target surface is public

## Risks and anti-patterns

- inventing too many contexts for a small problem
- renaming concepts without reducing confusion
- treating context maps as proof of good architecture when interfaces remain muddy
- copying center or sibling-repo law into a local surface instead of naming a light handoff
- turning a dual-posture repo into two unrelated identities rather than one bounded interface
- using context labels as decoration while the next diff still crosses owner boundaries

## Verification

- confirm the main ambiguity was reduced
- confirm interfaces or handoff points are named
- confirm the output helps future scoped changes
- confirm the map says what routes away when a stronger owner owns the truth
- confirm portable and integration-only wording remain distinct when both are present

## Technique traceability

Manifest-backed techniques:
- AOA-T-0016 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/proof/skill-support/bounded-context-map/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/instruction/docs-boundary/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

Project overlays should add:
- local domain vocabulary
- canonical docs that define terminology
- local examples of context boundaries
- local owner-route maps, portability rules, and generated-surface handoffs
