# AoA Skills System Design

## Role

`DESIGN.md` describes the system form of `aoa-skills`.

It is not the README, architecture reference, roadmap, skill bundle, agent
instruction card, generated catalog, or portable export contract.

It answers one question:

What shape should the AoA bounded execution canon take as it grows?

## Design Thesis

`aoa-skills` turns reusable practice into bounded execution objects for local
coding agents and human reviewers.

The repository is strongest when each skill can stand alone at runtime, while
still keeping honest bridges to reusable techniques, project overlays,
evaluation evidence, generated companions, and downstream install surfaces.

The skill owns the workflow.
The technique keeps the reusable practice.
The generated surface helps discovery.
The export carries the object outward.
The owner route keeps the boundary alive.

## Design as Appearance

`aoa-skills` should appear as a navigable skill canon, not a flat prompt pile.

A healthy skill layer has:

- clear source topology under `skills/`;
- one authored bundle per reusable workflow;
- visible lane cards for core, risk, session-growth, and project skills;
- mechanics packages that explain movement around canon without becoming canon;
- generated reader surfaces that point back to source;
- portable exports that carry skills without replacing their authored roots;
- validation routes that make status, export, and adoption claims inspectable.

The repository should feel useful to a low-context agent without requiring that
agent to absorb every AoA sibling repository first. Sibling routes should be
visible, but skill execution meaning should remain self-contained.

## Design as Anatomy

`aoa-skills` is not one document and not one runtime adapter.

It is composed of:

- authored skill bundles under `skills/`;
- lane-level `AGENTS.md` cards near durable editable districts;
- mechanics packages that describe skill-layer movement, review pressure,
  release support, adoption, recurrence, checkpoint, quest, and bridge routes;
- configuration seams for policy, profiles, export, and adapter metadata;
- scripts, schemas, tests, templates, examples, and manifests that keep the
  canon buildable and reviewable;
- generated companions under `generated/`;
- generated portable skill exports under `.agents/skills/`;
- review, decision, and audit surfaces that preserve why a skill or route moved.

Each layer may support the others. No layer should silently steal authority from
another layer.

## Design as Operation

The core operating path is:

`pick -> inspect -> expand -> object use`

A good skill operation has:

- a named skill object;
- a trigger boundary;
- explicit inputs and outputs;
- risks and anti-patterns;
- a validation route;
- an owner split for sibling truth;
- an export or adapter path when needed;
- a stop-line when the task belongs outside the skill layer.

Technique links may explain lineage, composition, decomposition, refresh
pressure, or extraction candidates. Runtime skill use should still remain
self-contained from the authored bundle.

## Design as Aim

The long aim is a usable execution canon for the AoA ecosystem.

That canon should help agents act with more precision, not with less
accountability. It should make repeated work easier to route, test, export,
review, and improve without turning skills into playbooks, proofs, memory
objects, runtime services, or center doctrine.

`aoa-skills` grows correctly when a future agent can enter a lane, understand
which object is source, run the right check, and leave a clean return route.

## Design Principles

### 1. Self-contained before connected

A skill should make sense from its authored bundle. Bridges enrich the object.
They do not rescue an incomplete workflow.

### 2. Source before export

`SKILL.md`, `techniques.yaml`, and bundle-local support artifacts own skill
meaning. `.agents/skills/*`, generated catalogs, manifests, runtime cards, and
adapter files carry or summarize that meaning.

### 3. Bridges Without Captivity

`aoa-techniques` and `aoa-skills` are directly related, but neither should
become a blocker for the other's legitimate work. Skills may compose techniques,
and repeated skill execution may produce technique extraction pressure.

### 4. Local-agent core, adapter-specific edge

Core skill meaning should use neutral local coding-agent language. Codex,
OpenAI, MCP, and other platform names belong where an adapter, compatibility
schema, export profile, or runtime seam actually requires them.

### 5. Topology beats flat accumulation

The source tree should help agents walk the canon. Functional lanes, local
route cards, and bounded mechanics packages are preferable to root sprawl,
unrouted legacy collections, or compatibility aliases in source.

### 6. Activation is a contract

Trigger boundaries, invocation posture, and implicit activation policy must be
reviewable. A skill should not surprise a task by activating outside its stated
scope.

### 7. Generated companions are companions

Generated and exported surfaces should be deterministic, reproducible, and
source-linked. If they drift, repair the source or builder, then regenerate.

### 8. Project overlays stay thin

Project skills may add paths, commands, local authority surfaces, and risk
posture. They should not smuggle downstream project truth into the reusable
skill canon.

### 9. Evidence layers stay separate

Selection, runtime inspection, evaluation evidence, public status, promotion
pressure, and downstream adoption audits are adjacent layers. Mixing them makes
claims harder to verify.

### 10. Growth routes outward cleanly

When a repeated workflow reveals reusable practice, route it to
`aoa-techniques`. When it needs proof doctrine, route it to `aoa-evals`. When it
becomes scenario composition, route it to `aoa-playbooks`. The skill layer
should sharpen owner boundaries, not absorb them.

## Good Design Feels Like

A contributor can find the canonical bundle.
An agent can identify the trigger boundary.
A reviewer can find the validation route.
A generated export can find its source.
A technique bridge can explain its evidence.
A project overlay can stay thin.
A future skill can find the lane where it belongs.

## Bad Design Smells Like

- flat prompt accumulation;
- root docs repeating every package;
- adapter names becoming core meaning;
- generated files treated as source truth;
- skill meaning that only works through a live sibling fetch;
- playbook, proof, memory, routing, role, or runtime authority hidden in a skill;
- status promotion without review evidence;
- project overlays that become downstream truth mirrors;
- compatibility aliases inside the canonical source topology.

## Relationship to Other Root Surfaces

[`README.md`](README.md) introduces the public repository.
[`AGENTS.md`](AGENTS.md) routes agent work.
[`DESIGN.AGENTS.md`](DESIGN.AGENTS.md) holds the design form of the
agent-facing guidance mesh.
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) explains the technical model and
layering details.
[`mechanics/README.md`](mechanics/README.md) routes owner-local skill mechanics.
[`mechanics/boundary-bridge/docs/LAYER_POSITION.md`](mechanics/boundary-bridge/docs/LAYER_POSITION.md)
names the boundary between skills, techniques, and sibling owners.
[`mechanics/ROADMAP.md`](mechanics/ROADMAP.md) routes future work into package
roadmaps.

`DESIGN.md` holds the system form of the skill layer.

## Use by Agents

Agents should consult this file when a change alters:

- repository shape;
- root surfaces;
- skill topology;
- generated or export posture;
- adapter vocabulary;
- technique bridge meaning;
- project overlay posture;
- activation boundaries;
- layer relationships;
- agent-facing form.

This file does not override local owner truth. It tells agents what kind of
shape the skill layer is preserving.
