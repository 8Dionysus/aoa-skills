# Bridge spec

This document defines how `aoa-skills` should consume and compose techniques from `aoa-techniques`.

## Goal

Keep techniques as the canonical source of reusable engineering practice while allowing skills to package those practices into Codex-friendly workflows.

## Non-goal

Skills should not be thin links that require Codex to fetch a remote repository at runtime to understand the technique.
The runtime artifact should remain self-contained enough to execute reviewably.

## Composition model

Each skill may reference one or more techniques by ID.
A skill can use selected sections from each referenced technique.

Recommended source sections:
- Intent
- When to use
- When not to use
- Inputs
- Outputs
- Core procedure
- Contracts
- Risks
- Validation
- Adaptation notes

Sections usually not copied verbatim into runtime skill content:
- Promotion history
- Public sanitization notes
- repository-internal evidence notes

## Recommended file: `techniques.yaml`

Each skill directory may contain a `techniques.yaml` manifest.

Suggested shape:

```yaml
skill_name: aoa-change-protocol
composition_mode: bounded
techniques:
  - id: AOA-T-0001
    repo: 8Dionysus/aoa-techniques
    path: techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md
    use_sections:
      - Intent
      - When to use
      - Inputs
      - Outputs
      - Core procedure
      - Contracts
      - Risks
      - Validation
```

## Build-time composition

Preferred model:
1. read one or more techniques from `aoa-techniques`
2. extract selected sections
3. generate or refresh `SKILL.md`
4. keep the final committed `SKILL.md` human-reviewable

This keeps skill execution stable and reproducible.

## Runtime expectations

At runtime, Codex should be able to use the committed `SKILL.md` without requiring live dependency resolution.

References to technique IDs may remain in the skill for traceability.

## Project overlays

Project overlays may add:
- local commands
- validation commands
- source-of-truth documents
- path assumptions
- explicit risk policy
- examples shaped for the local repository

Project overlays should not fork the core meaning of a technique unless they explicitly document the divergence.

## Drift policy

If a technique changes materially in `aoa-techniques`, dependent skills should be reviewed and refreshed.

A future automation flow may:
- detect changed technique IDs
- list dependent skills
- produce a refresh report

## Invocation policy

Skills should eventually declare one of these modes:
- implicit-friendly
- explicit-preferred
- explicit-only

Risk-heavy infrastructure skills should generally be explicit-only.

## Review requirements

A skill PR should make it clear:
- which techniques are referenced
- whether the skill is newly created or refreshed
- whether project overlays were updated
- whether the runtime `SKILL.md` changed meaningfully
