# Phased skill plan

This document records the scaffold expansion that established the current 13-skill public core.
It is now primarily a phase record rather than the main source of next-step planning.

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

## What landed after the scaffold pass

After the initial scaffold expansion, the repository also gained:
- honest `techniques.yaml` coverage across the current skill surface
- first examples or review checklists for all current skills
- a local validator for bundle shape, policy coherence, and `SKILL_INDEX.md` coverage

## What remains intentionally deferred

Deferred for later passes:
- schema-backed contracts and pinned upstream traceability
- build-time refresh tooling for skill composition
- autonomy and evaluation harnesses beyond shape validation
- formal maturity decisions and promotion criteria
- project-specific overlays after the public core is harder

## Expected next steps

1. add schema-backed contracts for `SKILL.md`, `techniques.yaml`, and `agents/openai.yaml`
2. add pinned traceability and refresh helpers for `SKILL.md`
3. introduce autonomy checks, prompt fixtures, and trigger-boundary evaluation
4. define a formal maturity ladder and promotion criteria
5. add thin project overlays only after the public core is harder
