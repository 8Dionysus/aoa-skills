---
name: titan-thread-turn-binding
description: Bind Titan bridge events, approvals, and replay state to explicit thread and turn ids for inspectable continuity. Use when a Titan service-cohort route needs this explicit bounded step. Do not use for hidden background agents, silent mutation, unreviewed proof sovereignty, or memory canonization without owner confirmation.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: project
  aoa_status: scaffold
  aoa_invocation_mode: explicit-only
  aoa_source_skill_path: skills/titan-thread-turn-binding/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-PENDING-TITAN-GATE-DISCIPLINE,AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
  aoa_portable_profile: codex-facing-wave-3
---

# titan-thread-turn-binding

## Intent
Use this skill to attach Titan bridge events and approvals to a specific thread and turn boundary.

## Trigger boundary
Use this skill when:
- events need a thread-turn identity
- approval or digest state must be scoped to one turn
- replay needs stable continuity keys

Do not use this skill when:
- thread or turn identifiers are missing
- the binding would collapse multiple sessions into one record
- binding would grant execution authority by itself

## Inputs
- thread id
- turn id
- event ids or payloads
- receipt ref
- bridge or console state path

## Outputs
- thread-turn binding record
- scoped event list
- approval refs
- replay key
- continuity warning

## Procedure
1. validate thread and turn identifiers
2. attach events and approvals to the binding
3. preserve receipt and source refs
4. reject ambiguous cross-session merges
5. return replayable binding state

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
