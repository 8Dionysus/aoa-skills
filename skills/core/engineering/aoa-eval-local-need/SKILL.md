---
name: aoa-eval-local-need
scope: core
status: scaffold
summary: Create a repo-local eval need packet when no existing eval fits, preserving owner route, evidence, rejected alternatives, and proof limits.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-0076
  - AOA-T-0094
  - AOA-T-0105
---

# aoa-eval-local-need

## Intent

Use this skill to record bounded local eval pressure under a repository's
`evals/intake/` surface after selection confirms that no existing eval fits.

## Trigger boundary

Use this skill when:
- a local repository needs an eval pressure packet but not a central proof
  bundle yet
- no existing local validator, test, script, or central eval bundle covers the
  failure or behavior
- a repeated session or implementation failure needs owner-routed follow-up
- the right next artifact is `evals/intake/*.eval_need.json`

Do not use this skill when:
- an existing eval can be applied now
- the missing object is a memory candidate, decision record, or source-truth map
- the target repo has no local eval port and no owner permission to create one
- the user asks for central `aoa-evals` proof acceptance

## Inputs

- target repository and local `evals/PORT.yaml`
- failure or behavior needing evaluation
- evidence refs, touched paths, expected invariant, and rejected existing
  surfaces
- owner route and validation commands

## Outputs

- one repo-local eval need packet under `evals/intake/`
- no central proof verdict
- named next review or design route
- validation result for the local port shape when available

## Procedure

1. verify that `aoa-eval-select` or equivalent inspection found no adequate
   existing surface
2. read local eval-port rules and confirm `evals/intake/` is the right write
   surface
3. write one bounded need packet with target behavior, evidence refs, owner
   route, rejected alternatives, proposed checks, and proof limits
4. avoid central `aoa-evals/evals/**` writes
5. run the local eval-port validator if available
6. report the packet path, owner route, and next review route

## Contracts

- local intake is pressure, not acceptance
- central proof promotion requires `aoa-evals` review
- packets must name rejected alternatives so later agents do not repeat the same
  search
- raw session refs must remain candidate evidence until reviewed

## Risks and anti-patterns

- using `candidates/` or another ad hoc directory when `intake/` is the local
  port route
- creating many broad packets instead of one bounded need
- omitting rejected existing evals
- smuggling central verdict language into local intake

## Verification

- confirm no existing eval fit
- confirm the target repo owns the local port
- confirm packet path and schema posture
- confirm evidence refs and proof limits
- confirm central proof surfaces were not changed

## Technique traceability

Manifest-backed techniques:
- AOA-T-0076 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/governance/decision-routing/owner-layer-triage/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0094 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/proof/owner-truth-closeout/canonical-owner-with-validated-mirror/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0105 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/proof/review-evidence/single-missing-evidence-request/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

- eval need schema
- local intake filename convention
- local-port validator command
