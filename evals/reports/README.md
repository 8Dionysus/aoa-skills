# Local Reports

Store local run or review reports that explain skill-local eval pressure.

Reports here are evidence notes, not central verdicts, scoring, regression, or
proof doctrine. Route central proof adoption to `aoa-evals`.

Active local report notes:

Public-safe live-dispatch receipts may be written here only through the
field-whitelisting review action. Raw receipts remain in the host-private
temporary root and must not be copied into this directory.

- [aoa-skill-live-dispatch-smoke-20260711-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-needs-rerun.json)
  records the reviewed pre-turn strict-config transport failure that opened the
  rollout-budget reminder-list repair loop; it contains no model-quality
  evidence and explicitly requires a rerun.
- [aoa-skill-live-dispatch-smoke-20260711-output-schema-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-output-schema-needs-rerun.json)
  records the reviewed Responses API strict-schema rejection that followed the
  transport repair; the request reached the API but no model output was
  produced, so it also carries no skill-quality evidence.
- [aoa-skill-live-dispatch-smoke-20260711-trajectory-budget-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-trajectory-budget-needs-rerun.json)
  records the first two completed model arms plus the root-child budget stop.
  The implicit pair remains candidate evidence, the structured arm did not run,
  and the full smoke requires a rerun before widening.
- [aoa-skill-live-dispatch-smoke-20260711-classification-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-classification-needs-rerun.json)
  preserves the reviewed four-arm receipt that exposed two classifier defects:
  a valid structured result was overridden by a late budget marker, and the
  expected root was treated as its own collision competitor. Its source-locked
  historical failure labels remain immutable evidence of the old classifier;
  they are not current verdicts, and the corrected harness requires a rerun.
- [aoa-skill-live-dispatch-smoke-20260711-control-contamination-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-control-contamination-needs-rerun.json)
  corrects the interpretation of the complete post-classifier smoke. Later
  `codex debug prompt-input` evidence showed a user-installed target skill in
  the supposed no-skill control and both user and repo copies in the aided arm;
  the run also lacked a uniform executable full-read/procedure path and used an
  ambiguous route/procedure grader. Its former trigger, trajectory, procedure,
  and no-lift labels are harness diagnostics only, not skill-defect evidence.
  The raw receipt remains immutable and a corrected smoke is required.
- [aoa-skill-live-dispatch-smoke-20260711-v2-cli-mcp-config-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-v2-cli-mcp-config-needs-rerun.json)
  records the first protocol-v2 smoke after its 12/12 prompt gate passed. The
  first CLI arm then failed before model spend because per-MCP disable
  overrides synthesized incomplete transport-free tables alongside
  `--ignore-user-config`; it contains adapter evidence only and requires the
  same smoke to be rerun after the CLI isolation repair.
- [aoa-skill-live-dispatch-smoke-20260711-v2-control-budget-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-v2-control-budget-needs-rerun.json)
  records the repaired CLI run in which the aided arm completed exact
  selection, full read, and atomic verification, while the matched control
  legitimately followed the equal-background session-memory route and
  exhausted the former 28k cap on its required owner reads. It publishes no
  pair/lift and requires the same smoke under an equal 48k paired cap.
- [aoa-skill-live-dispatch-smoke-20260711-v2-native-load-contract-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-v2-native-load-contract-needs-rerun.json)
  preserves the complete 48k v2 smoke. Its source-locked implicit
  positive-lift pair is candidate evidence and its root arm exposes a candidate
  missing-child-read gap, but the App arm used unsupported structured-only
  input. Its App `skill_load_gap` is a harness diagnosis, not a skill verdict.
- [aoa-skill-live-dispatch-smoke-20260711-v3-reviewed.json](aoa-skill-live-dispatch-smoke-20260711-v3-reviewed.json)
  records the first complete v3 smoke under its then-current grader. The
  implicit pair has candidate positive lift, the official App invocation passes
  native load, procedure, verification, and completion, and the explicit
  `aoa-eval` root selects
  `aoa-eval-apply` but does not full-read that child before following its
  procedure. The reviewed `skill_load_gap` routes back to the root handoff
  instruction and requires a same-case rerun after repair; it is not central
  proof or promotion evidence. Its fields remain source-locked to the v3
  grader and are not upgraded in place by later evidence semantics.
- [aoa-skill-live-dispatch-smoke-20260711-v3-read-command-ambiguity-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-v3-read-command-ambiguity-needs-rerun.json)
  preserves the exact-merged-tree v3 rerun after the root handoff repair. Its
  first three arms exposed four harness defects: model self-report still gated
  objective load, an implicitly selected child escaped the read check,
  read-only inspection was ambiguous under the "one command" fixture wording,
  and a zero-return output-contract failure was mislabeled as transport
  failure. The report preserves those historical measures without endorsing
  them and supports no pair, lift, skill-effect, or family conclusion. Repeat
  the smoke under v4 before widening.
- [aoa-skill-live-dispatch-smoke-20260711-v4-external-source-contamination-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-v4-external-source-contamination-needs-rerun.json)
  preserves the exact-merged-tree v4 rerun. The aided arm passed objective root
  and dynamic-child reads, but the control read a complete `aoa-eval` source
  file from an external canonical checkout before exhausting 48k. The public
  receipt immutably retains the historical `budget_exhausted` label; reviewed
  private command evidence places the earlier fault at filesystem-scope
  contamination. It supports no pair, lift, skill-effect, or family conclusion
  and requires a v5 fixture-scope rerun.
- [aoa-skill-live-dispatch-smoke-20260711-v5-chunked-read-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260711-v5-chunked-read-needs-rerun.json)
  preserves the exact-merged-tree v5 rerun. Prompt and filesystem scope were
  clean and all four arms completed, but the aided target's complete source was
  read across two ordered exact-path outputs. The v5 single-output detector
  recorded a false `skill_load_gap` and no-lift result. Historical fields stay
  immutable; replay validates only the v6 detector repair, and a fresh
  exact-merged v6 smoke is required before widening.
- [aoa-skill-live-dispatch-smoke-20260712-v6-transport-timeout-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260712-v6-transport-timeout-needs-rerun.json)
  preserves the exact-merged v6 rerun. Prompt visibility and fixture scope
  passed, but the first CLI transport reached its 180-second timeout before any
  turn event, output, usage, or pair. The private receipt stopped early while
  the historical v6 command still exited zero. This is transport and CLI-status
  evidence only; repeat after runtime availability under exact-merged v7.
- [aoa-skill-live-dispatch-smoke-20260712-v7-reviewed-route-lift.json](aoa-skill-live-dispatch-smoke-20260712-v7-reviewed-route-lift.json)
  preserves the complete exact-merged v7 smoke as reviewed candidate evidence.
  All four arms completed with clean prompt, fixture, load, procedure, and
  safety gates. Its generic `observed_lift=1` was derived only from
  route-contract correctness, so review accepts positive route lift and
  explicitly rejects completion or outcome-lift interpretation. V8 must repeat
  the same smoke with a pre-authored source-locked bounded outcome contract.
- [aoa-skill-live-dispatch-smoke-20260712-v8-outcome-answer-key-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260712-v8-outcome-answer-key-needs-rerun.json)
  preserves the complete exact-merged v8 smoke and its historical source-locked
  grader output: positive route lift, negative outcome lift, and one
  `bounded_outcome_miss`. Review returned to the source contract and found that
  its key expected deflection of the unavailable whole repository task even
  though the constrained output and fixture define the scored disposition for
  the exact downstream procedure. The aided arm completed and verified that
  fixture procedure while separately preserving external owner stop-lines.
  The recorded negative outcome is therefore answer-key pressure, not a skill
  verdict. V9 attempted a narrower scope; the next smoke exposed the remaining
  child/probe conflation now superseded by v10.
- [aoa-skill-live-dispatch-smoke-20260712-v9-child-route-native-dispatch-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260712-v9-child-route-native-dispatch-needs-rerun.json)
  preserves the complete exact-merged v9 smoke. Its aided arm selected and
  fully read `aoa-eval-select`, ran the fixture probe, and reported the missing
  target-repository evidence; its structured arm accepted official
  `aoa-eval-apply` input and completed the probe but reported the equivalent
  root-child hierarchy. V9 recorded outcome no-lift and
  `dispatch_policy_gap`; v10 source review shows both are harness semantics, not
  skill defects. Replay yields route `+1`, trajectory `+1`,
  procedure-disposition `0` with both reports correct, and objective outcome
  unscored. The historical v9 fields remain immutable; the exact-merged v10
  attempts are retained next.
- [aoa-skill-live-dispatch-smoke-20260712-v10-aided-inventory-budget-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260712-v10-aided-inventory-budget-needs-rerun.json)
  preserves the first exact-merged v10 attempt. Prompt, filesystem, storage,
  resource, and runtime gates passed, but the aided arm broadly enumerated the
  hidden fixture, read `aoa-eval-local-need`, and exhausted 48k before a final
  output, probe result, or pair. It is incomplete harness-pressure evidence,
  not a route or skill verdict.
- [aoa-skill-live-dispatch-smoke-20260712-v10-repeat-inventory-budget-needs-rerun.json](aoa-skill-live-dispatch-smoke-20260712-v10-repeat-inventory-budget-needs-rerun.json)
  preserves the unchanged v10 repeat. The implicit pair completed with
  positive route lift, zero trajectory lift, zero procedure-disposition lift,
  and objective outcome unscored; its aided arm selected
  `aoa-eval-local-need`. The root arm then exhausted 48k after broad listing
  and fixture-tree hashing, so the cohort stopped at three of four turns. The
  candidate trajectory observation remains reviewable, but the incomplete
  cohort and repeated inventory pressure require v11 harness repair and a
  fresh exact-merged rerun before skill interpretation.
- [aoa-skill-live-dispatch-smoke-20260712-v11-reviewed-route-trajectory-lift.json](aoa-skill-live-dispatch-smoke-20260712-v11-reviewed-route-trajectory-lift.json)
  preserves the complete exact-merged v11 smoke. All four arms completed with
  no failure class, external path access, or broad fixture inventory. The
  implicit pair reports route lift `+1`, source-locked selected-child
  trajectory lift `+1`, procedure-disposition lift `0` with both arms correct,
  and no objective outcome score. Direct root-to-child and official structured
  activation also passed their bounded contracts. This is reviewed candidate
  evidence only; it neither proves family-wide effectiveness nor authorizes
  pilot widening, proof acceptance, or promotion.
- [aoa-skill-live-dispatch-smoke-20260712-v12-reviewed-owner-action-no-lift.json](aoa-skill-live-dispatch-smoke-20260712-v12-reviewed-owner-action-no-lift.json)
  preserves the complete exact-merged v12 smoke that first exercised the
  separate owner-action outcome contract. All four arms completed without
  failure; route and selected-child trajectory lift are `+1`, while procedure
  disposition and the one-attempt outcome are correct in both arms (`0` lift).
  The receipt validates observability and anti-inspection boundaries only; it
  does not prove skill-specific outcome lift, whole-task completion, or pilot
  readiness beyond the still-incomplete 1/11 plus 1/11 coverage posture.
- [aoa-skill-live-dispatch-pilot13-20260712-v12-reviewed-mixed-returns-needs-rerun.json](aoa-skill-live-dispatch-pilot13-20260712-v12-reviewed-mixed-returns-needs-rerun.json)
  preserves the first complete exact-merged 30-turn pilot after both source
  coverage gates reached 11/11. All transport, prompt, filesystem, inventory,
  fixture, owner-action, and authority boundaries stayed clean, and every
  owner-action pair was correct in both arms. The receipt remains
  `needs-rerun` because review separated real manual-policy collision pressure
  from premature child/procedure expectations, ambient-control failure
  overclassification, and one valid overlay-to-base hierarchy that the
  structured report grader did not recognize. It is an adaptive-return map,
  not a negative family verdict. Later source reread keeps the
  `aoa-decision-find` expectation as a root-handoff candidate; v13 replay
  corrects only the ambient-control, no-dispatch prompt, and overlay hierarchy
  grader pressure without rewriting this v12 receipt.
- [aoa-skill-live-dispatch-pilot13-returns-20260712-v13-reviewed-partial-transport-needs-rerun.json](aoa-skill-live-dispatch-pilot13-returns-20260712-v13-reviewed-partial-transport-needs-rerun.json)
  preserves the first exact-merged bounded rerun. It stopped after 6 of 15
  turns when the `collision-33` control transport reached the source-locked
  180-second cap after turn start. Earlier prompt, filesystem, inventory, and
  owner-action gates were clean. This is partial transport evidence, not a
  completed pair verdict or a reason to widen the timeout.
- [aoa-skill-live-dispatch-pilot13-returns-20260712-v13-reviewed-partial-output-contract-needs-rerun.json](aoa-skill-live-dispatch-pilot13-returns-20260712-v13-reviewed-partial-output-contract-needs-rerun.json)
  preserves the fresh exact-source rerun that passed the earlier timeout point
  and reached 14 of 15 turns. Titan control then reported no selected skill
  together with `claims_loaded=true`, so the output contract correctly stopped
  the cohort before the final Abyss structured arm. The completed arms expose
  both real repo-skill collision pressure and remaining ambient/procedure
  grader ambiguity; the receipt remains candidate-only `needs-rerun` evidence.
- [aoa-skill-live-dispatch-pilot13-returns-20260712-v14-reviewed-complete-skill-returns-needs-rerun.json](aoa-skill-live-dispatch-pilot13-returns-20260712-v14-reviewed-complete-skill-returns-needs-rerun.json)
  preserves the first complete exact-merged v14 return: all 15 turns and seven
  pairs completed with prompt, filesystem, inventory, fixture, transport,
  owner, and authority boundaries clean. The corrected Abyss structured arm,
  both external ambient routes, the earlier timeout case, and Titan now pass.
  Three aided failures remain: `aoa-decision` stops before the required
  `aoa-decision-find` child, while `aoa-change-protocol` is selected once for an
  explicit-only approval-gate classification and once instead of the ATM10
  project overlay. This `needs-rerun` receipt narrows source repair to those two
  skills and requires the smallest affected rerun; it grants no proof or
  promotion authority.
- [aoa-skill-live-dispatch-pilot13-skill-returns-20260712-v14-reviewed-mixed-source-and-observation-returns-needs-rerun.json](aoa-skill-live-dispatch-pilot13-skill-returns-20260712-v14-reviewed-mixed-source-and-observation-returns-needs-rerun.json)
  preserves the first exact-merged six-turn source-return execution. It closes
  `collision-09`, confirms positive route and `aoa-decision-find` trajectory
  lift for `collision-38`, and narrows the remaining source work to that
  child's missing-input disposition plus the concrete ATM10 exclusion in
  `aoa-change-protocol`. The aided decision outcome command exits zero but
  exposes no required sentinel bytes, so objective outcome verification remains
  false. This mixed `needs-rerun` receipt grants no proof or promotion authority.
- [aoa-skill-live-dispatch-pilot13-skill-returns-20260712-v14-reviewed-clean-aided-returns-control-observation-gap.json](aoa-skill-live-dispatch-pilot13-skill-returns-20260712-v14-reviewed-clean-aided-returns-control-observation-gap.json)
  preserves the exact-merged rerun after the second source repair and verified
  runtime import. All aided arms have no failure class: the decision pair gains
  route, full child trajectory, procedure, and verified outcome; ATM10 keeps
  both generic and explicit overlay skills unloaded and verifies the owner
  route; approval stays correct in both arms. Two controls execute the exact
  outcome command once with exit zero but expose no sentinel bytes. The receipt
  therefore closes the aided source returns as reviewed candidate evidence but
  reserves control-lift interpretation for explicit observation-gap telemetry;
  it grants no proof or promotion authority.
- [aoa-skill-live-dispatch-pilot13-20260712-v15-reviewed-clean-routing-observation-qualified-outcomes.json](aoa-skill-live-dispatch-pilot13-20260712-v15-reviewed-clean-routing-observation-qualified-outcomes.json)
  preserves the complete exact-merged v15 pilot after the observation-gap
  telemetry repair. All 30 turns and 11 pairs complete with zero safety or
  failure class; five pairs gain route and procedure correctness and two gain
  selected-child trajectory correctness. Seven outcome comparisons are
  observation-clean and correct in both arms. The remaining four comparisons
  have a single missing-sentinel arm despite one successful exact command, so
  their two positive and two negative raw outcome lifts are explicitly
  observation-unclean and support no skill-effect interpretation. This is
  reviewed candidate evidence only and grants no proof or promotion authority.
- [aoa-skill-live-dispatch-full-collision-core-engineering-20260712-v16-reviewed-fixture-output-observation-gaps-needs-rerun.json](aoa-skill-live-dispatch-full-collision-core-engineering-20260712-v16-reviewed-fixture-output-observation-gaps-needs-rerun.json)
  preserves the first exact-merged bounded core-engineering wave. All sixteen
  turns and eight pairs complete, and every aided arm gains route plus
  procedure correctness. Six outcomes are observation-clean and correct in
  both arms; `collision-05` and `collision-06` have opposite single-arm outcome
  observation gaps. Three fixture probes also run once and exit zero but expose
  zero captured output, so their sentinel verification remains false and the
  receipt retains `fixture_execution_gap`. This is candidate
  `needs-rerun` evidence; repeat only both arms of `collision-01` and
  `collision-02` without changing skill source or verification rules.
- [aoa-skill-live-dispatch-full-collision-core-engineering-returns-20260712-v16-reviewed-clean.json](aoa-skill-live-dispatch-full-collision-core-engineering-returns-20260712-v16-reviewed-clean.json)
  preserves that exact-merged four-turn paired fixture return. All four arms
  complete with zero failure classes; every fixture and owner-action command
  is observed once, succeeds, exposes its sentinel, and verifies. Both pairs
  retain positive aided route and procedure lift with observation-clean,
  both-correct outcomes. This closes only the `collision-01`/`collision-02`
  fixture return as reviewed candidate evidence. It does not rewrite the first
  receipt, resolve its separate `collision-05`/`collision-06` outcome gaps, or
  grant proof or promotion authority.
- [aoa-skill-live-dispatch-full-collision-core-engineering-outcome-returns-20260712-v16-reviewed-clean.json](aoa-skill-live-dispatch-full-collision-core-engineering-outcome-returns-20260712-v16-reviewed-clean.json)
  preserves the exact-merged four-turn paired owner-action return. All four
  `collision-05` and `collision-06` arms complete with zero failure classes;
  each fixture and owner-action command is observed once, succeeds, exposes
  its sentinel, and verifies. Both pairs retain positive aided route and
  procedure lift with observation-clean, both-correct outcomes. Together with
  the fixture return, this closes all outstanding core-wave observation gaps
  as reviewed candidate evidence without granting proof or promotion authority.

Corrected live receipts under the v11-v16 evidence protocols are reviewable only
after canonical user-skill shadows, plugins, and every configured MCP id are
isolated with the adapter-appropriate mechanism (`--ignore-user-config` for
CLI exec, explicit per-id disables for prompt inspection and App Server);
prompt entry descriptions match the locked background; structured
`skills/list` exposes the exact unique 57-skill fixture map with zero MCP
startup; the official `$skill` text plus matching `skill` item is accepted;
native input acceptance remains separate from exact fixture-path full reads;
model `claims_loaded` stays separate from objective load; every expected or
dynamically selected child has a complete exact-path read; read-only inspection
commands remain load evidence separate from the fixture probe; one complete
output or ordered continuously covering source chunks can prove that read,
while overlaps are accepted and gaps, reverse-only coverage, unrelated output,
inventory mentions, and shadow paths remain insufficient; zero-return
output-contract invalidity remains separate from transport failure; every
model command remains within the fixture root, with external or parent-path
access classified as contamination before budget; broad internal enumeration,
recursive listing, and tree hashing are separately rejected before budget while
exact route-required reads remain allowed; one atomic
guidance-bound validator event is proved; caught transport exceptions preserve
elapsed duration and partial private stdout/stderr so recoverable events retain
their normal precedence; incomplete stopped-early cohorts return nonzero after
their private receipt is written, while complete negative cohorts remain valid
executions; and invalid pairs are
omitted without rewriting arm history. Public v11 pairs name route,
selected-child trajectory, and selected-procedure-disposition report lift
separately. Fixture execution is its own contract. Objective outcome lift is
`not_scored_no_observable_outcome` until an owner-bound observable surface
exists; the probe and model report never become their own grader. Public
validation rejects embedded absolute host paths as well as raw prompts,
transport ids, and credential-shaped values. Canonical repo skill names remain
public only in schema-typed skill-name fields, so names such as
`aoa-session-donor-harvest` do not become false transport-id leaks. Retained v1/v2 smokes remain
historical `needs-rerun` evidence; retained v3-v10 reports keep their original
review status and grader semantics, including v4's budget label and v5's
single-output read label, while v6 keeps its zero-duration and wrapper-success
history, v7 keeps its generic route-derived lift, v8 keeps its invalid answer
key, v9 keeps its child/probe/native-dispatch conflation, and both v10 attempts
keep their incomplete inventory/budget observations rather than being
rewritten in place.
- [aoa-eval-session-mining.report.md](aoa-eval-session-mining.report.md)
  records the first `.aoa` mining pass for `aoa-eval` trigger evidence and its
  proof limits.
- [aoa-eval-runtime-adoption-20260621.report.md](aoa-eval-runtime-adoption-20260621.report.md)
  records the local Codex runtime-adoption smoke for the `aoa-eval` front-door
  skill.
- [aoa-eval-self-awareness-contract-lane.report.md](aoa-eval-self-awareness-contract-lane.report.md)
  applies existing central eval surfaces to the `abyss-machine`
  self-awareness contract-lane episode as a local dogfood readout.
- [aoa-eval-battle-path-20260621.report.md](aoa-eval-battle-path-20260621.report.md)
  records an end-to-end local eval-port route through `aoa-evals-mcp`,
  `aoa-eval-apply`, deterministic skill checks, session refs, and post-write
  validation.
- [aoa-eval-prompt-trigger-harness-20260625.report.md](aoa-eval-prompt-trigger-harness-20260625.report.md)
  records the focused deterministic prompt-trigger harness for `aoa-eval`
  route correctness across front-door, subskill, negative, and owner-boundary
  cases.
