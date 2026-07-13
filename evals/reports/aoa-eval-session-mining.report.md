---
schema_version: local_eval_report_note_v1
owner_repo: aoa-skills
status: draft
authority_boundary: no verdict, scoring, regression, or proof doctrine authority
---

# aoa-eval session-mining report

## Scope

This report records the first local `.aoa` mining pass for the `aoa-eval`
trigger corpus. It is a local evidence note for `aoa-skills`, not a central
`aoa-evals` proof report.

## Method

1. Confirmed owner boundaries from `aoa-skills` route cards, `evals/AGENTS.md`,
   and the `aoa-evals` local eval-port standard.
2. Rechecked the active `.aoa` archive for the long session
   `019eb8c7-a7b5-76f0-b66a-0eb3791305ff`.
3. Ran provider status and narrow retrieval queries by trigger pressure:
   eval router, local eval port, `aoa-evals-mcp`, validators, and session
   mining.
4. Preserved session, segment, raw refs, and freshness. No session hit was
   promoted to proof.

## Provider Status

Provider status came from the `search-provider-status` operation owned by
`scripts/aoa_session_memory.py`, scoped to the OS Abyss workspace and `.aoa`
root.

Observed on 2026-06-15T16:51:05Z:

- selected provider set: `all`
- portable provider: `portable_sqlite`
- portable status: `ready_with_deferred_live_updates`
- index generated at: `2026-06-15T16:46:58Z`
- freshness: `current_with_deferred_live_updates`
- dirty sessions: 6
- actionable dirty sessions: 0
- deferred live sessions: 6, including the active long session

Interpretation: the provider is usable for route-first mining, but the live
session stream is still moving. Individual evidence refs below were accepted
only when their retrieval packet reported `segment_index_live_check: fresh`.

## Retrieval Scope

The `process-lessons` retrieval operation used three narrow packets:

- eval routing, trigger evals, local eval-port validation, and validators;
- `aoa-evals-mcp`, local eval-port candidates, and evidence validation;
- the named long session, constrained to trigger routing and local-port
  evidence.

Each retrieval used `portable_sqlite`, reported `ok: true`, and treated search
hits as candidate evidence that points back to raw/segment refs.

## Active-Session Evidence

| Class | Segment/event | Raw ref | Freshness | Local route |
| --- | --- | --- | --- | --- |
| router goal | `039__compaction-to-compaction.md#event-007511--user_intent--user-message` | `raw:line:7511` | `segment_index_live_check: fresh` | `aoa-eval` |
| router continuation | `042__compaction-to-compaction.md#event-008486--user_intent--user-message` | `raw:line:8486` | `segment_index_live_check: fresh` | `aoa-eval` |
| MCP/local-port boundary | `032__compaction-to-compaction.md#event-006805--security_touchpoint--tool-output-call_1gya9un2du6ytrl6uhn3zfjj` | `raw:line:6805` | `segment_index_live_check: fresh` | `aoa-eval-select` with owner-boundary stop |
| web/repo gates before mining | `038__compaction-to-compaction.md#event-007506--assistant_message--assistant-message` | `raw:line:7506` | `segment_index_live_check: fresh` | `aoa-eval-session-mining` |
| prior local-port closeout signal | `047__compaction-to-compaction.md#event-011361--assistant_message--event-message-agent_message` | `raw:line:11361` | `segment_index_live_check: fresh` | local-port federation context |
| process lesson signal | `047__compaction-to-compaction.md#event-011362--process_lesson--assistant-message` | `raw:line:11362` | `segment_index_live_check: fresh` | candidate lesson, not proof |

## Handoff

- Local suite note:
  `evals/suites/aoa-eval-trigger-corpus.suite.md`
- Existing deterministic trigger fixtures:
  `tests/fixtures/skill_evaluation_cases.yaml`
- Existing snapshots:
  `tests/fixtures/skill_evaluation_snapshots/aoa-eval*`

The corpus status is `draft` and local. Central adoption, scoring, verdicts,
regression truth, and proof doctrine remain outside this report and route to
`aoa-evals`.

## 2026-06-21 Refresh

The refresh used the full timer-free maintenance-status operation owned by the
workspace `.aoa` session-memory tool.

Observed at `2026-06-22T00:08:52Z`:

- search status: `current_with_deferred_live_updates`
- selected provider: `portable_sqlite`
- graph status: `stale`
- graph route: budgeted graph maintenance before GraphRAG-style synthesis
- deferred live sessions: 4, including the current long eval-port session
  `019eb8c7-a7b5-76f0-b66a-0eb3791305ff`

Interpretation: use portable SQLite search and raw/segment refs for narrow
trigger evidence; do not use stale graph state for proof-strength claims.

Refresh searches covered:

- `aoa-eval` skill triggers and local evals;
- self-awareness contract-lane eval evidence;
- `aoa-evals-mcp` local-port validation.

Refresh trigger families:

| Family | Evidence refs | Route implication |
| --- | --- | --- |
| local eval-port discovery | `2026-06-11__006`, `088__compaction-to-compaction.md#event-015320`, `raw:line:15320` | trigger `aoa-eval`; inventory before design |
| MCP dry-run/apply local write | `2026-06-11__006`, `083__compaction-to-compaction.md#event-015025`, `raw:line:15025`; `083__...#event-015032`, `raw:line:15032` | trigger `aoa-eval-apply`/runtime bridge check; preserve central stop-line |
| validator/schema failure during skill export | `2026-06-11__006`, `091__compaction-to-compaction.md#event-015941`, `raw:line:15941` | trigger apply/repair route instead of new proof design |
| trigger-collision/description eval pressure | `2026-06-13__003`, `014__compaction-to-compaction.md#event-003368`, `raw:line:3368` | trigger skill-router regression check |
| self-awareness contract-lane dogfood | `2026-06-13__003`, `170__compaction-to-compaction.md#event-086043`, `raw:line:86043` | keep as local dogfood evidence; no central promotion without owned `aoa-evals` route |

These refreshed refs strengthen the local trigger corpus, but they still do not
turn session-memory output into central proof. They are accepted here only as
repo-local evidence candidates for `aoa-skills`.
