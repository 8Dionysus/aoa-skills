# Validation Map

This directory holds the human route map for validator ownership in
`aoa-skills`.

Start with [`VALIDATOR_TOPOLOGY.md`](VALIDATOR_TOPOLOGY.md) when changing a
validator, lint, build check, audit, report, CI lane, or release gate.

The machine-readable inventory is
[`validator_inventory.json`](validator_inventory.json). It exists so tests can
catch orphan validation-like entrypoints before they become hidden gates.
