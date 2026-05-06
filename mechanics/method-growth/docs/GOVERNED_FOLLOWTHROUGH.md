# Governed Followthrough

Use this note after a reviewed candidate already has owner-local landing
context and the next question is: what is the next honest bounded move?

This surface is the reviewed decision layer that sits beside
`OWNER_STATUS_SURFACES.md`. It keeps one explicit next-step verdict visible
without pretending that the route already ran.

## Purpose

Once `candidate_ref` exists, the route may still need one small reviewable
decision:

- land directly in the owner repo
- stage a seed
- reanchor the owner
- prove first
- merge into an existing tracked object
- defer
- drop

The decision stays bounded and reviewed. It does not become a queue, a runner,
or schedule authority.

## Required Carry

Each decision keeps:

- `candidate_ref`
- strongest available earlier lineage refs when known
- `owner_repo`
- `owner_shape`
- `nearest_wrong_target`
- `verdict`
- `why_now`
- `why_not_nearest_wrong_target`
- `next_artifact_kind`
- `stop_conditions`
- `approval_posture`
- `evidence_refs`

## Allowed Verdicts

- `land_direct`
- `stage_seed`
- `reanchor_owner`
- `prove_first`
- `merge_into_existing`
- `defer`
- `drop`

## Negative Rules

Do not:

- call this a live queue
- call this a scheduler right
- infer owner truth from seed staging alone
- infer proof completion from owner landing alone
- mint `seed_ref` or `object_ref` here

If the verdict changes later, write a new reviewed decision or a reviewed owner
status update instead of silently overwriting the old one.
