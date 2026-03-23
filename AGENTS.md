# AGENTS.md

Guidance for coding agents and humans contributing to `aoa-skills`.

## Purpose

`aoa-skills` is the bounded execution canon of AoA.

It stores public, reusable, Codex-facing skill bundles that package reusable
practice into reviewable workflows an agent can execute. A skill is normally a
multi-technique or multi-action package; a single-technique skill is allowed
only as an explicit reviewed exception.

A skill here is not the origin of practice. It is the bounded execution form of practice.

## Owns

This repository is the source of truth for:

- skill bundle wording and workflow structure
- trigger boundaries
- invocation posture
- skill-level inputs and outputs
- reviewability and anti-pattern language at the skill layer
- technique dependency declaration at the skill layer
- generated skill catalogs and capsules

## Does not own

Do not treat this repository as the source of truth for:

- reusable engineering techniques in `aoa-techniques`
- proof doctrine or bounded verdict logic in `aoa-evals`
- routing and dispatch logic in `aoa-routing`
- role contracts in `aoa-agents`
- higher-level scenario composition in `aoa-playbooks`
- memory objects or recall surfaces in `aoa-memo`
- derived knowledge substrate semantics in `aoa-kag`
- private project-specific operations or unsanitized internal instructions

## Core rule

Only contribute skills that are:

- bounded
- reviewable
- public-safe
- useful to Codex
- traceable to reusable practice

If upstream practice already has a canonical home, do not duplicate it here as shallow technique prose.

## Read this first

Before making changes, read in this order:

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `docs/BRIDGE_SPEC.md`
4. the target `skills/*/SKILL.md`
5. any generated skill catalogs or capsules affected by the task

If the task touches technique dependencies, inspect the upstream technique bundles before editing.

## Primary objects

The most important objects in this repository are:

- `skills/*/SKILL.md`
- `skills/*/techniques.yaml` or the current dependency source for the skill
- generated skill catalogs
- generated skill capsules
- architecture and bridge docs referenced by the README

## Allowed changes

Safe, normal contributions include:

- refining a skill’s bounded workflow
- tightening trigger boundaries
- improving inputs, outputs, anti-patterns, and verification wording
- aligning a skill more clearly with upstream techniques
- fixing metadata drift between source files and generated outputs
- adding a new skill when it clearly packages upstream practice into a bounded workflow

## Changes requiring extra care

Use extra caution when:

- changing skill names or identifiers
- changing canonical/evaluated/scaffold status
- changing technique dependency shape
- changing generated catalog or capsule shape
- changing wording that downstream eval bundles or routing surfaces may rely on
- widening a skill beyond a bounded workflow into something that should be a playbook

## Hard NO

Do not contribute:

- secrets
- tokens
- internal-only URLs
- sensitive infrastructure details
- project-only dumps with no reusable overlay framing
- hidden destructive workflows with unclear safety boundaries
- skills with vague trigger boundaries
- skills that silently widen scope beyond the stated task

Do not:

- invent source practice here that belongs in `aoa-techniques`
- write eval doctrine here
- store role-contract meaning here
- store memory meaning here
- collapse scenario-level playbooks into the skill layer

## Repository doctrine

### Techniques and skills are not the same thing

- `aoa-techniques` stores reusable engineering techniques
- `aoa-skills` stores agent-facing skill bundles

A skill may depend on one or more techniques, but the default shape is a
composed package rather than a one-technique lift.
A technique should not be copied here as a shallow duplicate.

## Required for every skill bundle

Each skill should include:

- a canonical `SKILL.md`
- clear intent
- trigger boundary
- inputs and outputs
- explicit contracts
- risks and anti-patterns
- verification guidance
- technique traceability when relevant
- adaptation points for project overlays
- an explicit exception review when the skill is intentionally single-technique

Recommended when relevant:

- dependency manifests
- agent-specific overlay files
- examples or checks for risk-heavy skills

## Public hygiene

Assume everything here is public and reusable by strangers.

Write for portability:

- generalize private paths
- generalize internal hostnames
- strip secrets
- keep runtime assumptions explicit
- prefer small explicit workflow contracts

## Local working notes

- `TODO.local.md` and `PLANS.local.md` are local-only working files for private task control
- keep them out of git
- public roadmap or canonical docs must remain visible to git if the repo defines them that way

## Contribution doctrine

Use this flow:

`PLAN -> DIFF -> VERIFY -> REPORT`

### PLAN

State:

- what skill is being added or changed
- which upstream techniques it depends on
- what the main risk is
- whether downstream eval or routing surfaces may be affected

### DIFF

Keep the change focused.

Do not mix unrelated repository cleanup into a skill PR unless it is necessary for repository integrity.

### VERIFY

Confirm that:

- the skill remains bounded
- the trigger boundary is still coherent
- the skill remains public-safe
- technique references are still accurate
- the output remains reviewable by another human or agent

If metadata or generated skill surfaces changed, regenerate and validate them.

### REPORT

Summarize:

- what changed
- whether skill meaning changed or only metadata changed
- which techniques were referenced or refreshed
- whether generated outputs changed
- any remaining limits or follow-up work

## Validation

Run the validation commands documented in `README.md`.

If your change affects generated catalogs, capsules, or bridge outputs, regenerate and validate them before finishing.

Run tests or checks for touched surfaces when available. Do not claim checks you did not run.

## Cross-repo neighbors

Use these neighboring repositories when the task crosses boundaries:

- `aoa-techniques` for upstream reusable practice
- `aoa-evals` for bounded proof surfaces over skill behavior
- `aoa-routing` for smallest-next-object navigation
- `aoa-agents` for role contracts, handoff posture, and evaluation posture
- `aoa-playbooks` for recurring scenario composition
- `Agents-of-Abyss` for ecosystem-level map and boundary doctrine

## Output expectations

When reporting back after a change, include:

- which skills changed
- whether workflow meaning changed or only metadata changed
- whether technique dependencies changed
- whether generated outputs changed
- what validation was run
- any downstream follow-up likely needed in `aoa-evals` or `aoa-routing`

## Default editing posture

Prefer the smallest reviewable change.
Preserve canonical wording unless the task explicitly requires semantic change.
If semantic change is made, report it explicitly.
