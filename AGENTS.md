# AGENTS.md

Guidelines for coding agents and humans contributing to `aoa-skills`.

## Purpose

This repository stores **public, reusable, Codex-facing skills**.

Do not treat it as:
- a dump of raw prompts
- a backup of private project operations
- a duplicate of `aoa-techniques`
- a place for unsanitized internal instructions

## Core rule

Only contribute skills that are:
- bounded
- reviewable
- public-safe
- useful to Codex
- traceable to reusable practice

## Hard NO

Do not contribute:
- secrets
- tokens
- internal-only URLs
- sensitive infrastructure details
- project-only dumps with no overlay framing
- hidden destructive workflows with unclear safety boundaries
- skills with vague trigger boundaries
- skills that silently widen the task beyond the stated scope

## Repository doctrine

### Techniques and skills are not the same thing

- `aoa-techniques` stores reusable engineering techniques
- `aoa-skills` stores agent-facing skill bundles

A skill may depend on one or more techniques.
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

Recommended:
- `techniques.yaml`
- `agents/openai.yaml` when invocation policy matters
- examples or checks for risk-heavy skills

## Public hygiene

Assume everything here is public and reusable by strangers.

Write for portability:
- generalize private paths
- generalize internal hostnames
- strip secrets
- keep runtime assumptions explicit
- prefer small explicit workflow contracts

## Contribution doctrine

Use this flow:

`PLAN -> DIFF -> VERIFY -> REPORT`

### PLAN
State what skill is being added or changed, what technique dependencies it has, and what the main risk is.

### DIFF
Keep the change focused.
Do not mix unrelated repository cleanup into a skill PR.

### VERIFY
Confirm that:
- the skill remains bounded
- the trigger boundary is still coherent
- the skill remains public-safe
- technique references are still accurate enough
- the output remains reviewable by another human or agent

### REPORT
Summarize:
- what changed
- whether the skill meaning changed or only metadata changed
- which techniques were referenced or refreshed
- any remaining limits or follow-up work

## Invocation policy

Prefer these categories:
- `implicit-friendly`
- `explicit-preferred`
- `explicit-only`

Risk-heavy infrastructure or operational skills should usually be `explicit-only` or, at minimum, `explicit-preferred`.

## Preferred PR shape

Prefer:
- one new skill per PR
- or one focused skill refresh
- or one repository-level docs/template improvement

## Quality bar

A skill is stronger when it has:
- a sharp trigger boundary
- clear technique traceability
- explicit risks and anti-patterns
- visible verification guidance
- a stable final `SKILL.md`
- thin project overlays rather than hidden project assumptions

## Drift rule

If a source technique changes materially, dependent skills should be reviewed.
Do not silently let a skill drift into a new meaning without naming the change.

## Small reversible changes

Prefer small, reviewable, reversible edits.
Do not opportunistically refactor unrelated skill bundles while touching one skill.

## Security

If a proposed skill, example, or overlay reveals a leak, secret, or infrastructure-sensitive detail,
do not publish it as-is.
Sanitize first, or keep it out of the public repository.
