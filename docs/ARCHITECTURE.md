# Architecture

## Purpose

`aoa-skills` is a public repository of reusable Codex skills.
It is the operational companion to `aoa-techniques`.

- `aoa-techniques` answers: what is the technique, when should it be used, what are its invariants, risks, and validation rules?
- `aoa-skills` answers: how should Codex apply one or more techniques in a concrete agent workflow?

## Conceptual model

### Techniques

A technique is a minimal reproducible unit of engineering practice.
It is public-safe, documented, bounded, and validated.

### Skills

A skill is an agent-facing executable guidance bundle.
It packages:
- scoped instructions
- output expectations
- references
- optional scripts
- invocation policy
- technique composition metadata

A skill may rely on one technique or on several techniques.

## Layering

### Layer 1: origin project
A technique is born in a real project such as `atm10-agent` or `abyss-stack`.

### Layer 2: technique canon
The technique is sanitized, generalized, validated, and promoted into `aoa-techniques`.

### Layer 3: skill canon
A skill in `aoa-skills` references one or more techniques and composes them into a Codex-usable workflow.

### Layer 4: project overlay
A project-local overlay adds:
- repo paths
- commands
- source-of-truth files
- risk policies
- approval gates
- runtime assumptions

## Design rules

1. techniques are the source of truth for reusable practice
2. skills are allowed to summarize or compose techniques, but should not silently drift from them
3. runtime skill execution should not depend on live remote fetches
4. build-time composition is preferred over runtime remote dependency
5. project overlays should remain thin
6. dangerous or operationally sensitive skills should default to explicit invocation

## Skill categories

### Core skills
Reusable across many repositories.
Examples:
- change protocol
- TDD slice
- contract-test design
- bounded-context mapping

### Project skills
Reusable inside one project family.
Examples:
- `atm10-*`
- `abyss-*`

### Risk skills
Operational or destructive workflows that should require explicit invocation and strong guardrails.

## Build philosophy

Skills should be reviewable artifacts.
They can be generated or assembled from technique references, but the committed `SKILL.md` should remain understandable to a human reviewer without additional hidden state.

## Versioning direction

A skill should eventually record:
- its own version or revision
- the technique IDs it depends on
- optionally the source technique commit or release reference used when the skill was generated or updated
