# aoa-property-invariants status promotion review

## Current status

- current maturity status: `scaffold`
- scope: `core`
- current lineage: manifest-aligned with published techniques `AOA-T-0017` and `AOA-T-0007`

## Target status

- target maturity status: `evaluated`
- why this target now: published lineage, support-example guidance, and behavior-oriented evaluation coverage now exist together

## Evidence reviewed

- `skills/aoa-property-invariants/SKILL.md`
- `skills/aoa-property-invariants/techniques.yaml`
- `skills/aoa-property-invariants/examples/example.md`
- `tests/fixtures/skill_evaluation_cases.yaml`

## Findings

- the trigger boundary is coherent around broad behavioral truths and meaningful invariants rather than narrow snapshots
- published lineage is already clean, pinned, and free of placeholder metadata
- evaluation coverage exists for runtime self-containment, one `use` case, and multiple `do_not_use` boundary cases
- the example reinforces invariant-oriented coverage instead of widening the skill into generic exploratory testing

## Gaps and blockers

- no technical blocker remains for `evaluated`
- `canonical` is still deferred because this pass does not establish that `aoa-property-invariants` should yet be the default public reference for property-oriented testing

## Recommendation

Promote `aoa-property-invariants` to `evaluated` in the next PR.
Keep `canonical` deferred to a separate review and promotion decision.
