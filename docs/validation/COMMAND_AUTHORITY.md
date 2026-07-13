# Validation Command Authority

Validation commands use a hybrid authority model:

- `config/validation_lanes.json` is the canonical storage surface for full
  blocking lane command sequences and drift-path lists.
- `scripts/lanes/validation_lanes.py` is the loader/API for Python callers.
  Root `scripts/validation_lanes.py` is only compatibility ingress and a safe
  manifest-inspection CLI. Neither path may grow a second copy of lane
  sequences.
- Blocking lane sequences should name implementation modules under their
  script organ directories. Only allowlisted root `scripts/*.py` wrappers are
  compatibility front doors; they are not command-authority owners.
- Nearest `AGENTS.md` cards may name focused owner checks, lane ids, and local
  next routes for the changed surface.
- A canonical topical guide may keep focused command examples when that file is
  the primary owner of the operation: release, install/profile, runtime,
  component refresh, report generation, external conformance, MCP wiring, or
  an eval runner/suite contract. It must not copy a full blocking lane sequence
  already owned by `config/validation_lanes.json`.
- GitHub workflow YAML should call the lane entrypoint or release helper. It
  should not rebuild lane meaning inline.
- Decision records, changelogs, receipts, landing logs, legacy captures, and
  neighboring runbooks preserve verification scope or outcome, not executable
  command snippets.

Use this balance when adding or moving validation:

1. Put full repeated sequences in `config/validation_lanes.json`.
2. Keep local focused commands in the nearest `AGENTS.md` or canonical topical
   command owner when they help an agent or operator use that exact surface.
3. Record owner, lane, mode, callers, and failure route in
   `docs/validation/validator_inventory.json`.
4. Update tests when a new command store or workflow route is introduced.

Do not put executable validation or test commands in neighboring Markdown just
because a check was run there once. Outside the nearest focused `AGENTS.md`, a
canonical topical command owner, or an executable instruction-source home,
active and historical documents express the lane id, checked scope, result, or
owner route instead. Canonical skill bundles under `skills/` and portable agent
instruction sources under `.agents/` remain executable instruction owners;
they are not general documentation command stores.
