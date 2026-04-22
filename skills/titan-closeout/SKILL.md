---
name: titan-closeout
scope: project
status: scaffold
summary: Close a Titan service-cohort session with role, risk, provenance, gate, verification, and next-owner summary.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-TITAN-GATE-DISCIPLINE
  - AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
---

# titan-closeout

## Intent

Use this skill at the end of a Titan service-cohort session to close the local receipt without claiming final owner truth.

## Trigger boundary

Use this skill when:
- a Titan receipt is ready to close
- Atlas, Sentinel, and Mneme posture needs one summary
- Forge or Delta gates were used and need visible closeout

Do not use this skill when:
- the session has no receipt
- closeout would replace owner-repo validation
- memory candidates are being promoted without owner confirmation

## Inputs

- receipt path
- operator summary
- gates used
- validation evidence
- memory candidates and owner-route hints

## Outputs

- closed receipt or closeout packet
- role and boundary summary
- gate summary
- verification status
- next owner-repo action

## Procedure

1. validate the receipt exists
2. summarize Atlas route, Sentinel risk, and Mneme provenance
3. include Forge and Delta only when gated
4. record verification state honestly
5. return next owner route without canonizing memory

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
