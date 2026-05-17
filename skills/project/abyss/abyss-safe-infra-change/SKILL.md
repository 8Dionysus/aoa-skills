---
name: abyss-safe-infra-change
scope: project
status: evaluated
summary: Thin abyss overlay for bounded infrastructure or configuration changes with repo-relative operational surfaces, explicit local authority, and reviewable risk notes.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-0028
  - AOA-T-0001
---

# abyss-safe-infra-change

## Intent

Use this skill to adapt `aoa-safe-infra-change` to an `abyss-*` repository when the base operational workflow is correct but the local repo still needs repo-relative commands, authority notes, and risk framing.

## Trigger boundary

Use this skill when:
- the base `aoa-safe-infra-change` workflow is already correct, but an `abyss-*` repo needs repo-relative operational surfaces, commands, or approval notes
- the task is a bounded infrastructure, service, configuration, or operational change inside one local repo family
- the local surface is repo-owned operational material such as a compose file, service wrapper, env or config template, bootstrap script, deployment toggle, restart rule, runtime check, or generated operational receipt
- explicit local authority, rollback posture, or verification commands still need to be named before execution
- the change needs a local preflight, preview, stop line, or recovery anchor matched to the touched surface rather than a generic safety claim
- the family review doc and bundle-local checklist still need to stay aligned

Do not use this skill when:
- the task is really about producing a shareable public-safe artifact rather than the operational change itself; use `abyss-sanitized-share`
- no `abyss-*` repo adaptation is needed and the base `aoa-safe-infra-change` skill is sufficient
- the overlay would only restate the base workflow without adding a real local surface
- the main question is whether authority exists at all; use `aoa-approval-gate-check`
- the main need is to prefer or interpret a preview path before execution; use `aoa-dry-run-first`
- the touched surface belongs to a stronger owner repo, host-level service, secret plane, or deployment environment that has not been explicitly confirmed for this change
- the work would widen into broader project doctrine instead of a thin local overlay

## Inputs

- target operational change and touched local surface
- repo-relative operational files, commands, generated receipts, or runtime check paths
- surface class, side-effect class, and expected blast radius
- explicit local authority, approval posture, and stop condition
- preflight or preview path when one exists
- validation path and rollback or recovery anchor
- sensitivity notes for raw logs, host details, secrets, or unpublished runtime data
- base skill reference

## Outputs

- bounded local infra-change plan
- repo-relative command, path, or receipt sketch
- explicit local authority, approval, stop-line, and rollback note
- surface-specific verification plan with the smallest honest proof
- note about any material that must be sanitized before sharing
- pointer to the family review surface
- concise verification note for the local repo surface

## Procedure

1. start from `aoa-safe-infra-change` instead of inventing a new project-family workflow
2. read the nearest repo route card before treating a path as locally owned
3. classify the touched surface: source config, generated operational receipt, runtime wrapper, launch command, environment template, deployment toggle, or verification script
4. name the side effect, authority posture, stop condition, and rollback or recovery anchor before proposing execution
5. choose the smallest local preflight or preview that can prove the change shape without performing a stronger mutation
6. keep commands and paths repo-relative unless the operator explicitly authorizes a host or environment path
7. preserve the base risk framing, rollback thinking, and explicit verification posture
8. make explicit what still requires downstream human approval or repo-specific judgment

## Contracts

- preserve the base skill meaning
- keep paths and commands repo-relative
- keep local authority explicit
- keep host paths, secrets, credentials, and unpublished operational details out of shareable notes unless separately sanitized
- do not convert a generated receipt or runtime artifact into source authority
- keep the overlay explicit-only, public-safe, and reviewable

## Risks and anti-patterns

- hiding downstream authority inside vague local operational notes
- turning a thin overlay into project doctrine or a scenario bundle
- naming repo-relative commands without enough verification or rollback context
- treating a dry-run, generated receipt, or log sample as proof of a live mutation that did not happen
- using an `abyss-*` label to claim authority over a sibling owner or host-level surface
- copying raw runtime data into a review note when `abyss-sanitized-share` is the correct next step
- silently changing the base workflow instead of adapting the local repo surface

## Verification

- confirm the base skill is still the correct workflow
- confirm repo-relative paths, commands, receipts, or runtime checks are named explicitly
- confirm local authority, stop condition, rollback posture, and verification remain explicit
- confirm the selected preflight or preview is proportional to the side effect
- confirm no stronger host, secret, deployment, or sibling-owner authority was implied
- confirm the adaptation stays bounded to the local repo surface
- confirm the family review doc and bundle-local checklist stay aligned

## Technique traceability

Manifest-backed techniques:
- AOA-T-0028 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/execution/agent-workflows-core/confirmation-gated-mutating-action/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0001 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/execution/agent-workflows-core/plan-diff-apply-verify-report/TECHNIQUE.md` and sections: Intent, Outputs, Contracts, Risks, Validation

## Adaptation points

- repo-relative operational surfaces
- local authority and approval notes
- local validation commands
- rollback or recovery expectations
- family review doc and bundle-local review checklist
