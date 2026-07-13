# aoa-eval skill family research

Status: operationalization research packet
Date: 2026-06-21
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
- OpenAI's current agent workflow eval guide treats traces, graders, datasets,
  and eval runs as the core surfaces for agent evaluation. That maps to this
  skill family as: trace/route evidence first, stable datasets and regression
  checks only after we know the desired route.
  Source: https://developers.openai.com/api/docs/guides/agent-evals
- Anthropic's agent eval guide stresses clean isolated environments,
  nondeterminism-aware scoring, outcome checks over brittle exact trajectories
  unless the path itself matters, and tool-selection evals for browser/tool
  agents. That supports a first-step `aoa-eval` router check plus local
  validator/test execution before any central proof claim.
  Source: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- LangSmith separates final-response, trajectory, and single-step agent evals.
  The relevant OS Abyss unit is usually single-step route selection first,
  then trajectory verification only when a route must happen in a specific
  order.
  Source: https://docs.langchain.com/langsmith/evaluate-complex-agent
- LangChain's agent-evaluation checklist stresses manual review of real traces,
  clear success criteria, positive and negative cases, clean runs, repeated
  trials for nondeterminism, and promotion of stable capability evals into
  regression suites.
  Source: https://www.langchain.com/blog/agent-evaluation-readiness-checklist
- LangChain Agent Evals provides strict, unordered, subset, and superset
  trajectory matching modes. OS Abyss should reserve strict route contracts for
  authority-sensitive flows, not ordinary exploratory work.
  Source: https://docs.langchain.com/oss/python/langchain/test/evals
- Inspect AI frames serious agent evals around datasets, solvers/agents,
  tools, scorers, logs, and sandboxing. This matches the local/central split:
  local ports can name suites and run receipts; central `aoa-evals` owns
  scored proof bundles and promotion.
  Source: https://inspect.aisi.org.uk/
- MCP's tool specification makes tools model-controlled and schema-described,
  with explicit safety expectations for human involvement and trusted
  annotations. That supports using `aoa-evals-mcp` as an access/write bridge,
  but not as a proof authority.
  Source: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- The NSA/CISA MCP security guidance published in 2026 calls out dynamic tool
  invocation, implicit trust, context sharing, and input validation as agentic
  automation risks. For this repo family, MCP writes must therefore be
  path-confined, schema-checked, dry-run friendly, and unable to escalate into
  central source mutation.
  Source: https://media.defense.gov/2026/Jun/02/2003943289/-1/-1/0/CSI_MCP_SECURITY.PDF

## Repo evidence

The 2026-06-21 live inventory was built from `aoa-evals` with
`python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json`.

Current result: 15 repo-local ports, 15 valid, 0 invalid, 0 missing, 11
skeleton, 4 active. `aoa-evals` is deliberately excluded as
`central_proof_owner_not_repo_local_port`.

Active ports:

- `aoa-memo`: one intake packet; route `aoa-eval-select`.
- `aoa-routing`: one intake packet and one report; route `aoa-eval-select`.
- `aoa-skills`: one suite and three reports; route `aoa-eval-apply`.
- `connectors/aoa-4pda-connector`: one suite; route `aoa-eval-apply`.

Skeleton ports: `8Dionysus`, `ATM10-Agent`, `Agents-of-Abyss`, `Dionysus`,
`Tree-of-Sophia`, `aoa-agents`, `aoa-kag`, `aoa-playbooks`, `aoa-sdk`,
`aoa-stats`, and `aoa-techniques`.

This means the workflow is no longer a narrow example. It is a workspace-wide
port topology with valid dormant ports and a small number of live pressure
surfaces.

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
| `aoa-routing` | yes | active | 52 scripts, 201 tests, 31 validators |
| `aoa-sdk` | yes | skeleton | 81 scripts, 274 tests, 34 validators |
| `aoa-skills` | yes | active | 232 scripts, 325 tests, 79 validators |
| `aoa-stats` | yes | skeleton | 53 scripts, 91 tests, 23 validators |
| `aoa-techniques` | yes | skeleton | 103 scripts, 157 tests, 80 validators |
| `connectors/aoa-4pda-connector` | yes | active | connector-local suite pressure |

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

The 2026-06-21 `.aoa` refresh used the portable SQLite provider. Search was
usable with `status: current_with_deferred_live_updates`; graph was stale and
therefore not used for proof claims. Current live-tail sessions were deferred,
so the session refs below are candidate evidence with raw/segment refs, not
reviewed proof.

Initial missed-trigger candidates:

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
- Current long eval-port session `2026-06-11__006__у-меня-складывается-впечатление-что-для-всех`,
  session `019eb8c7-a7b5-76f0-b66a-0eb3791305ff`, contains concrete
  trigger-family evidence for `aoa-eval`:
  `083__compaction-to-compaction.md#event-015025` and `083__...#event-015032`
  show `aoa-evals-mcp` dry-run/apply local report writes;
  `088__compaction-to-compaction.md#event-015320` shows workspace-wide
  `evals/` discovery pressure; `091__...#event-015941` shows a validator/schema
  failure that should route to apply or repair instead of vague docs.
- The `2026-06-13__003__подключайся-к-моему-gmail-и-анализируй-все` session
  contains adjacent `aoa-skills` trigger work:
  `014__compaction-to-compaction.md#event-003368` for trigger-collision
  surfaces, `071__...#event-056429` for local port trigger-corpus inspection,
  and `170__...#event-086043` for the self-awareness contract-lane dogfood
  status.

These refs are raw/segment pointers only. They are evidence candidates until a
reviewed artifact or owner repo accepts the derived eval pressure.

## Local corpus landing

The first repo-local eval corpus now lives in:

- `evals/suites/aoa-eval-trigger-corpus.suite.md`
- `evals/reports/aoa-eval-session-mining.report.md`
- `evals/reports/aoa-eval-runtime-adoption-20260621.report.md`
- `evals/reports/aoa-eval-self-awareness-contract-lane.report.md`
- `evals/reports/aoa-eval-battle-path-20260621.report.md`

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

## 2026-06-21 operational readout

- `aoa-eval` is not manual-only in the local runtime evidence: the front-door
  skill is prompt-visible and the generated runtime discovery index marks it
  as `implicit_activation_policy: invoke`.
- Subskills remain manual by design; the front-door router chooses exactly one
  subroute.
- `aoa-evals-mcp` can now list local ports, inspect `aoa-skills`, recommend
  `aoa-eval-apply`, dry-run a local report write, apply the report, and keep
  local-port validation green.
- Central `aoa-evals` adoption is not warranted from this slice. The evidence
  is local trigger/runtime pressure, not central proof doctrine.

## 2026-07-12 source and execution handoff

The reviewed v11 live-dispatch smoke showed that `aoa-eval` can add bounded
route and selected-child trajectory lift without broad fixture archaeology.
The next adaptive return came from comparing that successful dispatch path
with the newer `aoa-evals` local-suite execution contract, not from treating a
single smoke as proof that the whole procedure was complete.

Two distinctions now belong in the skill family itself:

- A session-start, readiness, dashboard, generated reader, or MCP packet
  describes the live workspace it inspected. It must report root, commit,
  dirty/divergent posture, and freshness, but it does not turn a dirty canonical
  checkout into exact merged evidence. Commit-bound claims use the owner
  validator from a clean exact source tree while preserving the live checkout.
- A reviewed `local_eval_suite_execution_v1` sidecar is typed source execution
  intent. `ready` means `source-contract-ready` only. The repo owner or
  `aoa-eval-apply` must JIT-revalidate schema, canonical owner, paths, argv, and
  hashes; execute only the validated argv/cwd/timeout/exit contract; capture
  interpreter, dependency, plugin, config, and selected environment posture;
  and write a private receipt linked to source head and sidecar digest.

Inventory, Eval Forge, readiness, dashboards, session-start, generated readers,
and MCP remain inspect-only. The execution receipt is candidate evidence with
proof and promotion authority false. These boundaries are now fixture-backed
in the trigger corpus and must be regenerated into portable/runtime skill
surfaces before the next exact-merged live smoke.

## 2026-07-12 selection precedence return

The exact-merged smoke after that handoff passed every harness, prompt,
filesystem, inventory, fixture, transport, and owner-boundary gate. It still
found a skill-level ambiguity: with no target-repository evidence, the aided
router selected `aoa-eval-local-need` and then correctly blocked instead of
mutating. The source-declared trajectory expected `aoa-eval-select` because the
task asks to inspect existing surfaces and no selection has established fit or
no-fit.

The durable rule is now explicit:

- unknown fit, missing target evidence, or a request to inspect/decide among
  existing surfaces routes to `aoa-eval-select`;
- the selection child may return `blocked_missing_input` without changing
  route;
- missing evidence never counts as a no-fit result;
- `aoa-eval-local-need` requires an explicit no-fit result from selection or an
  equivalent owner inspection.

The reviewed negative-trajectory receipt remains immutable candidate evidence.
A source regression and snapshot guard the precedence, and a fresh exact-merged
smoke is required before widening the pilot.

That rerun selected and fully read `aoa-eval-select`, restored positive route
and selected-child trajectory lift, retained correct procedure disposition in
both implicit arms, and kept outcome unscored. This closes the bounded
precedence return; it does not change the next coverage gate of 11/11 declared
procedures plus 11/11 owner-observable outcomes.

## 2026-07-12 owner-observable outcome seam

The earlier v8 answer key failed because it graded an unavailable whole-task
result through the same fields used for selected-procedure disposition. V12
keeps those dimensions separate. A source-authored outcome contract now asks
one bounded owner question, exposes several adjacent candidate actions but not
the answer key in the plan lock, and accepts only one atomic
`outcome_validator.py` transport event. Generic fixture-probe success, route
selection, disposition prose, and model self-report cannot satisfy it.

This does not prove target-repository completion. It makes the next justified
owner action observable under the hermetic fixture. Reading, hashing, copying,
importing, reproducing, or retrying the validator invalidates causal
measurement; one wrong choice remains a valid negative outcome. The first
contract covers `collision-42`, bringing both pilot axes to 1/11. A fresh
exact-merged smoke must validate this seam before the same design expands to
the other ten implicit pilot cases.

That exact-merged v12 smoke completed all four arms with no failure class,
external read, broad fixture inventory, outcome-validator inspection, or
retry. The aided arm retained positive route and selected-child trajectory
lift; both arms chose the correct bounded owner action in one attempt, so
outcome lift is `0` with both correct. The result validates that the new seam is
measurable and independent. It does not show skill-specific outcome lift. The
next honest move is to preserve this reviewed receipt and author the remaining
ten pilot procedure/outcome contracts from their source skills.

## 2026-07-12 full pilot contract corpus

The reviewed seam has now been expanded from `collision-42` to all eleven
implicit `pilot13` cases without deriving answers from live output. Source
review separates three direct invoke routes that lack repository evidence, two
rooted routes that must select and fully read their first child, and six
explicit-only routes that must remain unloaded under implicit pressure. Their
procedure dispositions are respectively `blocked_missing_input` or
`not_applicable`, never fixture-probe completion.

Each case has a separate owner-action question with three deterministic,
sorted candidate values and one source-authored expected choice. The plan locks
the contract digests but does not reveal those choices; the live model receives
only the candidates and may complete exactly one validator attempt. Focused
harness validation now reports 11/11 procedure coverage and 11/11 objective
outcome coverage. The next claim boundary is narrow: the corpus makes the
30-turn pilot plan-eligible, but only an exact-merged, operator-confirmed,
host-routed run and review can say what the runtime actually does.

## 2026-07-12 first full pilot readout

The exact-merged 30-turn pilot completed under the medium host route with no
early stop. All prompt inventories, filesystem and broad-inventory guards,
fixture probes, transport returns, and authority boundaries passed. Every one
of the 22 implicit arms made exactly one owner-action attempt, did not inspect
the validator, and chose the source-correct action. The outcome seam therefore
generalized across the pilot, but produced `no_lift_both_correct` in all eleven
pairs rather than skill-specific outcome lift.

The adaptive returns are heterogeneous. `aoa-change-protocol` won implicit
manual-policy pressure for `aoa-summon`, `aoa-approval-gate-check`, and the
`atm10` overlay; those are candidate description/collision gaps. They must not
be conflated with the harness-side discoveries:

- a no-skill control that invokes an ambient non-target route did not load the
  manual target and must not be labelled a manual activation leak;
- `abyss-safe-infra-change` explicitly starts from `aoa-safe-infra-change`, so
  its target-plus-base-child report needs a source-declared hierarchy instead
  of `selection_report_miss`.

Manual-policy arms also consistently described the unavailable procedure as
blocked or owner-deferred rather than `not_applicable`. That may be prompt and
output-contract pressure, because no procedure is dispatched when the target
is manual-required. Preserve the reviewed `needs-rerun` receipt, repair and
replay these harness semantics first, then isolate the three skill collision
candidates through the smallest adjacent reruns before another full pilot.

## 2026-07-12 v13 harness return

Source reread corrected the initial `collision-38` hypothesis. `aoa-decision`
requires one chosen find/create/correct route, classifies find-or-understand
first, and loads only that child; `aoa-decision-find` then owns the narrow graph
lookup. The root-only live response is therefore still a child-handoff
candidate, not a reason to erase the source-authored child contract.

V13 repairs only the demonstrated harness pressure. Manual-policy failure
classification now applies to the aided treatment arm; an ambient non-target
control route may remain route-incorrect but is not a target activation leak.
Fixture guidance states that `manual_required` or `do_not_use` without target
dispatch has `procedure_disposition=not_applicable`. Structured reports gain a
separate source-locked target-to-base-child hierarchy, initially
`abyss-safe-infra-change` to `aoa-safe-infra-change`; an undeclared child still
fails report matching. Read-only replay of the immutable v12 raw pilot under
these grader rules removes the three control-side labels and the structured
selection miss, leaving 23 clean arms and seven aided returns: one decision
child handoff, three manual-policy procedure reports, and three manual-policy
collision routes. Replay validates the grader only and does not rewrite the
v12 receipt.

The next live step is therefore not another full pilot. The source-locked
`pilot13-returns` cohort keeps both arms for those seven implicit cases and only
the corrected Abyss structured report, for 15 turns total. This is the smallest
run that can confirm the v13 harness repairs while preserving the remaining
skill-route evidence and paired control boundary.

## 2026-07-12 bounded v13 live returns

Two exact-merged `pilot13-returns` attempts remain partial. The first stopped
at 6 of 15 turns on a post-start transport timeout. A fresh run passed that
point and reached 14 of 15, then failed the model-output contract because Titan
control combined `selected_skill=null` with `claims_loaded=true`. The final
Abyss structured arm therefore remains unobserved; neither receipt can close
the cohort.

The completed evidence still changes the next question. External ambient
routes such as `aoa-session-memory-global-route` and `abyss-machine` preserved
the explicit-only target boundary but were labelled as aided dispatch gaps,
whereas repo-visible `aoa-change-protocol` and `aoa-eval` activations are real
treatment-side collision or leak candidates. Manual no-target arms continued
to report blocked or deferred procedures despite the v13 `not_applicable`
instruction, so target-procedure semantics remain under-specified. The two
partial runs also varied on decision procedure disposition while preserving a
correct root-to-`aoa-decision-find` handoff in both, arguing against a decision
skill edit before the reporting contract is repaired.

Review exposed one earlier source-surface omission too: the new cohort existed
in the plan schema but not in private/public receipt cohort enums. Preserve the
two receipts under their original v13 measures, close schema parity with a
synthetic private-to-public test, then repair repo-vs-ambient activation and
output-field semantics before another live attempt.

## 2026-07-12 v14 target-report boundary

V14 makes the treatment boundary explicit. The runner classifies the reported
selected skill against the exact prompt-visible repo fixture names. A selected
external ambient route is recorded but is not repo-treatment activation, while
a selected prompt-visible repo skill remains a manual leak or collision
candidate. For manual targets, dispatch correctness now depends on
`route_decision=manual_required`; the independent target-load contract still
requires that the target was not read or natively loaded.

The same contract text now reaches implicit arms; v13 had appended its
`not_applicable` instruction only through the root/structured fixture-procedure
builder. The final prompt section states that route decision and procedure
disposition concern the expected target, that an ambient route does not make
the target invoked or blocked, and that `claims_loaded` must be false when no
skill is selected. The output schema descriptions preserve those distinctions.

Read-only replay of the 14-turn v13 private receipt changes only
`collision-20` and `collision-49` aided: each moves from
`dispatch_policy_gap` to `procedure_disposition_miss`. The replay leaves two
collision misroutes, two repo-skill manual activation leaks, one earlier
procedure miss, and the Titan output-contract failure. It validates v14
classification only and does not rewrite either v13 public receipt. A fresh
exact-merged v14 run remains required before skill edits.
