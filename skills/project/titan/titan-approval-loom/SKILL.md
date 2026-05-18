---
name: titan-approval-loom
scope: project
status: scaffold
summary: Maintain the app-server bridge approval queue while preserving Forge and Delta gates, receipts, and visible operator intent.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-0028
  - AOA-T-0045
  - AOA-T-0062
---

# titan-approval-loom

## Intent

Use this skill to inspect, add, or resolve approval-queue items for the Titan app-server bridge.

## Trigger boundary

Use this skill when:
- a bridge turn contains pending approvals
- operator intent must be matched to a queued action
- approval state must be replayable from ledger events

Do not use this skill when:
- an action should be auto-approved
- approval would bypass Forge or Delta gates
- the queue item has no receipt or thread-turn context

## Inputs

- bridge state path
- thread id and turn id
- approval request id
- operator decision
- receipt or event refs

## Outputs

- updated approval queue entry
- decision event candidate
- gate status summary
- blocked-action note when approval is insufficient

## Procedure

1. load the current bridge approval queue and receipt refs
2. separate pending, allowed, blocked, and expired approval entries
3. bind each approval to Forge or Delta without merging the gates
4. preserve replayable evidence for operator intent and queue state changes
5. return the next visible queue action without starting hidden execution

## Contracts

- The skill is explicit-only and must not be invoked as hidden background behavior.
- Titan role, helper/control-plane, runtime implementation, memory, proof, and public-runbook authority stays in owner repositories: aoa-agents, aoa-sdk, abyss-stack, aoa-memo, aoa-evals, and 8Dionysus.
- Receipts, bridge ledgers, console state, replay artifacts, approval records, and memory records are witnesses or candidates, not final owner truth.
- Forge mutation and Delta judgment gates must remain distinct, operator-visible, and receipt-linked.
- Missing source refs, missing approval, missing validation, or unclear owner route must be named as stop conditions.

## Risks and anti-patterns

- treating Titan vocabulary as permission to widen authority
- letting receipt, replay, console, or bridge state replace owner-repo evidence
- auto-approving Forge or Delta because a plan looks plausible
- promoting candidate memory, approvals, replay, or receipts into canon without owner review
- using the skill for an ordinary repo task that has no explicit Titan route

## Verification

- confirm direct skill invocation or explicit Titan service-cohort request is present
- confirm lane, gate, source refs, and owner surface are named when relevant
- confirm Forge or Delta locked or allowed state matches recorded approval evidence
- confirm generated artifacts are marked witness, candidate, derived, or advisory rather than final truth
- confirm next validation, replay, repair, or owner-route follow-up is named before continuation

## Technique traceability

Manifest-backed techniques:
- AOA-T-0028 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/execution/agent-workflows-core/confirmation-gated-mutating-action/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Validation
- AOA-T-0045 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/history/history-artifacts/witness-trace-as-reviewable-artifact/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0062 from `8Dionysus/aoa-techniques` at `fe4b04ed877916c46e60e70aaa9a1d4c86e81b6e` using path `techniques/continuity/handoff-continuation/episode-bounded-agent-loop/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

- Extract a Titan-specific reusable technique into aoa-techniques only after repeated reviewed evidence exists; do not add pending IDs as placeholders.
- Keep repo-local command examples in owner docs or examples rather than hard-coding them into skill law.
- If a Titan surface graduates from scaffold to reviewed or evaluated, add review evidence before changing status.
