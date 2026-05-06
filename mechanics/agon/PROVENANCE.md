# Agon Provenance

This file is the active-first bridge for Agon skill-layer mechanics.

Use it when a future edit needs to know how the package relates to earlier
flat Agon docs, candidate seed files, generated companions, recurrence
manifests, and tests.

## Source route

The first mechanics landing distilled these former flat Agon docs into
package-local active parts:

| Former path | Legacy snapshot | Current path |
|---|---|---|
| `docs/AGON_MOVE_SKILL_BRIDGE.md` | `mechanics/agon/legacy/raw/AGON_MOVE_SKILL_BRIDGE.md` | `mechanics/agon/parts/workflow-candidate-bridge/README.md` |
| `docs/AGON_WAVE4_SKILL_LANDING.md` | `mechanics/agon/legacy/raw/AGON_WAVE4_SKILL_LANDING.md` | `mechanics/agon/parts/candidate-validation-gate/README.md` |
| `docs/AGON_RECURRENCE_ADAPTER.md` | `mechanics/agon/legacy/raw/AGON_RECURRENCE_ADAPTER.md` | `mechanics/agon/parts/recurrence-observation/README.md` |
| `docs/AGON_WAVE15_SKILLS_LANDING.md` | `mechanics/agon/legacy/raw/AGON_WAVE15_SKILLS_LANDING.md` | `mechanics/agon/parts/epistemic-candidate-boundary/README.md` |
| `docs/AGON_EPISTEMIC_WORKFLOW_BOUNDARY.md` | `mechanics/agon/legacy/raw/AGON_EPISTEMIC_WORKFLOW_BOUNDARY.md` | `mechanics/agon/parts/epistemic-candidate-boundary/README.md` |
| `docs/AGON_EPISTEMIC_SKILL_CANDIDATES.md` | `mechanics/agon/legacy/raw/AGON_EPISTEMIC_SKILL_CANDIDATES.md` | `mechanics/agon/parts/epistemic-candidate-boundary/README.md` |

No canonical skill bundle meaning moved in that landing.

Historical wave labels belong in [legacy](legacy/README.md), this provenance
bridge, or generated/config lineage. They must not define active package roles,
part names, or route order.

## Active inputs

- `config/agon_skill_binding_candidates.seed.json`
- `config/agon_epistemic_skill_candidates.seed.json`
- `generated/agon_skill_binding_candidates.min.json`
- `generated/agon_epistemic_skill_candidates.min.json`
- `manifests/recurrence/component.agon.skill-binding-surfaces.json`
- `manifests/recurrence/hooks/component.agon.skill-binding-surfaces.hooks.json`

These inputs and companions stay below accepted skill truth.
Existing generated/config fields that preserve old wave labels are lineage
metadata until a separate schema migration removes them.

## Decision route

The structural decision for the first mechanics landing is
[`docs/decisions/2026-05-06-mechanics-agon-start.md`](../../docs/decisions/2026-05-06-mechanics-agon-start.md).

## Stop line

Do not use this provenance bridge as a reason to keep duplicate flat docs
copies. If a moved path is referenced, update the caller to the package-local
active path.
