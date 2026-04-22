---
name: titan-event-replay
scope: project
status: scaffold
summary: Replay Titan bridge or console events into inspectable state without granting runtime authority to the replay result.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-TITAN-GATE-DISCIPLINE
  - AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
---

# titan-event-replay

## Intent

Use this skill to replay Titan event logs and compare the resulting state to current bridge or console state.

## Trigger boundary

Use this skill when:
- bridge state must be reconstructed from events
- a digest or approval queue needs replay evidence
- metrics or closeout need traceable event order

Do not use this skill when:
- events are missing source refs
- replay output would be treated as proof or memory canon
- replay would mutate state without an explicit write target

## Inputs

- event log path
- optional current state path
- thread or turn filter
- receipt ref
- expected replay target

## Outputs

- replayed state summary
- event order report
- differences from current state
- authority warning
- next verification step

## Procedure

1. load events in ledger order
2. filter by thread or turn when requested
3. reconstruct lane, approval, and digest state
4. compare with current state when provided
5. return replay evidence and limits

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
