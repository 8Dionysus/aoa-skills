---
name: atm10-change-protocol
description: 'Explicit activation required: do not invoke or load this skill from an implicit match; wait for explicit user or operator invocation or a source-authorized parent-route selection. Apply the aoa-change-protocol workflow inside an atm10-* repository using repo-relative route cards, public docs, commands, checks, recovery anchors, and explicit local approval notes. Use when the base change protocol is correct but a thin project overlay is needed for ATM10-local command, source-of-truth, validation, or safety posture. Do not use when the base skill is sufficient without local adaptation, when document authority is the only question, or when a broader playbook is needed.'
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: project
  aoa_status: evaluated
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/project/atm10/atm10-change-protocol/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0001,AOA-T-0002
  aoa_portable_profile: codex-facing-wave-3
---

# atm10-change-protocol

## Intent
Use this skill to adapt `aoa-change-protocol` to an `atm10-*` repository without changing the base workflow meaning or moving ATM10 runtime authority into `aoa-skills`.

## Trigger boundary
Use this skill when:
- the base `aoa-change-protocol` workflow is already correct, but an `atm10-*` repo needs repo-relative paths, commands, or local approval notes
- a bounded non-trivial change still needs an explicit plan and verification path inside the local repo
- a contributor needs a thin local overlay rather than a fresh workflow design
- the change touches ATM10 public docs, scripts, schemas, source modules, tests, or workflow files and the nearest route cards must be read before editing
- a local validation tier, smoke command, dry-run posture, or recovery anchor must be named without widening the base workflow
- the family review doc and bundle-local checklist still need to stay aligned

Do not use this skill when:
- the task really needs a broader playbook or scenario bundle rather than a thin overlay
- the work would introduce new upstream technique meaning instead of adapting the local repo surface
- a more specific risk skill is still the clearer fit, such as `aoa-dry-run-first`, `aoa-safe-infra-change`, or `aoa-approval-gate-check`
- the task does not need repo-relative local adaptation and the base skill can be used directly
- the work would change live input events, operator automation authority, perception truth, retrieval/KAG truth, model-host posture, or service exposure without downstream ATM10-owned approval
- the request is only to clarify which ATM10 document owns a rule before any change plan exists; use `atm10-source-of-truth-check`

## Inputs
- target goal and touched local surface
- ATM10 route stack such as `AGENTS.md`, nearest nested `AGENTS.md`, `docs/SOURCE_OF_TRUTH.md`, `docs/RUNBOOK.md`, `docs/PRODUCT_EDGE_POSTURE.md`, or the exact touched local surface
- repo-relative source-of-truth files, generated/export companions, docs, scripts, schemas, tests, or workflow files
- repo-relative commands or checks, including whether they are full pytest, public-doc hardening, a script smoke, or a no-run explained check
- local approval or review rules
- local dry-run, report-only, rollback, or recovery posture
- base skill reference

## Outputs
- bounded local change plan
- route-card and source-of-truth evidence inspected
- repo-relative command or path sketch with the smallest honest verification tier
- explicit stop-line for downstream authority, operator safety, service exposure, or host-specific assumptions
- rollback or recovery anchor for the touched ATM10 surface
- pointer to the family review surface
- verification note for the local repo surface
- concise handoff on what stays downstream and explicit

## Procedure
1. start from `aoa-change-protocol` rather than rewriting the workflow
2. read the ATM10 root route card, then the nearest nested `AGENTS.md` for every touched path
3. when docs or public posture may move, read `docs/SOURCE_OF_TRUTH.md`; when runnable commands may move, read `docs/RUNBOOK.md`; when support claims or test tiers may move, read `docs/PRODUCT_EDGE_POSTURE.md`
4. classify the touched surface as docs, scripts, source, schemas, tests, workflow, generated/export, or operator/runtime-adjacent
5. name the repo-relative files, commands, review posture, and approval boundary that matter locally
6. keep the adaptation bounded to the local repo surface under change and preserve the base `plan -> scoped change -> verify -> report` shape
7. choose the smallest honest validation path, such as full `python -m pytest`, public-doc hardening tests, a script smoke, or an explicitly skipped check with reason
8. keep safe automation dry-run or report-only by default unless ATM10-owned docs, implementation, tests, and maintainer approval explicitly support a stronger path
9. name the rollback or recovery anchor before applying the change
10. report what changed, which local authority stayed downstream, what was verified, what was not verified, and where the next ATM10 owner route is

## Contracts
- preserve the base skill meaning
- keep paths and commands repo-relative
- keep local authority explicit
- keep the overlay reviewable and public-safe
- keep ATM10 owner truth in ATM10-owned route cards, docs, scripts, schemas, tests, and runtime artifacts
- keep generated, compact, exported, or installed surfaces weaker than the authored source they summarize
- keep dry-run/report-only behavior as the default for automation and policy surfaces unless downstream evidence says otherwise
- keep Windows 11 and PowerShell 7 command posture visible when the touched surface is operator-facing

## Risks and anti-patterns
- hiding downstream authority inside vague local notes
- turning a thin overlay into repo doctrine or a scenario bundle
- naming local commands without enough verification context
- silently changing the base workflow instead of adapting it
- treating `aoa-skills` as owner of ATM10 perception, KAG, retrieval, service, voice, operator-panel, or safe-automation runtime truth
- turning public-safe examples into private workstation paths, private run logs, local model paths, hostnames, tokens, or hidden local defaults
- using a generated report, run artifact, or installed skill export as the authoritative source for a change
- bypassing source-of-truth clarification when the real uncertainty is document authority rather than change execution

## Verification
- confirm the base skill is still the correct workflow
- confirm repo-relative paths and commands are named explicitly
- confirm the relevant ATM10 route cards and source-of-truth surfaces were inspected
- confirm approval posture is still downstream and explicit
- confirm the adaptation remains bounded to the local repo surface
- confirm the selected validation tier matches the touched surface and any skipped check is named
- confirm dry-run/report-only safety was preserved or the stronger posture is explicitly backed by ATM10-owned evidence
- confirm rollback or recovery posture is named for the touched surface
- confirm the family review doc and bundle-local checklist stay aligned

## Technique traceability
Manifest-backed techniques:
- AOA-T-0001 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/execution/agent-workflows-core/plan-diff-apply-verify-report/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/instruction/docs-boundary/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points
- repo-relative change surfaces
- local commands and verification steps
- local source-of-truth files
- local approval or review notes
- local stop-lines for operator safety, service exposure, model-host posture, and runtime-adjacent changes
- rollback, recovery, and artifact posture for ATM10-owned surfaces
- family review doc and bundle-local review checklist
