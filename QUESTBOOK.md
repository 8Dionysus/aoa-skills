# QUESTBOOK.md — aoa-skills

This file is the public tracked surface for deferred workflow, runtime-seam, and proof-alignment obligations that belong to `aoa-skills`.

Use it for:
- skill bundle gaps that survive a bounded edit
- skill/eval alignment debts
- `.agents/skills/` portable-layer and local-adapter contract follow-through
- overlay or two-stage-routing exceptions that recur often enough to need harvest
- recurring cross-repo bridge refresh and review truth-sync routes that need explicit automation or playbook classification

Do not use it for:
- one-off prompt tweaks
- raw local wrapper chatter
- transient generated noise that dies in the current diff
- replacing skill meaning that already lives in skill bundles and source docs

## Frontier
- `AOA-SK-Q-0003` — tighten the Codex portable layer and local adapter contract for .agents/skills export

## Near
- `AOA-SK-Q-0004` — harvest repeated overlay-specific exceptions into stable skill bundles or playbooks
- `AOA-SK-Q-0005` — reflect bounded skill bundles as abilities with pack-profile-aware unlock posture
- `AOA-SK-Q-0006` — classify the cross-repo technique refresh and truth-sync route for bounded automation follow-through
- `AOA-SK-Q-0008` — track checkpoint owner-promotion follow-through as an early skill-layer seam

## Latent / parked
- none yet

## Harvest candidates
- `AOA-SK-Q-0004` — harvest repeated overlay-specific exceptions into stable skill bundles or playbooks
- `AOA-SK-Q-0008` — track checkpoint owner-promotion follow-through as an early skill-layer seam

## Session-harvest family posture

The permanent project-core session-growth kernel in this repo is:

- `aoa-session-donor-harvest`
- `aoa-automation-opportunity-scan`
- `aoa-session-route-forks`
- `aoa-session-self-diagnose`
- `aoa-session-self-repair`
- `aoa-session-progression-lift`
- `aoa-quest-harvest`

It is authored under `repo-project-core-kernel`. The older
`repo-session-harvest-family` name remains as a backward-compatible rollout
alias, while narrower profiles remain available for the donor-harvest nucleus,
the automation scan seam, and the quest-harvest leaf. Skill meaning stays
source-owned in `aoa-skills`.

Kernel governance posture:

- the kernel is repo-wide hard-gated, not just installable
- every kernel skill must keep one detail receipt schema plus the shared
  `core_skill_application_receipt` schema
- the portable export must carry both refs for every kernel skill
- `generated/project_core_kernel_governance.min.json` is the canonical
  per-skill gate readout
- release is blocked if any kernel skill drops out of that contract

Family boundaries:

- `aoa-session-donor-harvest` is the nucleus for turning reviewed sessions into
  a bounded `HARVEST_PACKET`
- `aoa-automation-opportunity-scan` keeps automation-readiness detection
  explicit and checkpoint-aware instead of smuggling scheduler authority into
  donor or route notes
- `aoa-session-route-forks` makes next-route choices explicit when several
  honest routes survive
- `aoa-session-self-diagnose` stays read-only and classifies drift before
  repair
- `aoa-session-self-repair` authors checkpointed repair packets instead of
  silent self-mutation
- `aoa-session-progression-lift` keeps progression evidence multi-axis and
  reviewable
- `aoa-quest-harvest` remains the leaf skill for final promotion triage on one
  repeated reviewed quest unit

Family rules:

- use the family only after a reviewed run, closure, or pause
- do not use it inside an active route
- do not let route forks, progression, or quest flavor become hidden routing authority
- do not let diagnosis silently mutate anything
- do not let self-repair bypass checkpoint posture
- do not promote on one anecdotal repeat

## Project-core shape

The project-core shape in this repo now has two stable layers:

- `kernel` = the hard-gated seven-skill session-growth nucleus
- `outer ring` = the soft-gated engineering workbench around that nucleus

The outer ring currently contains:

- `aoa-adr-write`
- `aoa-source-of-truth-check`
- `aoa-bounded-context-map`
- `aoa-core-logic-boundary`
- `aoa-port-adapter-refactor`
- `aoa-change-protocol`
- `aoa-tdd-slice`
- `aoa-contract-test`
- `aoa-property-invariants`
- `aoa-invariant-coverage-audit`

Outer-ring posture:

- it is authored under `repo-project-core-outer-ring`
- it is repo-wide soft-gated through
  `generated/project_core_outer_ring_readiness.min.json`
- it stays classification-backed, not telemetry-backed
- it is not a second kernel and does not replace `repo-core-only`

Boundary notes:

- `repo-core-only` is the umbrella repo surface and must equal `kernel + outer ring`
- `repo-project-foundation` is the baseline install layer and must equal
  `kernel + outer ring + risk guard ring`
- the explicit safety perimeter is the separate `risk guard ring`, authored
  under `repo-project-risk-guard-ring`
- `repo-risk-explicit` remains as the backward-compatible alias for that same
  risk ring
- project overlays such as `atm10-*` and `abyss-*` stay outside both project-core
  layers and outside the risk guard ring membership

## Risk guard ring

The risk guard ring currently contains:

- `aoa-approval-gate-check`
- `aoa-dry-run-first`
- `aoa-local-stack-bringup`
- `aoa-safe-infra-change`
- `aoa-sanitized-share`

Risk-ring posture:

- it is authored under `repo-project-risk-guard-ring`
- `repo-risk-explicit` must stay an exact alias of the same five-skill surface
- it is repo-wide hard-gated through
  `generated/project_risk_guard_ring_governance.min.json`
- it stays explicit-only, scope=`risk`, and collision-family aligned
- it does not replace `repo-default` and it is not a second kernel

Adjacent overlays:

- `aoa-safe-infra-change` may have the adjacent project overlay
  `abyss-safe-infra-change`
- `aoa-sanitized-share` may have the adjacent project overlay
  `abyss-sanitized-share`
- those overlays are reported next to the ring, but they are not ring members

Foundation posture:

- `repo-project-foundation` is the stable install baseline for project work
- it carries the hard-gated session-growth kernel, the soft-gated engineering
  workbench, and the hard-gated risk perimeter together
- it intentionally excludes project overlays, which remain opt-in and local

Allowed `aoa-quest-harvest` verdicts:

- `keep/open quest`
- `promote to skill`
- `promote to playbook`
- `promote to orchestrator surface`
- `promote to proof surface`
- `promote to memo surface`

## Backing files

- `quests/*.yaml`
- `schemas/quest.schema.json`
- `schemas/quest_dispatch.schema.json`
- `generated/quest_catalog.min.example.json`
- `generated/quest_dispatch.min.example.json`
