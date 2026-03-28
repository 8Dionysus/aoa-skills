# Two-Stage Skill Selection

Wave 9 keeps skill activation split into two bounded steps.

## Stage 1

Read only compressed skill cards and candidate bands.

Output:

- shortlist candidates
- top band hints
- explicit/manual markers for risk skills

This stage is a narrowing seam only.

## Stage 2

Read only the shortlist plus existing full skill-side activation surfaces.

Output:

- `activate-candidate`
- `manual-invocation-required`
- `no-skill`

The stage-2 decider remains the activation authority.

## Why this lives partly in `aoa-skills`

The tiny-router cards are still derived from skill meaning:

- descriptions
- invocation posture
- scope
- companion relationships

That makes them a valid downstream bridge surface here.

The routing policy that uses those cards still belongs in `aoa-routing`.
