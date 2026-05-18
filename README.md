# aoa-skills

`aoa-skills` is the bounded execution canon of AoA: the place where reusable
practice becomes self-contained skill bundles a local coding agent can inspect,
execute, validate, and hand off.

It is the operational companion to `aoa-techniques`. Techniques keep reusable
practice meaning. Skills keep executable workflow meaning. The bridge is real,
but it is a bridge: technique links are lineage and composition evidence, not
hidden runtime dependencies or automatic status blockers.

Use this README as the public front door. Use the linked owner surfaces when
work becomes skill-local, mechanical, generated, exported, evaluated, or
repository-local.

> Current release: `v0.3.3`. See [CHANGELOG](CHANGELOG.md) for release notes.

## What This Repository Does

| Function | Skill-layer surface |
|---|---|
| Describes the system form of the skill canon | [DESIGN](DESIGN.md) |
| Describes the form of agent-facing guidance | [DESIGN.AGENTS](DESIGN.AGENTS.md) |
| Routes agent work through owner boundaries and local checks | [AGENTS](AGENTS.md) |
| Explains the technical source/generated/export model | [ARCHITECTURE](docs/ARCHITECTURE.md) |
| Maps the current public skill catalog | [SKILL_INDEX](SKILL_INDEX.md) |
| Holds canonical authored skill bundles | [skills](skills/README.md) |
| Routes owner-local skill mechanics | [mechanics](mechanics/README.md) |
| Publishes source-derived catalogs, matrices, and runtime companions | [generated](generated/README.md) |
| Carries the generated portable skill export | [.agents](.agents/AGENTS.md) |

This repository is strongest when it turns a repeated way of working into a
bounded, reviewable execution object. It is weakest when it tries to become
technique canon, proof doctrine, scenario composition, memory, routing, runtime,
or downstream truth.

## Start Here

Read only what matches your entry need.
When a question is package-deep, use the nearest mechanic surface instead of
turning this README into the package map.

| Need | Route |
|---|---|
| Shortest honest overview | this README, then [DESIGN](DESIGN.md), [SKILL_INDEX](SKILL_INDEX.md), and [ARCHITECTURE](docs/ARCHITECTURE.md) |
| Agent editing route | [AGENTS](AGENTS.md), then the nearest nested `AGENTS.md` |
| Skill-layer system form | [DESIGN](DESIGN.md) |
| Agent-surface design | [DESIGN.AGENTS](DESIGN.AGENTS.md) |
| Canonical source topology | [skills](skills/README.md) |
| Skill mechanics and package routes | [mechanics](mechanics/README.md) |
| Skill-technique boundary | [LAYER_POSITION](mechanics/boundary-bridge/docs/LAYER_POSITION.md) |
| Runtime use path | [RUNTIME_PATH](mechanics/release-support/docs/RUNTIME_PATH.md) |
| Evaluation and public status | [EVALUATION_PATH](mechanics/audit/docs/EVALUATION_PATH.md), [PUBLIC_SURFACE](mechanics/audit/docs/PUBLIC_SURFACE.md) |
| Export, install, and downstream adoption | [INSTALL_AND_PROFILES](mechanics/release-support/docs/INSTALL_AND_PROFILES.md), [COMPONENT_REFRESH_LAW](mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md) |
| Current direction and durable obligations | [mechanics/ROADMAP.md](mechanics/ROADMAP.md), then the nearest mechanic `ROADMAP.md`; [QUESTBOOK.md](QUESTBOOK.md) |
| AoA owner requests into this repo | [mechanics/OWNER_REQUEST_RECEIPTS.md](mechanics/OWNER_REQUEST_RECEIPTS.md) |
| Agon bounded-workflow bridge | [mechanics/agon/parts/workflow-candidate-bridge/README.md](mechanics/agon/parts/workflow-candidate-bridge/README.md) and [generated/agon_skill_binding_candidates.min.json](generated/agon_skill_binding_candidates.min.json) |
| Compact machine route | [SKILL_INDEX](SKILL_INDEX.md), [skill_intelligence_registry.min.json](generated/skill_intelligence_registry.min.json) |

## Route Modes

Every substantial change should choose the smallest route that owns the claim.

| Route mode | Use when | Start surface |
|---|---|---|
| `first-reading` | you need the shortest honest repository overview | `README.md` |
| `system-design` | skill-layer form, topology, export posture, or layer relationships change | [DESIGN](DESIGN.md) |
| `agent-surface-design` | AGENTS shape, card placement, route modes, or closeout expectations change | [DESIGN.AGENTS](DESIGN.AGENTS.md) |
| `skill-editing` | a canonical skill bundle, trigger boundary, invocation posture, or technique metadata changes | [skills/AGENTS](skills/AGENTS.md) |
| `mechanic-change` | owner-local movement around canon changes | [mechanics/README](mechanics/README.md) |
| `generated-surface` | derived catalogs, matrices, manifests, runtime cards, or export companions change | [generated/AGENTS](generated/AGENTS.md) |
| `export-refresh` | `.agents/skills`, install profiles, support resources, or downstream pack parity changes | [COMPONENT_REFRESH_LAW](mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md) |
| `public-status` | status, evaluation, promotion pressure, governance, or public claims change | [PUBLIC_SURFACE](mechanics/audit/docs/PUBLIC_SURFACE.md) |

## Claim Check

Before trusting or publishing a skill-layer claim, route it through the
smallest surface that can answer it.

| Claim question | Check |
|---|---|
| Is this repository allowed to own the claim? | [DESIGN](DESIGN.md), [ARCHITECTURE](docs/ARCHITECTURE.md) |
| Is this active skill meaning? | `skills/**/SKILL.md` and `skills/**/techniques.yaml` |
| Is this reusable practice rather than executable workflow? | `aoa-techniques`, not this repository |
| Is this proof doctrine or quality verdicting? | `aoa-evals`, with local routing through [EVALUATION_PATH](mechanics/audit/docs/EVALUATION_PATH.md) |
| Is this scenario composition or questline shape? | `aoa-playbooks`, not the skill bundle |
| Is this generated, exported, or installed output? | source builder/config first, then [generated](generated/AGENTS.md) or [.agents](.agents/AGENTS.md) |
| Does this affect downstream install parity? | [INSTALL_AND_PROFILES](mechanics/release-support/docs/INSTALL_AND_PROFILES.md) and workspace adoption audit |
| Does this change how agents work in the repository? | [AGENTS](AGENTS.md) and [DESIGN.AGENTS](DESIGN.AGENTS.md) |

Generated and exported surfaces are companions, not authority. Source bundles,
source config, mechanics packages, and owner repositories keep meaning.

## Current Contour

The current public contour is a source-topologized skill canon with generated
portable exports and owner-local mechanics around canon movement.

Current anchors:

- [skills](skills/README.md) for canonical skill bundles and source topology
- [DESIGN](DESIGN.md), [DESIGN.AGENTS](DESIGN.AGENTS.md), and
  [ARCHITECTURE](docs/ARCHITECTURE.md) for layer form and source/export
  discipline
- [mechanics](mechanics/README.md) for skill-layer movement, adoption,
  recurrence, checkpoint, quest, audit, boundary bridge, and release-support
  routes
- [mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md](mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md)
  for reviewed project-core session-growth kernel packet and receipt examples
- [generated](generated/README.md) for compact catalogs, matrices, runtime
  companions, and public read models
- [.agents](.agents/AGENTS.md) for generated portable skill export surfaces

Detailed mechanic futures live in `mechanics/<slug>/ROADMAP.md` or active
mechanic package surfaces, not in this README.

## Skill Canon

Canonical source bundles live under `skills/`:

| Lane | Use for |
|---|---|
| [core/engineering](skills/core/engineering/AGENTS.md) | reusable engineering workflows such as change protocol, ADRs, source truth, TDD, contracts, invariants, ports, and boundaries |
| [core/session-growth](skills/core/session-growth/AGENTS.md) | reviewed session-growth workflows such as harvest, route forks, repair, progression, quest harvest, closeout bridge, automation scan, and summon |
| [risk](skills/risk/AGENTS.md) | explicit risk guards for approval, dry run, infra changes, stack bring-up, and sanitized sharing |
| [project](skills/project/AGENTS.md) | thin project overlays that adapt reusable workflows to named owner families |

A skill bundle owns its `SKILL.md`, `techniques.yaml`, and bundle-local support
artifacts. Mechanics explain movement around the canon; they do not contain
canonical skills.

## Technical Districts

Root-adjacent districts have local route cards:

| District | Use for |
|---|---|
| [config](config/AGENTS.md) | portable export, policy, profile, trigger, and adapter inputs |
| [scripts](scripts/AGENTS.md) | builders, validators, reports, inspectors, installers, and runtime seams |
| [schemas](schemas/AGENTS.md) | machine contracts for generated and review surfaces |
| [tests](tests/AGENTS.md) | regression and contract checks |
| [docs](docs/AGENTS.md) | architecture, decisions, reviews, and supporting docs |
| [templates](templates/AGENTS.md) | reusable authoring templates |
| [examples](examples/AGENTS.md) | compact example objects and fixtures |
| [quests](quests/AGENTS.md) | durable skill-layer obligations |
| [manifests](manifests/AGENTS.md) | manifest posture and source-linked inventories |

District cards explain local handling. They do not replace skill bundles,
mechanics packages, generated-source builders, or sibling owner repositories.

## Verify

Use the narrowest check that matches the changed surface. For repo-wide or
release-facing changes, run:

```bash
python scripts/release_check.py
```

For root guidance changes, the minimum route is:

```bash
python scripts/validate_agents_design.py
python scripts/validate_nested_agents.py
python scripts/build_catalog.py --check
```

When release-facing status, review truth, or technique lineage can affect a
public claim, include the matching gates:

```bash
python scripts/validate_skills.py --fail-on-review-truth-sync
python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques --fail-on-drift
```

## Working Rule

Grow the skill canon by making the next execution route clearer.

Add bundles, mechanics, generated companions, examples, tests, and exports only
where they improve reviewability and preserve owner boundaries. When a detail
belongs to a technique, proof surface, playbook, route, memory object, runtime
body, downstream repository, roadmap, landing log, changelog, quest, or
decision record, route it there.

## License

Apache-2.0
