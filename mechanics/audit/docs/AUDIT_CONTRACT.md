# mechanics/audit/docs/AUDIT_CONTRACT.md

This file is the repo-local audit contract for `aoa-skills`.

Read it after `AGENTS.md` and before making changes.

## Repository role

`aoa-skills` is the bounded execution canon of AoA.

It owns:

- public local-agent workflow bundles,
- trigger boundaries, invocation posture, inputs, outputs, and bounded procedures,
- skill-level technique traceability and pinned bridge refs,
- repo-local runtime, evaluation, and public derived surfaces for skills,
- thin project overlays that stay public-safe and repo-local.

It does **not** own:

- reusable technique truth in `aoa-techniques`,
- bounded proof doctrine or verdict logic in `aoa-evals`,
- routing ownership in `aoa-routing`,
- downstream project authority, secrets, or private operations.

## Source-of-truth docs

Default reading order for audits:

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `mechanics/boundary-bridge/docs/LAYER_POSITION.md`
4. `mechanics/boundary-bridge/docs/BRIDGE_SPEC.md`
5. `mechanics/release-support/docs/RUNTIME_PATH.md`
6. `mechanics/audit/docs/EVALUATION_PATH.md`
7. `mechanics/audit/docs/PUBLIC_SURFACE.md`
8. `mechanics/boundary-bridge/docs/OVERLAY_SPEC.md`
9. `SKILL_INDEX.md`
10. the target `skills/**/SKILL.md`
11. the target `skills/**/techniques.yaml`
12. any matching `docs/reviews/...` records
13. the matching generated surfaces as **derived evidence only**:
   - `generated/skill_bundle_index.md`
   - `generated/skill_graph.md`
   - `generated/skill_composition_audit.md`
   - `generated/skill_evaluation_matrix.md`
   - `generated/public_surface.md`

Also apply the nearest nested `AGENTS.md` when working in subdirectories.

## High-risk surfaces

### Skill meaning and boundary posture

- `skills/**/SKILL.md`
- invocation mode, trigger boundary, inputs/outputs, contracts, anti-patterns, and verification wording
- risk-heavy skills, especially `explicit-only` bundles
- any wording that turns a bounded workflow into a vague super-skill

### Technique bridge and lineage

- `skills/**/techniques.yaml`
- `mechanics/boundary-bridge/docs/BRIDGE_SPEC.md`
- `scripts/reports/report_technique_drift.py`
- `scripts/refresh/refresh_skill_from_manifest.py`
- `scripts/refresh/refresh_skill_from_techniques.py`
- any change to pinned `source_ref` values or technique dependency shape

### Status, evidence, and governance surfaces

- `SKILL_INDEX.md`
- `generated/skill_composition_audit.*`
- `generated/skill_evaluation_matrix.*`
- `generated/public_surface.*`
- review records under `docs/reviews/`
- wording that changes `scaffold`, `evaluated`, or `canonical` posture

### Overlays and project-local adaptation

- `mechanics/boundary-bridge/docs/OVERLAY_SPEC.md`
- `mechanics/boundary-bridge/overlays/*/`
- `skills/atm10-*`
- overlay templates and review artifacts
- any change that makes a thin overlay behave like a downstream integration or playbook

### Derived surface contract layer

- `scripts/builders/build_catalog.py`
- `scripts/validation/validate_skills.py`
- `schemas/`
- `generated/*`
- `tests/fixtures/skill_evaluation_cases.yaml`

## Hard boundaries

Never:

- invent reusable engineering practice here when it belongs in `aoa-techniques`,
- move proof doctrine, verdict logic, or bounded-claim language here when it belongs in `aoa-evals`,
- let `generated/*` outrank authored `SKILL.md` or `techniques.yaml`,
- add a single-technique skill without an explicit exception review and composition-surface alignment,
- let a thin overlay author downstream truth, hidden authority, private instructions, or secrets,
- weaken a risk-heavy skill into default-live or implicit behavior without explicit human approval,
- use runtime walkthroughs or evaluation matrix rows as a substitute for readable skill meaning,
- claim validation or bridge refresh that was not actually run.

## Approval-required changes

Do not make these changes without explicit human confirmation:

- changing a skill name or identifier,
- changing `scope`, `status`, or `invocation_mode`,
- adding a new skill bundle,
- changing technique dependency shape across more than one skill,
- repinning or refreshing technique refs across a multi-skill wave,
- adding or materially expanding a live overlay pack,
- changing generated catalog, capsule, or section schema shape.

## Mandatory verification

### Minimum after meaningful changes

Use the release lane when the audit changes release-facing surfaces. Full lane
command authority stays in `config/validation_lanes.json`; nearest `AGENTS.md`
cards name the focused local route.

### When touching bundles, derived surfaces, or validation contracts

Use the source and generated/read-model routes for skill bundles and derived
surfaces. The owning surfaces are `scripts/validation/validate_skills.py`,
`scripts/builders/build_catalog.py`, and the validation lane manifest.

### When touching canonical skills, evaluation evidence, or public status surfaces

Use the evaluation report surface, with the canonical-gap failure mode when the
change is intended to block on evidence completeness.

### When touching one skill directly

Use the skill inspection surface for the changed skill and include evidence view
when the claim touches review or evaluation posture.

### When touching technique dependencies or bridge docs

Use the technique drift report surface against the local `aoa-techniques`
checkout.

If you are intentionally refreshing a published technique ref, keep the wave explicit and bounded:

Use the technique refresh helper for the named skill, then rebuild generated
read models and rerun the source skill validator through the focused owner
route.

### When touching scripts or validator behavior

Run the nearest tests for the affected script, validator, or generated surface.
For validation-command authority, use `docs/validation/COMMAND_AUTHORITY.md`.

Do not list a command in the report unless it was actually run.

## Review guidelines

Use these severity rules for GitHub review and local `/review`.

### Treat as P0

- committed secrets, private instructions, or internal-only URLs in skill or overlay surfaces
- a risk-heavy skill changing from `explicit-only` to a weaker invocation posture without explicit approval and matching docs/evidence updates
- overlay or skill wording that silently routes a bounded public workflow toward destructive or live operational behavior

### Treat as P1

- a skill widens beyond a bounded workflow
- runtime wording duplicates or rewrites technique truth instead of packaging it
- single-technique composition appears without exception review or without updating the composition audit surface
- `SKILL.md`, `techniques.yaml`, and derived catalogs or matrices drift apart
- status or invocation changes appear without matching review or evidence surfaces
- overlay packs begin acting like downstream integrations or scenario playbooks
- claiming validation that was not actually run

Ignore low-value wording nits unless the task explicitly requests copyediting.

## Required report shape

Every audit or patch report for this repo should include:

### PLAN

- task restatement
- touched or inspected skills or surfaces
- main risk: boundary, bridge drift, status/evidence, overlay, or public hygiene

### DIFF

- what changed
- whether skill meaning changed or only metadata, docs, or generated surfaces changed
- whether technique dependencies or invocation posture changed

### VERIFY

- release-lane status when release-facing surfaces changed
- any catalog, skill validation, evaluation, inspection, drift, or focused test
  commands actually run
- what was not run

### REPORT

- current skill boundary after the change
- whether status, invocation mode, technique traceability, or overlay posture changed
- any downstream follow-up likely needed in `aoa-evals`, `aoa-routing`, or a downstream project repo

### RESIDUAL RISK

- upstream technique refs not yet refreshed
- generated surfaces not re-read
- overlay assumptions or evidence paths not exercised

## Routing rule

If the requested work mainly changes:

- reusable engineering practice or technique truth, route to `aoa-techniques`;
- bounded proof claims, verdict logic, or public eval wording, route to `aoa-evals`;
- downstream project authority or private operational detail, route to the downstream repository;
- ecosystem ownership or layer-map language, route to `Agents-of-Abyss`.
