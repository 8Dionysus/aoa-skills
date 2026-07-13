# aoa-skills Charter

## Purpose

`aoa-skills` is the AoA bounded execution canon.
It stores public, reusable skill bundles that package practice into
self-contained workflows a local coding agent can inspect, execute, validate,
export, and improve.

The repository is allowed to define skill workflow meaning.
It is not allowed to absorb the owners of practice, proof, routing, memory,
runtime, roles, scenarios, or downstream project truth.

## Authority Boundary

This charter answers what `aoa-skills` may claim about the skill layer.

Operational editing routes live in [AGENTS](AGENTS.md). System form lives in
[DESIGN](DESIGN.md). Agent-facing guidance form lives in
[DESIGN.AGENTS](DESIGN.AGENTS.md). The technical source/generated/export model
lives in [ARCHITECTURE](docs/ARCHITECTURE.md).

This charter gives those surfaces their repository boundary; it does not
replace them.

## Mission

`aoa-skills` exists so reusable ways of working can become bounded execution
objects without hiding source truth or owner boundaries.

It should:

- keep each skill self-contained, reviewable, public-safe, and useful to a
  local coding agent
- preserve trigger boundaries, inputs, outputs, risks, contracts, validation,
  and invocation posture
- keep technique bridges visible without making techniques a hidden runtime
  dependency for every skill use
- publish generated and portable companions only from source-owned skill
  bundles, config, review evidence, and builders
- support downstream adoption without claiming downstream adoption truth

## What This Repository Owns

| Skill-layer object | Meaning |
|---|---|
| Canonical skill bundles | authored `skills/**/SKILL.md` workflow meaning |
| Skill metadata | `techniques.yaml`, invocation posture, trigger boundaries, and bundle-local support artifacts |
| Skill topology | source lanes for core, risk, project, and other reviewed skill families |
| Skill policy seams | repo-owned config for activation, export profiles, adapter metadata, and portable packaging |
| Generated companions | catalogs, matrices, runtime cards, support indexes, intelligence registries, and release manifests derived from source |
| Portable exports | `.agents/skills/*` as generated transport for compatible runtimes |
| Skill-layer mechanics | owner-local movement around canon, including audit, release support, adoption pressure, recurrence, checkpoint carry, quest integration, boundary bridges, and candidate routing |
| Skill review evidence | records that explain status, promotion pressure, exceptions, and public claims without replacing source bundles |
| Owner-local stats port | skill-domain measurement questions, populations, evidence refs, and authority ceilings under `stats/` |

## Routed To Stronger Owners

| Object class | Stronger owner |
|---|---|
| reusable practice truth | `aoa-techniques` |
| proof doctrine, verdicts, scoring, and regression authority | `aoa-evals` |
| dispatch, recommendation, and route policy | `aoa-routing` |
| recurring scenarios, campaigns, and route choreography | `aoa-playbooks` |
| role identity, persona contracts, standing posture, and handoffs | `aoa-agents` |
| memory, retention, recall, and witness objects | `aoa-memo` |
| graph, retrieval, and KAG substrate semantics | `aoa-kag`, derived from source owners |
| shared statistical grammar, aggregation, and cross-owner views | `aoa-stats`, derived from owner-local evidence; skill-domain measurement meaning remains in `stats/` here |
| runtime services, storage, workers, daemons, and deployment | `abyss-stack` |
| typed helpers, compatibility, activation, and control-plane implementation | `aoa-sdk` |
| AoA constitutional identity, federation map, and center law | `Agents-of-Abyss` |
| ToS-authored knowledge meaning | `Tree-of-Sophia` |
| consuming project truth and local adoption receipts | downstream owner repositories |

## Canon Discipline

A skill claim is healthy when a reader can identify the workflow, trigger,
inputs, outputs, stop-line, validation signal, risk, and owner boundary without
needing private context.

Technique links may explain lineage, composition, decomposition, refresh
pressure, or future extraction. They do not make an incomplete skill complete.

Generated outputs and portable exports are companions. They may route,
compress, inspect, or transport skill meaning for machines, but authored skill
bundles, source config, review records, and builders keep authority.

Mechanics may prepare canon, preserve lineage, route candidates, and constrain
movement around skills. They do not contain canonical skills.

Project overlays should stay thin. They may adapt a reusable workflow to a
named owner family, but they must not become mirrors of downstream project
truth.

## Review Rule

Before changing the repository's root posture, skill-canon boundary,
source/export relationship, public route map, or owner split, check:

1. this charter for repository authority
2. [DESIGN](DESIGN.md) for the system form being preserved
3. [DESIGN.AGENTS](DESIGN.AGENTS.md) for agent-facing route shape
4. [AGENTS](AGENTS.md) for the active editing route
5. [ARCHITECTURE](docs/ARCHITECTURE.md) for source/generated/export structure
6. [LAYER_POSITION](mechanics/boundary-bridge/docs/LAYER_POSITION.md) for
   sibling owner boundaries
7. [mechanics](mechanics/README.md) when the change concerns movement around
   canon
8. generated surfaces, builders, validators, and review records before claiming
   parity or status

If the change belongs to another AoA repo, `aoa-skills` should route to that
owner rather than absorbing the object.
