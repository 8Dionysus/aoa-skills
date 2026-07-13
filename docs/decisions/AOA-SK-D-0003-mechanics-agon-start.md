# Mechanics Agon Start

- Decision ID: AOA-SK-D-0003

## Index Metadata

- Original date: 2026-05-06
- Surface classes: mechanic package
- Skill lanes: none
- Mechanic parents: agon
- Guard families: source topology
- Posture: accepted mechanic start

Date: 2026-05-06

Status: accepted

## Context

`aoa-skills` already had mature skill bundles, generated exports, reviews,
runtime surfaces, and downstream bridge surfaces. Its mechanics-shaped guidance
was still mostly flat under `docs/`.

`Agents-of-Abyss` now shows the mature pattern for center mechanics: package
cards, active parts, owner boundaries, provenance bridges, landing logs, and
validation lanes. `aoa-techniques` shows the owner-local translation: use the
same compact card shape, but say `Local owns` rather than importing center
authority.

The Agon skill-binding surface was the smallest complete first package:
compact docs, explicit stop-lines, candidate config, generated companions,
recurrence manifests, and existing tests.

## Decision

Create `mechanics/` as the skill-layer mechanics district and land
`mechanics/agon/` as the first package.

Distill the former flat Agon docs into package-local active parts:

- `docs/AGON_MOVE_SKILL_BRIDGE.md` -> `mechanics/agon/parts/workflow-candidate-bridge/README.md`
- `docs/AGON_WAVE4_SKILL_LANDING.md` -> `mechanics/agon/parts/candidate-validation-gate/README.md`
- `docs/AGON_RECURRENCE_ADAPTER.md` -> `mechanics/agon/parts/recurrence-observation/README.md`
- `docs/AGON_WAVE15_SKILLS_LANDING.md` -> `mechanics/agon/parts/epistemic-candidate-boundary/README.md`
- `docs/AGON_EPISTEMIC_WORKFLOW_BOUNDARY.md` -> `mechanics/agon/parts/epistemic-candidate-boundary/README.md`
- `docs/AGON_EPISTEMIC_SKILL_CANDIDATES.md` -> `mechanics/agon/parts/epistemic-candidate-boundary/README.md`

Add package route surfaces for card, direction, parts, provenance, landing log,
roadmap, and package-local raw legacy snapshots.

Do not change canonical skill bundle meaning in this slice.
Old wave labels stay provenance-only. They may identify prior generated/config
lineage, but they must not define active mechanics part names or active route
order.

## Consequences

- Future agents have a real mechanics entry route before opening Agon
  candidate, generated, or recurrence surfaces.
- The docs root is lighter and no longer owns Agon active guidance.
- Recurrence manifests and tests point at package-local active paths with
  functional names.
- Former flat docs wording remains available under
  `mechanics/agon/legacy/raw/` for migration audits.
- The mechanics package standard can now be copied to the next bounded package
  without moving the whole flat docs surface at once.
- Existing generated candidate companions remain requested-only and weaker than
  source config plus normal skill review.

## Verification

Verification covered Agon skill-binding and epistemic candidate parity and
validation, their focused tests, mechanics route/topology checks, and nested
agent cards.
