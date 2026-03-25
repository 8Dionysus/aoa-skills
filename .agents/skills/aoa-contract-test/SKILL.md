---
name: aoa-contract-test
description: Design or extend contract-oriented validation at module, service, or workflow boundaries. Use when two components interact across a meaningful interface, downstream assumptions matter, or a smoke path needs an explicit contract. Do not use for purely local changes or when the real need is invariant or property testing instead of boundary validation.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: core
  aoa_status: canonical
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/aoa-contract-test/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0003,AOA-T-0015
  aoa_portable_profile: codex-facing-wave-2
---

# aoa-contract-test

## Intent
Strengthen boundary reliability by making expected inputs, outputs, and validation summaries explicit.

## Trigger boundary
Use this skill when:
- two modules or services interact across a meaningful boundary
- a smoke path or interface needs a stable validation contract
- a change risks breaking downstream assumptions

Do not use this skill when:
- the change is entirely local and does not affect a meaningful boundary
- the boundary itself is still semantically unclear and naming is drifting; use `aoa-bounded-context-map`
- the main problem is expressing a broad invariant rather than a boundary contract; use `aoa-property-invariants`
- the main problem is auditing whether existing checks really cover a stable rule; use `aoa-invariant-coverage-audit`
- a broad system rewrite is needed before the boundary itself is stable

## Inputs
- boundary under review
- expected inputs and outputs
- current verification surface
- known downstream dependencies

## Outputs
- explicit contract assumptions
- tests or smoke summary changes
- verification notes
- downstream impact notes

## Procedure
1. identify the boundary and its consumers
2. state the expected input/output behavior
3. express the contract in tests, smoke summaries, or structured checks
4. verify both the boundary behavior and the reporting shape
5. report what became explicit and what remains weak

## Contracts
- the contract should be visible to another human or agent
- verification should be tied to the boundary, not only to internals
- downstream assumptions should be named when relevant

## Risks and anti-patterns
- vague contracts that do not actually constrain behavior
- treating a smoke summary as proof when it does not cover the real boundary
- changing interface behavior without downstream impact notes

## Verification
- confirm the contract is visible and reviewable
- confirm validation is tied to the interface or boundary
- confirm downstream impact was considered when relevant

## Technique traceability
Manifest-backed techniques:
- AOA-T-0003 from `8Dionysus/aoa-techniques` at `609693c2782510e0811ba7ecb4904bc06cf40c38` using path `techniques/evaluation/contract-first-smoke-summary/TECHNIQUE.md` and sections: Intent, When to use, Outputs, Contracts, Validation
- AOA-T-0015 from `8Dionysus/aoa-techniques` at `609693c2782510e0811ba7ecb4904bc06cf40c38` using path `techniques/evaluation/contract-test-design/TECHNIQUE.md` and sections: Intent, Inputs, Core procedure, Risks

## Adaptation points
Project overlays should add:
- local endpoints or module boundaries
- local smoke or test commands
- boundary-specific invariants
