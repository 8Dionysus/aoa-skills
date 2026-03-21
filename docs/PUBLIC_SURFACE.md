# Public surface

This document explains how to read the derived public-product surface of `aoa-skills`
without assuming hidden release metadata or private repository state.

For runtime inspection and skill selection, use `RUNTIME_PATH.md` first.
That guide covers the `pick -> inspect -> expand -> object use` path.
This document stays separate and only explains derived governance/public-surface signals.
If you are trying to choose or execute an object, this is the wrong layer.

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

## Runtime boundary

This surface does not tell you how to select or inspect a skill at runtime.
It only explains the derived governance and public-product signals that already exist in the repository.

If you are choosing a skill, start with `docs/RUNTIME_PATH.md`.
If you are reading status or release signals, stay here and in `generated/public_surface.md`.

## Current reading order

Use this order when orienting in the public surface:

1. `README.md`
2. `docs/README.md`
3. `docs/RUNTIME_PATH.md`
4. `docs/PUBLIC_SURFACE.md`
5. `generated/public_surface.md`
6. `SKILL_INDEX.md`
7. the target `skills/<skill-name>/SKILL.md`

## What this layer does not do

This wave does not introduce:
- GitHub releases
- tags
- changelog workflow
- new skill frontmatter metadata
- implicit promotions

The public-product surface remains repo-local and derived.

Future stubs:

TODO: if the derived public-product layer ever needs a richer release summary, keep it generated and separate from runtime inspection.

TODO: if cross-repo public-surface signals become necessary, derive them from existing repo facts rather than live fetches.

TODO: if the runtime path ever needs a routing index, keep that in `RUNTIME_PATH.md` or a separate runtime helper rather than blending it into this derived surface.
