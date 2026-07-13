# Repository structure

## Top level

- `README.md` — project entry point
- `CHARTER.md` — repository authority boundary for the skill layer
- `DESIGN.md` — skill-system form
- `DESIGN.AGENTS.md` — agent-facing guidance form
- `AGENTS.md` — active agent route law
- `SKILL_INDEX.md` — public map of current skills and their maturity
- `CHANGELOG.md` — release-visible history
- `CONTRIBUTING.md` — public contribution route
- `SECURITY.md` — private reporting route for sensitive findings
- `docs/` — architecture, repository layout, review records, governance lanes,
  and preserved root reference
- `QUESTBOOK.md` — compact public index for durable skill-layer obligations
- `mechanics/ROADMAP.md` — roadmap router; package roadmaps own future contours
- `mechanics/` — owner-local skill-layer movement surfaces around AoA mechanics
- `mechanics/ARTIFACT_TOPOLOGY.md` — placement law for mechanic-owned schemas,
  examples, config, generated companions, manifests, scripts, tests, and quests
- `mechanics/release-support/docs/RUNTIME_PATH.md` — main runtime guide for `pick -> inspect -> expand -> object use`
- `mechanics/audit/docs/PUBLIC_SURFACE.md` — public guide to the current governance and product-signaling layer
- `mechanics/method-growth/docs/PROMOTION_PATH.md` — public repository convention for maturity transitions
- `mechanics/boundary-bridge/docs/OVERLAY_SPEC.md` — repo-local contract for thin project overlays and validator fixture packs
- `docs/reviews/` — public review records for candidate and promotion work
- `docs/reviews/canonical-candidates/` — canonical-candidate review records
- `docs/reviews/status-promotions/` — review records for non-canonical promotion steps
- `mechanics/growth-cycle/session-harvests/` — bounded session learning before owner-layer truth
- `mechanics/growth-cycle/templates/` — Growth-cycle-owned harvest-note templates
- `templates/` — templates for authoring skills and related files
- `templates/RUNTIME_EXAMPLE.template.md` — canonical runtime example scaffold
- `templates/PROJECT_OVERLAY.template.md` — canonical project overlay scaffold
- `templates/PROJECT_OVERLAY_SKILL.template.md` — canonical overlayed skill scaffold
- `.agents/` — generated portable skill export layer
- `config/` — repo-wide portable export, policy, profile, runtime, trigger-eval, and router inputs
- `examples/` — root-owned examples only; mechanic examples live under the owning `mechanics/<slug>/` package or nearest part
- `manifests/` — manifest route district; records live with owning mechanic packages or parts
- `quests/` — lane-first durable obligation sources under `quests/<lane>/<state>/`
- `skills/` — canonical skill source topology
- `stats/` — owner-local statistical questions, measurement contracts, and
  evidence-linked reference packets
- `generated/` — derived reader catalogs, portable export discovery, runtime seams, support-resource manifests, and trigger-eval data
- `scripts/` — deterministic repo-wide builders, validators, reports, inspectors, and release helpers
- `schemas/` — repo-wide machine-readable contracts; mechanic-local schemas live with their package or part

There is no root `legacy/` district. Durable rationale belongs in
`docs/decisions/`, bounded session learning belongs in `mechanics/growth-cycle/session-harvests/`,
and raw mechanic lineage belongs under the corresponding package-local
`mechanics/<slug>/legacy/` lane.

## Skill bundle shape

Each skill lives under the recursive source topology:

- `skills/core/engineering/<skill-name>/`
- `skills/core/session-growth/<skill-name>/`
- `skills/risk/<skill-name>/`
- `skills/project/<family>/<skill-name>/`

The bundle identifier remains the leaf directory name. Do not add flat
compatibility aliases at `skills/<skill-name>/`; the generated portable export
under `.agents/skills/*` is the flat compatibility surface.

Recommended contents:

- `SKILL.md` — main runtime skill document
- `techniques.yaml` — bridge manifest that records which techniques shape the skill
- `agents/openai.yaml` — optional invocation and policy settings
- `references/` — optional reference docs or excerpts
- `scripts/` — optional deterministic helper utilities for skill-owned support bundles
- `assets/` — optional structured templates or schemas for skill-owned support bundles
- `examples/` — optional runtime examples or bounded mini scenarios
- `checks/` — optional review checklist or validation notes, with `checks/review.md` as the canonical checklist path

## Naming convention

Use one of these prefixes:
- `aoa-` for public core skills
- `atm10-` for project-family skills around `atm10-agent`
- `abyss-` for project-family skills around `abyss-stack`
- `titan-` for Titan project-family skills

Examples:
- `aoa-change-protocol`
- `aoa-tdd-slice`
- `aoa-contract-test`
- `atm10-change-protocol`
- `abyss-safe-infra-change`
- `titan-runtime-gate`

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

Belong in generated skill catalogs:
- derived routing and reader surfaces
- deterministic projections of committed `SKILL.md` and `techniques.yaml`
- routing and reader data derived from source files

Belong in `.agents/skills/*`:
- generated portable skill export files
- frontmatter and `agents/openai.yaml` derived from canonical skills plus portable export config
- transport data derived from source files and portable export config

Belong in `generated/skill_walkthroughs.json` and `generated/skill_walkthroughs.md`:
- derived runtime inspect surfaces
- support-artifact aware entry points for `pick -> inspect -> expand -> object use`
- runtime inspection data derived from committed `SKILL.md`, local support artifacts, and public review records

Belong in `generated/public_surface.json` and `generated/public_surface.md`:
- derived governance and public-product signaling
- cohort views such as default references, default-reference-ready skills, and pending-lineage blockers
- status readouts derived from source files, review records, and evaluation fixtures

Belong in generated portable, runtime, support-resource, and release manifest surfaces:
- portable discovery, activation, install, and trust surfaces
- deterministic projections of `.agents/skills/*`, canonical invocation policy, and repo-owned portable-layer config
- transport and runtime data derived from source bundles and portable export config

Belong in `agents/openai.yaml`:
- invocation mode
- policy
- adapter-specific metadata

Belong in `docs/reviews/`:
- candidate review records
- promotion review records
- public evidence notes about repository-level review decisions
- explicit notes about whether machine floors pass, whether skill meaning changed, and what blocks the next status step

## What should not live here

- private secrets
- environment-specific sensitive paths
- one-off shortcuts that were not generalized
- techniques that should live in `aoa-techniques`
- project runtime state or logs

## Local-only surfaces

- `TODO.local.md` and `PLANS.local.md` are clone-local planning notes and stay gitignored
- `seeds/` is a clone-local scratch area for seed files and stays gitignored
