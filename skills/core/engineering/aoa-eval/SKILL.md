---
name: aoa-eval
scope: core
status: scaffold
summary: Route AoA eval-lane work by raising the available session readiness packet and Eval Forge front door, finding existing local or central eval surfaces first, then selecting apply, local-need, design, or session-mining from route signs without moving proof authority.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-0003
  - AOA-T-0076
  - AOA-T-0094
---

# aoa-eval

## Intent

Use this skill as the front door for AoA evaluation work. It decides whether a
task should inspect existing evals, apply an existing eval or validator, record
repo-local eval pressure, design a local eval suite, or mine `.aoa` session
evidence for missed eval triggers.

When the OS Abyss `aoa-evals` workspace is available, this skill also starts by
raising the read-only eval session readiness packet so a fresh agent can see the
current tools, local eval ports, stop lines, freshness blockers, and
candidate-only packet contract before choosing a subskill.

When that packet exposes `eval_forge_front_door`, use it as the live Eval Forge
orientation surface. It should point to the Forge operating path
`mechanics/proof-object/parts/eval-authoring/docs/EVAL_FORGE_OPERATING_PATH.md`,
the session-mining criteria/reject taxonomy
`mechanics/proof-object/parts/eval-authoring/docs/SESSION_MINING_CRITERIA.md`,
the local-port decision matrix
`mechanics/proof-object/parts/eval-authoring/docs/LOCAL_PORT_DECISION_MATRIX.md`,
the latest route-review report, the worksheet example, and exact route
commands. These references are routing aids, not proof authority.

## Trigger boundary

Use this skill when:
- the user asks whether an eval exists, whether one should be added, or how to
  connect evals to a repository
- a repeated failure, validation gap, proof gap, regression, trigger miss, or
  local `evals/` port appears during repository work
- route signs can trigger this skill even when the user never says `eval`:
  repeated agent route failure, skipped validator/test/script evidence, unsafe
  proof/local/MCP/session mixing, or missed trigger behavior is enough pressure
- the task mentions `aoa-evals`, `aoa-evals-mcp`, local eval ports, eval intake,
  graders, traces, regressions, validators, tests, or scripts as evaluation
  surfaces
- a repo-family or workspace-local eval-port inventory, or missing/skeleton/active/invalid port status, is available before choosing a local eval route
- an OS Abyss eval session needs a current readiness packet before selecting
  tools or touching local eval files
- session evidence may reveal missed eval moments, but only after web and repo
  owner surfaces have been checked
- a route must separate proof authority, local intake pressure, MCP access, and
  raw session evidence

Do not use this skill when:
- the task is only to add an ordinary unit test with no eval routing question;
  use the normal engineering workflow or `aoa-contract-test`
- keywords alone such as `eval`, `test`, `landing`, or `done` are not
  sufficient without route pressure
- the task is only to find source authority; use `aoa-source-of-truth-check`
- the task is only to record or correct durable rationale; use `aoa-decision`
- the task is only memory candidate writeback; use `aoa-memo-writeback`
- the user explicitly asks to edit central `aoa-evals` proof doctrine; route to
  the `aoa-evals` repo and its validators instead of making this skill the owner

## Inputs

- user intent, target repository, touched paths, failure mode, or eval name
- local `evals/PORT.yaml`, `evals/intake/`, scripts, tests, validators, and repo
  route cards
- central `aoa-evals` docs, schemas, validators, reports, and review surfaces
- optional repo-family or workspace local-port inventory/read-model; in OS
  Abyss this may be `aoa-evals/scripts/build_local_eval_port_inventory.py`
- optional OS Abyss eval session-start/readiness command; when present this is
  `aoa-evals/scripts/aoa_eval_session_start.py`
- optional `eval_forge_front_door` packet fields from session-start/readiness:
  `surface_refs`, `exact_commands`, `surface_status`, stop-lines, and
  non-proof boundary flags
- optional candidate-packet validator; when present this is
  `aoa-evals/scripts/validate_eval_candidate_packets.py`
- `aoa-evals-mcp` packets when available, treated as access-plane data
- optional `.aoa` session evidence through `aoa-session-memory-evidence-route`
  when the task asks how an eval, validator, test, MCP, failure, or trigger was
  used in prior sessions
- `.aoa` search hits, segments, raw refs, and freshness only when session mining
  is the chosen route

## Outputs

- exactly one chosen route: `aoa-eval-select`, `aoa-eval-apply`,
  `aoa-eval-local-need`, `aoa-eval-design`, or `aoa-eval-session-mining`
- owner-boundary statement naming proof owner, local port owner, and any MCP or
  `.aoa` evidence role
- session-start status when a workspace readiness command exists, including
  freshness blockers and stop lines that constrain the route
- selected Eval Forge front-door refs and commands when the readiness packet
  exposes them, with proof authority explicitly kept false
- selected existing eval, validation command, intake packet path, draft suite, or
  session-mining report
- stop line when no owner surface is safe to write

## Procedure

1. when an OS Abyss `aoa-evals` checkout is available, raise the read-only
   session readiness packet before choosing a subskill:
   - from the `aoa-evals` repo, run
     `python scripts/aoa_eval_session_start.py --json`
   - treat its active repo routes, support registry, candidate queue summary,
     freshness blockers, and stop lines as advisory routing evidence
   - if it exposes `eval_forge_front_door`, inspect `surface_refs`,
     `exact_commands`, `surface_status`, and non-proof boundary flags before
     classifying the route
   - use `EVAL_FORGE_OPERATING_PATH.md` for the first operating path,
     `SESSION_MINING_CRITERIA.md` before session mining,
     `LOCAL_PORT_DECISION_MATRIX.md` before local intake/design, and the
     worksheet example before owner-review worksheet work
   - if the command is missing or fails, name that gap and continue with local
     and central source inspection instead of inventing a route
2. before importing `.aoa` or trace-derived eval candidates, validate the
   candidate-only contract when the validator is available:
   `python scripts/validate_eval_candidate_packets.py --schema-only`; validate
   any actual packet path before using it as candidate evidence
3. classify the pressure:
   - existing eval may fit: use `aoa-eval-select`
   - existing eval or validator should run: use `aoa-eval-apply`
   - no eval fits and a repo-local pressure packet is needed: use
     `aoa-eval-local-need`
   - a local eval suite or report needs design: use `aoa-eval-design`
   - `.aoa` evidence should be mined for missed trigger cases: use
     `aoa-eval-session-mining`
4. if a repo-family or workspace local-port inventory is available, consult it
   before local need/design/session mining to distinguish missing, skeleton,
   active, invalid, and stale local surfaces; treat inventory route keys as
   advisory routing evidence, not proof or mutation authority
5. check local owner route first: repository `AGENTS.md`, `evals/PORT.yaml`,
   nearby validators, tests, scripts, and local route docs
6. check central `aoa-evals` only for proof doctrine, local-port contract,
   central bundles, scoring, verdicts, or review rules
7. use `aoa-evals-mcp` only as a runtime access plane; do not let an MCP packet
   create proof truth or write central eval bundles
8. when prior-session behavior matters, use `aoa-session-memory-evidence-route`
   or the equivalent `aoa-session-memory-mcp` read-only packet to find usage,
   consequence, failure, and raw refs; keep those refs candidate-only until the
   local or central eval owner accepts them
9. load exactly one subskill after classification; keep the other subskills out
   of context unless the route changes
10. if no safe route exists, stop with the missing owner evidence and the next
   narrow source to inspect
11. after any write or eval run, report the route, owner surface, evidence used,
   validation command, and remaining proof risk

## Contracts

- `aoa-evals` owns proof doctrine and central eval verdicts
- local repositories own their `evals/` ports and can hold intake pressure
  without becoming proof authorities
- `.aoa` raw traces are candidate evidence, not reviewed truth
- `aoa-session-memory` evidence routes can locate usage and consequences, but
  they do not own proof doctrine, verdicts, scoring, baselines, or eval
  promotion
- session-start packets, generated dashboards, support registries, and candidate
  queue summaries are read-only routing aids, not proof objects
- Eval Forge front-door references and route commands help choose the next
  owner route, but they do not score, promote, accept, or prove an eval
- candidate packets must remain candidate-only until reviewed by the owning
  local or central surface
- MCP tools are access planes and must not silently promote local pressure into
  central proof
- workspace inventories and route read-models are advisory selectors; source
  files and owner validators remain stronger
- the router chooses one subskill to control scope and avoid mixed authority
- new evals should be created only after existing local and central surfaces were
  inspected

## Risks and anti-patterns

- treating every test as an eval or every eval as a central `aoa-evals` object
- creating a local eval need before checking existing validators and tests
- skipping an available session-start packet and then designing from stale local
  memory
- letting `.aoa` search hits override repo-local source files
- importing trace or session evidence without candidate-packet validation
- treating a readiness dashboard, generated reader, or candidate queue as a
  verdict, score, baseline, or proof promotion
- treating the Eval Forge front door as a central proof bundle instead of a
  route into existing surfaces, local ports, worksheets, rejects, or review
- letting MCP writes bypass owner review
- loading every subskill for a simple route decision
- promoting scaffolded trigger pressure to canonical proof without review

## Verification

- confirm exactly one subskill route was selected
- confirm local `evals/PORT.yaml` was inspected or the absence was named
- if a workspace inventory was used, name the inventory command or MCP resource
  and the route recommendation it returned
- if a session-start readiness packet was available, confirm it was run and
  name any freshness blocker or stop line that constrained the route
- when `eval_forge_front_door` is available, confirm its operating path,
  criteria, local-port matrix, route-review or worksheet refs, and exact
  commands were considered as routing evidence only
- confirm central `aoa-evals` authority was kept separate from local intake
- confirm existing scripts, tests, and validators were considered before new
  design
- confirm `.aoa` evidence is marked candidate-only when used
- confirm session-memory evidence packets, if used, include raw/segment/session
  refs and did not replace local or central eval owner review
- confirm session or trace-derived candidate evidence passed the candidate
  packet validator when the validator exists
- confirm any generated or derived surfaces were rebuilt through owner builders
- confirm final report names validation and skipped checks

## Technique traceability

Manifest-backed techniques:
- AOA-T-0003 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/proof/evaluation-chain/contract-first-smoke-summary/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0076 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/governance/decision-routing/owner-layer-triage/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0094 from `8Dionysus/aoa-techniques` at `1a7d146957108ecefc24219c7d56357c5a4a2c2c` using path `techniques/proof/owner-truth-closeout/canonical-owner-with-validated-mirror/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

- local eval-port schema and status vocabulary
- `aoa-evals-mcp` tool names
- repo-local validator/test/script command names
- session search provider and freshness policy
