---
name: titan-receipt
scope: project
status: scaffold
summary: Create, validate, note, or close Titan session receipts as witnesses rather than final truth.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-TITAN-GATE-DISCIPLINE
  - AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
---

# titan-receipt

## Intent

Use this skill to manage local Titan session receipts for summon, gate, note, validation, and closeout steps.

## Trigger boundary

Use this skill when:
- a Titan session needs a receipt
- an existing receipt needs validation or a note
- a gated action or closeout must be attached to receipt state

Do not use this skill when:
- receipt state would be treated as owner truth
- the receipt path is unclear
- notes would contain secrets or unreviewed claims

## Inputs

- workspace root
- operator id
- receipt path
- note or closeout summary
- gate refs or validation command

## Outputs

- created or updated receipt
- validation result
- receipt note
- closeout state
- authority warning

## Procedure

1. choose the receipt action
2. validate required fields and path
3. write or inspect only the requested receipt surface
4. preserve gates and source refs
5. return status and next owner route

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
