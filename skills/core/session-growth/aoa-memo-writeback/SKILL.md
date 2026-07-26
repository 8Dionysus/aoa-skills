---
name: aoa-memo-writeback
description: "First memo writeback before any memo artifact exists; read this SKILL.md from its host-listed path only. Decide whether live-session, closeout, landed-work, PR, diff, or review evidence yields one guarded candidate, export, or no-write result. If a constructed path already failed before any other action, recover exactly once from the host locator and report `package_path_recovered`; never search or probe. If an existing concrete memo candidate, export, quarantine packet, memory object, corpus identity, lifecycle target, or read-model target is named or supplied, select aoa-memo directly. Do not use for eval mining, raw session maintenance, generic harvest, durable memory, owner intake/review, recall, or proof."
---

# aoa-memo-writeback

## Intent

Preserve the first writeback judgment that the previous consolidation removed:
notice when live or closing work produced a bounded lesson worth remembering,
decide its real owner, and create or route its first guarded artifact without
turning session history into memory truth.

## Trigger boundary

Use this skill when:

- a live session, closeout, PR, diff, review, release, or recurring correction
  may contain a durable owner lesson not captured by the final artifact alone,
  and no concrete memo candidate, export, or memory object exists yet
- the decision is still whether to write a local candidate, prepare an export,
  record route-only debt, request owner review, or write nothing
- the caller explicitly authorizes creation of the first guarded local
  candidate from inspectable work evidence

Do not use this skill when:

- the task is eval-trigger/session-case mining, `.aoa` preservation/index
  repair, generic session harvest, review of an existing candidate/export/
  quarantine packet/object, corpus recall or lifecycle work, direct durable
  `aoa-memo` landing, or proof/scoring work

## Inputs

- likely owner and stronger owner; task/closeout/landed-work context; inspectable
  session, source, PR, review, or receipt refs; local memo-port status; privacy,
  freshness, review posture, and confirmation that no concrete memo artifact
  already represents this writeback

## Outputs

- one `memo_writeback_decision`: `write_candidate`, `prepare_export`,
  `no_writeback_needed`, `route_only_debt`, `needs_owner_review`, or `blocked`
  or `owner_handoff`
- when authorized, one guarded owner-local candidate or reviewed export packet;
  otherwise a no-write stop line or route-only debt with inspectable refs

## Procedure

1. Before reading this bundle, inspect only the request. If it already names or
   supplies a concrete candidate, export, quarantine packet, memory object,
   corpus identity, lifecycle target, or memory read-model target, do not load
   this skill. Select `aoa-memo` directly.
2. After selection, the first tool turn must read only this bundle's
   `SKILL.md` by copying the absolute `(file: ...)` source locator appended by
   the host to this skill's catalog entry. Do not reconstruct the path from a
   presumed skill root, `.system`, `$CODEX_HOME`, the workspace, or the skill
   name. Do not combine the read with `pwd`, `AGENTS`, workspace inspection, or
   another command.

   If one constructed package path already failed with a pure not-found result
   before this body loaded and no workspace, search, or other action occurred,
   read the exact host locator next and set
   `package_path_recovered: true`. This is a degraded one-call recovery, not a
   clean package entry; report it in the result and do not claim equivalent
   routing cost. Any second miss, search, directory probe, workspace read, or
   absent/failed literal locator is `blocked_package_path_not_observed`.
3. Read `references/contract.yaml`, then `references/writeback.md`, from that
   same bundle. Do not inspect the task workspace before both are loaded.
4. Check whether the inspected evidence unexpectedly supplies a concrete candidate, export,
   quarantine packet, memory object, corpus identity, or lifecycle target. If
   it does, return `owner_handoff` to `aoa-memo` without opening owner-corpus
   surfaces or creating another artifact.
5. Name three distinct owners before judging whether the material belongs in
   memo:
   - `origin_owner` owns the source claim and local candidate;
   - `memory_intake_owner` is `aoa-memo` for reviewed intake and durable-memory
     lifecycle only;
   - `procedure_owner` is `aoa-skills` and is provenance, never the stronger
     owner of the material.
   If the caller requests `owner` and `stronger_owner`, return
   `origin_owner` and `aoa-memo` respectively, while stating that `aoa-memo`
   cannot override origin source truth.
6. Use session evidence when the meaning lived in the interaction; reconcile it
   with source/PR/review evidence without letting either silently replace the
   other.
7. Choose exactly one decision and honor its effect boundary. Candidate writing
   requires an existing admitted local `memo/` port and explicit authorization.
   Before choosing between a local candidate/review route and
   `route_only_debt`, read the exact conventional `memo/PORT.yaml` once. A
   closeout statement that a port is admitted is evidence to check, not port
   authority. Use its `owner_repo` as the repository-level `origin_owner` while
   keeping any missing exact material-source path visible.
8. Stop before durable memory landing unless the active task explicitly enters
   the `aoa-memo` reviewed-corpus owner route.

## Contracts

- `.aoa` is evidence and routing context, never reviewed memory truth
- owner-local candidate, export packet, reviewed intake, and durable memory are
  separate lifecycle states and effects
- one candidate carries one bounded memory question with source and evidence
  refs; it is not a session recap
- an existing candidate, export, object, or corpus question belongs to
  `aoa-memo`; writeback never creates a second representation to avoid review
- missing owner ports produce route-only debt, not invented directories
- technique records may explain provenance but are not runtime dependencies

## Risks and anti-patterns

- treating every commit, progress note, mood, or interesting thought as memory
- using a clean diff summary instead of the session evidence that explains why
  a correction matters
- smuggling proof, routing, runtime, role, playbook, KAG, ToS, source doctrine,
  secrets, or private raw transcript detail into memo ownership
- turning `reviewed_write` or an MCP dry run into durable authority

## Verification

- confirm owner/stronger-owner, bounded memory question, source and evidence
  refs, freshness, privacy, local-port status, chosen decision, and effect
- confirm candidate guardrails and review posture; inspect any packet manually
- after an authorized candidate write, use the file-change result and one exact
  read of that candidate as the complete effect/artifact check; do not run
  `git status`, `pwd`, `stat`, directory inspection, or another command merely
  to restate the write
- report `package_path_recovered` when the one-call not-found recovery occurred;
  keep its extra call visible instead of rewriting it as clean package entry
- report what was written, what stayed local, what was not promoted, validation
  used, and the next owner route

## Adaptation points

Owners supply memory-worthy trigger classes, local port schemas/builders,
privacy rules, export policy, reviewed-intake route, and closeout conventions.
