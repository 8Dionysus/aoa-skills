# Local adapter contract around the Codex-facing export

This document defines the smallest adapter seam for runtimes that want to consume `aoa-skills` without implementing native Codex skill discovery.

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

Use:

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

This gives local runtimes a dedicated tool seam instead of requiring direct file reading in the model loop.

## Policy rules

Adapters must respect `allow_implicit_invocation`.

- if `true`, a local runtime may auto-select the skill when the prompt matches
- if `false`, the runtime must require explicit user or router intent before activation

Do not silently relax this policy in downstream wrappers.

## Resource access

Allowlist the activated skill directory so bundled `scripts/`, `references/`, and `assets/` can be read without extra prompts.

The allowlist root for each activated skill is emitted in the activation payload and repeated in `generated/local_adapter_manifest.json`.

## Context rules

Once a skill is activated:

- keep the activation payload stable through the task
- avoid re-injecting the same skill repeatedly
- do not drop the active skill during context compaction unless the task clearly moved away from it
- prefer `context_retention` and `runtime_contract` over ad hoc wrapper notes

## Intended layering

The local adapter is a wrapper around `.agents/skills`.
It is not a replacement format.
