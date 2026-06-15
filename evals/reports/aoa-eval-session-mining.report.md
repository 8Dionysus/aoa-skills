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

Command:

```bash
python3 scripts/aoa_session_memory.py search-provider-status \
  --workspace-root /srv/AbyssOS \
  --aoa-root /srv/AbyssOS/.aoa
```

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

## Retrieval Commands

```bash
python3 scripts/aoa_session_memory.py retrieve process-lessons \
  --workspace-root /srv/AbyssOS \
  --aoa-root /srv/AbyssOS/.aoa \
  --query 'aoa-eval trigger evals local eval port validator' \
  --limit 8 \
  --event-limit 8
```

```bash
python3 scripts/aoa_session_memory.py retrieve process-lessons \
  --workspace-root /srv/AbyssOS \
  --aoa-root /srv/AbyssOS/.aoa \
  --query 'aoa-evals-mcp local eval port evidence candidate validator' \
  --limit 8 \
  --event-limit 8
```

```bash
python3 scripts/aoa_session_memory.py retrieve process-lessons \
  --workspace-root /srv/AbyssOS \
  --aoa-root /srv/AbyssOS/.aoa \
  --session '2026-06-11__006__у-меня-складывается-впечатление-что-для-всех' \
  --query 'trigger eval skill session mining local eval port' \
  --limit 12 \
  --event-limit 12
```

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
