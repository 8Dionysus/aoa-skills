---
name: aoa-eval-select
description: 'Explicit activation required: do not invoke or load this skill from an implicit match; wait for explicit user or operator invocation or a source-authorized parent-route selection. Inspect repo-local eval ports, tests, validators, scripts, reports, intake files, and central aoa-evals standards before new eval work, then select the smallest existing surface or a no-fit route. Use when the task asks which eval should apply to a change, failure, regression, or trigger miss. When the parent has classified selection but the target repository, touched paths, local eval port, nearby proof surfaces, or central standard is unavailable inside the active evidence boundary, stop with blocked_missing_input; do not relabel missing input as deferred_owner_boundary or infer fit/no-fit. Do not use when the eval is already selected and should run, when no-fit has already been established, or when the real issue is source authority rather than eval coverage.'
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: core
  aoa_status: scaffold
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/core/engineering/aoa-eval-select/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0003,AOA-T-0076,AOA-T-0094
  aoa_portable_profile: codex-facing-wave-3
---

# aoa-eval-select

## Intent
Use this skill to find whether an existing eval, validator, test, script, report,
or local-port artifact already covers the current pressure before designing a
new eval.

## Trigger boundary
Use this skill when:
- a task asks which eval should be used for a change, failure, or regression
- a repository has a local `evals/` port and the agent needs to inspect it
  before writing anything new
- central `aoa-evals` may already contain the relevant proof pattern or local
  port contract
- existing validators, tests, or scripts may be the honest eval surface
- the parent has classified selection, but the target repository, touched
  paths, local eval port, nearby proof surfaces, or central standard is
  unavailable inside the active evidence boundary; select this child only to
  stop with `blocked_missing_input` rather than infer fit or no-fit

Do not use this skill when:
- an already selected eval simply needs to be run; use `aoa-eval-apply`
- no eval exists and the next move is a local intake packet; use
  `aoa-eval-local-need`
- the user asks for a new suite design after selection has already failed; use
  `aoa-eval-design`
- source authority rather than eval coverage is the problem

## Inputs
- target repo and touched paths
- local `evals/PORT.yaml`, `evals/README.md`, `evals/intake/`, and eval reports
- scripts, tests, validators, schemas, generated manifests, and route docs
- central `aoa-evals` docs and local-port standard
- MCP list/inspect packets when available

## Outputs
- selected existing eval, validator, test, script, or report surface
- reason the surface fits or does not fit
- owner and proof-authority classification
- next route: apply, local need, design, or stop

## Procedure
1. if the selection route is chosen but the target repository, touched paths,
   local eval port, nearby proof surfaces, or central standard is unavailable
   inside the active evidence boundary and no permitted packet or source read
   can supply it, stop with `blocked_missing_input`; do not relabel missing
   input as `deferred_owner_boundary`
2. read the target repo route law and local `evals/PORT.yaml` when present
3. inventory local `evals/`, tests, validators, and scripts around the touched
   paths
4. inspect central `aoa-evals` only for reusable proof doctrine, local-port
   standard, or central bundle matches
5. prefer deterministic local scripts and tests for coding-agent behavior when
   they already constrain the outcome
6. use MCP list/inspect only to narrow the search; verify important claims
   against source files
7. classify the result as exact fit, partial fit, nearest wrong target, no fit,
   or blocked by stale/missing owner evidence
8. hand off to `aoa-eval-apply`, `aoa-eval-local-need`, or `aoa-eval-design`
   only after selection is clear

## Contracts
- existing local proof surfaces beat new design pressure
- central proof doctrine may guide but not absorb repo-local intake
- selection reports confidence and nearest wrong target instead of guessing
- generated indexes and MCP packets are read models until source-verified
- missing selection context inside the active evidence boundary ends as
  `blocked_missing_input`, not as fit, no-fit, or owner-boundary deferral

## Risks and anti-patterns
- skipping local validators because a central eval sounds more official
- selecting a test that only checks incidental behavior
- turning a partial fit into a proof verdict
- reading all repos when touched paths already narrow the search
- relabelling absent selection inputs as `deferred_owner_boundary`

## Verification
- confirm local port presence, absence, and status
- confirm selected surface and owner route
- confirm why nearest alternatives were rejected
- confirm next route is one of apply, local need, design, or stop
- confirm absent selection inputs stopped as `blocked_missing_input` without
  being relabelled as `deferred_owner_boundary`
- confirm central `aoa-evals` was not rewritten

## Technique traceability
Manifest-backed techniques:
- AOA-T-0003 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/proof/evaluation-chain/contract-first-smoke-summary/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0076 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/governance/decision-routing/owner-layer-triage/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0094 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/proof/owner-truth-closeout/canonical-owner-with-validated-mirror/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points
- local eval-port paths
- repo-local validation command names
- central proof bundle naming
