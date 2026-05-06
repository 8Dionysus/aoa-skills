# Sixth wave

Wave 6 adds the governed runtime layer above the raw wave-4 seam.

The raw seam still exists.
What changes now is that activation can be wrapped in three quiet controls that matter for local and semi-local runtimes:

1. trust-gate repo-scoped skills
2. allow read-only access to bundled skill resources without per-file permission friction
3. protect activated skill context from compaction drift and duplicate reinjection

## Why this wave exists

The earlier waves exported skills cleanly, added trigger evals, and built a dedicated runtime seam.

What remained too soft was governance at the moment of use.
A local wrapper could already discover and activate a skill. But without a trust check, a repository could inject behavior by merely existing. Without a path allowlist, every bundled resource became a speed bump. Without context guarding, the skill could silently evaporate mid-run.

## Main additions

- `scripts/build_runtime_guardrails.py`
- `scripts/skill_runtime_guardrails.py`
- `generated/repo_trust_gate_manifest.json`
- `generated/permission_allowlist_manifest.json`
- `generated/skill_context_guard_manifest.json`
- `generated/runtime_guardrail_tool_schemas.json`
- `generated/runtime_guardrail_prompt_blocks.json`
- `generated/runtime_guardrail_manifest.json`
- `config/runtime_guardrail_policy.json`
- examples for trust stores, merged allowlists, and governed runtime config
- wave-6 tests and CI drift coverage

## Design stance

- `scripts/skill_runtime_seam.py` remains the raw activation seam.
- `scripts/skill_runtime_guardrails.py` is the governed seam for local-friendly adapters.
- Trust is enforced at repo scope, not at skill-content scope.
- Allowlists stay read-only and do not eagerly read bundled resources.
- Compaction protection uses durable packets and dedupe keys instead of blind reinjection.
- The governed seam does not invent a new skill format. It wraps the existing Codex-facing export.
- This wave does not pull wave-5 orchestration canon back into `aoa-skills`.
