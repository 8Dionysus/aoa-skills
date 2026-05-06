# RPG

This package owns the `aoa-skills` side of RPG-shaped reader surfaces:
ability-card and loadout posture over existing skill bundles.

RPG here is thinner than the center mechanic in `Agents-of-Abyss`. The center
owns ecosystem world grammar. This repo only owns bounded reader posture that
makes skill bundles easier to inspect without changing skill truth.

## Mechanic card

Status: `landed-local-reader-start`.

### Trigger

Use this package when ability cards, loadout hints, pack-profile posture, or
progression-shaped reader cues need to describe skill bundles without becoming
runtime state or scenario choreography.

### Local owns

This package owns skill ability-card reader boundaries, loadout reader posture,
pack-profile hint boundaries, generated ability companion routes, and
stop-lines that keep RPG reflection below canonical skill meaning.

### Stronger owner split

`Agents-of-Abyss` owns center RPG world grammar. `aoa-agents` owns role and
progression contract truth. `aoa-playbooks` owns scenario and campaign
choreography. `aoa-evals` owns proof verdicts. `aoa-memo` owns memory and
chronicle objects. `aoa-routing` owns routing behavior. `aoa-stats` owns
derived summaries. Runtime state belongs to `abyss-stack` and owner projects.

### Inputs

- canonical skill bundle path
- technique dependency and evaluation evidence
- pack-profile and trust-policy context
- adapter and overlay posture
- generated ability-card examples
- progression-shaped reader hints

### Outputs

- ability reader boundary
- loadout reader posture
- generated companion route
- owner handoff cue
- no skill truth, runtime inventory, role canon, proof, quest, memory, route,
  or owner acceptance

### Must not claim

- hidden ontology
- runtime ledger or equipped state
- role canon
- canonical skill truth
- playbook choreography
- proof verdict
- quest closure
- memory canon
- routing authority
- owner acceptance
- automatic skill promotion

### Validation

Use [AGENTS](AGENTS.md#validation) for exact package checks.

### Next route

Start from [DIRECTION](DIRECTION.md), [PARTS](PARTS.md), and the relevant
active part. Use [PROVENANCE](PROVENANCE.md) when auditing how the package
landed from the former flat docs surface and which generated ability or
pack-profile companions belong to the route.

## Active route

- [Direction](DIRECTION.md): current intent, boundaries, and route posture.
- [Parts](PARTS.md): active part map.
- [Provenance](PROVENANCE.md): active-first bridge to moved docs, generated
  ability surfaces, pack/profile sources, and owner routes.
- [Landing Log](LANDING_LOG.md): dated accounting for checked landings.
- [Roadmap](ROADMAP.md): next honest RPG passes.

## Functioning parts

- [Ability Reader Boundary](parts/ability-reader-boundary/README.md): ability
  cards as derived reader surfaces over skill bundles.
- [Loadout Posture](parts/loadout-posture/README.md): loadout as pack-profile
  reader hint, not runtime inventory.

## Boundary

RPG can help readers understand skills as abilities and loadout hints. It does
not rewrite `SKILL.md`, create runtime equipped state, author scenarios, prove
progression, or accept owner work.
