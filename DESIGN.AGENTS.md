# AoA Skills Agent Surface Design

## Role

`DESIGN.AGENTS.md` describes the desired form of agent-facing guidance within
`aoa-skills`.

It is not an `AGENTS.md` card, skill bundle, prompt library, policy matrix,
charter, roadmap, schema, validator, generated index, or portable export.

It answers one question:

What shape should agent-facing surfaces take so agents can change and use the
skill canon without losing bundle truth, generated boundaries, evidence,
reviewability, or return routes?

## Design Thesis

`aoa-skills` should not give agents one giant instruction wall.

It should give them a navigable mesh:

- a root card that names repository identity, owner boundaries, and route
  choice;
- lane cards that narrow work under `skills/`, `mechanics/`, `generated/`,
  `config/`, `scripts/`, `schemas/`, `tests/`, `templates/`, and other durable
  districts;
- bundle surfaces that keep skill meaning stronger than generated summaries;
- mechanics surfaces that route movement around canon without becoming canon;
- validation surfaces that turn source, status, export, and adoption claims
  into checkable work;
- closeout contracts that let the next agent resume without archaeology.

Agent guidance is useful when it routes to the nearest owner surface and stops
before stealing authority from that surface.

The root names the skill-layer road system.
The nearest card narrows the lane.
The bundle keeps workflow truth.
The builder carries derived surfaces.
The validator tests the claim.
The closeout returns the work to reviewable memory.

## Design as Appearance

Agent guidance should appear as a readable route network.

A healthy `aoa-skills` agent-facing layer has:

- a root `AGENTS.md` that starts with the canonical six-section card shape;
- local `AGENTS.md` cards in durable editable districts;
- explicit owner boundaries for skills, mechanics, generated surfaces, config,
  scripts, schemas, tests, examples, quests, manifests, and templates;
- named validation routes near the work;
- negative boundaries that say what must not be claimed;
- closeout expectations for changed surfaces, skipped checks, remaining risk,
  and next owner route;
- generated companions that help navigation without becoming source truth.

A low-context agent should be able to answer: where am I, what owns this, what
must I read, what must I not claim, how do I verify, and where do I hand off?

## Design as Anatomy

The agent-facing layer has several different organs.

### Root card

The root `AGENTS.md` owns repository identity, route modes, owner boundaries,
cross-repository routing, broad validation posture, and closeout expectations.

It should route to local truth. It should not contain every skill, mechanic,
script, or generated-surface rule.

### Lane cards

Lane cards own local risks and source surfaces for durable districts such as
`skills/`, `mechanics/`, `generated/`, `config/`, `scripts/`, `schemas/`,
`tests/`, `examples/`, `templates/`, `manifests/`, and `quests/`.

They narrow the root card. They do not overturn it.

### Skill bundle surfaces

`SKILL.md`, `techniques.yaml`, and bundle-local `checks/`, `examples/`,
`references/`, `scripts/`, assets, or adapter files own bundle meaning when
present.

Agent cards route to these surfaces. They should not restate every bundle
contract.

### Mechanics package cards

Mechanics cards describe movement around skill canon: candidate intake,
adoption, audit, release support, recurrence, checkpoint carry, questbook
integration, RPG reader surfaces, Agon bridges, antifragility, and boundary
bridges.

They should name local source surfaces, package validation, owner requests,
generated mirrors, and stop-lines.

### Generated and export cards

Generated and portable export cards protect derived surfaces. They should name
the builder or source config before any edit route.

They must say when a file is not hand-authored.

### Validation surfaces

Builders, validators, tests, audits, and release checks make skill-layer agency
inspectable.

A card that permits a meaningful mutation should name the smallest useful
validation path or the source surface that names it.

### Review and decision surfaces

Reviews, decisions, audit reports, session harvests, and promotion-pressure
surfaces preserve why a skill or route moved.

They are not substitutes for changing the active source surface when active
meaning has changed.

## Design as Operation

A safe agent move in `aoa-skills` follows this route before content mutation:

1. Read the root card.
2. Read the nearest local card for every touched path.
3. Read the route-mode surface named by the root or local card.
4. Read the source bundle, mechanic package, config, builder, schema, validator,
   or generated-source owner that owns the claim.
5. Make the smallest change that preserves the owner boundary.
6. Regenerate derived surfaces from source when a source-backed derived layer
   moved.
7. Run the narrowest relevant validation first, then broader gates when the
   change is release-facing, route-facing, export-facing, structural, or
   cross-owner.
8. Close out with changed surfaces, checks run, checks skipped, remaining risk,
   decision-review result, and next owner route.

Agency becomes stronger when it can stop, explain itself, and hand off cleanly.

## Design as Authority

Agent guidance in `aoa-skills` may:

- route work;
- name local risks;
- name owner surfaces;
- require reading order;
- require validation;
- set closeout shape;
- prevent common unsafe claims.

It must not:

- override authored skill bundles;
- claim technique truth that belongs in `aoa-techniques`;
- claim proof doctrine that belongs in `aoa-evals`;
- claim routing, memory, KAG, stats, playbook, role, or runtime authority;
- claim live downstream adoption without downstream receipt;
- promote skill status without review evidence;
- turn generated or exported surfaces into authority;
- hand-edit generated surfaces as source truth;
- use Codex-specific adapter vocabulary as core skill meaning unless the
  surface is actually an adapter or compatibility layer;
- hide semantic changes under "docs-only", "metadata-only", or formatting
  language.

The agent layer is route law for work. It is not the skill canon, proof system,
runtime body, or sibling owner.

## Canonical Card Shape

Every durable `AGENTS.md` card under `aoa-skills` should begin from this shape
unless a local validator intentionally preserves an older transitional card:

```markdown
# AGENTS.md

## Applies to

## Role

## Read before editing

## Boundaries

## Validation

## Closeout
```

This shape is intentionally plain.

`Applies to` tells the agent where the card rules.
`Role` tells the agent what this lane is for.
`Read before editing` names the minimum orientation path.
`Boundaries` prevents authority drift.
`Validation` turns action into checkable work.
`Closeout` preserves handoff memory.

Optional sections may be added when the lane needs them: `Purpose`, `Owner
lane`, `Route modes`, `Source surfaces`, `Post-change route review`, `Hard no`,
`Review-critical drift`, `Decision review`, or local equivalents.

Optional sections should sharpen the route. They should not decorate it into
fog.

## Design Principles

### 1. Locality before abstraction

The nearest relevant card should carry the local rule. Root guidance should
route without trying to own every local surface.

### 2. Routes before commands

A good card says which surface owns the claim, which route to follow, which
check to run, and where to hand off.

### 3. Source before instruction

Instructions are guidance. Source surfaces own meaning. When they conflict, the
agent should stop and report the conflict instead of inventing reconciliation.

### 4. Negative boundaries are design

A clear "do not" protects against silent authority transfer.

### 5. Validation is the handshake with reality

Substantial cards should name the smallest useful validation path. Broad release
gates matter, but local checks keep work grounded.

### 6. Closeout is continuity

Closeout is the next agent's doorway: changed surfaces, checks, skips, remaining
risk, and the route where work resumes.

### 7. Generated companions are companions

Generated summaries, indexes, manifests, and exports are useful when they
compress and route. They become dangerous when they author meaning or hide their
source.

### 8. Portability comes from repeated shape

Portable guidance is not copied text. It is copied discipline: the same card
shape, owner logic, validation posture, and closeout memory, adapted to local
truth.

### 9. Adapter vocabulary stays at the edge

Core skill law should describe agent-facing workflows in neutral terms.
Platform-specific names belong in adapter surfaces, generated exports, install
profiles, and compatibility documentation.

### 10. Agency must remain returnable

An agent may act, propose, validate, route, summarize, and hand off. Durable
action should preserve review, rollback, evidence, and a route back to the
owner surface.

## Good Agent Design Feels Like

A low-context agent can find the nearest rule.
A skill can find its bundle.
A generated export can find its builder.
A public claim can find its evidence.
A risk-heavy action can find its gate.
A future agent can find the closeout.
A sibling owner can remain outside the skill layer.

## Bad Agent Design Smells Like

- one enormous root card that tries to control every district;
- local cards duplicating root doctrine instead of naming local risk;
- instructions that cite no owner surface;
- validation commands copied everywhere and allowed to drift;
- generated indexes treated as source authority;
- adapter-specific naming used as core meaning;
- status claims without review evidence;
- hidden runtime, memory, proof, routing, or downstream acceptance claims;
- closeouts that only say "done";
- durable directories without a local card or explicit exemption.

## Relationship to Other Surfaces

`README.md` introduces the repository.
`CHARTER.md` names the repository authority boundary.
`DESIGN.md` names the skill-layer system form.
`AGENTS.md` routes agent work in the repository.
Nested `AGENTS.md` cards narrow local work.
`docs/ARCHITECTURE.md` explains the technical model.
`mechanics/README.md` routes owner-local skill mechanics.
`generated/` and `.agents/skills/` remain derived companions built from source.
`.agents/spark/` is an agent-facing Spark lane for launch, result, handoff, and
validation packets; it is not authored skill meaning.

`DESIGN.AGENTS.md` holds the design form of the agent-facing layer.

It tells humans and agents what kind of agent guidance they are preserving when
they add, move, split, validate, generate, or port `AGENTS.md` surfaces.

## Portability to Sibling Projects

Sibling repositories may adopt this shape without adopting `aoa-skills` truth.

The portable minimum is:

- one root `AGENTS.md`;
- local cards for durable editable districts;
- the canonical six-section card shape;
- explicit owner surfaces;
- explicit negative boundaries;
- validation named close to the work;
- closeout that records changed surfaces, checks, skipped checks, risk, and next
  route;
- generated summaries only when they remain source-linked and reproducible.

Port the shape, then let the local owner speak in its own tongue.

## Use by Agents

Agents should consult this file when a change alters:

- the shape of any `AGENTS.md` card;
- root-to-local precedence;
- route modes or reading order;
- validation authority;
- generated or exported agent-facing companions;
- closeout requirements;
- local card placement;
- cross-repository owner routing;
- adapter vocabulary in agent-facing guidance;
- portability of skill guidance to another repository.

This file does not override local owner truth. It tells agents what kind of
agent-facing form they are preserving.

## Landing Rule

When this design changes, review whether the following surfaces also need to
move:

- root `AGENTS.md`;
- affected nested `AGENTS.md` cards;
- `README.md`;
- `docs/README.md`;
- `docs/ARCHITECTURE.md`;
- `mechanics/README.md`;
- validators for card shape, generated freshness, export parity, and release
  checks;
- generated companions when a source-backed machine capsule changed;
- `CHANGELOG.md` and `docs/decisions/` when the root or route-law meaning
  changed.

Only update a surface when its meaning actually moved. The design is a compass,
not a broom.
