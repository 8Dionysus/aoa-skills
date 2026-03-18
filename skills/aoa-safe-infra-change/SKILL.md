---
name: aoa-safe-infra-change
scope: risk
status: scaffold
summary: Make bounded infrastructure or configuration changes with explicit risk framing, verification, and reversible execution discipline.
invocation_mode: explicit-only
technique_dependencies: []
---

# aoa-safe-infra-change

## Intent

Use this skill to shape infrastructure, service, configuration, or operational changes into a safer bounded workflow.

## Trigger boundary

Use this skill when:
- the task changes infrastructure, services, configuration, orchestration, or operational surfaces
- the change has runtime, safety, or deployment implications
- the task needs stronger verification and rollback thinking than a normal code edit

Do not use this skill when:
- the task is a purely local code change with no operational implications
- a more specific risk skill should be used instead
- the operator has not provided enough authority for the requested action

## Inputs

- target change
- touched operational surfaces
- stated authority or approval state
- validation path
- rollback idea

## Outputs

- explicit risk-aware plan
- bounded infrastructure or config change
- verification result
- report with remaining risk notes

## Procedure

1. identify the operational surface and main risk
2. confirm whether the change belongs to a high-risk or explicit-only category
3. keep the change small and reviewable
4. avoid unrelated cleanup or hidden expansion of scope
5. verify the result using the strongest practical bounded checks available
6. report what changed, what was verified, and what remains risky or deferred

## Contracts

- infrastructure changes should stay explicit and reviewable
- risk should be named before apply, not after failure
- verification should be stronger than symbolic confidence
- rollback thinking should exist before execution

## Risks and anti-patterns

- treating infra edits like ordinary code edits
- making broad config or orchestration changes under a narrow task label
- relying on weak verification for changes with real runtime impact
- skipping explicit risk framing because the diff looks small

## Verification

- confirm the operational surface was named clearly
- confirm the change stayed bounded
- confirm verification was explicit and proportional to the risk
- confirm the report includes unresolved risk or recovery notes

## Future traceability

Technique linkage is intentionally deferred for this scaffold.
Later revisions may connect this skill to reusable techniques in `aoa-techniques`.

## Adaptation points

Future project overlays may add:
- local risk classifications
- approval rules
- preferred validation commands
- rollback or recovery expectations
