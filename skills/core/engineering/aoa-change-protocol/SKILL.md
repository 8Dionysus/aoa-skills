---
name: aoa-change-protocol
scope: core
status: canonical
summary: Bounded workflow for a local coding agent to read the owner route, plan a scoped change, verify it explicitly, and report it clearly, while deferring approval classification and manual project overlays to their explicit owners.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-0001
  - AOA-T-0002
---

# aoa-change-protocol

## Intent

Ground non-trivial changes in the owner route before editing, then keep the diff reviewable and explicitly verified without hidden scope expansion.

## Trigger boundary

Use this skill when:
- the change affects code, config, docs, or operational surfaces in a meaningful way
- the task benefits from an explicit plan and verification path
- the task touches more than a trivial wording fix
- the request references previous work, sibling repositories, root surfaces, mechanics, generated outputs, or owner boundaries that must be inspected before planning

Do not use this skill when:
- the edit is tiny and has no meaningful review or operational consequence
- a more specific risk skill should be used instead
- the task is only to classify whether a production or sensitive action is allowed; keep the explicit-only approval-gate owner unloaded and require a deliberate manual route
- a project-specific manual overlay is the semantic owner; do not substitute the generic base workflow or load the overlay implicitly

## Inputs

- target goal
- owner repository or route surface
- touched files or surfaces
- source-of-truth or route-law surfaces that constrain the change
- optional prior-session evidence when the request asks how this repository,
  tool, MCP, hook, validator, failure, or change pattern behaved before,
  preferably as a compact usage-chain packet when the question is about usage,
  outcomes, consequences, recurrence, or nearby errors for a stable anchor
- main risk
- intended validation path
- rollback idea

## Outputs

- explicit plan
- scoped change
- named verification result
- post-change route review when source-of-truth, generated, decision, roadmap, changelog, quest, mechanic, or owner surfaces may have moved
- concise final report

## Procedure

1. choose the owner repository and read the nearest route card, `AGENTS.md`, source-of-truth surfaces, and local validation path before planning
2. before treating the generic workflow as selected, check whether the task is
   only approval classification or whether a manual project overlay owns the
   repo-relative route. In either case, keep the explicit owner unloaded,
   report the deliberate manual route, and stop this generic procedure
3. state the goal, touched surfaces, and evidence already inspected; if the request depends on prior work, inspect the current repo state rather than relying on memory
4. when prior-session behavior matters for risk, speed, or recurrence, use
   `aoa-session-memory-evidence-route` or an equivalent read-only
   `aoa-session-memory-mcp` packet; for a stable skill/MCP/hook/tool/script/test
   anchor, ask for `usage-chain` first when the question is how it was used,
   what happened after, or which failures/consequences followed; use
   `entity-dossier` when source identity, graph/cooccurrence/timeline context,
   related entities, or a heavier human packet is needed; expand to usage
   audit, neighborhood, literal, graph, goal, or answer routes only when the
   first packet is stale, truncated, missing refs, or too coarse; use the result
   as route evidence only
5. identify the main risk, owner boundary, and rollback or recovery shape before editing
6. prepare the smallest reviewable change that follows the current source route
7. avoid unrelated cleanup, opportunistic refactors, or importing a sibling owner's authority into the local surface
8. apply the change inside the declared scope
9. run or name explicit verification, including generated/export rebuilds when source surfaces feed derived outputs
10. perform the narrow post-change route review only for surfaces whose meaning actually moved
11. report what changed, what was verified, what was skipped, what remains risky, and where the next owner route is

## Contracts

- the change must remain reviewable
- verification must be explicit, not implied
- the change should stay inside the declared scope
- rollback thinking should exist before apply
- the plan should be grounded in inspected source surfaces, not only conversation memory or generic pattern recall
- generated, exported, compact, or derived surfaces should be refreshed from source rather than hand-authored as truth
- prior-session evidence can shape risk and route choice, but it does not
  override current owner files, validators, or live runtime state
- cross-repo or mechanics changes should name owner boundaries and stop-lines before moving content

## Risks and anti-patterns

- over-formalizing trivial edits
- symbolic verification that creates false safety
- using the report as a substitute for a readable diff
- silently expanding the task during implementation
- planning from stale memory when the repository already has route cards, mechanics, or source-of-truth docs that answer the question
- treating legacy, provenance, generated, or sibling-owner surfaces as if they were the active local contract
- inserting broad law blocks into local surfaces instead of shaping the change through the existing route

## Verification

- confirm the owner route and relevant source surfaces were inspected before apply
- confirm approval-classification and manual project-overlay tasks were not
  absorbed by the generic workflow or used to load an explicit owner implicitly
- confirm the change stayed scoped
- confirm at least one explicit verification step was run or intentionally skipped with explanation
- if prior-session evidence was used, confirm the usage-chain, dossier, or
  fallback route packet refs were named and current source/runtime evidence
  still controlled the change
- confirm generated or export surfaces were rebuilt when canonical inputs changed
- confirm the post-change route review touched only surfaces whose meaning moved
- confirm the report includes outcome, rollback thinking, skipped checks, and remaining owner-route risk

## Technique traceability

Manifest-backed techniques:
- AOA-T-0001 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/execution/agent-workflows-core/plan-diff-apply-verify-report/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/instruction/docs-boundary/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

Project overlays should add:
- local source-of-truth files
- local validation commands
- local risk tiers
- approval or review rules
- local post-change route review surfaces such as changelog, roadmap, decision records, generated indexes, questbooks, or mechanics ledgers
