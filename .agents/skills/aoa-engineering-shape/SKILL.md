---
name: aoa-engineering-shape
description: An implicit match may suggest this skill, but must not load or execute it until explicit invocation or a source-authorized parent-route selection. Shape one software responsibility boundary through bounded-context, core-boundary, or port-adapter mode. Use when responsibilities, reusable rules, orchestration, or concrete dependencies are entangled and a small owner-aware boundary is needed before implementation. Do not use for source-authority lookup, ordinary edits, test design, or a boundary that is already clear.
license: Apache-2.0
compatibility: Designed for Codex or a compatible coding-agent host with repository file access and an interactive shell. Network access is optional and owner-specific tools are never assumed.
metadata:
  aoa_scope: core
  aoa_status: reviewed
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/core/engineering/aoa-engineering-shape/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_portable_profile: codex-facing-v2
---

# aoa-engineering-shape

## Intent
Choose one shaping lens and return the smallest boundary that improves ownership
and changeability without installing an architecture framework by default.

## Trigger boundary
Use this skill when:

- domain responsibilities are overloaded, stable rules are mixed with glue, or
  a concrete dependency leaks across a meaningful seam

Do not use this skill when:

- the real task is source authority, decision history, verification, an
  ordinary edit, or implementation after the boundary is already explicit

## Inputs
- target system or code slice, owner surfaces, current responsibilities
- concrete ambiguity, repeated rule, or leaking dependency

## Outputs
- exactly one mode result with boundary, interfaces, owner, migration edge,
  verification need, unresolved question, and stop line

## Procedure
### Mode selection

| Mode | Select when | Output center |
|---|---|---|
| `contexts` | Meanings, responsibilities, or owner domains are overloaded. | Context map and interfaces. |
| `core` | Stable rules are mixed with loading, rendering, orchestration, or infrastructure. | Reusable rule center and edge responsibilities. |
| `port-adapter` | A concrete database, API, filesystem, CLI, or provider leaks inward. | Purpose-shaped port and adapter contracts. |

Select one mode. If two are necessary, finish the upstream boundary first and
hand its output to a later task-local node.

### Mode: contexts

1. Name contexts by responsibility rather than directory or team label.
2. For each, state owner truth, inputs, outputs, and what it must not own.
3. Trace interfaces and identify one real responsibility leak or unresolved
   ownership edge. Do not invent hierarchy where a typed relation is enough.

### Mode: core

1. Identify the stable rule or data transformation that survives delivery
   mechanisms.
2. Keep source loading, policy selection, orchestration, persistence, rendering,
   and transport at explicit edges.
3. Propose the smallest extraction and compatibility projection; do not freeze
   an incidental current representation as the domain model.

### Mode: port-adapter

1. Define a purpose-shaped port from the consumer need, including inputs,
   outputs, errors, fallback, limits, and observability.
2. Place concrete implementations behind adapters and keep policy choices at
   the composition root.
3. Name parity and failure checks, including how degraded or truncated behavior
   remains visible instead of silently changing semantics.

## Contracts
- owner facts remain with their owner; this bundle supplies procedure only
- one primary responsibility center; cross-relations stay explicit
- errors, fallback, and limits are part of a port contract, not hidden adapter
  behavior
- a proposed boundary is not accepted architecture until its owner adopts it

## Risks and anti-patterns
- generic clean-architecture diagrams without exact local responsibilities
- making directories, frameworks, or current technique names the semantic core
- creating a port with no consumer or a context map for a spelling fix

## Verification
- confirm the selected mode matches the actual pressure
- cite the local responsibility/rule/dependency that motivated the boundary
- state migration compatibility, what remains unresolved, and what this result
  does not authorize

Stop after one reviewable boundary and next-owner question. Do not implement or
multiply abstractions unless the request separately authorizes that effect.

## Adaptation points
Owners provide local vocabulary, interfaces, compatibility windows, and
validation commands. Those facts remain owner data, not forks of this skill.
