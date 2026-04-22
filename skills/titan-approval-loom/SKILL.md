---
name: titan-approval-loom
scope: project
status: scaffold
summary: Maintain the app-server bridge approval queue while preserving Forge and Delta gates, receipts, and visible operator intent.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-TITAN-GATE-DISCIPLINE
  - AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
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

1. load the bridge state or event source
2. match the approval request to thread and turn
3. confirm the operator decision is explicit
4. preserve Forge and Delta gate requirements
5. record the approval event and replay path

## Contracts

- The skill is explicit-only and must not be invoked as hidden background behavior.
- Titan receipts, bridge ledgers, console state, and memory records are witnesses, not final owner truth.
- Forge mutation and Delta judgment gates must remain distinct and visible.
- Owner-repo validation and human judgment remain stronger than the local skill output.

## Risks and anti-patterns

- treating Titan vocabulary as permission to widen authority
- letting receipt or replay state replace owner-repo evidence
- auto-approving Forge or Delta because a plan looks plausible
- canonizing candidate memory without source-owned confirmation

## Verification

- confirm the request and outputs stayed inside the declared Titan lane
- confirm any mutation or judgment gate was explicit and recorded
- confirm source refs, receipt refs, or ledger refs are preserved when available
- confirm the result names stop lines and remaining owner validation needs

## Technique traceability

Pending Titan workflow techniques:
- AOA-T-PENDING-TITAN-GATE-DISCIPLINE
- AOA-T-PENDING-TITAN-RECEIPT-LINEAGE

## Adaptation points

- Replace pending technique refs with published aoa-techniques refs after the Titan workflow techniques are promoted.
- Keep repo-local command examples in owner docs or examples rather than hard-coding them into the skill law.
- If a Titan surface graduates from scaffold to reviewed, add review evidence before changing status.
