---
name: titan-runtime-gate
scope: project
status: scaffold
summary: Activate Forge mutation or Delta judgment lanes only through matching explicit runtime gates on a Titan receipt.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-TITAN-GATE-DISCIPLINE
  - AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
---

# titan-runtime-gate

## Intent

Use this skill when a Titan session needs to activate Forge or Delta from locked to gated state.

## Trigger boundary

Use this skill when:
- Forge needs a mutation gate
- Delta needs a judgment gate
- a receipt must record lane activation before proceeding

Do not use this skill when:
- Atlas, Sentinel, or Mneme are being gated unnecessarily
- Forge is requested with judgment or Delta with mutation
- the receipt does not exist

## Inputs

- receipt path
- requested Titan
- gate kind
- intent text
- operator approval ref

## Outputs

- updated gate state
- allowed or blocked decision
- receipt event
- lane summary
- next validation step

## Procedure

1. confirm receipt exists
2. confirm requested Titan is Forge or Delta
3. confirm gate kind matches the Titan
4. record the gate event
5. return the updated roster state

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
