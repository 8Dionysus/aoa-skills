# AUDIT.md

This file is the repo-local audit contract for `aoa-skills`.

Read it after `AGENTS.md` and before making changes.

## Repository role

`aoa-skills` is the bounded execution canon of AoA.

It owns:

- public Codex-facing workflow bundles,
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
3. `docs/LAYER_POSITION.md`
4. `docs/BRIDGE_SPEC.md`
5. `docs/RUNTIME_PATH.md`
6. `docs/EVALUATION_PATH.md`
7. `docs/PUBLIC_SURFACE.md`
8. `docs/OVERLAY_SPEC.md`
9. `SKILL_INDEX.md`
10. the target `skills/*/SKILL.md`
11. the target `skills/*/techniques.yaml`
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

- `skills/*/SKILL.md`
- invocation mode, trigger boundary, inputs/outputs, contracts, anti-patterns, and verification wording
- risk-heavy skills, especially `explicit-only` bundles
- any wording that turns a bounded workflow into a vague super-skill

### Technique bridge and lineage

- `skills/*/techniques.yaml`
- `docs/BRIDGE_SPEC.md`
- `scripts/report_technique_drift.py`
- `scripts/refresh_skill_from_manifest.py`
- `scripts/refresh_skill_from_techniques.py`
- any change to pinned `source_ref` values or technique dependency shape

### Status, evidence, and governance surfaces

- `SKILL_INDEX.md`
- `generated/skill_composition_audit.*`
- `generated/skill_evaluation_matrix.*`
- `generated/public_surface.*`
- review records under `docs/reviews/`
- wording that changes `scaffold`, `evaluated`, or `canonical` posture

### Overlays and project-local adaptation

- `docs/OVERLAY_SPEC.md`
- `docs/overlays/*/`
- `skills/atm10-*`
- overlay templates and review artifacts
- any change that makes a thin overlay behave like a downstream integration or playbook

### Derived surface contract layer

- `scripts/build_catalog.py`
- `scripts/validate_skills.py`
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

```bash
python scripts/release_check.py
```

### When touching bundles, derived surfaces, or validation contracts

```bash
python scripts/build_catalog.py
python scripts/validate_skills.py
python scripts/build_catalog.py --check
```

### When touching canonical skills, evaluation evidence, or public status surfaces

```bash
python scripts/report_skill_evaluation.py
python scripts/report_skill_evaluation.py --fail-on-canonical-gaps
```

### When touching one skill directly

```bash
python scripts/inspect_skill.py --skill <skill-name>
python scripts/inspect_skill.py --skill <skill-name> --view evidence
```

### When touching technique dependencies or bridge docs

```bash
python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques
```

If you are intentionally refreshing a published technique ref, keep the wave explicit and bounded:

```bash
python scripts/refresh_skill_from_techniques.py --skill <skill-name> --techniques-repo ../aoa-techniques
python scripts/build_catalog.py
python scripts/validate_skills.py
```

### When touching scripts or validator behavior

Run the nearest `pytest` modules for the affected surfaces, for example:

```bash
python -m pytest tests/test_validate_skills.py tests/test_build_catalog.py
```

Do not list a command in the report unless it was actually run.

## Review guidelines

Use these severity rules for Codex GitHub review and local `/review`.

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

- `python scripts/release_check.py` status
- any `build_catalog`, `validate_skills`, `report_skill_evaluation`, `inspect_skill`, or drift commands actually run
- any `pytest` modules actually run
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
