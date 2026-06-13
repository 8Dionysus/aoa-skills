---
name: aoa-eval-apply
scope: core
status: scaffold
summary: Run or route an already selected eval, validator, test, or script, then report what the evidence proves and what remains unproven.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-0003
  - AOA-T-0007
  - AOA-T-0096
---

# aoa-eval-apply

## Intent

Use this skill to apply an existing eval surface after selection is clear. The
output is an evidence report, not a proof promotion.

## Trigger boundary

Use this skill when:
- an existing eval, validator, test, or script has already been selected
- a local or central evaluation command should be run or routed
- the user needs to know what the run proves, what failed, and what remains
  outside coverage
- generated outputs need to be rebuilt or checked as part of the selected eval

Do not use this skill when:
- no existing eval has been selected yet; use `aoa-eval-select`
- the next honest move is to record missing eval pressure; use
  `aoa-eval-local-need`
- the task is to invent a new suite; use `aoa-eval-design`
- the command would mutate production or central proof surfaces without owner
  permission

## Inputs

- selected eval or validation command
- repo-local route law and command prerequisites
- expected artifacts, reports, generated outputs, and pass/fail criteria
- prior failure or regression context

## Outputs

- commands run and results observed
- artifacts or reports produced
- evidence classification: green proof, regression, inconclusive, blocked, or
  outside coverage
- next route if failure should become an intake need or suite design

## Procedure

1. confirm the selected eval surface and owner repo
2. inspect prerequisites and choose the smallest command that exercises the
   intended evidence surface
3. run deterministic local checks before subjective review when possible
4. capture outputs, generated drift, and artifact paths
5. classify what the run proves and explicitly name what it does not prove
6. if the run exposes missing coverage, route to `aoa-eval-local-need`
7. if the run requires new design, route to `aoa-eval-design`
8. report commands, results, artifacts, and remaining risk

## Contracts

- applying an eval does not create a central verdict unless `aoa-evals` owns and
  validates that promotion
- failed or inconclusive runs are evidence, not permission to guess
- generated drift must be resolved through owner builders
- local eval reports must stay under local repo surfaces unless central review
  accepts them

## Risks and anti-patterns

- running a broad release gate when a focused validator is enough
- treating green tests as complete proof outside their scope
- hiding generated drift
- promoting failure observations without a reproducible command

## Verification

- confirm the selected eval existed before running
- confirm command, cwd, and result
- confirm artifacts and generated drift status
- confirm proof limits and next route
- confirm no central proof file was written through MCP

## Technique traceability

Manifest-backed techniques:
- AOA-T-0003 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/proof/evaluation-chain/contract-first-smoke-summary/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0007 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/proof/evaluation-chain/signal-first-gate-promotion/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0096 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/proof/owner-truth-closeout/pinned-validation-matrix-before-generated-publish/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

- repo-local command runner
- report artifact format
- generated rebuild order
