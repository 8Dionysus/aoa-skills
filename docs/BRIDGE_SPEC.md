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
    source_ref: 0123456789abcdef0123456789abcdef01234567
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

Published techniques should be pinned to a concrete upstream commit SHA in `source_ref`.
Pending techniques should use `path: TBD` and `source_ref: TBD` until the upstream technique is published.

## Build-time composition

Preferred model:
1. read one or more techniques from `aoa-techniques`
1. resolve them at the pinned `source_ref`
2. extract selected sections
3. generate or refresh `SKILL.md`
4. keep the final committed `SKILL.md` human-reviewable

This keeps skill execution stable and reproducible.

Current local helper:

```bash
python scripts/refresh_skill_from_manifest.py --skill aoa-change-protocol
```

Explicit single-skill write mode:

```bash
python scripts/refresh_skill_from_manifest.py --skill aoa-change-protocol --write
```

The helper is dry-run-first. Repo-wide write mode remains intentionally unavailable in this pass.

The helper now also reports bridge-coverage gaps against the committed runtime shape.
Those gaps are review signals, not auto-generated content.
Single-skill write mode may refresh `technique_dependencies` and the traceability block,
but it must not invent missing runtime sections on behalf of the author.

Current cross-repo hardening helpers:

```bash
python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques
python scripts/refresh_skill_from_techniques.py --skill aoa-change-protocol --techniques-repo ../aoa-techniques
```

`report_technique_drift.py` compares published `source_ref` values against a chosen local
`aoa-techniques` ref and reports `clean`, `drifted`, or `pending` technique refs per skill.
With `--fail-on-drift`, it becomes a CI-facing signal without changing the default repo-local validator.

`refresh_skill_from_techniques.py` is dry-run-first and bounded to explicitly named skills.
It updates published `source_ref` values in `techniques.yaml`, then regenerates
`technique_dependencies` and the `## Technique traceability` block in `SKILL.md`.
It must not invent missing runtime sections on behalf of the author.

Bridge-coverage mapping in the current pass:

- `summary` -> frontmatter `summary`
- `Intent` -> `## Intent`
- `When to use` -> `## Trigger boundary`
- `When not to use` -> `## Trigger boundary`
- `Inputs` -> `## Inputs`
- `Outputs` -> `## Outputs`
- `Core procedure` -> `## Procedure`
- `Contracts` -> `## Contracts`
- `Risks` -> `## Risks and anti-patterns`
- `Validation` -> `## Verification`
- `Adaptation notes` -> `## Adaptation points`

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

Recommended local workflow:

1. run `python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques`
2. run `python scripts/refresh_skill_from_techniques.py --skill <skill-name> --techniques-repo ../aoa-techniques`
3. manually review whether the upstream drift changes runtime meaning or only pinned refs and traceability
4. rebuild generated reader surfaces with `python scripts/build_catalog.py`
5. re-run `python scripts/validate_skills.py`

The bridge/drift flow uses CLI output and ordinary git diff as the review surface.
It does not add committed drift-report artifacts.

## Invocation policy

Skills should eventually declare one of these modes:
- implicit-friendly
- explicit-preferred
- explicit-only

Risk-heavy infrastructure skills should generally be explicit-only.

## Review requirements

A skill PR should make it clear:
- which techniques are referenced
- which upstream source refs were pinned or refreshed
- whether the skill is newly created or refreshed
- whether project overlays were updated
- whether the runtime `SKILL.md` changed meaningfully
