---
name: aoa-source-of-truth-check
scope: core
status: scaffold
summary: Check whether repository guidance, canonical docs, and operational instructions have clear ownership and do not silently conflict.
invocation_mode: explicit-preferred
technique_dependencies: []
---

# aoa-source-of-truth-check

## Intent

Use this skill to clarify which files are authoritative for status, architecture, run instructions, policy, and change guidance.

## Trigger boundary

Use this skill when:
- a repository has several docs that may overlap or conflict
- contributors may not know which file to trust first
- a change touches docs, process, or operational guidance
- confusion exists between overview docs and authoritative docs

Do not use this skill when:
- the repository is tiny and has no meaningful source-of-truth ambiguity
- the task is purely code-local with no documentation or policy impact

## Inputs

- repository docs surface
- target area of ambiguity or overlap
- known canonical files if any
- current contributor confusion points

## Outputs

- clearer source-of-truth map
- note of overlaps or conflicts
- proposed or implemented document role clarification
- verification summary

## Procedure

1. identify the main docs or guidance files involved in the target area
2. determine which file should be authoritative for each concern
3. note any overlap, contradiction, or role ambiguity
4. clarify or propose clarifying document ownership and purpose
5. keep the change bounded to the guidance surface under review
6. verify that the result reduces ambiguity for future changes

## Contracts

- authoritative sources should be visible and named explicitly
- overview documents should not silently replace canonical ones
- role separation should reduce confusion, not create extra ceremony
- the resulting guidance should be understandable to another human or agent

## Risks and anti-patterns

- over-formalizing a tiny docs surface
- creating many labels without reducing ambiguity
- moving truth across files without clearly signaling the change
- letting summaries masquerade as canonical instructions

## Verification

- confirm the main source-of-truth ambiguity was reduced
- confirm authoritative files are named explicitly
- confirm overlaps or conflicts were surfaced rather than hidden
- confirm the result helps future contributors orient faster

## Future traceability

Technique linkage is intentionally deferred for this scaffold.
Later revisions may connect this skill to reusable techniques in `aoa-techniques`.

## Adaptation points

Future project overlays may add:
- local doc hierarchies
- preferred canonical-file patterns
- local review rules for doc changes
- repository-specific examples of authoritative surfaces
