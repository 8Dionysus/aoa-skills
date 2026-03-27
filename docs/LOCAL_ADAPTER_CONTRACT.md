# Local adapter contract around the Codex-facing export

This document defines the smallest adapter seam for runtimes that want to consume `aoa-skills` without implementing native Codex skill discovery.
It now sits alongside the wave-4 dedicated-tool runtime seam and remains the backward-compatible path for older wrappers.

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

Primary runtime wrappers should prefer:

```bash
python scripts/skill_runtime_guardrails.py activate --repo-root . --skill <skill-name> --trust-store .aoa/repo-trust-store.json --format json
```

Raw/debug runtime wrappers may still use:

```bash
python scripts/skill_runtime_seam.py activate --repo-root . --skill <skill-name> --format json
```

Legacy local wrappers may continue to use:

```bash
python scripts/activate_skill.py --repo-root . --skill <skill-name> --format json
```

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
For `aoa-dry-run-first`, `aoa-safe-infra-change`, and `aoa-local-stack-bringup`, the bundled resource inventory now also includes deterministic helper scripts, bounded references, and structured templates or schemas mirrored from canonical `skills/*/{scripts,references,assets}`.

## Policy rules

Adapters must respect `allow_implicit_invocation`.

- if `true`, a local runtime may auto-select the skill when the prompt matches
- if `false`, the runtime must require explicit user or router intent before activation

Do not silently relax this policy in downstream wrappers.

## Resource access

Allow trust-gated activation first, then allowlist the activated skill directory so bundled `scripts/`, `references/`, and `assets/` can be read without extra prompts.

The trust-store hint lives at `.aoa/repo-trust-store.json`.
The allowlist root for each activated skill is emitted in the activation payload and repeated in `generated/local_adapter_manifest.json`.
Use `python scripts/skill_runtime_guardrails.py allowlist --repo-root . --session-file .aoa/skill-runtime-session.json --format json` to resolve the merged read-only paths for active skills.

## Context rules

Once a skill is activated:

- keep the activation payload stable through the task
- avoid re-injecting the same skill repeatedly
- do not drop the active skill during context compaction unless the task clearly moved away from it
- prefer `context_retention` and `runtime_contract` over ad hoc wrapper notes

For long-running local agents, prefer the explicit governed session path in `scripts/skill_runtime_guardrails.py status|compact|rehydrate` instead of maintaining parallel compaction notes outside the repo-owned seam.

## Intended layering

The local adapter is a wrapper around `.agents/skills`.
It is not a replacement format.
