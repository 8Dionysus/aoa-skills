---
name: aoa-eval
description: An implicit match may suggest this skill, but must not load or execute it until explicit invocation or a source-authorized parent-route selection. Route one AoA evaluation need through select, apply, or propose mode while preserving local owner and proof-authority boundaries. Use when an existing eval/check must be found or run, or a confirmed no-fit needs an owner-local intake/design candidate. Do not use for ordinary one-off tests, undefined invariants, green-command reporting, or direct edits to central proof authority.
license: Apache-2.0
compatibility: Designed for Codex or a compatible coding-agent host with repository file access and an interactive shell. Network access is optional and owner-specific tools are never assumed.
metadata:
  aoa_scope: core
  aoa_status: reviewed
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/core/engineering/aoa-eval/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_portable_profile: codex-facing-v2
---

# aoa-eval

## Intent
Choose one evaluation lifecycle mode without treating local evidence, a healthy
Forge, or a green command as proof beyond its declared owner and invariant.

## Trigger boundary
Use this skill when:

- an eval/check must be selected or applied, or a verified no-fit needs a local
  intake/design proposal with explicit proof limits

Do not use this skill when:

- the task is an ordinary unit test, the invariant/acceptance target is unknown,
  or the request would make this skill a central proof-authority writer

## Inputs
- invariant/acceptance target, owner repo and source ref, local/central inventory
- for apply: exact selected surface, command, prerequisites, expected artifacts,
  accepted exits, pass criteria, and effect posture

## Outputs
- exactly one mode result with owner, source/environment, evidence/proof class,
  drift, artifact, next route, and stop line

## Procedure
### Mode selection

| Mode | Select when | Output |
|---|---|---|
| `select` | No exact evidence surface has been selected. | Exact/partial/no-fit choice and next route. |
| `apply` | Surface, command, and acceptance contract are already explicit. | Bounded execution result and proof limit. |
| `propose` | Selection established no adequate fit. | Owner-local intake or suite-design candidate, not proof. |

### Shared procedure

1. Read the local eval route and stronger proof-owner boundary before acting.
2. Preserve repo, source ref, model/host/tools, environment, and effect posture.
3. Run or design only the selected mode. Do not load legacy eval children.

### Mode: select

1. Inventory the narrowest owner-local and central surfaces relevant to the
   invariant.
2. Compare fit, command, prerequisites, artifact, freshness, owner, and proof
   class; reject nearest alternatives explicitly.
3. Return exact fit to `apply`, or a bounded partial/no-fit to `propose`. Do not
   execute or design during selection.

### Mode: apply

1. Refuse when exact command, source ref, accepted result, or required input is
   missing; return to `select` rather than guessing.
2. Run only named JIT owner checks and the exact selected command in its owner
   root. Do not substitute a broader green gate.
3. Inspect stdout/artifacts manually, classify drift and partial results, and
   distinguish command success from invariant satisfaction and central proof.

### Mode: propose

1. Require a recorded no-fit, stable invariant, owner home, and acceptance
   criteria. Reviewed traces may support a candidate but are never required or
   authoritative.
2. Choose the smallest owner-local intake or design packet; do not edit central
   catalogs, mint proof, or create a permanent validator merely to fill a gap.
3. State manual cases that must precede any durable suite and the owner review
   that would admit it.

## Contracts
- local evidence remains local unless a stronger owner accepts it
- Eval Forge readiness is infrastructure health, not result proof
- selection, execution, proposal, promotion, and central proof are separate
- a session-memory provider is optional candidate evidence and may be absent

## Risks and anti-patterns
- selecting by keyword, running a broad gate, or reporting exit zero as proof
- designing before no-fit/invariant/owner are known
- allowing eval machinery or generated dashboards to outrank owner sources

## Verification
- confirm one mode and exact owner/source/environment posture
- inspect artifacts/results manually against declared acceptance criteria
- state proof limit, skipped checks, drift, and next owner route

## Adaptation points
Repositories supply local eval ports, commands, artifacts, and acceptance
criteria; `aoa-evals` and Eval Forge supply only their own owner contracts.
