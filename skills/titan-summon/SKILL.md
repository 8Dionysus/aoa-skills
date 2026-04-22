---
name: titan-summon
scope: project
status: scaffold
summary: Begin an explicit Titan service-cohort session with Atlas, Sentinel, and Mneme active and Forge or Delta locked.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-TITAN-GATE-DISCIPLINE
  - AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
---

# titan-summon

## Intent

Use this skill to begin a Codex session with the first Titan service cohort after an explicit operator summon.

## Trigger boundary

Use this skill when:
- the operator explicitly requests the Titan cohort
- the session needs Atlas route, Sentinel risk, and Mneme provenance lanes
- Forge and Delta must remain locked until later gates

Do not use this skill when:
- the request asks for hidden background agents
- Forge should mutate before a target and validation exist
- Delta should issue final truth without bounded evidence

## Inputs

- workspace root
- summon prompt reference
- operator intent
- receipt output path
- initial route question

## Outputs

- summon receipt candidate
- active and locked roster state
- route, risk, and memory posture summary
- gate status
- next move

## Procedure

1. confirm explicit summon intent
2. use the service-cohort summon prompt
3. activate Atlas, Sentinel, and Mneme only
4. keep Forge locked until mutation intent
5. keep Delta locked until judgment intent

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
