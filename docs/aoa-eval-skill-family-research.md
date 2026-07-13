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
classification only and does not rewrite either v13 public receipt.

## 2026-07-12 complete v14 live return

The fresh exact-merged v14 execution completes all 15 turns and all seven
pairs. It records zero prompt, filesystem, inventory, fixture, transport,
owner-action, or authority failures. The final Abyss structured arm now proves
the source-declared overlay-to-base hierarchy without overriding native target
dispatch/load. The earlier `collision-33` timeout, the external ambient routes
in `collision-20` and `collision-49`, and Titan's null-selection contract all
return clean under fresh transport rather than replay alone.

Only three aided failures remain. `collision-38` selects and fully reads
`aoa-decision` but stops at the root: route and outcome improve, while the
source-authored `aoa-decision-find` trajectory and procedure remain incorrect
in both arms. `collision-09` correctly keeps `aoa-approval-gate-check` unloaded
and reports `manual_required`, yet loads the prompt-visible generic
`aoa-change-protocol`, so the remaining failure is a real treatment activation
leak. `collision-14` selects that same generic skill instead of
`atm10-change-protocol`; route and procedure show negative lift and the bounded
outcome remains incorrect in both arms.

The evidence now supports a two-skill source return rather than another harness
revision: strengthen the `aoa-decision` root-to-find handoff and narrow
`aoa-change-protocol` around explicit-only approval-gate and project-overlay
owners. Preserve the v14 receipt as `needs-rerun`, add deterministic regression
cases first, then execute only the smallest affected live cohort before any
full-pilot or family widening.

## 2026-07-12 v14 skill-source repair

Red-first deterministic fixtures now bind the two source changes exposed by
the complete v14 run. `aoa-decision` classifies first, then must select and
fully read exactly one find, create, or correct child before graph lookup,
source reads, or writes; a root-only find route is explicitly incomplete. Its
prompt-visible portable description carries the same handoff rule.

`aoa-change-protocol` retains implicit activation for genuinely generic bounded
changes, but its source and prompt-visible description now exclude two owner
classes before selection: approval-only classification for production or
sensitive actions, and project-specific manual overlays such as the ATM10
repo-relative route. The change neither relaxes the explicit target policies
nor makes the generic workflow manual. Collision-family adjacency now records
the observed risk boundary for derived routers as well.

The next live step is source-locked as `pilot13-skill-returns`: six turns, both
arms for `collision-38`, `collision-09`, and `collision-14`, no unrelated
trajectory or structured cases, procedure and outcome coverage 3/3, and full
private/public cohort schema parity. This contraction reduces model spend while
preserving paired evidence. Exact-merged execution is still required; green
deterministic checks alone cannot claim the runtime collision is repaired.

## 2026-07-12 first skill-return execution

The exact-merged six-turn run completes all three pairs without prompt,
filesystem, inventory, fixture, transport-process, owner-action, safety, or
authority contamination. `collision-09` is now clean: the aided arm selects no
repo skill, keeps the explicit approval owner unloaded, reports the required
manual route, and gains the bounded owner outcome over control. This closes the
approval-only source return.

`collision-38` also confirms that the root repair worked. The aided arm selects
`aoa-decision`, fully reads `aoa-decision-find`, and gains both route and
trajectory over control. Its remaining procedure mismatch is narrower: with no
graph status, changed paths, target record, or owner packet, the child reports
`deferred_owner_boundary` rather than the source-locked
`blocked_missing_input`. The exact expected owner-action command exits zero in
one attempt, but the aided command event exposes no sentinel output bytes.
Outcome verification therefore remains false; command identity and exit status
must not substitute for the missing observable output.

`collision-14` reports the correct manual target route, target procedure, and
owner outcome, but still selects and claims the prompt-visible generic
`aoa-change-protocol`. The abstract project-overlay exclusion is therefore too
weak for the concrete ATM10 repo-relative wording. The next return is bounded:
make the decision child name the missing-input terminal disposition, make the
generic change-protocol description reject ATM10 repo-relative paths, commands,
and approval notes before load, preserve the outcome observation gap, and rerun
the affected cohort without changing the explicit targets or the proof rule.

## 2026-07-12 second skill-return repair

The second repair follows the narrower live evidence rather than widening the
root skills again. `aoa-decision-find` now distinguishes missing evidence from
an owner refusal: when the permitted boundary offers neither graph or fallback
lookup nor graph status, changed paths, target records, or an owner repository
packet, its procedure stops with `blocked_missing_input` and explicitly rejects
`deferred_owner_boundary`. Existing graph-first lookup, source-note authority,
and create/correct handoffs remain unchanged.

The generic change protocol now carries the concrete prompt-visible negative
signal that the first repair lacked. An ATM10 repository request for
repo-relative paths, local commands, or local approval notes reports the manual
owner route without loading either generic `aoa-change-protocol` or the
explicit overlay. This is an overlay-owned boundary, not a rule that makes
ordinary generic change work manual.

Both contracts were introduced red-first against source and portable
descriptions. The existing six-turn cohort remains the smallest safe rerun: it
rechecks the already-closed approval pair, the repaired decision disposition,
the concrete ATM10 exclusion, and the still-unverified outcome sentinel under
fresh transport. No deterministic result closes that live observation return.

## 2026-07-12 clean aided skill return

The exact-merged rerun completes all six turns with no aided failure class and
with every prompt, filesystem, inventory, fixture, dispatch, load,
transport-process, owner-action, safety, and authority boundary clean.
`collision-38` now selects and fully reads `aoa-decision-find`, reports
`blocked_missing_input`, and gains route, trajectory, procedure disposition,
and verified owner outcome over control. `collision-14` selects no skill, keeps
both generic and explicit overlay procedures unloaded, reports the manual ATM10
owner route, and verifies its outcome. `collision-09` stays correct in both
arms, so its outcome is a no-lift-both-correct result rather than a regression.

The rerun also confirms that the earlier missing sentinel was not an aided
skill defect. The exact owner-action command exits zero but exposes no sentinel
bytes in the `collision-38` and `collision-14` control arms this time. Their
outcome verification correctly remains false, while the aided commands expose
the sentinel and verify. This closes the two source returns but does not make
the resulting positive control contrast stable proof. Preserve the receipt as
reviewed candidate evidence, add an explicit per-arm and pair-level
output-observation-gap signal, and only then widen to the full pilot.

## 2026-07-12 v15 outcome observation telemetry

V15 makes the recurring transport observation explicit without changing the
verdict. An arm receives `outcome_output_observation_gap=true` only when a
source-locked outcome contract exists, the exact command is observed once, the
command succeeds, the validator is not inspected, and the required sentinel is
still absent. Outcome verification and contract match remain false.

Matched pairs now publish aided and control gap booleans, one bounded effect
class (`none`, `aided_only`, `control_only`, or `both`), and
`outcome_lift_observation_clean`. A positive or negative lift can therefore stay
visible while reviewers can see that its output observation is not clean. No
new skill failure class is introduced because the gap can occur in either arm
after a correct command and is not evidence that a source skill routed badly.

Read-only projection of the reviewed clean-aided v14 private receipt produces
`none` plus a clean lift for `collision-09`, and `control_only` plus
`outcome_lift_observation_clean=false` for `collision-14` and `collision-38`.
The committed v14 receipt remains immutable. V15 applies to future runs and
keeps historical projection backward-compatible; after exact merge, the next
live step returns to the full pilot rather than repeating a source repair.

## 2026-07-12 complete v15 full pilot

The exact-merged v15 widening completes all 30 turns and all eleven pairs with
zero failure classes. Prompt and background locks, filesystem and inventory
scope, fixture execution, dispatch and load, transport process, owner boundary,
proof, promotion, and the root/structured arms all remain clean. Runtime parity
was reverified at 36/36 before execution, and post-run memory, resource, and
storage validators report zero failures or warnings.

Five pairs show positive route and selected-procedure lift:
`collision-01`, `collision-03`, `collision-08`, `collision-38`, and
`collision-42`. The decision and eval roots (`collision-38` and
`collision-42`) also show positive full-child trajectory lift. The other six
pairs are no-lift-both-correct on route and procedure, which is the honest
result for explicit/manual boundaries already recoverable from the control
prompt.

Outcome telemetry prevents overclaiming. Seven pairs are
observation-clean and correct in both arms. `collision-03` and `collision-08`
show apparent positive outcome lift only because the control has a
`control_only` sentinel gap. `collision-20` and `collision-33` show apparent
negative lift only because the aided arm has an `aided_only` gap. All four exact
commands were single-attempt, zero-exit, and validator-uninspected, so their
missing sentinel remains an observation defect rather than a source-skill
verdict.

The full pilot therefore closes the repaired routing slice but does not justify
one aggregate family score. The next broad plans are much larger and only
partially contract-covered: `full-collision` is 98 turns with 10/49 procedure
and outcome pairs declared, while `coverage-closure` is 87 turns with 1/17
paired contracts plus broad root/structured arms. Before spending sustained
cohort budget, partition those surfaces into bounded contract-complete waves;
do not use missing answer keys as silent unscored success.

## 2026-07-12 v16 bounded broad-cohort partitions

The broad parents remain complete inventory views, but no longer need to be
the execution unit. `full-collision` is partitioned into five semantic waves:
core engineering, safety and overlays, session growth, authority routing, and
eval children. `coverage-closure` is partitioned into core implicit cases, two
Titan implicit waves, all root-child trajectories, non-Titan structured input,
and Titan structured input. The eleven child waves are disjoint and their
trial-identity union exactly equals the two parents.

The partition is an executable contract, not a documentation grouping. Every
wave must use `required` or `required_for_live` for both implicit contract axes,
require the second source-locked confirmation, stay at or below 30 turns,
512 MiB estimated private evidence, 512 MiB estimated memory, and the medium
resource class. The runner rejects overlap, missing parent trials, extra
trials, unscored modes, or a wider resource envelope during plan load.

The first runnable wave is `full-collision-core-engineering`: all sixteen arms
for `collision-01` through `collision-08`. Five new source-derived contracts
cover property authoring, core-versus-glue separation, port and adapter
refactoring, TDD slicing, and producer-consumer contract tests. Each prompt
lacks the concrete repository surface needed to perform the requested change,
so the honest procedure is `blocked_missing_input` and the bounded owner action
requests the specific source, invariant, caller, test, or interface evidence.
Together with the three earlier pilot anchors, the wave is 8/8 on procedure and
8/8 on outcome coverage. Later implicit waves remain plan-visible but stop
before preflight until their own answer keys are authored; root and structured
waves have no implicit pair axis and retain their existing dispatch/load
contracts.

## 2026-07-12 first v16 core-engineering execution return

The exact-merged core wave completes all sixteen turns and eight pairs. All
eight aided arms select the intended skill, satisfy load, report the
source-locked `blocked_missing_input` procedure, and gain route plus procedure
correctness over control. Six owner-action comparisons are observation-clean
and correct in both arms. This is strong candidate evidence that the core
engineering skills add routing and procedural discipline when concrete source
inputs are absent, but it is not yet a clean wave receipt.

Three arms retain `fixture_execution_gap`: `collision-01` control and both
`collision-02` arms. In each, the one exact fixture command is observed and
exits zero, but its captured output is exactly zero bytes; the other thirteen
arms expose the same 234-byte valid sentinel payload. This is a fixture-output
observation return, not evidence to edit `aoa-invariant-coverage-audit` or
`aoa-property-invariants`, and the sentinel requirement remains unchanged.

Outcome telemetry independently qualifies two comparisons. `collision-05` is
`aided_only` and `collision-06` is `control_only`, so their raw negative and
positive lifts are observation-unclean. The other six pairs are clean
no-lift-both-correct outcomes. Preserve the full receipt as `needs-rerun`, add
`full-collision-core-engineering-returns` with both arms of only
`collision-01` and `collision-02`, and repeat after exact merge. Do not rerun
the other six pairs or widen to the next collision wave until the fixture
return is classified.
