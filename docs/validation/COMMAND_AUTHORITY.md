# Validation Command Authority

Validation commands use a hybrid authority model:

- `config/validation_lanes.json` is the canonical storage surface for full
  blocking lane command sequences and drift-path lists.
- `scripts/validation_lanes.py` is a loader and compatibility API for Python
  callers. It must not grow its own second copy of lane sequences.
- Nearest `AGENTS.md` cards may name focused owner checks, lane ids, and local
  next routes for the changed surface.
- GitHub workflow YAML should call `scripts/ci_gate.py --mode ...` or the
  release helper entrypoint. It should not rebuild lane meaning inline.
- Historical decision records, changelogs, landing logs, legacy captures, and
  command-owner runbooks may preserve command evidence or usage examples, but
  they are not active lane authority.

Use this balance when adding or moving validation:

1. Put full repeated sequences in `config/validation_lanes.json`.
2. Keep local focused commands in the nearest `AGENTS.md` only when they help an
   agent iterate on that owner surface.
3. Record owner, lane, mode, callers, and failure route in
   `docs/validation/validator_inventory.json`.
4. Update tests when a new command store or workflow route is introduced.

Do not put validation command blocks in active route, topology, audit, quest, or
scenario documentation when the same route can be expressed as a lane id,
focused owner surface, or nearest `AGENTS.md` pointer.
