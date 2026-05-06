# Recurrence

This package owns the `aoa-skills` side of recurrence: observation producers
and review-decision closure around skill activation pressure.

Recurrence here is thinner than the center mechanic in `Agents-of-Abyss`.
The center owns return law and continuity vocabulary. This repo only owns
skill-layer signals that may inform trigger review, applicability review,
candidate intake, or bounded follow-through.

## Mechanic card

Status: `landed-local-observation-start`.

### Trigger

Use this package when skill beacons, trigger-gap observations, live receipt
signals, generated activation evidence, or session-harvest repeats need to
become review pressure without becoming automatic skill invocation.

### Local owns

This package owns skill-layer observation producer posture, recurrence-fed
review decision closure, source/projection boundaries for recurrence manifests,
and stop-lines around activation authority.

### Stronger owner split

`Agents-of-Abyss` owns recurrence law and owner-request grammar. `aoa-sdk` owns
typed recurrence carry and control-plane helpers. `aoa-routing` owns dispatch.
`aoa-memo` owns memory recall. `aoa-playbooks` owns recurring choreography.
`aoa-evals` owns proof. `aoa-stats` owns derived visibility. Owner repos own
accepted refreshes and local behavior.

### Inputs

- description-trigger observations
- trigger-eval gaps
- skill evaluation matrix signals
- live skill receipts
- session-harvest notes
- recurrence component and hook manifest drift

### Outputs

- observation posture
- review-decision closure route
- trigger-eval or applicability-map follow-through cue
- owner route for proof, routing, memory, runtime, stats, or scenario pressure
- no automatic activation or refresh by itself

### Must not claim

- ambient continuity
- automatic skill invocation
- automatic component refresh
- recursor spawn
- memory sovereignty
- proof verdict
- generated evidence as source truth
- owner acceptance

### Validation

Use [AGENTS](AGENTS.md#validation) for exact package checks.

### Next route

Start from [DIRECTION](DIRECTION.md), [PARTS](PARTS.md), and the relevant
active part. Use [PROVENANCE](PROVENANCE.md) when auditing how the package
landed from former flat docs, recurrence manifests, hooks, and neighbor
mechanics.

## Active route

- [Direction](DIRECTION.md): current intent, boundaries, and route posture.
- [Parts](PARTS.md): active part map.
- [Provenance](PROVENANCE.md): active-first bridge to moved docs, manifests,
  hooks, Agon recurrence, and neighbor mechanics.
- [Landing Log](LANDING_LOG.md): dated accounting for checked landings.
- [Roadmap](ROADMAP.md): next honest recurrence passes.

## Functioning parts

- [Live Observation Producers](parts/live-observation-producers/README.md):
  producer inputs that may feed skill review.
- [Review Decision Closure](parts/review-decision-closure/README.md):
  recurrence-fed decision posture without activation authority.

## Boundary

Recurrence can surface repeated skill pressure and route review. It does not
invoke skills, refresh components, mutate manifests, create memory, prove
claims, or accept owner work.
