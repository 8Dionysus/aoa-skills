---
schema_version: local_eval_report_note_v1
owner_repo: aoa-skills
status: draft
title: aoa-eval battle path
summary: End-to-end local eval-port route through aoa-evals-mcp, aoa-eval-apply, deterministic
  skill checks, session refs, and post-write local-port validation.
refs:
- docs/aoa-eval-skill-family-research.md
- evals/suites/aoa-eval-trigger-corpus.suite.md
- evals/reports/aoa-eval-session-mining.report.md
- evals/reports/aoa-eval-runtime-adoption-20260621.report.md
authority_boundary: no verdict, scoring, regression, or proof doctrine authority
---

## Scope

This report records one end-to-end `aoa-eval` battle path through a real OS
Abyss repo-local eval port.

Chosen repo: `aoa-skills`.

Reason: the central local-port inventory classifies `aoa-skills` as an active
repo-local port with one suite and three report notes. Its route recommendation
is `active_suite_apply_or_regression_check`, subskill `aoa-eval-apply`.

This is local evidence only. It does not compute verdicts, scoring, regression
truth, or central `aoa-evals` proof doctrine.

## Route

Question:

> Does the `aoa-eval` skill trigger and route OS Abyss eval pressure through
> existing local surfaces before designing new evals?

Route decision:

1. Inspect live local-port inventory from central `aoa-evals`.
2. Inspect `aoa-skills` through `aoa-evals-mcp`.
3. Prefer the existing local trigger suite and skill validators.
4. Run deterministic local checks.
5. Write this repo-local battle-path report through the bounded MCP local
   report writer.
6. Validate the local eval port after mutation.

## MCP Evidence

The `aoa-evals-mcp` local-port view read the current `aoa-skills` port from the
`abyss-stack` source checkout.

Observed:

- status: `active`
- counts: `intake=0`, `suites=1`, `reports=3`, `active_pressure=4`
- route key: `active_suite_apply_or_regression_check`
- route: `aoa-eval-apply`
- validation: valid with no issues

The `aoa-evals-mcp` `find-or-propose-local` read used the `aoa-skills` owner
and asked whether existing local surfaces route eval pressure before new eval
design.

Observed:

- local port remains active
- route recommendation remains `aoa-eval-apply`
- no central match or proposal was promoted
- no `eval_need_v1` was created because existing local surfaces are the right
  first route

## Applied Checks

The local suite points to deterministic skill-router and trigger surfaces rather
than model-scored central proof.

Checks run for this battle path:

- central local-port protocol validation;
- focused `aoa-eval` skill validation and tests;
- trigger and description-trigger lint;
- the `source-fast` lane.

Observed results:

- local eval-port validation passed
- `aoa-eval` skill validation passed
- focused pytest passed: `5 passed, 21 subtests passed`
- trigger lint passed: 219 trigger cases across 56 skills
- description-trigger lint passed: 265 cases across 56 skills
- source-fast gate passed

Post-write local-port validation reran the central protocol against this owner.

Observed result: `Local eval port validation passed.`

Post-write MCP readback used the `aoa-evals-mcp` local-port view for
`aoa-skills`.

Observed:

- status: `active`
- counts: `intake=0`, `suites=1`, `reports=4`, `active_pressure=5`
- validation: valid with no issues

## Session Evidence

Session mining used portable SQLite search, not stale graph state. Current
trigger-family refs are recorded in:

- `evals/reports/aoa-eval-session-mining.report.md`
- `docs/aoa-eval-skill-family-research.md`

Representative refs:

- `2026-06-11__006`, `083__compaction-to-compaction.md#event-015025`,
  `raw:line:15025`: MCP dry-run local report write.
- `2026-06-11__006`, `083__compaction-to-compaction.md#event-015032`,
  `raw:line:15032`: MCP apply local report write.
- `2026-06-11__006`, `088__compaction-to-compaction.md#event-015320`,
  `raw:line:15320`: workspace-wide local `evals/` discovery pressure.
- `2026-06-11__006`, `091__compaction-to-compaction.md#event-015941`,
  `raw:line:15941`: validator/schema failure that should route to apply or
  repair.

## Conclusion

The battle path works for this slice:

- local `evals/` port discovery identifies the right active repo;
- `aoa-evals-mcp` routes to `aoa-eval-apply`;
- existing suite/report surfaces are preferred over creating a new intake;
- deterministic local checks validate the trigger corpus and skill surface;
- MCP writes only a bounded local report note under `evals/reports/`;
- central `aoa-evals` proof adoption is not warranted yet.

Next scaling step: build a small prompt-trigger harness over the existing
`skill_evaluation_cases.yaml` and snapshots so runtime skill choice can be
checked as a repeatable single-step route eval, not only by manual prompt
inspection.
