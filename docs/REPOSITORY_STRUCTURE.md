# Repository structure

## Top level

- `README.md` — project entry point
- `SKILL_INDEX.md` — public map of current skills and their maturity
- `docs/` — architecture, bridge rules, roadmap, conventions
- `docs/RUNTIME_PATH.md` — main runtime guide for `pick -> inspect -> expand -> object use`
- `docs/PUBLIC_SURFACE.md` — public guide to the current governance and product-signaling layer
- `docs/PROMOTION_PATH.md` — public repository convention for maturity transitions
- `docs/reviews/` — public review records for candidate and promotion work
- `docs/reviews/canonical-candidates/` — canonical-candidate review records
- `docs/reviews/status-promotions/` — review records for non-canonical promotion steps
- `templates/` — templates for authoring skills and related files
- `templates/RUNTIME_EXAMPLE.template.md` — canonical runtime example scaffold
- `skills/` — skill bundles
- `generated/` — derived reader catalogs generated from committed skill markdown and manifests
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
- `examples/` — optional runtime examples or bounded mini scenarios
- `checks/` — optional review checklist or validation notes, with `checks/review.md` as the canonical checklist path

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

Belong in `generated/skill_catalog*.json`:
- derived routing and reader surfaces
- deterministic projections of committed `SKILL.md` and `techniques.yaml`
- no new authority beyond the source files

Belong in `generated/skill_walkthroughs.json` and `generated/skill_walkthroughs.md`:
- derived runtime inspect surfaces
- support-artifact aware entry points for `pick -> inspect -> expand -> object use`
- no new authority beyond committed `SKILL.md`, local support artifacts, and public review records

Belong in `generated/public_surface.json` and `generated/public_surface.md`:
- derived governance and public-product signaling
- cohort views such as default references, candidate-ready skills, and pending-lineage blockers
- no status change authority beyond the source files, review records, and evaluation fixtures

Belong in `agents/openai.yaml`:
- invocation mode
- policy
- future Codex-specific metadata

Belong in `docs/reviews/`:
- candidate review records
- promotion review records
- public evidence notes about repository-level review decisions
- explicit notes about whether machine floors pass, whether skill meaning changed, and what blocks the next status step

## What should not live here

- private secrets
- environment-specific sensitive paths
- one-off hacks that were not generalized
- techniques that should live in `aoa-techniques`
- project runtime state or logs
