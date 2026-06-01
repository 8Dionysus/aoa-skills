# Docs Map

This directory routes readable documentation for the AoA skill system.
It should stay a map, not a second README, release log, mechanics atlas, or
generated-surface summary.

## First Routes

| Need | Start Here |
|---|---|
| Repository authority boundary | [`../CHARTER.md`](../CHARTER.md) |
| System form | [`../DESIGN.md`](../DESIGN.md) |
| Agent-facing form | [`../DESIGN.AGENTS.md`](../DESIGN.AGENTS.md) |
| Technical source/generated/export model | [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| Repository layout | [`REPOSITORY_STRUCTURE.md`](REPOSITORY_STRUCTURE.md) |
| Validator topology and inventory | [`validation/VALIDATOR_TOPOLOGY.md`](validation/VALIDATOR_TOPOLOGY.md) |
| Validation command authority | [`validation/COMMAND_AUTHORITY.md`](validation/COMMAND_AUTHORITY.md) |
| Test topology and inventory | [`testing/TEST_TOPOLOGY.md`](testing/TEST_TOPOLOGY.md) |
| Current skill map | [`../SKILL_INDEX.md`](../SKILL_INDEX.md) |
| Canonical skill bundles | [`../skills/README.md`](../skills/README.md) |
| Owner-local mechanics | [`../mechanics/README.md`](../mechanics/README.md) |
| Release path | [`../mechanics/release-support/docs/RELEASING.md`](../mechanics/release-support/docs/RELEASING.md) |

## Owner Surfaces

| Question | Owner Surface |
|---|---|
| Where do sibling owner boundaries sit? | [`../mechanics/boundary-bridge/docs/LAYER_POSITION.md`](../mechanics/boundary-bridge/docs/LAYER_POSITION.md) |
| How are AoA center requests received here? | [`../mechanics/OWNER_REQUEST_RECEIPTS.md`](../mechanics/OWNER_REQUEST_RECEIPTS.md) |
| Where are requested Agon workflows bounded before skill landing? | [`../mechanics/agon/parts/workflow-candidate-bridge/README.md`](../mechanics/agon/parts/workflow-candidate-bridge/README.md) |
| How do skills move through maturity? | [`../mechanics/method-growth/docs/PROMOTION_PATH.md`](../mechanics/method-growth/docs/PROMOTION_PATH.md) |
| How is repeated use routed to review pressure? | [`../mechanics/method-growth/docs/PROMOTION_PRESSURE.md`](../mechanics/method-growth/docs/PROMOTION_PRESSURE.md) |
| Where are owner landing status surfaces bounded? | [`../mechanics/method-growth/docs/OWNER_STATUS_SURFACES.md`](../mechanics/method-growth/docs/OWNER_STATUS_SURFACES.md) |
| Where is owner follow-through kept non-runtime? | [`../mechanics/method-growth/docs/GOVERNED_FOLLOWTHROUGH.md`](../mechanics/method-growth/docs/GOVERNED_FOLLOWTHROUGH.md) |
| How is runtime use inspected? | [`../mechanics/release-support/docs/RUNTIME_PATH.md`](../mechanics/release-support/docs/RUNTIME_PATH.md) |
| How are generated/export surfaces refreshed? | [`../mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md`](../mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md) |
| Where is evaluation evidence read? | [`../mechanics/audit/docs/EVALUATION_PATH.md`](../mechanics/audit/docs/EVALUATION_PATH.md) |
| Where is public status read? | [`../mechanics/audit/docs/PUBLIC_SURFACE.md`](../mechanics/audit/docs/PUBLIC_SURFACE.md) |
| Where is session-growth kernel maturity tracked? | [`../mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md`](../mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md) |
| Where are session-harvest notes kept? | [`../mechanics/growth-cycle/session-harvests/README.md`](../mechanics/growth-cycle/session-harvests/README.md) |

## Review And History

| Surface | Role |
|---|---|
| [`decisions/`](decisions/README.md) | decision records for structural, workflow, and ownership changes |
| [`reviews/`](reviews/) | review records for status, canonical candidates, and exceptions |
| [`AGENTS_ROOT_REFERENCE.md`](AGENTS_ROOT_REFERENCE.md) | preserved historical root guidance; not the active command or authority source |

Generated files under `../generated/`, portable exports under
`../.agents/skills/`, and Spark lane packets under `../.agents/spark/` are
reader, runtime, transport, or agent-lane companions. Follow them back to source
bundles, source config, review records, mechanics packages, or builders before
changing meaning.
