---
name: aoa-session-harvest
description: Convert explicitly reviewed session evidence into bounded reusable candidates through extract, classify, or branch mode. Use when a reviewed task trace contains repeatable units, an isolated unit needs its next owner/artifact route, or several continuations must remain visible. Do not use on live or unreviewed notes, for automatic promotion, or to write owner truth, quests, skills, playbooks, telemetry, or memory directly.
scope: core
status: reviewed
summary: One reviewed-evidence family for candidate extraction, lifecycle classification, and visible route branches.
invocation_mode: explicit-preferred
---

# aoa-session-harvest

## Intent

Turn reviewed experience into session-local candidates and typed handoffs while
keeping all destination owners responsible for acceptance.

## Trigger boundary

Use this skill when:

- a bounded reviewed session/evidence packet contains repeatable units, a
  candidate needs classification, or materially different next routes must be
  compared without hidden execution

Do not use this skill when:

- evidence is active, raw, unreviewed, missing its boundary, or the request asks
  for direct owner writes, automatic promotion, scheduling, or execution

## Inputs

- reviewed evidence boundary and refs; optional explicit baseline/checkpoint
- one intent: extract, classify, or branch

## Outputs

- session-local candidate/route packet with evidence posture, owner hint,
  rejected nearest target, effect `none`, and stop line

## Procedure

### Mode selection

| Mode | Select when | Output |
|---|---|---|
| `extract` | Reusable units have not yet been isolated. | Candidate units plus unresolved residue. |
| `classify` | One reviewed unit is isolated and needs a next artifact/owner verdict. | Defer/reject/propose skill, playbook, eval, memo, tool, adapter, or no artifact. |
| `branch` | Several continuations must expose gains, costs, risks, owners, and stops. | Branch cards and a non-executing default/hold option. |

### Mode: extract

1. Disposition every supplied hint before it influences a candidate.
2. Extract only reusable reviewed units; keep design pressure and unknowns as
   residue without candidate IDs.
3. Assign one primary reuse kind and owner shape, preserving cluster and evidence
   refs. Candidate refs are session-local and non-authoritative.

### Mode: classify

1. Require recurrence, stable inputs/outputs, proof posture, reversibility,
   risk, approval sensitivity, and independent composition value.
2. Compare destinations by object kind: procedure, workflow, tool, guard,
   adapter, eval, memo candidate, or no durable artifact.
3. Return only a proposal to the destination owner. A repeated unit is not
   automatically a skill, and a green result is not promotion evidence.

### Mode: branch

1. Preserve materially different routes rather than collapsing them into a
   hidden recommendation.
2. For each route state gain, cost, risk, owner, prerequisite, effect, stop, and
   handoff ABI.
3. A default is advisory. Launch, delegation, scheduling, and mutation require
   their own owner/runtime gate.

## Contracts

- reviewed evidence only; no dependency on a session-memory provider
- candidates remain session-local until an owner accepts a bounded handoff
- one primary object kind/owner hint; typed alternatives may remain visible
- extraction, classification, promotion, execution, and telemetry are separate

## Risks and anti-patterns

- mining live transcripts, universalizing one success, or minting authoritative
  IDs from a session
- treating quests, receipts, progression scores, or telemetry as procedure output
- hard-coding the next named skill instead of returning a typed handoff

## Verification

- trace every candidate claim to reviewed refs and disposition stale hints
- confirm no owner file, memory, routing, KAG, telemetry, or runtime state changed
- state rejected destinations, unresolved residue, and required owner review

## Adaptation points

Sessions supply their evidence packet and boundaries; destination owners supply
their intake contracts. Neither is copied into this skill.
