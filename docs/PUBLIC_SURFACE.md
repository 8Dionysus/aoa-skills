# Public surface

This document explains how to read the public-product surface of `aoa-skills`
without assuming hidden release metadata or private repository state.

The current signaling layer is intentionally derived from facts that already exist:
- skill `status`
- technique lineage in `techniques.yaml`
- public review records
- evaluation fixtures
- explicit-only policy files where relevant

The current human-readable matrix is generated in:

- `generated/public_surface.md`

The machine-readable companion is:

- `generated/public_surface.json`

## How to read the signals

### `canonical`

`canonical` means the skill is the current default public reference for its workflow class.
It is more than "good" or "evaluated"; it is the current recommended starting point.

### `evaluated`

`evaluated` means the skill already has behavior-oriented evidence.
It is trustworthy enough to use, but it is not automatically the default public reference.

### `candidate_ready`

`candidate_ready` is a derived governance signal.
It means the current machine-readable canonical gate checks pass, but no promotion happened yet.

It does not:
- change `status`
- replace review judgment
- imply that promotion is automatic

### `pending lineage`

`pending lineage` means upstream technique publication or manifest completeness still blocks the canonical path.
It does not cancel `evaluated`.
It means the skill is reviewed and tested at the skill layer, but the upstream technique layer is not fully published yet.

### `explicit-only`

`explicit-only` is an invocation posture, not a maturity status.
It means the skill requires explicit invocation and matching policy posture.

## Current reading order

Use this order when orienting in the public surface:

1. `README.md`
2. `docs/README.md`
3. `docs/PUBLIC_SURFACE.md`
4. `generated/public_surface.md`
5. `SKILL_INDEX.md`
6. the target `skills/<skill-name>/SKILL.md`

## What this layer does not do

This wave does not introduce:
- GitHub releases
- tags
- changelog workflow
- new skill frontmatter metadata
- implicit promotions

The public-product surface remains repo-local and derived.
