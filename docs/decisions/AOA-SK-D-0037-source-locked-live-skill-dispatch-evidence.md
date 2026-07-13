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

The exact-merged-tree v8 rerun exposed a semantic prerequisite in the outcome
answer key itself. Its constrained model-output contract defines
`procedure_disposition` for the downstream skill procedure, and the fixture
names that procedure exactly. The pre-authored v8 key nevertheless expected
deflection of the larger unavailable repository task. The observed negative
outcome therefore returned to contract scope review rather than authorizing a
skill edit.

The exact-merged-tree v9 rerun exposed the deeper boundary. The aided arm chose
`aoa-eval-select`, not `aoa-eval-apply`, because the case asks to inspect
existing eval surfaces before applying one and supplies no target repository.
It correctly reported `blocked_missing_input` while independently running the
fixture validator. The structured arm accepted official `aoa-eval-apply` input
but reported the equivalent `aoa-eval` root-to-child hierarchy. V9 had confused
the fixture probe with the child procedure and model selection report with
transport-native dispatch.

The exact-merged v10 attempts exposed a separate breadth prerequisite. The
first aided arm broadly enumerated the hidden fixture and exhausted 48k before
final output. An unchanged repeat completed the implicit pair, then the root
trajectory broadly listed and hashed the fixture tree before the same cap stop.
Both runs stayed inside the filesystem boundary, but exact-path read evidence
had become mixed with unnecessary full-tree archaeology. A path-safe command
is therefore not automatically a scope-bounded command.

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

- paired implicit aided and no-skill control turns that report route,
  selected-child trajectory, and selected-procedure-disposition report lift as
  separate dimensions while leaving objective outcome unscored when the fixture
  exposes none;
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
`aoa_codex_app_server_skill_input_contract_v11` and protocol revision
`codex-cli-0.144.1-live-dispatch-evidence-v14`. It follows the
[official App Server invocation shape](https://learn.chatgpt.com/docs/app-server#start-a-turn-invoke-a-skill)
and Codex [progressive-disclosure load semantics](https://learn.chatgpt.com/docs/customization/overview#skills).
Retained receipts source-locked to v1-v10 keep their original protocol and
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
is available for evidence-bearing skill reads and one independent hermetic
fixture-execution probe. Read-only skill-file inspection commands are load and
trajectory evidence, not the probe or selected skill procedure.
Every completed or in-progress model command must remain inside the fixture
root. Absolute host, workspace, session-memory, user-config, other-repository,
or parent-traversal paths are `harness_contamination` before budget, dispatch,
load, procedure, or lift interpretation. System executables and `/dev/null`
remain tooling exceptions and do not widen the data boundary.
Inside that root, commands must also avoid broad enumeration, recursive
listing, and tree hashing. Exact reads of fixture guidance, the selected root
or target skill, at most one selected child, and the named validator remain
allowed. A completed or in-progress broad inventory command is
`fixture_inventory_scope_violation` before budget or skill interpretation.
Every arm receives the exact fixture probe
`python3 fixture_validator.py`. Transport records full reads, exact command
observation, zero exit, and `AOA_FIXTURE_VALIDATOR_OK` verification as separate
measures.
A full read must come from successful transport events that name the exact
fixture `SKILL.md` path. One output may contain the whole source, or ordered
outputs may continuously cover it; overlaps are allowed, unrelated outputs are
ignored, and gaps or reverse-only coverage remain incomplete. An expected or
dynamically selected child must have that full read before the load contract
passes. The model's `claims_loaded` field remains a self-report and never gates
objective load. Accepted native input is recorded separately and never
relabeled as a raw read. Procedure verification remains atomic: one completed
exact-command event
must carry both zero exit and exactly one sentinel JSON payload matching the
fixture-guidance digest, schema/status, no-drift, and no-proof-authority fields.
Split or forged evidence does not pass. Probe success does not determine the
selected child procedure disposition or whole-task outcome.
A separate source-locked owner-action contract may add exactly one bounded
candidate choice through `python3 outcome_validator.py --candidate <value>`.
The answer is not present in the plan lock. One atomic zero-exit sentinel event
is observable outcome evidence; reading, copying, hashing, importing,
reproducing, or retrying the validator contaminates the measurement. A wrong
single choice is a negative outcome, not a procedure or transport failure.
An explicit `true` mutation, proof-authority, or promotion claim is classified
as an owner-boundary safety violation before generic output invalidity, even
though the strict response schema also forbids that value.

Raw prompts, events, transport identifiers, and model output remain in `0600`
files below the source-locked `0700` host-private root. Public receipts are
field-whitelisted projections with digests, per-arm observations, paired deltas,
failure classes, and review status. Measures distinguish prompt visibility,
model selection report, sent structured dispatch, accepted native input, raw
full-read evidence, dispatch/load contracts, selected-child trajectory,
fixture execution, selected-procedure disposition/completion/deflection report,
and objective-outcome availability. They publish no raw text and no aggregate
score.
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

Transport exceptions preserve their observed elapsed duration and partial
private stdout/stderr. Recoverable JSONL events and usage retain their normal
turn-start, budget, filesystem-scope, and failure-precedence meaning. Once the
private receipt is safely written, an incomplete `stopped_early` cohort reports its
bounded stop reason and returns process exit 1. A complete cohort returns exit
0 even when it records negative skill behavior: shell status describes whether
the planned measurement completed, not whether the model passed the case.

## Rationale

This route measures different evidence stages without collapsing them. A skill
surface being prompt-visible is not the same as being selected; selection is
not transport dispatch; sent structured input is not accepted native load; a
model load claim is neither native acceptance nor a complete
transport-observed raw read; a child read is not its procedure disposition; the
fixture probe is neither the child procedure nor an objective task outcome; and
a route-contract match is not completion or central proof.

Source locks make a rerun comparable. Exact shadow disabling, pre-turn
inventory checks, and command-level fixture-scope evidence make the
aided/control difference attributable to the fixture instead of an installed
user copy or a source checkout reached through the read-only filesystem. Paired
background digests expose other prompt-surface drift rather than crediting
general model knowledge. Host routing bounds resource and storage pressure.
Private/raw and public/digest separation keeps review possible without
publishing session material. Paired route, trajectory, and procedure-
disposition report lift are
undefined and omitted when either arm has an output-contract, transport,
budget, runtime-profile, or owner-boundary safety failure. Objective outcome is
unscored when no separate contract exists; when the source declares a bounded
owner-action contract, only its atomic transport observation may be scored. A
zero-return invalid structured result is `output_contract_invalid`; transport
failure is reserved for failed or timed-out transport. A contaminated pair
remains visible without rewriting the original failure classification of
either arm.
Collision neighbourhoods are contextual candidates rather than adversarial
truth: selecting the expected target is never a collision merely because the
target also appears in its own neighbourhood list.

## Consequences

- Positive: dispatch, manual reachability, structured selection, route lift,
  selected-child trajectory, fixture execution, and procedure-disposition
  pressure can be
  reproduced against an exact source and runtime protocol without one lift
  masquerading as the other.
- Positive: harness contamination is rejected before model spend, and public
  evidence can locate a gap at visibility, dispatch, load, procedure,
  verification, completion, or deflection instead of collapsing stages.
- Positive: source locks and transport-appropriate per-adapter isolation cover
  canonical user-skill shadows, plugins, and configured MCP ids; structured
  turns prove a unique 57-skill surface and zero MCP startup before model spend.
- Positive: fixture-scope grading rejects filesystem treatment leakage even
  when prompt visibility is clean and a later budget marker would otherwise
  hide the earlier contamination.
- Positive: inventory-scope grading rejects path-safe but causally unbounded
  full-tree archaeology before a later budget marker can turn it into a cap
  problem or apparent skill defect.
- Positive: complete source exposure can be proven across ordinary bounded
  chunk reads without accepting inventory mentions, unrelated metadata, gaps,
  reverse-only coverage, or same-name shadow paths.
- Positive: host orchestration can distinguish a complete negative cohort from
  an incomplete transport or safety stop, and timeout duration no longer
  collapses to zero.
- Positive: failures carry bounded adaptive return routes instead of one score.
- Positive: ordinary CI proves the harness contract without spending model
  turns or treating model quality as deterministic repository proof.
- Tradeoff: Codex App Server upgrades require an explicit protocol-contract and
  source-lock refresh before live use.
- Tradeoff: single cohort observations remain candidate evidence; review and
  repeated runs are needed before changing skill status or promotion posture.
- Tradeoff: the 48k ceiling raises worst-case live-campaign cost; non-smoke
  cohorts therefore retain the second exact high-cost confirmation token.
- Follow-up: preserve the first full pilot, correct its harness and contract
  returns, isolate the manual-policy skill candidates with bounded reruns, and
  repeat the guarded pilot before widening toward all 57 skills.

## Current Applicability

As of 2026-07-12:

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
- Current inventory contract: commands may use exact route-required files but
  may not enumerate, recursively list, or hash the fixture tree;
  `fixture_inventory_scope_violation` precedes budget classification.
- Current cap contract: every arm receives the same source-locked 48k ceiling;
  paired arms may differ in actual use but never in available budget.
- Current contract schema: `aoa_codex_app_server_skill_input_contract_v12`.
- Current protocol lock: `codex-cli-0.144.1-live-dispatch-evidence-v17`.
- Current pair contract: new receipts publish route, selected-child trajectory,
  and selected-procedure-disposition report lift separately. Sent structured
  dispatch, accepted native load, model hierarchy report, and fixture execution
  remain independent measures. Objective outcome is
  `not_scored_no_observable_outcome` without a source contract; the v12 corpus
  separately observes one bounded next owner action for every implicit pilot
  case.
- Historical protocols: retained v1-v2 smokes are `needs-rerun`; v2 produced a
  valid candidate implicit pair but used an unsupported structured-only App
  input and cannot support its App load label. Retained v3-v6 reports keep their
  original review status and old grader semantics. The reviewed v7 report also
  keeps its historical generic route-derived lift rather than being rewritten.
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
  fault to harness contamination.
- Current rerun posture: the exact-merged-tree v5 smoke is also `needs-rerun`.
  It kept prompt and filesystem scope clean and completed all four arms, but its
  aided target read was split across two ordered exact-path outputs. The v5
  single-output detector recorded a false `skill_load_gap` and no-lift result;
  its historical fields remain immutable. V6 smoke was required before pilot
  widening and is now retained separately below.
- Current rerun posture: the exact-merged-tree v6 smoke is also `needs-rerun`.
  It passed prompt visibility and fixture scope, then the first CLI transport
  timed out at 180 seconds before any turn event, output, usage, or pair. Its
  private receipt stopped early, but the v6 command returned zero and the host
  wrapper reported success. The old zero duration and process status remain
  immutable; v7 was required to rerun after runtime availability.
- Reviewed v7 candidate: the exact-merged smoke completed four of four arms,
  passed prompt/background, fixture, load, procedure, and safety gates, and
  recorded generic `observed_lift=1`. Code and raw review show that v7 derived
  this field solely from route-contract correctness. It is therefore positive
  route evidence, not completion or outcome lift.
- Current rerun posture: the exact-merged v8 smoke completed all four turns and
  recorded positive route lift plus negative outcome lift under its immutable
  source lock. Review found that its answer key incorrectly graded deflection
  of the larger unavailable repository task rather than completion of the exact
  downstream fixture procedure declared by the model-output contract. Its
  public receipt is `needs-rerun` harness evidence, not a negative skill
  outcome. V9's attempted correction is superseded by the next item.
- Current rerun posture: the exact-merged v9 smoke completed all four turns.
  Its aided arm selected the source-correct `aoa-eval-select` child and blocked
  on missing target-repository evidence; its structured arm accepted official
  `aoa-eval-apply` input but reported the equivalent root-child hierarchy. V10
  replay yields route `+1`, trajectory `+1`, procedure-disposition `0` with
  both reports correct, and no objective outcome score. The public v9 receipt
  remains immutable `needs-rerun` harness evidence. V10 is retained below.
- Current rerun posture: the first exact-merged v10 attempt stopped the aided
  arm on budget exhaustion after broad hidden fixture enumeration and before
  final output or pair construction. The unchanged repeat completed the
  implicit pair with candidate positive route lift, zero trajectory lift, and
  correct procedure disposition, then stopped the root trajectory after broad
  listing and tree hashing. Both public receipts are immutable `needs-rerun`
  harness evidence. Their former requirement for a fresh v11 rerun is satisfied
  by the next item; the inventory-pressured `aoa-eval-local-need` observation
  does not pressure a skill or contract.
- Reviewed v11 smoke: exact-merged v11 completed all four arms with no
  failures, external reads, or broad inventory commands. The aided arm selected
  `aoa-eval`, fully read the source-correct `aoa-eval-select` child, and
  reported `blocked_missing_input`; the control had no skill surface and did
  not select either route. The pair therefore records route `+1`, trajectory
  `+1`, procedure-disposition `0` with both reports correct, and objective
  outcome unscored. The direct root-to-`aoa-eval-apply` and official structured
  `aoa-eval-apply` arms also matched their dispatch, load, probe, and boundary
  contracts. This is reviewed candidate evidence, not a family verdict or
  promotion signal. At that source head, pilot planning exposed 1/11 procedure
  contracts and 0/11 objective outcomes; confirmed execution was blocked
  before preflight until both reached 11/11.
- Current adaptive return: comparing the successful v11 route with the accepted
  `aoa-evals` local-suite execution contract found a procedure gap in the skill
  source. `aoa-eval` must distinguish live-workspace readiness from exact-source
  evidence; `aoa-eval-apply` must JIT-revalidate a selected sidecar with the
  owner validator, execute only its typed invocation, capture environment
  posture, and write a private source-linked receipt. Readiness and MCP remain
  inspect-only, `source-contract-ready` is not runtime reproducibility, and the
  change requires a fresh exact-merged smoke before pilot widening.
- Current reviewed return: that exact-merged post-alignment smoke completed all
  four arms with clean harness evidence and route lift `+1`, but the aided root
  selected `aoa-eval-local-need` while target-repository fit was still unknown.
  The required child was `aoa-eval-select`; trajectory lift is `0` with both
  arms incorrect, procedure disposition is correct in both arms, and outcome is
  unscored. Missing evidence must not become a no-fit conclusion. Preserve the
  receipt and harden selection precedence before the next exact smoke.
- Reviewed repaired v11 rerun: exact-merged v11 after the fail-closed precedence
  change completed four of four arms with no failure class. The aided root
  selected and fully read `aoa-eval-select`; route and trajectory lift are each
  `+1`, both procedure dispositions are correct, outcome remains unscored, and
  all isolation/fixture gates pass. This closes the precedence return as
  candidate evidence; at that source head pilot coverage remained 1/11
  procedures and 0/11 outcomes.
- Reviewed v12 seam posture: deterministic validation covered 1/11 procedure
  contracts and 1/11 owner-observable outcomes. The exact-merged v12 smoke
  validated one-attempt observability with both arms correct and no
  contamination, authorizing source review of the other ten cases.
- Current pilot contract posture: all 11 implicit pairs have source-locked
  procedure contracts and separate owner-observable outcome contracts.
  Deterministic planning reports 11/11 on both required axes.
- Current pilot evidence: the first exact-merged 30-turn run completed with all
  prompt, transport, filesystem, inventory, fixture, owner-action, and
  authority gates clean. All 11 outcome pairs were correct in both arms. The
  reviewed receipt is `needs-rerun`, not a negative family verdict, because it
  contains both manual-policy skill collision candidates and distinct
  harness/contract return routes that must be corrected first.
- Current v13 replay posture: source reread retains `collision-38` as a real
  root-child handoff candidate. Aided-only manual failure classification,
  explicit no-dispatch disposition guidance, and one source-declared
  target-to-base-child structured hierarchy remove three control-side labels
  and the Abyss selection-report miss from read-only replay. The immutable v12
  receipt is not rewritten; a fresh bounded rerun is still required.
- Current bounded-rerun posture: `pilot13-returns` contains the seven affected
  implicit pairs and the corrected Abyss structured-report case, exactly 15
  turns. It requires both source contract axes and a second high-cost token,
  while omitting already-clean pilot and unaffected trajectory arms.
- Current bounded-rerun evidence: the first exact-merged attempt stopped at
  6/15 on a post-start transport timeout. A fresh attempt passed that point and
  stopped at 14/15 on an output contradiction. Both receipts are preserved as
  `needs-rerun` historical evidence.
- Current v14 posture: selected reports are classified against the exact
  prompt-visible repo surface; external ambient routes do not become treatment
  activation. Target-specific report guidance now reaches implicit arms.
  The fresh exact-merged run completes 15/15 with every harness, transport,
  owner, safety, and final structured-arm boundary clean. It leaves exactly
  three aided source candidates. The first six-turn source-return execution
  closes the approval-gate collision and confirms the `aoa-decision-find`
  handoff. After the second source repair and runtime refresh, the exact rerun
  has no aided failure class and closes the child disposition plus concrete
  ATM10 collision. V15 now exposes recurring missing sentinel bytes as per-arm
  and pair-level observation-gap telemetry, while keeping affected outcomes
  unverified. The exact v15 full pilot completes 30/30 with zero failure classes;
  five route/procedure pairs and two child trajectories improve, while four
  outcome contrasts remain observation-unclean. V16 now partitions both broad
  parents into eleven disjoint, exact-cover waves and fail-closes each implicit
  wave on missing contracts; the 16-turn core-engineering wave is the first
  contract-complete widening. Its first exact run completes every arm and gives
  all eight aided pairs route/procedure lift, but three zero-output fixture
  probes require the smallest paired `collision-01`/`collision-02` return. That
  exact four-turn return is now clean and confirms an observation-layer gap,
  not a skill defect. The remaining unclean evidence is limited to opposite
  single-arm owner-action gaps in `collision-05` and `collision-06`; the second
  exact four-turn paired return is also clean. Together the returns close every
  outstanding core-wave observation gap without changing skill source or
  evidence rules. The safety-overlay wave was next and remained fail-closed on
  incomplete source-authored contracts until its complete source pass closed
  that design gate at 11/11 procedure and 11/11 owner-action pairs, with six
  new skill refs entering the confirmation lock. No safety-overlay live
  evidence existed at that checkpoint. The subsequent exact-merged execution
  completes 22/22 with zero failure classes or observation gaps; nine manual
  pairs are both-correct without lift and the two generic invoke pairs gain
  positive route/procedure lift. Session-growth is next; its subsequent source
  pass closes all 14 contracts on both axes and the typed cohort-slug sanitizer
  gap. Its first exact live run completes 28/28 but remains `needs-rerun` on
  three manual target-report gaps and one ambient competing-skill
  classification. V17 repairs the shared description and grader owners and
  opens only the exact eight-turn paired return; no later wave is open yet.
- Superseded by: none.

## Review Log

### 2026-07-12 - Bind the session-growth routing repair in v17

- Prompt-visible owner: derive a policy preamble during portable export for all
  45 non-invoke skills. `manual` forbids an implicit load; `suggest` may only
  recommend. Explicit user/operator invocation and source-authorized parent
  selection remain valid, so root-child trajectories are not broken.
- Measurement owner: a correctly manual unread target may coexist with a
  repo-visible ambient skill. Continue to fail target-facing `invoke`, target
  load, wrong target procedure disposition, and competing wins for non-manual
  targets.
- Previous v14 assumption revised: repo visibility alone is not enough to call
  a selected skill the target treatment when the output contract explicitly
  distinguishes `selected_skill` from the expected target. Target report and
  objective read evidence own that judgment.
- Protocol: bump to live evidence v17 and app-server evidence contract v12;
  keep every v16 receipt immutable under its original grader and source lock.
- Return: add exactly both arms of collisions 21, 22, 25, and 33, for eight
  turns and four complete pairs. Exact merge, refreshed installed-profile
  parity, host gates, and both confirmations remain required; proof and
  promotion authority stay false.

### 2026-07-12 - Preserve the session-growth routing return

- Exact source: the completed run uses merged commit `7c5803c`, the verified
  installed foundation profile, v16 protocol, 37 isolated shadows, 11 disabled
  MCP ids, medium agent wrapper, concurrency one, and fresh storage/resource
  gates. A prior unsupported-model transport failure stops before skill work
  and is not promoted into public skill evidence.
- Complete observation: 28/28 turns and 14/14 pairs complete; every fixture and
  owner-action probe is single-attempt, successful, observed, and verified.
  All outcomes are observation-clean and correct in both arms. External access,
  broad inventory, owner-boundary, prompt-visibility, and post-host issues are
  zero.
- Aided gaps: cases 21, 22, and 25 leave their explicit-only target unread but
  select ambient eval/session-mining and misreport the target route as
  `invoke`. Case 33 keeps the target manual with `not_applicable`, but ambient
  `aoa-change-protocol` reaches the competing-skill classifier first.
- Diagnosis: explicit-only policy exists in portable metadata but not in the
  trigger-visible description, while the classifier contradicts its ambient
  skill report contract for an otherwise-correct manual target. Treat these as
  shared runtime-description and measurement-order gaps, not four independent
  target-skill defects.
- Return: preserve the public-safe receipt as reviewed `needs-rerun`; repair
  both shared contracts red-first and add a paired return containing only
  collisions 21, 22, 25, and 33. Proof and promotion authority remain false.

### 2026-07-12 - Close the session-growth source contracts

- Scope: `full-collision-session-growth` contains exactly both arms of
  `collision-20` through `collision-33`, for 28 turns and 14 pairs.
- Procedure split: cases 20-27, 29, 31, and 33 are explicit-only or
  deliberately manual and remain `not_applicable`; generic invoke cases 28,
  30, and 32 select their intended base route but stop at
  `blocked_missing_input` for absent owner surfaces.
- Owner actions: all fourteen pairs now select one source-derived decision from
  three sorted candidates without granting writeback, delegation, diagnosis,
  repair, automation, commit, push, or fabricated change authority.
- Source lock: add the nine session-growth and Abyss skill sources newly cited
  by collisions 21-32; preserve existing collision-20 and collision-33
  anchors unchanged.
- Sanitizer return: the focused synthetic receipt exposed a false positive on
  the plan-owned `full-collision-session-growth` slug. Treat typed cohort
  fields as bounded portable slugs while continuing to reject leading
  transport-shaped ids such as `session-deadbeef` and all untyped leaks.
- Verification and authority: the focused synthetic cohort completes 28/28,
  validates both receipt schemas, and reaches 14/14 on both contract axes.
  This removes only the source-design block. Exact merge, runtime parity, host
  gates, both confirmations, and reviewed live evidence remain mandatory;
  proof and promotion authority stay false.

### 2026-07-12 - Review the exact safety-overlay execution

- Exact source: the 22-turn run uses the merged 11/11 contract packet, unchanged
  installed skill profile, v16 protocol, isolated shadow/MCP sets, medium host
  wrapper, concurrency one, and both confirmation tokens.
- Complete evidence: 22/22 turns and 11/11 pairs complete with no failure class,
  early stop, output observation gap, external filesystem access, or broad
  inventory command.
- Manual safety: cases 09-14, 16, 18, and 19 are correct in both arms without
  loading the manual skill. Route, procedure, and owner-action effects are
  clean `no_lift_both_correct`, with the owner boundary present everywhere.
- Generic value: cases 15 and 17 select and fully read their generic skills,
  stop at `blocked_missing_input`, and show positive aided route plus procedure
  lift; their owner actions are clean and correct in both arms.
- Fixture confidence: all 22 fixture and owner-action probes are observed once,
  succeed, expose their sentinel, and verify.
- Authority and next gate: preserve a reviewed candidate receipt with proof and
  promotion false. Session-growth was blocked at 2/14 procedure and 2/14
  owner-action contracts at this checkpoint; source contract design had to
  precede its live run.

### 2026-07-12 - Close the safety-overlay source contracts

- Scope: `full-collision-safety-overlays` contains exactly both arms of
  `collision-09` through `collision-19`, for 22 turns and 11 pairs.
- Procedure split: manual risk/project cases 09-14, 16, 18, and 19 remain
  `not_applicable` with visible owner boundaries; generic base cases 15 and 17
  select their skills but stop at `blocked_missing_input` for absent owner
  repository evidence.
- Owner actions: every pair has one deterministic source-derived decision among
  three sorted candidates. None authorizes production mutation, hidden overlay
  loading, raw publication, or fabricated document/change authority.
- Source lock: add only the six newly cited `SKILL.md` sources. Correct the
  collision-14 rationale from `explicit-only` to the canonical
  `explicit-preferred` mode plus the collision's deliberate manual owner route;
  keep its expected disposition and owner action unchanged.
- Verification: the focused synthetic cohort completes 22/22, validates both
  receipt schemas, and raises packet coverage to 11/11 on both contract axes.
- Authority: this is contract readiness only. Live execution still requires an
  exact merged source, runtime parity, host gates, both confirmations, and
  reviewed candidate evidence; proof and promotion authority remain false.

### 2026-07-12 - Close the core-wave observation loop

- Exact source: the outcome return runs from the merged return contract with
  the unchanged installed skill profile, v16 protocol, isolated shadow/MCP
  sets, medium host wrapper, and both confirmations.
- Outcome closure: all four `collision-05`/`collision-06` arms observe one
  successful fixture command and one successful owner-action command, expose
  both required sentinels, verify, and retain no failure class or output gap.
- Skill signal: both aided arms again select and load the intended skill and
  produce positive route plus procedure lift; both outcome pairs are clean and
  correct in both arms.
- Combined decision: the fixture return and outcome return now cover every
  observation gap from the first core execution. Keep the original receipt as
  historical `needs-rerun` evidence and both returns as reviewed candidate
  evidence; do not rewrite history or widen authority.
- Next gate: close the core wave as evidence-complete and move contract design
  to the safety-overlay wave. Live execution remains blocked until that wave
  has complete source-owned procedure and outcome contracts.

### 2026-07-12 - Close the fixture return and isolate the outcome return

- Exact source: the four-turn return runs from the merged evidence contract
  with the same skill-source profile, v16 protocol, isolated shadows and MCPs,
  medium host wrapper, and both confirmations.
- Fixture closure: all four `collision-01`/`collision-02` arms observe one
  successful exact fixture command and the required sentinel; all fixture
  execution contracts now match and no failure class remains.
- Skill signal: both aided arms again select and load the intended skill,
  report the source-locked `blocked_missing_input` procedure, and produce
  positive route plus procedure lift over control.
- Outcome signal: both returned owner-action pairs are observation-clean and
  correct in both arms. The result is reviewed candidate evidence only and
  grants no proof or promotion authority.
- Remaining return: the first full-wave receipt still has opposite single-arm
  owner-action observation gaps for `collision-05` and `collision-06`. Add a
  separate four-turn paired outcome return for exactly those cases and keep the
  next collision wave closed until it is reviewed.

### 2026-07-12 - Return the first core wave to fixture output observation

- Complete evidence: all sixteen turns and eight pairs complete; prompt,
  filesystem, inventory, transport process, owner, proof, and promotion
  boundaries remain clean.
- Skill signal: every aided arm matches its intended route and
  source-locked procedure, producing positive route and procedure lift in all
  eight pairs.
- Clean outcomes: six pairs are observation-clean and correct in both arms.
  `collision-05` is `aided_only` and `collision-06` is `control_only`, so their
  raw outcome contrasts are not stable skill-effect evidence.
- Fixture return: `collision-01` control plus both `collision-02` arms observe
  the one exact fixture command and exit zero, but capture zero output bytes;
  fixture verification stays false and all three retain
  `fixture_execution_gap`. The other thirteen arms expose the valid 234-byte
  sentinel payload.
- Decision: preserve the full receipt as `needs-rerun`, make no skill-source or
  proof relaxation, and add a four-turn paired return containing only
  `collision-01` and `collision-02`. Do not widen until that return is reviewed.

### 2026-07-12 - Make broad widening an exact bounded partition contract

- Trigger: the 98-turn `full-collision` and 87-turn `coverage-closure` parents
  were complete inventories but unsafe execution units, and most implicit
  pairs were still declared-only.
- Partition: five semantic collision waves and six closure waves must be
  disjoint and together reproduce every parent trial identity exactly.
- Bound: every wave requires a second exact confirmation, stays at or below 30
  turns, 512 MiB private evidence and memory demand, and light or medium host
  class. Parent inventory views may remain sustained and declared-only.
- Fail-closed rule: child waves may use only `required` or
  `required_for_live`; any missing implicit procedure or outcome contract stops
  before preflight and model spend.
- First slice: `full-collision-core-engineering` covers `collision-01` through
  `collision-08`. New source-authored answer keys for property invariants,
  core logic, port/adapter, TDD, and contract-test routes make the wave 8/8 on
  both contract axes.
- Confirmation ownership: the source plan now carries
  `second_confirmation_required`; cohort names no longer form a hidden runner
  allowlist for the second token.
- Decision: bump the live evidence protocol to v16, land deterministic
  partition and receipt-schema coverage first, then execute only the exact
  merged core wave and return to source, harness, or runtime from its evidence.

### 2026-07-12 - Review the complete v15 full pilot and contract the next widening

- Exact evidence: all 30 turns and eleven pairs complete with no failure class;
  every prompt, scope, fixture, transport-process, owner, safety, proof, and
  promotion boundary remains clean.
- Routing effect: five pairs have positive route and procedure lift; decision
  and eval roots also have positive full-child trajectory lift. Six pairs are
  no-lift-both-correct at those route boundaries.
- Clean outcome evidence: seven pairs are observation-clean and correct in both
  arms, so they show zero owner-outcome lift.
- Qualified outcome evidence: `collision-03` and `collision-08` are
  `control_only`; `collision-20` and `collision-33` are `aided_only`. Their
  apparent positive or negative outcome lift is not stable skill evidence.
- Decision: preserve the public-safe receipt as reviewed candidate evidence,
  with no aggregate score or promotion. Do not jump directly to the 98-turn
  `full-collision` or 87-turn `coverage-closure` plans while their declared
  procedure/outcome coverage is only 10/49 and 1/17; partition and complete the
  next waves first.

### 2026-07-12 - Separate outcome observation gaps from lift in v15

- Trigger: exact single-attempt outcome commands exited zero without sentinel
  bytes first in one aided arm, then in two controls after the source repair.
- Telemetry: publish a per-arm `outcome_output_observation_gap`, aided/control
  pair flags, a bounded gap effect class, and
  `outcome_lift_observation_clean`.
- Proof boundary: a gap requires every command-side prerequisite except the
  sentinel; it never changes `outcome_verification_observed`, outcome contract
  match, failure precedence, proof authority, or promotion authority.
- Compatibility: new public fields are optional in the v1 receipt schema;
  current projections backfill them from existing bounded measures, while
  committed historical receipts remain immutable.
- Replay: the reviewed v14 clean-aided receipt yields `none` for
  `collision-09` and `control_only` for `collision-14` and `collision-38`; the
  latter two lift values remain visible but observation-unclean.
- Decision: bump the live evidence protocol to v15, validate the bounded
  vocabulary and flag consistency, then widen to the full pilot after exact
  merge rather than changing skill source again.

### 2026-07-12 - Close aided source returns and retain control observation gaps

- Exact evidence: all six turns and all three pairs complete after exact merge
  plus verified 36/36 runtime foundation import; every harness, owner, safety,
  and authority boundary stays clean.
- Decision result: `collision-38` aided gains route, complete
  `aoa-decision-find` trajectory, `blocked_missing_input` procedure, and
  sentinel-verified owner outcome over control.
- ATM10 result: `collision-14` aided loads neither generic nor explicit overlay,
  reports the manual owner route, and verifies the bounded owner outcome.
- Approval result: `collision-09` remains correct in both arms, giving honest
  zero lift rather than manufacturing a treatment effect.
- Observation return: the exact owner-action command exits zero without
  sentinel bytes in two control arms. Keep both outcomes unverified and do not
  treat their positive aided-control lift as stable proof.
- Decision: preserve the public-safe receipt as reviewed candidate evidence;
  add explicit per-arm and pair-level output-observation-gap telemetry without
  changing verification, then widen to the full pilot.

### 2026-07-12 - Repair the two narrowed source returns

- Decision child: when the active permitted boundary has neither graph or
  fallback lookup nor graph status, changed paths, target records, or an owner
  repository packet, `aoa-decision-find` now stops with
  `blocked_missing_input`; it does not reinterpret missing inputs as
  `deferred_owner_boundary`.
- ATM10 exclusion: a prompt that names an ATM10 repository and asks for
  repo-relative paths, local commands, or local approval notes now reports the
  manual owner route without loading generic `aoa-change-protocol` or the
  explicit overlay.
- Preserved behavior: decision graph lookup and source-note verification remain
  active when their evidence is available; generic bounded changes remain
  implicitly routable; both explicit targets and the owner-action answer keys
  remain unchanged.
- Proof boundary: the empty aided sentinel event remains an observation return.
  Exact command identity and zero exit do not become outcome verification.
- Decision: bind both changes red-first in source and prompt-visible contracts,
  refresh generated/export/runtime parity, then repeat the existing six-turn
  cohort before any full-pilot widening.

### 2026-07-12 - Preserve the mixed first skill-return execution

- Exact evidence: all six `pilot13-skill-returns` turns and all three pairs
  complete on the merged source with clean prompt, filesystem, inventory,
  fixture, transport-process, owner-action, safety, and authority boundaries.
- Closed return: `collision-09` keeps the approval owner and every repo skill
  unloaded, reports the manual target route, and gains the source-locked owner
  outcome over control.
- Decision return: `collision-38` now gains route and the complete
  `aoa-decision-find` child trajectory. The child still reports
  `deferred_owner_boundary` where the absent graph and owner packet requires
  `blocked_missing_input`.
- Observation return: the aided arm runs the exact owner-action command once
  with exit zero but exposes no sentinel output bytes. Keep outcome verification
  false and preserve the event as an observation gap rather than weakening the
  sentinel contract or changing the answer key.
- Boundary return: `collision-14` gets the target route, procedure, and outcome
  right while still loading generic `aoa-change-protocol`. Strengthen only the
  concrete ATM10 repo-relative exclusion; do not make generic changes manual or
  alter the explicit ATM10 overlay.
- Decision: retain the public-safe receipt as `needs-rerun`, apply the two
  narrow source corrections, refresh prompt-visible runtime parity, and repeat
  the affected cohort before widening.

### 2026-07-12 - Repair two source boundaries and bind a six-turn return

- Decision root: classify first, then select and fully read exactly one
  `aoa-decision-find`, `aoa-decision-create`, or `aoa-decision-correct` child
  before graph lookup or a write. A root-only route that merely names the child
  is incomplete.
- Generic change boundary: keep `aoa-change-protocol` implicitly available for
  generic bounded work, but exclude approval-only production classification
  and project-specific manual-overlay ownership in both source and portable
  prompt descriptions.
- Rejected alternatives: do not weaken the `collision-38` child contract; do
  not make the entire change protocol manual; do not change or implicitly load
  the explicit-only approval and ATM10 target skills.
- Eval contraction: add `pilot13-skill-returns` with only both arms of
  `collision-38`, `collision-09`, and `collision-14`, 3/3 procedure contracts,
  3/3 owner-action contracts, a high-cost token, and private/public cohort enum
  parity.
- Stop line: source, generated, and deterministic checks cannot close the live
  return. Merge the exact tree, verify prompt visibility, then run the six-turn
  cohort under normal host gates before widening.

### 2026-07-12 - Contract the complete v14 return to two source skills

- Exact evidence: all 15 `pilot13-returns` turns and all seven pairs complete;
  prompt, filesystem, inventory, fixture, transport, owner-action, authority,
  and the final Abyss structured contracts stay clean.
- Cleared returns: `collision-20`, `collision-33`, `collision-49`, Titan, and
  the Abyss overlay-to-base hierarchy have no failure class under fresh v14
  transport.
- Decision return: `collision-38` reads `aoa-decision` but does not select and
  fully read the source-required `aoa-decision-find` child. Keep the trajectory
  contract and strengthen the root handoff rather than weakening the grader.
- Boundary return: `aoa-change-protocol` is loaded for the explicit-only
  `aoa-approval-gate-check` case and displaces `atm10-change-protocol` in the
  ATM10 overlay case. The explicit targets remain unchanged; narrow the generic
  skill boundary.
- Decision: preserve the public-safe receipt as `needs-rerun`; add deterministic
  regressions before editing the two source skills, then exact-merge and rerun
  only the three affected pairs before widening.

### 2026-07-12 - Separate repo treatment from ambient target reporting in v14

- Live evidence: `collision-20` aided reported
  `aoa-session-memory-global-route`, while `collision-49` aided reported
  `abyss-machine`. Both kept the explicit target unloaded and chose
  `manual_required`, but v13 rejected the non-target selected name.
- Counter-evidence: `aoa-change-protocol` and `aoa-eval` were prompt-visible
  repo selections and were invoked or claimed loaded. Those remain real
  treatment-side collision/leak candidates.
- Prompt return: v13 no-dispatch guidance lived only in
  `_with_fixture_procedure`; implicit arms used `_with_fixture_scope` directly,
  so the instruction never reached the pilot pairs.
- Output return: Titan control combined `selected_skill=null` with
  `claims_loaded=true`. Keep this invalid, and make the null-load invariant
  explicit in the final target-report guidance and output schema description.
- Decision: classify reported selection against the exact prompt-visible repo
  names; let manual target dispatch depend on `manual_required` while target
  load remains independently false; append target procedure semantics to every
  arm; publish only booleans for repo-visible versus non-treatment reporting.
- Replay: under v14, only `collision-20` aided and `collision-49` aided change,
  each from `dispatch_policy_gap` to `procedure_disposition_miss`. Two
  collisions, two repo activation leaks, one existing procedure miss, and one
  output-contract failure remain. Preserve v13 receipts unchanged and require a
  fresh exact-merged v14 run before editing skills.

### 2026-07-12 - Preserve partial v13 returns and close receipt schema parity

- First attempt: stopped after six turns when `collision-33` control reached
  the source-locked 180-second transport cap after turn start. Scope and prior
  owner-action gates remained clean.
- Fresh attempt: passed the earlier timeout and reached fourteen turns. Titan
  control then combined no selected skill with `claims_loaded=true`; the model
  output validator correctly stopped before the final Abyss structured arm.
- Live return: external ambient routes preserved the explicit target boundary
  but were still graded as aided policy gaps, while repo-visible
  `aoa-change-protocol` and `aoa-eval` activations remain real collision/leak
  candidates. Manual target procedure disposition also stayed ambiguous.
- Source return: `pilot13-returns` was added to the plan schema but omitted from
  private and public receipt cohort enums, so review rejected the new raw
  receipts before projection.
- Decision: preserve both partial receipts under their original v13 measures;
  add the missing cohort enum and an end-to-end synthetic private/public test;
  land this evidence repair before changing grader semantics or spending on a
  third live attempt.

### 2026-07-12 - Bind the smallest live confirmation of v13 returns

- Input: v13 read-only replay leaves seven aided returns and removes four
  harness-side false labels, but replay cannot replace a fresh transport run.
- Rejected option: rerunning all 30 pilot turns would repeat thirteen already
  clean arms and spend evidence budget without increasing discrimination.
- Cohort contract: retain both aided and control arms for `collision-38`,
  `collision-20`, `collision-33`, `collision-09`, `collision-14`,
  `collision-49`, and `desc-titan-03-manual`; add only structured
  `abyss-safe-infra-change`; include no trajectory arms.
- Safety: require complete procedure and owner-outcome contracts for all seven
  pairs, the exact source confirmation token, the second high-cost token, and
  normal storage/resource/runtime/prompt isolation preflights.
- Decision: add `pilot13-returns` as a 15-turn medium cohort. A clean rerun may
  validate the repaired measurement path; it cannot promote a skill, rewrite
  the v12 receipt, or authorize wider cohorts by itself.

### 2026-07-12 - Separate v13 harness repairs from remaining skill candidates

- Corrected interpretation: the first review tentatively treated the
  `collision-38` child expectation as premature. Source reread shows that
  `aoa-decision` must choose one find/create/correct route, classifies
  find-or-understand first, and loads only that child. Keep
  `aoa-decision-find` as the source-authored handoff candidate.
- Manual control boundary: a control arm that invokes an ambient non-target
  route did not load the explicit-only target. Keep its target route match
  false for pair contrast, but do not call it a target activation leak or route
  it to a skill repair.
- Procedure boundary: when manual-required or do-not-use selects no target
  procedure, the selected-procedure disposition is `not_applicable`; blocked
  and owner-deferred describe a dispatched procedure and need explicit prompt
  separation.
- Structured report boundary: `abyss-safe-infra-change` source starts from
  `aoa-safe-infra-change`. Add a separate source-locked target-to-base-child
  hierarchy; do not weaken direct-target or unrelated-child checks.
- Replay result: v13 read-only regrading of the immutable v12 raw pilot yields
  23 clean arms and seven aided returns: one decision handoff, three manual
  procedure reports, and three manual collision routes. This validates the
  corrected grader only and does not replace or rewrite the public receipt.
- Decision: bump the live evidence protocol to v13, bind both hierarchy source
  skills into the plan and JIT sidecar, then run the smallest affected live
  cases before any new full pilot or skill promotion claim.

### 2026-07-12 - Preserve the first full pilot as mixed adaptive returns

- Source posture: PR #315 merged as `7d5fcd0f`; its squash tree exactly matched
  the reviewed feature tree. The 30-turn plan and both operator tokens were
  bound to that clean detached source under protocol v12.
- Host posture: storage allowed the 512 MiB private target and the source-
  printed medium/agent resource route launched without force. The wrapper
  returned zero with 163.4 MiB peak memory and 18.6 MiB peak swap.
- Clean evidence: all 30 turns completed; no prompt, filesystem, broad
  inventory, transport, fixture, outcome-validator, owner-boundary, proof, or
  promotion gate failed. All eleven owner-action pairs were correct in both
  arms with exactly one uninspected attempt.
- Skill candidates: implicit pressure selected `aoa-change-protocol` instead
  of preserving the manual boundaries of `aoa-summon`,
  `aoa-approval-gate-check`, and `atm10-change-protocol`.
- Harness and contract returns: `collision-38` prematurely required
  `aoa-decision-find` before graph status; ambient non-target control routes
  were labelled manual activation leaks; manual no-dispatch procedures did not
  share the authored `not_applicable` vocabulary; and the structured grader
  rejected the source-valid `abyss-safe-infra-change` to
  `aoa-safe-infra-change` hierarchy.
- Decision: preserve a public-safe `needs-rerun` receipt. Repair privacy
  projection, source contracts, and grader semantics before changing skills;
  then rerun the smallest affected cases before another full pilot.
- Privacy return: typed canonical skill names containing `session`, `thread`,
  or `turn` are public repo identifiers, not transport ids. Accept them only in
  schema-typed skill-name fields while retaining UUID, bare transport-id, path,
  credential, and raw-field rejection everywhere else.

### 2026-07-12 - Close both pilot contract coverage gates

- Previous posture: the exact-merged v12 smoke validated one `collision-42`
  owner-action seam, leaving ten implicit pilot cases without complete
  procedure and outcome contracts.
- Source review: three direct invoke cases lack the repository evidence needed
  to complete their procedures; two root routes must select and fully read
  their first child before blocking; six explicit-only skills must stay
  unloaded and report `not_applicable` under implicit pressure.
- Decision: author one source-locked procedure contract and one independent,
  sorted three-choice owner-action contract for every implicit pilot case.
  Keep child-read expectations null where no child exists, and keep fixture
  execution, procedure disposition, bounded owner choice, and whole-task
  completion separate.
- Validation boundary: deterministic expansion and plan tests now report 11/11
  procedure coverage and 11/11 outcome coverage while preserving fail-closed
  tests for an incomplete corpus. This makes the pilot plan-eligible only; it
  is not live evidence, a family verdict, central proof, or promotion authority.
- Next route: merge the exact source, obtain the source-bound plan and high-cost
  tokens, run through host resource gates, and review every return before any
  broader cohort.

### 2026-07-12 - Validate the owner-action seam on exact-merged v12

- Source posture: PR #313 merged as `25596566`; its squash tree exactly matched
  the reviewed feature tree. The smoke planned and ran from a clean detached
  worktree at that exact commit under protocol v12.
- New evidence: all four arms completed with no failure class, external read,
  broad fixture inventory, outcome-validator inspection, or retry. Route and
  selected-child trajectory lift are `+1`. Procedure disposition and the
  owner-action outcome are correct in both arms, so each reports `0` lift.
- Decision: accept the public receipt as evidence that the outcome seam is
  independently observable and anti-inspection guards hold. Do not infer
  skill-specific outcome lift from a no-lift-both-correct pair.
- Boundary: the receipt remains owner-local candidate evidence. It does not
  prove target-repository completion, family-wide effectiveness, central eval
  acceptance, promotion, or pilot readiness.
- Next route: preserve the reviewed receipt, then author procedure and outcome
  contracts for the remaining ten pilot cases before any 30-turn execution.

### 2026-07-12 - Add one-attempt owner-observable outcome seam

- Previous assumption: because the fixture could not complete the external
  repository task, every objective outcome had to remain unscored.
- New distinction: external task completion is still unavailable, but a
  source-authored next owner action can be observed independently through one
  bounded command event without reusing route, disposition, or generic probe
  evidence.
- Decision: store candidate choices and the expected owner action in a separate
  source-locked corpus; omit the answer from the plan lock; accept exactly one
  atomic zero-exit sentinel event; classify validator inspection or retry as
  contamination; keep a wrong single choice as negative outcome evidence; and
  make both smoke contract axes required before preflight.
- Boundary: this is a fixture-scoped decision outcome, not repository mutation,
  whole-task completion, a central eval verdict, proof acceptance, or skill
  promotion authority.
- Validation: red-first tests cover source/schema locks, answer-key omission,
  atomic command success, validator-inspection rejection, pair scoring, public
  projection, and retained v1-v11 receipt compatibility. A fresh exact-merged
  v12 smoke must pass before the shape expands beyond `collision-42`.

### 2026-07-12 - Validate fail-closed selection precedence on exact-merged source

- Previous evidence: the post-JIT smoke chose `aoa-eval-local-need` while fit
  was unknown, yielding route lift `+1` but trajectory lift `0` with both arms
  incorrect.
- Source repair: make unknown fit, missing target evidence, and inspect/decide
  requests route to `aoa-eval-select`; local need requires an explicit no-fit
  result.
- New evidence: the fresh exact-merged rerun completed all four arms. The aided
  root selected and fully read `aoa-eval-select`; control had no repo skill.
  Route and trajectory lift are each `+1`, both procedure dispositions are
  correct, and every prompt, fixture, filesystem, inventory, transport, and
  owner-boundary gate passes.
- Boundary: objective outcome remains unscored and one successful smoke is not
  a family verdict, status promotion, or permission to run the pilot before its
  11/11 procedure and outcome coverage gates close.
- Decision: close the precedence adaptive return, preserve both before/after
  receipts, and move next to owner-observable pilot contract design.

### 2026-07-12 - Keep unknown fit in selection before local intake

- Previous assumption: the existing phrases "existing eval may fit" and
  "inspect current surfaces before local need" were strong enough to keep an
  underspecified target in `aoa-eval-select`.
- New evidence: the exact-merged post-JIT smoke passed every prompt, fixture,
  filesystem, inventory, transport, and owner-boundary gate, but its aided arm
  selected and fully read `aoa-eval-local-need`. It correctly returned
  `blocked_missing_input` without mutation; the route itself was premature
  because no selection had established no-fit.
- Decision: unknown fit, missing target evidence, or an inspect/decide request
  routes to `aoa-eval-select`, which may stop on missing input. Local need is
  allowed only after an explicit no-fit result from selection or equivalent
  owner inspection.
- Evidence posture: preserve the reviewed receipt with route lift `+1`,
  trajectory lift `0` and both incorrect, procedure-disposition lift `0` and
  both correct, and unscored outcome. It is candidate evidence, not a central
  verdict or family claim.
- Validation: red-first source regression, dedicated trigger snapshot,
  generated/export parity, exact owner JIT suite execution, and a fresh
  exact-merged smoke before pilot widening.

### 2026-07-12 - Carry the owner JIT execution contract into the selected skill

- Previous assumption: once `aoa-eval-apply` had selected an existing
  deterministic eval, its general command/artifact/proof-limit procedure was
  enough to apply any local suite safely.
- New evidence: the accepted `aoa-evals` local-port contract gives reviewed
  `*.suite.json` files a narrower handoff. Readiness, dashboards, generated
  readers, and MCP may report `source-contract-ready` but cannot execute;
  owner/apply must JIT-revalidate the current source, invoke the exact typed
  runner, capture environment posture, and write a private execution receipt.
  Live MCP status also described a dirty divergent canonical workspace while
  exact merged validation remained available from a separate clean tree.
- Decision: make source identity explicit in `aoa-eval`, preserve dirty
  canonical workspaces, and make sidecar JIT validation plus exact invocation,
  environment capture, and private receipt part of `aoa-eval-apply`. Add a
  positive trigger/snapshot case for an already-selected sidecar.
- Boundary: this adopts the owner handoff; it does not move schema, readiness,
  proof, verdict, scoring, promotion, or execution authority into MCP or
  generated readers. A green execution remains candidate evidence.
- Validation: focused trigger/snapshot tests, owner sidecar validation against
  an exact source tree, generated/export parity, private post-commit receipts,
  and a fresh exact-merged v11 smoke before pilot widening.

### 2026-07-12 - Validate bounded route and trajectory lift on exact-merged v11

- Previous pressure: v10 could not distinguish a genuine child-route problem
  from the context cost and causal noise of full-tree fixture archaeology.
- New evidence: the source-locked v11 smoke completed all four arms. Every arm
  stayed inside the fixture, used zero broad inventory commands, passed the
  independent fixture probe, and retained owner/proof/promotion stop lines.
- Pair readout: aided `aoa-eval` selected and fully read `aoa-eval-select`;
  control did neither. Route and selected-child trajectory lift are each `+1`.
  Both arms correctly reported the selected procedure as
  `blocked_missing_input`, so procedure-disposition lift is `0` with both
  correct. No owner-bound objective outcome exists, so outcome lift remains
  null and `not_scored_no_observable_outcome`.
- Direct/structured readout: the manual root arm selected
  `aoa-eval-apply`, and the App Server arm accepted official structured
  `aoa-eval-apply` input. Both matched dispatch/load and fixture-execution
  contracts without rewriting native evidence from model reporting.
- Decision: treat v11 as reviewed positive route/trajectory candidate evidence
  and close the inventory-harness return. Do not edit or promote `aoa-eval`
  from this single smoke. Return next to the source corpus and owner-bound
  observation design until pilot coverage reaches 11/11 on both required axes.
- Boundary: `completed` means the bounded four-arm measurement completed. It
  does not mean whole-task outcome, central eval verdict, proof acceptance,
  family-wide effectiveness, or promotion.

### 2026-07-12 - Bound exact reads without full-tree fixture archaeology

- Previous assumption: keeping every model command inside the hermetic fixture
  was enough to make its read evidence bounded; any later cap stop could be
  reviewed mainly as a budget or skill-trajectory question.
- New evidence: the first exact-merged v10 aided arm used broad hidden
  enumeration and stopped before final output. An unchanged repeat completed
  aided/control, then the explicit root arm read the expected child but also
  listed and hashed the full fixture before exhausting 48k. The repeated shape
  occurred in different arms while storage, resource, runtime, prompt, and
  external-filesystem gates remained clean.
- Replay boundary: the v11 detector finds two distinct broad commands in the
  first aided arm and, in the unchanged repeat, two in aided, two in control,
  and four in the root trajectory. This validates the new grader only; the v10
  public fields remain immutable.
- Decision: v11 prompt and fixture guidance allow only exact route-required
  reads: guidance, selected root or target, at most one selected child, and the
  named validator. Command events separately detect `rg --files`, `find`,
  `tree`, recursive `ls`, `du`, inventory pipelines, and broad tree hashing as
  `fixture_inventory_scope_violation` before budget or skill interpretation.
- Boundary: this does not reveal which child to choose, forbid the required
  complete child read, raise the cap, or relabel either immutable v10 receipt.
  The completed aided `trajectory_break` remains candidate evidence until a
  fresh v11 run removes inventory pressure.
- Validation: red-first tests distinguish exact reads from broad enumeration,
  prove inventory violation outranks budget, preserve v1-v10 public receipt
  compatibility, and retain the pilot stop at 1/11 procedure plus 0/11 outcome
  coverage.

### 2026-07-12 - Separate native dispatch, child procedure, fixture probe, and outcome

- Previous assumption: once v9 bound `procedure_disposition` to a downstream
  procedure, `python3 fixture_validator.py` could stand in for that procedure;
  structured model output also had to report the invoked child directly or the
  native dispatch was considered wrong.
- New evidence: the exact-merged v9 smoke selected and fully read
  `aoa-eval-select`, correctly blocked on missing target-repository evidence,
  and independently passed the fixture validator. Its structured arm accepted
  official `aoa-eval-apply` input, passed the same probe, and reported
  `aoa-eval` plus `aoa-eval-apply` as an equivalent root-child hierarchy. V9
  recorded outcome no-lift and `dispatch_policy_gap`, revealing grader pressure
  rather than two skill defects.
- Boundary map: the necessary lenses are object-kind/vocabulary,
  authority/proof, interface/handoff, and surface-state. Transport owns sent
  structured dispatch and accepted native load. Model output owns only its
  direct or hierarchy report. Case/root/child source owns expected trajectory
  and procedure disposition. The fixture validator owns only hermetic probe
  execution. A private/public live receipt is candidate evidence. No current
  surface owns an objective external-task outcome observation.
- Decision: v10 publishes route, selected-child trajectory, fixture execution,
  and selected-procedure-disposition report as separate contracts. A
  structured hierarchy report is exact only when both its root and child match
  the source-declared `root_child_trajectories` edge. The
  `collision-42` source contract expects `aoa-eval-select`, its complete read,
  and `blocked_missing_input`. Official structured input sent/accepted is not
  overridden by that report. Objective outcome lift is null with
  `not_scored_no_observable_outcome`.
- Adaptive return: wrong declared child is `trajectory_break`; a correct child
  with a mismatched disposition report is `procedure_disposition_miss`; a
  missing validator probe is `fixture_execution_gap`; a structured report that
  matches neither the direct target nor the exact source-declared root-child
  edge is `selection_report_miss` without changing native dispatch/load facts.
  None authorizes a skill edit until its stronger source contract survives
  review.
- Boundary: v8 and v9 receipts remain immutable. V10 replay of raw evidence is
  grader validation only: v8 becomes route `+1`, trajectory `0`, procedure
  `-1`; v9 becomes route `+1`, trajectory `+1`, procedure `0`; both have
  objective outcome unscored. A fresh exact-merged v10 smoke is required.
- Validation: red-first tests cover native dispatch versus hierarchy report,
  child trajectory versus procedure disposition, fixture-probe independence,
  historical receipt compatibility, and pilot blocking at 1/11 procedure plus
  0/11 objective outcome coverage before full repository and cross-surface
  gates.

### 2026-07-12 - Bind outcome to the downstream procedure, not the whole task

- Later status: superseded by the v10 review above. The fresh v9 smoke proved
  that the fixture probe and selected child procedure did not share one scope,
  so the positive outcome expectation in this historical step is not current
  doctrine.

- Previous assumption: because the `collision-42` prompt withholds real
  repository inputs, the pre-authored outcome key should expect
  `blocked_missing_input`, no completion, and deflection even after the exact
  hermetic fixture procedure succeeds.
- New evidence: the exact-merged v8 smoke recorded positive route lift and
  negative outcome lift. The aided arm selected and fully read `aoa-eval` and
  `aoa-eval-apply`, executed `python3 fixture_validator.py`, observed its zero
  return and guidance-bound sentinel, and reported the bounded procedure as
  completed while separately preserving the missing real-repository inputs and
  owner stop-lines. More importantly, the pre-existing constrained model-output
  schema defines `procedure_disposition` as the disposition of the downstream
  skill procedure; the fixture and selected child procedure agree with that
  scope. The live observation triggered review but did not author the new key.
- Decision: v9 names the scope
  `bounded_downstream_procedure_outcome`, derives the `collision-42` expectation
  as completed/verified/non-deflected from the model-output, case, fixture, and
  skill sources, publishes that scope on current measures and pairs, and keeps
  outcome matching independent of route correctness.
- Boundary: bounded procedure completion is not completion of an external
  repository task, proof acceptance, or permission to ignore missing owner
  inputs. The v8 receipt and its negative outcome remain immutable under the
  invalid historical key and are classified `needs-rerun`; they are not
  silently relabeled by v9. Historical public receipts remain schema-readable.
- Adaptive return: an apparent `bounded_outcome_miss` must first be checked
  against the declared scope and the authoritative procedure semantics. Only
  after the key survives that review may the same evidence pressure a skill
  procedure.
- Validation: red-first tests require the corrected scope/key, preserve legacy
  v8 public validation, and force replayed aided/control arms to produce
  positive route and positive downstream procedure-outcome lift. Full harness,
  repo lanes, local eval-port, decision-index, generated/export parity, and a
  fresh exact-merged v9 smoke remain required before `pilot13`.

### 2026-07-12 - Split route lift from source-locked bounded outcome lift

- Previous assumption: a matched implicit pair could publish one generic
  `observed_lift` and `effect_class` derived from route-contract correctness
  while procedure disposition, completion, and deflection remained separate
  arm measures.
- New evidence: the exact-merged v7 smoke completed all four arms and produced
  a clean positive pair. The aided arm routed and loaded `aoa-eval`, ran and
  verified the fixture validator, then correctly reported missing owner input;
  the control ran the same validator but deferred to an owner boundary. The v7
  pair code nevertheless used only `route_contract_match`, so its generic
  positive label could be misread as completion or outcome lift.
- Decision: preserve v7 unchanged as reviewed route-contract evidence. For v8,
  replace generic new-pair fields with explicit route and outcome dimensions;
  source-lock bounded outcome contracts authored from case, skill, and fixture
  sources before live execution; make outcome matching independent of route;
  publish bounded mismatch dimensions; and report missing contracts as
  `not_scored_no_contract` rather than false or zero lift.
- Boundary: the `collision-42` contract proves only the hermetic fixture
  outcome. It does not prove inspection or completion in a real target repo,
  does not use the v7 observation as an answer key, and does not widen local or
  central proof authority. Historical v1-v7 pair fields remain reviewable but
  are not upgraded in place.
- Adaptive return: when an aided route/load passes but its declared bounded
  outcome does not, use `bounded_outcome_miss` to review both the skill
  procedure and the source-authored contract before repeating the same case.
- Validation: red-first tests must force route and outcome lift to opposite
  signs, reject required smoke planning without its contract, preserve legacy
  pair review, validate public privacy/schema shape, and rerun the full harness
  before a fresh exact-merged v8 smoke.

### 2026-07-12 - Make process exit report cohort completeness

- Previous assumption: writing a private receipt was sufficient for the live
  runner to return process exit 0, because semantic failure remained visible in
  the receipt.
- New evidence: the exact merged v6 smoke passed prompt and fixture-scope gates,
  then the first CLI transport timed out at 180 seconds before any turn event,
  model output, usage, or pair. The receipt correctly set
  `stopped_early=true` and `transport_failure`, but reset duration to zero and
  the `run` command returned 0, causing the host wrapper to report success for
  an incomplete cohort.
- Decision: measure elapsed time around CLI and App Server transport calls;
  preserve that duration plus partial private streams, parsed JSONL events, and
  usage on caught exceptions; publish `stopped_early` and `stop_reason` in the
  bounded command summary; and return exit 1 only for an incomplete cohort
  after its private receipt has been written. Complete negative model evidence
  remains a successfully executed cohort and exits 0.
- Boundary: the v6 public receipt remains immutable under its historical
  zero-duration and process-success behavior. A prior rate-limit packet at full
  primary utilization is runtime context, not proof of the sole timeout cause;
  no skill, pair, lift, status, promotion, or family conclusion follows.
- Tradeoff: orchestration now treats stopped-early runs as command failures and
  must inspect the preserved receipt for the bounded reason. This is deliberate:
  the wrapper should not equate artifact creation with completed measurement.
- Validation: red-first tests must distinguish complete-negative exit 0 from
  incomplete exit 1, prove the bounded summary fields, and preserve observed
  timeout duration before landing v7 and repeating only after runtime
  availability.

### 2026-07-11 - Assemble complete skill reads across ordered transport events

- Previous assumption: requiring one successful command output to contain the
  complete exact-path `SKILL.md` source was a safe proxy for a complete read.
- New evidence: the exact merged v5 aided arm selected `aoa-eval`, read its
  complete source in two consecutive exact-path ranges, read the dynamically
  selected `aoa-eval-apply` child completely, and verified the fixture
  procedure. The v5 grader nevertheless emitted `skill_load_gap` because
  neither root-read output alone contained the whole source.
- Decision: accept either one complete successful exact-path output or ordered
  successful exact-path outputs whose source intervals continuously cover the
  file. Permit overlap, ignore unrelated outputs, and reject gaps,
  reverse-only coverage, failed commands, inventory mentions, and shadow paths.
- Boundary: the v5 public receipt remains immutable under its historical
  single-output semantics. Raw replay proves the grader repair only and does
  not replace a fresh v6 live result or support status, promotion, family, or
  all-skill conclusions.
- Tradeoff: the detector is slightly more stateful, but it models normal
  progressive reading of long skills without weakening exact-path, success,
  order, or complete-source requirements.
- Validation: preserve the real v5 two-chunk shape in a red-first regression;
  prove overlap and unrelated metadata do not break continuous coverage; keep
  missing, reversed, inventory-only, and shadow-path cases negative; replay the
  private v5 trace; then land v6 and repeat the exact merged smoke.

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
prove selected-route procedure execution or completion outside its declared
source contract. Fixture-probe success is not external-task completion. A
`needs-rerun` receipt or a run
with prompt/background contamination must not drive skill edits, promotion, or
outcome-lift claims. Route, trajectory, model disposition report, and fixture
execution must not be relabeled as objective outcome evidence. Only a separate
source-locked owner-action validator event can fill that dimension, and it does
not imply whole-task completion. Pilot widening requires both complete
procedure-contract coverage and separately observable owner-bound outcome
coverage.

## Validation

- `python -m pytest -q tests/test_live_skill_dispatch_harness.py`
- `python scripts/lanes/ci_gate.py --mode source-fast`
- local eval-port validation through the current `aoa-evals` owner
- decision-index regeneration and parity check
- exact `codex --version`, App Server schema contract, resource-wrapper cgroup,
  storage preflight, shadow-set lock, and `codex debug prompt-input` inventory
  checks before a live turn
- exact-merged complete-corpus review before each pilot rerun, then reviewed
  pilot evidence before any broader widening or skill-defect claim
- one-attempt outcome-validator, no-answer-in-plan, and anti-inspection tests
  before any owner-action outcome is scored
