# Phased skill plan

This document records the current phased expansion plan for scaffold skills.

## Principle for this pass

In this pass, skills are added as public scaffolds.
They are intentionally not yet tightly linked to specific techniques or project overlays.
Preparation traces are acceptable.
The main goal is to prepare the repository surface and the skill vocabulary.

## Phase A: starter core skills

Already present:
- `aoa-change-protocol`
- `aoa-tdd-slice`
- `aoa-contract-test`
- `aoa-bounded-context-map`
- `aoa-property-invariants`

## Phase B: architecture and refactor scaffolds

Added in this expansion:
- `aoa-port-adapter-refactor`
- `aoa-core-logic-boundary`
- `aoa-adr-write`
- `aoa-source-of-truth-check`

## Phase C: risk and ops scaffolds

Added in this expansion:
- `aoa-safe-infra-change`
- `aoa-approval-gate-check`
- `aoa-dry-run-first`
- `aoa-sanitized-share`

## What is intentionally deferred

Deferred for later passes:
- hard linkage to published techniques
- project-specific overlays
- stronger examples and checks
- canonical versus promoted maturity decisions
- generation or refresh tooling for skill composition

## Expected next steps

1. review the new scaffolds for naming and scope quality
2. keep `SKILL_INDEX.md` and docs surface aligned as scaffold skills land
3. publish missing techniques in `aoa-techniques`
4. replace placeholders and add technique traceability where it becomes real
5. add examples, checks, and thin project overlays only after the public core becomes stable
