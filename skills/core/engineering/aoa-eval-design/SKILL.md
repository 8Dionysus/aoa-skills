---
name: aoa-eval-design
scope: core
status: scaffold
summary: Design a local eval suite or report after selection fails, using deterministic checks first and leaving central proof acceptance to aoa-evals.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-0015
  - AOA-T-0017
  - AOA-T-0007
---

# aoa-eval-design

## Intent

Use this skill to design a bounded local eval suite, prompt set, report, or
validator plan after existing surfaces have been inspected and found
insufficient.

## Trigger boundary

Use this skill when:
- a local eval needs design from a clear failure mode or missing invariant
- deterministic tests, validators, or scripts should be planned before rubric or
  transcript graders
- positive, negative, collision, or regression cases need to be shaped for a
  local repo
- the output is a draft suite or report, not central proof acceptance
- the parent has classified design after selection, but the explicit invariant
  or behavior, target repository, local owner path, or rejected existing
  surfaces is unavailable inside the active evidence boundary; select this
  child only to stop with `blocked_missing_input` rather than design generically

Do not use this skill when:
- an existing eval should simply run now
- the right next artifact is only an intake pressure packet
- the invariant is unknown and discovery is still needed
- the user asks for central `aoa-evals` proof doctrine changes

## Inputs

- selected failure mode, target behavior, invariant, or trigger boundary
- local repo tests, scripts, validators, fixtures, generated surfaces, and
  `evals/` port
- evidence refs and rejected existing evals
- central `aoa-evals` standards when relevant

## Outputs

- draft suite structure, report plan, fixture set, or validator design
- positive, negative, and regression cases
- deterministic checks first, rubric or trace review only when needed
- proof limit and owner handoff

## Procedure

1. if the design route is selected but the explicit invariant or behavior,
   target repository, local owner path, or rejected existing surfaces is
   unavailable inside the active evidence boundary and no permitted packet or
   source read can supply it, stop with `blocked_missing_input`; do not relabel
   missing input as `deferred_owner_boundary`
2. restate the behavior or invariant to evaluate
3. choose the lowest-level deterministic checks that can constrain it
4. add positive and negative examples; add collision cases for trigger or router
   behavior
5. add trace or rubric review only where deterministic checks cannot cover the
   behavior
6. place the draft in the local eval port or report surface named by the repo
7. keep central acceptance language out of the draft
8. hand off to `aoa-eval-apply` when a runnable check exists

## Contracts

- design starts after selection fails, not before
- local design remains local until central review accepts it
- deterministic checks are preferred for coding-agent behavior
- transcript and rubric grading are supporting layers when objective checks are
  insufficient
- missing design context inside the active evidence boundary ends as
  `blocked_missing_input`, not as a generic draft or owner-boundary deferral

## Risks and anti-patterns

- designing a suite around vague success criteria
- using only positive examples
- creating rubric-only evals where a script or test can check the behavior
- making one local report sound like system-wide proof
- relabelling absent design inputs as `deferred_owner_boundary`

## Verification

- confirm the target invariant or behavior is explicit
- confirm positive, negative, and regression cases exist or are deliberately
  deferred
- confirm deterministic checks were considered first
- confirm local owner path and proof limit
- confirm absent design inputs stopped as `blocked_missing_input` without being
  relabelled as `deferred_owner_boundary`
- confirm next runnable command or review route

## Technique traceability

Manifest-backed techniques:
- AOA-T-0015 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/proof/skill-support/contract-test-design/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0017 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/proof/skill-support/property-invariants/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0007 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/proof/evaluation-chain/signal-first-gate-promotion/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

- local fixture format
- local suite/report naming
- central review handoff
