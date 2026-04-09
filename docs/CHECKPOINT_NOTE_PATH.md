# Checkpoint Note Path

`aoa-skills` keeps the session-growth core ring explicit and reviewed.
This note defines the lighter checkpoint-note layer that can exist before the
existing post-session family is invoked.

## Purpose

Use a checkpoint note when Codex or another bounded wrapper needs to preserve
mid-session growth candidates after meaningful checkpoints such as:

- a commit
- a green verification pass
- a PR opening or merge
- a long pause
- a manual checkpoint marker

The checkpoint note is an additive pre-harvest seam. It is not a replacement
for the reviewed session-harvest family.

## Boundary

- checkpoint capture is not harvest verdict
- checkpoint capture is append-only and lower-authority
- checkpoint capture may preserve owner hints, evidence refs, and promotion
  conditions
- checkpoint capture does not emit `HARVEST_PACKET`
- checkpoint capture does not emit `CORE_SKILL_APPLICATION_RECEIPT`
- existing session-harvest skills remain `explicit-only`
- the project core kernel remains `finish`-stage for real receipt publication

## What belongs in a checkpoint note

- checkpoint history with meaningful checkpoint kinds
- candidate clusters that survived the checkpoint
- review posture such as `collecting` or `reviewable`
- evidence refs and owner hints
- promotion recommendations such as `local_note`, `dionysus_note`, or
  `harvest_handoff`
- defer reasons when owner ambiguity or thin evidence remains

## What does not belong in a checkpoint note

- final donor harvest verdicts
- final progression or diagnosis packets
- automation authority
- memory canon
- hidden mutation authority

## Promotion read

The honest route is:

`checkpoint capture -> reviewed checkpoint note -> Dionysus promoted note or harvest handoff -> explicit core ring`

Promotion stays explicit. A checkpoint note may prepare reviewed closeout, but
it does not become a silent substitute for the existing session-growth family.

When the session is ready for explicit reviewed closeout, the honest bridge is
`aoa-checkpoint-closeout-bridge`: it may use checkpoint hints as shortlist
inputs, but it must still reread the reviewed artifact and any receipt evidence
before driving `aoa-session-donor-harvest`, `aoa-session-progression-lift`, and
`aoa-quest-harvest`.
