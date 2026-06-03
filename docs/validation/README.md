# Validation Map

This directory holds the human route map for validator ownership in
`aoa-skills`.

Start with [`SCRIPT_TOPOLOGY.md`](SCRIPT_TOPOLOGY.md) when moving scripts,
adding script organs, or changing root ingress paths.

Use [`VALIDATOR_TOPOLOGY.md`](VALIDATOR_TOPOLOGY.md) when changing a validator,
lint, build check, audit, report, CI lane, or release gate.

Use [`COMMAND_AUTHORITY.md`](COMMAND_AUTHORITY.md) before moving validation
commands between the lane manifest, Python callers, GitHub workflow YAML, and
nearest `AGENTS.md` cards.

The validator machine-readable inventory is
[`validator_inventory.json`](validator_inventory.json). It exists so tests can
catch orphan validation-like entrypoints before they become hidden gates.

The script organ inventory is [`script_inventory.json`](script_inventory.json).
