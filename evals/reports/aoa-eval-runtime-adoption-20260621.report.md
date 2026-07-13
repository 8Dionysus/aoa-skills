---
schema_version: local_eval_report_note_v1
owner_repo: aoa-skills
status: draft
title: aoa-eval runtime adoption smoke
summary: 'Records a local runtime-adoption smoke for the aoa-eval front-door skill:
  prompt-visible availability, runtime discovery policy, existing trigger fixtures,
  and remaining proof limits.'
refs:
- .agents/skills/aoa-eval/SKILL.md
- generated/runtime_discovery_index.json
- tests/fixtures/skill_evaluation_cases.yaml
- tests/fixtures/skill_evaluation_snapshots/aoa-eval/eval_router_existing_or_missing_eval_route.md
- tests/fixtures/skill_evaluation_snapshots/aoa-eval/eval_router_plain_unit_test.md
- tests/fixtures/skill_evaluation_snapshots/aoa-eval-select/eval_select_existing_surface.md
- tests/fixtures/skill_evaluation_snapshots/aoa-eval-apply/eval_apply_selected_validator.md
- tests/fixtures/skill_evaluation_snapshots/aoa-eval-local-need/eval_local_need_no_existing_fit.md
- tests/fixtures/skill_evaluation_snapshots/aoa-eval-design/eval_design_local_suite.md
- tests/fixtures/skill_evaluation_snapshots/aoa-eval-session-mining/eval_session_mining_missed_triggers.md
- evals/suites/aoa-eval-trigger-corpus.suite.md
- evals/reports/aoa-eval-session-mining.report.md
- evals/reports/aoa-eval-self-awareness-contract-lane.report.md
authority_boundary: no verdict, scoring, regression, or proof doctrine authority
---

## Scope

This local report records a runtime-adoption smoke for the `aoa-eval` skill family.

It is an `aoa-skills` local evidence note. It is not a central `aoa-evals` verdict, score, regression marker, proof receipt, or status promotion.

## Question

Is `aoa-eval` only manual, or does the live Codex runtime have enough prompt-visible and generated runtime evidence to treat it as an invokeable front-door route for eval-lane pressure?

## Web-Practice Alignment

Current agent-eval practice emphasizes trajectory, first-step routing, tool calls, and handoff behavior, not only final answers. For this smoke, the relevant behavior is therefore:

`user eval pressure -> visible front-door skill -> route classification -> exactly one subskill path -> local/central owner boundary`.

This matches the `aoa-eval` contract: the front-door chooses `select`, `apply`, `local-need`, `design`, or `session-mining`; it does not become proof authority.

## Observed Runtime Evidence

### Prompt-visible availability

Prompt-visible availability was checked through the Codex prompt-input debug
surface with an eval-port existence question and a focused read of the visible
eval-route context.

Observed result:

- `aoa-eval` appears in the model-visible available skills list.
- The visible description says to route eval-lane work by checking existing local and central eval surfaces first.
- The visible trigger text mentions eval existence, local evals, `aoa-evals`, validators, tests, scripts, traces, regressions, local eval ports, and `aoa-evals-mcp`.

### Runtime discovery policy

Current `generated/runtime_discovery_index.json` contains:

```text
aoa-eval:
  invocation_mode: explicit-preferred
  implicit_activation_policy: invoke
  mutation_surface: repo

aoa-eval-select:
  implicit_activation_policy: manual

aoa-eval-apply:
  implicit_activation_policy: manual

aoa-eval-local-need:
  implicit_activation_policy: manual

aoa-eval-design:
  implicit_activation_policy: manual

aoa-eval-session-mining:
  implicit_activation_policy: manual
```

Interpretation: the front-door router is not manual-only. The subskills remain manual because they should be selected after classification, preserving the one-route contract.

### Existing fixture coverage

Existing trigger-boundary fixtures include:

- `eval_router_existing_or_missing_eval_route`: positive front-door trigger.
- `eval_router_plain_unit_test`: negative ordinary-test boundary.
- `eval_router_drifted_contract_lane`: positive authority-sensitive contract-lane pressure.
- `eval_router_active_vs_stale_cleanup_boundary`: positive active-vs-stale cleanup pressure.
- `eval_router_source_authority_only`: negative source-authority-only boundary.

Existing snapshot cases cover positive and negative selection for:

- `aoa-eval`
- `aoa-eval-select`
- `aoa-eval-apply`
- `aoa-eval-local-need`
- `aoa-eval-design`
- `aoa-eval-session-mining`

Existing local suite/report surfaces:

- `evals/suites/aoa-eval-trigger-corpus.suite.md`
- `evals/reports/aoa-eval-session-mining.report.md`
- `evals/reports/aoa-eval-self-awareness-contract-lane.report.md`

## Adoption Readout

Local read: runtime adoption is present for the front-door skill, but still evidence-only.

Supported:

- The current Codex prompt exposes `aoa-eval` as an available skill.
- The generated runtime discovery index marks `aoa-eval` as `implicit_activation_policy: invoke`.
- The subskill family remains manual, which matches the intended classification-then-subskill route.
- Existing deterministic fixtures cover positive, negative, and adjacent route cases.
- Existing local reports preserve candidate evidence and proof limits.

Not supported:

- This does not prove every Codex host process has reloaded the same prompt-visible skill list.
- This does not prove model behavior will always choose `aoa-eval` correctly.
- This does not promote `aoa-eval` from scaffold status.
- This does not create central `aoa-evals` proof acceptance or regression authority.

## Owner Boundary

- `aoa-skills` owns skill trigger behavior, runtime discovery/read-model surfaces, fixture cases, and this local report.
- `aoa-evals` owns central proof doctrine, verdicts, scoring, regression authority, and any later central adoption.
- `codex debug prompt-input` is runtime evidence, not source truth.
- `generated/runtime_discovery_index.json` is a generated read model, not stronger than source `SKILL.md`.

## Next Route

The honest next step is not a new central eval bundle. The next step is a narrow runtime-behavior check if we want stronger confidence: run or build a small prompt-trigger harness that compares representative user prompts against expected skill/subskill decisions, using the existing `skill_evaluation_cases.yaml` and snapshots as the expected trajectory contract.
