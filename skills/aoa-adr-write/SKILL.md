---
name: aoa-adr-write
scope: core
status: canonical
summary: Record a meaningful architectural or workflow decision, place it in the canonical note surface, and verify that future readers can find the rationale rather than only the outcome.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-0033
  - AOA-T-0002
---

# aoa-adr-write

## Intent

Use this skill to capture an architectural, structural, or workflow decision in a concise reviewable note, then place and verify that note in the canonical repo surface so the rationale stays findable.

## Trigger boundary

Use this skill when:
- a decision changes structure, boundaries, tooling, or workflow expectations
- future contributors will need to know why a path was chosen
- several plausible options existed and the reasoning matters
- the team or project risks repeating the same debate later
- the note needs a clear canonical home, not just a one-off comment

Do not use this skill when:
- the change is tiny and self-evident
- the note would only restate an obvious diff with no real decision content
- the main problem is unclear authoritative documentation rather than decision rationale; use `aoa-source-of-truth-check` first
- the main problem is deciding whether logic belongs in the core or at the edge; use `aoa-core-logic-boundary` first

## Inputs

- decision to record
- context and problem statement
- relevant options or alternatives
- chosen path and rationale
- known consequences or tradeoffs

## Outputs

- concise decision note or ADR draft
- statement of rationale
- consequence notes
- canonical placement or reference for the note
- verification that the note landed in the expected decision surface
- verification that the note matches the actual change

## Procedure

1. state the context and the problem the decision addresses
2. list the main options if they meaningfully shaped the choice
3. record the chosen decision in clear language
4. note why it was chosen and what tradeoffs it introduces
5. place the note in the canonical decision surface or repo-local home that future reviewers should use
6. connect the note to the actual change surface when relevant
7. verify that the note explains the decision rather than narrating the diff only
8. verify that the note is reachable from the intended canonical location

## Contracts

- the note should explain why, not just what changed
- the decision should be bounded and understandable
- tradeoffs should not be hidden behind certainty theater
- the note should help future reviewers, not merely satisfy process
- the note should have an explicit canonical placement, not a hidden or implied home
- verification should check both rationale quality and note placement

## Risks and anti-patterns

- writing an ADR for a trivial edit with no real decision
- using inflated language to mask weak reasoning
- recording the chosen path without naming consequences
- letting the ADR drift away from the actual change
- treating placement as optional after the note is written
- using the skill when the main work is still source-of-truth clarification

## Verification

- confirm the decision was meaningful enough to record
- confirm the rationale is explicit
- confirm consequences or tradeoffs are named
- confirm the note aligns with the real change surface
- confirm the note is placed where future reviewers will look for it
- confirm the canonical location or reference is part of the result, not an afterthought

## Technique traceability

Manifest-backed techniques:
- AOA-T-0033 from `8Dionysus/aoa-techniques` at `5c6f0496edc3c2e74590baa35627c85fe58ef765` using path `techniques/docs/decision-rationale-recording/TECHNIQUE.md` and sections: Intent, When to use, When not to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `5c6f0496edc3c2e74590baa35627c85fe58ef765` using path `techniques/docs/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, When not to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

Future project overlays may add:
- local ADR templates
- alternative decision-note homes outside formal `docs/adr/` layouts
- local placement rules
- local template variants that still preserve context, options, decision, and consequences
- architecture review expectations
- cross-linking rules back to canonical authority docs without replacing them
- repository-specific examples
