# Bridge spec

This document defines how `aoa-skills` should consume and compose techniques from `aoa-techniques`.

## Goal

Keep techniques as the canonical source of reusable engineering practice while
allowing skills to package those practices into Codex-friendly workflows.
Skills are expected to act as composition packages, not as thin mirrors of a
single technique.
`docs/LAYER_POSITION.md` is the repo-owned boundary note for where this bridge
fits in the wider AoA layer map.

## Non-goal

Skills should not be thin links that require Codex to fetch a remote repository at runtime to understand the technique.
The runtime artifact should remain self-contained enough to execute reviewably.

## Composition model

Each skill may reference one or more techniques by ID, but the default shape is
multi-technique and/or multi-action composition.
A skill that references only one technique must carry an explicit exception
review explaining why it still deserves a skill boundary.
A skill can use selected sections from each referenced technique.
This bridge does not move recurring scenario method into `aoa-skills`; that
canon remains in `aoa-playbooks`.

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

## KAG/source-lift posture

For KAG/source-lift consumers:
- use `AOA-T-0019` as the canonical bundle-level metadata spine for lookup, review posture, and direct adjacency
- use `AOA-T-0018` as the bounded section-lift layer when section-level navigation is needed
- keep the authored `TECHNIQUE.md` markdown authoritative for meaning; derived catalogs, manifests, and section surfaces stay subordinate
- do not widen the metadata spine into all-docs authority, schema-first meaning, or a replacement for markdown sections

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
2. apply a composition filter to decide whether the input should refresh an
   existing skill, become a new multi-technique skill, require an explicit
   single-technique exception review, or be deferred
3. extract selected sections
4. generate or refresh `SKILL.md`
5. keep the final committed `SKILL.md` human-reviewable

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

## Current fan-out proof

One upstream source technique can stay aligned across multiple skill bundles without hand-copied divergence.

- source:
  - `AOA-T-0001` from `aoa-techniques`
- target consumer surfaces:
  - `skills/aoa-change-protocol/techniques.yaml`
  - `skills/aoa-change-protocol/SKILL.md`
  - `skills/aoa-safe-infra-change/techniques.yaml`
  - `skills/aoa-safe-infra-change/SKILL.md`
- drift control:
  - `python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques --skill aoa-change-protocol --skill aoa-safe-infra-change`
  - `python scripts/refresh_skill_from_techniques.py --skill aoa-change-protocol --skill aoa-safe-infra-change --techniques-repo ../aoa-techniques`

This is the current donor evidence shape for one-source to many-target distribution:
one pinned source ref, multiple committed consumer surfaces, and explicit refresh tooling when the upstream source changes.

## Current refresh-wave examples

Published-ref refresh waves stay repo-local and reviewable.
They resolve one local `aoa-techniques` ref, apply it to an explicit skill cohort,
and use ordinary diff plus bridge-coverage output as the review surface.

Shared-donor refresh example:

- shared upstream donor:
  - `AOA-T-0017` from `aoa-techniques`
- target consumer surfaces:
  - `skills/aoa-invariant-coverage-audit/techniques.yaml`
  - `skills/aoa-invariant-coverage-audit/SKILL.md`
  - `skills/aoa-property-invariants/techniques.yaml`
  - `skills/aoa-property-invariants/SKILL.md`
- review posture:
  - both bundles may be refreshed against the same resolved local target ref in one bounded wave
  - the refresh remains acceptable even when only one referenced technique in the bundle is currently `drifted`

Mixed-lineage refresh example:

- target skill:
  - `aoa-dry-run-first`
- published technique ref:
  - `AOA-T-0004` may refresh to the resolved local target ref
- pending technique ref:
  - `AOA-T-PENDING-DRY-RUN-FIRST` stays `path: TBD` and `source_ref: TBD`

Bounded repo-local wave example:

```bash
python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques --skill aoa-bounded-context-map --skill aoa-contract-test --skill aoa-dry-run-first --skill aoa-invariant-coverage-audit --skill aoa-property-invariants --skill aoa-tdd-slice
python scripts/refresh_skill_from_techniques.py --skill aoa-bounded-context-map --skill aoa-contract-test --skill aoa-dry-run-first --skill aoa-invariant-coverage-audit --skill aoa-property-invariants --skill aoa-tdd-slice --techniques-repo ../aoa-techniques
```

This kind of wave refreshes already published refs and the traceability surfaces that depend on them.
It does not close pending lineage and does not widen into upstream publication work inside `aoa-techniques`.

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
They are not a reason to collapse a technique into a thin one-technique skill
when the skill layer does not add a real package boundary.

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
For multi-skill refreshes, prefer explicit `--skill` lists against a local `../aoa-techniques` checkout rather than a broad repin.
If a selected skill is mixed-lineage, refresh only its published refs and keep pending entries at `TBD` until the upstream technique is published.
Future technique harvests should pass through the composition filter above
before any skill file is created or refreshed.

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
