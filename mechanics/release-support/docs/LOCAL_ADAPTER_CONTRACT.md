# Local adapter contract around the portable export

This document defines the smallest adapter seam for runtimes that want to consume `aoa-skills` without implementing native skill discovery.
It sits alongside the dedicated-tool runtime seam and remains the backward-compatible path for older wrappers.

## Discovery

Use `generated/local_adapter_manifest.min.json` as the compact discovery surface.

Each entry gives:

- `name`
- `description`
- `path`
- `allow_implicit_invocation`
- `trust_posture`

This is enough for a local router or preselector to choose which skill to activate.

## Activation

Primary runtime wrappers should prefer the guarded runtime owner, with an
explicit trust store and activation payload. Raw/debug wrappers may use the raw
runtime seam when trust-policy behavior is intentionally outside the inspection
scope. Legacy wrappers may continue through compatibility activation ingress
while downstream callers migrate.

`RUNTIME_GOVERNANCE_LAYER.md` owns the exact governed operation map.

The activation payload returns:

- skill metadata
- invocation mode
- `allow_implicit_invocation`
- `agents/openai.yaml` content
- bundled resource inventory
- allowlist paths
- `runtime_contract`
- `context_retention`
- `trust_policy`
- the full markdown instructions body

The legacy activation payload is now backed by the governed seam, so it stays compatible while sharing the same generated contracts and export root.
For `aoa-dry-run-first`, `aoa-safe-infra-change`, and `aoa-local-stack-bringup`, the bundled resource inventory now also includes deterministic helper scripts, bounded references, and structured templates or schemas mirrored from canonical `skills/**/{scripts,references,assets}`.

## Policy rules

Adapters must respect `allow_implicit_invocation`.

- if `true`, a local runtime may auto-select the skill when the prompt matches
- if `false`, the runtime must require explicit user or router intent before activation

Do not silently relax this policy in downstream wrappers.

## Resource access

Allow trust-gated activation first, then allowlist the activated skill directory so bundled `scripts/`, `references/`, and `assets/` can be read without extra prompts.

The trust-store hint lives at `.aoa/repo-trust-store.json`.
The allowlist root for each activated skill is emitted in the activation payload and repeated in `generated/local_adapter_manifest.json`.
`scripts/skill_runtime_guardrails.py` owns resolution of the merged read-only
allowlist paths for active skills.

## Context rules

Once a skill is activated:

- keep the activation payload stable through the task
- avoid re-injecting the same skill repeatedly
- do not drop the active skill during context compaction unless the task clearly moved away from it
- prefer `context_retention` and `runtime_contract` over ad hoc wrapper notes

For long-running local agents, prefer the governed `status`, `compact`, and
`rehydrate` operations instead of maintaining parallel compaction notes outside
the repo-owned seam. `RUNTIME_GOVERNANCE_LAYER.md` owns their invocation.

## Intended layering

The local adapter is a wrapper around `.agents/skills`.
It is not a replacement format.
