# Candidate Lineage Contract

`aoa-skills` is the first owner layer where a reviewed reusable unit may receive
`candidate_ref`.

## Main rule

`aoa-session-donor-harvest` may mint `candidate_ref` only after:

- the session artifact is reviewed
- the reusable unit is bounded
- one chosen owner hypothesis exists
- one nearest-wrong target was considered honestly

Checkpoint carry may arrive with `cluster_ref`, owner hints, evidence refs, and
status posture, but it stays provisional until donor harvest performs the
reviewed owner-shaping pass.

For the shorter donor-harvest bridge note, read
`docs/CANDIDATE_REF_REFINERY.md`.
For the next owner-local tracked surfaces after `candidate_ref` exists, read
`docs/OWNER_STATUS_SURFACES.md` and `docs/GOVERNED_FOLLOWTHROUGH.md`.

## Required carried fields

Each accepted donor-harvest candidate should keep:

- `candidate_ref`
- `cluster_ref` when available
- `owner_hypothesis`
- `owner_shape`
- `nearest_wrong_target`
- `status_posture`
- `evidence_refs`
- `supersedes`
- `merged_into`
- `drop_reason`

## Negative rules

Do not:

- mint `candidate_ref` from an unreviewed session
- mint `candidate_ref` for vague theme clouds or resonance-only residue
- route first-authoring candidate identity into `aoa-routing` or `aoa-kag`
- confuse `candidate_ref` with planted seed identity or final owner object
