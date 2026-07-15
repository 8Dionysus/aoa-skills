# Validation Command Authority

`config/validation_lanes.json` is the only source of repeated blocking command
sequences. `scripts/lanes/validation_lanes.py` loads it;
`scripts/lanes/ci_gate.py` and `scripts/lanes/release_check.py` execute it.
Root script wrappers are compatibility ingress only.

Nearest `AGENTS.md` cards may name one focused check or lane, but should not
copy the full sequence. CI should call a lane entrypoint. Historical decisions,
reviews, and receipts record results or rationale, never become command stores.

Adding a command requires a durable owner invariant, a live implementation,
clear effect posture, and a failure route. Do not add a command solely to make
a refactor appear covered.
