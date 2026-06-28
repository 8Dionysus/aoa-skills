---
schema_version: local_eval_report_note_v1
owner_repo: aoa-skills
status: draft
title: aoa-eval prompt trigger harness
summary: Records the local deterministic prompt-trigger harness for aoa-eval route
  correctness across front-door, subskill, negative, and owner-boundary cases.
refs:
- evals/suites/aoa-eval-trigger-corpus.suite.md
- tests/test_aoa_eval_prompt_trigger_harness.py
- tests/fixtures/skill_evaluation_cases.yaml
- tests/fixtures/skill_evaluation_snapshots/aoa-eval/eval_router_existing_or_missing_eval_route.md
- tests/fixtures/skill_evaluation_snapshots/aoa-eval/eval_router_plain_unit_test.md
- docs/testing/TEST_TOPOLOGY.md
- docs/testing/test_inventory.json
authority_boundary: no verdict, scoring, regression, or proof doctrine authority
---

## Scope

This report records the local `aoa-eval` prompt-trigger harness added on
2026-06-25.

The harness checks route correctness over existing `aoa-skills` fixture and
snapshot surfaces. It does not score model output, promote a central eval
bundle, or claim proof for `aoa-evals`.

## Question

Can `aoa-skills` repeatably check whether representative eval-pressure prompts
route to the correct `aoa-eval` front-door or subskill decision?

## Covered Classes

The harness covers the required local prompt classes:

- session front door/readiness packet before subskill selection
- existing eval select/apply
- local eval need/design
- selected validator or test route
- session mining after web/repo gates
- negative non-eval prompts
- unclear owner boundary and stale-vs-active cleanup pressure

It uses existing `skill_evaluation_cases.yaml` entries and snapshots instead of
introducing a new fixture format.

## Checks

- Focused harness route: `tests/test_aoa_eval_prompt_trigger_harness.py`.
  Observed result: `5 passed, 40 subtests passed`.
- Neighbor route: prompt harness plus trigger corpus, skill evaluation,
  evaluated-status checks, and test topology. Observed result:
  `21 passed, 604 subtests passed`.
- Skill source validation route: `validate_skills` scoped to `aoa-eval`.
  Observed result: `Validation passed for skill 'aoa-eval'.`

## Boundary

This is a repo-local route harness:

- `aoa-skills` owns prompts, snapshots, skill trigger behavior, and this report.
- `aoa-evals` owns central proof doctrine, verdicts, scoring, and regression
  promotion.
- `aoa-evals-mcp` remains an access plane and must not be treated as proof
  authority.
- Session-derived material in the suite remains candidate evidence until an
  owner surface reviews it.

## Result

The `aoa-eval` trigger regression slice now has a focused repeatable command.
It also now guards the per-session readiness route: when the OS Abyss
`aoa-evals` checkout is available, the router should raise
`aoa_eval_session_start.py` before choosing a subskill and should validate the
candidate-only packet contract before using session evidence.

The next route for this repo is `aoa-eval-apply`: run this harness when changing
`aoa-eval` trigger wording, prompt fixtures, snapshots, or local eval trigger
corpus material.
