# Live Eval Runners

This directory holds owner-local runner implementations for the `aoa-skills`
eval port. The runners may produce candidate evidence; they do not own central
verdicts, scoring, regression truth, proof acceptance, or promotion.

## Live Skill Dispatch

`run_live_skill_dispatch.py` separates two layers:

- deterministic source-contract validation, exercised by
  `tests/test_live_skill_dispatch_harness.py`;
- explicitly confirmed live cohorts, whose raw evidence stays below the
  source-locked host-private root.

The default action is a read-only plan. A live run additionally requires the
exact confirmation token printed by that plan. The source-locked cohort field
`second_confirmation_required` decides whether the printed high-cost token is
also mandatory; only `smoke` currently sets it false.
The pilot plan publishes selected-procedure contract coverage and objective
outcome-observation coverage separately. It remains executable only at 11 of
11 for both; the current corpus now has 11/11 procedure contracts and 11/11
objective outcomes. This makes planning eligible to print the two exact live
confirmation tokens, but does not bypass storage, resource, runtime, prompt,
shadow, or operator-confirmation gates. Planning eligibility alone never proves
a run; the first reviewed `pilot13` result is described below.
The 15-turn `pilot13-returns` cohort is the smallest exact rerun of its seven
remaining implicit pairs plus the corrected Abyss structured-report case; it
does not repeat already-clean pilot arms.
The 6-turn `pilot13-skill-returns` cohort narrows the next exact-source run to
the three pairs changed by the v14 skill-source repair: `collision-38`,
`collision-09`, and `collision-14`. It requires complete procedure and outcome
contracts plus the high-cost token and contains no unrelated trajectory or
structured arms.
V16 keeps the two broad cohorts as inventory parents and names eleven bounded
execution waves below them. Runner validation requires disjoint waves whose
trial identities exactly cover each parent, rejects any child wider than 30
turns or 512 MiB, and forbids `declared_only` contract posture on a wave.
The four-turn `full-collision-core-engineering-returns` cohort preserves both
arms of only `collision-01` and `collision-02`, the pairs affected by the first
wave's zero-output fixture observation return.
The separate four-turn `full-collision-core-engineering-outcome-returns`
cohort preserves both arms of only `collision-05` and `collision-06`, whose
first-run owner-action sentinels were observed in opposite single arms.
The procedure source contract lives at
`evals/suites/aoa-skill-live-dispatch-procedures.json`; the separate bounded
owner-action corpus lives at
`evals/suites/aoa-skill-live-dispatch-outcomes.json`.
Smoke marks both dimensions `required`; deleting either contract makes planning
fail before confirmation or preflight.

Planning discovers exact external `SKILL.md` files whose canonical names
shadow the repo export, including canonical targets behind symlinked user-skill
directories. Only their count and deterministic digest enter the
confirmation/source lock; absolute paths remain private. A confirmed run
rediscovers the set and disables those canonical file paths in every CLI, App
Server, and prompt-inspection adapter. Plugin features are disabled. The exact
configured MCP-name inventory is separately count/digest locked. CLI exec arms
use `--ignore-user-config` and must not synthesize otherwise absent MCP tables;
prompt inspection and App Server, which retain the user config needed by those
transports, disable every locked MCP id explicitly.

Before each model turn, the runner calls `codex debug prompt-input` under the
same fixture, skill-shadow, and feature-disable configuration, with the
transport-appropriate MCP isolation described above. The aided fixture must
expose exactly the repo skills with `allow_implicit_invocation: true`
(currently 12 of 57),
while the control must expose zero repo skills. The paired non-repo background
inventory digests must match. Each entry fingerprint binds its model-visible
name, resolved path, and description, so description-only drift is detected. A
mismatch stops before the model turn as `harness_contamination`.

The structured arm has a second pre-turn gate. App Server `skills/list` must
equal the full 57-skill fixture path map, with exactly one enabled path per repo
name, and no configured MCP startup event may appear before `turn/start`. Its
turn follows the
[official App Server skill-invocation contract](https://learn.chatgpt.com/docs/app-server#start-a-turn-invoke-a-skill):
the text begins with the exact `$skill` mention and the adjacent structured
`skill` item carries the same fixture name and path. An accepted official input
is version-locked native-load evidence, distinct from a raw shell full read.
Sending that validated input is transport-owned dispatch evidence; the model's
later direct-target report or exact root-to-child hierarchy declared by
`root_child_trajectories` is retained separately and cannot override the native
dispatch/load facts. A correct child under an unrelated root is not an
equivalent hierarchy report, and a direct target report carrying a conflicting
child is not exact either. Those report-only mismatches are
`selection_report_miss`; they do not rewrite successful native dispatch or load
evidence as `dispatch_policy_gap`.
These rules use contract schema `aoa_codex_app_server_skill_input_contract_v11`
and protocol revision `codex-cli-0.144.1-live-dispatch-evidence-v16`. Retained
v1-v15 receipts stay source-locked to their original protocol and review status;
they are never upgraded in place.

Run the confirmed command only as the child of the plan packet's
`resource_launch_prefix`. The wrapper must produce the expected
`ABYSS_RESOURCE_CLASS`, `ABYSS_RESOURCE_KIND=agent`, and
`abyss-machine-agent-<class>-*.service` cgroup. The runner independently calls
the storage write preflight and checks the exact Codex version before creating
its private run directory.

Every live arm has the same source-locked 48k weighted-token ceiling. In
particular, aided and control arms must remain cap-symmetric even when the
control selects a longer source-locked ambient route; widening only one side
would invalidate paired lift.

The sandbox remains read-only and network-disabled, but the read-only shell
tool is available for evidence-bearing reads and the independent hermetic
fixture probe. Read-only skill-file inspection commands collect load evidence.
All arms run the exact probe `python3 fixture_validator.py`; it proves fixture
executability only and does not define the selected child procedure or external
task outcome. A declared owner-action outcome instead requires exactly one
`python3 outcome_validator.py --candidate <value>` event. Reading, copying,
hashing, importing, reproducing, or retrying that validator contaminates the
measurement; a missing or wrong single choice remains a negative outcome rather
than a transport or procedure failure. V10+ private and public measures name its command, exit, and
sentinel facts only with `fixture_*` fields; the runner accepts historical
`procedure_command_*` fields solely as a read-only replay fallback for retained
v1-v9 receipts. Transport evidence records full `SKILL.md`
reads only from the exact fixture paths with complete source content. One
successful output may contain the whole file, or ordered successful outputs may
continuously cover it; overlapping chunks are allowed, unrelated exact-path
metadata outputs are ignored, and gaps or reverse-only coverage remain
incomplete. Public
measures keep the model's `claims_loaded` self-report, accepted native input,
and raw full-read events separate: the self-report never gates objective load
evidence, the explicit root is natively loaded, any expected or dynamically
selected child still requires a raw read, and the official App Server dual
input natively loads its target.
Every model command remains confined to the fixture root. An observed absolute
host, workspace, session-memory, user-config, other-repository, or
parent-traversal path is `harness_contamination` before budget, dispatch, load,
procedure, or lift interpretation. System executables and `/dev/null` are
tooling exceptions; they do not authorize data reads outside the fixture.
V11 additionally forbids broad in-fixture enumeration, recursive listing, and
tree hashing. `rg --files`, `find`, `tree`, recursive `ls`, `du`, and inventory
pipelines return `fixture_inventory_scope_violation` before a later budget
marker. Exact reads of fixture guidance, the selected root or target, at most
one selected child, and the named validator remain allowed.
Verification requires the same completed exact-command event to carry zero
exit and exactly one `AOA_FIXTURE_VALIDATOR_OK` JSON payload bound to the
current fixture-guidance digest; split success/sentinel events do not pass.

Example planning command:

```bash
python evals/runners/run_live_skill_dispatch.py plan \
  --repo-root . \
  --cohort smoke \
  --model MODEL \
  --effort medium
```

Do not paste raw receipts into Git, issue trackers, or chat. Review them locally
and use the runner's `review` action to create a field-whitelisted public
receipt under `evals/reports/` only after assigning an explicit review status.
Public measures keep prompt visibility, model selection report, transport-owned
structured dispatch, accepted native load, exact reads, route, selected-child
trajectory, fixture execution, model-reported procedure disposition, and
objective outcome posture separate. Each implicit pair reports route lift,
source-locked child-trajectory lift, and source-locked procedure-disposition
report lift as distinct dimensions. `python3 fixture_validator.py` has its own
fixture-execution match. When no owner-action contract exists, pairs keep null
outcome lift with `not_scored_no_observable_outcome`. Under v12, a source-locked
contract may instead score one atomic transport-observed owner choice; neither
generic probe success nor model self-report may fill that gap. A
correct selection without the required native-load or child/full-read evidence
returns `skill_load_gap` to the same case. A wrong activation decision after the
route is available is instead `dispatch_policy_gap`. A normal zero-return
transport whose final structured result violates the bounded output schema is
`output_contract_invalid`, not `transport_failure`; none of these classes is
proof of a skill defect or completed work.

A caught CLI or App Server transport exception preserves its observed elapsed
milliseconds plus any partial stdout/stderr; recoverable JSONL events and usage
continue through turn-start, budget, filesystem-scope, and failure-precedence
grading. After the private receipt is safely written, the `run` command
returns exit 1 with `status=stopped_early` and the bounded stop reason when the
cohort is incomplete. A complete cohort still returns exit 0 even when it
records negative skill evidence; process status reports measurement completeness,
not model quality.

All scored lift dimensions are omitted when either arm has an output-contract,
transport, budget, runtime, or owner-boundary safety failure. Contamination
remains an explicit pair outcome but never rewrites either arm's recorded
classification. A source-locked aided route with the wrong declared child
returns `trajectory_break`; a correct child whose disposition report misses the
source contract returns `procedure_disposition_miss`; a missing probe returns
`fixture_execution_gap` to harness repair rather than child-skill repair.
Public review also
walks every string value and rejects an absolute host path even when it is
embedded in prose, in addition to credential and transport-id leakage.

The 2026-07-11 complete post-classifier smoke is retained only as a
`needs-rerun` harness diagnosis. User-skill prompt contamination, a disabled
full-read/shell path, and an ambiguous route/procedure grader make its former
trigger, trajectory, procedure, and lift interpretations non-actionable.

The exact-merged-tree v3 rerun after the `aoa-eval` child-handoff repair is also
retained as `needs-rerun` harness evidence. Its first three arms exposed that
the v3 grader still treated `claims_loaded` as load proof, did not bind an
implicitly selected child to its required read, classified a zero-return
output-contract failure as transport failure, and let the phrase "one command"
obscure that read-only inspection commands were allowed. It supports no pair,
lift, or skill-effect conclusion and required the now-retained v4 rerun.

The exact-merged-tree v4 rerun is retained as a second `needs-rerun` harness
receipt. Its aided arm completed objective root and dynamic-child reads, but
the control then read a complete `aoa-eval` source file from an external
canonical checkout before exhausting its budget. The historical v4 grader
reported only `budget_exhausted`; local raw review established that filesystem
scope contamination occurred earlier. It supports no pair, lift, skill-effect,
or family conclusion. The v5 fixture-scope rerun must pass before widening.

The exact-merged-tree v5 rerun fixed filesystem isolation and completed all four
arms, but its aided root read arrived as two ordered exact-path chunks. The v5
grader required one command output to contain the entire root source and
therefore recorded a false `skill_load_gap` and `no_lift_both_incorrect`. Its
public receipt remains immutable `needs-rerun` evidence; raw replay under v6 is
a harness regression check, not a replacement live result. Repeat the smoke on
an exact merged v6 tree before widening to `pilot13`.

The exact-merged-tree v6 rerun passed prompt and fixture-scope gates, then its
first CLI transport timed out at the 180-second cap before any turn event,
output, usage, or pair. The historical v6 runner wrote a correct private
stopped-early receipt but returned process exit 0, so the host wrapper reported
success for an incomplete cohort. The public receipt remains immutable
`needs-rerun` evidence. V7 repairs duration and process-status observability;
the same smoke must wait for runtime availability and then run on an exact
merged v7 tree before `pilot13`.

The exact-merged-tree v7 smoke then completed all four arms and recorded a
positive generic pair lift. Its v7 implementation derived that field solely
from route-contract correctness, even though the implicit arms reported
different deflection dispositions and neither reported completion. The reviewed
public receipt therefore preserves v7 as positive route-contract evidence only.
V8 removes the ambiguous generic fields from new pairs, source-locks the smoke
outcome contract before planning, and requires a fresh exact-merged smoke before
`pilot13`.

The exact-merged v8 smoke completed four of four arms and reported positive
route lift but negative outcome lift. V9 first corrected the whole-task versus
downstream-procedure wording, but the next live run showed that this still
treated the fixture probe as if it were the selected child procedure. V8's
aided arm selected `aoa-eval-apply`; source review of `collision-42` instead
requires `aoa-eval-select` before any apply/local-need/design decision. The v8
receipt therefore remains immutable `needs-rerun` harness evidence.

The exact-merged v9 smoke also completed four of four arms. It selected and
fully read `aoa-eval-select`, correctly reported missing target-repository
evidence, and retained positive route lift. Its structured arm accepted the
official `aoa-eval-apply` input and completed the fixture probe but reported the
equivalent root-to-child hierarchy, which v9 incorrectly allowed model
self-report to override as `dispatch_policy_gap`. V10 replay separates these
contexts: v9 becomes route `+1`, trajectory `+1`, procedure-disposition `0`
with both reports correct, and objective outcome unscored. The public v9
receipt remains historical `needs-rerun`; replay is grader validation, not a
replacement live result or proof.

The first exact-merged v10 smoke stopped its aided arm on budget exhaustion
after broad hidden fixture enumeration and before any final output or pair. An
unchanged repeat completed the implicit pair, recorded a candidate
`trajectory_break` for `aoa-eval-local-need`, then stopped the explicit root
arm after broad listing and tree hashing consumed the cap. Both receipts are
immutable `needs-rerun` harness evidence. V11 makes inventory breadth explicit
in prompt guidance and command-event grading before another exact-merged smoke;
neither incomplete v10 run authorizes a skill edit or pilot widening.

The exact-merged v11 smoke completed all four arms with zero broad inventory
commands and no failures. Its reviewed pair separates positive route lift
`+1`, positive source-locked selected-child trajectory lift `+1`, correct
procedure disposition in both arms (`0` lift), and an unavailable objective
outcome. The manual root and structured App Server arms also matched their
dispatch, load, fixture-execution, and boundary contracts. This closes the
inventory-harness return only; pilot execution remains blocked until the
source corpus supplies 11/11 procedure contracts and 11/11 owner-bound outcome
observations.

After those gates closed, the first exact-merged 30-turn `pilot13` completed
without transport, prompt, filesystem, inventory, fixture, owner-action, or
authority contamination. All eleven bounded outcomes were correct in both
arms. Its reviewed public receipt is still `needs-rerun`: the run exposed
manual-policy collision candidates and, separately, contract/grader gaps for
decision graph-first routing, ambient control routes, manual no-dispatch
disposition, and an Abyss overlay-to-base hierarchy. Treat those as distinct
adaptive returns; do not collapse them into one pilot score or edit a skill
until the harness-side returns are removed.

V13 makes those harness returns explicit. Manual-policy failure classes apply
to the aided arm, while an ambient non-target control route remains available
for pair contrast without being called a target activation leak. No-dispatch
manual or do-not-use outputs are prompted to report `not_applicable`. A new
source-locked structured child-hierarchy map accepts target-plus-declared-base
reports separately from the existing declared-root-plus-target shape. Replay
of v12 raw evidence under v13 is grader validation only and never rewrites the
reviewed public receipt.

The first two exact-merged `pilot13-returns` executions are intentionally
preserved as partial `needs-rerun` receipts. One stopped on a non-repeated
post-start timeout after 6 turns; the fresh run reached 14 turns and then
failed the output contract on `selected_skill=null` plus
`claims_loaded=true`. Review also found that the receipt schemas had not added
the new cohort enum. Private/public schema parity and an end-to-end synthetic
receipt test are required before any further live review or grader revision.

V14 classifies `selected_skill` against the exact repo-visible prompt surface.
An external ambient route can coexist with a correct manual target decision;
it does not become repo-treatment activation. A prompt-visible repo selection
still fails the manual policy when invoked or claimed loaded. The target-report
contract is now appended to implicit prompts as well as root/structured arms:
route decision and procedure disposition are target-specific, ambient work does
not make the target procedure blocked, and null selection requires
`claims_loaded=false`. Read-only replay of the 14-turn v13 receipt moves two
ambient aided arms from dispatch-policy failure to procedure-disposition
failure and changes nothing else.

The fresh exact-merged v14 execution completes all 15 turns and seven pairs.
Prompt visibility, filesystem scope, inventory scope, fixture execution,
transport, owner action, and authority boundaries all stay clean; the final
Abyss structured arm also matches native dispatch, load, hierarchy, and fixture
contracts. `collision-20`, `collision-33`, `collision-49`, and the Titan pair
now have no failure class. The only remaining aided failures are the
`collision-38` root-only decision trajectory, the `collision-09` explicit-only
approval-gate activation by `aoa-change-protocol`, and the `collision-14` ATM10
overlay displacement by the same generic skill. Preserve the reviewed v14
receipt, repair only `aoa-decision` and `aoa-change-protocol`, and rerun the
smallest affected set before widening.

The first exact-merged six-turn `pilot13-skill-returns` execution closes
`collision-09` and confirms that `collision-38` now gains both the root route
and complete `aoa-decision-find` child trajectory. That decision pair still
misses its source-locked procedure disposition, and its aided exact outcome
command exits zero without exposing the required sentinel output; outcome
verification remains false. `collision-14` gets the manual target route,
procedure, and owner outcome right but still loads repo-visible
`aoa-change-protocol`. Preserve the mixed receipt, repair only those two narrow
source boundaries, and repeat the affected cohort without changing proof
semantics.

The second source repair makes those boundaries literal in prompt-visible
text. `aoa-decision-find` stops with `blocked_missing_input` only when the
permitted boundary supplies neither graph/fallback lookup nor graph and owner
inputs. `aoa-change-protocol` stays unloaded for concrete ATM10 repo-relative
path, local-command, or approval-note requests and does not load the explicit
overlay. The six-turn cohort remains unchanged so the closed approval pair and
the missing aided outcome sentinel are both checked again under fresh transport.

The exact-merged rerun has no aided failure class. The decision pair gains all
four scored axes, ATM10 no longer loads the generic skill and verifies the owner
outcome, and approval remains correct in both arms. The previously missing
aided sentinel is now observed, but the same zero-exit/no-sentinel condition
appears in two controls. Preserve the run as reviewed candidate evidence that
closes the source repair; add explicit observation-gap telemetry before using
those control contrasts in a widened pilot.

V15 records an outcome output-observation gap only when the source-locked exact
command is observed once, exits zero, the validator stays uninspected, and the
required sentinel is absent. The arm outcome remains unverified. Pairs publish
the aided/control flags, `none`, `aided_only`, `control_only`, or `both`, and an
`outcome_lift_observation_clean` marker. Read-only v14 replay labels the two
clean-aided receipt controls `control_only` without rewriting the receipt or
creating a skill failure. Exact-merged full-pilot execution is the next live
step.

That exact-merged v15 full pilot completes all 30 turns and eleven pairs with no
failure class. Five pairs improve route and procedure disposition, including
two positive root-child trajectories; six pairs are already correct in both
arms. Seven outcome pairs are observation-clean and correct in both arms. Two
control-only and two aided-only sentinel gaps make the remaining apparent
outcome lift observation-unclean. Preserve the reviewed receipt, then partition
and contract-complete the 98-turn full-collision and 87-turn coverage-closure
surfaces before sustained execution.

V16 implements that return as an exact partition contract. The five collision
waves and six closure waves have no overlap and reproduce both parents exactly;
each wave is bounded and second-confirmed. Missing implicit contracts now stop
a wave before preflight. The first runnable widening is the 16-turn
`full-collision-core-engineering` wave with all eight procedure and outcome
pairs source-locked. The remaining implicit waves stay plan-visible but
fail-closed until their own contracts are complete; root and structured waves
have no implicit pair dimension and retain separate dispatch, load, hierarchy,
and fixture checks.

The first exact v16 core wave completes 16/16. Every aided arm gains route and
procedure correctness, while six outcome pairs are observation-clean and
correct in both arms. Three fixture commands across `collision-01` and
`collision-02` are observed once and exit zero but expose no output bytes;
their sentinel verification remains false and the public receipt is
`needs-rerun`. Two other outcome contrasts are observation-unclean. The return
cohort therefore repeats only those first two paired cases after exact merge;
it does not relax fixture verification or justify a skill-source change.

That exact fixture return completes 4/4 with no failure class. All fixture and
owner-action probes are observed once, succeed, expose their required
sentinels, and verify; both aided arms retain positive route and procedure
lift, and both outcomes are observation-clean and correct in both arms. This
classifies the earlier fixture failures as observation gaps without changing
skill source. The original `collision-05` and `collision-06` owner-action gaps
remain outside that receipt, so the separate outcome-return cohort repeats
only those two pairs before another collision wave can open.

That exact outcome return also completes 4/4 with no failure class. Every
fixture and owner-action probe for `collision-05` and `collision-06` is
observed once, succeeds, exposes its required sentinel, and verifies. Both
aided arms retain positive route and procedure lift, and both outcomes are
observation-clean and correct in both arms. Together the two paired returns
close all outstanding observation gaps from the first core wave. The next
collision wave now has complete source-authored contract coverage but has not
run live.

`full-collision-safety-overlays` expands both arms of collisions 09-19 and is
complete at 11/11 procedure plus 11/11 owner-action pairs. Manual risk and
project-overlay cases preserve `not_applicable` with explicit owner boundaries;
generic base cases 15 and 17 use `blocked_missing_input` for absent repository
evidence. Six newly cited skill sources enter the plan lock. This packet is
eligible for exact-merged preflight only; contract completeness is not a live
result and does not grant proof or promotion authority.

The exact-merged safety-overlay run completes 22/22 with no failure class or
observation gap. All nine manual pairs are correct in both arms without lift;
the two generic invoke pairs, `collision-15` and `collision-17`, gain positive
aided route plus procedure lift, while their owner-action outcomes remain clean
and correct in both arms. Every fixture and outcome probe is single-attempt,
successful, and verified. The reviewed public receipt remains candidate-only.
The next 28-turn session-growth wave is now source-contract-complete at 14/14
procedure and 14/14 outcome pairs. Eleven explicit or deliberately manual
cases remain `not_applicable`; generic cases 28, 30, and 32 select their base
routes and stop at `blocked_missing_input`. The focused synthetic execution
validates all 28 arms and both receipt schemas. Public receipt validation now
treats `cohort` as a bounded plan slug: interior wording such as
`full-collision-session-growth` is valid, while transport-shaped leading ids
such as `session-deadbeef` remain rejected. Contract readiness is not live
evidence; execute only after exact merge, runtime parity, host gates, and both
confirmations.

That exact-merged execution now completes 28/28 turns and 14/14 pairs. Every
fixture and owner-action probe is single-attempt, successful, observed, and
verified; no output gap, external filesystem access, broad inventory command,
or owner-boundary failure occurs. The receipt is nevertheless
`needs-rerun`: collisions 21, 22, and 25 report the manual target route as
`invoke` while selecting the ambient `aoa-eval` session-mining trajectory, and
collision 33 is classified as a competing-skill win even though its target
route and procedure remain correctly manual and `not_applicable`. Preserve the
full receipt, repair the prompt-visible explicit-only policy and ambient-route
classification, and return only both arms of those four cases.

See `evals/suites/aoa-skill-live-dispatch-harness.suite.md` and
`docs/decisions/AOA-SK-D-0037-source-locked-live-skill-dispatch-evidence.md` for
the evidence and authority boundaries.
