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
- explicit root-to-child trajectories where complete root and child
  `SKILL.md` reads must be visible in transport events;
- structured App Server skill input, bound to the exact 57-skill fixture path
  map and the server-issued thread id, with no `$skill` activation in its text
  item and no configured MCP startup before the turn;
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

The corrected structured-causality and hermetic pre-turn contract uses schema
`aoa_codex_app_server_skill_input_contract_v2` and protocol revision
`codex-cli-0.144.1-app-server-skill-input-v2`. Retained receipts source-locked
to v1 are historical `needs-rerun` evidence and are not upgraded in place.

The source-locked caps include both the rollout token limit and its required
list of remaining-token reminder thresholds. Every CLI and App Server arm must
pass both values explicitly under strict config so an installed Codex contract
change fails in deterministic adapter tests or pre-turn smoke, not midway
through a campaign.

Root-child trajectories have a separate 48k weighted-token cap because proving
a full child read adds bounded tool-output context that exhausted the common
28k cap in the first real smoke. Implicit and structured arms retain 28k, and a
cap stop without a valid result is classified as `budget_exhausted`, not generic
transport failure. A late budget event after a zero-return, contract-valid
model output cannot override that usable result; the normal semantic classifier
still decides its failure class. Any further increase requires reviewed
cap/context evidence and a same-case rerun.

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
procedure. Root/child and structured arms receive the exact command
`python3 fixture_validator.py`. Transport records full reads, exact command
observation, zero exit, and `AOA_FIXTURE_VALIDATOR_OK` verification as separate
measures.
A full read must name the exact fixture `SKILL.md` path and contain its complete
source. Procedure verification is atomic: one completed exact-command event
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
selection, model load claim, full-read evidence, dispatch and load contracts,
procedure disposition, execution, verification, completion, and deflection.
They publish no raw text and no aggregate score.
Public safety validation walks every string and rejects an absolute host path
even when it is embedded inside a longer prose value.

`skill_load_gap` is the bounded return route when the exact target was selected
but required activation or full-read evidence was not observed. It returns to
read tooling or skill-load behavior for the same case rather than mislabeling
the result as a trigger, trajectory, or procedure defect.

`dispatch_policy_gap` is distinct: the route was available, but the activation
decision violated the expected implicit, manual, trajectory, or explicit
dispatch policy. It returns to dispatch policy, not read tooling.

## Rationale

This route measures different evidence stages without collapsing them. A skill
surface being prompt-visible is not the same as being selected; selection is
not activation; a model load claim is not a complete transport-observed read; a
read is not procedure execution; an exit code is not sentinel verification;
and a route-contract match is neither observed completion nor central proof.

Source locks make a rerun comparable. Exact shadow disabling and pre-turn
inventory checks make the aided/control difference attributable to the fixture
instead of an installed user copy. Paired background digests expose other
prompt-surface drift rather than crediting general model knowledge. Host routing
bounds resource and storage pressure. Private/raw and public/digest separation
keeps review possible without publishing session material.
Paired lift is undefined and omitted when either arm has a transport, budget,
runtime-profile, or owner-boundary safety failure. A contaminated pair remains
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
- Positive: failures carry bounded adaptive return routes instead of one score.
- Positive: ordinary CI proves the harness contract without spending model
  turns or treating model quality as deterministic repository proof.
- Tradeoff: Codex App Server upgrades require an explicit protocol-contract and
  source-lock refresh before live use.
- Tradeoff: single cohort observations remain candidate evidence; review and
  repeated runs are needed before changing skill status or promotion posture.
- Follow-up: rerun smoke under the corrected isolation and evidence contract;
  only then use reviewed smoke and pilot receipts to repair the smallest skill
  cohort before widening to all 57 skills.

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
- Current contract schema: `aoa_codex_app_server_skill_input_contract_v2`.
- Current protocol lock: `codex-cli-0.144.1-app-server-skill-input-v2`.
- Historical protocol: the retained complete smoke is source-locked to v1 and
  `needs-rerun`.
- Superseded by: none.

## Review Log

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
