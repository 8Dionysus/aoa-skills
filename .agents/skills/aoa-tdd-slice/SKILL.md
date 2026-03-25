---
name: aoa-tdd-slice
description: Implement a bounded feature slice through test-first discipline, minimal implementation, and explicit refactor boundaries. Use when a behavior change can be specified in tests before code and confidence or regression resistance matters. Do not use for undefined exploratory work, one-off glue, or broader architectural restructuring.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: core
  aoa_status: canonical
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/aoa-tdd-slice/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0014,AOA-T-0001
  aoa_portable_profile: codex-facing-wave-3
---

# aoa-tdd-slice

## Intent
Use test-first discipline to implement a small feature slice with a clear behavioral target and explicit verification.

## Trigger boundary
Use this skill when:
- a behavior change can be expressed as tests before implementation
- the task fits a bounded slice rather than a broad rewrite
- confidence and regression resistance matter

Do not use this skill when:
- the task is purely exploratory and behavior is still undefined
- the task is mostly one-off glue with no reusable logic
- the main problem is a stable interface or boundary contract rather than a feature slice; use `aoa-contract-test`
- the main problem is invariant coverage rather than slice implementation; use `aoa-property-invariants`
- broader architectural restructuring is the real need

## Inputs
- desired behavior
- target module or slice
- constraints and non-goals
- available test surface

## Outputs
- new or updated tests
- minimal implementation
- small refactor if needed
- verification summary

## Procedure
1. define the desired behavior in a bounded way
2. add or update tests before implementation
3. make the smallest change that satisfies the tests
4. refactor only inside the declared slice
5. run the tests and record the result
6. report what behavior is now specified and what remains out of scope

## Contracts
- behavior should be made explicit before implementation when reasonably possible
- the implementation should stay bounded to the slice
- unrelated refactors should be avoided
- tests should express behavior, not incidental implementation detail

## Risks and anti-patterns
- writing tests that merely mirror the implementation
- turning a small slice into a hidden architectural rewrite
- using TDD ritualistically where the problem is not well-shaped yet
- overfitting tests to brittle internal details

## Verification
- confirm tests were added or updated first when the task was suitable for TDD
- confirm the implementation stayed bounded
- confirm the relevant test suite passed
- confirm the report names the covered behavior and the untouched behavior

## Technique traceability
Manifest-backed techniques:
- AOA-T-0014 from `8Dionysus/aoa-techniques` at `609693c2782510e0811ba7ecb4904bc06cf40c38` using path `techniques/agent-workflows/tdd-slice/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0001 from `8Dionysus/aoa-techniques` at `609693c2782510e0811ba7ecb4904bc06cf40c38` using path `techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md` and sections: Contracts, Validation

## Adaptation points
Project overlays should add:
- local test commands
- local module boundaries
- guidance for when TDD is mandatory versus optional
