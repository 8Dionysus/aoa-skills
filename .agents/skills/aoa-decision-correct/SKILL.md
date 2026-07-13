---
name: aoa-decision-correct
description: 'Explicit activation required: do not invoke or load this skill from an implicit match; wait for explicit user or operator invocation or a source-authorized parent-route selection. Correct, supersede, reindex, or repair graph-coverage drift in AoA decision records by checking graph issues, editing source notes first, rebuilding repo-local indexes, and refreshing the workspace decision graph. Use when a decision note, index metadata, source-surface list, status, supersession, generated index, unknown surface, or graph packet is stale or wrong. When the parent has classified correction but the target decision record, owning source note, repo-local index contract, or graph/owner packet is unavailable inside the active evidence boundary, stop with blocked_missing_input; do not relabel missing input as deferred_owner_boundary. Do not use for pure lookup or for creating a new decision note.'
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: core
  aoa_status: evaluated
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/core/engineering/aoa-decision-correct/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0001,AOA-T-0033,AOA-T-0002
  aoa_portable_profile: codex-facing-wave-3
---

# aoa-decision-correct

## Intent
Use this skill to repair an existing decision record, its index metadata,
supersession links, source-surface list, or generated decision indexes without
letting the workspace graph become the authority.

## Trigger boundary
Use this skill when:
- a decision record is stale, incomplete, misindexed, wrongly sourced, or needs supersession
- generated decision indexes are out of date with source metadata
- graph lookup shows a mismatch that must be verified against the source note
- a correction must preserve local decision-lane law and validation
- the parent has classified a correction route, but the target decision record,
  owning source note, repo-local index contract, or graph/owner packet is
  unavailable inside the active evidence boundary; select this child only to
  stop with `blocked_missing_input` rather than invent correction context

Do not use this skill when:
- the task is only to find relevant rationale; use `aoa-decision-find`
- a new durable decision is required instead; use `aoa-decision-create`
- the source surface itself is wrong and no decision-lane change is needed
- a generated graph or index can be refreshed without source-note drift
- the correction would rewrite history instead of adding an explicit supersession or status change

## Inputs
- target decision ID, path, source surface, stale index, or graph mismatch
- `aoa_decisions` status, issues, decision, changed-path, source-surface,
  owner-surface, or repo packet for the target record when available
- repo-local decision route card, template, source note, and generated indexes
- source files changed by the correction when relevant
- validation commands for decision indexes and affected surfaces

## Outputs
- corrected source decision note or explicit no-change finding
- regenerated repo-local decision indexes when metadata changed
- refreshed or checked workspace graph
- clear report of old mismatch, correction, validation, and any remaining risk

## Procedure
1. if the correction route is selected but the target decision record, owning
   source note, repo-local index contract, or graph/owner packet is unavailable
   inside the active evidence boundary and no permitted packet or source read
   can supply it, stop with `blocked_missing_input`; do not relabel missing
   input as `deferred_owner_boundary`
2. use `aoa_decisions` status and issues first, then fetch the target decision,
   changed-path, source-surface, owner-surface, or repo packet when available
3. if graph issues exist for the target repo, classify whether the fix belongs
   to the source note, local index contract, workspace graph registry, or cache refresh
4. read the source decision note before editing anything
5. read the repo-local decision route card and generated index contract
6. classify the correction as metadata, source-surface list, status,
   supersession, typo-only, or generated-index drift
7. edit the source note first; use explicit supersession or status language for
   semantic changes instead of silent history rewrite
8. regenerate repo-local decision indexes when metadata or source-record shape changed
9. run the repo-local decision validator/check and any affected surface validator
10. refresh or check the workspace graph, run the decision-graph lane when available,
   and compare the corrected graph packet
11. report whether the graph, source note, and local indexes are now aligned

## Contracts
- source notes are edited before generated indexes or graph cache
- generated graph/cache refresh cannot be used to hide source drift
- semantic corrections must preserve reviewable history through status or supersession
- typo-only fixes should not inflate into new rationale
- validation must cover the owner repo, not only the workspace graph
- graph issue packets are triage inputs; they do not replace source-note or
  local-contract inspection
- missing required correction context inside the active evidence boundary ends
  as `blocked_missing_input`, not as an owner-boundary deferral

## Risks and anti-patterns
- fixing only generated indexes while leaving source metadata wrong
- changing meaning silently without status or supersession
- broad rewriting because a small metadata fix was requested
- trusting a stale graph packet after editing source files
- applying another repo's metadata vocabulary where it does not fit
- clearing cache freshness while leaving an unknown decision-lane surface unmodeled
- relabelling absent correction inputs as `deferred_owner_boundary`

## Verification
- confirm the source note was inspected and, if needed, edited
- confirm generated indexes were regenerated only from source metadata
- confirm repo-local decision checks passed or failures are explicit
- confirm absent correction inputs stopped as `blocked_missing_input` without
  being relabelled as `deferred_owner_boundary`
- confirm workspace graph refresh/check and decision-graph lane see the corrected state
- confirm semantic rewrites are avoided or made explicit through supersession/status

## Technique traceability
Manifest-backed techniques:
- AOA-T-0001 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/execution/agent-workflows-core/plan-diff-apply-verify-report/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0033 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/instruction/docs-boundary/decision-rationale-recording/TECHNIQUE.md` and sections: Intent, When to use, When not to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/instruction/docs-boundary/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points
- repo-specific supersession/status vocabulary
- repo-local generated index commands
- decision validator and affected surface validator
- MCP refresh command or graph fallback
