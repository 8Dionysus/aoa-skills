# Mechanics Surface Rehome

- Decision ID: AOA-SK-D-0013

## Index Metadata

- Original date: 2026-05-06
- Surface classes: root/topology, mechanic package, legacy/provenance
- Skill lanes: none
- Mechanic parents: cross-mechanic
- Guard families: source topology, docs route
- Posture: accepted mechanics surface rehome

Date: 2026-05-06

Status: accepted

Superseded in part by
`AOA-SK-D-0001-distributed-mechanics-roadmaps-and-root-questbook.md`: repo future
direction is now routed through `mechanics/ROADMAP.md`, while package
`ROADMAP.md` files own package contours and root `QUESTBOOK.md` owns the public
quest index.

## Context

Several active `aoa-skills` mechanics surfaces had outgrown the flat root and
`docs/` layer. They described audit, release support, boundary bridges,
experience workflow posture, quest obligations, overlays, and current direction,
but their placement made them look like unrelated docs instead of package-owned
movement surfaces.

The repo already had the AoA-style mechanics package shape:
`README.md`, `AGENTS.md`, `DIRECTION.md`, `PARTS.md`, `PROVENANCE.md`,
`LANDING_LOG.md`, `ROADMAP.md`, active `docs/`, and package-local `legacy/`
when source lineage matters.

## Decision

Move mechanics-shaped root and flat-doc surfaces into owning packages under
`mechanics/`:

- audit contract, evaluation, public-surface, and activation evidence under
  `mechanics/audit/`
- layer-position, bridge, overlays, OpenAI/Codex wiring, and tiny-router bridge
  under `mechanics/boundary-bridge/`
- adoption/governance/service/office/receipt/install/policy/rollback workflow
  posture under `mechanics/experience/`
- maturity and promotion docs under `mechanics/method-growth/`
- questbook index under `mechanics/questbook/`
- portable export, runtime, release, install, support-resource, and wave-history
  surfaces under `mechanics/release-support/`
- repo current direction under `mechanics/ROADMAP.md`

Keep canonical skill bundles in `skills/`, generated surfaces in `generated/`
and `.agents/skills/`, review/governance records in `docs/`, and quest objects
in `quests/`.

## Rationale

This keeps root docs short and route-driven while giving each mechanics concern
a durable local home. It also avoids copying AoA center authority into
`aoa-skills`: local packages own skill-layer movement and stop-lines, while
stronger owner repositories keep final doctrine, proof, routing, playbook,
runtime, memory, or downstream truth.

## Consequences

- References, scripts, validators, tests, generated surfaces, and package maps
  must use the new paths.
- Former paths may appear only as provenance or historical source mapping, not
  as active entry routes.
- Future mechanics work should deepen one package at a time instead of adding
  another broad flat-doc wave.
