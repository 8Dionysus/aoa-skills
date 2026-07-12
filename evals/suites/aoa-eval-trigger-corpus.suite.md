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

Can a future agent decide whether the right next route is an existing eval, a
validator/test/script, local eval intake/design, session mining, an owner
boundary stop, or no eval route at all?

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

### session_front_door_first

- route: `aoa-eval`
- source: active OS Abyss eval-control work
- fixture case: `eval_router_session_front_door`
- fixture file: `tests/fixtures/skill_evaluation_cases.yaml`
- required command when `aoa-evals` is available:
  `python scripts/aoa_eval_session_start.py --json`
- required Forge front-door refs when the readiness packet exposes them:
  `EVAL_FORGE_OPERATING_PATH.md`, `SESSION_MINING_CRITERIA.md`,
  `LOCAL_PORT_DECISION_MATRIX.md`, latest route-review report, worksheet
  example, and exact route commands
- candidate validator before session evidence:
  `python scripts/validate_eval_candidate_packets.py --schema-only`
- reason: a new agent session must raise the current eval-control read model
  and Eval Forge front door before selecting tools, writing local eval files, or
  importing session evidence. The packet is a route aid only; it cannot score,
  promote, or accept proof.

### route_signs_without_keywords

- route: `aoa-eval`
- source: Eval Forge dogfood candidate packet
- candidate packet:
  `/srv/AbyssOS/aoa-evals/mechanics/audit/parts/candidate-readers/packets/session-mining/aoa-eval-keyword-mining-blindspot.eval_candidate.json`
- Forge owner route: `aoa-skills` / `trigger_design_case`
- fixture case: `eval_router_route_sign_without_eval_keyword`
- fixture file: `tests/fixtures/skill_evaluation_cases.yaml`
- snapshot:
  `tests/fixtures/skill_evaluation_snapshots/aoa-eval/eval_router_route_sign_without_eval_keyword.md`
- reason: the candidate exposed a blind spot in keyword-based session mining.
  A future agent should trigger `aoa-eval` from route signs: repeated
  validation/proof pressure, skipped validator or test evidence, unsafe
  proof/local/MCP/session mixing, active-vs-stale uncertainty, or missed
  trigger behavior. The user or agent does not need to literally say `eval`.
  The source packet remains candidate-only and carries no proof authority.

### keyword_only_reject

- route: no `aoa-eval` trigger
- fixture case: `eval_router_keyword_only_noise`
- fixture file: `tests/fixtures/skill_evaluation_cases.yaml`
- snapshot:
  `tests/fixtures/skill_evaluation_snapshots/aoa-eval/eval_router_keyword_only_noise.md`
- reason: keywords alone such as `eval`, `test`, `landing`, or `done` are not
  enough. The router needs route pressure: an owner-boundary question,
  repeated failure, proof gap, selected evaluation surface, local eval-port
  pressure, or session/trace candidate evidence.

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

Additional live dogfood case:

- route: `aoa-eval-select`, then `aoa-eval-apply` as a local report
- source: active long-session self-awareness contract-lane episode
- session: `019eb8c7-a7b5-76f0-b66a-0eb3791305ff`
- label: `2026-06-11__006__у-меня-складывается-впечатление-что-для-всех`
- trigger segment:
  `017__compaction-to-compaction.md#event-003667--user_intent--user-message`
- raw ref: `raw:line:3667`
- report:
  `evals/reports/aoa-eval-self-awareness-contract-lane.report.md`
- selected eval surfaces: `aoa-diagnosis-cause-discipline`,
  `aoa-repair-boundedness`, `aoa-verification-honesty`, and
  `aoa-approval-boundary-adherence`
- reason: the cluster involved emotionally loaded suspected drift, active-vs-
  stale host ownership, bounded repair, and residual live validation risk. The
  expected behavior is to select existing central eval surfaces and publish a
  local readout instead of designing a new bundle first.

Fixture-backed generalization:

- route: `aoa-eval`
- fixture cases: `eval_router_drifted_contract_lane`,
  `eval_router_active_vs_stale_cleanup_boundary`, and
  `eval_router_source_authority_only`
- fixture file: `tests/fixtures/skill_evaluation_cases.yaml`
- reason: the self-awareness episode is only the observed specimen. The durable
  trigger family is broader: suspicious drift in an authority-sensitive contract
  lane, active-vs-stale cleanup pressure before deletion, and the negative
  boundary where the task is only source-authority lookup rather than eval-lane
  work.

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

### selected_local_suite_jit_apply

- route: `aoa-eval-apply`
- fixture case: `eval_apply_selected_local_suite_sidecar`
- fixture file: `tests/fixtures/skill_evaluation_cases.yaml`
- snapshot:
  `tests/fixtures/skill_evaluation_snapshots/aoa-eval-apply/eval_apply_selected_local_suite_sidecar.md`
- selected source surface: reviewed
  `evals/suites/<slug>.suite.json` with
  `schema_version: local_eval_suite_execution_v1`
- owner handoff: the current `aoa-evals` local-port validator must report
  `source-contract-ready` against the selected source tree immediately before
  execution
- reason: discovery, readiness, dashboard, and MCP packets may identify a
  runnable candidate but may not invoke it. The repo owner or
  `aoa-eval-apply` must preserve a dirty canonical workspace, JIT-revalidate an
  exact source tree when the claim is commit-bound, invoke only the typed
  argv/cwd/timeout/exit contract, capture the environment, and write a private
  owner-local receipt. Source readiness is not runtime reproducibility or
  central proof acceptance.

### unknown_fit_selects_before_local_need

- route: `aoa-eval`, then `aoa-eval-select`
- fixture case: `eval_router_unknown_fit_selects_before_local_need`
- fixture file: `tests/fixtures/skill_evaluation_cases.yaml`
- snapshot:
  `tests/fixtures/skill_evaluation_snapshots/aoa-eval/eval_router_unknown_fit_selects_before_local_need.md`
- live source: exact-merged v11 smoke after the owner JIT/source-posture skill
  upgrade
- reviewed public receipt:
  `evals/reports/aoa-skill-live-dispatch-smoke-20260712-v11-reviewed-local-need-trajectory-break.json`
- verified rerun receipt:
  `evals/reports/aoa-skill-live-dispatch-smoke-20260712-v11-reviewed-select-precedence-lift.json`
- reason: the aided arm selected and loaded `aoa-eval` but chose
  `aoa-eval-local-need` while target-repository evidence and fit were still
  unknown. Missing evidence is not a no-fit result. Selection must remain the
  first child and may itself return `blocked_missing_input`; local intake is
  eligible only after explicit owner-reviewed no-fit evidence. The fresh
  exact-merged rerun selected and fully read `aoa-eval-select`, restoring
  positive selected-child trajectory lift while leaving outcome unscored.

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
- A selected execution sidecar routes to JIT owner validation and exact typed
  invocation; inspect-only readiness or MCP output never executes it.
- Live-workspace readiness and exact-source validation remain separate evidence
  statements, and unrelated dirty canonical work is preserved.
- Unknown fit or missing target evidence routes to `aoa-eval-select`; local
  intake requires an explicit no-fit result and never follows absence alone.
- Local files remain candidate evidence until reviewed by the proper owner.
