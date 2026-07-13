# Local Suites

Local deterministic suite notes and fixtures can live here when they protect
skill-owned workflow, trigger, or export contracts.

Suites here do not own central verdict, scoring, regression, or proof doctrine.
Route portable proof bundles to `aoa-evals`.

Active local suite notes:

- [aoa-eval-trigger-corpus.suite.md](aoa-eval-trigger-corpus.suite.md) captures
  the first `aoa-eval` trigger corpus with session refs, owner routes, and a
  no-trigger case.
- [aoa-skill-live-dispatch-harness.suite.md](aoa-skill-live-dispatch-harness.suite.md) defines
  bounded smoke, pilot, pilot-return, collision, and coverage-closure cohorts.
  Its live runs require exact confirmation and host resource/storage gates; its
  deterministic harness contract is the only part eligible for ordinary
  local-suite execution.
  [aoa-skill-live-dispatch-procedures.json](aoa-skill-live-dispatch-procedures.json)
  holds source-authored selected-child and procedure-disposition expectations.
  [aoa-skill-live-dispatch-outcomes.json](aoa-skill-live-dispatch-outcomes.json)
  separately holds bounded owner-action choices. Missing outcome contracts
  remain explicitly unscored; the independent fixture probe and whole-task
  completion stay separate, broad fixture inventory and outcome-validator
  inspection are rejected, and live observations cannot write or inspect their
  own answer key. The current pilot corpus covers all 11 implicit pairs on both
  procedure and owner-action axes; live execution still requires exact source
  and high-cost confirmation plus all host/runtime preflights.
