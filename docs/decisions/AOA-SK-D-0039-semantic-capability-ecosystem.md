# Semantic Capability Ecosystem

- Decision ID: AOA-SK-D-0039
- Status: Accepted
- Date: 2026-07-15
- Owner surface: `capabilities/`, `skills/`, `config/`, `mechanics/`, `evals/`,
  `kag/`, and their deterministic projections

## Index Metadata

- Original date: 2026-07-15
- Surface classes: root/topology, skill source, generated/readout, export/runtime, review/governance, validation guard, memory/writeback, mechanic package
- Skill lanes: core/engineering, core/session-growth, core/stewardship, portable/export
- Mechanic parents: agon, questbook, release-support, cross-mechanic
- Guard families: source topology, generated/read-model, export/runtime, release/tooling, questbook, memo writeback, evaluation/public surface
- Posture: accepted semantic capability ecosystem v2

## Context

The repository had grown to 57 separately routed skills plus technique
manifests, activation machinery, evaluation proxies, review readouts, mechanics,
and generated registries. Many leaf skills were actually modes of the same
procedure. Their descriptions competed for limited discovery context, several
validators protected retired topology rather than behavior, and mandatory
technique lineage made a portable procedure depend on a sibling representation.

The required future shape is an agent-OS capability ecosystem: discovery must
stay small, composition must preserve real input/output and compatibility
relations, effects must remain owner-scoped, and a skill must earn its place by
improving held-out work rather than by passing structural checks. Session-memory
systems may provide candidate evidence, but their availability and quality
cannot be a runtime prerequisite for the skill layer.

## Options Considered

- Repair all 57 bundles in place, retain technique manifests, and strengthen
  their routers and validators.
- Replace the catalog with a few broad monolithic skills and encode all routing
  in prose.
- Model a semantic capability tree plus typed cross-relations, expose only
  independently callable bundles, and assemble a task-local DAG for execution.

## Decision

Choose the third option.

1. `capabilities/families/*.yaml` owns the semantic capability tree. Every node
   has one primary parent for navigation; typed relations carry requirements,
   products, composition, handoff, alternatives, conflicts, adaptation, and
   supersession.
2. A task selects the smallest compatible capability set and assembles a
   task-local DAG from declared inputs, outputs, effects, tools, and relations.
   The DAG is runtime/session state and is never committed as repository truth.
3. `skills/**/SKILL.md` exists only for independently callable procedural
   bundles. The initial source surface is seven bundles: `aoa-decision` is
   advertised; engineering-shape, eval, verification, knowledge-stewardship,
   session-harvest, and session-recovery remain deferred until held-out manual
   evidence justifies wider discovery.
4. The former 57 skills are accounted for in
   `capabilities/legacy-skill-migration.yaml` as absorbed modes, aliases,
   external owner routes, or retired behavior. Compatibility names aid search;
   they do not recreate callable child bundles.
5. Technique references are optional provenance only. No source build, export,
   discovery, planning, or execution contract may require `aoa-techniques` or
   a `techniques.yaml` file.
6. Skills own procedures; MCP and runtime owners provide live actions/data;
   playbooks own stabilized multi-step workflows. Portable `.agents/skills/*`
   stays a flat generated host projection, while KAG stays a derived discovery
   and return map.
7. Manual comparison is the behavioral authority: no skill, current skill,
   candidate/composition, direct versus retrieval, positive versus negative,
   isolated versus coexistence, and flat selection versus task-local DAG where
   relevant. Validators are admitted only for durable deterministic invariants
   observed through that work; a green result never promotes a capability.
8. Raw traces, one-session reports, task-local plans, and session identifiers
   remain session-owned. This repository keeps only reusable owner sources and
   owner-safe projections; it does not pre-create an empty local memo port.
9. Active mechanics are limited to Agon candidate intake, Questbook durable
   obligations, and release support. Agon requests enter as capability
   candidates, not presumptive skills. Other former mechanics remain in Git
   history unless a current independent owner contract re-establishes them.

## Rationale

The tree makes discovery explainable without exposing every atomic operation.
Typed relations preserve composition that a pure directory hierarchy cannot,
and a task-local DAG avoids turning one reusable sequence into a universal
workflow. Seven focused bundles keep portable discovery bounded while the
capability graph can still represent external tools, guards, workflows, human
gates, and internal modes without multiplying `SKILL.md` files.

Optional technique provenance preserves useful lineage without coupling skill
availability to a sibling repo. Manual-first lifecycle decisions prevent
structural tests, generated reports, or session-memory retrieval from becoming
surrogate outcome truth. Explicit owner and session boundaries keep the
repository durable and public-safe.

## Consequences

- Positive: discovery pressure falls from 57 competing bundles to one
  advertised front door plus six deliberate challengers.
- Positive: every former skill has an explicit destination; removed source is
  recoverable from Git history without active compatibility scaffolding.
- Positive: composition, conflicts, effects, provenance, lifecycle, and owner
  return routes are machine-readable without making the graph execution truth.
- Tradeoff: six bundles remain intentionally harder to discover until manual
  trials establish benefit and coexistence safety.
- Tradeoff: tree/graph/DAG parity and portable projection add deterministic
  maintenance work, but that work protects an actual cross-surface contract.
- Tradeoff: platform and model behavior must be rechecked; common Markdown
  format does not imply runtime parity.
- Follow-up: repeat clean-host and held-out manual trials after material model,
  host, owner-contract, or workflow drift; revise, promote, split, merge,
  demote, or remove candidates only when new evidence changes the disposition.

## Supersession Map

- This decision supersedes the active topology portions of AOA-SK-D-0015,
  AOA-SK-D-0019, AOA-SK-D-0021, AOA-SK-D-0022, AOA-SK-D-0023,
  AOA-SK-D-0026, AOA-SK-D-0036, AOA-SK-D-0037, and AOA-SK-D-0038.
- It revises the concrete lane, validator, test, and script inventories of
  AOA-SK-D-0028 through AOA-SK-D-0031 while preserving their source/derived and
  single-command-authority principles.
- It absorbs the callable child-chain implementation of AOA-SK-D-0034 and
  AOA-SK-D-0035 into the `aoa-decision` family while preserving authored
  decision records as authority and graph lookup as a bounded aid.
- AOA-SK-D-0017's requirement for lived-use evidence remains valid, now under
  the stricter manual baseline/challenger and held-out lifecycle rule.

## Current Applicability

As of 2026-07-17, the authored tree contains ten families, 98 nodes, and 162
typed relations. Nine shared source bundles exist. Seven are advertised
challengers: `aoa-checkpoint-closeout-bridge`, `aoa-decision`, `aoa-eval`,
`aoa-knowledge-stewardship`, `aoa-memo-writeback`, and
`aoa-session-harvest`, plus `aoa-session-recovery` after its natural
coexistence case. Engineering-shape and verification remain degraded and
deferred while their preserved procedures and natural retrieval value are
evaluated. Advertisement records a bounded current
disposition; it does not establish global installation, general outcome lift,
or baseline equivalence.
The old source bundles, mandatory technique bridge, old eval/stat proxies,
Spark lane, obsolete mechanics, inherited review records, and repo-local memo
candidate port have left the active tree.

The 57-entry migration map is a functional-disposition ledger, not a list of
renames. All fifty-seven entries are now `manual-evaluated`. The final closed slice
adds the fifteen Titan functions, the Artifact Trust function, and both ATM10
overlays to the earlier thirty-eight dispositions, then closes
`abyss-self-diagnostic-spine` through its installed-profile fresh-session
trial. No entry advanced from a graph target, installed filename, plausible
final answer, or green structural check alone.

## Review Log

### 2026-07-23 - Close the final diagnostic disposition through real execution

- Discovery result: a fresh neutral Codex session received only a natural
  request for current read-only `agent-full` state with truth goal
  `live_available`. It selected only `abyss-self-diagnostic-spine` from the
  complete installed profile without being given the skill name.
- Source-return result: the session read the installed bundle and its
  `aoa_skill_source_receipt_v2`, verified all package identity dimensions,
  followed the exact clean `abyss-stack` owner root, read the canonical
  contract and only the selected `observe` procedure, and searched no sibling
  checkout.
- Execution result: it invoked `scripts/aoa-diagnose --preset agent-full
  --truth-goal live_available` exactly once with no pipe, redirect, wrapper, or
  write flag. The owner command returned a current
  `diagnostic_session_v1` and exit code `1`; the agent correctly preserved that
  as typed `repairable_under_governance` evidence rather than a tool failure.
- Effect and claim result: source-authored, deployed, trial-proven, and
  live-available truth stayed separate; mixed warn, fail, and pass axes and
  drift classes remained explicit. No capture, latest refresh, repair,
  restart, promotion, quest mutation, or recovery execution occurred.
- Verdict and limit: mark `abyss-self-diagnostic-spine`
  `manual-evaluated`, completing all 57 functional dispositions. This proves
  natural discovery, owner source return, one current read-only owner
  execution, typed result handling, and bounded handoff on the exercised host.
  It does not prove global Abyss health, repair correctness, all selectors,
  cross-host behavior, or future routing after material catalog or runtime
  drift.

### 2026-07-23 - Restore Titan as three owner bundles plus real owner routes

- Packaging result: fifteen former Titan names no longer compete as fifteen
  global Markdown entries. `aoa-sdk` owns three callable packages:
  `titan-console` for console, approval witness and queue, unsent plan, and
  receipt modes; `titan-appserver-bridge` for visible bridge and replay modes;
  and `titan-memory-loom` for candidate ingest, recall, and effect-free
  retention handoff. Their conditional procedures, typed ABI, effects,
  verification, failure modes, and manual-case health remain in the owner
  packages rather than in this graph.
- Owner split: `aoa-summon` remains the executable summon procedure in
  `aoa-agents`; reviewed retention and pruning meaning remains with
  `aoa-memo`. The graph records those handoffs without pretending the SDK owns
  role, durable-memory, or operator authority.
- Guard result: mutation, runtime-transition, and thread-turn enforcement stay
  blocked and unavailable. SDK normalization and witness helpers are
  provenance for those requirements, not live guard owners and not a reason
  to advertise fictitious guard skills.
- Workflow result: Titan closeout remains a degraded `aoa-playbooks` route.
  No new closeout skill is created before an executable `aoa-playbooks` MCP
  owner exists.
- Verdict and limit: all fifteen legacy dispositions are
  `manual-evaluated`. This proves the owner-package consolidation, exercised
  helper behavior, negative routing, owner handoffs, and unavailable-guard
  honesty. It does not prove live Titan runtime enforcement, hidden execution,
  operator authentication, or executable playbook closeout.

### 2026-07-23 - Promote Artifact Trust from adapter label to owner procedure

- Representation correction: the former migration target named only the
  read-only central adapter. The functional successor is now the
  `abyss-machine` owner package `os-abyss-artifact-trust-loop`; the adapter
  remains a derived read route and cannot replace the procedure.
- Manual result: natural pre-consumption selection, authorized producer work,
  positive local-agent admission, empty-registry unknown, source-ref mismatch
  denial, production-consumer manual review, degraded MCP fallback, ordinary
  source-edit exclusion, and neighboring release/eval coexistence all
  preserved the distinct inspect, prepare, admit, and audit phases.
- Verdict discipline: `allow`, `warn`, `deny`, `manual_review_required`,
  `unknown`, and `not_applicable` stayed distinct. Build success did not become
  promotion or consumption authority, and stale or incomplete MCP evidence
  returned to the owner CLI.
- Verdict and limit: mark `os-abyss-artifact-trust-loop`
  `manual-evaluated` and advertise its owner package. This proves the exercised
  artifact classes and owner surfaces, not universal producer coverage,
  runtime trust-root enforcement, release authorization, or cross-host parity.

### 2026-07-23 - Keep ATM10 as evaluated owner adapters, not copied skills

- Authority comparison: no skill found the correct owner roles but performed a
  broad scan; the retained overlay bounded the route; the current
  `aoa-knowledge-stewardship` authority mode plus the ATM10 adapter preserved
  the same result through exact owner records and return handles. Observed raw
  input was 111,410, 59,084, and 66,572 tokens respectively on those exercised
  arms.
- Change comparison: the host-native repository-change loop and old overlay
  both produced a correct change, but the overlay imposed intent-chain,
  test-first, and rollback ceremony even where the owner task did not require
  it. Observed raw input was 54,466 without the overlay, 60,046 with it, and
  65,749 for the current host loop plus owner adapter.
- Disposition: neither overlay earns a callable global bundle. Their remaining
  value is an owner-qualified semantic adapter: one binds a requested or
  prospective change to current ATM10 route law; the other resolves an actual
  source-role conflict from exact supplied surfaces. Decision rationale stays
  with the decision owner.
- Verdict and limit: mark both ATM10 entries `manual-evaluated`. Removing the
  repository's stale shared skill copies remains gated on a fresh OS profile
  that exposes every shared front door removed from that repository.

### 2026-07-17 - Close four generic risk packages into enforcement and owner bindings

- Trial posture: fresh isolated Codex CLI `0.144.5` sessions on model
  `gpt-5.6-sol` compared no skill with the exact `94e5d0e` procedure against
  bounded owner contracts, including deliberately missing bindings. Original
  packages that were not host-visible were loaded directly so procedure value
  remained separable from discoverability failure. Raw prompts, traces,
  fixtures, checksums, and task-local reports remain session-owned.
- Approval result: both no-skill and the retained procedure refused the
  mutation when the user had not explicitly authorized the exact operation and
  supplied its matching confirmation token. A colleague request and a token
  merely present in owner material were correctly insufficient. The old skill
  adds a reviewable classification, but neither that classification nor any
  skill can grant or prove authority. Its successor is the acting runtime and
  target-owner enforcement route; the guard remains deferred with
  `manual-baseline` enforcement evidence even though the legacy disposition is
  now evaluated.
- Preview result: both arms ran only the target owner's preview, named the
  exact unexecuted apply action, stated what preview did and did not prove, and
  left owner state unchanged. The retained procedure additionally compared a
  checksum, but this did not create distinct outcome value on the exercised
  case. Preview implementation therefore belongs to the target owner, not a
  generic host prose skill. Its shared route is dormant and unavailable until
  an exact owner preview binding exists.
- Local-stack result: both bound arms rendered the selected service set, ran
  selector-matched readiness, started exactly once, observed owner status, and
  exposed the stop command without executing it. The retained procedure makes
  the order `render -> doctor -> start once -> status` explicit. The unbound
  case returned `blocked_binding_unavailable` without inventing services,
  commands, or a stop path. The preserved capability is therefore an
  owner-bound workflow, not a generic global skill.
- Infrastructure result: both bound arms applied the one authorized mutation
  exactly once and observed the owner's resulting state. The retained
  procedure preserved the stronger sequence
  `inspect -> preview -> apply once -> verify`, while the unbound case stopped
  as `blocked_binding_unavailable`. Rollback remained a separately authorized
  operation and was not executed. The successor stays unavailable until a
  target owner supplies the exact mutation, verification, and recovery
  binding.
- Contract correction: approval now explicitly distinguishes routing from
  enforcement. Preview is owned by the target runtime owner and cannot be
  satisfied by a plan or agent explanation. Local-stack and infrastructure
  workflows preserve their observed operation order, one-effect boundary,
  claim limits, and unbound failure state. All four retain the old package only
  as optional functional-baseline provenance and create no replacement skill
  bundle.
- Verdict and limit: mark all four legacy entries `manual-evaluated`.
  `aoa-dry-run-first` is baseline-equivalent; approval still requires runtime
  enforcement; local-stack and infrastructure remain owner-bound actions.
  These results prove the four dispositions on the exercised owner contracts.
  They do not prove universal host enforcement, any real target-owner binding,
  failed-start recovery, rollback execution, cross-model parity, or general
  cost superiority.

### 2026-07-17 - Replace three generic skills only after host-workflow equivalence

- Trial posture: fresh disposable repositories compared no skill with the
  exact `94e5d0e` procedure on Codex CLI `0.144.5`, model
  `gpt-5.6-sol`, maximum reasoning, isolated skill homes, and no user goals,
  memories, or hooks. Raw prompts, traces, and fixtures remain session-local.
  Metadata-only compatibility projection was used only when the old package
  itself was not prompt-visible; that discoverability failure remains part of
  the result.
- Repository-change result: both arms changed only the authored source,
  invoked the owner builder, checked the builder result and diff, preserved
  unrelated state, and stopped without a commit. No skill used 15,981 raw
  input tokens and the old skill used 54,337 on the exercised positive case.
  On a tiny wording-edit negative case, the old skill falsely activated,
  loaded its body, and only then applied its own exclusion. The host-native
  workflow therefore preserves the positive procedure with lower observed
  discovery cost and avoids retaining that global false-positive route.
- Test-first result: both arms observed a real red failure, made the same
  minimal green change, ran the focused and owner checks, and preserved scope
  on both a pure module case and a held-out builder/export case. The module
  comparison used 29,977 raw input tokens without the skill and 43,448 with
  it; the builder comparison used 35,717 and 19,150 respectively. The
  exploratory negative case selected no TDD skill and made no change. These
  opposite cost results support behavioral equivalence, not general token,
  latency, or outcome superiority.
- Local-commit result: under workspace-write both arms attempted the correct
  bounded stage but stopped truthfully when the host could not create
  `.git/index.lock`. In disposable danger-full-access repositories, both arms
  committed only the authorized file, left unrelated dirty work untouched,
  and stopped before push. No skill used 6,851 raw input tokens and the old
  compatibility package used 11,641. The original old package was not
  prompt-visible, while the compatibility projection falsely activated on a
  review-only request before returning a correct deferred disposition.
- Contract correction: `aoa-change-protocol` and `aoa-tdd-slice` now route to
  evaluated host-native workflows. `aoa-commit-growth-seam` routes to the new
  narrow `workflow.operations.local-commit`, whose ABI preserves explicit
  authorization, unrelated-state exclusion, verification debt, metadata-write
  failure, and the stop before every remote effect. The broader remote Git
  closeout is separate and remains unbound until independently evaluated.
  Host provenance records the exact observed runtime version as evidence, not
  as an invented authored package; the old skill paths remain optional
  functional baselines at their exact commit.
- Verdict and limit: mark all three legacy entries `manual-evaluated` with
  baseline equivalence and add no replacement skill bundle. Their successor is
  globally present as host behavior rather than discovered through the skill
  catalog. This proves the exercised positive, negative, failure, and held-out
  cases on one host/model contract. It does not prove universal host
  availability, remote Git closeout, cross-model parity, or future behavior
  after a material runtime contract change.

### 2026-07-17 - Restore engineering-shape procedures without promoting discovery

- Observed loss: the first consolidated `aoa-engineering-shape` package kept
  three mode names but compressed away the operational boundary-lens,
  core-shape, and adapter-seam tables that made the old procedures usable
  beyond generic architecture advice. A correct-looking final answer did not
  preserve those procedures.
- Correction: version `0.2.1` keeps one short front door and restores the full
  old operational shapes in exactly one conditionally loaded `contexts`,
  `core`, or `port-adapter` reference. Technique lineage is no longer a
  runtime dependency. The owner contract, typed output, unresolved-owner
  posture, mode handoffs, and stop lines remain explicit.
- Manual result: direct old/current/candidate comparisons covered overloaded
  context vocabulary, a leaking database dependency, a stable rule mixed
  with delivery, and a sequencing case where an unresolved access-policy
  owner required `contexts` before `core` or `port-adapter`. The candidate
  selected one mode, loaded only its contract and selected procedure, kept
  owner gaps unresolved, produced the expected typed boundary, and changed no
  target files.
- Counter-evidence: on the exercised explicit fixtures, no-skill produced
  materially equivalent boundary decisions with lower context cost. The
  candidate therefore proves procedure preservation, not added outcome value
  or a reason for implicit discovery.
- Discovery result: a natural full-profile request selected
  `aoa-engineering-shape` and the `core` procedure. The first result assigned a
  route owner to an unrelated source file; after the owner-resolution contract
  was tightened, the fresh rerun kept that source owner unresolved and loaded
  no sibling AoA procedure.
- Verdict and limit: mark `aoa-bounded-context-map`,
  `aoa-core-logic-boundary`, and `aoa-port-adapter-refactor`
  `manual-evaluated` with baseline equivalence. Keep
  `aoa-engineering-shape` deferred because the exercised no-skill arms reached
  equivalent boundaries at lower context cost; functional preservation and
  natural selection do not yet justify permanent implicit discovery.

### 2026-07-17 - Restore verification procedures without promoting discovery

- Observed loss: the first consolidated `aoa-verification` package retained
  the names `contract`, `coverage-audit`, and `property`, but compressed away
  the operational tables that defined consumer seams, invariant-to-check
  mapping, independent oracles, counterexample shrinking, durable-check
  admission, and precise claim limits.
- Correction: version `0.2.3` keeps one short front door and restores one
  conditional procedure per mode. It reads the authoritative owner rule before
  implementation, checks, examples, or generated views; uses exact supplied
  paths before search; runs a named check only when it adds distinct evidence;
  does not retry a check under altered framework settings; and stops expanding
  a falsified property after a minimal counterexample unless an independent
  property, shrink, or bounded positive subdomain remains. Technique lineage
  is not a runtime dependency.
- Manual result: direct no-skill, retained-baseline, compressed-current, and
  restored-candidate comparisons covered a receipt producer/consumer contract,
  a route-normalization property, and a source-coverage claim. The restored
  candidate exposed active receipts with missing source identity, last-write
  wins and forbidden commit substitution, and a green coverage check that hid
  stale and unresolved owners. It preserved the independent oracle, effect
  boundary, no-check decision where writes were forbidden, and exact claim
  limit without creating a test or validator.
- Route result: after correction, the three candidate cases used 11, 8, and 11
  read-only commands with 171,942, 139,389, and 138,482 raw input tokens. They
  avoided repository-wide inventory, status and hash collection, altered-test
  retries, duplicate property runs, and unrelated procedure loading.
- Counter-evidence: no-skill and the compressed current package reached
  materially equivalent outcome conclusions on these explicit fixtures.
  Restoring the procedures therefore proves functional preservation and a
  more bounded route, not general outcome lift or a reason for implicit
  discovery.
- Coexistence debt: the full-profile coverage case also loaded the global
  session-memory route and searched memory despite complete exact fixture
  inputs. That is a separate false-activation defect in the neighboring
  session-memory route; it is not evidence against the verification procedure,
  and no `.aoa` owner surface was changed here.
- Discovery result: a natural full-profile coverage question selected
  `aoa-verification`, ran the unchanged owner check once, and used manual cases
  plus source inspection to expose the green check's exact false claim. The
  neighboring session-memory route also activated despite complete local
  inputs; this remains a coexistence defect outside the verification package.
- Verdict and limit: mark `aoa-contract-test`,
  `aoa-invariant-coverage-audit`, and `aoa-property-invariants`
  `manual-evaluated` with baseline equivalence. Keep `aoa-verification`
  degraded and deferred: its three procedures are preserved, but no-skill and
  compressed-current arms often reached equivalent conclusions and the
  full-profile collision remains unresolved.

### 2026-07-23 - Bound current home-skill-port selection

- Manual pressure: a fresh-session request supplied an exact owner root and
  named the current AoA home-skill-port acceptance target. `aoa-eval` correctly
  formed `select -> apply`, selected the exact owner validator, ran only that
  command, and returned the strict proof limit. Selection nevertheless read
  session memory, enumerated the target tree, inspected its workflow pin, and
  compared validator history after the exact contract route was already
  sufficient.
- Correction: version `0.2.6` adds a current home-skill-port fast path. It
  reads the supplied target manifest, returns through the installed bundle's
  `aoa-skills` source handle, reads the exact owner contract and validator, and
  then stops discovery. Target-wide inventory, workflow-pin archaeology, and
  Git-generation comparison are excluded unless historical parity is the
  actual request.
- Evidence route: reinstall the candidate and repeat the same held-out
  `select -> apply` task. Require the same exact validator, full apply
  preflight, one command, no write, and strict proof limit with the widened
  discovery absent.
- Claim limit: this is a bounded selection optimization for one current shared
  contract. It does not establish generic latency or token superiority, and
  it does not remove the existing historical-evidence route when history is
  explicitly material.

### 2026-07-17 - Restore, compose, and evaluate the eval family

- Observed loss: the first consolidated `aoa-eval` retained five mode names but
  reduced their operational procedures. Selection widened into unrelated
  repository and session evidence; apply could run with an incomplete
  execution contract; local need did not fail closed on its admitted owner
  schema; and design could imply that apply would create an absent surface.
- Correction: version `0.2.5` keeps one advertised front door and restores
  `select`, `apply`, `local-need`, `design`, and `session-mining` as direct
  conditional references. Selection uses exact supplied paths before a bounded
  relevant inventory and stops when the verdict is decisive. Apply reports
  every required dotted input before target reads or execution. Local need
  requires the admitted owner port and packet schema. Design ends at owner
  review, followed by separately authorized implementation and a new select.
  Technique lineage is not a runtime dependency.
- Selection comparison: on the same no-fit fixture, no skill, the retained
  baseline, and the compressed package reached the same substantive verdict
  but used 18, 17, and 16 commands with 123,467, 130,512, and 126,387 raw input
  tokens and opened unrelated memo, closeout, or session material. The final
  candidate used nine commands and 84,010 raw input tokens, inspected only the
  bounded eval route and inventory, and stopped without execute, intake, or
  design.
- Apply and intake result: with `command.accepted_exit_codes` omitted, the
  final apply route stopped before reading the target or running a command,
  while all comparison routes executed. With a complete contract it ran only
  the selected command and separated exit status, invariant verdict, actual
  effect, and proof limit. Local need likewise blocked without the owner schema
  and, with complete inputs, returned one schema-conforming owner-review packet
  without creating a validator or suite.
- Baseline-equivalent modes: design returned bounded manual cases, false-green
  risks, a future deterministic component, and owner review without creating
  scaffolding. Session mining preserved provider, freshness, raw provenance,
  rejected cases, and eval-specific next routes without becoming generic
  harvest or memo writeback. Both preserved the old functional baseline but
  did not demonstrate general outcome lift.
- Discovery, coexistence, and composition: a natural eval request selected
  only `aoa-eval`; an already named ordinary test selected no AoA skill; an
  eval-plus-verification request selected the eval front door and ran the exact
  local check; and a direct task-local `select -> apply` composition loaded the
  two procedures, matched the source digest, ran exactly one owner command, and
  observed six of six checks passing.
- Counter-evidence and limit: no-skill often reached the same final conclusion,
  so the supported gains are bounded discovery, preflight, owner/schema
  discipline, effect control, and smaller relevant context, not general answer,
  model, token, or latency superiority. The first composition fixture also
  exposed a wrong module path; the fixture was corrected and the failure
  remained visible rather than being reclassified as success.
- Verdict: advertise `aoa-eval` as an evaluated challenger. Mark
  `aoa-eval`, `aoa-eval-select`, `aoa-eval-apply`, and
  `aoa-eval-local-need` `manual-evaluated` with demonstrated added value.
  Mark `aoa-eval-design` and `aoa-eval-session-mining`
  `manual-evaluated` with baseline equivalence. Recheck after material
  host/model, owner-route, or catalog drift.

### 2026-07-17 - Restore and advertise knowledge stewardship

- Observed loss: the compressed knowledge family preserved the
  `sanitized-share` name but did not require the exact destination contract
  before private reads. In a deliberately incomplete task, no-skill, the old
  baseline, the compressed package, and the first restored candidates all
  opened raw material and proposed a derivative. One candidate also borrowed
  the custody owner as destination owner.
- Correction: final package version `0.2.6` keeps one knowledge front door and
  conditionally loads exactly one full procedure. `sanitized-share` requires
  the exact supplied sensitivity and destination contracts before any target
  read, forbids response transport or custody-owner substitution, separates
  inline output, one authorized derivative write, publication, and durable
  memory, and stops direct publication before target reads when its owner
  workflow is absent. `authority-map` restores the old operational authority
  shapes for public/owner overlays, source/config, operations, generated
  transport, provenance, decision rationale, sibling owners, and status.
- Manual result: with complete contracts, the candidate retained the bounded
  technical lesson, removed direct and compositional private topology, stated
  residual correlation risk and exact claim limits, and changed nothing. In an
  authorized disposable case it created exactly one review draft, reread only
  that file once, and performed no inventory, validator, publication, export,
  receipt, or memory write. With the destination contract omitted, the final
  candidate read only its package and returned
  `blocked_missing_input(destination_contract_ref)` while all three comparison
  routes opened raw material.
- Discovery and coexistence: the initial host adapter disabled implicit
  invocation, so a natural positive request bypassed the skill. After the
  description and activation policy were corrected, the same request selected
  only `aoa-knowledge-stewardship`; ordinary prose selected no AoA skill; a
  closeout-retention request selected only `aoa-memo-writeback`; and direct
  publication without its workflow loaded only the knowledge front door,
  returned `blocked_missing_owner_workflow`, and did not open target inputs.
- Authority-map result: on an authored-versus-generated route conflict,
  no-skill incorrectly relabelled the route owner as exact rebuild owner. The
  old baseline, compressed package, and restored candidate kept both rebuild
  owner and missing `source_ref` unresolved and blocked the consumer. In a
  broader public-entrypoint/private-overlay/generated-catalog case, the
  restored candidate selected the same minimal authority shape as the old
  baseline, returned the complete source-to-catalog-to-consumer fan-out, and
  repeated none of the private overlay values.
- Routing correction: the first natural authority request was incorrectly
  captured by `aoa-decision` because its description said generic
  `source/index drift`. The decision trigger now applies only to decision
  record/index drift and explicitly excludes current source authority. The
  repeated request selected only `aoa-knowledge-stewardship`; the exact
  rationale request still selected only `aoa-decision`.
- Counter-evidence and limit: with fully specified safe tasks, no-skill also
  produced useful results at lower context cost in most cases. The demonstrated
  added value is fail-closed pre-raw/effect discipline and one avoided owner
  inference; the authority mode otherwise establishes baseline equivalence, not
  general answer, token, or latency superiority. Results are limited to the
  exercised Codex host, model, profile, and fixtures.
- Verdict: advertise `aoa-knowledge-stewardship` as an evaluated candidate
  challenger. Mark the legacy `aoa-sanitized-share` and
  `aoa-source-of-truth-check` dispositions `manual-evaluated`; the former has
  demonstrated added value and the latter has baseline equivalence. Recheck
  both after host/model or owner-contract drift.

### 2026-07-17 - Restore first writeback without merging it into memo review

- Observed loss: the earlier seven-bundle consolidation represented memo
  writeback as a semantic handoff, but no advertised procedure independently
  noticed a memory-worthy work closeout before a candidate existed. A generic
  harvest classifier also intercepted one natural retention question.
- Correction: `aoa-memo-writeback` version `0.2.8` is again the advertised
  first-writeback front door. `aoa-session-harvest` version `0.2.2` now
  requires an explicitly named reviewed-session input and deflects natural
  work-closeout retention questions to writeback. Existing candidates,
  exports, objects, corpus identities, lifecycle targets, and read-model
  targets route directly to the owner `aoa-memo` bundle.
- Manual result: a natural closeout with no `memo` or `writeback` wording
  selected writeback, loaded only its package, exact closeout, and admitted
  local port, preserved the origin owner versus `aoa-memo` intake-owner split,
  and stopped at `needs_owner_review` without guessing a missing source path.
  An ordinary progress note returned `no_writeback_needed`. A separately
  authorized disposable case created exactly one guarded local candidate,
  reread it once, and created no export, durable memory, receipt, generated
  projection, test, or validator.
- Remaining decision branches were then exercised in separate fresh disposable
  fixtures. Explicit owner review plus an admitted export contract produced
  exactly one `candidate_only` intake packet and no local candidate or durable
  effect. An absent conventional `memo/PORT.yaml` produced
  `route_only_debt` after one exact not-found check and no alternate search.
  Unsanitized sensitive evidence produced `blocked`, repeated none of the
  credential marker, and created no artifact. Together with the prior
  `needs_owner_review`, `write_candidate`, `no_writeback_needed`, and
  existing-artifact owner handoff trials, this covers every material decision
  and effect class of the output ABI.
- Owner-family result: an existing candidate selected `aoa-memo` directly.
  Owner `recall`, `review`, and requested `evolve` routes loaded contract,
  source return, and one mode in order. Review stopped at `candidate_only`;
  evolve stopped target-first at `needs_owner_review`; exact-ID recall compared
  one corpus object with one generated capsule without broad search.
- Coexistence result: an already named test loaded no AoA skill. A raw `.aoa`
  request selected session-memory routing rather than memo, writeback, or
  harvest. Its stale-index fallback later widened beyond the bounded trial and
  was stopped without changing `.aoa`; that session-memory retrieval behavior
  is not evidence for this skill's quality.
- Runtime-path limit: the exercised Codex model sometimes constructed one
  wrong `.system` path despite an exact host `file:` locator. The final contract
  permits one not-found-only recovery before any workspace action, requires
  `package_path_recovered` in the result, and keeps the extra call visible.
  Repeated probes, search, or hidden recovery remain terminal. Clean package
  entry was also observed, but is not claimed as universal.
- Verdict and limit: mark legacy `aoa-memo-writeback` `manual-evaluated` with
  demonstrated added value while the current bundle remains a candidate
  challenger. The result supports natural positive, progress-only negative,
  all material decision/effect classes, existing-object coexistence,
  named-test negative, and raw-session deflection on this host/model/profile.
  It does not prove cross-model or cross-host parity, general token or latency
  improvement, durable-memory admission, or session-memory retrieval quality.

### 2026-07-17 - Bound exact-ID decision lookup

- Observed defect: in a full-profile coexistence trial, an exact decision
  rationale request selected only `aoa-decision` but still widened through
  repository discovery. It consumed 13 tool calls and 227,423 raw session
  tokens even though the request supplied both the owner root and canonical
  decision ID.
- Correction: `find` now treats that pair as a navigation contract. It reads
  the owner root and decision-lane cards, resolves the exact canonical-ID index
  row, reads only the matched authored record in ascending non-overlapping
  windows, and forbids workspace orientation and repository-wide search.
- Manual result: a fresh neutral-profile trial selected `aoa-decision`, used
  exactly five read-only calls, read the decision record once, returned the
  correct rationale and current applicability, and performed no broad search
  or unrelated source read. Raw session usage was 95,306 tokens.
- Claim limit: this admits the exact-ID `find` route for the exercised wording,
  Codex host, model, and owner layout only. It does not prove general decision
  retrieval, `record`, `correct`, cross-host behavior, or general token and
  latency superiority.

### 2026-07-17 - Close the five-bundle decision migration

- Scope: the manual program exercised all five legacy functions behind the
  consolidated family: root selection, exact-ID `find`, `aoa-adr-write` and
  `aoa-decision-create` through `record`, and source-first
  `aoa-decision-correct`.
- Record result: four-arm fresh-session comparisons covered one complete
  accepted decision, missing material decision inputs, and a local accepted
  choice already preserved by a sufficient reviewed implementation note. The
  final candidate wrote exactly one source record and rebuilt only the declared
  index in the positive case, stopped with an inline incomplete draft and no
  effects when required rationale was absent, and returned
  `no_record_needed` without opening unrelated decision records, indexes,
  builders, Git, or hash inventory when the lighter artifact was sufficient.
- Correct result: separate fixtures covered generated-index-only drift, a
  missing declared builder, and semantic supersession. The final candidate
  left correct authored source byte-identical for derived-only drift, refused
  a manual generated-index patch when the builder was missing, and preserved
  the old record's context and rationale while applying only the owner's
  explicit status and `Superseded by` vocabulary before rebuilding and
  checking the index.
- Find and coexistence result: exact owner root plus canonical ID selected only
  `aoa-decision` both in a neutral profile and among fourteen neighboring AoA
  front doors. It treated the exact index as a locator, grounded every claim in
  the authored record, loaded no knowledge, memo, eval, harvest, recovery, or
  session-memory procedure, and made no changes.
- Corrections from observed behavior: version `0.2.2` replaced broad exact-ID
  discovery with a bounded owner route, stopped Git probing in declared
  non-VCS roots, and made the lighter-artifact negative result terminate
  immediately. The retained `94e5d0e` `aoa-adr-write` body still supplied a
  useful behavioral baseline, but its original package is not directly
  discoverable on Codex `0.144.5` because its frontmatter has `summary` rather
  than the required `description`; procedure comparisons used a temporary
  metadata-only compatibility projection.
- Verdict and limit: mark `aoa-decision`, `aoa-decision-find`,
  `aoa-decision-create`, `aoa-adr-write`, and `aoa-decision-correct`
  `manual-evaluated`. The consolidated package preserves their procedures and
  improves bounded discovery, missing-input discipline, non-VCS effect
  discipline, and current-host package compatibility. Equivalent successful
  outcomes from no-skill or legacy arms prevent any claim of general answer,
  token, latency, cross-model, or cross-host superiority.

### 2026-07-17 - Close reviewed-session harvest and transitional closeout

- Standalone harvest result: `extract` isolated three reusable units from one
  closed reviewed packet, retained rejected and unrelated residue, and stopped
  before classification or owner acceptance. The same explicit promotion
  request against a live unreviewed packet returned
  `blocked_unreviewed_evidence` before loading a mode and changed nothing.
- Automation result: natural full-profile requests selected only
  `aoa-session-harvest`. Four reviewed repetitions of a read-only parity route
  produced a `seed_ready` human-invoked `dry_run_preview` playbook seed while
  rejecting a scheduler and rebuild authority. A one-off incident produced
  `manual_only/not_now`, named every missing readiness condition, and created
  no script, check, schedule, playbook, or owner write.
- Composition result: the transitional
  `aoa-checkpoint-closeout-bridge` executed a closed current-session artifact
  through `harvest.extract`, `harvest.classify`, owner
  `progression.lift`, `harvest.promote`, `harvest.branch`, and
  `closeout.report`. Every node recorded
  `selected -> loaded -> started -> produced -> verified -> completed`, an
  observable procedure load and primary-evidence reread, typed input/output,
  and an actual result. Cross-session and generated hints were rejected; no
  owner, quest, progression, memory, route, KAG, stats, or playbook surface was
  changed. The corresponding live/unreviewed case stopped before downstream
  loading.
- Verdict and limit: mark `aoa-session-donor-harvest`,
  `aoa-quest-harvest`, `aoa-session-route-forks`,
  `aoa-automation-opportunity-scan`, and
  `aoa-checkpoint-closeout-bridge` `manual-evaluated`. The harvest front door
  remains an advertised challenger; the checkpoint front door remains
  transitional only until `aoa-playbooks` exposes a real executable MCP route.
  These trials prove reviewed-session boundaries and actual agent-executed DAG
  nodes, not a generic DAG runtime, destination-owner acceptance, or hidden
  playbook ownership.

### 2026-07-17 - Close session diagnosis and bounded repair

- Diagnose result: no-skill, retained baseline, compressed current, and
  restored candidate all localized repeated `401 missing bearer` evidence to
  the Codex-to-MCP client/auth-forwarding boundary while refusing to blame the
  healthy owner or infer the exact configuration layer. The candidate retained
  symptoms, alternatives, unknowns, likely owners, smallest repair shape,
  proof limit, and the separate-repair stop line.
- Repair result: proposal-only trials distinguished `proposed`, `prepared`,
  `executed`, and `verified` rather than upgrading a plan to an effect. An
  authorized fixture trial captured the pre-state, changed exactly one bearer
  forwarding boolean, passed JSON, focused behavior, neighboring-field, and
  exact-diff checks, and removed the temporary checkpoint. A separate failing
  trial made the same one allowed attempt, observed an independent health
  failure, restored the exact pre-state and digest, verified restored
  behavior, and removed the checkpoint instead of expanding the diff or
  weakening the check.
- Verdict and limit: mark `aoa-session-self-diagnose` and
  `aoa-session-self-repair` `manual-evaluated`. Diagnosis is baseline
  equivalent; repair demonstrates added state/effect/rollback discipline. Keep
  the family degraded and deferred until a natural coexistence case establishes
  retrieval value without neighboring session-route interference.

### 2026-07-17 - Admit natural recovery retrieval after coexistence evidence

- Observed retrieval failure: two fresh natural requests supplied complete
  repeated bearer-failure evidence and correctly excluded Abyss runtime and
  historical-memory work, but the base model answered without loading the
  recovery package. The package itself declared
  `allow_implicit_invocation: false`, so a natural coexistence success was
  impossible regardless of description quality.
- Candidate correction: change only the activation policy from `suggest` to
  `invoke`; keep the reviewed-evidence trigger, procedure, effects, and owner
  boundaries unchanged.
- Manual result: the repeated reviewed incident selected only
  `aoa-session-recovery`, loaded the front door, `diagnose` procedure, and
  contract, and loaded neither the Abyss diagnostic skill nor session-memory
  guidance. It preserved the healthy MCP owner as disconfirming evidence, kept
  the exact client configuration owner unresolved, returned one read-only
  `session-diagnosis`, and left the repair at `proposed` with post-repair
  health `not_run`.
- Negative result: a generic question about one command's non-zero exit loaded
  no AoA skill and caused no tool call.
- Verdict and limit: advertise `aoa-session-recovery` version `0.2.1` as a
  challenger. The result proves natural reviewed-failure retrieval, one
  neighboring Abyss exclusion, one session-memory exclusion, and one generic
  negative on the exercised Codex host/model. It does not prove every incident
  wording, cross-host or cross-model behavior, universal repair bindings, or
  general token and latency superiority.

### 2026-07-17 - Restore progression to its owner home

- Comparison result: no-skill and the retained baseline could describe a
  cautious growth interpretation, while the shared compressed route was
  intercepted by memo writeback. The owner-home
  `aoa-session-progression-lift` required an agent identity, current baseline,
  closed reviewed refs, and attribution limits; returned a typed multi-axis
  delta candidate; separated confirmed, provisional, contested, and
  no-movement axes; and prohibited direct rank, unlock, authority, routing, or
  progression mutation.
- Negative and coexistence result: live self-assessment without agent,
  baseline, closure, review, and refs produced no candidate. In a full profile,
  the natural reviewed-progression request selected the owner skill, resolved
  its source-return handle to the `aoa-agents` package and owner model, and
  changed no owner object.
- Verdict and limit: mark legacy `aoa-session-progression-lift`
  `manual-evaluated` with demonstrated owner-routing and attribution value. Its
  canonical truth belongs in the `aoa-agents` owner package; the prepared
  package remains a candidate until that owner worktree is landed and the
  final OS profile installs its verified projection.

### 2026-07-17 - Restore summon as an owner skill with a real host binding

- Representation correction: the old migration target treated summon as the
  host's generic delegation workflow. That preserved an action label but lost
  the owner procedure that checks the parent anchor, passport, gates, named
  outputs, runtime states, return validation, and closeout handoff. The
  successor is now the same-name `aoa-agents` owner skill; the generic host
  workflow remains a required execute-mode binding rather than skill truth.
- Decision and failure result: the owner package returned `split_required` for
  unsplit `d3+` work and `blocked_binding_unavailable` when a tested execution
  surface did not yield a usable child handle. It did not turn a plan or
  schema-valid packet into a launched child.
- Successful execution result: a separate bounded trial resolved the owner
  source serially, launched exactly one child through the available host
  interface, observed running and completed host states, received exactly the
  two named outputs, validated them against the parent request, and left the
  inspected owner contract byte-identical.
- Authority result: the returned child analysis correctly preserved the
  distinction between procedural guidance and enforcement. The skill can
  require explicit authorization, owner binding, rollback readiness, and
  post-change verification; it cannot itself prove or grant those conditions.
- Verdict and limit: mark legacy `aoa-summon` `manual-evaluated` with
  demonstrated owner-routing, execution-state, and return-validation value.
  This proves one bounded host binding and one truthful binding failure, not
  universal host availability, cross-model behavior, or permission to bypass
  approval, proof, progression, stress, or owner boundaries. The owner package
  remains a candidate until its worktree is landed and the final OS profile
  installs the verified projection.

### 2026-07-15 - User projection declared without widening the catalog

- AOA-SK-D-0040 now owns the user/repository projection split.
- `user-default` adds a user-scoped transport for the already advertised
  `aoa-decision` bundle; it does not promote any of the six deferred bundles.
- Packaging checks now cover every declared profile, while prompt visibility
  and selection remain manual host evidence.

## Boundaries

This decision does not prove that any deferred bundle improves outcomes, make
KAG or a generated graph authoritative, turn an alias into a callable skill,
grant MCP/tool permissions, move workflow ownership into a skill, or allow
session evidence to be committed as owner truth. It does not require every
capability node to become a skill.

## Validation

- Manually inspect the exact 57-entry migration and the nine source procedures.
- Build and validate the capability graph, portable export, Questbook, Agon
  candidate projections, decision indexes, and every declared install profile.
- Exercise positive, negative, coexistence, direct/retrieved, and composed cases
  in clean prompt-visible sessions before any lifecycle promotion.
- Validate the repo-local KAG family through the `aoa-kag` owner generator and
  validator after all authored sources are staged.
- Inspect the final tree and diff for stale paths, session identifiers,
  mandatory technique dependencies, temporary artifacts, and deleted-owner
  scaffolding.
