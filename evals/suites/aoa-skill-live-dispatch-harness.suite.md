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
| `full-collision-core-engineering` | 16 | collisions 01-08 with three regression anchors and five new contracts | medium |
| `full-collision-core-engineering-returns` | 4 | paired fixture-output return for collisions 01-02 | medium |
| `full-collision-core-engineering-outcome-returns` | 4 | paired owner-action output return for collisions 05-06 | medium |
| `full-collision-safety-overlays` | 22 | collisions 09-19 | medium |
| `full-collision-session-growth` | 28 | collisions 20-33 | medium |
| `full-collision-session-growth-returns` | 8 | paired hidden-manual non-activation and ambient-classification return for collisions 21, 22, 25, and 33 | medium |
| `full-collision-authority-routing` | 22 | collisions 34-43 plus artifact-trust collision 49 | medium |
| `full-collision-authority-routing-returns` | 6 | paired parent/child observability return for collisions 39-41 | medium |
| `full-collision-authority-routing-procedure-returns` | 4 | paired decision-create/correct terminal return for collisions 40-41 | medium |
| `full-collision-eval-children` | 10 | collisions 44-48 | medium |
| `coverage-closure-core-implicit` | 4 | ADR and memo-writeback implicit reachability | medium |
| `coverage-closure-titan-implicit-a` | 16 | Titan implicit cases 01-08 | medium |
| `coverage-closure-titan-implicit-b` | 14 | Titan implicit cases 09-15 | medium |
| `coverage-closure-root-trajectories` | 8 | all decision/eval root-child trajectories | medium |
| `coverage-closure-structured-core` | 30 | all non-Titan non-invoke structured routes | medium |
| `coverage-closure-structured-titan` | 15 | all Titan structured routes | medium |

Every cohort beyond smoke currently requires a second exact high-cost token,
as declared by its source plan rather than inferred from its name. Widen only
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

V15 adds that telemetry without weakening outcome proof. A per-arm gap requires
the exact single attempt, successful exit, validator non-inspection, and missing
sentinel together. Matched pairs publish aided/control gap flags, one bounded
gap class, and `outcome_lift_observation_clean`; the underlying outcome match
stays false. Read-only v14 projection labels the two affected controls
`control_only` and leaves `collision-09` clean. Historical public receipts are
not rewritten, and no new skill failure class is introduced.

The exact-merged v15 full pilot then completes 30/30 turns and eleven pairs
with no failure class. Five pairs show positive route and procedure lift, and
the decision plus eval roots also show positive full-child trajectory lift.
Six route/procedure pairs are no-lift-both-correct. Seven outcome pairs are
observation-clean and correct in both arms; two `control_only` and two
`aided_only` gaps qualify the remaining apparent outcome lift. This is reviewed
candidate evidence, not an aggregate family score. The 98-turn full-collision
and 87-turn coverage-closure plans remain declared-only inventory parents;
live widening uses their contract-gated child waves rather than either parent.

V16 turns that partition into a machine contract. Five collision waves and six
coverage-closure waves are disjoint and together reproduce every parent trial
identity. A wave must require both implicit contract axes, require the second
confirmation, remain at or below 30 turns and 512 MiB, and use light or medium
host class. Missing implicit contracts block before preflight. The first
runnable widening, `full-collision-core-engineering`, covers collisions 01-08
with all eight procedure and owner-action contracts present; the five new
answer keys request the concrete source evidence needed by property, core
logic, port/adapter, TDD, and contract-test procedures rather than fabricating
work inside the hermetic fixture.

The first exact-merged v16 core wave completes all sixteen turns. Every aided
arm gains route and procedure correctness; six outcomes are observation-clean
and correct in both arms. Three fixture probes (`collision-01` control and both
`collision-02` arms) are observed once and exit zero but expose zero output
bytes, while the other thirteen expose the valid 234-byte sentinel payload.
Those arms retain `fixture_execution_gap`. `collision-05` and `collision-06`
also have opposite single-arm outcome observation gaps, so neither raw outcome
contrast is stable. Preserve the full receipt as `needs-rerun` and repeat only
both arms of `collision-01` and `collision-02` through the four-turn return
cohort; do not change skill source or weaken either sentinel contract.

The exact-merged fixture return then completes all four arms without a failure
class. Every fixture and owner-action command is observed once, succeeds,
exposes the required sentinel, and verifies. Both pairs retain positive aided
route and procedure lift with observation-clean, both-correct outcomes. This
closes the fixture return but does not retroactively rewrite the first receipt.
Its separate `collision-05` and `collision-06` owner-action observation gaps
remain unclean, so `full-collision-core-engineering-outcome-returns` repeats
only both arms of those two cases before the next collision wave opens.

The exact-merged outcome return then completes all four `collision-05` and
`collision-06` arms without a failure class or output gap. Every fixture and
owner-action command is observed once, succeeds, exposes its sentinel, and
verifies; both pairs retain positive aided route and procedure lift with
observation-clean, both-correct outcomes. Together with the clean fixture
return, every outstanding observation gap from the first core wave now has an
exact paired clean return. The core wave closes as evidence-complete candidate
evidence, while proof/promotion authority stays false. At that checkpoint the
safety-overlay wave remained blocked on incomplete source-authored contracts.

The safety-overlay source pass closes that next design gate. Both arms of
collisions 09-19 now have 11/11 procedure and 11/11 owner-action contracts.
Manual risk and project-overlay cases preserve `not_applicable` plus a visible
owner route; generic base cases 15 and 17 use `blocked_missing_input` for the
absent owner repository surfaces. Six newly referenced skill files enter the
source lock, and collision-14 rationale now matches its canonical
`explicit-preferred` mode while preserving the deliberate manual overlay
boundary. The focused synthetic cohort completes 22/22 and validates both
receipt schemas. This is contract readiness only; no safety-overlay live
receipt exists yet, and proof/promotion authority remains false.

The subsequent exact-merged safety-overlay execution completes all 22 arms and
11 pairs with zero failure classes or observation gaps. The nine manual pairs
are correct in both arms without skill loading or lift, preserving their owner
boundaries. The generic `collision-15` and `collision-17` pairs select and fully
read their intended base skills, report `blocked_missing_input`, and gain
positive aided route plus procedure lift. Every fixture and owner-action probe
is observed once, succeeds, exposes its sentinel, and verifies. Preserve the
public receipt as reviewed candidate evidence with proof/promotion false. At
that checkpoint the session-growth wave remained blocked at 2/14 contracts on
both implicit axes.

The session-growth source pass closes the next deterministic gate. Both arms
of collisions 20-33 now have 14/14 procedure and 14/14 owner-action contracts.
Cases 20-27, 29, 31, and 33 preserve their explicit or deliberately manual
activation boundary as `not_applicable`; generic invoke cases 28, 30, and 32
stop at `blocked_missing_input` for absent owner repositories, documents,
diffs, and checks. Nine newly referenced skill files enter the source lock.

The focused synthetic expansion completes 28/28 and validates private and
public schemas. It also returns to the runner after finding that the generic
transport-id regex rejected the typed plan slug
`full-collision-session-growth`. Typed cohort slugs now permit interior
`session` wording but still reject leading transport-shaped ids such as
`session-deadbeef`; untyped strings retain the stronger generic scan. This is
contract readiness only. No live session-growth conclusion exists before the
exact-merged source, runtime parity, host gates, both confirmations, and a
reviewed candidate receipt.

The first exact-merged session-growth run completes all 28 arms and 14 pairs.
Every fixture and owner-action probe is observed exactly once, succeeds,
exposes its sentinel, and verifies; all outcome pairs are observation-clean and
correct in both arms. Prompt visibility, filesystem scope, inventory, owner,
proof, promotion, and post-run host boundaries remain clean.

The wave still remains `needs-rerun`. In collisions 21, 22, and 25 the aided
arm leaves the explicit-only target unread but selects ambient
`aoa-eval`/`aoa-eval-session-mining`, then misreports the target-facing route
as `invoke`. Collision 33 keeps `aoa-summon` manual and its procedure
`not_applicable`, but an ambient `aoa-change-protocol` selection reaches the
competing-skill classifier before the correct manual target contract. These
are shared prompt-visible invocation-policy and measurement-ordering gaps, not
evidence to rewrite the four target skills independently. Preserve the full
receipt and repeat only both arms of cases 21, 22, 25, and 33 after a red-first
repair.

V17 repairs the shared causes before that return. The portable exporter makes
activation law prompt-visible in the description itself: 43 `manual` entries
forbid implicit load, two `suggest` entries may be recommended but not loaded,
and both classes still permit an explicit invocation or source-authorized
parent selection. The 12 `invoke` descriptions keep their authored text. The
failure classifier also evaluates a manual target by its target-facing report
and objective read evidence rather than treating every repo-visible ambient
selection as a competing win. The paired
`full-collision-session-growth-returns` cohort contains exactly eight arms for
cases 21, 22, 25, and 33 and retains their existing procedure and owner-action
contracts.

Exact-merged prompt-input inspection subsequently revises the first v17 causal
hypothesis. Native Codex includes only skills with
`allow_implicit_invocation=true` in the implicit Available-skills inventory;
all four return targets are manual and absent in both arms. V18 therefore
separates raw report fields from score eligibility. For an unseen manual target,
`route_decision` and procedure disposition remain reviewable raw observations
but neither can establish target-specific routing or procedure adherence.
Objective full-read/native-load evidence remains the strict non-activation
guard, fixture and owner-outcome contracts remain scored, and an exact target
claim plus load or any objective target read still fails. The return packet now
states four procedure contracts, zero route/procedure-score-eligible pairs,
four manual non-activation guards, and four owner-outcome pairs. Explicit
reachability remains in `coverage-closure-structured-core`.

The exact-merged v18 return completes all eight arms and four pairs with no
failure class, external filesystem access, broad fixture inventory, or outcome
observation gap. All four hidden targets stay prompt-invisible and unread in
both arms; every manual non-activation, fixture-execution, and owner-outcome
contract matches. Route and procedure effects remain
`not_scored_target_not_prompt_visible`, while the objective guard is
`no_lift_both_correct`. Preserve the result as the reviewed candidate receipt
[`aoa-skill-live-dispatch-full-collision-session-growth-returns-20260713-v18-reviewed-hidden-manual-non-activation.json`](../reports/aoa-skill-live-dispatch-full-collision-session-growth-returns-20260713-v18-reviewed-hidden-manual-non-activation.json),
with proof and promotion authority false. The next semantic wave is
`full-collision-authority-routing`; this result does not pre-authorize it or
substitute for its own preflight.

The authority-routing source pass closes that preflight design gate. The wave
contains both arms of collisions 34-43 plus 49: 22 turns and 11 pairs. Existing
decision-root, eval-root, and artifact-trust anchors 38, 42, and 49 stay
unchanged. New contracts make prompt-visible cases 34, 36, 37, and 43 stop at
`blocked_missing_input`; hidden manual cases 35, 39, 40, and 41 remain
`not_applicable` and receive objective non-activation guards. The decision
create/correct child sources newly enter the confirmation lock.

The packet is now complete at 11/11 procedure and 11/11 owner-outcome
contracts, with six route/procedure-score-eligible pairs and five hidden-manual
pairs. The focused deterministic execution completes 22/22 and validates both
receipt schemas. This is source-contract readiness only. Exact merge, runtime
parity, host admission, both confirmation tokens, and a reviewed live receipt
remain mandatory; proof and promotion authority stay false.

The first exact-merged live execution completes all 22 arms. Fixture and
owner-action contracts match in every arm; filesystem scope, inventory scope,
and outcome observation stay clean. All six prompt-visible routes gain positive
aided route and procedure lift. Preserve the reviewed v18 receipt as
[`aoa-skill-live-dispatch-full-collision-authority-routing-20260713-v18-reviewed-parent-trajectory-observability-needs-rerun.json`](../reports/aoa-skill-live-dispatch-full-collision-authority-routing-20260713-v18-reviewed-parent-trajectory-observability-needs-rerun.json).

Its two `manual_activation_leak` labels are not sufficient evidence of direct
manual activation. Cases 39 and 41 select the prompt-visible decision root and
read the exact child already declared by `root_child_trajectories`; the
implicit trial fails to carry that parent contract into v18 grading. After a
red-first observability repair, repeat only both arms of cases 39-41. That
return must still expose the case-40 missing child read and the case-41 terminal
disposition rather than automatically converting parent authorization into a
pass.

V19 completes that red-first repair without changing the decision skills. For
implicit cases declared in `root_child_trajectories`, the prompt-visible root is
now the scored dispatch target and its one source-declared hidden child is a
separate trajectory/procedure obligation. A parent-selected child read can no
longer become `manual_activation_leak`; a missing full child read remains
`skill_load_gap`, a wrong or absent child report remains `trajectory_break`, and
an incorrect terminal remains `procedure_disposition_miss`. The authority wave
therefore has nine scored route/procedure pairs and only two independent hidden
manual guards. The new
`full-collision-authority-routing-returns` cohort contains exactly both arms of
cases 39-41, for six turns. Deterministic replay and both receipt schemas are
green. The suite freshness sidecar now tracks every declared decision/eval
parent and child source so the future eval-child wave cannot inherit stale
authored guidance. Exact merge, installed runtime parity, host admission, both
confirmation tokens, and a reviewed live return remain mandatory.

The exact-merged v19 return now completes all six arms and all three pairs
without an early stop, prompt/fixture contamination, external access, broad
inventory, transport failure, or outcome-observation gap. Every aided arm
selects prompt-visible `aoa-decision`, fully reads the one declared child, and
gains positive route and trajectory lift. Case 39 also reaches the expected
`blocked_missing_input` terminal. Cases 40 and 41 instead report
`deferred_owner_boundary` after correctly selecting and reading
`aoa-decision-create` or `aoa-decision-correct`; both are
`procedure_disposition_miss`. Preserve the candidate-only result as
[`aoa-skill-live-dispatch-full-collision-authority-routing-returns-20260713-v19-reviewed-procedure-returns-needs-rerun.json`](../reports/aoa-skill-live-dispatch-full-collision-authority-routing-returns-20260713-v19-reviewed-procedure-returns-needs-rerun.json).
Repair the two child missing-input terminals red-first and repeat only both arms
of cases 40-41. The receipt does not authorize proof, promotion, or the next
eval-child wave.

The bounded source repair now makes that missing-input terminal explicit in
both `aoa-decision-create` and `aoa-decision-correct`: once the parent has
classified the child route, unavailable required context inside the permitted
evidence boundary ends as `blocked_missing_input`, never
`deferred_owner_boundary`. The same rule is present in the portable
prompt-visible descriptions. The source snapshot now locks the authored
`config/portable_skill_overrides.json` as well as its generated `.agents/skills`
projection, and the freshness sidecar tracks both child sources plus that
override. Its typed live-harness entrypoint now exercises the
source-to-description contract directly. The four-turn
`full-collision-authority-routing-procedure-returns` cohort repeats only both
arms of cases 40-41. Deterministic validation is necessary but does not claim a
live correction; exact merge, runtime parity, host admission, both
confirmations, and reviewed execution remain mandatory before widening.

The exact-merged four-turn return now completes all four arms and both pairs
without a failure class, early stop, prompt/fixture contamination, external
access, broad inventory, or outcome-observation gap. Both aided arms select
prompt-visible `aoa-decision`, fully read the exact create/correct child, and
report `blocked_missing_input`; both controls remain correctly
`not_applicable`. Route, child trajectory, and procedure disposition each gain
positive aided lift, while both owner outcomes are observation-clean and
correct in both arms. Preserve the reviewed candidate receipt as
[`aoa-skill-live-dispatch-full-collision-authority-routing-procedure-returns-20260713-v19-reviewed-clean.json`](../reports/aoa-skill-live-dispatch-full-collision-authority-routing-procedure-returns-20260713-v19-reviewed-clean.json).
This closes the authority procedure return without granting proof or promotion.
The next declared wave, `full-collision-eval-children`, is still only a plan:
its five pairs are route-score-eligible but have 0/5 procedure and 0/5 owner
outcome contracts, so live execution remains unauthorized until that
source-owned design gate is closed.

The eval-child source pass now closes that deterministic design gate without
changing protocol v19. Each hidden child has an explicit parent-classified
missing-input terminal in source and portable description: select lacks target
eval surfaces; apply lacks the exact selected command and source context;
local-need lacks the owned port/schema and packet evidence; design lacks the
explicit invariant and local owner path; session-mining lacks trigger classes,
provider freshness, and the target owner map. Each child must be fully read and
then stop at `blocked_missing_input`, never substitute the fixture probe,
invent a write/ref, or relabel missing input as `deferred_owner_boundary`.
Cases 44-48 now have 5/5 source-locked procedure contracts and 5/5 independent
owner-action contracts. The plan confirmation additionally locks all five child
sources rather than only root/select/apply. The existing ten-turn
`full-collision-eval-children` cohort is deterministic-contract-complete, but
exact merge, installed runtime parity, host admission, both confirmations, and
reviewed live evidence remain mandatory before any family conclusion.

The first exact-merged/runtime-parity execution completed all ten turns but did
not close the wave. Preserve the reviewed candidate-only return as
[`aoa-skill-live-dispatch-full-collision-eval-children-20260713-v19-needs-rerun.json`](../reports/aoa-skill-live-dispatch-full-collision-eval-children-20260713-v19-needs-rerun.json).
All five aided arms selected and fully read their intended child and reported
the expected `blocked_missing_input` procedure. Cases 47-48 nevertheless read
only the first 240 lines of the prompt-visible eval root, so both retain
`skill_load_gap`; case 45 chose the wrong single objective candidate even
though its final blocked next step requested the correct selected-command
context. The bounded source return now makes a current root read to EOF
explicit after every prefix-limited read and makes the exact apply
command/source-context request the mandatory next owner action while forbidding
the fixture probe as the selected eval. Exact merge, runtime parity, host
admission, and a full ten-turn rerun remain required. Proof and promotion stay
false.

The same source return exposed a generated-lane dependency: portable export
updated the apply description after Skill Intelligence had already been built.
The owner lane manifest now refreshes or checks the catalog after portable
export in generated, export, and release routes, and both Skill Intelligence
registries are blocking drift paths. This prevents a portable-only skill repair
from appearing export-clean while its model-facing intelligence projection is
stale.

The complete exact-merge rerun closes the earlier apply owner-action miss and
both root-prefix gaps, but still does not close the wave. Preserve the second
reviewed candidate-only return as
[`aoa-skill-live-dispatch-full-collision-eval-children-20260713-v19-second-needs-rerun.json`](../reports/aoa-skill-live-dispatch-full-collision-eval-children-20260713-v19-second-needs-rerun.json).
Cases 44-46 and 48 are clean across root load, intended child load, procedure,
and owner outcome. Case 47 reads the root to EOF yet routes the explicit bounded
suite design request to select, then fully reads the wrong child. The root now
gives explicit design intent precedence over general missing-input selection;
missing invariant or target inputs must block inside design rather than change
the route. Exact merge, runtime parity, host admission, and another full
ten-turn rerun remain mandatory. Proof and promotion stay false.

The exact-merged rerun after that return closes the wave. Preserve the reviewed
candidate-only result as
[`aoa-skill-live-dispatch-full-collision-eval-children-20260713-v19-reviewed.json`](../reports/aoa-skill-live-dispatch-full-collision-eval-children-20260713-v19-reviewed.json).
All ten turns complete without a failure class. Every aided arm selects the
eval root and intended child, reads both completely, and matches dispatch,
load, trajectory, `blocked_missing_input` procedure, owner-boundary, fixture,
and owner-outcome contracts. All five pairs have positive route, trajectory,
and procedure lift; outcomes are observation-clean. This closes the bounded
full-collision eval-child wave, not central proof or promotion. The next live
boundary is the coverage-closure partition. Its source audit now closes all 17
implicit pairs at 17/17 procedure and 17/17 owner-action coverage. One ADR pair
is route/procedure-score eligible; memo writeback and all fifteen Titan pairs
remain deliberate/manual non-activation guards. The source snapshot locks every
referenced owner skill, and synthetic confirmed execution covers all 34 paired
turns. This is deterministic readiness rather than live evidence. After exact
merge, runtime parity, host admission, and fresh confirmation tokens, execute
the four-turn `coverage-closure-core-implicit` wave first and review it before
either Titan child wave.

## Safety And Privacy

The plan locks Git head, authored portable overrides, all portable skill files,
generated/config inputs,
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
`aoa_codex_app_server_skill_input_contract_v14` and protocol revision
`codex-cli-0.144.1-live-dispatch-evidence-v19`. Retained v1-v18 receipts remain
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
