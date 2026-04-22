---
name: titan-approval-ledger
scope: project
status: scaffold
summary: Record explicit operator approval for Forge mutation or Delta judgment gates without treating approval records as owner truth.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-TITAN-GATE-DISCIPLINE
  - AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
---

# titan-approval-ledger

## Intent

Use this skill to record an explicit Titan approval decision for a bounded Forge mutation or Delta judgment gate.

## Trigger boundary

Use this skill when:
- an operator has approved a named Forge or Delta gate
- the approval must be attached to a receipt, console ledger, or bridge ledger
- the next step needs visible approval evidence before execution continues

Do not use this skill when:
- the request has no explicit operator approval
- the action is not tied to a Titan receipt or ledger
- approval is being inferred from silence or convenience

## Inputs

- receipt or ledger reference
- approved Titan lane
- gate kind
- operator intent text
- scope and validation expectation

## Outputs

- approval record candidate
- gate kind and target lane
- source refs for the receipt or ledger
- stop note when the approval is missing or ambiguous

## Procedure

1. confirm the approval is explicit
2. bind the approval to the receipt or bridge ledger
3. confirm Forge uses mutation and Delta uses judgment
4. record scope, target, and validation expectation
5. return the approval record and any stop lines

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
