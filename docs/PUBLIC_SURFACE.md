# Public surface

This document explains how to read the derived public-product surface of `aoa-skills`
without assuming hidden release metadata or private repository state.

Use this guide when you need status, promotion, or governance signals.
For runtime inspection and skill selection, use `RUNTIME_PATH.md` first.
For evaluation evidence and matrix reading, use `EVALUATION_PATH.md` first.
If you are trying to choose or execute an object, this is the wrong layer.

The current signaling layer is intentionally derived from facts that already exist:
- skill `status`
- technique lineage in `techniques.yaml`
- public review records
- evaluation fixtures
- governance lane decisions in `docs/governance/lanes.yaml`
- explicit-only policy files where relevant

The current human-readable matrix is generated in:

- `generated/public_surface.md`

The machine-readable companion is:

- `generated/public_surface.json`

The explicit governance-decision companion is:

- `docs/governance/lanes.yaml`
- `docs/governance/lanes.md`

The maintenance and readiness companion is:

- `generated/governance_backlog.md`

The packaging and relationship companions are:

- `generated/skill_bundle_index.md`
- `generated/skill_graph.md`
- `generated/skill_boundary_matrix.md`

Read the live counts in those derived surfaces instead of treating this guide as a second status ledger.
`generated/public_surface.md` and `generated/governance_backlog.md` are the authoritative readouts for the current total-skill count, default-reference cohort, candidate-ready cohort, pending-lineage state, and maintenance/readiness view.

These derived surfaces stay separate on purpose:
- `generated/public_surface.*` is the status and promotion readout
- `generated/governance_backlog.*` is the maintenance and readiness queue
- `generated/skill_boundary_matrix.*` cross-links adjacency evidence to governance lanes
- `generated/skill_bundle_index.*` and `generated/skill_graph.*` are packaging and relationship views

## How to read the signals

### `canonical`

`canonical` means the skill is the current default public reference for its workflow class.
It is more than "good" or "evaluated"; it is the current recommended starting point.

### `evaluated`

`evaluated` means the skill already has behavior-oriented evidence.
It is trustworthy enough to use, but it is not automatically the default public reference.

### `candidate_ready`

`candidate_ready` is a derived machine gate-pass signal.
It means the current canonical gate checks pass, but no promotion happened yet.

It does not:
- change `status`
- decide default-reference authority
- replace review judgment
- imply that promotion is automatic

### `governance decision`

`governance_decision` is the explicit repo-local governance outcome attached through a lane.

- `default_reference` means the skill is the recorded default reference in that lane
- `stay_evaluated` means the skill is candidate-ready or otherwise well-evidenced, but the recorded governance outcome is to keep it at `evaluated`

This is why `candidate_ready` and `stay_evaluated` can coexist without contradiction.

### `pending lineage`

`pending lineage` means upstream technique publication or manifest completeness still blocks the canonical path.
It does not cancel `evaluated`.
It means the skill is reviewed and tested at the skill layer, but the upstream technique layer is not fully published yet.

### `explicit-only`

`explicit-only` is an invocation posture, not a maturity status.
It means the skill requires explicit invocation and matching policy posture.

## Runtime boundary

This surface does not tell you how to select, inspect, or evaluate a skill at runtime.
It only explains the derived governance and public-product signals that already exist in the repository.

If you are choosing a skill, start with `docs/RUNTIME_PATH.md`.
If you are reading matrix evidence, start with `docs/EVALUATION_PATH.md`.
If you are reading status or release signals, stay here and in `generated/public_surface.md`.
If you are reading maintenance readiness, use `generated/governance_backlog.md`.
If you are reading bundle shape or adjacency, use `generated/skill_bundle_index.md`, `generated/skill_graph.md`, and `generated/skill_boundary_matrix.md`.

## Current reading order

Use this order when orienting in the public surface:

1. `README.md`
2. `docs/README.md`
3. `docs/RUNTIME_PATH.md`
4. `docs/EVALUATION_PATH.md`
5. `docs/PUBLIC_SURFACE.md`
6. `generated/public_surface.md`
7. `generated/governance_backlog.md`
8. `generated/skill_boundary_matrix.md`
9. `generated/skill_bundle_index.md`
10. `generated/skill_graph.md`
11. `SKILL_INDEX.md`
12. the target `skills/<skill-name>/SKILL.md`

## What this layer does not do

This wave does not introduce:
- GitHub releases
- tags
- changelog workflow
- new skill frontmatter metadata
- implicit promotions

The public-product surface remains repo-local and derived.
Overlay preparation is also separate from this layer; the thin contract lives in `docs/OVERLAY_SPEC.md`, and repo-local live exemplar packs such as `docs/overlays/atm10/PROJECT_OVERLAY.md` stay distinct from downstream adoption.
If you need the human review records behind a candidate or promotion decision, use `docs/reviews/README.md` and the matching file in `docs/reviews/canonical-candidates/` or `docs/reviews/status-promotions/`.

Future stubs:

TODO: if the derived public-product layer ever needs a richer release summary, keep it generated and separate from runtime inspection.

TODO: if cross-repo public-surface signals become necessary, derive them from existing repo facts rather than live fetches.

TODO: if the runtime path ever needs a routing index, keep that in `RUNTIME_PATH.md` or a separate runtime helper rather than blending it into this derived surface.

TODO: if the evaluation matrix ever needs a richer public-facing overlay, keep it in a separate repo-local evidence surface rather than folding it into public status signaling.
