# aoa-adr-write status promotion review

## Current status

- current maturity status: `scaffold`
- current machine-checkable floor: manifest-aligned, but still depends on pending technique `AOA-T-PENDING-ADR-WRITE`
- scope: `core`
- current lineage: pending upstream lineage plus a bounded ADR-writing workflow surface

## Target status

- target maturity status: `evaluated`
- why this target now: the skill already has a sharp decision-recording boundary, reviewable inputs/outputs, and a bounded verification step, so the remaining work is promotion evidence rather than a meaning change
- next status after this step: `canonical` remains deferred until published lineage exists and a separate default-use decision is recorded

## Evidence reviewed

- `skills/aoa-adr-write/SKILL.md`
- `skills/aoa-adr-write/techniques.yaml`
- `skills/aoa-adr-write/examples/example.md`
- repository-level promotion conventions in `templates/STATUS_PROMOTION_REVIEW.template.md`

## Findings

- the trigger boundary is crisp around decisions that change structure, boundaries, tooling, or workflow expectations
- the workflow is bounded to recording rationale, tradeoffs, and consequences rather than narrating a diff
- the current pending lineage remains honest and does not block `evaluated`
- the skill does not widen into general architecture governance or source-of-truth classification

## Gaps and blockers

- pending upstream technique lineage remains unresolved, so `canonical` stays blocked
- `aoa-adr-write` still depends on the shared evaluation fixture surface for repository-level evaluated coverage

## Recommendation

Promotion to `evaluated` is appropriate in this pass.
Keep `canonical` deferred until the upstream ADR-writing technique is published and refreshed.
