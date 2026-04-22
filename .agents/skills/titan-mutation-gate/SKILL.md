---
name: titan-mutation-gate
description: Gate Forge workspace-write work with explicit intent, target paths, prechecks, validation, and rollback or stop posture. Use when a Titan service-cohort route needs this explicit bounded step. Do not use for hidden background agents, silent mutation, unreviewed proof sovereignty, or memory canonization without owner confirmation.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: project
  aoa_status: scaffold
  aoa_invocation_mode: explicit-only
  aoa_source_skill_path: skills/titan-mutation-gate/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-PENDING-TITAN-GATE-DISCIPLINE,AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
  aoa_portable_profile: codex-facing-wave-3
---

# titan-mutation-gate

## Intent
Use this skill before Forge performs any workspace-write or code mutation work.

## Trigger boundary
Use this skill when:
- Forge is being asked to edit files
- the mutation target and validation path need to be explicit
- Atlas, Sentinel, and Mneme prechecks must be visible before mutation

Do not use this skill when:
- the request has no explicit mutation intent
- targets or validation are unclear
- the action is destructive without approval and rollback posture

## Inputs
- intent text
- target repos and paths
- allowed actor
- precheck evidence
- validation command
- rollback or stop condition

## Outputs
- mutation gate packet
- allowed or blocked decision
- precheck summary
- validation expectation
- rollback or stop note

## Procedure
1. verify explicit mutation intent
2. verify target repo and paths
3. collect Atlas route, Sentinel risk, and Mneme provenance notes
4. confirm Forge is the allowed actor
5. record validation and rollback or stop path

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
