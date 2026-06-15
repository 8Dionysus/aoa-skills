# aoa-eval skill family research

Status: first-slice research packet
Date: 2026-06-13
Owner repo: `aoa-skills`

## Question

Build a Codex skill family that notices evaluation moments in OS Abyss work,
selects and applies existing eval surfaces when they exist, and creates
repo-local eval pressure when they do not.

This is a skill-routing problem, not a proof-authority migration. The central
proof owner remains `aoa-evals`; local sibling repositories expose only
repo-native `evals/` ports and intake pressure.

## Web evidence

- OpenAI's Codex skill documentation says skills are reusable workflows loaded
  by name/description first, and that the description is the primary implicit
  activation surface. It also recommends focused skills, optional scripts only
  when deterministic behavior or external tooling is needed, and prompt tests
  for trigger behavior.
  Source: https://developers.openai.com/codex/skills
- OpenAI's January 22, 2026 skill-eval guide frames a skill eval as
  `prompt -> captured run (trace + artifacts) -> checks -> score`, and calls
  out regressions such as wrong trigger, skipped required step, or extra files.
  Source: https://developers.openai.com/blog/eval-skills
- OpenAI's agent workflow eval guide starts with traces while behavior is still
  being debugged, then moves to datasets and eval runs once the team knows what
  "good" looks like and needs repeatability.
  Source: https://developers.openai.com/api/docs/guides/agent-evals
- Anthropic's agent eval guide separates capability evals from regression
  evals, points coding agents toward deterministic tests first, and treats
  transcript grading as an additional behavioral layer when tests alone are not
  enough.
  Source: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- LangChain's agent-evaluation checklist stresses manual review of real traces,
  clear success criteria, positive and negative cases, trace/run/thread levels,
  and feeding production failures back into datasets and error analysis.
  Source: https://www.langchain.com/blog/agent-evaluation-readiness-checklist
- AgentSkills trigger guidance treats skill descriptions as stochastic trigger
  surfaces that should be tested with should-trigger and should-not-trigger
  prompts, repeated runs, and stable train/validation splits.
  Source: https://agentskills.io/skill-creation/optimizing-descriptions
- MCP's tool specification makes tool exposure model-controlled but still calls
  for clear exposed-tool visibility and human-in-the-loop confirmation for
  operations. That supports using `aoa-evals-mcp` as an access plane, not proof
  authority.
  Source: https://modelcontextprotocol.io/specification/2025-06-18/server/tools

## Repo evidence

All 15 `/srv/AbyssOS` git repositories were mapped. Fourteen repositories have
`evals/PORT.yaml` with `schema_version: local_eval_port_v1`; `aoa-evals` itself
does not expose a local port because it is the central proof owner. Only
`aoa-memo` currently advertises `status: active`; the other local ports are
`skeleton`.

| Repo | Local eval port | Status | Script/test/validator pressure |
| --- | --- | --- | --- |
| `8Dionysus` | yes | skeleton | 51 scripts, 38 tests, 19 validators |
| `ATM10-Agent` | yes | skeleton | 178 scripts, 323 tests, 8 validators |
| `Agents-of-Abyss` | yes | skeleton | 227 scripts, 283 tests, 158 validators |
| `Dionysus` | yes | skeleton | 41 scripts, 43 tests, 63 validators |
| `Tree-of-Sophia` | yes | skeleton | 47 scripts, 33 tests, 32 validators |
| `aoa-agents` | yes | skeleton | 112 scripts, 97 tests, 70 validators |
| `aoa-evals` | central owner | n/a | 544 scripts, 165 tests, 606 validators |
| `aoa-kag` | yes | skeleton | 27 scripts, 52 tests, 20 validators |
| `aoa-memo` | yes | active | 278 scripts, 190 tests, 167 validators |
| `aoa-playbooks` | yes | skeleton | 110 scripts, 71 tests, 64 validators |
| `aoa-routing` | yes | skeleton | 52 scripts, 201 tests, 31 validators |
| `aoa-sdk` | yes | skeleton | 81 scripts, 274 tests, 34 validators |
| `aoa-skills` | yes | skeleton | 232 scripts, 325 tests, 79 validators |
| `aoa-stats` | yes | skeleton | 53 scripts, 91 tests, 23 validators |
| `aoa-techniques` | yes | skeleton | 103 scripts, 157 tests, 80 validators |

The density of existing scripts, tests, and validators means the skill should
start by selecting current local proof surfaces before designing new evals.

## Owner boundaries

- `aoa-skills` owns the skill family, trigger descriptions, invocation policy,
  trigger eval cases, and skill validation.
- `aoa-evals` owns proof doctrine, central eval bundles, scoring/verdict rules,
  regression promotion, and the local eval-port standard.
- `abyss-stack` owns runnable MCP access planes such as `aoa-evals-mcp`; MCP can
  list, inspect, or draft narrow local-port artifacts, but cannot make proof
  truth.
- `.aoa` owns raw evidence, segments, search indexes, and freshness. It is a
  candidate-evidence plane, not reviewed proof.
- `aoa-routing` owns router/read-model projections if the skill family later
  needs route-pack changes.

## Trigger classes

- Explicit: `$aoa-eval` or one direct subskill name.
- Should trigger: user asks whether an eval exists, whether to add one, which
  validation should guard a change, how to convert a repeated failure into an
  eval, or how to use local `evals/` ports.
- Manual subskill: prompts that semantically match select/apply/local-need/
  design/session-mining should surface as manual routes unless the router
  selects them.
- Should not trigger: ordinary one-off unit tests, docs edits with no eval
  pressure, source-of-truth/decision/memo/session-memory tasks better owned by
  existing skills, or central `aoa-evals` proof changes requested directly.
- Prefer other skill: decision records, memo writeback, source-of-truth mapping,
  invariant-property authoring, and ordinary contract-test creation each have
  stronger existing skill owners unless the task is specifically about eval
  routing.

## Skill family

- `aoa-eval`: front-door router. It picks exactly one eval route and enforces
  owner boundaries.
- `aoa-eval-select`: inspect central/local eval surfaces and choose an existing
  candidate before any new design.
- `aoa-eval-apply`: run or route existing deterministic evals, validators, or
  scripts and report what they prove.
- `aoa-eval-local-need`: create a repo-local `evals/intake/*.eval_need.json`
  pressure packet when no eval fits.
- `aoa-eval-design`: draft a local eval suite/report without claiming central
  proof authority.
- `aoa-eval-session-mining`: mine `.aoa` after research gates pass for missed
  eval triggers and candidate failures.

## Session evidence

The `.aoa` search index was fresh at `2026-06-13T18:15:08Z`. Initial missed-
trigger candidates:

- `2026-05-25__001__давай-дошлифуем-рефакторинг-aoa-evals-вопрос-в`,
  session `019e5c96-3c6b-7382-a17d-4d76a4d4c079`, segment `039`, events
  `004823`, `004824`, `004615`; this cluster involved `aoa-evals-mcp` source,
  tests, validators, and verification gaps. It is a good `aoa-eval-select` and
  `aoa-eval-apply` trigger example.
- `2026-06-04__003__у-нас-в-отрефакторенных-репо-есть-определенным`,
  session `019e9388-dc4c-7f82-b6bf-04bea3aed7f4`, segment `077`, events
  `014678`, `014680`; this cluster involved `aoa-evals-mcp` and evidence
  candidate validation. It is a local-port and MCP-access-plane trigger
  example.
- `2026-06-03__006__в-aoa-evals-мы-только-только-провели`, session
  `019e8f02-62ef-7931-ab39-631e4bde80a8`, segments `025`, `030`, `039`, `070`,
  `072`, `074`, `080`; this cluster involved validator/test refactors and
  mechanics proof pressure. It is a session-mining and validator-selection
  trigger example.
- `2026-05-06__001__хорошо-делай`, session
  `019dfb8e-2e54-7f92-9eb2-f26b13eeaa2d`, segments `008`, `009`, `027`,
  `046`, `048`, `053`; this cluster involved description-trigger evals,
  trigger lint, and tiny-router validation. It is a skill-trigger eval
  regression example.

These refs are raw/segment pointers only. They are evidence candidates until a
reviewed artifact or owner repo accepts the derived eval pressure.

## Local corpus landing

The first repo-local eval corpus now lives in:

- `evals/suites/aoa-eval-trigger-corpus.suite.md`
- `evals/reports/aoa-eval-session-mining.report.md`

The suite turns the research taxonomy into local trigger classes with
raw/segment refs, including an explicit no-trigger case from the existing
skill-evaluation fixtures. The report records the current `.aoa` provider
status and marks the mining output as candidate evidence, not central proof.

## First-slice implementation

1. Land the skill family in `skills/core/engineering/` with `status: scaffold`.
   Do not claim canonical/evaluated status until review snapshots and stronger
   eval evidence exist.
2. Give only `aoa-eval` implicit `invoke` policy. Subskills stay `manual` and
   are selected by the router or direct explicit invocation.
3. Add policy and trigger fixture coverage for explicit, should-trigger,
   manual, negative, and collision families.
4. Regenerate portable exports, description-trigger evals, support resources,
   and tiny-router inputs through existing builders.
5. Validate with source-fast, trigger lint, description-trigger lint,
   `validate_agent_skills`, `report_skill_evaluation`, and focused tests.

## Later work

- Add central `aoa-evals` review for the local eval-port schema only if new
  intake fields are required.
- Add `aoa-routing` projections only after the skill family proves route
  pressure that the current router cannot represent.
- Promote from scaffold only after snapshot cases, reviewer notes, and real
  session-derived regression cases pass.
