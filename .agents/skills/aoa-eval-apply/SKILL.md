---
name: aoa-eval-apply
description: 'Explicit activation required: do not invoke or load this skill from an implicit match; wait for explicit user or operator invocation or a source-authorized parent-route selection. Run or route an already selected eval, validator, test, or script, then report command results, artifacts, generated drift, proof limits, and next route. Use when the eval surface is already selected and the task is to apply it rather than choose or design it. Do not use when no existing eval has been selected, when an intake need should be recorded first, or when central proof promotion is being requested.'
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: core
  aoa_status: scaffold
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/core/engineering/aoa-eval-apply/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0003,AOA-T-0007,AOA-T-0096
  aoa_portable_profile: codex-facing-wave-3
---

# aoa-eval-apply

## Intent
Use this skill to apply an existing eval surface after selection is clear. The
output is an evidence report, not a proof promotion. When a selected local
suite exposes `evals/suites/<slug>.suite.json`, treat that sidecar as typed
source execution intent: it must be JIT-revalidated by the current owner before
its exact runner may execute.

## Trigger boundary
Use this skill when:
- an existing eval, validator, test, or script has already been selected
- a local or central evaluation command should be run or routed
- the user needs to know what the run proves, what failed, and what remains
  outside coverage
- generated outputs need to be rebuilt or checked as part of the selected eval
- a selected repo-local suite has a machine-readable execution sidecar whose
  freshness and runtime invocation must be applied

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
- optional `evals/suites/<slug>.suite.json` sidecar plus the current owner
  schema/validator that classifies it as absent, invalid, stale, or ready
- exact source tree or commit when the result will be merge-, release-, or
  publication-bound
- expected artifacts, reports, generated outputs, and pass/fail criteria
- prior failure or regression context

## Outputs
- commands run and results observed
- artifacts or reports produced
- evidence classification: passed candidate evidence, regression candidate,
  inconclusive, blocked, or outside coverage
- for a sidecar-backed suite: JIT state, exact invocation, environment capture,
  and owner-local execution receipt
- next route if failure should become an intake need or suite design

## Procedure
1. confirm the selected eval surface, owner repo, source root, and source ref;
   if exact merged evidence is required, use a clean exact tree without
   modifying a dirty canonical checkout
2. inspect prerequisites and choose the smallest command that exercises the
   intended evidence surface
3. if a local suite sidecar exists, use the current owner validator to
   JIT-revalidate schema, canonical owner identity, paths, typed argv, and every
   tracked source hash; proceed only from `source-contract-ready`
4. inventory, readiness, dashboard, and MCP surfaces may inspect the sidecar but
   must not execute it
5. invoke only the validated `runner.argv`, `runner.cwd`, timeout, and accepted
   exit codes; do not substitute a wrapper, broader gate, or reconstructed
   command
6. capture interpreter, dependency inventory digest, ambient pytest plugins,
   config, and selected environment before interpreting the result
7. write an owner-local, private-by-default execution receipt linked to the
   source head and sidecar digest; keep proof and promotion authority false
8. when no sidecar exists, run the selected deterministic command with the same
   source, cwd, result, artifact, and proof-limit reporting discipline
9. capture outputs, generated drift, and artifact paths
10. classify what the run proves and explicitly name what it does not prove
11. if the run exposes missing coverage, route to `aoa-eval-local-need`; if it
    requires new design, route to `aoa-eval-design`
12. report commands, results, artifacts, source posture, environment posture,
    and remaining risk

## Contracts
- applying an eval does not create a central verdict unless `aoa-evals` owns and
  validates that promotion
- `source-contract-ready` proves reviewed source shape and hashes only; runtime
  reproducibility remains false unless a stronger owner proves a pinned
  environment
- a stale or invalid sidecar blocks execution until its source owner repairs or
  refreshes it; live output cannot author its own tracked hashes
- inventory, MCP, and generated readiness surfaces never gain execution or
  receipt-publication authority from discovering a sidecar
- failed or inconclusive runs are evidence, not permission to guess
- generated drift must be resolved through owner builders
- local eval reports must stay under local repo surfaces unless central review
  accepts them

## Risks and anti-patterns
- running a broad release gate when a focused validator is enough
- treating green tests as complete proof outside their scope
- executing a sidecar from inventory/MCP output without immediate owner JIT
  validation
- changing `runner.argv`, cwd, timeout, accepted codes, or tracked hashes at run
  time to make a stale contract pass
- treating an environment capture or execution receipt as reproducible runtime,
  central proof, or promotion
- hiding generated drift
- promoting failure observations without a reproducible command

## Verification
- confirm the selected eval existed before running
- confirm source root/ref and whether the observation came from a live dirty
  workspace or an exact source tree
- for a sidecar-backed suite, confirm the owner validator reported ready
  immediately before execution and no inventory/MCP surface executed it
- confirm exact command, cwd, timeout, accepted exit codes, and result
- confirm environment capture and the private execution receipt's source-head
  and sidecar-digest links
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
