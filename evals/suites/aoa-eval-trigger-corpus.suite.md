---
schema_version: local_eval_suite_note_v1
owner_repo: aoa-skills
status: draft
authority_boundary: no verdict, scoring, regression, or proof doctrine authority
---

# aoa-eval trigger corpus

## Scope

This local suite records trigger pressure for the `aoa-eval` skill family. It
is a repo-local corpus for future trigger checks, not a central `aoa-evals`
bundle.

The suite protects one question:

```text
Can a future agent decide whether the right next route is an existing eval,
a validator/test/script, local eval intake/design, session mining, an owner
boundary stop, or no eval route at all?
```

## Owner Boundary

- `aoa-skills` owns the skill trigger behavior, skill-evaluation fixtures,
  local suite note, and local report note.
- `aoa-evals` owns central proof doctrine, central eval bundles, scoring,
  verdicts, regression promotion, and local eval-port validation standards.
- `.aoa` owns raw transcript evidence, generated segments, search provider
  status, and freshness. Session hits here are candidate evidence only.
- `aoa-evals-mcp` is an access plane. It may inspect or plan local-port writes,
  but it must not create central proof truth.

## Trigger Classes

### should_use_aoa_eval_router

- route: `aoa-eval`
- source: active long-session goal
- session: `019eb8c7-a7b5-76f0-b66a-0eb3791305ff`
- label: `2026-06-11__006__у-меня-складывается-впечатление-что-для-всех`
- segment: `039__compaction-to-compaction.md#event-007511--user_intent--user-message`
- raw ref: `raw:line:7511`
- freshness: `fresh`, `segment_index_live_check: fresh`
- reason: the objective explicitly asks for an eval router that detects eval
  moments, selects/applies existing evals, designs local pressure when none fit,
  and preserves owner boundaries.

### should_use_existing_eval_select_or_apply

- route: `aoa-eval-select`, then `aoa-eval-apply` when a surface is selected
- source: earlier session candidate from the research packet
- session: `019e5c96-3c6b-7382-a17d-4d76a4d4c079`
- label: `2026-05-25__001__давай-дошлифуем-рефакторинг-aoa-evals-вопрос-в`
- segment: `039`
- events: `004823`, `004824`, `004615`
- reason: the cluster involved `aoa-evals-mcp` source, tests, validators, and
  verification gaps. The expected behavior is to inspect existing central/local
  surfaces before designing anything new.

### should_design_missing_or_local_need

- route: `aoa-eval-local-need` or `aoa-eval-design`
- source: earlier session candidate from the research packet
- session: `019e9388-dc4c-7f82-b6bf-04bea3aed7f4`
- label: `2026-06-04__003__у-нас-в-отрефакторенных-репо-есть-определенным`
- segment: `077`
- events: `014678`, `014680`
- reason: the cluster involved `aoa-evals-mcp`, evidence candidates, and local
  eval-port access-plane pressure. If no existing eval fits, the right output is
  bounded local intake or a draft local suite/report.

### should_run_validator_or_test

- route: `aoa-eval-select`, then the selected validator, test, or script
- source: earlier session candidate from the research packet
- session: `019e8f02-62ef-7931-ab39-631e4bde80a8`
- label: `2026-06-03__006__в-aoa-evals-мы-только-только-провели`
- segments: `025`, `030`, `039`, `070`, `072`, `074`, `080`
- reason: the cluster involved validator/test refactors and mechanics proof
  pressure. The trigger should prefer an existing deterministic surface before
  creating new eval intake.

### should_not_trigger_eval

- route: no `aoa-eval` trigger
- source: existing deterministic skill-evaluation fixture
- fixture case: `eval_router_plain_unit_test`
- fixture file: `tests/fixtures/skill_evaluation_cases.yaml`
- snapshot:
  `tests/fixtures/skill_evaluation_snapshots/aoa-eval/eval_router_plain_unit_test.md`
- reason: an ordinary unit test for a local helper with no eval routing,
  repeated proof gap, regression, or local eval-port question belongs to the
  normal engineering route, not the eval router.

### owner_boundary_unclear

- route: `aoa-eval-select` plus owner-boundary stop line
- source: active long-session local-port/MCP evidence
- session: `019eb8c7-a7b5-76f0-b66a-0eb3791305ff`
- label: `2026-06-11__006__у-меня-складывается-впечатление-что-для-всех`
- segment:
  `032__compaction-to-compaction.md#event-006805--security_touchpoint--tool-output-call_1gya9un2du6ytrl6uhn3zfjj`
- raw ref: `raw:line:6805`
- freshness: `fresh`, `segment_index_live_check: fresh`
- reason: MCP and local-port write surfaces can create local pressure files, but
  the router must stop before treating MCP output as central proof authority.

### session_mining_after_gates

- route: `aoa-eval-session-mining`
- source: active long-session web/repo synthesis before session mining
- session: `019eb8c7-a7b5-76f0-b66a-0eb3791305ff`
- label: `2026-06-11__006__у-меня-складывается-впечатление-что-для-всех`
- segment:
  `038__compaction-to-compaction.md#event-007506--assistant_message--assistant-message`
- raw ref: `raw:line:7506`
- freshness: `fresh`, `segment_index_live_check: fresh`
- reason: the mining route should run only after web evidence, repo-local eval
  ports, validators/tests/scripts, skill surfaces, and owner boundaries have
  already shaped the trigger taxonomy.

### trigger_eval_regression

- route: `aoa-eval-design` for local trigger regression corpus, then skill
  evaluation fixtures
- source: earlier session candidate from the research packet
- session: `019dfb8e-2e54-7f92-9eb2-f26b13eeaa2d`
- label: `2026-05-06__001__хорошо-делай`
- segments: `008`, `009`, `027`, `046`, `048`, `053`
- reason: the cluster involved description-trigger evals, trigger lint, and
  tiny-router validation. It belongs in trigger-behavior coverage rather than
  central proof adoption.

## Checks This Suite Expects

- The router names exactly one route for each pressure point.
- Existing evals, validators, tests, and scripts are inspected before local
  intake or design.
- Session-derived cases include session id, segment ref, raw ref when
  available, and freshness.
- Negative cases stay negative when there is no eval-lane pressure.
- Owner-boundary cases name the wrong route and stop before proof authority
  moves out of `aoa-evals`.
- Local files remain candidate evidence until reviewed by the proper owner.
