---
schema_version: local_eval_suite_note_v1
owner_repo: aoa-skills
status: reviewed
authority_boundary: no verdict, scoring, regression, proof doctrine, proof acceptance, or promotion authority
---

# AoA skill live dispatch harness

## Question

Can the current Codex runtime distinguish prompt visibility, model selection
report, transport-owned dispatch, native/load evidence, selected-child
trajectory, independent fixture execution, selected-procedure disposition, and
objective outcome availability against the exact current portable export
without confusing any one stage with the next?

## Arms

- `implicit_aided`: repo-default `.agents/skills` is present, while a pre-turn
  prompt inspection must expose exactly the repo skills whose policy declares
  `allow_implicit_invocation: true` (12 of 57 in the current profile).
- `implicit_control`: the same opaque fixture context has no repo skill
  surface, and pre-turn prompt inspection must expose zero repo skills.
- `root_manual_child`: an explicit root skill must lead to the expected child;
  accepted `$root` invocation is version-locked native root-load evidence, while
  transport must still show a complete read of the selected child and the
  independent bounded fixture probe.
- `app_server_structured`: before `turn/start`, `skills/list` must expose the
  exact enabled fixture-path map for all 57 repo skills, including one and only
  one path for the target, and no configured MCP startup event may occur. The
  server-issued thread follows the official contract with both the exact
  `$skill` text prefix and the matching structured `skill` item. Acceptance is
  native target-load evidence; transport must separately prove the bounded
  fixture probe.

Before any model turn, every arm runs `codex debug prompt-input` under the same
fixture, disabled-feature, and exact external-shadow configuration as its live
adapter. Any repo-skill inventory mismatch stops as `harness_contamination`.
The implicit pair is comparable only when its non-repo background inventory
digests also match. Those digests bind the model-visible name, resolved path,
and description fingerprint for every entry, so a description-only change is
background drift rather than an invisible treatment difference.

The paired implicit arms publish route lift, selected-child trajectory lift,
and selected-procedure-disposition report lift separately. The shared source
contract is authored from the case, root, child, model-output, and fixture
sources before the live run. `python3 fixture_validator.py` is an independent
fixture-execution probe, not the child procedure. V12 adds a separate
source-locked owner-action contract: exactly one
`python3 outcome_validator.py --candidate <value>` event can make a bounded
decision observable without claiming that the unavailable repository task
completed. No dimension is collapsed into an aggregate score.

The current source corpora are
`evals/suites/aoa-skill-live-dispatch-procedures.json` for child/procedure
disposition and `evals/suites/aoa-skill-live-dispatch-outcomes.json` for the
separate bounded owner-action choice.
Smoke requires both source contracts; a missing contract fails planning rather
than silently reverting the outcome dimension to unscored.

## Cohorts

| Cohort | Turns | Purpose | Host class |
| --- | ---: | --- | --- |
| `smoke` | 4 | one implicit pair, one trajectory, one structured input | light |
| `pilot13` | 30 | representative core, risk, project, and Titan pressure | medium |
| `pilot13-returns` | 15 | seven mixed-return pairs plus the corrected Abyss structured report | medium |
| `pilot13-skill-returns` | 6 | three pairs affected by the v14 skill-source repair | medium |
| `full-collision` | 98 | all 49 collision cases as aided/control pairs | sustained |
| `coverage-closure` | 87 | uncovered skills, all root-child trajectories, and all non-invoke structured routes | sustained |

Every cohort beyond smoke requires a second exact high-cost token. Widen only
after reviewing the preceding cohort and repairing any return route it opens.
`pilot13` is additionally `required_for_live`: planning may expose incomplete
procedure-contract and objective-outcome coverage, but confirmed execution
stops before preflight or model spend until both reach all 11 implicit pairs.
The current posture is 11/11 procedure contracts and 11/11 objective outcomes.
This closes only the deterministic coverage gate. The first pilot has since run
as mixed `needs-rerun` evidence, and every rerun still requires an exact source
token, high-cost token, and all host/runtime preflights.

`pilot13-returns` is the bounded v13 confirmation cohort. It preserves both
arms for the seven implicit cases that remained after read-only regrading and
adds only the Abyss structured case whose source-declared overlay-to-base report
was newly recognized. It intentionally excludes already-clean pilot cases and
unaffected trajectory/structured arms. Passing it validates the repaired live
measurement path; it does not by itself promote any skill or replace the
reviewed v12 pilot receipt.

`pilot13-skill-returns` is the next adaptive contraction. It keeps only both
arms of `collision-38`, `collision-09`, and `collision-14`, the three pairs
whose exact v14 evidence changed the `aoa-decision` and `aoa-change-protocol`
source boundaries. It requires all three procedure and owner-action contracts,
schema parity, an exact source token, a high-cost token, and normal host gates.
Passing it can close only these source returns; it cannot replace the wider
pilot or authorize family promotion.

## Evidence Semantics

- fixture presence is availability evidence;
- prompt inspection is model-visible inventory evidence, not dispatch evidence;
- a selected output name is a model report, not transport dispatch, activation,
  or load evidence;
- `claims_loaded` is a model self-report, not objective load evidence or a raw
  read proof, and it never gates the load contract;
- a sent official App Server `$skill` plus `skill` item is transport dispatch
  evidence; accepted exact `$root` or structured input is version-locked
  native-load evidence under Codex
  [progressive disclosure](https://learn.chatgpt.com/docs/customization/overview#skills),
  not a raw shell read;
- an expected or dynamically selected child must be full-read before its load
  contract can pass; the selected child name alone is selection evidence;
- a target, root, or child full read is observed only from completed, zero-exit
  transport events that name the exact fixture `SKILL.md` path; one event may
  contain the whole source, or ordered events may continuously cover it, with
  overlaps allowed and unrelated outputs ignored; gaps, reverse-only coverage,
  and external shadows with the same canonical name do not satisfy the
  contract;
- dispatch-contract, model selection-report, and load-contract matches are
  published separately; a direct target report and the exact source-declared
  root-child hierarchy report cannot override native structured dispatch/load
  evidence, while a matching child under an unrelated root is not equivalent
  and a direct target plus a conflicting child is not exact;
- read-only skill-file inspection commands collect load and trajectory evidence;
- completed or in-progress model commands must remain inside the fixture root;
  absolute host, workspace, session-memory, user-config, other-repository, or
  parent-traversal paths are `harness_contamination` before any budget or skill
  interpretation, while system executables and `/dev/null` remain tooling;
- broad in-fixture enumeration, recursive listing, or tree hashing is
  `fixture_inventory_scope_violation` before budget or skill interpretation;
  exact reads of guidance, the selected root or target, at most one selected
  child, and the named validator remain allowed;
- every arm receives the independent fixture-execution probe
  `python3 fixture_validator.py`; verification is atomic and succeeds only when
  the same completed command event carries zero exit plus exactly one
  `AOA_FIXTURE_VALIDATOR_OK` JSON payload matching status, schema, no generated
  drift, no proof authority, and the current fixture `AGENTS.md` digest;
- a declared objective outcome is a separate single-attempt owner-action
  choice. The model receives a bounded candidate set but not the answer key;
  only one exact completed outcome-validator command with zero exit and its
  contract-bound sentinel passes. Reading, copying, printing, hashing,
  importing, reproducing, or retrying the validator contaminates the pair;
  generic probe success and model prose never satisfy this contract;
- fixture execution, selected-child trajectory, model-reported procedure
  disposition, completion/deflection report, and objective outcome posture are
  published separately; none is task completion or central proof;
- source contracts declare the expected child, child read, selected-procedure
  disposition report, and owner boundary before live execution. Fixture command
  success is graded independently, and no current observation is relabeled as
  objective outcome evidence;
- a competing-neighbourhood entry becomes a collision only when the selected
  skill differs from the expected target;
- a late budget marker cannot replace a contract-valid, zero-return model
  result; the result continues through the semantic failure classifier;
- an explicit `true` mutation, proof, or promotion claim is a safety failure
  before generic output-contract invalidity is considered;
- a normal zero-return transport with an invalid final structured result is
  `output_contract_invalid`, not `transport_failure`;
- caught transport exceptions preserve observed elapsed milliseconds and any
  partial private stdout/stderr, including recoverable JSONL events and usage;
- after preserving the private receipt, an incomplete stopped-early cohort
  reports its stop reason and exits nonzero, while a fully measured cohort exits
  zero even when its skill evidence is negative;
- raw `.aoa` episodes and live transcripts remain reviewed candidates.

The first complete post-classifier-fix smoke from 2026-07-11 is `needs-rerun`,
not reviewed evidence of skill defects. Live prompt inspection later showed
that a user-installed skill shadow remained model-visible in the control and
duplicated the aided target. The run also disabled the shell path required to
prove complete skill reads and supplied no unambiguous selected procedure to
the root/structured grader. Its trigger, trajectory, procedure, and outcome-lift
labels therefore diagnose harness pressure only.

The first complete v3 smoke under its then-current grader from 2026-07-11 is
reviewed candidate evidence.
It records one positive-lift implicit pair, a passing official App invocation,
and one explicit root trajectory in which `aoa-eval` selects
`aoa-eval-apply` but does not full-read the selected child before following its
procedure. That `skill_load_gap` returns to the root skill handoff instruction
and the same case must be rerun after repair. The receipt remains non-proof and
non-promotional. Its fields remain governed by the historical v3 grader and are
not silently upgraded to v4 semantics.

The exact-merged-tree v3 rerun after that repair is separately retained as
`needs-rerun` harness evidence. The first three arms showed that v3 still gated
objective load on `claims_loaded`, omitted a dynamically selected implicit
child from the read requirement, conflated a zero-return output-contract
failure with transport failure, and left read-only inspection ambiguous under
the fixture's "one command" wording. Its recorded pair and failure labels do
not support lift, skill-effect, or family conclusions. The same smoke must be
rerun under v4 before pilot widening.

The exact-merged-tree v4 rerun is also `needs-rerun`. Its aided arm passed
objective root and dynamically selected child reads, but the control read a
complete `aoa-eval` source file from an external canonical checkout before the
48k budget stopped it. V4 recorded `budget_exhausted` because it did not yet
grade filesystem scope; raw review places the earlier fault at harness
contamination. The receipt supports no pair, lift, skill-effect, or family
conclusion. Repeat the smoke under v5 before pilot widening.

The exact-merged-tree v5 rerun is also `needs-rerun`. It fixed fixture
filesystem isolation and completed all four arms, but the aided root source was
read in two ordered exact-path chunks. The v5 grader required one command
output to contain the whole file and therefore emitted a false
`skill_load_gap` and `no_lift_both_incorrect`. The historical fields remain
unchanged; replay under v6 proves only the detector repair. Repeat the live
smoke under exact-merged v6 before pilot widening.

The exact-merged-tree v6 rerun is also `needs-rerun`. Prompt visibility and
fixture scope passed, but the first CLI transport timed out after 180 seconds
before a turn event, output, usage, or pair. The v6 private receipt correctly
stopped early, while its command still exited zero and made the host wrapper
look successful. V7 preserves timeout duration and returns nonzero for an
incomplete cohort. Repeat only after runtime availability and exact-merged v7
validation.

The exact-merged-tree v7 smoke completed all four turns with clean prompt,
fixture, load, procedure, and safety evidence. Its historical pair grader
computed generic `observed_lift=1` only from `route_contract_match`. Review
therefore accepts it as bounded positive route-contract evidence, not as
completion or outcome lift. The immutable public receipt is
`aoa-skill-live-dispatch-smoke-20260712-v7-reviewed-route-lift.json`. V8 returns
to the grader, source-locks the smoke outcome before execution, and requires a
fresh exact-merged rerun before pilot widening.

The exact-merged-tree v8 smoke completed all four turns and separated positive
route lift from a recorded negative outcome lift. Adaptive review returned to
the source contract instead of editing the skill. V9 corrected the immediate
whole-task/procedure wording, but a fresh live run showed that it still treated
`python3 fixture_validator.py` as the selected child procedure. The v8 aided
arm chose `aoa-eval-apply`; the source case requires `aoa-eval-select` before
apply/local-need/design classification. Its immutable public receipt is
`aoa-skill-live-dispatch-smoke-20260712-v8-outcome-answer-key-needs-rerun.json`.
It proves harness-contract pressure, not negative skill outcome.

The exact-merged-tree v9 smoke also completed all four turns. Its aided arm
selected and fully read `aoa-eval-select`, ran the independent fixture probe,
and correctly reported missing target-repository evidence. Its structured arm
accepted official `aoa-eval-apply` input and completed the probe, but reported
the equivalent `aoa-eval` root plus `aoa-eval-apply` child hierarchy; v9 let
that report override native dispatch and labeled `dispatch_policy_gap`. The
immutable receipt
`aoa-skill-live-dispatch-smoke-20260712-v9-child-route-native-dispatch-needs-rerun.json`
is harness evidence only. V10 replay yields route `+1`, trajectory `+1`,
procedure-disposition `0` with both reports correct, and no observable outcome
score. The exact-merged v10 attempts are retained below.

The first exact-merged-tree v10 attempt stopped the aided arm on budget
exhaustion after broad hidden fixture enumeration and before final output or a
pair. An unchanged repeat completed the implicit pair, recorded candidate
positive route lift plus a `trajectory_break` for `aoa-eval-local-need`, then
stopped the explicit root arm after broad listing and tree hashing consumed the
cap. Both immutable public receipts are `needs-rerun` harness evidence. V11
adds an explicit bounded inventory contract and requires another exact-merged
smoke before interpreting that trajectory observation or widening. Read-only
v11 replay finds broad-command counts `2` in the first aided arm and `2/2/4`
across aided/control/root in the repeat; replay validates the grader and does
not rewrite either v10 receipt.

The fresh exact-merged-tree v11 smoke completed four of four arms. Every arm
stayed inside the fixture, emitted zero broad inventory commands, passed the
independent fixture probe, and had no failure class. The implicit pair records
route `+1`, source-locked selected-child trajectory `+1`, and
procedure-disposition `0` with both arms correct; objective outcome remains
unscored because the fixture exposes none. The manual root selected
`aoa-eval-apply`, and the structured arm accepted official `aoa-eval-apply`
input, with both matching their bounded contracts. The public reviewed receipt
is candidate evidence, not a central verdict, family-wide claim, or permission
to widen before pilot coverage reaches 11/11 procedure and 11/11 outcome.

The next adaptive return comes from owner-contract comparison rather than a
failed v11 arm. The accepted local-suite execution contract requires
`aoa-eval-apply` to JIT-revalidate a selected `*.suite.json`, invoke only its
typed runner, capture environment posture, and write a private source-linked
receipt; readiness and MCP remain inspect-only. It also requires `aoa-eval` to
separate live dirty-workspace packets from exact-source validation. Those skill
changes alter the source lock, so the reviewed smoke remains historical
candidate evidence and a fresh exact-merged v11 smoke is required before pilot
widening.

That required smoke completed all four arms with clean prompt, filesystem,
inventory, fixture, transport, and owner-boundary evidence. Route lift remained
`+1`, but the aided arm selected and fully read `aoa-eval-local-need` while
target-repository fit was still unknown; the source contract requires
`aoa-eval-select`. Selected-child trajectory lift is therefore `0` with both
arms incorrect, procedure-disposition lift is `0` with both reports correct,
and objective outcome remains unscored. The reviewed public receipt is
`aoa-skill-live-dispatch-smoke-20260712-v11-reviewed-local-need-trajectory-break.json`.
This is a valid skill-route candidate, not a harness rerun condition. Return to
selection precedence, preserve the receipt unchanged, and repeat the exact
smoke before pilot widening.

The fresh exact-merged rerun after that repair also completed all four arms.
The aided root selected and fully read `aoa-eval-select`; control selected no
repo skill. Route and selected-child trajectory lift are each `+1`, both
implicit arms correctly report `blocked_missing_input`, procedure-disposition
lift is `0` with both correct, and objective outcome remains unscored. No arm
has a failure class, external read, or broad inventory command. The reviewed
public receipt is
`aoa-skill-live-dispatch-smoke-20260712-v11-reviewed-select-precedence-lift.json`.
This closes the selection-precedence return as bounded candidate evidence;
pilot widening remains blocked by 1/11 procedure and 0/11 outcome coverage.

V12 now source-locks the first owner-observable outcome contract for
`collision-42`. It asks for the next justified eval-owner action, not external
repository completion, and binds the answer to a one-attempt transport event.
Deterministic tests prove the answer is absent from the plan lock and that
validator inspection or retry invalidates causal measurement. A fresh
exact-merged v12 smoke is required before expanding the same contract shape to
the remaining ten pilot cases. Pilot coverage is now 1/11 on both required
axes.

That exact-merged v12 smoke completed four of four arms with no failure class.
Both implicit arms used exactly one outcome command, passed the contract-bound
sentinel, and did not inspect or retry the validator. The aided arm retained
route lift `+1` and selected-child trajectory lift `+1`; procedure disposition
and owner-action outcome were correct in both arms, producing `0` lift for each
dimension. The reviewed public receipt is
`aoa-skill-live-dispatch-smoke-20260712-v12-reviewed-owner-action-no-lift.json`.
This validates the outcome seam, not skill-specific outcome lift or pilot
authorization; expand the reviewed contract shape to the remaining ten cases
before pilot execution.

That expansion is now source-authored for all eleven implicit pilot cases. The
three underspecified direct invoke routes stop at `blocked_missing_input`; the
two rooted routes additionally lock their first child and complete child read;
the six explicit-only routes remain `not_applicable` under implicit pressure.
Each case also has a separate sorted three-choice owner-action contract whose
answer is hidden behind the same one-attempt validator boundary. Deterministic
tests now report 11/11 on both axes. This authorizes only the next guarded step:
review and merge the exact source, then plan and run `pilot13` with its printed
operator tokens and host gates.

The first exact-merged `pilot13` then completed all 30 turns without transport,
prompt, filesystem, inventory, fixture, outcome-validator, or authority
failure. All eleven owner-action pairs were correct in both arms. Review still
marks the receipt `needs-rerun`: `collision-33`, `collision-09`, and
`collision-14` expose manual-policy collision pressure, while `collision-38`,
ambient manual controls, manual no-dispatch disposition, and the
`abyss-safe-infra-change` to `aoa-safe-infra-change` report expose contract or
harness returns that must be corrected before skill conclusions or another
full pilot. Preserve the receipt and repeat only the smallest affected cases
after each repair.

Source reread retains `collision-38` as a root-to-`aoa-decision-find` handoff
candidate: it is not a grader correction. V13 repairs the other demonstrated
harness returns. Manual failure labels apply only to aided arms; no-dispatch
manual/do-not-use prompts require `not_applicable`; and a separate
`structured_report_child_hierarchies` source map accepts an exact target plus
its declared base child. Replay of the immutable v12 private evidence removes
three control-side labels and the Abyss structured report miss, leaving seven
aided return candidates. Replay validates v13 grading and does not alter the
reviewed v12 receipt.

The first exact-merged `pilot13-returns` attempt stopped after six turns on a
post-start transport timeout. A fresh attempt passed that point and stopped at
14 of 15 on a contradictory Titan control report: no selected skill but
`claims_loaded=true`. Both receipts remain partial `needs-rerun` evidence, and
the final Abyss structured arm is still unobserved. Review additionally found
that the plan/schema cohort addition had not reached the private/public receipt
cohort enums. Close that schema parity with a real private-to-public synthetic
receipt test before interpreting or rerunning the live cohort.

V14 separates the reported selection surface from the target policy. The exact
prompt-visible repo name set determines whether a reported selection belongs
to the treatment; external ambient routes are reported separately and do not
load an explicit-only target. The target-report contract now reaches implicit
arms, defines procedure disposition for the target rather than an ambient
procedure, and requires `claims_loaded=false` when `selected_skill` is null.
Replay of the 14-turn v13 raw evidence changes only two aided classifications,
from dispatch policy gaps to target procedure disposition misses. It leaves all
other failures intact and never alters the reviewed v13 receipt.

The exact-merged v14 run then completes all 15 turns. Every prompt, filesystem,
inventory, fixture, transport, owner-action, and authority gate is clean, and
the previously unobserved Abyss structured arm passes its dispatch, load,
hierarchy, and fixture contracts. The return set contracts to three aided
failures: `collision-38` reads the `aoa-decision` root but does not hand the find
task to `aoa-decision-find`; `collision-09` loads repo-visible
`aoa-change-protocol` for an explicit-only approval-gate classification; and
`collision-14` selects the same generic skill instead of the ATM10 project
overlay. This is a source-repair boundary, not a family verdict: preserve the
receipt, change only those two source skills, and rerun the smallest affected
case set before widening.

The source repair now makes `aoa-decision` fully read exactly one classified
child before graph or source work, and makes prompt-visible
`aoa-change-protocol` defer before loading on approval-only or manual-overlay
tasks. Red-first source and portable-description tests bind both boundaries.
The new `pilot13-skill-returns` cohort carries only the six affected arms and
has private/public receipt schema parity before any live spend.

The exact-merged six-turn execution closes the approval-gate pair and confirms
the decision root-to-find handoff with positive route and trajectory lift. It
also reveals two narrower source returns: `aoa-decision-find` reports
`deferred_owner_boundary` instead of `blocked_missing_input` when every graph
and owner input is absent, while the concrete ATM10 repo-relative prompt still
loads generic `aoa-change-protocol`. The aided decision outcome command is exact
and exits zero, but its command event contains no sentinel output; the harness
correctly leaves outcome verification false. Preserve that observation gap,
repair only the two source boundaries, and rerun before widening.

The red-first second source repair gives the selected decision child the exact
`blocked_missing_input` terminal for an evidence boundary with no graph,
fallback, or owner inputs, and gives the generic change protocol the exact
ATM10 repo-relative do-not-load boundary. Neither the explicit target policies,
the owner-action answer keys, nor the absent-sentinel proof rule changes. The
existing six-turn cohort remains the next source-locked live step.

The exact-merged rerun then clears every aided failure class. `collision-38`
passes route, child trajectory, procedure, and sentinel-verified outcome;
`collision-14` keeps both generic and explicit overlay skills unloaded and
verifies the owner route; `collision-09` remains correct in both arms. Two
control arms execute the exact outcome command once with exit zero but expose
no sentinel bytes. The receipt stays reviewed candidate evidence: source repair
is closed, while explicit observation-gap telemetry remains required before
full-pilot outcome-lift interpretation.

## Safety And Privacy

The plan locks Git head, all portable skill files, generated/config inputs,
profile revision, Codex protocol revision, caps, trial identities, and the
count plus digest of exact external shadowing `SKILL.md` paths. Discovery
resolves user-skill symlinks and locks/disables their canonical target files,
not only the link spelling. The absolute paths stay private. The same canonical
paths are disabled in every CLI, prompt-inspection, and App Server adapter, and
run-time rediscovery must match the confirmation/source lock. Plugin features
are disabled. The exact configured MCP-name set receives its own count/digest
source lock. CLI exec arms isolate it by ignoring user config and must not add
partial MCP tables; prompt inspection and App Server retain user config and
therefore disable every locked id explicitly. Deterministic adapter tests guard
both sides of this transport-specific contract.

These hermetic invocation rules use contract schema
`aoa_codex_app_server_skill_input_contract_v11` and protocol revision
`codex-cli-0.144.1-live-dispatch-evidence-v14`. Retained v1-v13 receipts remain
source-locked to their original protocol and review status and are not upgraded
in place.

Live execution requires `abyss-machine resource launch`, independent storage
and runtime gates, read-only sandboxing, network-disabled policy, concurrency
one, source-locked rollout token limits plus reminder thresholds, and an opaque
private fixture per turn. Read-only shell execution is available only so the
model can expose fixture-local full skill reads and run the independent
`python3 fixture_validator.py` probe; the probe, fixture, and owner stop-lines
do not authorize mutation or external filesystem inspection. All arms use the
same 48k weighted-token ceiling. The
matched implicit pair must remain cap-symmetric: the corrected control can
legitimately select the source-locked ambient session-memory route, whose
required owner reads exceeded the former 28k ceiling. The runner rejects empty,
non-positive, or limit-reaching reminder lists before transport startup.

The source-locked model-output schema must also satisfy the Responses API
strict subset before a plan or run can be produced: the root and nested objects
are closed, every property is required, every property declares an explicit
type or supported union, and arrays declare item schemas.

Raw artifacts stay under
`/srv/abyss-machine/tmp/ai/aoa-skill-live-evals` with directory mode `0700` and
file mode `0600`. Public receipts whitelist fields and reject paths,
credentials, transport/session ids, raw-note fields, or proof/promotion
authority, including an absolute host path embedded inside a longer prose
value. Public canonical skill names are accepted only in their schema-typed
skill-name fields; bare `session-*`, `thread-*`, or `turn-*` identifiers remain
rejected.

## Adaptive Return

Each bounded failure class names an earlier layer to repair: harness,
description/policy, collision family, manual policy, root/child trajectory,
native-load/full-read tooling, fixture execution, selected-procedure
disposition contract, objective-outcome observability,
owner boundary, runtime profile/source lock, reviewed budget, or transport.
`skill_load_gap` returns to
the same case when the exact skill was selected but required native-load or
child/full-read evidence is absent; it must not be mislabeled as a trigger,
trajectory, or procedure defect. `dispatch_policy_gap` is separate: it means the
exact route was available but the model's activation decision violated the
expected implicit, manual, trajectory, or explicit dispatch policy. A
structured model report that misses both the exact direct target and the
source-declared root-child edge is `selection_report_miss`; native
dispatch/load facts remain unchanged. A
wide fixture listing, recursive inventory, or tree hash is
`fixture_inventory_scope_violation` and returns to fixture guidance and command
grading before any cap increase or skill edit. A
zero-return transport with invalid structured output is
`output_contract_invalid`; actual transport failure or timeout remains
`transport_failure`. Budget exhaustion is separate when the source-locked cap
stops the turn before a valid result; a late marker after a valid result does
not hide the result's semantic classification. `trajectory_break` returns an
aided root with the wrong declared child to root/child review;
`procedure_disposition_miss` returns a correct trajectory with a mismatched
model report to the selected procedure and source contract;
`fixture_execution_gap` returns only to the hermetic probe. Absence of an
objective outcome contract remains `not_scored_no_observable_outcome`, not a
failure or inferred score. After repair, repeat smoke or the smallest affected
adjacent family before widening again. If a later observation exposes
an ambiguous fixture or grader, return to the harness and invalidate affected
downstream interpretations before changing a skill.

Filesystem-scope contamination and internal inventory-scope violation precede
budget classification: once a model command leaves the fixture or broadly
enumerates it, later token exhaustion cannot make that arm evaluable or justify
a cap increase.

Pair scoring is defined only when both implicit arms produced evaluable
dispatch evidence. Output-contract invalidity, transport failure, budget
exhaustion, runtime-profile drift, or owner-boundary safety violation on either
side emits no lift score.
Prompt/context contamination remains visible as a `contaminated` pair, but pair
construction never rewrites either arm's failure history.
