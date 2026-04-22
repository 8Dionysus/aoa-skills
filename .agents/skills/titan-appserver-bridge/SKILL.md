---
name: titan-appserver-bridge
description: Operate the Titan app-server bridge as inspectable thread, turn, event, approval, replay, and metrics state without hidden execution. Use when a Titan service-cohort route needs this explicit bounded step. Do not use for hidden background agents, silent mutation, unreviewed proof sovereignty, or memory canonization without owner confirmation.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: project
  aoa_status: scaffold
  aoa_invocation_mode: explicit-only
  aoa_source_skill_path: skills/titan-appserver-bridge/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-PENDING-TITAN-GATE-DISCIPLINE,AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
  aoa_portable_profile: codex-facing-wave-3
---

# titan-appserver-bridge

## Intent
Use this skill to prepare or inspect the Titan app-server bridge while keeping Codex execution visible and gated.

## Trigger boundary
Use this skill when:
- a Titan console needs a JSON-RPC shaped bridge
- thread and turn events need normalization
- approvals, replay, or metrics need one bounded bridge state

Do not use this skill when:
- the request asks for hidden background agents
- the bridge would execute Codex without an operator-visible plan
- role truth or memory truth would be moved into the bridge

## Inputs
- workspace root
- bridge state path
- thread and turn identifiers
- event payloads or launch plan request
- approval and receipt refs

## Outputs
- bridge plan or state summary
- normalized event candidates
- approval queue status
- replay or metrics summary
- explicit non-execution note

## Procedure
1. confirm bridge purpose and non-execution posture
2. bind inputs to thread and turn
3. normalize incoming events
4. route approval items to the approval loom
5. return replayable state and metrics without launching hidden work

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
