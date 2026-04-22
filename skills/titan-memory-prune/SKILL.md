---
name: titan-memory-prune
scope: project
status: scaffold
summary: Propose redaction, tombstone, or pruning candidates for Titan memory without silent deletion or canon rewrite.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-TITAN-GATE-DISCIPLINE
  - AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
---

# titan-memory-prune

## Intent

Use this skill to review Titan memory records for retention, masking, tombstone, or pruning proposals.

## Trigger boundary

Use this skill when:
- a Titan memory record may be stale, sensitive, or wrong
- a recall result needs redaction handling
- a bearer lineage record should preserve fall or correction without erasure

Do not use this skill when:
- the request asks for silent deletion
- the record lacks source or authority metadata
- pruning would hide an important lineage event

## Inputs

- memory record id
- source refs
- reason for prune request
- retention rule
- operator or owner confirmation state

## Outputs

- redaction proposal
- tombstone proposal
- records to keep unchanged
- reason and source refs
- stop line for missing confirmation

## Procedure

1. inspect the record and source refs
2. classify the reason for pruning
3. prefer masks or tombstones before deletion
4. preserve lineage-significant events
5. return proposals and required confirmations

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
