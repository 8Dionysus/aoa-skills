# aoa-skills

`aoa-skills` is the AoA skill system: the canon, tooling, review surfaces, and
portable export path for self-contained skill bundles a local coding agent can
inspect, execute, validate, export, and improve.

A skill is a bounded workflow object. It is not a loose prompt, not
project-local shorthand, and not a hidden shortcut. The system exists so AoA can
grow reusable execution ability without hiding ownership, evidence, activation
boundaries, or downstream adoption truth.

Use this README as the public front door. When work becomes agent-operational,
skill-local, mechanical, generated, exported, or status-bearing, follow the
linked owner surface instead of expanding this page.

> Current release: `v0.4.0`. See [CHANGELOG](CHANGELOG.md) for release notes.

## What This Repository Does

| Function | Surface |
|---|---|
| Repository authority boundary | [CHARTER](CHARTER.md) |
| Skill-layer system form | [DESIGN](DESIGN.md) |
| Agent-facing guidance form | [DESIGN.AGENTS](DESIGN.AGENTS.md) |
| Agent route law and local checks | [AGENTS](AGENTS.md) |
| Technical source/generated/export model | [ARCHITECTURE](docs/ARCHITECTURE.md) |
| Public skill catalog | [SKILL_INDEX](SKILL_INDEX.md) |
| Canonical skill bundles | [skills](skills/README.md) |
| Owner-local skill mechanics | [mechanics](mechanics/README.md) |
| Derived reader surfaces | [generated](generated/README.md) |
| Portable skill export | [.agents](.agents/AGENTS.md) |

This repository is strongest when it turns a repeated way of working into a
bounded, reviewable execution object. It is weakest when it tries to become
sibling repository doctrine, proof doctrine, route law, memory, runtime, scenario
composition, or downstream adoption truth.

## Start Here

Read only what matches your entry need.

| Need | Route |
|---|---|
| Shortest honest overview | this README, then [CHARTER](CHARTER.md), [DESIGN](DESIGN.md), [SKILL_INDEX](SKILL_INDEX.md), and [ARCHITECTURE](docs/ARCHITECTURE.md) |
| Agent editing route | [AGENTS](AGENTS.md), then the nearest nested `AGENTS.md` |
| Skill source topology | [skills](skills/README.md) |
| Boundary with sibling owner repos | [LAYER_POSITION](mechanics/boundary-bridge/docs/LAYER_POSITION.md) |
| Runtime use path | [RUNTIME_PATH](mechanics/release-support/docs/RUNTIME_PATH.md) |
| Public status and evaluation | [PUBLIC_SURFACE](mechanics/audit/docs/PUBLIC_SURFACE.md) and [EVALUATION_PATH](mechanics/audit/docs/EVALUATION_PATH.md) |
| Install, export, and downstream refresh | [INSTALL_AND_PROFILES](mechanics/release-support/docs/INSTALL_AND_PROFILES.md) and [COMPONENT_REFRESH_LAW](mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md) |
| Current direction | [mechanics/ROADMAP.md](mechanics/ROADMAP.md), then the nearest mechanic `ROADMAP.md`; [QUESTBOOK.md](QUESTBOOK.md) |
| AoA center requests into this repo | [mechanics/OWNER_REQUEST_RECEIPTS.md](mechanics/OWNER_REQUEST_RECEIPTS.md) |

For package-deep questions, start from [mechanics](mechanics/README.md) and
continue to the nearest mechanic package. The root README should not become the
package atlas.

## Skill Canon

Canonical bundles live under [skills](skills/README.md):

| Lane | Use for |
|---|---|
| [core/engineering](skills/core/engineering/AGENTS.md) | reusable engineering workflows such as change protocol, ADRs, source truth, TDD, contracts, invariants, ports, and boundaries |
| [core/session-growth](skills/core/session-growth/AGENTS.md) | reviewed session-growth workflows such as harvest, route forks, repair, progression, quest harvest, closeout bridge, automation scan, and summon |
| [risk](skills/risk/AGENTS.md) | explicit risk guards for approval, dry run, infra changes, stack bring-up, and sanitized sharing |
| [project](skills/project/AGENTS.md) | thin project overlays that adapt reusable workflows to named owner families |

A bundle owns its `SKILL.md`, `techniques.yaml`, and bundle-local support
artifacts. Mechanics explain movement around the canon; they do not contain
canonical skills.

## Mechanics And Evidence

[mechanics](mechanics/README.md) holds owner-local movement around the skill
canon: method growth, recurrence, checkpoint carry, quest integration, audit,
release support, antifragility, RPG reader surfaces, experience, and boundary
bridges.

Two currently important route anchors:

- [workflow-candidate-bridge](mechanics/agon/parts/workflow-candidate-bridge/README.md)
  keeps requested Agon workflow candidates bounded before any skill landing.
- [agon_skill_binding_candidates.min.json](generated/agon_skill_binding_candidates.min.json)
  is the generated companion for that bridge.

Generated and exported surfaces are companions. Source bundles, source config,
builders, review records, mechanics packages, and owner repositories keep
meaning.

## Validate

Use [AGENTS](AGENTS.md) and the nearest local `AGENTS.md` for executable
validation routes. For release and public-claim checks, start from
[RELEASING](mechanics/release-support/docs/RELEASING.md) and the relevant
release-support or audit surface.

## Working Rule

Grow the skill canon by making the next execution route clearer.

Add bundles, mechanics, generated companions, examples, tests, and exports only
where they improve reviewability and preserve owner boundaries. When detail
belongs to a technique, proof surface, playbook, route, memory object, runtime
body, downstream repository, roadmap, landing log, changelog, quest, decision
record, or agent route card, route it there.

## License

Apache-2.0
