# Owner Status Surfaces

Use this note after `candidate_ref` already exists and the next honest move is a
reviewed owner-local landing that is still weaker than final object truth.

`aoa-skills` owns the first tracked owner-status landing for skill-layer
candidates. It does not turn that landing into seed truth, proof truth, or a
stable landed object by itself.

For the candidate minting seam that happens before this surface, read
`CANDIDATE_LINEAGE_CONTRACT.md` and `CANDIDATE_REF_REFINERY.md` first.

## Purpose

This surface exists so a reviewed candidate does not remain only in:

- runtime-local `.aoa` carry
- chat memory
- seed staging
- implied future work

It is the first honest owner-side place to track:

- first owner landing
- reanchor after owner-fit correction
- thin-evidence holding
- later merge
- later supersession
- honest drop

## Boundary

This surface is:

- reviewed-only
- tracked status
- owner-local
- weaker than landed owner object truth

This surface is not:

- raw checkpoint carry
- seed truth
- final object truth
- proof authority
- scheduler authority

It must not mint `seed_ref` or `object_ref`.

## Required Identity

Each reviewed owner landing keeps:

- `candidate_ref`
- strongest available earlier lineage refs when known, especially `cluster_ref`
- `owner_repo`
- `owner_shape`
- `nearest_wrong_target`
- `evidence_refs`
- `reviewed_at`
- `status_note`

## Status Posture

Keep the live Growth Refinery posture grammar and widen it only for explicit
terminal owner outcomes:

- `early`
- `reanchor`
- `thin-evidence`
- `stable`
- `merged`
- `superseded`
- `dropped`

`thin-evidence` keeps the existing repo grammar. Do not introduce a second
spelling such as `thin_evidence` here.

## Update Law

Use explicit update fields instead of silent replacement:

- `supersedes`
- `superseded_by`
- `merged_into`
- `drop_reason`
- `drop_stage`
- `drop_evidence_refs`

If the landing moves into `merged`, `superseded`, or `dropped`, the terminal
metadata must become explicit and reviewable in the same surface.

## Neighbor Surface

After this landing exists, the next bounded route verdict belongs in
`GOVERNED_FOLLOWTHROUGH.md`.
