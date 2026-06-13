---
name: aoa-eval
description: Route AoA eval-lane work by checking existing local and central eval surfaces first, then choosing apply, local intake need, local design, or session mining while preserving owner boundaries. Use when a task asks whether an eval exists, whether one should be added, how local evals connect to aoa-evals, or how validators, tests, scripts, traces, regressions, trigger misses, local eval ports, or aoa-evals-mcp should be used as evaluation surfaces. Do not use for ordinary one-off tests, source-of-truth mapping, decision records, memo writeback, or direct central aoa-evals proof-authority edits.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: core
  aoa_status: scaffold
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/core/engineering/aoa-eval/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0003,AOA-T-0076,AOA-T-0094
  aoa_portable_profile: codex-facing-wave-3
---

# aoa-eval

## Intent
Use this skill as the front door for AoA evaluation work. It decides whether a
task should inspect existing evals, apply an existing eval or validator, record
repo-local eval pressure, design a local eval suite, or mine `.aoa` session
evidence for missed eval triggers.

## Trigger boundary
Use this skill when:
- the user asks whether an eval exists, whether one should be added, or how to
  connect evals to a repository
- a repeated failure, validation gap, proof gap, regression, trigger miss, or
  local `evals/` port appears during repository work
- the task mentions `aoa-evals`, `aoa-evals-mcp`, local eval ports, eval intake,
  graders, traces, regressions, validators, tests, or scripts as evaluation
  surfaces
- session evidence may reveal missed eval moments, but only after web and repo
  owner surfaces have been checked
- a route must separate proof authority, local intake pressure, MCP access, and
  raw session evidence

Do not use this skill when:
- the task is only to add an ordinary unit test with no eval routing question;
  use the normal engineering workflow or `aoa-contract-test`
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
- `aoa-evals-mcp` packets when available, treated as access-plane data
- `.aoa` search hits, segments, raw refs, and freshness only when session mining
  is the chosen route

## Outputs
- exactly one chosen route: `aoa-eval-select`, `aoa-eval-apply`,
  `aoa-eval-local-need`, `aoa-eval-design`, or `aoa-eval-session-mining`
- owner-boundary statement naming proof owner, local port owner, and any MCP or
  `.aoa` evidence role
- selected existing eval, validation command, intake packet path, draft suite, or
  session-mining report
- stop line when no owner surface is safe to write

## Procedure
1. classify the pressure:
   - existing eval may fit: use `aoa-eval-select`
   - existing eval or validator should run: use `aoa-eval-apply`
   - no eval fits and a repo-local pressure packet is needed: use
     `aoa-eval-local-need`
   - a local eval suite or report needs design: use `aoa-eval-design`
   - `.aoa` evidence should be mined for missed trigger cases: use
     `aoa-eval-session-mining`
2. check local owner route first: repository `AGENTS.md`, `evals/PORT.yaml`,
   nearby validators, tests, scripts, and local route docs
3. check central `aoa-evals` only for proof doctrine, local-port contract,
   central bundles, scoring, verdicts, or review rules
4. use `aoa-evals-mcp` only as a runtime access plane; do not let an MCP packet
   create proof truth or write central eval bundles
5. load exactly one subskill after classification; keep the other subskills out
   of context unless the route changes
6. if no safe route exists, stop with the missing owner evidence and the next
   narrow source to inspect
7. after any write or eval run, report the route, owner surface, evidence used,
   validation command, and remaining proof risk

## Contracts
- `aoa-evals` owns proof doctrine and central eval verdicts
- local repositories own their `evals/` ports and can hold intake pressure
  without becoming proof authorities
- `.aoa` raw traces are candidate evidence, not reviewed truth
- MCP tools are access planes and must not silently promote local pressure into
  central proof
- the router chooses one subskill to control scope and avoid mixed authority
- new evals should be created only after existing local and central surfaces were
  inspected

## Risks and anti-patterns
- treating every test as an eval or every eval as a central `aoa-evals` object
- creating a local eval need before checking existing validators and tests
- letting `.aoa` search hits override repo-local source files
- letting MCP writes bypass owner review
- loading every subskill for a simple route decision
- promoting scaffolded trigger pressure to canonical proof without review

## Verification
- confirm exactly one subskill route was selected
- confirm local `evals/PORT.yaml` was inspected or the absence was named
- confirm central `aoa-evals` authority was kept separate from local intake
- confirm existing scripts, tests, and validators were considered before new
  design
- confirm `.aoa` evidence is marked candidate-only when used
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
