# Session Growth Kernel Maturity

This note marks the Wave 4 maturity seam for the remaining project-core
session-growth kernel skills inside `aoa-skills`.

The live route stays:

`aoa-sdk -> aoa-skills -> aoa-playbooks -> aoa-stats`

Inside this repo, the Wave 4 home is the existing
`examples/session_growth_artifacts/` family. The staging pack suggested
`examples/session-growth-kernel/`; this repo keeps the live family name instead
of creating a second competing example tree.

## Scope

This Wave 4 seam gives reviewed packet and receipt examples to:

- `aoa-automation-opportunity-scan`
- `aoa-session-route-forks`
- `aoa-session-self-diagnose`
- `aoa-session-self-repair`
- `aoa-session-progression-lift`

It stays subordinate to:

- reviewed closeout carry in `aoa-sdk`
- reviewed candidate identity in `CANDIDATE_REF_REFINERY.md`
- owner truth, proof truth, and approval gates in downstream repos

## Boundary

These examples are:

- reviewed packet and receipt witnesses
- recommendation-only
- append-only
- bounded by the project-core kernel finish stage

These examples are not:

- scheduler truth
- hidden execution
- seed minting
- object truth
- silent mutation authority

`aoa-skills` may carry `candidate_ref` here only because the reviewed minting
seam already happened earlier. It must not mint `seed_ref` or `object_ref`
here.

## Minimal Example Contract

Each Wave 4 packet keeps:

- `source_reviewed_artifact_ref`
- strongest available lineage refs
- one owner hint or owner target
- `status_posture`
- one explicit stop or defer condition

Each Wave 4 detail receipt:

- cites the packet in `evidence_refs`
- stays smaller than the packet
- uses the existing skill-local receipt kind
- does not replace packet meaning

Each Wave 4 core receipt:

- uses `core_skill_application_receipt`
- points back to the bounded detail receipt
- stays `application_stage: finish`
- remains weaker than the detail receipt it names

## Live Example Family

Wave 4 examples live in:

- `examples/session_growth_artifacts/*.wave4.json`
- `examples/session_growth_artifacts/core_skill_application_receipts.wave4.json`

The shared reviewed closeout source for this slice is:

- `repo:aoa-sdk/examples/closeout_followthrough_decision.example.json`

The shared kernel contract remains:

- `config/project_core_skill_kernel.json`
- `scripts/publish_core_skill_receipts.py`

A generated kernel-maturity summary is intentionally deferred until the repo
has a builder for it. The source-authored doc and examples remain the live
truth for this slice.
