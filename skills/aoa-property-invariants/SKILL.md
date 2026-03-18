---
name: aoa-property-invariants
scope: core
status: scaffold
summary: Express stable system or domain truths as invariant-oriented tests and checks rather than only enumerating examples.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-PENDING-PROPERTY-INVARIANTS
  - AOA-T-0007
---

# aoa-property-invariants

## Intent

Use invariant-oriented thinking to test broad behavior through properties rather than only through a short list of fixed examples.

## Trigger boundary

Use this skill when:
- a rule should hold across many inputs or states
- examples alone feel too narrow
- the system has conservation, monotonicity, idempotency, or structural invariants
- safety or correctness depends on broad input coverage

Do not use this skill when:
- the behavior is mostly about presentation details or narrow snapshots
- no meaningful invariant is yet understood

## Inputs

- target rule or domain truth
- current examples or tests
- input space or generators
- known edge cases

## Outputs

- explicit invariants
- property-oriented tests or checks
- notes on generator assumptions
- verification summary

## Procedure

1. identify what must remain true across many cases
2. separate strong invariants from weak hopes or vague expectations
3. express those invariants as property-oriented tests or repeated checks
4. keep the generators or inputs bounded and reviewable
5. run the checks and report what properties now constrain behavior

## Contracts

- each property should express a real invariant, not a wish
- the test should broaden coverage beyond a small handpicked set
- generator assumptions should remain understandable

## Risks and anti-patterns

- writing weak properties that prove almost nothing
- confusing random data with meaningful coverage
- using property checks where a small set of concrete examples would be clearer
- hiding domain confusion behind fancy generator logic

## Verification

- confirm the property expresses a meaningful invariant
- confirm the invariant broadens coverage beyond fixed examples
- confirm the result is understandable to another human or agent

## Technique traceability

Primary source techniques:
- AOA-T-PENDING-PROPERTY-INVARIANTS
- AOA-T-0007 signal-first-gate-promotion

## Adaptation points

Project overlays should add:
- local generator tools
- domain-specific invariants
- rules for when property-based checks are mandatory, optional, or out of scope
