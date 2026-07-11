# Source-Locked Live Skill Dispatch Evidence

- Decision ID: AOA-SK-D-0037
- Status: Accepted
- Date: 2026-07-11
- Owner surface: `evals/runners/run_live_skill_dispatch.py`,
  `evals/suites/aoa-skill-live-dispatch.plan.json`, and the related schemas

## Index Metadata

- Original date: 2026-07-11
- Surface classes: validation guard, export/runtime, review/governance
- Skill lanes: none
- Mechanic parents: none
- Guard families: evaluation/public surface, export/runtime, release/tooling
- Posture: accepted source-locked live evidence route

## Context

Generated trigger cases, static descriptions, installed-skill counts, and
session mentions do not prove that a current Codex runtime can distinguish,
load, follow, or correctly defer an AoA skill. Raw model transcripts can expose
that pressure, but they are private, costly, runtime-dependent, and too weak to
become proof or promotion authority by themselves.

The repository needs a repeatable live check without turning ordinary CI into a
model benchmark or letting a convenient aggregate score erase dispatch,
manual-policy, trajectory, owner-boundary, and transport failures.

The first complete post-classifier-fix smoke exposed a missing prerequisite in
that check. `codex debug prompt-input` later showed a user-installed `aoa-eval`
skill in the supposed no-skill control and both the repo and user copies in the
aided arm. Some adapters also disabled the read-only shell path needed to prove
full skill reads, while the root and structured prompts did not name an exact
procedure even though the grader expected one. Those observations invalidate
the run as evidence of trigger, trajectory, procedure, or outcome-lift defects;
the receipt is `needs-rerun` harness evidence instead.

The exact-merged-tree v4 rerun exposed the next prerequisite. Prompt inventory
was clean and the aided arm passed objective root and dynamic-child reads, but
the control used the read-only shell to reach an external canonical checkout
and read a complete repo skill before exhausting its cap. Prompt isolation did
not imply filesystem isolation, and budget was downstream of contamination.

## Options Considered

- Infer effectiveness from session mentions, generated trigger fixtures, and
  installed files only.
- Run broad model-backed checks automatically in CI and retain raw transcripts
  with repository reports.
- Keep deterministic harness validation in the normal test lane and require a
  prompt-isolated, source-locked, operator-confirmed, host-routed campaign for
  every live cohort.

## Decision

Choose the third option.

The live harness has four observable arms:

- paired implicit aided and no-skill control turns for dispatch and observed
  outcome lift;
- explicit root-to-child trajectories where accepted `$root` input is native
  root-load evidence and the selected child still needs a complete raw read;
- structured App Server skill input, bound to the exact 57-skill fixture path
  map and the server-issued thread id, with the official paired `$skill` text
  prefix plus matching `skill` item and no configured MCP startup before the
  turn;
- deterministic harness tests that validate all schemas, cohort expansion,
  adapters, privacy projection, and stop-lines without making model calls.

Before any arm spends a model turn, run `codex debug prompt-input` with the
same fixture, disabled features, and external-skill overrides as the live
adapter. The aided fixture must expose exactly the portable repo skills whose
policy declares `allow_implicit_invocation: true` (12 of 57 in the current
profile). The no-skill control must expose zero repo skills. The paired non-repo
background inventory digests must match. A background entry fingerprint binds
its model-visible name, resolved path, and description, so description drift is
part of the treatment contract. Any mismatch is `harness_contamination` and
stops before the model turn. Structured App Server arms additionally require
`skills/list` to equal the exact enabled fixture-path map for all 57 repo skills
before `turn/start`.

Live execution defaults to `plan`, binds model, effort, Git head, all portable
skill files, generated/config inputs, profile revision, Codex protocol revision,
caps, trial identities, and the count plus digest of the discovered external
shadow-skill set into exact confirmation tokens, and requires a second token
for every cohort beyond smoke. The exact external `SKILL.md` paths stay private,
are rediscovered before execution, and are disabled in every CLI, App Server,
and prompt-inspection adapter. User-skill symlinks are resolved and their
canonical target files are the locked and disabled identities. Plugin features
are disabled independently. The configured MCP-name inventory has its own
count/digest lock. CLI exec arms use `--ignore-user-config` and must not
synthesize partial MCP tables; prompt inspection and App Server retain user
config and explicitly disable every locked id. A shadow or MCP count/digest
change is source/runtime drift, not a reason to reuse the old token.

The corrected hermetic pre-turn and evidence contract uses schema
`aoa_codex_app_server_skill_input_contract_v5` and protocol revision
`codex-cli-0.144.1-live-dispatch-evidence-v5`. It follows the
[official App Server invocation shape](https://learn.chatgpt.com/docs/app-server#start-a-turn-invoke-a-skill)
and Codex [progressive-disclosure load semantics](https://learn.chatgpt.com/docs/customization/overview#skills).
Retained receipts source-locked to v1-v4 keep their original protocol and
review status and are not upgraded in place.

The source-locked caps include both the rollout token limit and its required
list of remaining-token reminder thresholds. Every CLI and App Server arm must
pass both values explicitly under strict config so an installed Codex contract
change fails in deterministic adapter tests or pre-turn smoke, not midway
through a campaign.

All arms use a 48k weighted-token cap. Root-child trajectories first established
that floor because proving a full child read exhausted the former 28k cap. The
corrected matched control then selected the source-locked ambient session-memory
route and its required owner reads also exceeded 28k. Giving both implicit arms
the same 48k ceiling preserves treatment/control symmetry without deleting a
real background route. A cap stop without a valid result is classified as
`budget_exhausted`, not generic transport failure. A late budget event after a
zero-return, contract-valid model output cannot override that usable result; the
normal semantic classifier still decides its failure class. Any further
increase requires reviewed cap/context evidence and a same-case rerun.

Planning also validates the model-output schema against the bounded Responses
API strict-output contract before issuing a confirmation token. Draft 2020-12
validity alone is insufficient because a locally valid `const` or `enum`
without an explicit type is rejected by the runtime API.

The run must execute inside `abyss-machine resource launch`; the runner verifies
the resource class, agent kind, and cgroup, independently requires a storage
write preflight for its private host-owned root, and stops on runtime drift,
privacy contamination, owner-boundary widening, or transport failure. The
sandbox remains read-only and network-disabled, while read-only shell execution
is available for evidence-bearing skill reads and one hermetic fixture
procedure. Read-only skill-file inspection commands are evidence collection,
remain allowed before the procedure, and do not count as procedure commands.
Every completed or in-progress model command must remain inside the fixture
root. Absolute host, workspace, session-memory, user-config, other-repository,
or parent-traversal paths are `harness_contamination` before budget, dispatch,
load, procedure, or lift interpretation. System executables and `/dev/null`
remain tooling exceptions and do not widen the data boundary.
Root/child and structured arms receive the exact procedure command
`python3 fixture_validator.py`. Transport records full reads, exact command
observation, zero exit, and `AOA_FIXTURE_VALIDATOR_OK` verification as separate
measures.
A full read must name the exact fixture `SKILL.md` path and contain its complete
source. An expected or dynamically selected child must have that full read
before the load contract passes. The model's `claims_loaded` field remains a
self-report and never gates objective load. Accepted native input is recorded
separately and never relabeled as a raw read. Procedure verification is atomic:
one completed exact-command event
must carry both zero exit and exactly one sentinel JSON payload matching the
fixture-guidance digest, schema/status, no-drift, and no-proof-authority fields.
Split or forged evidence does not pass.
An explicit `true` mutation, proof-authority, or promotion claim is classified
as an owner-boundary safety violation before generic output invalidity, even
though the strict response schema also forbids that value.

Raw prompts, events, transport identifiers, and model output remain in `0600`
files below the source-locked `0700` host-private root. Public receipts are
field-whitelisted projections with digests, per-arm observations, paired deltas,
failure classes, and review status. Measures distinguish prompt visibility,
selection, model load claim, accepted native input, raw full-read evidence,
dispatch and load contracts, procedure disposition, execution, verification,
completion, and deflection. They publish no raw text and no aggregate score.
Public safety validation walks every string and rejects an absolute host path
even when it is embedded inside a longer prose value.

`skill_load_gap` is the bounded return route when the exact target was selected
but required native-load or child/full-read evidence was not observed. It
returns to native-load/full-read tooling or skill behavior for the same case
rather than mislabeling the result as a trigger, trajectory, or procedure
defect.

`dispatch_policy_gap` is distinct: the route was available, but the activation
decision violated the expected implicit, manual, trajectory, or explicit
dispatch policy. It returns to dispatch policy, not read tooling.

## Rationale

This route measures different evidence stages without collapsing them. A skill
surface being prompt-visible is not the same as being selected; selection is
not accepted native input; a model load claim is neither native acceptance nor
a complete transport-observed raw read; a read is not procedure execution; an
exit code is not sentinel verification;
and a route-contract match is neither observed completion nor central proof.

Source locks make a rerun comparable. Exact shadow disabling, pre-turn
inventory checks, and command-level fixture-scope evidence make the
aided/control difference attributable to the fixture instead of an installed
user copy or a source checkout reached through the read-only filesystem. Paired background digests expose other
prompt-surface drift rather than crediting general model knowledge. Host routing
bounds resource and storage pressure. Private/raw and public/digest separation
keeps review possible without publishing session material.
Paired lift is undefined and omitted when either arm has an output-contract,
transport, budget, runtime-profile, or owner-boundary safety failure. A
zero-return invalid structured result is `output_contract_invalid`; transport
failure is reserved for failed or timed-out transport. A contaminated pair
remains
visible without rewriting the original failure classification of either arm.
Collision neighbourhoods are contextual candidates rather than adversarial
truth: selecting the expected target is never a collision merely because the
target also appears in its own neighbourhood list.

## Consequences

- Positive: dispatch, manual reachability, structured selection, trajectory,
  and paired outcome-lift pressure can be reproduced against an exact source and
  runtime protocol.
- Positive: harness contamination is rejected before model spend, and public
  evidence can locate a gap at visibility, dispatch, load, procedure,
  verification, completion, or deflection instead of collapsing stages.
- Positive: source locks and transport-appropriate per-adapter isolation cover
  canonical user-skill shadows, plugins, and configured MCP ids; structured
  turns prove a unique 57-skill surface and zero MCP startup before model spend.
- Positive: fixture-scope grading rejects filesystem treatment leakage even
  when prompt visibility is clean and a later budget marker would otherwise
  hide the earlier contamination.
- Positive: failures carry bounded adaptive return routes instead of one score.
- Positive: ordinary CI proves the harness contract without spending model
  turns or treating model quality as deterministic repository proof.
- Tradeoff: Codex App Server upgrades require an explicit protocol-contract and
  source-lock refresh before live use.
- Tradeoff: single cohort observations remain candidate evidence; review and
  repeated runs are needed before changing skill status or promotion posture.
- Tradeoff: the 48k ceiling raises worst-case live-campaign cost; non-smoke
  cohorts therefore retain the second exact high-cost confirmation token.
- Follow-up: v4 repaired claim/read/output grading, but its exact-merged-tree
  rerun exposed an external source read in the control. Land the v5
  fixture-scope gate and repeat the exact smoke before any pilot widening, then
  use reviewed pilot receipts to continue toward all 57 skills.

## Current Applicability

As of 2026-07-11:

- Still valid: central verdict, scoring, regression, proof doctrine, and proof
  acceptance remain in `aoa-evals`.
- Still valid: `.aoa` raw session episodes remain reviewed candidate evidence,
  not automatic proof of skill use or success.
- Changed: the complete post-classifier smoke is `needs-rerun` because its
  prompt-visible control was contaminated and its read/procedure grader was not
  executable and unambiguous across adapters.
- Current visibility contract: aided fixtures expose exactly the 12 of 57 repo
  skills marked `allow_implicit_invocation: true`; controls expose zero repo
  skills, and paired background description fingerprints match. Structured
  arms expose exactly one fixture path for every one of the 57 repo skills and
  no configured MCP startup before the turn.
- Current filesystem contract: model commands may read only inside the fixture;
  external absolute or parent-traversal access is contamination before budget
  or any skill-effect interpretation.
- Current cap contract: every arm receives the same source-locked 48k ceiling;
  paired arms may differ in actual use but never in available budget.
- Current contract schema: `aoa_codex_app_server_skill_input_contract_v5`.
- Current protocol lock: `codex-cli-0.144.1-live-dispatch-evidence-v5`.
- Historical protocols: retained v1-v2 smokes are `needs-rerun`; v2 produced a
  valid candidate implicit pair but used an unsupported structured-only App
  input and cannot support its App load label. Retained v3-v4 reports keep their
  original review status and old grader semantics.
- Reviewed v3 candidate: the implicit pair records positive lift and the App
  arm passes its native-load/procedure path, while the explicit `aoa-eval`
  trajectory selects `aoa-eval-apply` without a complete child read. That
  observation supports a bounded root-handoff repair and same-case rerun, not
  central proof, status promotion, or a family-wide verdict.
- Current rerun posture: the first exact-merged-tree v3 rerun after that repair
  is `needs-rerun`. It exposed self-report load gating, a missing
  dynamic-child read check, read/procedure ambiguity, and
  output-contract/transport conflation. It supports no pair, lift,
  skill-effect, or family conclusion.
- Current rerun posture: the exact-merged-tree v4 smoke is also `needs-rerun`.
  Its aided arm passed objective root and dynamic-child reads, but the control
  read a complete repo skill from an external canonical checkout before budget
  exhaustion. V4 preserved the budget label; raw review routes the earlier
  fault to harness contamination. V5 smoke must pass before pilot widening.
- Superseded by: none.

## Review Log

### 2026-07-11 - Grade fixture filesystem scope before budget or skill effect

- Previous assumption: prompt-visible skill isolation plus exact fixture-path
  load checks made the aided/control treatment boundary sufficient; a later
  budget stop could therefore be interpreted as cap pressure.
- New evidence: the exact merged v4 run kept prompt visibility clean and its
  aided arm passed objective root and dynamic-child reads. The control then
  traversed ambient session-memory owner files and read a complete `aoa-eval`
  source from an external canonical checkout before the 48k stop. The old
  grader reported `budget_exhausted`, hiding the earlier treatment leakage.
- Decision: confine every model command to the fixture root, publish
  `fixture_filesystem_scope_match`, and classify observed absolute external or
  parent-traversal access as `harness_contamination` before budget, dispatch,
  load, procedure, pair, or lift interpretation. System executables and
  `/dev/null` remain tooling exceptions.
- Boundary: the v4 public receipt remains immutable under its historical budget
  label. Reviewed private events justify a harness repair only; they support no
  pair, lift, skill-effect, status, promotion, or family conclusion.
- Tradeoff: the bounded fixture no longer measures unrestricted ambient owner
  traversal in the causal smoke. Ecological background-route behavior can be a
  separate reviewed cohort only after the causal fixture is sound.
- Validation: replay the raw v4 events through the new detector, preserve
  fixture-local chained skill reads, reject absolute and parent escapes, prove
  contamination outranks budget, then land v5 and repeat the exact merged smoke.

### 2026-07-11 - Separate objective load evidence from self-report and procedure commands

- Previous assumption: `claims_loaded` could safely participate in the load
  gate, the statically expected child was sufficient for read checking, and
  naming one exact procedure command made read-only inspection unambiguous.
- New evidence: the exact merged root-handoff rerun selected `aoa-eval` and
  `aoa-eval-apply` but skipped the child read after interpreting the fixture as
  a one-command constraint. The implicit route could select a dynamic child
  that the grader did not bind to a read. A zero-return invalid final result was
  also reported as transport failure.
- Decision: derive objective load only from accepted native input and complete
  exact-path reads; bind both expected and dynamically selected children;
  preserve `claims_loaded` only as a separate model self-report; explicitly
  allow read-only inspection before the one procedure command; and classify
  zero-return schema failure as `output_contract_invalid`.
- Boundary: the v3 rerun is immutable `needs-rerun` harness evidence. It drives
  no pair, lift, skill-effect, status, promotion, or family conclusion.
- Tradeoff: explicit inspection may add read commands and context, but only the
  selected child is loaded and the procedure remains exactly one command.
- Validation: deterministic tests must prove the claim/evidence split, dynamic
  child binding, command boundary, output taxonomy, and pair omission; then
  land v4 and repeat the exact merged smoke before pilot widening.

### 2026-07-11 - Return a valid child-load gap to the root workflow

- Previous assumption: telling the router to load exactly one selected subskill
  was sufficient to distinguish selection from loading while controlling
  context.
- New evidence: the source-locked v3 smoke natively loaded `aoa-eval`, selected
  the expected `aoa-eval-apply` child, ran and verified the fixture procedure,
  but produced no complete read of the child `SKILL.md`. The official App arm
  passed under the same protocol, so the missing read is no longer explained by
  the v2 harness defect.
- Decision: keep the trigger and invocation policy unchanged; require the root
  router to read the selected child's complete `SKILL.md` before applying or
  claiming its procedure, and state that a selected child name is selection
  evidence only.
- Boundary: the reviewed receipt is evidence context, not decision or proof
  authority. The source skill owns the workflow repair; `aoa-evals` retains
  central verdict, scoring, regression, and proof doctrine.
- Tradeoff: the explicit handoff adds a small amount of context and may increase
  a root trajectory's token use, but still loads one child rather than the whole
  family.
- Validation: add a focused source regression, rebuild generated/export
  companions through their owner builders, and repeat the exact v3 smoke before
  pilot widening.

### 2026-07-11 - Align native-load evidence with the official Codex contract

- Previous assumption: a structured App Server `skill` item without textual
  activation could isolate causality, and every loaded skill needed a separate
  shell full-read event.
- New reality: official Codex documentation defines App invocation as the pair
  of `$skill` text plus a matching `skill` item and says `SKILL.md` loads when a
  skill is chosen. The completed v2 smoke therefore contains a valid candidate
  implicit pair, a candidate missing-child-read trajectory, and an invalid App
  load interpretation.
- Reason: native input acceptance and raw shell reads are different evidence
  kinds. Collapsing them created a false App `skill_load_gap` while hiding the
  real question of whether the selected child was loaded.
- Validation: bump to v3, assert the official dual input, publish native input
  acceptance separately from full-read observation, retain v2 as
  `needs-rerun`, and repeat smoke before any skill edit or pilot widening.

### 2026-07-11 - Preserve matched-pair symmetry across an ambient route

- Previous assumption: 28k was sufficient for implicit and structured arms
  after root-child trajectories received a separate 48k cap.
- New reality: once shadow isolation became correct, the no-repo-skill control
  legitimately selected the equal-background session-memory route and read
  68,295 characters of required owner material before the 28k budget stopped
  it. The aided arm read 15,095 characters and completed.
- Reason: deleting the ambient route would weaken ecological validity, while
  raising only the control cap would invalidate paired lift. Both implicit arms
  therefore receive the same 48k ceiling, shared with the other live arms.
- Validation: source-lock the cap, assert equal aided/control argv, retain the
  stopped receipt as `needs-rerun`, and repeat the exact smoke before pilot.

### 2026-07-11 - Correct CLI MCP isolation without weakening App gates

- Previous assumption: every configured MCP id could receive the same
  `enabled=false` override in every adapter.
- New reality: CLI exec already removes all user MCP tables with
  `--ignore-user-config`; adding name-only overrides reconstructs incomplete
  tables without transports and fails before model spend. Prompt inspection and
  App Server still need explicit per-id disables because they retain user
  config.
- Reason: the first protocol-v2 smoke passed its 12/12 prompt gate but stopped
  on `invalid transport` before a model turn, so it contains adapter evidence
  only and requires a rerun.
- Validation: deterministic argv tests must prove absence of MCP-table
  overrides on CLI exec and their presence on prompt inspection and App Server,
  followed by a source-locked smoke before any pilot widening.

### 2026-07-11 - Correct prompt isolation and evidence-stage grading

- Previous assumption: fixture absence plus `--ignore-user-config` made a
  no-skill control, and route output alone could support trajectory/procedure
  classification while read-only shell execution was disabled in some arms.
- New reality: model-visible prompt inspection found an installed user shadow
  in the control and a duplicate in the aided arm; full reads and a selected
  procedure also lacked a uniform executable evidence path.
- Reason: the complete smoke labels could otherwise be mistaken for skill
  defects even though the harness did not isolate or prove their prerequisites.
- Source surfaces updated: live runner, plan and receipt contracts, suite note,
  runner/report guidance, and this clarification of `AOA-SK-D-0037`.
- Validation: deterministic tests must prove exact-path disabling, source-lock
  drift, canonical symlink shadow handling, plugin and configured-MCP
  isolation, pre-turn contamination stop, the complete structured 57-skill
  map, zero MCP startup, exact fixture-path full reads, atomic exact command,
  zero exit plus guidance-bound sentinel verification, non-scored invalid
  pairs, arm-history preservation, embedded-path privacy, public projection,
  and legacy receipt review before a corrected smoke is interpreted.

## Boundaries

This decision does not make `aoa-skills` a central model-evaluation owner. It
does not allow automatic skill promotion, public raw transcripts, unattended
high-cost cohorts, or execution of repository mutation tasks. A green route
receipt proves only the evidence dimensions it explicitly records and does not
prove completion outside the bounded fixture. A `needs-rerun` receipt or a run
with prompt/background contamination must not drive skill edits, promotion, or
outcome-lift claims.

## Validation

- `python -m pytest -q tests/test_live_skill_dispatch_harness.py`
- `python scripts/lanes/ci_gate.py --mode source-fast`
- local eval-port validation through the current `aoa-evals` owner
- decision-index regeneration and parity check
- exact `codex --version`, App Server schema contract, resource-wrapper cgroup,
  storage preflight, shadow-set lock, and `codex debug prompt-input` inventory
  checks before a live turn
- corrected smoke review before any pilot widening or skill-defect claim
