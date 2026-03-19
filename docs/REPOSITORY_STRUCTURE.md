# Repository structure

## Top level

- `README.md` — project entry point
- `SKILL_INDEX.md` — public map of current skills and their maturity
- `docs/` — architecture, bridge rules, roadmap, conventions
- `docs/reviews/` — public review records for candidate and promotion work
- `docs/reviews/canonical-candidates/` — canonical-candidate review records
- `docs/reviews/status-promotions/` — review records for non-canonical promotion steps
- `templates/` — templates for authoring skills and related files
- `skills/` — skill bundles
- `scripts/` — optional generation or validation helpers
- `schemas/` — optional machine-readable schemas

## Skill bundle shape

Each skill lives in:

`skills/<skill-name>/`

Recommended contents:

- `SKILL.md` — main Codex-facing runtime skill document
- `techniques.yaml` — bridge manifest that records which techniques shape the skill
- `agents/openai.yaml` — optional invocation and policy settings
- `references/` — optional reference docs or excerpts
- `examples/` — optional example prompts, outputs, or mini scenarios
- `checks/` — optional review checklist or validation notes

## Initial naming convention

Use one of these prefixes:
- `aoa-` for public core skills
- `atm10-` for project-family skills around `atm10-agent`
- `abyss-` for project-family skills around `abyss-stack`

Examples:
- `aoa-change-protocol`
- `aoa-tdd-slice`
- `aoa-contract-test`
- `atm10-perception-tests`
- `abyss-port-exposure-guard`

## Files that belong in the skill

Belong in `SKILL.md`:
- intent for the agent
- trigger boundary
- expected inputs
- expected outputs
- concrete step-by-step procedure
- explicit anti-patterns
- done criteria or verification guidance

Belong in `techniques.yaml`:
- upstream technique IDs
- source paths and pinned source refs
- selected sections
- composition notes

Belong in `agents/openai.yaml`:
- invocation mode
- policy
- future Codex-specific metadata

Belong in `docs/reviews/`:
- candidate review records
- promotion review records
- public evidence notes about repository-level review decisions

## What should not live here

- private secrets
- environment-specific sensitive paths
- one-off hacks that were not generalized
- techniques that should live in `aoa-techniques`
- project runtime state or logs
