# Second wave for the Codex-facing portable layer

The first wave solved shape and portability.
The second wave solves reliability.

## Objectives

1. Make skill trigger quality testable instead of intuitive.
2. Make explicit-only policy visible in evals and local wrappers.
3. Give non-Codex runtimes a narrow seam around the Codex-facing export.
4. Keep the export generated, reviewable, and drift-checked.

## The four additions

### 1. Policy-aware trigger evals

`generated/skill_trigger_eval_cases.jsonl` moves the seed from a flat CSV into a richer JSONL schema:

- `case_id`
- `skill_name`
- `mode`
- `expected_behavior`
- `expected_skill`
- `competing_skills`
- `invocation_mode`
- `prompt`
- `note`

This matters because explicit-only skills must not be graded as if they should implicitly auto-trigger.

### 2. Collision families

`generated/skill_trigger_collision_matrix.json` adds the adjacent-skill families that are most likely to blur together:

- decision record vs source-of-truth mapping
- context mapping vs core-logic extraction vs port-adapter refactor
- bounded change vs TDD slice vs contract tests
- property authoring vs coverage audit
- approval gate vs dry run vs infra change vs local stack bringup vs sanitized share
- base skills vs ATM10 overlays

The point is not just to ask “does this skill ever trigger?”
The point is to ask “does this skill beat the right neighbors for the right reason?”

### 3. Local adapter seam

The portable export remains `.agents/skills/*`.
Local-friendly runtimes adapt around it through:

- `generated/local_adapter_manifest.json`
- `generated/local_adapter_manifest.min.json`
- `scripts/activate_skill.py`

This gives a runtime a compact discovery view first, then a structured activation payload when it needs the full skill.

### 4. Export hardening

The upgraded builder and validator add:

- resource copying from canonical `skills/<name>/{scripts,references,assets}`
- support for optional `config/openai_skill_extensions.json`
- local-adapter manifest regeneration
- policy validation against canonical invocation mode
- CI drift checks

## Integration posture

Keep these surfaces conceptually separate:

- canonical authoring
  - `skills/*/SKILL.md`
  - `generated/skill_sections.full.json`
  - `generated/skill_catalog.min.json`
- Codex-facing export
  - `.agents/skills/*`
- local adapter seam
  - `generated/local_adapter_manifest*.json`
  - `scripts/activate_skill.py`

The export stays common.
Wrappers stay downstream.
