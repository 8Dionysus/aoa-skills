---
name: aoa-session-recovery
description: An implicit match may suggest this skill, but must not load or execute it until explicit invocation or a source-authorized parent-route selection. Diagnose recurring session or workflow failure and prepare the smallest owner-routed repair through diagnose or propose-repair mode. Use when reviewed evidence shows contamination, drift, repeated tool/route failure, or a known diagnosis needs a reversible repair packet. Do not use on one live mood note, to mutate an owner directly, or to create durable validators before repeated manual evidence establishes an invariant.
license: Apache-2.0
compatibility: Designed for Codex or a compatible coding-agent host with repository file access and an interactive shell. Network access is optional and owner-specific tools are never assumed.
metadata:
  aoa_scope: core
  aoa_status: reviewed
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/core/session-growth/aoa-session-recovery/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_portable_profile: codex-facing-v2
---

# aoa-session-recovery

## Intent
Separate symptoms, causes, and owner effects so a session can learn without
turning self-diagnosis into hidden mutation authority.

## Trigger boundary
Use this skill when:

- reviewed evidence shows repeated contamination, routing drift, tool failure,
  false confidence, or a reviewed diagnosis needs a bounded repair proposal

Do not use this skill when:

- evidence is live/unreviewed, a diagnosis already exists but only execution is
  requested, or the skill would need to mutate the target owner directly

## Inputs
- reviewed evidence packet or diagnosis with refs, target owner, constraints,
  and any current checkpoint/rollback posture

## Outputs
- exactly one diagnosis or repair-proposal packet with evidence posture, owner,
  reversibility, manual checks, uncertainty, effect `none`, and stop line

## Procedure
### Mode selection

| Mode | Select when | Output |
|---|---|---|
| `diagnose` | Symptoms are reviewed but causes/owner are not yet established. | Symptoms, causes, inference, unknowns, drift class, owner hints. |
| `propose-repair` | A reviewed diagnosis exists. | Smallest diff shape, checkpoint, rollback, checks, cleanup, handoff. |

### Mode: diagnose

1. Separate observed symptoms from confirmed causes, inference, and unknowns.
2. Seek disconfirming evidence and classify contamination, evidence-boundary,
   routing, lifecycle, ownership, or tool/runtime drift.
3. Name immediate session owner and possible durable owner separately. Propose a
   repair shape but perform no mutation and assign no blame as settled truth.

### Mode: propose-repair

1. Require a reviewed diagnosis; do not manufacture one from the repair request.
2. Define the smallest owner/target diff, execution posture, checkpoint,
   rollback, bounded retries, manual health checks, stop/escalation, and cleanup.
3. Route the proposal to the target owner. Examples or dry runs show viability,
   not execution or verification of this repair.
4. Add a durable validator only after the same stable failure invariant recurs
   and manual checks prove what it must catch.

## Contracts
- reviewed session evidence is input, not owner truth or durable memory
- diagnosis is read-only; proposal is not authorization or execution
- target owners own mutations, checks, rollback, and durable policy
- unknowns remain unknown and successful examples retain bounded claim limits

## Risks and anti-patterns
- self-confirming diagnosis, broad terrain search after missing evidence, or
  assigning owner fault from one symptom
- repairing without rollback/cleanup or using a new validator as scaffolding
- reporting a proposed or previewed repair as applied and verified

## Verification
- trace symptoms/causes or repair fields to reviewed evidence/diagnosis refs
- confirm no target owner, runtime, session archive, or provider was mutated
- state manual checks, skipped execution, remaining uncertainty, and handoff

## Adaptation points
The session supplies reviewed evidence; each target owner supplies its mutation,
checkpoint, validation, and rollback contracts.
