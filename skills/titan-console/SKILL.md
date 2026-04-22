---
name: titan-console
scope: project
status: scaffold
summary: Open or maintain a visible Titan operator-console state while keeping Forge and Delta locked until approvals exist.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-TITAN-GATE-DISCIPLINE
  - AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
---

# titan-console

## Intent

Use this skill to create, inspect, or update an operator-visible Titan console state.

## Trigger boundary

Use this skill when:
- the operator wants a visible Titan lane dashboard
- console state must show active, locked, or gated lanes
- approvals and digests need local console tracking

Do not use this skill when:
- the console would become role truth
- Forge or Delta would unlock without explicit approval
- the console would silently launch app-server work

## Inputs

- workspace root
- console state path
- receipt path
- operator intent
- lane updates or approval refs

## Outputs

- console state summary
- lane status table
- approval gate status
- digest candidate
- blocked-action notes

## Procedure

1. load or initialize console state
2. show Atlas, Sentinel, Mneme, Forge, and Delta lanes
3. keep Forge and Delta locked until matching approvals
4. record visible events and digest notes
5. return state and next explicit action

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
