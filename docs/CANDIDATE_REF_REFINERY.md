# Candidate Ref Refinery

This note defines the `aoa-skills` side of the Growth Refinery lineage route.

The route stays:

`cluster_ref -> candidate_ref -> seed_ref -> object_ref`

`aoa-skills` is the first honest home of reviewed `candidate_ref`.

It is not:

- the first home of `cluster_ref`
- the first home of `seed_ref`
- the final home of planted `object_ref`

Once `candidate_ref` exists, the next reviewed owner-local tracked surfaces are:

- `docs/OWNER_STATUS_SURFACES.md`
- `docs/GOVERNED_FOLLOWTHROUGH.md`

## Boundary

`aoa-skills` may:

- mint `candidate_ref` after reviewed donor harvest
- preserve incoming `cluster_ref`
- preserve `owner_hypothesis`
- preserve `owner_shape`
- preserve `nearest_wrong_target`
- preserve `evidence_refs`
- preserve `status_posture`
- preserve `supersedes`
- preserve `merged_into`
- preserve `drop_reason`

`aoa-skills` must not:

- mint `candidate_ref` before reviewed donor harvest
- mint `seed_ref`
- mint `object_ref`
- collapse reviewed candidate identity into final owner truth
- treat `aoa-routing` or `aoa-kag` as first-authoring homes

## Existing Home

Reviewed candidate identity remains anchored in the existing donor-harvest path:

- `skills/aoa-session-donor-harvest/SKILL.md`
- `skills/aoa-session-donor-harvest/references/harvest-packet-receipt-schema.yaml`
- `skills/aoa-session-donor-harvest/references/candidate-lineage-receipt-schema.yaml`
- `examples/session_growth_artifacts/candidate_lineage_receipt.alpha.json`
- `examples/reviewed_owner_landing_bundle.example.json`
- `examples/route_followthrough_decision.example.json`

This wave patches the existing `harvest_packet_receipt` shape.
It does not create a second competing receipt kind.

## Minting Rule

Mint `candidate_ref` only when:

- the source session artifact is reviewed
- the reusable unit is bounded
- the owner hypothesis is explicit
- the nearest wrong target is explicit
- the candidate survives theme-only rejection

## Negative Rules

Do not:

- mint `candidate_ref` from live session residue
- treat donor harvest as proof that an owner repo already accepted the unit
- collapse a mixed multi-owner route into one fake candidate
- widen the route so far that the candidate stops being bounded

## Later Neighbor

For the later reviewed packet and receipt route that uses existing
`candidate_ref` without turning it into seed or object truth, read
`SESSION_GROWTH_KERNEL_MATURITY.md`.
