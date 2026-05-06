# Checkpoint

This package owns the `aoa-skills` side of the cross-project Checkpoint
mechanic: checkpoint-note protocol and the boundary into explicit reviewed
closeout.

It keeps mid-session carry provisional while preserving the route into
`aoa-checkpoint-closeout-bridge` when a reviewed closeout artifact exists.

## Mechanic card

Status: `landed-local-note-bridge`.

### Trigger

Use this package when checkpoint evidence needs to be preserved, reviewed,
promoted, or handed into an explicit closeout bridge without minting
`candidate_ref`, final harvest verdicts, progression verdicts, quest verdicts,
memory canon, or owner truth.

### Local owns

This package owns checkpoint-note protocol, pre-harvest stop-lines, schema and
example route, the bridge boundary into `aoa-checkpoint-closeout-bridge`, and
the local distinction between checkpoint collection and reviewed closeout
execution.

### Stronger owner split

`Agents-of-Abyss` owns center Checkpoint law and owner map. `aoa-sdk` owns
checkpoint controls, local ledgers, typed readers, and closeout-context
builders. `aoa-agents` owns self-agent checkpoint posture. `aoa-memo` owns
durable memory and recall objects. `aoa-playbooks` owns recurring checkpoint
choreography. `aoa-evals` owns proof. `aoa-routing` owns re-entry hints.
`aoa-stats` owns derived visibility. `Dionysus` owns reviewed checkpoint
snapshots and seed-stage lineage when promotion is explicit. `abyss-stack` owns
runtime checkpoint exports.

### Inputs

- checkpoint signal, pause point, commit, green verification, PR, merge, or
  owner-followthrough boundary
- provisional `cluster_ref`, owner hints, evidence refs, promotion conditions,
  and review posture
- reviewed session artifact when moving into closeout bridge execution
- session checkpoint schema and example
- canonical checkpoint closeout bridge skill

### Outputs

- checkpoint note route
- provisional candidate cluster carry
- reviewed closeout bridge request
- Dionysus note or harvest handoff recommendation
- no candidate, harvest, progression, quest, memory, proof, runtime, or owner
  truth by itself

### Must not claim

- `candidate_ref`
- harvest verdict
- progression verdict
- quest verdict
- memory canon
- proof verdict
- runtime activation
- owner acceptance
- hidden scheduler
- autonomous self-repair

### Validation

Use [AGENTS](AGENTS.md#validation) for exact package checks.

### Next route

Start from [DIRECTION](DIRECTION.md), [PARTS](PARTS.md), and the relevant
active part. Use [PROVENANCE](PROVENANCE.md) when auditing how the package
landed from the former flat docs surface and which schema/example/skill
companions belong to the route.

## Active route

- [Direction](DIRECTION.md): current intent, boundaries, and route posture.
- [Parts](PARTS.md): active part map.
- [Provenance](PROVENANCE.md): active-first bridge to moved docs, schema,
  example, bridge skill, and neighbor mechanics.
- [Landing Log](LANDING_LOG.md): dated accounting for checked landings.
- [Roadmap](ROADMAP.md): next honest checkpoint passes.
- [Docs](docs/README.md): active checkpoint contract docs.

## Functioning parts

- [Checkpoint Note Lane](parts/checkpoint-note-lane/README.md): additive
  pre-harvest checkpoint-note capture.
- [Closeout Bridge Boundary](parts/closeout-bridge-boundary/README.md): route
  from reviewed checkpoint hints into explicit reviewed closeout execution.

## Boundary

Checkpoint mechanics can preserve and route provisional carry. They do not
replace the session-growth family, do not execute the bridge skill by
themselves, and do not mint final verdicts from checkpoint notes.
