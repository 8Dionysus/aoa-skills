---
name: atm10-source-of-truth-check
description: 'Explicit activation required: do not invoke or load this skill from an implicit match; wait for explicit user or operator invocation or a source-authorized parent-route selection. Apply the aoa-source-of-truth-check workflow inside an atm10-* repository using repo-relative public-surface roles, document maps, canonical-file patterns, entrypoint trimming, and local review posture. Use when contributors need a thin project overlay to identify authoritative ATM10 docs or separate active, archived, generated, local-only, and runtime-adjacent surfaces. Do not use when the task is broader policy design, purely code-local, runtime authority, or better handled by the base skill without local adaptation.'
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: project
  aoa_status: evaluated
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/project/atm10/atm10-source-of-truth-check/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0013,AOA-T-0002,AOA-T-0009
  aoa_portable_profile: codex-facing-wave-3
---

# atm10-source-of-truth-check

## Intent
Use this skill to adapt `aoa-source-of-truth-check` to an `atm10-*` repository when the base workflow is right but the local public-doc and repo-surface map needs repo-relative detail.

## Trigger boundary
Use this skill when:
- the base `aoa-source-of-truth-check` workflow is already correct, but an `atm10-*` repo needs local canonical-file patterns, repo-relative docs, or doc review rules
- contributors need a thin overlay that maps repo-relative docs such as `README.md`, `docs/ARCHITECTURE.md`, or `docs/[canonical-guide].md`
- confusion exists between overview docs and authoritative files inside one local repo
- active commands, archived commands, public status, support-profile claims, runtime baseline notes, release posture, or local-only planning surfaces are being mixed
- a top-level ATM10 entrypoint is accumulating runbook-scale detail that should move to a canonical home
- a public-safe local route must distinguish tracked docs from ignored maintainer scratch, internal chronology, private logs, or tool-local config
- the family review doc and bundle-local checklist still need to stay aligned

Do not use this skill when:
- the main need is broader policy design rather than local document authority mapping
- the task is purely code-local and has no meaningful docs or guidance ambiguity
- the work would introduce new upstream technique meaning instead of thin local adaptation
- the main need is recording rationale for a decision rather than clarifying authority; use `aoa-adr-write`
- the authoritative files are already clear and the remaining work is an ordinary bounded change; use `atm10-change-protocol` or the base `aoa-change-protocol`
- the question belongs to ATM10 runtime behavior, perception truth, model-host selection, operator automation, or private local state rather than document authority

## Inputs
- repo-relative docs or guidance surfaces
- local canonical-file candidates
- local review rules for doc changes
- contributor confusion points
- ATM10 public-surface roles from `docs/SOURCE_OF_TRUTH.md`
- affected active, archived, generated/export, local-only, internal, or runtime-adjacent surfaces
- candidate validation path such as public-doc hardening tests, nested AGENTS checks, or a no-run review note
- base skill reference

## Outputs
- local source-of-truth map
- active/current versus archived, generated/export, local-only, internal, or runtime-adjacent placement map
- bounded clarification note
- repo-relative canonical-file pattern
- lightweight entrypoint guidance when a summary doc should route outward instead of duplicating commands or counters
- pointer to the family review surface
- verification summary for the local docs surface

## Procedure
1. start from `aoa-source-of-truth-check` instead of inventing a family-specific docs doctrine
2. read the ATM10 root route card and `docs/SOURCE_OF_TRUTH.md`; if a touched path has a nested `AGENTS.md`, read that before judging local authority
3. name the repo-relative docs, source/config/schema surfaces, generated/export companions, run artifacts, or local-only surfaces involved in the ambiguity
4. map each local concern to the smallest authoritative home, such as `MANIFEST.md` for public current state, `ROADMAP.md` for direction, `docs/RUNBOOK.md` for active runnable commands, `docs/ARCHIVED_TRACKS.md` for archived/recoverable command references, `docs/PRODUCT_EDGE_POSTURE.md` for support/test-tier claims, `docs/QWEN3_MODEL_STACK.md` for model/runtime baseline posture, or `docs/SOURCE_OF_TRUTH.md` for document-role rules
5. keep `README.md` and other entrypoints short and link-driven once the canonical home exists
6. separate tracked public docs from ignored local-only planning, internal chronology, private logs, host-specific paths, tokens, and tool-local config
7. keep the adaptation bounded to the local repo surface under review
8. make explicit what still depends on downstream human review, unpublished local policy, or ATM10-owned runtime evidence
9. verify that the clarification reduces ambiguity without making `aoa-skills` the authority for ATM10 behavior

## Contracts
- preserve the base skill meaning
- keep local file maps repo-relative and explicit
- surface local authority and review posture without hiding it
- keep the overlay public-safe and reviewable
- keep ATM10 source-of-truth claims inside ATM10-owned public docs and route cards
- keep active runbook content separate from archived or recoverable references
- keep generated, exported, installed, and run-artifact surfaces weaker than the authored files they summarize
- keep public support-profile claims no broader than the docs and test tiers that actually validate them
- keep private workstation paths, local model paths, private logs, hostnames, tokens, screenshots with sensitive details, and internal scratch out of public examples

## Risks and anti-patterns
- inventing a broader docs governance framework inside a thin overlay
- using family labels without reducing local ambiguity
- hiding local review rules in prose that looks canonical
- silently replacing the base skill with project doctrine
- treating `README.md`, generated outputs, run artifacts, or installed skills as the source of truth when ATM10 already has canonical docs
- mixing active commands with archived/recoverable references
- spreading release cadence, supported profiles, or test-tier claims across several docs when one canonical surface owns them
- turning ignored local-only planning or internal chronology into public truth
- using this overlay to make runtime, service, model, operator automation, or perception decisions that belong in ATM10-owned implementation and docs

## Verification
- confirm the base skill is still the right workflow
- confirm authoritative repo-relative files are named explicitly
- confirm local review posture is visible rather than implied
- confirm the adaptation reduces ambiguity without widening scope
- confirm active, archived, generated/export, local-only, internal, and runtime-adjacent surfaces are not collapsed into one role
- confirm entrypoint docs stay short and route to canonical homes where those exist
- confirm public-safe boundaries and private/local-only exclusions are preserved
- confirm any support-profile, release, or runtime-baseline wording points to the owning ATM10 surface
- confirm the family review doc and bundle-local checklist stay aligned

## Technique traceability
Manifest-backed techniques:
- AOA-T-0013 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/instruction/instruction-surface/single-source-rule-distribution/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/instruction/docs-boundary/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0009 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/instruction/docs-boundary/lightweight-status-snapshot/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points
- local doc hierarchies
- repo-relative canonical-file patterns
- local review rules for doc changes
- repository-specific authority examples
- lightweight entrypoint rules for `README.md`, `MANIFEST.md`, and other summary docs
- active versus archived command placement
- public-safe exclusions for internal scratch, private logs, host-specific paths, and tool-local config
- family review doc and bundle-local review checklist
